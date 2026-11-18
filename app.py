from pathlib import Path
import json
import re
import streamlit as st

BASE = Path(__file__).parent
DATA_PATH = BASE / "hanon_data.json"
LOGO_PATH = BASE / "logo_hanon.png"

st.set_page_config(page_title="Hanon-V", page_icon="📚", layout="wide", initial_sidebar_state="expanded")
with DATA_PATH.open("r", encoding="utf-8") as f:
    DATA = json.load(f)

SEM_COLORS = {
    1: "#6F6298",  # lavanda apagada
    2: "#4E756D",  # salvia
    3: "#9B5E63",  # rosa arcilla
    4: "#536F8F",  # azul grisáceo
    5: "#826A43",  # arena tostada
    6: "#4D777B",  # verde azulado
}

st.markdown(r"""
<style>
:root { color-scheme: light; }
html, body, [data-testid="stAppViewContainer"], .stApp {
  background: #F7F7F3 !important; color: #263448 !important;
}
[data-testid="stHeader"] { background: rgba(247,247,243,.92) !important; }
[data-testid="stSidebar"] {
  background: #EEF0EA !important; border-right: 1px solid #D8DED7;
}
[data-testid="stSidebar"] * { color: #2C3A4B !important; }
.block-container { max-width: 1480px; padding-top: 1.3rem; padding-bottom: 3rem; }
h1,h2,h3,h4 { color: #29394D !important; letter-spacing: -.025em; }
p, li, label, .stMarkdown, .stCaption, [data-testid="stMetricValue"] { color: #344256; }
small, .stCaption { color: #667487 !important; }
a { color: #496F91 !important; text-decoration-thickness: 1px; }
button, [data-testid="baseButton-secondary"], [data-testid="baseButton-primary"] {
  border-radius: 12px !important; border-color: #CAD5D1 !important;
}
[data-testid="stBaseButton-primary"] { background: #6F89A6 !important; color: #fff !important; }
[data-testid="stMetric"] { background: #FFFFFF; border: 1px solid #E0E5DF; padding: .85rem 1rem; border-radius: 16px; box-shadow: 0 3px 12px rgba(39,55,73,.035); }
[data-testid="stExpander"] { background: #FFFFFF; border: 1px solid #E0E5DF; border-radius: 14px; }
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stTextInput"] input { background: #FFFFFF !important; color: #263448 !important; border-color: #CFD8D2 !important; }
[data-testid="stRadio"] label { color: #344256 !important; }
hr { border-color: #E0E5DF !important; }
.hanon-hero {
  position: relative; overflow: hidden; display:flex; align-items:center; gap:1.35rem;
  padding:1.35rem 1.5rem; border-radius:22px; background:linear-gradient(115deg,#FFFFFF 0%,#F0F3EE 68%,#E8EEF0 100%);
  border:1px solid #DCE4DE; box-shadow:0 8px 24px rgba(40,58,76,.055); margin-bottom:1rem;
}
.hanon-hero:after { content:"✦   ·   ○"; position:absolute; right:1.2rem; bottom:.3rem; font-size:2.5rem; color:#D7E0D8; letter-spacing:.25rem; }
.hanon-hero img { width:112px; height:112px; object-fit:cover; border-radius:17px; border:1px solid #D6DFDA; }
.hanon-title { font-size:2.35rem; line-height:1.05; font-weight:800; color:#26384C; margin:0; }
.hanon-subtitle { color:#627286; font-size:1rem; margin-top:.55rem; }
.hanon-kicker { color:#788C83; text-transform:uppercase; letter-spacing:.13em; font-size:.72rem; font-weight:800; }
.hanon-card { background:#FFFFFF; border:1px solid #E0E5DF; border-radius:17px; padding:1rem; min-height:118px; box-shadow:0 3px 12px rgba(39,55,73,.035); }
.semester-chip { display:inline-block; border-radius:12px; padding:.5rem .85rem; color:#fff !important; font-weight:750; letter-spacing:.01em; }
.area-pill { display:inline-block; padding:.28rem .7rem; background:#E8EEE8; color:#536A60; border-radius:999px; font-size:.78rem; font-weight:700; }
.topic-panel { background:#FFFFFF; border:1px solid #E0E5DF; border-radius:18px; padding:1.2rem 1.35rem; box-shadow:0 4px 16px rgba(39,55,73,.035); }
.doodle { color:#AABBB0; font-size:1.35rem; letter-spacing:.5rem; }
.notice { background:#F0F3EE; border-left:4px solid #9BAFA2; border-radius:8px; padding:.85rem 1rem; color:#46576A; }
</style>
""", unsafe_allow_html=True)

