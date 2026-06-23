#!/usr/bin/env python3
"""引用查證器：把草稿書目丟進來，回傳「權威」的作者/標題/卷期頁，並標出不符之處。

專治最常見的引用幻覺：**張冠李戴**——標題搜對了，作者卻是從記憶塞進去的（常是該領域更有名的人）。
本工具不靠記憶：每筆都向 Crossref / doi.org 取回真實 metadata，逐欄比對，讓作者不符「現形」。

⚠ 設計原則（經跨 AI 檢核後修正）：
- **絕不把「連不上」當成「捏造」**。網路/SSL/限流/逾時 → `NETWORK_ERROR`，要求重試，**不可據此刪文獻**。
- `DOI_INVALID` 只用於 doi.org handle API **確認不存在**的 DOI。
- 作者比對採**正規化、第一作者、token 精確比對**（不再用子字串），避免「Li 命中 Williams」誤判與放行張冠李戴。
- 作者無法自動確認（中文、或權威 metadata 無作者、或未提供作者）→ **不給 VERIFIED**，標需人工。

用法:
    python3 verify_refs.py refs.json          # refs.json 為陣列
    echo '[{...}]' | python3 verify_refs.py - # 從 stdin 讀

輸入每筆物件欄位（皆可選，但至少要有 title 或 doi）:
    {"id":"W7-1", "authors":"林照真", "year":2021,
     "title":"社交媒體假訊息的操作模式初探：以兩個臺灣政治傳播個案為例",
     "journal":"中華傳播學刊", "doi":"10.3966/172635812021060039001"}

判讀（verdict）:
    VERIFIED            標題＋第一作者姓相符（年份若兩邊都有則一併比對）→ 可標 ✅（仍建議人工掃一眼）
    AUTHOR_MISMATCH     標題相符，但第一作者對不上（疑似張冠李戴）→ 改用權威作者，標 ❓  [嚴重]
    AUTHOR_UNVERIFIED   文獻存在，但作者無法自動確認（中文/權威無作者/未提供作者）→ 抓原頁讀作者，標 ❓
    YEAR_MISMATCH       標題相符但年份不符 → 改用權威年份
    TITLE_DOI_MISMATCH  DOI 真實可解析，但你給的標題對不上 → DOI 指向另一篇，務必核對  [嚴重]
    DOI_INVALID         DOI 經 handle API 確認不存在 → 高度疑似捏造，移除  [嚴重]
    NOT_IN_CROSSREF     Crossref 無候選（中文期刊/專書/新聞常如此）→ 非等於不存在，走人工分支
    NETWORK_ERROR       網路/SSL/限流/逾時，未完成查證 → 重試；**切勿據此判為捏造或刪除**
    INPUT_INVALID       既無 title 也無 doi → 無法查
    PARTIAL             標題中等相似 → 標 ❓ 人工確認
    ERROR               該筆處理時發生例外（已隔離，不影響其他筆）

退出碼: 0 全部 VERIFIED；2 有「嚴重」(AUTHOR_MISMATCH/TITLE_DOI_MISMATCH/DOI_INVALID)；3 有其他需人工項。

僅用標準函式庫（urllib），無需安裝套件。Crossref 禮貌池 User-Agent 已內建。
"""
import json
import re
import socket
import ssl
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher

UA = "course-syllabus-skill/1.1 (mailto:jay8956047@gmail.com)"
CR_WORK = "https://api.crossref.org/works/"
CR_QUERY = "https://api.crossref.org/works"
HANDLE_API = "https://doi.org/api/handles/"

SEVERE = {"AUTHOR_MISMATCH", "TITLE_DOI_MISMATCH", "DOI_INVALID"}


def _ssl_ctx():
    """macOS 上系統 python 常缺 CA 根憑證；優先用 certifi，否則退回系統預設。"""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


_CTX = _ssl_ctx()


def _fetch(url, accept="application/json", timeout=25, retries=2):
    """回 (status, body, errkind)。errkind: None=成功 / 'notfound'=確認404 / 'network'=連不上或限流。

    關鍵：嚴格區分「確認不存在(404/410)」與「基礎設施失敗」——後者絕不可當成不存在。
    """
    last = "network"
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
                return r.status, r.read().decode("utf-8", "replace"), None
        except urllib.error.HTTPError as e:
            try:
                ebody = e.read().decode("utf-8", "replace")
            except Exception:
                ebody = None
            # 404/410 仍回傳 body：doi.org handle API 對不存在的 handle 是「404 + responseCode 100」
            if e.code in (404, 410):
                return e.code, ebody, "notfound"
            # 429 / 5xx 為暫時性 → 重試；4xx 其他（401/403）無法判定 → network
            if e.code in (429, 500, 502, 503, 504):
                last = "network"
            else:
                return e.code, ebody, "network"
        except (urllib.error.URLError, ssl.SSLError, socket.timeout, TimeoutError, ConnectionError):
            last = "network"
        except Exception:
            last = "network"
        if attempt < retries:
            time.sleep(0.6 * (attempt + 1))
    return None, None, last


