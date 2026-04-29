"""
╔══════════════════════════════════════════════════════════════╗
║   ILLUMINATI KNOWLEDGE GRAPH — STREAMLIT DASHBOARD          ║
║   100% OFFLINE — No API key needed                          ║
║   Run: streamlit run app.py                                 ║
╚══════════════════════════════════════════════════════════════╝
"""

import re, random
from collections import defaultdict

import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

# ══════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════

st.set_page_config(
    page_title="Illuminati · Knowledge Graph",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
#  CUSTOM CSS
# ══════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Mono', monospace;
    background-color: #0a0a0f;
    color: #e0ddd6;
}
.stApp { background-color: #0a0a0f; }

/* Header */
.hero {
    background: linear-gradient(180deg, #11111a 0%, #0a0a0f 100%);
    border-bottom: 1px solid #2a2a3d;
    padding: 2rem 1rem 1.5rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.hero-eye  { font-size: 3rem; margin-bottom: 0.2rem; }
.hero-title {
    font-family: 'Cinzel', serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 900;
    letter-spacing: 12px;
    color: #c9a84c;
    text-shadow: 0 0 40px rgba(201,168,76,0.3);
    margin: 0;
}
.hero-sub {
    font-size: 0.65rem;
    letter-spacing: 4px;
    color: #8888aa;
    margin-top: 0.4rem;
    text-transform: uppercase;
}
.hero-badge {
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: #27ae60;
    margin-top: 0.25rem;
}

/* Stat cards */
.stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 1rem; }
.stat-card {
    background: #181825;
    border: 1px solid #2a2a3d;
    border-top: 3px solid #c9a84c;
    padding: 1rem;
    text-align: center;
    flex: 1;
    min-width: 110px;
    border-radius: 2px;
}
.stat-icon { font-size: 1.2rem; color: #c9a84c; margin-bottom: 4px; }
.stat-val  { font-family: 'Cinzel', serif; font-size: 1.6rem; font-weight: 700; color: #e0ddd6; }
.stat-lbl  { font-size: 0.55rem; color: #8888aa; letter-spacing: 2px; text-transform: uppercase; margin-top: 3px; }

/* Section titles */
.sec-title {
    font-family: 'Cinzel', serif;
    font-size: 0.75rem;
    color: #e0ddd6;
    letter-spacing: 3px;
    text-transform: uppercase;
    border-bottom: 1px solid #2a2a3d;
    padding-bottom: 6px;
    margin-bottom: 10px;
}
.sec-title span { color: #c9a84c; }

/* Entity badges */
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 2px;
    font-size: 0.65rem;
    letter-spacing: 1px;
    font-weight: 600;
}

/* Story */
.story-container {
    max-width: 720px;
    margin: 0 auto;
    border-left: 3px solid rgba(201,168,76,0.2);
    padding-left: 2rem;
}
.story-title {
    font-family: 'Cinzel', serif;
    font-size: clamp(1.2rem, 3vw, 2rem);
    font-weight: 900;
    color: #c9a84c;
    text-align: center;
    letter-spacing: 4px;
    text-shadow: 0 0 28px rgba(201,168,76,0.3);
    margin-bottom: 0.5rem;
}
.story-divider { color: #c9a84c; letter-spacing: 8px; text-align: center; font-size: 0.75rem; margin: 0.5rem 0; }
.story-para {
    font-family: 'Palatino Linotype', Georgia, serif;
    font-size: 0.95rem;
    line-height: 1.95;
    color: #ccc8c0;
    margin-bottom: 1.2rem;
    text-align: justify;
}
.story-finis {
    text-align: center;
    color: #c9a84c;
    font-family: 'Cinzel', serif;
    letter-spacing: 8px;
    font-size: 0.85rem;
    padding: 1.5rem 0;
    border-top: 1px solid #2a2a3d;
    margin-top: 1rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #11111a !important;
    border-right: 1px solid #2a2a3d;
}
section[data-testid="stSidebar"] * { color: #e0ddd6 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #11111a; border-bottom: 1px solid #2a2a3d; gap: 0; }
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8888aa;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 1px;
    padding: 0.75rem 1.5rem;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] { color: #c9a84c !important; border-bottom: 2px solid #c9a84c !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #c9a84c, #8a6a1e) !important;
    color: #000 !important;
    font-family: 'Cinzel', serif !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    border: none !important;
    padding: 0.75rem 2.5rem !important;
    border-radius: 2px !important;
    box-shadow: 0 0 28px rgba(201,168,76,0.3) !important;
    font-size: 0.85rem !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.9 !important; }

/* Dataframe */
.stDataFrame { background: #181825; }

/* Hide streamlit branding */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  CORPUS
# ══════════════════════════════════════════════

CORPUS = """
The Illuminati was founded on May 1, 1776, by Adam Weishaupt, a professor at the University of Ingolstadt in Bavaria.
Weishaupt created the Order of the Illuminati to oppose religious influence over public life and promote Enlightenment ideals.
The Bavarian government outlawed the Illuminati in 1785, but conspiracy theorists believe the organization went underground.
According to modern conspiracy theories, the Illuminati secretly controls world governments, financial institutions, and the media.
The Rothschild banking family is frequently accused of being core members of the Illuminati inner circle.
The Federal Reserve, the World Bank, and the IMF are said to be financial instruments used by the Illuminati to control global economies.
The New World Order is the end goal of the Illuminati, a single world government under their control.
George Soros, Bill Gates, and the Rockefeller Foundation are often accused of funding Illuminati agendas.
The United Nations is believed by conspiracy theorists to be a front organization used by the Illuminati.
Secret symbols of the Illuminati are said to appear on the US Dollar bill, particularly the All-Seeing Eye above the pyramid.
Freemasonry is considered by theorists to be a sister organization that shares leadership with the Illuminati.
The Council on Foreign Relations and the Bilderberg Group are accused of being Illuminati-controlled policy bodies.
Hollywood, the music industry, and mainstream media are thought to be controlled by the Illuminati to manipulate public opinion.
Jay-Z, Beyonce, and Lady Gaga are frequently accused of using Illuminati symbolism in their performances.
MK-Ultra, a real CIA mind control program, is cited as evidence that the Illuminati manipulates individuals through governments.
The assassination of John F. Kennedy is often linked to the Illuminati, who allegedly ordered his death for opposing their agenda.
Princess Diana death is also claimed to be an Illuminati orchestrated event to silence her humanitarian influence.
The September 11 attacks are sometimes attributed to the Illuminati staging a false flag event to justify global surveillance.
Ancient secret societies like the Knights Templar and the Order of the Rosicrucians are considered Illuminati predecessors.
The Vatican and the Catholic Church are accused of working alongside the Illuminati to control spiritual life globally.
Area 51 is rumored to house Illuminati alien technology deals meant to accelerate their technological dominance.
The World Economic Forum in Davos is seen as a modern gathering place for Illuminati-affiliated global elites.
Rockefeller Foundation funded global health initiatives are alleged to be population control programs run by the Illuminati.
The media empire of Rupert Murdoch is accused of being an Illuminati propaganda machine.
""".strip()

# ══════════════════════════════════════════════
#  NLP PIPELINE
# ══════════════════════════════════════════════

ENTITY_COLORS = {
    "PERSON":   "#e74c3c",
    "ORG":      "#3498db",
    "EVENT":    "#e67e22",
    "CONCEPT":  "#9b59b6",
    "LOCATION": "#27ae60",
    "ARTIFACT": "#f39c12",
    "DATE":     "#95a5a6",
}

GAZETTEER = {
    "PERSON":   ["Adam Weishaupt","George Soros","Bill Gates","Jay-Z","Beyonce",
                 "Lady Gaga","John F. Kennedy","Princess Diana","Rupert Murdoch"],
    "ORG":      ["Illuminati","Order of the Illuminati","Rothschild","Federal Reserve",
                 "World Bank","IMF","United Nations","Freemasonry",
                 "Council on Foreign Relations","Bilderberg Group","Hollywood","CIA",
                 "Vatican","Catholic Church","Knights Templar","Order of the Rosicrucians",
                 "Rockefeller Foundation","World Economic Forum","Bavarian government"],
    "LOCATION": ["Bavaria","Ingolstadt","Area 51","Davos"],
    "EVENT":    ["MK-Ultra","September 11 attacks",
                 "assassination of John F. Kennedy","Princess Diana death"],
    "CONCEPT":  ["New World Order","Enlightenment","false flag",
                 "mind control","global surveillance","population control"],
    "ARTIFACT": ["All-Seeing Eye","US Dollar bill","pyramid"],
    "DATE":     ["May 1, 1776","1776","1785"],
}

DESCRIPTIONS = {
    "Adam Weishaupt":"Bavarian professor who founded the Illuminati on May 1, 1776",
    "Illuminati":"Secret society alleged to control world governments and institutions",
    "Order of the Illuminati":"Original name of the secret society founded by Weishaupt",
    "Rothschild":"Banking dynasty accused of being Illuminati financiers",
    "Federal Reserve":"US central bank alleged to be an Illuminati financial instrument",
    "New World Order":"Alleged Illuminati goal of a single world government",
    "George Soros":"Billionaire accused of funding Illuminati-linked agendas",
    "Bill Gates":"Tech magnate accused of ties to Illuminati population control",
    "United Nations":"International body alleged to be an Illuminati front organization",
    "All-Seeing Eye":"Illuminati symbol said to appear on the US Dollar bill",
    "Freemasonry":"Secret fraternal order considered a sister group to the Illuminati",
    "Bilderberg Group":"Elite annual conference accused of being Illuminati policy body",
    "Jay-Z":"Rapper accused of using Illuminati symbolism in performances",
    "Beyonce":"Pop star accused of embedding Illuminati imagery in her art",
    "Lady Gaga":"Musician frequently accused of displaying Illuminati symbolism",
    "MK-Ultra":"Real CIA mind control program cited as proof of Illuminati influence",
    "John F. Kennedy":"US president allegedly assassinated on Illuminati orders",
    "Princess Diana":"British royal whose death is claimed to be Illuminati-orchestrated",
    "September 11 attacks":"Attacks some attribute to an Illuminati false flag operation",
    "Vatican":"Catholic institution accused of an alliance with the Illuminati",
    "Knights Templar":"Medieval secret society considered a predecessor of the Illuminati",
    "CIA":"US intelligence agency alleged to act as an Illuminati instrument",
    "Bavaria":"German region where the Illuminati was originally founded",
    "Area 51":"Secret US base rumored to house Illuminati-alien technology",
    "World Economic Forum":"Davos gathering seen as a modern Illuminati meeting place",
    "Rockefeller Foundation":"Philanthropic body accused of running Illuminati-linked programs",
    "Hollywood":"Film industry alleged to be an Illuminati propaganda machine",
    "Rupert Murdoch":"Media mogul whose empire is accused of being Illuminati propaganda",
    "Council on Foreign Relations":"US policy group accused of being Illuminati-controlled",
    "World Bank":"International lender alleged to be an Illuminati economic tool",
    "IMF":"International monetary body accused of serving Illuminati interests",
    "US Dollar bill":"Currency bearing Illuminati symbols including the All-Seeing Eye",
    "Order of the Rosicrucians":"Ancient mystical order considered an Illuminati predecessor",
    "Catholic Church":"Religious institution accused of Illuminati collaboration",
    "May 1, 1776":"Date the Illuminati was officially founded by Adam Weishaupt",
    "1785":"Year the Bavarian government officially banned the Illuminati",
    "Davos":"Swiss city hosting the World Economic Forum gatherings",
    "Ingolstadt":"Bavarian city where the University of Ingolstadt is located",
    "false flag":"Covert operation designed to deceive and blamed on another party",
    "mind control":"Psychological manipulation technique allegedly used by the Illuminati",
    "global surveillance":"Mass monitoring system allegedly justified by Illuminati false flags",
    "population control":"Alleged Illuminati agenda to reduce global population",
    "pyramid":"Illuminati architectural symbol appearing on the US Dollar",
    "Bavarian government":"18th-century authority that banned the Illuminati in 1785",
    "1776":"Year the Illuminati was founded",
}

RELATION_RULES = [
    (r"Adam Weishaupt",           "FOUNDED",           r"(Illuminati|Order of the Illuminati)"),
    (r"(Illuminati)",             "CONTROLS",          r"Federal Reserve"),
    (r"(Illuminati)",             "CONTROLS",          r"World Bank"),
    (r"(Illuminati)",             "CONTROLS",          r"IMF"),
    (r"(Illuminati)",             "CONTROLS",          r"United Nations"),
    (r"(Illuminati)",             "CONTROLS",          r"Hollywood"),
    (r"Rothschild",               "MEMBER_OF",         r"(Illuminati)"),
    (r"George Soros",             "FUNDS",             r"(Illuminati)"),
    (r"Bill Gates",               "FUNDS",             r"(Illuminati)"),
    (r"Rockefeller Foundation",   "FUNDS",             r"(Illuminati)"),
    (r"(Illuminati)",             "GOAL_IS",           r"New World Order"),
    (r"(Illuminati)",             "SYMBOL_OF",         r"All-Seeing Eye"),
    (r"All-Seeing Eye",           "APPEARS_ON",        r"US Dollar bill"),
    (r"(Illuminati)",             "LINKED_TO",         r"Freemasonry"),
    (r"Knights Templar",          "PREDECESSOR_OF",    r"(Illuminati)"),
    (r"Order of the Rosicrucians","PREDECESSOR_OF",    r"(Illuminati)"),
    (r"Bilderberg Group",         "CONTROLLED_BY",     r"(Illuminati)"),
    (r"Council on Foreign Relations","CONTROLLED_BY",  r"(Illuminati)"),
    (r"CIA",                      "CONDUCTED",         r"MK-Ultra"),
    (r"(Illuminati)",             "USED",              r"MK-Ultra"),
    (r"(Illuminati)",             "ORDERED",           r"assassination of John F. Kennedy"),
    (r"(Illuminati)",             "ORCHESTRATED",      r"Princess Diana death"),
    (r"(Illuminati)",             "STAGED",            r"September 11 attacks"),
    (r"Vatican",                  "ALLIED_WITH",       r"(Illuminati)"),
    (r"Catholic Church",          "ALLIED_WITH",       r"(Illuminati)"),
    (r"Jay-Z",                    "ACCUSED_OF",        r"(Illuminati)"),
    (r"Beyonce",                  "ACCUSED_OF",        r"(Illuminati)"),
    (r"Lady Gaga",                "ACCUSED_OF",        r"(Illuminati)"),
    (r"Adam Weishaupt",           "BASED_IN",          r"Bavaria"),
    (r"(Illuminati)",             "FOUNDED_IN",        r"Bavaria"),
    (r"(Illuminati)",             "BANNED_BY",         r"Bavarian government"),
    (r"Area 51",                  "LINKED_TO",         r"(Illuminati)"),
    (r"World Economic Forum",     "LINKED_TO",         r"(Illuminati)"),
    (r"Rupert Murdoch",           "SERVES",            r"(Illuminati)"),
    (r"Freemasonry",              "SHARES_LEADERSHIP", r"(Illuminati)"),
    (r"(Illuminati)",             "FOUNDED_ON",        r"May 1, 1776"),
    (r"Bavarian government",      "BANNED",            r"(Illuminati)"),
]


@st.cache_data
def run_pipeline():
    # --- Entity Extraction ---
    entities, seen = [], set()
    for label, names in GAZETTEER.items():
        for name in names:
            pat = re.compile(re.escape(name), re.IGNORECASE)
            if pat.search(CORPUS) and name not in seen:
                seen.add(name)
                entities.append({
                    "text": name, "label": label,
                    "description": DESCRIPTIONS.get(name, f"{label}: {name}"),
                    "count": len(pat.findall(CORPUS)),
                })

    # --- Relation Extraction ---
    entity_names = {e["text"] for e in entities}
    relations, rel_seen = [], set()
    for subj_pat, rel, obj_pat in RELATION_RULES:
        sm = re.search(subj_pat, CORPUS, re.IGNORECASE)
        om = re.search(obj_pat,  CORPUS, re.IGNORECASE)
        if not sm or not om: continue
        sc = next((n for n in entity_names if re.search(re.escape(sm.group()), n, re.IGNORECASE)), None)
        oc = next((n for n in entity_names if re.search(re.escape(om.group()), n, re.IGNORECASE)), None)
        if not sc or not oc or sc == oc: continue
        key = (sc, rel, oc)
        if key in rel_seen: continue
        rel_seen.add(key)
        sents  = CORPUS.split(".")
        co_occ = sum(1 for s in sents if re.search(subj_pat,s,re.IGNORECASE) and re.search(obj_pat,s,re.IGNORECASE))
        relations.append({"subject":sc,"relation":rel,"object":oc,
                          "confidence": round(min(0.95, 0.55+co_occ*0.15), 2)})

    # --- Knowledge Graph ---
    G = nx.DiGraph()
    for e in entities:
        G.add_node(e["text"], label=e["label"],
                   description=e["description"],
                   color=ENTITY_COLORS.get(e["label"],"#bdc3c7"),
                   count=e["count"])
    for r in relations:
        if r["subject"] in G and r["object"] in G:
            G.add_edge(r["subject"], r["object"],
                       relation=r["relation"], confidence=r["confidence"])

    # --- Stats ---
    dc = nx.degree_centrality(G)
    bc = nx.betweenness_centrality(G)
    pr = nx.pagerank(G, alpha=0.85)
    type_dist, rel_dist = defaultdict(int), defaultdict(int)
    for _, d in G.nodes(data=True):   type_dist[d.get("label","?")] += 1
    for _, _, d in G.edges(data=True): rel_dist[d.get("relation","?")] += 1

    def top8(m):
        return sorted(m.items(), key=lambda x:-x[1])[:8]

    stats = {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "density":   round(nx.density(G), 4),
        "components":nx.number_weakly_connected_components(G),
        "top_degree":      top8(dc),
        "top_betweenness": top8(bc),
        "top_pagerank":    top8(pr),
        "entity_dist":     dict(type_dist),
        "relation_dist":   dict(rel_dist),
        "pagerank":        pr,
    }

    # --- Story ---
    random.seed(42)
    def find(label, n=1):
        m = [e["text"] for e in entities if e["label"]==label]
        random.shuffle(m)
        return m[:n] if n>1 else (m[0] if m else "???")
    def pick(lst, fallback="???"):
        return lst[0] if isinstance(lst,list) and lst else fallback
    def pick_match(lst, *kws):
        if isinstance(lst,list):
            for kw in kws:
                h = next((o for o in lst if kw.lower() in o.lower()),None)
                if h: return h
            return lst[0] if lst else "???"
        return lst or "???"

    persons=find("PERSON",6); orgs=find("ORG",8); events=find("EVENT",2)
    concepts=find("CONCEPT",2); artifacts=find("ARTIFACT",2)
    locations=find("LOCATION",2); dates=find("DATE",2)

    protagonist = random.choice(["Professor Elena Marsh","Dr. Riya Anand","Agent Sara Wolfe"])
    story = f"""\
— THE EYE THAT NEVER CLOSES —

The call comes at {random.choice(["3:17 AM","2:44 AM","4:01 AM"])} — an encrypted message containing one image: the {pick(artifacts)}, circled in red.
{protagonist} stares at the screen, surrounded by years of research on {pick_match(orgs,"Illuminati")}. The symbol appears on the {pick(artifacts if isinstance(artifacts,list) and len(artifacts)>1 else ["US Dollar bill"])}.
What the world dismisses as coincidence, she knows is design.

She traces the origin back to {pick(persons)}, who on {pick(dates) if isinstance(dates,list) and dates else "May 1, 1776"} established {pick_match(orgs,"Illuminati")} in {pick(locations) if isinstance(locations,list) and locations else "Bavaria"}.
The Bavarian government tried to destroy them in 1785. They failed. You cannot outlaw an idea written in blood.

The web is vast. {pick_match(orgs,"Illuminati")} controls the {pick_match(orgs,"Federal Reserve","World Bank","IMF")} and funnels orders through {pick_match(orgs,"Nation","Forum","United")}.
{pick_match(orgs,"Freemasonry","Vatican","CIA")} enforces the doctrine of silence. At the top of the pyramid sit {persons[1] if len(persons)>1 else "George Soros"} and {persons[2] if len(persons)>2 else "Bill Gates"} — names whose wealth and reach span every continent.

Their goal has never changed: the {pick(concepts) if concepts else "New World Order"}. Not a fantasy — a centuries-old architectural project.
They co-opted {pick_match(orgs,"Hollywood","media")} to shape minds, used {pick_match(orgs,"CIA")} to break them,
and eliminated those who came too close — {persons[3] if len(persons)>3 else "John F. Kennedy"}, and later {persons[4] if len(persons)>4 else "Princess Diana"}.

Now, cross-referencing the {pick_match(orgs,"Council","Bilderberg")} guest list with leaked {pick_match(orgs,"Templar","Rosicrucian","Freemas")} documents,
{protagonist} finds a name she has seen twice before. Her cursor hovers. She hesitates.

The {pick(artifacts)} on the Dollar is not a national symbol.
It is a signature. A declaration. A promise.

They were always here. They are not hiding anymore.
The eye, it turns out, has been watching her all along."""

    return entities, relations, G, stats, story


# ══════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════

st.markdown("""
<div class="hero">
  <div class="hero-eye">👁</div>
  <div class="hero-title">ILLUMINATI</div>
  <div class="hero-sub">Knowledge Graph &nbsp;·&nbsp; NLP Pipeline &nbsp;·&nbsp; Story Engine</div>
  <div class="hero-badge">✅ &nbsp;100% Offline — No API key required</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 👁 Controls")
    st.markdown("---")

    if st.button("⚡  RUN FULL PIPELINE"):
        st.session_state["ran"] = True

    st.markdown("---")
    st.markdown("**Graph Layout**")
    layout_choice = st.selectbox("Physics layout",
        ["barnes_hut","force_atlas_2based","hierarchical_repulsion","repulsion"],
        index=0, label_visibility="collapsed")

    st.markdown("**Filter by Entity Type**")
    type_filter = st.selectbox("Entity type",
        ["ALL"] + list(ENTITY_COLORS.keys()),
        index=0, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**Legend**")
    for label, color in ENTITY_COLORS.items():
        st.markdown(
            f'<span style="color:{color};font-size:11px;letter-spacing:1px">◆ {label}</span>',
            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:9px;color:#8888aa;letter-spacing:1px">NLP ASSIGNMENT · BITS PILANI<br>Illuminati Conspiracy Theory<br>Knowledge Graph Pipeline</div>',
                unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  MAIN CONTENT
# ══════════════════════════════════════════════

if not st.session_state.get("ran"):
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;
                justify-content:center;padding:80px 20px;text-align:center">
        <div style="font-size:5rem;opacity:0.1;margin-bottom:1rem">👁</div>
        <div style="font-family:'Cinzel',serif;font-size:1rem;color:#8888aa;
                    letter-spacing:3px;text-transform:uppercase">
            Click ⚡ RUN FULL PIPELINE in the sidebar to begin
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Run pipeline (cached)
with st.spinner("🔍 Extracting entities..."):
    entities, relations, G, stats, story = run_pipeline()

# Success banner
st.success(f"✅ Pipeline complete — {len(entities)} entities · {len(relations)} relations · {G.number_of_edges()} graph edges")

# ══════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "🕸  Knowledge Graph",
    "🔬  NER & Relations",
    "📖  Generated Story",
    "📊  Graph Metrics",
])

# ─────────────────────────────────────────────
#  TAB 1 — KNOWLEDGE GRAPH
# ─────────────────────────────────────────────
with tab1:
    pr = stats["pagerank"]
    max_pr = max(pr.values()) if pr else 1

    # Filter entities
    filtered_entities = entities if type_filter == "ALL" else [
        e for e in entities if e["label"] == type_filter
    ]
    filtered_names = {e["text"] for e in filtered_entities}

    nodes, edges = [], []
    for e in filtered_entities:
        size = 20 + 40 * (pr.get(e["text"], 0) / max_pr)
        nodes.append(Node(
            id=e["text"], label=e["text"],
            size=size, color=ENTITY_COLORS.get(e["label"],"#aaa"),
            title=f"[{e['label']}] {e['description']}",
            font={"color":"#ffffff","size":10},
        ))
    for r in relations:
        if r["subject"] in filtered_names and r["object"] in filtered_names:
            edges.append(Edge(
                source=r["subject"], target=r["object"],
                label=r["relation"],
                color="#c9a84c",
                font={"color":"#aaaaaa","size":8},
                arrows="to",
            ))

    config = Config(
        width="100%", height=580,
        directed=True,
        physics=True,
        hierarchical=False,
        solver=layout_choice,
        nodeHighlightBehavior=True,
        highlightColor="#ffd700",
        backgroundColor="#0a0a0f",
        node={"labelProperty":"label"},
        link={"labelProperty":"label","renderLabel":True},
    )

    st.markdown(f'<div class="sec-title"><span>▸</span> Interactive Knowledge Graph &nbsp;·&nbsp; {len(nodes)} nodes &nbsp;·&nbsp; {len(edges)} edges</div>', unsafe_allow_html=True)
    agraph(nodes=nodes, edges=edges, config=config)
    st.caption("💡 Drag nodes to rearrange · Scroll to zoom · Click a node to highlight connections · Use sidebar to filter by entity type")

# ─────────────────────────────────────────────
#  TAB 2 — NER & RELATIONS
# ─────────────────────────────────────────────
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f'<div class="sec-title"><span>▸</span> Named Entities ({len(entities)})</div>', unsafe_allow_html=True)
        ent_df = pd.DataFrame([{
            "Entity":      e["text"],
            "Type":        e["label"],
            "Freq":        e["count"],
            "Description": e["description"],
        } for e in entities])

        # Color-code type column
        def color_type(val):
            color = ENTITY_COLORS.get(val,"#aaa")
            return f"background-color:{color}22;color:{color};font-weight:600"

        st.dataframe(
            ent_df.style.applymap(color_type, subset=["Type"]),
            use_container_width=True, height=420,
            hide_index=True,
        )

    with col2:
        st.markdown(f'<div class="sec-title"><span>▸</span> Relation Triples ({len(relations)})</div>', unsafe_allow_html=True)
        rel_df = pd.DataFrame([{
            "Subject":    r["subject"],
            "Relation":   r["relation"],
            "Object":     r["object"],
            "Confidence": r["confidence"],
        } for r in relations])

        st.dataframe(rel_df, use_container_width=True, height=420, hide_index=True)

    st.markdown("---")
    st.markdown('<div class="sec-title"><span>▸</span> Source Corpus</div>', unsafe_allow_html=True)
    st.code(CORPUS, language=None)

# ─────────────────────────────────────────────
#  TAB 3 — STORY
# ─────────────────────────────────────────────
with tab3:
    lines = story.strip().split("\n")
    title = lines[0].strip("— ").strip()
    body  = "\n".join(lines[1:]).strip()
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]

    st.markdown('<div class="story-divider">— — —</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="story-title">{title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="story-divider">— — —</div>', unsafe_allow_html=True)

    st.markdown('<div class="story-container">', unsafe_allow_html=True)
    for i, para in enumerate(paras):
        indent = "text-indent:2em;" if i > 0 else ""
        st.markdown(f'<p class="story-para" style="{indent}">{para}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="story-finis">👁 &nbsp; FINIS &nbsp; 👁</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TAB 4 — GRAPH METRICS
# ─────────────────────────────────────────────
with tab4:
    # Stat cards
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card"><div class="stat-icon">◉</div><div class="stat-val">{stats['num_nodes']}</div><div class="stat-lbl">Entities</div></div>
        <div class="stat-card"><div class="stat-icon">⇌</div><div class="stat-val">{stats['num_edges']}</div><div class="stat-lbl">Relations</div></div>
        <div class="stat-card"><div class="stat-icon">▦</div><div class="stat-val">{stats['density']}</div><div class="stat-lbl">Density</div></div>
        <div class="stat-card"><div class="stat-icon">⊕</div><div class="stat-val">{stats['components']}</div><div class="stat-lbl">Components</div></div>
    </div>
    """, unsafe_allow_html=True)

    CHART_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Mono, monospace", color="#e0ddd6", size=10),
        margin=dict(l=8,r=8,t=36,b=8), showlegend=False,
    )

    def hbar(data, title, color):
        labels = [d[0][:22] for d in data]
        vals   = [round(float(d[1]),4) for d in data]
        max_v  = max(vals) if vals else 1
        opacities = [0.4 + 0.6*(v/max_v) for v in vals]
        fig = go.Figure(go.Bar(
            x=vals, y=labels, orientation="h",
            marker=dict(color=color, opacity=opacities,
                        line=dict(color=color,width=0.5)),
            text=[f"{v:.3f}" for v in vals], textposition="outside",
            textfont=dict(size=9,color="#e0ddd6"),
        ))
        fig.update_layout(
            title=dict(text=title,font=dict(size=11,color="#c9a84c",family="Cinzel, serif")),
            xaxis=dict(showgrid=True,gridcolor="#2a2a3d",zeroline=False),
            yaxis=dict(showgrid=False,autorange="reversed"), **CHART_LAYOUT)
        return fig

    # Row 1 — centrality charts
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(hbar(stats["top_degree"],      "Degree Centrality",      "#c9a84c"),
                        use_container_width=True)
    with c2:
        st.plotly_chart(hbar(stats["top_betweenness"], "Betweenness Centrality", "#e74c3c"),
                        use_container_width=True)
    with c3:
        st.plotly_chart(hbar(stats["top_pagerank"],    "PageRank",               "#3498db"),
                        use_container_width=True)

    # Row 2 — distributions
    c4, c5 = st.columns(2)
    with c4:
        st.markdown('<div class="sec-title"><span>▸</span> Entity Type Distribution</div>',
                    unsafe_allow_html=True)
        dist = stats["entity_dist"]
        labs, vals = list(dist.keys()), list(dist.values())
        cols = [ENTITY_COLORS.get(l,"#7f8c8d") for l in labs]
        fig_pie = go.Figure(go.Pie(
            labels=labs, values=vals, hole=0.42,
            marker=dict(colors=cols, line=dict(color="#0a0a0f",width=2)),
            textfont=dict(family="IBM Plex Mono",size=9),
        ))
        fig_pie.update_layout(**CHART_LAYOUT,
            legend=dict(font=dict(size=9),bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c5:
        st.markdown('<div class="sec-title"><span>▸</span> Relation Type Frequency</div>',
                    unsafe_allow_html=True)
        rdist = stats["relation_dist"]
        items = sorted(rdist.items(), key=lambda x:-x[1])[:12]
        rlabs, rvals = [i[0] for i in items], [i[1] for i in items]
        max_r = max(rvals) if rvals else 1
        fig_vbar = go.Figure(go.Bar(
            x=rlabs, y=rvals,
            marker=dict(color="#9b59b6",
                        opacity=[0.4+0.6*(v/max_r) for v in rvals],
                        line=dict(color="#9b59b6",width=0.5)),
            text=rvals, textposition="outside",
            textfont=dict(size=9,color="#e0ddd6"),
        ))
        fig_vbar.update_layout(
            xaxis=dict(showgrid=False,tickfont=dict(size=8),tickangle=-35),
            yaxis=dict(showgrid=True,gridcolor="#2a2a3d"),
            **CHART_LAYOUT)
        st.plotly_chart(fig_vbar, use_container_width=True)