RECORDS = DATA["semesters_1_4"]
SEM_DATA = DATA["semesters_5_6"]


def as_list(value):
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def clean_url(value):
    return str(value).rstrip(".,;)")


def show_material(item):
    st.markdown('<div class="topic-panel">', unsafe_allow_html=True)
    st.subheader(item.get("topic", "Tema"))
    st.caption(item.get("course", ""))
    prereq = item.get("prereq", "")
    if prereq:
        st.markdown("**Prerrequisitos**")
        for p in as_list(prereq):
            st.write("• " + str(p))
    for title, key in [("Puntos clave", "points"), ("Fuentes de información", "sources"), ("Videos y recursos de apoyo", "videos")]:
        values = as_list(item.get(key))
        with st.expander(f"{title} · {len(values)}", expanded=(key == "points")):
            if not values:
                st.caption("Este apartado no contiene elementos registrados.")
            for value in values:
                value = str(value)
                urls = re.findall(r"https?://\S+", value)
                if urls:
                    label = value
                    st.markdown(f"• {label}")
                    for url in urls:
                        st.markdown(f"  [Abrir recurso]({clean_url(url)})")
                else:
                    st.write("• " + value)
    st.markdown('</div>', unsafe_allow_html=True)


def group_number(topic):
    m = re.match(r"\s*(\d+)(?:[.:])", str(topic))
    return m.group(1) if m else "Otros"


def records_for_course(semester, course):
    return [r for r in RECORDS if r["semester"] == semester and r["course"] == course]


def search_records(uda_query="", topic_query=""):
    uq = uda_query.casefold().strip()
    tq = topic_query.casefold().strip()
    if not uq and not tq:
        return []
    found = []
    for r in RECORDS:
        uda_text = r.get("course", "").casefold()
        topic_text = " ".join([r.get("topic", ""), str(r.get("prereq", "")),
                                " ".join(map(str, as_list(r.get("points"))))]).casefold()
        if (not uq or uq in uda_text) and (not tq or tq in topic_text):
            found.append((f"Área general · Semestre {r['semester']}", r))
    for sem, areas in SEM_DATA.items():
        for area in areas:
            for uda in area.get("udas", []):
                uda_text = (area["name"] + " " + uda["name"]).casefold()
                topic_text = " ".join(str(t) for b in uda.get("blocks", []) for t in b.get("topics", [])).casefold()
                if (not uq or uq in uda_text) and (not tq or tq in topic_text):
                    item = {"course": uda["name"], "topic": "Temario de " + uda["name"],
                            "prereq": uda.get("prereq", []), "sources": uda.get("sources", []),
                            "points": [t for b in uda.get("blocks", []) for t in b.get("topics", [])],
                            "videos": uda.get("videos", [])}
                    found.append((f"Área propedéutica · Semestre {sem} · {area['name']}", item))
    return found


def bibliography_items():
    # Retain source attribution by semester and UDA, avoiding exact repeated entries within each UDA.
    groups = []
    for sem in range(1, 5):
        for course in sorted({r["course"] for r in RECORDS if r["semester"] == sem}, key=str.casefold):
            vals = []
            for r in RECORDS:
                if r["semester"] == sem and r["course"] == course:
                    vals.extend(as_list(r.get("sources")))
            unique = list(dict.fromkeys(str(v) for v in vals if str(v).strip()))
            if unique:
                groups.append((f"Semestre {sem} · {course}", unique))
    for sem in ("5", "6"):
        for area in SEM_DATA.get(sem, []):
            for uda in area.get("udas", []):
                unique = list(dict.fromkeys(str(v) for v in as_list(uda.get("sources")) if str(v).strip()))
                if unique:
                    groups.append((f"Semestre {sem} · {area['name']} · {uda['name']}", unique))
    return groups


# A home-page semester card can open the corresponding study view directly.
if st.session_state.pop("navigate_to_tema", False):
    st.session_state["page"] = "Temario"
    st.session_state["chosen_semester"] = st.session_state.pop("next_semester", 1)
    st.session_state["semester_radio"] = st.session_state["chosen_semester"]