def norm(s: str) -> str:
    """正規化標題：NFKC（全半形統一）、去標點與空白、轉小寫，保留中英數字。"""
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[\s　]+", "", s)
    s = re.sub(r"[^\w一-鿿]", "", s)
    return s


def title_sim(a: str, b: str) -> float:
    return round(SequenceMatcher(None, norm(a), norm(b)).ratio(), 3)


def provided_first_tokens(author_str: str):
    """回 (第一作者姓氏的正規化 token 集合, is_cjk)。無法取得回 (set(), True)。

    兩側都 token 化、用交集比對，能容忍複姓/連字號/小品詞姓（Müller-Lyer、van der Berg），
    又因為是 token 相等（非子字串）不會「Li 命中 Williams」。
    """
    if not author_str:
        return set(), True
    first = re.split(r"[、,，;；&]|\band\b|等", author_str.strip(), flags=re.I)[0].strip()
    if not first:
        return set(), True
    if re.search(r"[一-鿿]", first):
        return set(), True  # 中文無法跨羅馬拼音自動比對
    # "Family, Given" → 取逗號前；其餘整段 token 化（去掉單字母縮寫）
    chunk = first.split(",")[0] if "," in first else first
    return {t for t in norm_name(chunk).split() if len(t) >= 2}, False


def cr_authors(item: dict):
    """Crossref / CSL author → 顯示字串 + family 名 token 集合（小寫）。"""
    disp, fam_tokens = [], set()
    for a in item.get("author", []) or []:
        fam = (a.get("family") or "").strip()
        giv = (a.get("given") or "").strip()
        name = (a.get("name") or "").strip()
        if fam:
            disp.append(f"{fam}, {giv}".strip(", "))
            fam_tokens.update(norm_name(fam).split())
        elif name:
            disp.append(name)
            fam_tokens.update(norm_name(name).split())
    return disp, fam_tokens


def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"[^\w\s]", " ", s)


def author_match(provided: str, fam_tokens):
    """第一作者姓氏 token 交集比對。True/False/None(中文或無法比對→需人工)。

    注意：本檢查只驗『第一作者姓』；換掉非第一作者的張冠李戴本工具偵測不到（見 docstring 限縮）。
    """
    toks, is_cjk = provided_first_tokens(provided)
    if is_cjk or not toks:
        return None            # 中文無法跨羅馬拼音自動比對；未提供作者亦回 None
    if not fam_tokens:
        return None            # 權威 metadata 無作者
    return bool(toks & fam_tokens)  # token 交集，容忍複姓、避免子字串誤判


def _year_from(item: dict):
    for key in ("issued", "published-print", "published-online", "published", "created"):
        dp = (item.get(key) or {}).get("date-parts") if isinstance(item.get(key), dict) else None
        if dp and dp[0] and dp[0][0]:
            return dp[0][0]
    return None


def from_item(item: dict) -> dict:
    disp, fam_tokens = cr_authors(item)
    title = item.get("title")
    if isinstance(title, list):
        title = title[0] if title else ""
    cont = item.get("container-title")
    if isinstance(cont, list):
        cont = cont[0] if cont else ""
    return {
        "title": title or "",
        "authors": disp,
        "_fams": fam_tokens,
        "journal": cont or "",
        "year": _year_from(item),
        "volume": item.get("volume", ""),
        "issue": item.get("issue", ""),
        "page": item.get("page", ""),
        "doi": item.get("DOI") or item.get("doi", ""),
        "publisher": item.get("publisher", ""),
    }


def clean_doi(doi: str) -> str:
    """正規化 DOI 輸入：去掉 doi:／https://(dx.)doi.org/ 前綴、大小寫 host、前後雜訊。"""
    doi = (doi or "").strip()
    doi = re.sub(r"(?i)^\s*doi:\s*", "", doi)
    doi = re.sub(r"(?i)^https?://(dx\.)?doi\.org/", "", doi)
    m = re.search(r"10\.\d{4,9}/\S+", doi)
    return m.group(0).rstrip(").,;") if m else doi


