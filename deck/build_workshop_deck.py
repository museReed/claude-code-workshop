#!/usr/bin/env python3
"""Ad-hoc slide-builder run: 04-口述腳本.md -> reveal.js deck.
Applies the designed pipeline manually: archetypes + KCL theme + inline SVG
diagrams + inline Lucide icons (offline, themeable) + speaker notes + one chart.
Run: python3 build_workshop_deck.py   ->  workshop-deck.html
"""
import re, pathlib
IC = pathlib.Path("/tmp/ic")
INNER = {}
for f in IC.glob("*.svg"):
    t = f.read_text(encoding="utf-8")
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    m = re.search(r"<svg[^>]*>(.*)</svg>", t, flags=re.S)
    INNER[f.stem] = m.group(1).strip() if m else ""

def ic(name):
    return (f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{INNER.get(name,"")}</svg>')

def notes(**kw):
    parts = []
    if kw.get("time"): parts.append(f"⏱ {kw['time']}")
    if kw.get("hook"): parts.append(f"🪝 Hook：{kw['hook']}")
    if kw.get("points"): parts.append("🔑 " + "／".join(kw["points"]))
    if kw.get("say"): parts.append(f"🎤 {kw['say']}")
    if kw.get("analogy"): parts.append(f"🌰 {kw['analogy']}")
    if kw.get("warn"): parts.append(f"⚠️ {kw['warn']}")
    if kw.get("transition"): parts.append(f"→ {kw['transition']}")
    return "<aside class='notes'>" + "\n\n".join(parts) + "</aside>"

S = []  # slides

def section(title, eyebrow, lead="", **n):
    S.append(f"""<section data-background-color="#0E1A2F" class="dark">
      <div class="eyebrow">● {eyebrow}</div><h2>{title}</h2>
      {f'<p class="lede">{lead}</p>' if lead else ''}{notes(**n)}</section>""")

def concept(title, eyebrow, lead, points, icon=None, analogy="", **n):
    pts = "".join(f"<li>{p}</li>" for p in points)
    icon_h = f'<div class="c-icon">{ic(icon)}</div>' if icon else ''
    an = f'<div class="analogy">🌰 {analogy}</div>' if analogy else ''
    S.append(f"""<section data-background-color="#FBFBFD">
      <div class="eyebrow">● {eyebrow}</div><h2>{title}</h2>
      <div class="c-body">{icon_h}<div><p class="lede">{lead}</p><ul class="pts">{pts}</ul>{an}</div></div>
      {notes(**n)}</section>""")

def vocab(title, eyebrow, terms, **n):
    cards = "".join(
        f'<div class="vc"><div class="vc-h">{ic(i)}<span>{t}</span></div><div class="vc-d">{d}</div></div>'
        for t, d, i in terms)
    S.append(f"""<section data-background-color="#FBFBFD">
      <div class="eyebrow">● {eyebrow}</div><h2>{title}</h2>
      <div class="vgrid">{cards}</div>{notes(**n)}</section>""")

def tiers(title, eyebrow, rows, **n):
    body = "".join(
        f'<div class="tier {cls}"><span class="t-badge">{b}</span><span class="t-name">{nm}</span>'
        f'<span class="t-cost">{cost}</span><span class="t-use">{use}</span></div>'
        for b, nm, cost, use, cls in rows)
    S.append(f"""<section data-background-color="#FBFBFD">
      <div class="eyebrow">● {eyebrow}</div><h2>{title}</h2>
      <div class="tiers">{body}</div>{notes(**n)}</section>""")

def matrix(title, eyebrow, cols, rows, foot="", **n):
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = ""
    for label, cls, cells in rows:
        tds = "".join(f"<td>{c}</td>" for c in cells)
        body += f'<tr class="{cls}"><th class="rh">{label}</th>{tds}</tr>'
    f = f'<div class="mx-foot">{foot}</div>' if foot else ''
    S.append(f"""<section data-background-color="#FBFBFD">
      <div class="eyebrow">● {eyebrow}</div><h2 class="sm">{title}</h2>
      <table class="matrix"><thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table>{f}{notes(**n)}</section>""")

def chart(title, eyebrow, bars, unit, **n):
    mx = max(v for _, v, _ in bars)
    rows = ""
    for lbl, v, note in bars:
        w = int(v / mx * 100)
        rows += (f'<div class="bar-row"><span class="bar-lbl">{lbl}</span>'
                 f'<span class="bar-track"><span class="bar-fill" style="width:{w}%"></span></span>'
                 f'<span class="bar-val">{note}</span></div>')
    S.append(f"""<section data-background-color="#FBFBFD">
      <div class="eyebrow">● {eyebrow}</div><h2>{title}</h2>
      <div class="chart">{rows}</div><div class="chart-unit">{unit}</div>{notes(**n)}</section>""")

def layered(title, eyebrow, **n):
    svg = """<svg viewBox="0 0 980 430" class="diagram">
      <defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#D4AD2B"/><stop offset="1" stop-color="#B8902E"/></linearGradient></defs>
      <g class="fragment" data-fragment-index="1"><rect x="20" y="300" width="700" height="110" rx="16" fill="#0E1A2F"/>
        <text x="46" y="345" fill="#F1D98B" font-size="30" font-weight="700">Model · LLM</text>
        <text x="46" y="375" fill="rgba(255,255,255,.6)" font-size="16">第一層 · 基礎引擎</text>
        <text x="46" y="398" fill="rgba(255,255,255,.85)" font-size="15" font-family="monospace">GPT · Claude · Gemini</text>
        <text x="700" y="362" text-anchor="end" fill="#F1D98B" font-size="18" font-weight="600">會生成 →</text></g>
      <g class="fragment" data-fragment-index="2"><rect x="20" y="170" width="700" height="110" rx="16" fill="#1d2d4a"/>
        <text x="46" y="215" fill="#fff" font-size="30" font-weight="700">Product</text>
        <text x="46" y="245" fill="rgba(255,255,255,.6)" font-size="16">第二層 · 對話介面</text>
        <text x="46" y="268" fill="rgba(255,255,255,.85)" font-size="15" font-family="monospace">ChatGPT · Gemini app</text>
        <text x="700" y="232" text-anchor="end" fill="#fff" font-size="18" font-weight="600">會聊天 →</text></g>
      <g class="fragment" data-fragment-index="3"><rect x="20" y="40" width="700" height="110" rx="16" fill="url(#g)"/>
        <text x="46" y="85" fill="#0E1A2F" font-size="30" font-weight="700">Agent</text>
        <text x="46" y="115" fill="rgba(14,26,47,.7)" font-size="16">第三層 · 動手做</text>
        <text x="46" y="138" fill="rgba(14,26,47,.85)" font-size="15" font-family="monospace">Claude Code · Cursor</text>
        <text x="700" y="102" text-anchor="end" fill="#0E1A2F" font-size="18" font-weight="700">會做事 →</text></g>
      <g class="fragment" data-fragment-index="3"><line x1="900" y1="395" x2="900" y2="70" stroke="#B8902E" stroke-width="2"/>
        <polygon points="900,52 893,72 907,72" fill="#B8902E"/>
        <text x="918" y="250" fill="#B8902E" font-size="15" transform="rotate(90 918,250)">愈上層 = 愈具體 = 愈能交付</text></g></svg>"""
    S.append(f"""<section data-background-color="#FBFBFD">
      <div class="eyebrow">● {eyebrow}</div><h2 class="sm">{title}</h2>{svg}{notes(**n)}</section>""")

def comparison(title, eyebrow, left, right, **n):
    def col(c, good):
        items = "".join(f'<li><span class="{"v" if good else "x"}">{"✓" if good else "✗"}</span> {i}</li>' for i in c["items"])
        return (f'<div class="cmp-card {"good" if good else ""}"><div class="cmp-tag">{c["tag"]}</div>'
                f'<div class="cmp-name">{c["name"]}</div><ul>{items}</ul>'
                f'<div class="cmp-foot {"win" if good else "bad"}">{c["foot"]}</div></div>')
    S.append(f"""<section data-background-color="#FBFBFD">
      <div class="eyebrow">● {eyebrow}</div><h2 class="sm">{title}</h2>
      <div class="cmp">{col(left,False)}{col(right,True)}</div>{notes(**n)}</section>""")

def steps(title, eyebrow, items, **n):
    body = "".join(
        f'<div class="step"><span class="step-l">{l}</span><div class="step-b"><b>{nm}</b><span>{d}</span></div>'
        f'<span class="step-m">{actor} · {time}</span></div>' for l, nm, d, actor, time in items)
    S.append(f"""<section data-background-color="#FBFBFD">
      <div class="eyebrow">● {eyebrow}</div><h2 class="sm">{title}</h2>
      <div class="steps">{body}</div>{notes(**n)}</section>""")

def ccc(title, eyebrow, items, **n):
    body = "".join(
        f'<div class="ccc-card"><div class="ccc-ic">{ic(i)}</div><div class="ccc-h"><b>C</b>{rest}</div>'
        f'<div class="ccc-zh">{zh}</div><div class="ccc-d">{d}</div><div class="ccc-a">🌰 {an}</div></div>'
        for rest, zh, d, an, i in items)
    S.append(f"""<section data-background-color="#FBFBFD">
      <div class="eyebrow">● {eyebrow}</div><h2 class="sm">{title}</h2>
      <div class="cccg">{body}</div>{notes(**n)}</section>""")

def punchline(text, eyebrow, flow=False, **n):
    f = ""
    if flow:
        def g(name, color): return (f'<span class="flow-ic" style="color:{color}">{ic(name)}</span>')
        f = f"""<div class="flow">
          <span class="flow-grp grey">{g('user','#9aa6b8')}<small>你</small></span><span class="ar grey">→</span>
          <span class="flow-grp grey">{g('wrench','#9aa6b8')}<small>工具</small></span>
          <span class="ar big">→</span>
          <span class="flow-grp">{g('user','#D4AD2B')}<small>你</small></span><span class="ar">→</span>
          <span class="flow-grp gold">{g('bot','#D4AD2B')}<small>AI Agent</small></span><span class="ar">→</span>
          <span class="flow-grp">{g('wrench','#D4AD2B')}<small>工具</small></span></div>"""
    S.append(f"""<section data-background-color="#0E1A2F" class="dark">
      <div class="eyebrow">● {eyebrow}</div>{f}<p class="punch">{text}</p>{notes(**n)}</section>""")

def closing(text, sub):
    S.append(f"""<section data-background-color="#0E1A2F" class="dark center">
      <p class="closing-t">{text}</p><p class="closing-s">{sub}</p></section>""")

# ============ SLIDES (from 04-口述腳本.md) ============
section("這三小時,你會學會<span class='accent'>指揮 AI</span>", "Claude Code Workshop", "把想法變成可運行成果——不靠寫 code,靠指揮 AI。",
        time="開場", hook="會被 AI 取代的人 vs 用 AI 取代別人的人,差在會不會『指揮』。今天讓你變後者。", transition="先問三個誠實的問題")

concept("我們為什麼<span class='accent'>要在這裡</span>", "第 0 章 · 8 min · 為什麼", "2026,AI 從『會聊天的工具』變成『會幫你動手的同事』。",
        ["門檻被打掉:不用先學程式語言", "會寫程式變便宜,會判斷與管理變更值錢", "今天聚焦『指揮』,不求精通"],
        icon="sparkles", analogy="你是廚房裡的主廚——不一定自己切菜,但你決定做什麼菜、嚐味道、決定上不上桌。",
        time="8 min", transition="先把幾個名詞講清楚,等下才有共同語言")

vocab("通用 AI 知識", "第 1 章 · 12 min · 詞彙(一詞一句,深入點卡片)", [
    ("LLM", "會讀懂你的話、生出文字的 AI 大腦", "brain-circuit"),
    ("Generative AI", "會『生出』新東西的 AI 總稱", "sparkles"),
    ("Prompt", "你打給 AI 的那段話、那個指令", "message-square-text"),
    ("Token", "計算與收費的最小單位", "coins"),
    ("Context Window", "一次能同時記得的內容上限", "layout-panel-top"),
    ("Tool", "讓 AI 能『動手』的外掛能力", "wrench"),
    ("MCP", "接上外部工具的『萬用插座標準』", "plug"),
    ("RAG", "先查資料再回答,不純憑記憶", "book-search"),
    ("Agentic AI", "自己規劃、動手、修正的設計思路", "workflow"),
    ("AI Agent", "把自主能力做成的實際程式", "bot"),
    ("Hallucination", "一本正經地編造不存在的事實(紅線)", "triangle-alert"),
], hook="十幾個詞不要求記住,只要求聽到不慌——深入比喻自己點卡片看。",
   say="LLM=讀過整個網路的實習生,憑印象接話、不查證(所以才有幻覺);MCP=USB-C 標準,各家照規格做自己的 server;Hallucination=它在生成不是查證,務必自己核實。",
   warn="Generative AI=會生成的總稱(含 LLM);會動手的是 Agentic/AI Agent,別講反。",
   transition="這些是概念;接著看今天實際會用到的工具")

vocab("平台與工具", "第 1 章 · 今天螢幕上會出現的", [
    ("Cursor", "內建 AI 的編輯器,今天用它自動裝環境", "mouse-pointer-click"),
    ("VS Code", "微軟免費編輯器,Cursor 的底子", "code"),
    ("Claude Code", "跑在終端機的 Claude,會讀寫檔案、做事", "bot"),
    ("GitHub", "程式碼雲端倉庫 + 版本 + 分享", "github"),
    ("Obsidian", "把 markdown 變可連結、可搜尋的知識庫", "notebook-text"),
    ("Terminal", "用打字指令操作電腦,Claude Code 跑在裡面", "terminal"),
], hook="這些不是概念,是你今天會點開、會用的 App。", transition="講一個最常搞混的:模型其實分三級")

tiers("同一件事,每家都有<span class='accent'>三種等級</span>", "第 1.1 章 · 模型分級", [
    ("第 1 級", "深度推理 · Opus 級", "$$$ 最貴最慢", "複雜規劃、難題、寫架構", "t1"),
    ("第 2 級", "均衡日常 · Sonnet 級", "$$ 系統預設", "八成任務:對話、寫程式、整理", "t2"),
    ("第 3 級", "高速廉價 · Haiku 級", "$ 最快最省", "大量簡單:分類、翻譯、即時", "t3"),
], hook="挑模型像挑車——挑『夠用的最便宜那一台』。", warn="不要丟 70B 參數;context window 以 token 計,跟參數量是兩回事。",
   transition="各家其實都有對應的同級品")

matrix("各廠商的<span class='accent'>同級對照</span>", "第 1.1 章 · 模型 × 廠商", [
    "Anthropic", "Google", "OpenAI", "DeepSeek", "阿里巴巴"], [
    ("第 1 級", "mx1", ["Claude Opus 4.8", "Gemini 2.5 Pro", "GPT-5 / o", "DeepSeek-R1", "Qwen Max"]),
    ("第 2 級", "mx2", ["Claude Sonnet 4.6", "Gemini 2.5 Flash", "GPT-5 mini", "DeepSeek-V3", "Qwen Plus"]),
    ("第 3 級", "mx3", ["Claude Haiku 4.5", "Gemini Flash-Lite", "GPT-5 nano", "—", "Qwen Turbo"]),
], foot="模型名稱更新快,記不住沒關係——記『三層』概念就好。",
   points=["挑夠用的最便宜那一層"], transition="把鏡頭拉遠:AI 其實分三層")

layered("由下往上,愈上層愈<span class='accent'>具體</span>", "第 2 章 · 15 min · 三層架構",
        hook="有人說『公司要投資 AI』,你要反問:你說的是哪一層?",
        points=["LLM=大腦會生成", "Product 困在對話框", "Agent 會交付"], transition="用 100 份問卷讓他們有感")

comparison("分析 <span class='accent'>100 份問卷</span>", "第 2 章 · 同一任務兩個世界",
    {"tag": "Product · ChatGPT", "name": "你自己動手", "items": ["資料一筆筆貼進去", "AI 說『應該怎麼分析』", "你再去 Excel 跑"], "foot": "30 分鐘 → 半成品"},
    {"tag": "Agent · Claude Code", "name": "它幫你動手", "items": ["直接讀 survey.csv", "自己寫 Python 並執行", "圖表自動輸出"], "foot": "10 分鐘 → 完整初稿"},
    analogy="Product 像隔玻璃的顧問;Agent 像走進辦公室幫你動手的同事。", transition="一句話收尾")

punchline("不只是效率差異——是從<br><strong>『我操作工具』</strong>變成<strong>『我管理 AI 去操作工具』</strong>", "第 2 章 · 收尾", flow=True,
          say="慢、停一下講這句金句。", transition="講這麼多,Claude Code 還沒裝——讓 AI 去裝 AI")

steps("讓 AI(Cursor)安裝 AI(Claude Code)", "第 3 章 · 安裝(課前已裝,課堂只驗收)", [
    ("A", "裝 Cursor", "登入選免費,別點 Pro", "學員", "2m"),
    ("B", "餵 setup.md 給 Cursor", "它自己裝 Node/Claude Code/API key", "Cursor AI", "5m"),
    ("C", "clone 素材", "親手打第一行指令", "學員", "3m"),
    ("D", "第一次跟 claude 對話", "白話問『我在哪個資料夾?』", "學員+AI", "3m"),
    ("E", "裝狀態列面板", "claude-hud:三行 slash 指令", "學員+AI", "3m"),
    ("F", "GitHub 建 repo + push", "Claude Code 自己跑 gh", "學員+AI", "3m"),
    ("G", "點題", "你剛指揮了兩個 AI Agent", "—", "—"),
], hook="你只手動裝一個 Cursor,剩下讓 AI 代勞——這本身就是第一課。", transition="停一下,點題")

concept("你剛剛<span class='accent'>指揮了兩個 AI Agent</span>", "點題 G · 4 min", "Cursor 幫你裝環境、Claude Code 幫你做事——它們都是 AI Agent。",
        ["帶走的是『指揮力』,不是某個工具", "Permission Model:每步問 Allow", "你按同意它才動——人始終在控制圈"],
        icon="bot", analogy="工具會一直換,『指揮 AI 把事做完』的能力不會。",
        time="4 min(上次只講 30 秒)", transition="那怎麼把指令下好?三個字母")

ccc("怎麼跟 AI 溝通 · <span class='accent'>CCC 框架</span>", "第 4 章 · 15 min", [
    ("ontext", "背景", "任務、輸入、給誰看、現有檔案——AI 沒有讀心術", "交辦助理:別只說『處理一下』", "target"),
    ("onstraints", "限制", "格式、長度、能/不能做什麼——邊界在哪", "找設計師:別只說『弄好看』", "ruler"),
    ("heck", "驗證", "有沒有當真?抽查?——唯一不能外包的", "實習生交報告:先抽查再簽名", "circle-check"),
], hook="多數人覺得『AI 不行』,其實是『我給的指令太爛』。", transition="框架有了,最重要——動手")

section("換你當主角 · <span class='accent'>動手做</span>", "第 5 章 · 30 min · 實作", "挑一個你真的在乎的場景,自己跑一遍:下指令 → 看它做 → 判斷要不要採納。",
        hook="這裡是 70% 動手的主場,我少講、巡場。", points=["白話下指令配 CCC", "它問 Allow 就看就按", "拿到結果先 Check 抽查"], transition="看幾組成果,重點是為什麼採納/丟掉")

concept("從原型到<span class='accent'>產品</span>", "第 7 章 · 15 min", "我用 Claude Code 做的爬蟲、找房平台——做這些幾乎沒寫 code。",
        ["專注『告訴它要什麼』,再當 QA 檢查", "低成本快速出 MVP,驗證想法行不行", "進階詞:CLAUDE.md / Skill / Git(今天知道有就好)"],
        icon="git-branch", analogy="像用樂高先拼一個能動的模型,對了再認真做。", time="15 min", transition="最後,別讓成果死在硬碟裡")

concept("CLAUDE.md · AI 的<span class='accent'>onboarding 手冊</span>", "第 7.1 章 · 5 min", "還記得 Claude Code 好像『已經懂你』嗎?秘密在這個檔案。",
        ["專案脈絡、偏好、紅線寫一次,AI 每次自動讀", "下指令字數省一半、品質更好", "MEMORY.md(Auto memory)是 Claude 自己寫的筆記,跟它互補"],
        icon="notebook-text", analogy="就是給 AI 的新員工 onboarding 包。", time="5 min", transition="收尾:成果的歸宿")

concept("你的成果<span class='accent'>歸宿</span>", "第 8 章 · 15 min · 收尾", "今天跑出來的東西,是你個人知識庫的起點。",
        ["GitHub:雲端備份、版本、可分享連結", "Obsidian:把 markdown 變可連結、可搜尋的知識庫", "養一個貼近你工作的 AI Agent——像賈維斯"],
        icon="github", time="15 min", transition="最後一句")

closing("你不需要會寫 code,<br>但你需要會 <strong>指揮 AI 寫 code</strong>", "整堂課的中心思想")

# ============ ASSEMBLE ============
CSS = """
:root{--navy:#0E1A2F;--navy2:#1d2d4a;--gold:#B8902E;--gold-b:#D4AD2B;--cream:#FBFBFD;--ink:#16202e;--ink2:#4a5568;--line:#e4e3df;--tint:rgba(184,144,46,.1)}
.reveal{font-family:"DM Sans","Noto Serif TC",sans-serif;font-size:30px;color:var(--ink)}
.reveal .slides{text-align:left}
.reveal h2{font-family:"Cormorant Garamond","Noto Serif TC",serif;font-size:1.8em;font-weight:700;line-height:1.1;margin:.1em 0 .4em}
.reveal h2.sm{font-size:1.4em}
.reveal .accent{color:var(--gold)} .reveal .dark .accent{color:var(--gold-b)}
.reveal .eyebrow{font-family:"JetBrains Mono",monospace;font-size:.46em;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);font-weight:600;margin-bottom:.5em}
.reveal .lede{color:var(--ink2);font-size:.66em;line-height:1.6} .reveal .dark .lede{color:rgba(255,255,255,.82)}
.reveal .dark{color:#fff} .reveal .dark h2{color:#fff}
.reveal .center{text-align:center}
.ic{width:1em;height:1em;vertical-align:middle}
.c-body{display:flex;gap:26px;align-items:flex-start;margin-top:6px}
.c-icon{flex:0 0 auto;color:var(--gold);font-size:64px;line-height:1;margin-top:6px}
.pts{font-size:.6em;line-height:1.7;color:var(--ink2);margin:.2em 0 0;padding-left:1.1em}
.analogy{margin-top:16px;font-size:.56em;color:var(--ink2);background:var(--tint);border-left:3px solid var(--gold);padding:10px 14px;border-radius:8px}
.vgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;font-size:.5em}
.vc{background:#fff;border:1px solid var(--line);border-radius:12px;padding:13px 15px}
.vc-h{display:flex;align-items:center;gap:9px;font-family:"JetBrains Mono",monospace;font-weight:600;color:var(--ink);margin-bottom:5px}
.vc-h .ic{color:var(--gold);font-size:22px;width:22px;height:22px} .vc-d{color:var(--ink2);line-height:1.5}
.tiers{display:flex;flex-direction:column;gap:12px;margin-top:6px}
.tier{display:grid;grid-template-columns:120px 1fr auto;gap:18px;align-items:center;padding:18px 22px;border-radius:14px;font-size:.5em}
.tier.t1{background:linear-gradient(135deg,var(--gold),var(--gold-b));color:var(--navy)}
.tier.t2{background:var(--navy2);color:#fff} .tier.t3{background:var(--navy);color:var(--gold-b)}
.t-badge{font-family:"JetBrains Mono",monospace;font-weight:700} .t-name{font-weight:700;font-size:1.15em}
.t-cost{font-family:"JetBrains Mono",monospace;opacity:.85} .t-use{grid-column:2/4;opacity:.85;font-size:.92em}
.tier{grid-template-areas:"b n c" "b u u"}
.t-badge{grid-area:b}.t-name{grid-area:n}.t-cost{grid-area:c}.t-use{grid-area:u}
.matrix{width:100%;border-collapse:collapse;font-size:.42em;margin-top:8px}
.matrix th,.matrix td{padding:11px 12px;text-align:left;border-bottom:1px solid var(--line)}
.matrix thead th{font-family:"JetBrains Mono",monospace;color:var(--ink2);border-bottom:2px solid var(--line)}
.matrix .rh{font-family:"JetBrains Mono",monospace;font-weight:700;white-space:nowrap}
.matrix tr.mx1 .rh{color:var(--gold)} .matrix td{color:var(--ink2)}
.mx-foot{font-size:.4em;color:var(--ink2);margin-top:12px;font-family:"JetBrains Mono",monospace}
.chart{display:flex;flex-direction:column;gap:16px;margin-top:14px;font-size:.55em}
.bar-row{display:grid;grid-template-columns:120px 1fr 60px;align-items:center;gap:14px}
.bar-lbl{font-weight:600} .bar-track{background:var(--line);border-radius:100px;height:26px;overflow:hidden}
.bar-fill{display:block;height:100%;background:linear-gradient(90deg,var(--gold),var(--gold-b));border-radius:100px}
.bar-val{font-family:"JetBrains Mono",monospace;color:var(--gold);font-weight:700}
.chart-unit{font-size:.42em;color:var(--ink2);margin-top:14px;font-family:"JetBrains Mono",monospace}
.diagram{width:100%;height:auto;margin-top:4px}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:6px;font-size:.5em}
.cmp-card{border:1px solid var(--line);border-radius:16px;padding:22px;background:#fff}
.cmp-card.good{border-color:rgba(184,144,46,.5);background:var(--tint)}
.cmp-tag{font-family:"JetBrains Mono",monospace;font-size:.82em;color:var(--gold);margin-bottom:.2em}
.cmp-name{font-size:1.3em;font-weight:700;margin-bottom:.4em} .cmp-card ul{list-style:none;padding:0;line-height:1.9;color:var(--ink2)}
.x{color:#c0796b;font-weight:700}.v{color:var(--gold);font-weight:700}
.cmp-foot{margin-top:.4em;font-family:"JetBrains Mono",monospace;font-weight:700}.cmp-foot.bad{color:#b04a3a}.cmp-foot.win{color:var(--gold)}
.steps{display:flex;flex-direction:column;gap:8px;font-size:.46em;margin-top:4px}
.step{display:grid;grid-template-columns:40px 1fr auto;gap:14px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:11px;padding:11px 16px}
.step-l{width:34px;height:34px;border-radius:50%;background:var(--gold);color:#fff;font-family:"JetBrains Mono",monospace;font-weight:700;display:flex;align-items:center;justify-content:center}
.step-b b{color:var(--ink)} .step-b span{display:block;color:var(--ink2)} .step-m{font-family:"JetBrains Mono",monospace;color:var(--ink2);font-size:.85em;white-space:nowrap}
.cccg{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:6px;font-size:.5em}
.ccc-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px}
.ccc-ic{color:var(--gold);font-size:38px;margin-bottom:8px} .ccc-h{font-family:"Cormorant Garamond",serif;font-size:1.7em;font-weight:700}
.ccc-h b{color:var(--gold)} .ccc-zh{color:var(--ink2);font-weight:600;margin:.1em 0 .4em} .ccc-d{color:var(--ink2);line-height:1.5}
.ccc-a{margin-top:10px;color:var(--ink2);background:var(--tint);padding:8px 11px;border-radius:8px;font-size:.92em}
.flow{display:flex;align-items:center;gap:14px;justify-content:center;margin:10px 0 26px}
.flow-grp{display:flex;flex-direction:column;align-items:center;gap:4px} .flow-grp small{font-size:.4em;color:#fff} .flow-grp.gold small,.flow-grp small{color:#fff}
.flow-ic{font-size:46px} .flow-grp.grey small{color:#9aa6b8}
.ar{color:var(--gold-b);font-size:30px;font-weight:700}.ar.grey{color:#9aa6b8}.ar.big{font-size:40px}
.punch{font-family:"Cormorant Garamond","Noto Serif TC",serif;font-size:1.4em;font-weight:700;line-height:1.35}.punch strong{color:var(--gold-b)}
.closing-t{font-family:"Cormorant Garamond","Noto Serif TC",serif;font-size:2em;font-weight:700;line-height:1.25;text-align:center}.closing-t strong{color:var(--gold-b)}
.closing-s{text-align:center;font-family:"JetBrains Mono",monospace;font-size:.42em;letter-spacing:.1em;color:rgba(255,255,255,.5);margin-top:1.4em}
.reveal aside.notes{font-size:15px;line-height:1.5}
"""

HTML = f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Claude Code Workshop · Deck</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/white.css">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&family=Noto+Serif+TC:wght@500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="reveal"><div class="slides">
{''.join(S)}
</div></div>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/notes/notes.js"></script>
<script>Reveal.initialize({{hash:true,slideNumber:'c/t',transition:'slide',width:1280,height:720,margin:0.07,plugins:[RevealNotes]}});</script>
</body></html>"""

out = pathlib.Path(__file__).with_name("workshop-deck.html")
out.write_text(HTML, encoding="utf-8")
print(f"wrote {out}  ({len(S)} slides)")