# Sidebar navigation
st.sidebar.markdown("<div class='hanon-kicker'>Guía local de estudio</div>", unsafe_allow_html=True)
st.sidebar.markdown("## Hanon-V")
page = st.sidebar.radio("Navegación", ["Inicio", "Temario", "Buscador", "Bibliografía", "Agradecimientos"], label_visibility="collapsed", key="page")
st.sidebar.divider()
st.sidebar.caption("Área general")
st.sidebar.caption("Área propedéutica")
st.sidebar.markdown("<div class='doodle'>✧  ◦  ✎  ◦</div>", unsafe_allow_html=True)

# Header shared across pages
logo_col, title_col = st.columns([0.382, 0.618], vertical_alignment="center")
with logo_col:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=118)
with title_col:
    st.markdown("<div class='hanon-kicker'>Programa de consulta · Bachillerato General</div>", unsafe_allow_html=True)
    st.markdown("<div class='hanon-title'>Hanon-V</div>", unsafe_allow_html=True)
    st.markdown("<div class='hanon-subtitle'>Hanon-V: reprobar es fácil si nunca lo has usado</div>", unsafe_allow_html=True)
st.divider()

if page == "Inicio":
    left, right = st.columns([0.618, 0.382], gap="large", vertical_alignment="center")
    with left:
        st.markdown("## Tu temario, organizado para consultar sin perder tiempo")
        st.write("Explora por semestre, UDA, bloque y tema. También puedes buscar conceptos y consultar las fuentes asociadas a cada contenido.")
        st.markdown("<div class='doodle'>✧  📚  ◦  ✎  ◦  ❀</div>", unsafe_allow_html=True)
        st.markdown("<span class='area-pill'>Área general · Semestres 1–4</span> &nbsp; <span class='area-pill'>Área propedéutica · Semestres 5–6</span>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="hanon-card"><div class="hanon-kicker">Hanon-V</div><h3>Una ruta clara para estudiar</h3><p>Seis semestres, sus áreas y sus unidades de aprendizaje organizadas en una sola interfaz.</p><div class="doodle">✦  ◦  ✧</div></div>', unsafe_allow_html=True)
    st.markdown("### Explorar por semestre")
    col_a, col_b = st.columns([0.618, 0.382], gap="medium")
    for i, sem in enumerate(range(1, 7)):
        target = col_a if i % 2 == 0 else col_b
        with target:
            area_name = "Área general" if sem <= 4 else "Área propedéutica"
            st.markdown(f'<div class="hanon-card"><span class="semester-chip" style="background:{SEM_COLORS[sem]}">Semestre {sem}</span><p style="margin:.7rem 0 0;color:#657488">{area_name}</p></div>', unsafe_allow_html=True)
            if st.button(f"Consultar semestre {sem}", key=f"home_sem_{sem}", use_container_width=True):
                st.session_state["next_semester"] = sem
                st.session_state["navigate_to_tema"] = True
                st.rerun()
    st.markdown("### ¿Qué ofrece la consulta?")
    m1, m2, m3 = st.columns(3)
    m1.metric("Semestres", "6")
    m2.metric("Temas en área general", f"{len(RECORDS):,}")
    m3.metric("Áreas propedéuticas", "10")
    st.markdown("### Ahorro potencial por consulta")
    st.write("Estimación orientativa basada en el supuesto indicado para el proyecto: una consulta en Hanon-V puede evitar hasta ocho consultas breves a una IA usadas únicamente para aclarar qué buscar.")
    a, b, c = st.columns(3)
    a.metric("Agua potencialmente evitada", "≈ 2.6 mL", help="8 × 0.322 mL por consulta de IA; estimación de referencia, no medición de Hanon-V.")
    b.metric("Electricidad potencialmente evitada", "≈ 2.7 Wh", help="8 × 0.34 Wh por consulta breve; estimación de referencia.")
    c.metric("Tiempo potencialmente ahorrado", "≈ 16 min", help="8 × 2 minutos, según el supuesto del proyecto.")
    st.caption("No son ahorros medidos por la aplicación. Se estima únicamente el consumo de inferencia de ocho consultas breves de IA que podrían evitarse; no incluye el consumo del dispositivo, la red ni la electricidad y refrigeración del servidor local. El impacto real varía según modelo, longitud de respuesta, centro de datos y método de cálculo.")
    with st.expander("Base de la estimación y fuentes"):
        st.markdown("- **Electricidad:** 0.34 Wh por consulta promedio de ChatGPT, valor citado en la literatura consultada; ocho consultas equivalen a aproximadamente 2.72 Wh.")
        st.markdown("- **Agua:** 0.322 mL por consulta promedio de ChatGPT, cifra publicada y discutida en el estudio consultado; ocho consultas equivalen a aproximadamente 2.576 mL.")
        st.markdown("- **Tiempo:** 2 minutos por consulta, supuesto de este proyecto; ocho consultas equivalen a 16 minutos.")
        st.markdown("Fuentes: [The Hidden Thirst of AI (2026)](https://www.mdpi.com/3042-9242/1/2/8) · [Stanford AI Index Report 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report).")

elif page == "Temario":
    # Golden-ratio split: 38.2% controls and 61.8% study content.
    nav_col, content_col = st.columns([0.382, 0.618], gap="large")
    with nav_col:
        st.markdown("### Semestres")
        sem_options = list(range(1, 7))
        default_sem = int(st.session_state.get("chosen_semester", 1))
        semester = st.radio("Selecciona un semestre", sem_options, index=sem_options.index(default_sem) if default_sem in sem_options else 0,
                            format_func=lambda n: f"Semestre {n}", key="semester_radio")
        st.session_state["chosen_semester"] = semester
        color = SEM_COLORS[semester]
        area_label = "Área general" if semester <= 4 else "Área propedéutica"
        st.markdown(f'<span class="semester-chip" style="background:{color}">Semestre {semester}</span> &nbsp; <span class="area-pill">{area_label}</span>', unsafe_allow_html=True)
        if semester <= 4:
            sem_items = [r for r in RECORDS if r["semester"] == semester]
            courses = sorted({r["course"] for r in sem_items}, key=str.casefold)
            course = st.selectbox("Buscar UDA / seleccionar UDA", courses, key=f"course_select_{semester}")
            course_items = [r for r in sem_items if r["course"] == course]
            blocks = {}
            for item in course_items:
                blocks.setdefault(group_number(item["topic"]), []).append(item)
            block_names = list(blocks)
            if len(block_names) > 1 or (block_names and block_names[0] != "Otros"):
                block = st.selectbox("Bloque", block_names, format_func=lambda x: f"Bloque {x}" if x != "Otros" else "Otros temas", key=f"block_{semester}_{course}")
                topic_items = blocks[block]
            else:
                topic_items = course_items
            topic_names = [x["topic"] for x in topic_items]
            chosen_topic = st.selectbox("Tema", topic_names, key=f"topic_{semester}_{course}_{block_names[0] if block_names else 'none'}")
            selected = next(x for x in topic_items if x["topic"] == chosen_topic)
        else:
            areas = SEM_DATA[str(semester)]
            area_names = [a["name"] for a in areas]
            area = st.selectbox("Área propedéutica", area_names, key=f"area_{semester}")
            area_data = next(a for a in areas if a["name"] == area)
            udas = area_data["udas"]
            uda_names = [u["name"] for u in udas]
            uda_name = st.selectbox("UDA", uda_names, key=f"uda_{semester}_{area}")
            uda = next(u for u in udas if u["name"] == uda_name)
            blocks = uda.get("blocks", [])
            block_names = [b["name"] for b in blocks]
            if block_names:
                block_name = st.selectbox("Bloque", block_names, key=f"block_{semester}_{area}_{uda_name}")
                block_data = next(b for b in blocks if b["name"] == block_name)
                topic = st.selectbox("Tema", block_data.get("topics", []), key=f"topic_{semester}_{area}_{uda_name}_{block_name}")
                selected = {"course": uda_name, "topic": topic, "prereq": uda.get("prereq", []), "sources": uda.get("sources", []),
                            "points": [topic], "videos": uda.get("videos", [])}
            else:
                selected = {"course": uda_name, "topic": uda_name, "prereq": uda.get("prereq", []), "sources": uda.get("sources", []), "points": [], "videos": uda.get("videos", [])}
    with content_col:
        st.markdown("### Contenido de estudio")
        if semester <= 4:
            st.caption(f"Área general · Semestre {semester} · {selected.get('course','')}")
            show_material(selected)
        else:
            st.caption(f"Área propedéutica · Semestre {semester} · {area}")
            st.markdown(f"**{selected.get('course','')}**")
            st.markdown(f"**Prerrequisitos**")
            for p in as_list(selected.get("prereq")): st.write("• " + str(p))
            st.markdown("**Tema seleccionado**")
            st.write(selected.get("topic", ""))
            with st.expander("Fuentes de consulta", expanded=True):
                for s in as_list(selected.get("sources")): st.write("• " + str(s))
            with st.expander("Videos y recursos de apoyo"):
                for v in as_list(selected.get("videos")):
                    st.write("• " + str(v))

elif page == "Buscador":
    left, right = st.columns([0.382, 0.618], gap="large")
    with left:
        st.markdown("### Buscar UDA")
        uda_query = st.text_input("Nombre de la UDA", placeholder="Ej. Biología, Física, Ética…")
        st.markdown("### Buscar tema")
        topic_query = st.text_input("Tema o concepto", placeholder="Ej. derivadas, Porfiriato, fotosíntesis…")
        results = search_records(uda_query, topic_query)
        st.caption(f"{len(results)} coincidencias")
        if results:
            labels = [f"{where} · {item.get('course','')} — {item.get('topic','')}" for where, item in results[:100]]
            choice = st.selectbox("Resultados", labels)
            selected_idx = labels.index(choice)
            selected_where, selected_item = results[selected_idx]
        else:
            selected_where, selected_item = None, None
            if query: st.info("No se encontraron coincidencias. Prueba con otra palabra o parte del título.")
    with right:
        st.markdown("### Resultado")
        if selected_item:
            st.caption(selected_where)
            show_material(selected_item)
        else:
            st.markdown('<div class="notice">Los resultados aparecerán aquí. Puedes buscar por nombre de UDA, tema o concepto; si llenas ambos campos, se aplicarán los dos criterios.</div>', unsafe_allow_html=True)

elif page == "Bibliografía":
    st.markdown("## Programa Bachillerato General Plan 2020 de la Universidad de Guanajuato")
    st.markdown('<span class="area-pill">Nuestro temario está basado en el Programa Bachillerato General Plan 2020 de la Universidad de Guanajuato.</span>', unsafe_allow_html=True)
    st.markdown("Nuestro temario está basado en el Programa Bachillerato General Plan 2020 de la Universidad de Guanajuato. Este proyecto no es un material didáctico oficial de la Universidad de Guanajuato, sino un trabajo independiente que sirva como apoyo para sus estudiantes, pues no tiene fines lucrativos. Todos los derechos del temario le pertenecen a la Universidad de Guanajuato.")
    st.divider()
    st.markdown("### Fuentes y bibliografía por semestre y UDA")
    st.caption("Se muestran las fuentes y libros vinculados a los contenidos registrados en el programa. Las referencias se conservan tal como aparecen en los datos fuente.")
    groups = bibliography_items()
    for label, sources in groups:
        with st.expander(f"{label} · {len(sources)} fuentes"):
            for source in sources:
                urls = re.findall(r"https?://\S+", source)
                st.markdown("• " + source)
                for url in urls:
                    st.markdown(f"  [Abrir fuente]({clean_url(url)})")

elif page == "Agradecimientos":
    st.markdown("## Agradecimientos")
    jose_url = "https://inba.gob.mx/multimedia/prensa/galerias/13055/13055-IMG_BG_POST-jose_jose_%C2%A9cortesia_sony_music.jpg"
    try:
        st.image(jose_url, width=260, caption="José José · Fotografía cortesía de Sony Music, difundida por el INBAL.")
    except Exception:
        st.markdown("[Consultar fotografía de José José en el sitio del INBAL](https://inba.gob.mx/prensa/13055/jose-jose-uno-de-los-mas-grandes-interpretes-de-mexico)")
    st.markdown("De parte del programador y director de este humilde proyecto:")
    st.markdown("> «Deseo agradecer este trabajo a todos nuestros colaboradores e involucrados en la realización del mismo, que si bien tuvimos jornadas laborales bastante pesadas y donde nuestro horario de sueño cayó más rápido que la bolsa de valores en 1929, logramos concluir exitosamente este trabajo.")
    st.markdown("«Asimismo, deseo extender mis agradecimientos personales hacia José Rómulo Sosa Ortiz, mejor conocido como el Príncipe de la Canción José José, que sin su música hubiera sido un martirio programar esta guía de estudio; también agradezco a todos los demás artistas que me acompañaron de forma consciente o fortuita, pues no tengo Spotify Premium y se colaban varios artistas. Y sobre todo, a ti, alumno que está leyendo esto, pues para ti se ha diseñado este proyecto. Se les quiere, aunque posiblemente estén reprobando medio semestre <3. Arthur».")

st.divider()
st.caption("Hanon-V · Proyecto independiente de consulta académica · Interfaz local")