def resolve_doi(doi: str):
    """回 (source, auth)。source ∈ crossref|doi.org|resolves|notfound|network。

    **fail-safe 原則：唯一能判 `notfound`（→DOI_INVALID）的權威來源是 doi.org handle API 的 responseCode
    (100/200=不存在)。** 其餘任何拿不到結論的情況（解析失敗、未知 rc、HTTP 404、連線問題）一律回 `network`，
    寧可標「未完成查證」也不誤判捏造而誘導刪除真實文獻。
    """
    doi = clean_doi(doi)
    # 1) Crossref（英文文獻 metadata 最完整）
    st, body, err = _fetch(CR_WORK + urllib.parse.quote(doi))
    if body and st == 200:
        try:
            return "crossref", from_item(json.loads(body)["message"])
        except Exception:
            pass
    # 2) doi.org content negotiation（DataCite/mEDRA 等）
    st, body, err = _fetch("https://doi.org/" + urllib.parse.quote(doi),
                           accept="application/vnd.citationstyles.csl+json")
    if body and st == 200:
        try:
            return "doi.org", from_item(json.loads(body))
        except Exception:
            pass
    # 3) handle API：唯一的權威存在性判定。對不存在的 handle 是「HTTP 404 + responseCode 100」，
    #    故不論 200/404 都要解析 body 的 responseCode（1=存在, 100/200=確認不存在）。
    st, body, err = _fetch(HANDLE_API + urllib.parse.quote(doi))
    if body:
        try:
            rc = json.loads(body).get("responseCode")
            if rc == 1:
                return "resolves", None       # 真實存在但無機讀 metadata（如華藝中文期刊）
            if rc in (100, 200):
                return "notfound", None        # 權威確認不存在
        except Exception:
            pass
    # 拿不到權威結論 → 一律 network（fail-safe，不誤判捏造）
    return "network", None


def query_crossref(title: str, authors: str):
    """回 (candidates, errkind)。"""
    q = urllib.parse.urlencode({"query.bibliographic": f"{title} {authors}".strip(), "rows": 5})
    st, body, err = _fetch(f"{CR_QUERY}?{q}")
    if body and st == 200:
        try:
            items = json.loads(body)["message"].get("items", [])
            return [from_item(i) for i in items], None
        except Exception:
            return [], "network"
    return [], err or "network"


def _build(res, verdict, auth=None, sim=None, amatch=None, year_ok=None, note=None):
    res["verdict"] = verdict
    if sim is not None:
        res["title_similarity"] = sim
    res["author_auto_match"] = amatch
    if year_ok is not None:
        res["year_match"] = year_ok
    if auth is not None:
        res["authoritative"] = {k: auth[k] for k in
                                ("title", "authors", "journal", "year", "volume", "issue", "page", "doi", "publisher")}
    if note:
        res["note"] = note
    return res


def grade(ref, auth, source, res):
    prov_title = ref.get("title", "")
    sim = title_sim(prov_title, auth["title"]) if prov_title else None
    amatch = author_match(ref.get("authors", ""), auth["_fams"])
    yr_ref, yr_auth = ref.get("year"), auth.get("year")
    year_ok = (str(yr_ref) == str(yr_auth)) if (yr_ref is not None and yr_auth is not None) else None

    doi_path = source in ("crossref", "doi.org") and ref.get("doi")
    # DOI 真但標題對不上 → 指向另一篇（嚴重）
    if doi_path and sim is not None and sim < 0.55:
        return _build(res, "TITLE_DOI_MISMATCH", auth, sim, amatch, year_ok,
                      f"⚠ DOI 可解析但你給的標題對不上（相似度 {sim}）。此 DOI 指向：「{auth['title']}」。請核對是否貼錯 DOI 或張冠李戴。")
    # query 模式最佳候選太弱 → 非「不存在」，而是 Crossref 無此筆
    if not doi_path and (sim is None or sim < 0.55):
        return _build(res, "NOT_IN_CROSSREF", None, sim, None, None,
                      "Crossref 找不到夠相似的候選。中文期刊/專書/新聞常如此，**不等於不存在**；請用 firecrawl/WebFetch 走人工查證。")
    if amatch is False:
        return _build(res, "AUTHOR_MISMATCH", auth, sim, amatch, year_ok,
                      f"⚠ 疑似張冠李戴：標題相符但第一作者對不上。權威作者＝{auth['authors']}。請改用權威作者並標 ❓。")
    if year_ok is False:
        return _build(res, "YEAR_MISMATCH", auth, sim, amatch, year_ok,
                      f"年份不符：權威年份＝{auth.get('year')}。請改用權威年份。")
    if amatch is None:
        if not auth.get("authors"):
            note = ("⚠ 標題/期刊已確認存在，但機讀 metadata 不含作者（華藝等中文期刊常見）。"
                    "張冠李戴最常發生在這裡：務必用 firecrawl/WebFetch 抓該文章頁讀出『真實作者』，"
                    "絕不可沿用記憶或輸入的作者；確認前標 ❓。")
        else:
            note = (f"作者無法自動比對（中文需跨羅馬拼音，或未提供作者）。權威作者＝{auth['authors']}。"
                    "請人工核對作者後再定 ✅；未確認前標 ❓。")
        return _build(res, "AUTHOR_UNVERIFIED", auth, sim, amatch, year_ok, note)
    # amatch True
    if prov_title is None or prov_title == "" or sim >= 0.8:
        note = None
        if year_ok is None:
            note = "已驗：第一作者姓相符；但年份未能比對（一方缺年份），請順手確認年份。"
        elif not prov_title:
            note = "已驗：DOI 解析且第一作者姓相符；未提供標題故未比對標題。"
        return _build(res, "VERIFIED", auth, sim, amatch, year_ok, note)
    return _build(res, "PARTIAL", auth, sim, amatch, year_ok,
                  f"標題僅中等相似（{sim}），請人工確認是否同一篇。")


def process(ref: dict) -> dict:
    res = {"id": ref.get("id", "?"),
           "input": {k: ref.get(k) for k in ("authors", "year", "title", "journal", "doi")}}
    try:
        has_doi = bool(ref.get("doi"))
        has_title = bool(ref.get("title"))
        if not has_doi and not has_title:
            return _build(res, "INPUT_INVALID", note="此筆既無 title 也無 doi，無法查證。")

        if has_doi:
            source, auth = resolve_doi(ref["doi"])
            if source == "network":
                return _build(res, "NETWORK_ERROR", note="網路/SSL/限流/逾時，未完成查證。請稍後重試；**切勿據此判為捏造或刪除文獻**。")
            if source == "notfound":
                return _build(res, "DOI_INVALID", note="DOI 經 doi.org handle API 確認不存在 → 高度疑似捏造，移除該 DOI 或整筆。")
            if source == "resolves":
                return _build(res, "AUTHOR_UNVERIFIED", note=(
                    "DOI 真實可解析至出版商，但 metadata 無法機讀（如華藝 10.3966 中文期刊）。"
                    "務必用 firecrawl/WebFetch 抓該頁逐欄謄寫並『人工核對作者』；確認前標 ❓，勿當已驗證。"))
            return grade(ref, auth, source, res)

        cands, err = query_crossref(ref.get("title", ""), ref.get("authors", ""))
        if err == "network":
            return _build(res, "NETWORK_ERROR", note="Crossref 查詢失敗（網路/限流）。請重試；**切勿據此判為不存在或刪除**。")
        if not cands:
            return _build(res, "NOT_IN_CROSSREF", note="Crossref 無候選。中文期刊/專書/新聞常如此，非等於不存在；請走人工分支。")
        best = max(cands, key=lambda c: title_sim(ref.get("title", ""), c["title"]))
        return grade(ref, best, "crossref-query", res)
    except Exception as e:
        return _build(res, "ERROR", note=f"處理此筆時發生例外（已隔離）：{type(e).__name__}: {e}")


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write(__doc__)
        return 1
    try:
        raw = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
        refs = json.loads(raw)
    except FileNotFoundError:
        sys.stderr.write(f"找不到輸入檔：{sys.argv[1]}\n")
        return 1
    except json.JSONDecodeError as e:
        sys.stderr.write(f"輸入不是合法 JSON：{e}\n")
        return 1
    if isinstance(refs, dict):
        refs = [refs]

    results = []
    for ref in refs:
        if not isinstance(ref, dict):
            results.append({"id": "?", "verdict": "INPUT_INVALID", "note": "此筆不是物件，已略過。"})
            continue
        results.append(process(ref))
        time.sleep(0.34)  # 對 Crossref 友善

    print(f"{'ID':<8} {'VERDICT':<18} {'sim':<6} {'作者比對':<8} 權威作者 / 備註")
    print("-" * 104)
    has_severe = has_manual = False
    for r in results:
        v = r["verdict"]
        auth = r.get("authoritative", {})
        am = {True: "✓符", False: "✗不符", None: "需人工"}.get(r.get("author_auto_match"), "-")
        info = auth.get("authors") or r.get("note", "")
        if isinstance(info, list):
            info = "; ".join(info)
        print(f"{r['id']:<8} {v:<18} {str(r.get('title_similarity','-')):<6} {am:<8} {str(info)[:62]}")
        if v in SEVERE:
            has_severe = True
        elif v != "VERIFIED":
            has_manual = True

    if sys.argv[1] != "-":
        out_path = sys.argv[1] + ".verified.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n權威 metadata 已寫出：{out_path}")
        print("→ 請『只從這份輸出謄寫』書目欄位（尤其作者），不要從記憶補。")
    print("提醒：NETWORK_ERROR / NOT_IN_CROSSREF 代表『未完成查證』，不是『不存在』——勿據此刪除文獻。")
    return 2 if has_severe else (3 if has_manual else 0)


if __name__ == "__main__":
    sys.exit(main())
