"""
Path KG — AI-навигатор по госуслугам Кыргызстана
Streamlit фронтенд — финальная версия
"""

import streamlit as st
import sys
import os

st.set_page_config(
    page_title="Path KG — Навигатор госуслуг",
    page_icon="🇰🇬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #1A1A2E; }
.stApp { background: #F5F7FA; color: #1A1A2E; }

section[data-testid="stSidebar"] {
    background: #0C2D6B !important;
    border-right: none;
    box-shadow: 2px 0 12px rgba(12,45,107,0.15);
}
section[data-testid="stSidebar"] * { color: #D6E4FF !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(201,168,76,0.35) !important; }
.sidebar-gold-line { height: 2px; background: linear-gradient(90deg, #C9A84C, transparent); margin: 12px 0; border-radius: 1px; }

.brand-header { font-family: 'Playfair Display', serif; font-size: 1.9rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.01em; line-height: 1.1; }
.brand-header span { color: #C9A84C; }
.brand-tagline { font-size: 0.7rem; color: rgba(214,228,255,0.6); letter-spacing: 0.18em; text-transform: uppercase; margin-top: 5px; }

section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.08) !important;
    color: #D6E4FF !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 9px 14px !important;
    text-align: left !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(201,168,76,0.18) !important;
    border-color: #C9A84C !important;
    color: #FFFFFF !important;
}

.main .stButton > button, .block-container .stButton > button {
    background: #FFFFFF !important;
    color: #0C2D6B !important;
    border: 1px solid #DDE3EE !important;
    border-radius: 10px !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    text-align: left !important;
    transition: all 0.2s !important;
    width: 100% !important;
    white-space: pre-wrap !important;
    line-height: 1.5 !important;
}
.main .stButton > button:hover, .block-container .stButton > button:hover {
    background: #E3F0FF !important;
    border-color: #1565C0 !important;
}

.badge { display: inline-block; padding: 3px 11px; border-radius: 4px; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }
.badge-full    { background: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }
.badge-partial { background: #FFF8E1; color: #F57F17; border: 1px solid #FFE082; }
.badge-offline { background: #ECEFF1; color: #546E7A; border: 1px solid #CFD8DC; }

.readiness-bar-wrap { background: #DDE3EE; border-radius: 6px; height: 8px; width: 100%; overflow: hidden; margin: 8px 0; }
.readiness-bar-fill { height: 100%; border-radius: 6px; }
.readiness-label { font-size: 0.72rem; color: #546E7A; margin-bottom: 3px; font-weight: 500; }

.step-item { display: flex; gap: 14px; align-items: flex-start; margin-bottom: 14px; }
.step-num { width: 28px; height: 28px; min-width: 28px; border-radius: 50%; background: #0C2D6B; color: #FFFFFF; font-size: 0.72rem; font-weight: 700; display: flex; align-items: center; justify-content: center; margin-top: 1px; }
.step-text { font-size: 0.86rem; color: #374151; line-height: 1.6; }

.tariff-row { display: flex; justify-content: space-between; padding: 9px 14px; border-radius: 6px; margin-bottom: 3px; font-size: 0.83rem; border: 1px solid #DDE3EE; }
.tariff-row:nth-child(odd)  { background: #FFFFFF; }
.tariff-row:nth-child(even) { background: #F5F7FA; }
.tariff-row .t-цена { color: #1565C0; font-weight: 600; }

.chip { display: inline-block; padding: 5px 13px; border-radius: 4px; font-size: 0.74rem; margin: 3px 4px 3px 0; font-weight: 500; }
.chip-ok      { background:#E8F5E9; color:#2E7D32; border:1px solid #A5D6A7; }
.chip-missing { background:#FFEBEE; color:#C62828; border:1px solid #FFCDD2; }
.chip-neutral { background:#E8EAF6; color:#3949AB; border:1px solid #C5CAE9; }

.next-banner { background: linear-gradient(135deg, #E3F0FF, #EEF4FF); border: 1px solid #90CAF9; border-left: 4px solid #1565C0; border-radius: 8px; padding: 14px 18px; margin: 12px 0; }
.next-banner-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.14em; color: #1565C0; font-weight: 700; margin-bottom: 5px; }
.next-banner-text  { font-size: 0.92rem; color: #0C2D6B; font-weight: 500; }

.savings-banner { background: linear-gradient(135deg, #E8F5E9, #F1F8E9); border: 1px solid #A5D6A7; border-left: 4px solid #2E7D32; border-radius: 8px; padding: 12px 18px; margin: 10px 0; font-size: 0.88rem; color: #1B5E20; font-weight: 500; }

.special-cases { background: #FFF8E1; border-left: 3px solid #F57F17; border-radius: 0 8px 8px 0; padding: 12px 16px; font-size: 0.82rem; color: #4E342E; line-height: 1.6; margin: 10px 0; }
.special-cases-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: #E65100; font-weight: 700; margin-bottom: 6px; }

.info-row { display: flex; gap: 10px; margin-bottom: 10px; align-items: center; padding: 8px 12px; background: #FFFFFF; border-radius: 8px; border: 1px solid #DDE3EE; }
.info-label { font-size: 0.68rem; color: #78909C; min-width: 76px; text-transform: uppercase; letter-spacing: 0.07em; font-weight: 600; }
.info-value { font-size: 0.87rem; color: #1A1A2E; font-weight: 500; }

.ai-summary { background: #FFFFFF; border-left: 4px solid #C9A84C; border-radius: 0 10px 10px 0; padding: 16px 20px; font-size: 0.88rem; color: #374151; line-height: 1.7; }

.section-heading { font-size: 0.68rem; letter-spacing: 0.16em; text-transform: uppercase; color: #78909C; margin: 22px 0 10px; font-weight: 700; border-bottom: 1px solid #DDE3EE; padding-bottom: 6px; }

.path-chain { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: 0.78rem; color: #78909C; margin: 6px 0 14px; }
.path-chain .arrow { color: #B0BEC5; font-weight: 700; }
.path-chain .node  { background: #ECEFF1; border-radius: 4px; padding: 3px 10px; color: #546E7A; border: 1px solid #CFD8DC; }
.path-chain .node-final { background: #E3F0FF; border-radius: 4px; padding: 3px 10px; color: #1565C0; border: 1px solid #90CAF9; font-weight: 600; }

.org-card { background: #FFFFFF; border: 1px solid #DDE3EE; border-radius: 8px; padding: 10px 14px; margin-bottom: 6px; }

.welcome-hero {
    background: linear-gradient(135deg, #0C2D6B 0%, #1A3F7A 60%, #1565C0 100%);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.welcome-hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(201,168,76,0.08);
}
.welcome-hero::after {
    content: '';
    position: absolute;
    bottom: -60px; right: 60px;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.welcome-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.25;
    margin-bottom: 12px;
}
.welcome-title span { color: #C9A84C; }
.welcome-desc {
    font-size: 0.95rem;
    color: rgba(214,228,255,0.85);
    line-height: 1.65;
    max-width: 560px;
    margin-bottom: 22px;
}
.welcome-badges { display: flex; flex-wrap: wrap; gap: 10px; }
.w-badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(201,168,76,0.4);
    border-radius: 20px;
    padding: 5px 16px;
    font-size: 0.75rem;
    color: #C9A84C;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.w-badge-white {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 5px 16px;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.85);
    font-weight: 500;
}

.about-lead {
    font-size: 1.05rem;
    color: #546E7A;
    line-height: 1.75;
    max-width: 680px;
    margin-bottom: 32px;
}
.about-lead strong { color: #0C2D6B; }

.tech-card {
    background: #FFFFFF;
    border: 1px solid #DDE3EE;
    border-top: 3px solid #1565C0;
    border-radius: 12px;
    padding: 22px 20px;
    height: 100%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.tech-card-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #0C2D6B;
    margin-bottom: 8px;
}
.tech-card-desc {
    font-size: 0.8rem;
    color: #546E7A;
    line-height: 1.6;
}

.impact-row { display: flex; gap: 16px; flex-wrap: wrap; margin: 28px 0; }
.impact-item {
    background: #FFFFFF;
    border: 1px solid #DDE3EE;
    border-radius: 12px;
    padding: 18px 22px;
    flex: 1;
    min-width: 140px;
    text-align: center;
}
.impact-num { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #0C2D6B; }
.impact-num span { color: #C9A84C; }
.impact-label { font-size: 0.75rem; color: #78909C; margin-top: 4px; font-weight: 500; }

.how-step {
    display: flex;
    gap: 16px;
    align-items: flex-start;
    padding: 16px 0;
    border-bottom: 1px solid #EEF2F7;
}
.how-step:last-child { border-bottom: none; }
.how-step-num {
    width: 36px; height: 36px; min-width: 36px;
    border-radius: 50%;
    background: #0C2D6B;
    color: #C9A84C;
    font-size: 0.9rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
}
.how-step-title { font-size: 0.92rem; font-weight: 600; color: #0C2D6B; margin-bottom: 4px; }
.how-step-desc  { font-size: 0.82rem; color: #546E7A; line-height: 1.55; }

.chat-msg-user      { background: #E3F0FF; border-radius: 12px 12px 4px 12px; padding: 10px 14px; margin: 6px 0; font-size: 0.86rem; color: #0C2D6B; max-width: 85%; margin-left: auto; }
.chat-msg-assistant { background: #FFFFFF; border: 1px solid #DDE3EE; border-radius: 12px 12px 12px 4px; padding: 10px 14px; margin: 6px 0; font-size: 0.86rem; color: #374151; max-width: 90%; }
.chat-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: #B0BEC5; margin-bottom: 3px; font-weight: 600; }

div[data-testid="stTextInput"] > div > div > input {
    background: #F5F7FA !important;
    border: 1px solid #DDE3EE !important;
    color: #1A1A2E !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
}
div[data-testid="stTextInput"] > div > div > input::placeholder { color: #9CA3AF !important; }
div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #1565C0 !important;
    box-shadow: 0 0 0 3px rgba(21,101,192,0.1) !important;
    background: #FFFFFF !important;
}
section[data-testid="stSidebar"] div[data-testid="stTextInput"] > div > div > input {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(201,168,76,0.4) !important;
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] div[data-testid="stTextInput"] > div > div > input::placeholder { color: rgba(214,228,255,0.5) !important; }
section[data-testid="stSidebar"] div[data-testid="stTextInput"] > div > div > input:focus { border-color: #C9A84C !important; box-shadow: none !important; }
div[data-testid="stMultiSelect"] * { font-size: 0.83rem !important; }
div[data-testid="stExpander"] { background: #FFFFFF !important; border: 1px solid #DDE3EE !important; border-radius: 10px !important; }

.empty-state { margin-top: 20px; text-align: center; color: #B0BEC5; }
.empty-state-icon { font-size: 3rem; margin-bottom: 16px; opacity: 0.4; }
.empty-state-text { font-size: 1rem; color: #78909C; font-family: 'Playfair Display', serif; }

hr { border-color: rgba(201,168,76,0.3) !important; }

div[data-testid="stTabs"] button {
    color: #78909C !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #0C2D6B !important;
    border-bottom: 2px solid #0C2D6B !important;
    font-weight: 600 !important;
}
div[data-testid="stTabs"] button:hover {
    color: #1565C0 !important;
    border-bottom-color: #1565C0 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<script>
function activateTabFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const tab = urlParams.get('tab');
    if (!tab) return;
    const tabsContainer = document.querySelector('[data-testid="stTabs"]');
    if (!tabsContainer) return;
    const buttons = tabsContainer.querySelectorAll('button');
    let index = -1;
    if (tab === 'nav') index = 0;
    else if (tab === 'chat') index = 1;
    else if (tab === 'form') index = 2;
    else if (tab === 'about') index = 3;
    if (index >= 0 && buttons[index] && !buttons[index].classList.contains('active')) {
        buttons[index].click();
    }
}
window.addEventListener('load', activateTabFromUrl);
new MutationObserver(activateTabFromUrl).observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

try:
    from main import (
        detect_service, analyze_service, format_answer,
        get_next_step, SERVICES,
    )
    from k_g import get_plan, G
    BACKEND_OK = True
    _import_error = None
    try:
        from main import chat_answer
    except ImportError:
        chat_answer = None
    try:
        from main import get_life_situations
    except ImportError:
        get_life_situations = None
    try:
        from main import get_savings_message
    except ImportError:
        get_savings_message = None
    from pdf_filler import fill_sti_163
except ImportError as e:
    BACKEND_OK = False
    _import_error = str(e)

def badge_html(status: str) -> str:
    mapping = {
        "Full":    ("badge-full",    "✓ Онлайн"),
        "Partial": ("badge-partial", "◐ Частично"),
        "Offline": ("badge-offline", "⊘ Лично"),
    }
    cls, label = mapping.get(status, ("badge-offline", status))
    return f'<span class="badge {cls}">{label}</span>'

def readiness_bar(pct: int) -> str:
    color = "#2E7D32" if pct >= 80 else ("#F57F17" if pct >= 40 else "#C62828")
    return f"""
    <div class="readiness-label">Готовность: <strong style="color:{color}">{pct}%</strong></div>
    <div class="readiness-bar-wrap">
        <div class="readiness-bar-fill" style="width:{pct}%; background:{color};"></div>
    </div>"""

def render_steps(steps: list):
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
        <div class="step-item">
            <div class="step-num">{i}</div>
            <div class="step-text">{step}</div>
        </div>""", unsafe_allow_html=True)

def render_tariffs(tariffs: list):
    st.markdown('<div class="section-heading">Тарифы</div>', unsafe_allow_html=True)
    rows = ""
    for t in tariffs:
        rows += f'<div class="tariff-row"><span>{t.get("срок","")}</span><span class="t-цена">{t.get("цена","")}</span></div>'
    st.markdown(rows, unsafe_allow_html=True)

def render_path(path: list):
    if not path:
        return
    st.markdown('<div class="section-heading">Путь к услуге</div>', unsafe_allow_html=True)
    chain_html = '<div class="path-chain">'
    for i, name in enumerate(path):
        cls = "node-final" if i == len(path) - 1 else "node"
        chain_html += f'<span class="{cls}">{name}</span>'
        if i < len(path) - 1:
            chain_html += '<span class="arrow">→</span>'
    chain_html += "</div>"
    st.markdown(chain_html, unsafe_allow_html=True)

def render_doc_chips(has_docs, missing_docs):
    html = ""
    for d in has_docs:
        html += f'<span class="chip chip-ok">✓ {d}</span>'
    for d in missing_docs:
        html += f'<span class="chip chip-missing">✗ {d}</span>'
    if html:
        st.markdown(html, unsafe_allow_html=True)

def render_info_row(icon, label, value):
    st.markdown(f"""
    <div class="info-row">
        <span style="font-size:1rem;width:22px;text-align:center;">{icon}</span>
        <span class="info-label">{label}</span>
        <span class="info-value">{value}</span>
    </div>""", unsafe_allow_html=True)

def render_checklist_copy(service_name: str, has_docs: list, missing_docs: list):
    lines = [f"Чеклист для: {service_name}", ""]
    if has_docs:
        lines.append("Уже есть:")
        for d in has_docs:
            lines.append(f"  ✓ {d}")
        lines.append("")
    if missing_docs:
        lines.append("Нужно получить:")
        for d in missing_docs:
            lines.append(f"  ☐ {d}")
    with st.expander("Скопировать чеклист документов"):
        st.code("\n".join(lines), language=None)

defaults = {
    "selected_service":   None,
    "analysis":           None,
    "ai_summary":         None,
    "user_docs":          [],
    "query":              "",
    "chat_history":       [],
    "selected_situation": None,
    "form_data":          {},
    "form_step":          0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 20px;">
        <div class="brand-header">Path<span>KG</span></div>
        <div class="brand-tagline">Твой путь в госуслугах</div>
        <div class="sidebar-gold-line" style="margin-top:14px;"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-heading">Поиск</div>', unsafe_allow_html=True)
    query = st.text_input(
        "Что вам нужно?",
        value=st.session_state.query,
        placeholder="Например: хочу открыть ИП...",
        label_visibility="collapsed",
    )
    if st.button("Найти услугу"):
        if query.strip() and BACKEND_OK:
            with st.spinner("Определяю..."):
                sid = detect_service(query)
            if sid:
                st.session_state.selected_service   = sid
                st.session_state.query              = query
                st.session_state.analysis           = None
                st.session_state.ai_summary         = None
                st.session_state.selected_situation = None
                st.query_params.tab = "nav"
                st.rerun()
            else:
                st.warning("Не удалось определить услугу. Выберите из списка.")
        elif not BACKEND_OK:
            st.error(f"Ошибка импорта: {_import_error}")

    st.markdown("---")

    st.markdown('<div class="section-heading">Мои документы</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.72rem;color:rgba(214,228,255,0.55);margin-bottom:8px;">Отметьте что уже есть — система пересчитает готовность</div>', unsafe_allow_html=True)
    all_doc_options = [
        "ID-карта (паспорт)",
        "Медсправка о рождении (№103/у)",
        "Свидетельство о браке",
        "Техпаспорт/Договор на жильё",
        "Заявление STI-163",
        "Облачная ЭЦП",
        "Свидетельство о рождении",
        "Нотариальное согласие родителя",
    ]
    selected_docs = st.multiselect(
        "Документы при себе",
        options=all_doc_options,
        default=st.session_state.user_docs,
        label_visibility="collapsed",
    )
    if selected_docs != st.session_state.user_docs:
        st.session_state.user_docs = selected_docs
        st.session_state.analysis  = None
        st.session_state.ai_summary = None

    st.markdown("---")

    st.markdown('<div class="section-heading">Все услуги</div>', unsafe_allow_html=True)
    if BACKEND_OK:
        for sid in SERVICES:
            node = G.nodes.get(sid, {})
            name = node.get("name", SERVICES[sid])
            if st.button(name, key=f"svc_{sid}", use_container_width=True):
                st.session_state.selected_service   = sid
                st.session_state.analysis           = None
                st.session_state.ai_summary         = None
                st.session_state.selected_situation = None
                st.query_params.tab = "nav"
                st.rerun()

if not BACKEND_OK:
    st.error(f"Не удалось загрузить бэкенд: `{_import_error}`")
    st.stop()

if "tab" not in st.query_params:
    st.query_params.tab = "nav"

tab_nav, tab_chat, tab_form, tab_about = st.tabs(["Навигатор", "Чат-помощник", "Заполнить заявление", "О проекте"])

with tab_nav:
    if not st.session_state.selected_service:
        st.markdown("""
        <div class="welcome-hero">
            <div class="welcome-title">
                Навигатор по госуслугам <span>КР</span>
            </div>
            <div class="welcome-desc">
                Точные маршруты оформления документов на основе граф-базы данных.
                Актуальные сроки, стоимость и адреса. Без галлюцинаций —
                только верифицированные данные.<br>
                <strong>Твой путь в госуслугах</strong>
            </div>
            <div class="welcome-badges">
                <span class="w-badge">Knowledge Graph</span>
                <span class="w-badge-white">8 услуг КР</span>
                <span class="w-badge-white">Актуально на март 2026</span>
                <span class="w-badge-white">Кыргызча / Русский</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:0.72rem;letter-spacing:0.16em;text-transform:uppercase;
                    color:#78909C;font-weight:700;border-bottom:1px solid #DDE3EE;
                    padding-bottom:6px;margin-bottom:16px;">
            Что вам нужно сделать?
        </div>
        """, unsafe_allow_html=True)

        LIFE_SITUATIONS = [
            {"id": "baby", "name": "Родился ребёнок", "desc": "Свидетельство, ПИН, прописка", "services": ["s_birth_reg", "s_balagа_benefit", "s_propiska_online"]},
            {"id": "travel", "name": "Выехать за рубеж", "desc": "ID-карта, загранпаспорт", "services": ["s_id_first", "s_zagran_get"]},
            {"id": "business", "name": "Открыть бизнес", "desc": "Регистрация ИП онлайн", "services": ["s_id_first", "s_ip_register"]},
            {"id": "move", "name": "Переезд / новая прописка", "desc": "Прописка онлайн или через ЦОН", "services": ["s_ecp", "s_propiska_online", "s_propiska_offline"]},
            {"id": "first_id", "name": "Исполнилось 16 лет", "desc": "Первая ID-карта", "services": ["s_id_first"]},
        ]

        if get_life_situations and BACKEND_OK:
            try:
                life_sits = get_life_situations()
                for ls in life_sits:
                    ls.pop("emoji", None)
            except Exception:
                life_sits = LIFE_SITUATIONS
        else:
            life_sits = LIFE_SITUATIONS

        ls_cols = st.columns(len(life_sits))
        for i, ls in enumerate(life_sits):
            with ls_cols[i]:
                label = f"{ls['name']}\n{ls.get('desc','')}"
                if st.button(label, key=f"ls_{ls['id']}", use_container_width=True):
                    st.session_state.selected_situation = ls
                    st.rerun()

        if st.session_state.selected_situation:
            ls = st.session_state.selected_situation
            st.markdown("---")
            st.markdown(f"""
            <div style="font-family:'Playfair Display',serif;font-size:1.15rem;color:#0C2D6B;margin:16px 0 4px;">
                {ls['name']}
            </div>
            <div style="font-size:0.82rem;color:#78909C;margin-bottom:16px;">{ls.get('desc','')}</div>
            """, unsafe_allow_html=True)

            for step_num, svc_id in enumerate(ls.get("services", []), 1):
                node = G.nodes.get(svc_id, {})
                svc_name = node.get("name", svc_id)
                svc_срок = node.get("срок", "—")
                svc_цена = node.get("стоимость", "—")
                svc_stat = node.get("status_digital", "Offline")

                col_info, col_btn = st.columns([5, 2])
                with col_info:
                    st.markdown(f"""
                    <div style="display:flex;align-items:flex-start;gap:12px;padding:12px 14px;
                                background:#FFFFFF;border:1px solid #DDE3EE;border-radius:10px;margin-bottom:8px;">
                        <div style="width:26px;height:26px;min-width:26px;border-radius:50%;
                                    background:#0C2D6B;color:#fff;font-size:0.72rem;font-weight:700;
                                    display:flex;align-items:center;justify-content:center;margin-top:2px;">
                            {step_num}
                        </div>
                        <div>
                            <div style="font-size:0.9rem;font-weight:600;color:#0C2D6B;">{svc_name}</div>
                            <div style="font-size:0.75rem;color:#78909C;margin-top:3px;">
                                {badge_html(svc_stat)} &nbsp; {svc_срок} &nbsp;|&nbsp; {svc_цена}
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with col_btn:
                    if st.button("Открыть →", key=f"ls_open_{svc_id}_{step_num}", use_container_width=True):
                        st.session_state.selected_service   = svc_id
                        st.session_state.analysis           = None
                        st.session_state.ai_summary         = None
                        st.session_state.selected_situation = None
                        st.query_params.tab = "nav"
                        st.rerun()

            if st.button("← Назад к ситуациям", key="ls_back"):
                st.session_state.selected_situation = None
                st.rerun()
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🇰🇬</div>
                <div class="empty-state-text">Или выберите услугу из списка слева</div>
                <div style="font-size:0.76rem;color:#B0BEC5;margin-top:6px;">Либо введите запрос: «хочу загранпаспорт»</div>
            </div>
            """, unsafe_allow_html=True)

    else:
        sid = st.session_state.selected_service
        if st.session_state.analysis is None:
            with st.spinner("Анализирую..."):
                st.session_state.analysis = analyze_service(sid, st.session_state.user_docs)
        data = st.session_state.analysis

        if "error" in data:
            st.error(data["error"])
        else:
            col_name, col_badge = st.columns([5, 2])
            with col_name:
                st.markdown(f"""
                <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:#0C2D6B;margin-bottom:4px;">
                    {data.get('service_name','')}
                </div>""", unsafe_allow_html=True)
            with col_badge:
                st.markdown(
                    f'<div style="padding-top:6px;text-align:right;">{badge_html(data.get("digital_status",""))}</div>',
                    unsafe_allow_html=True,
                )

            if data.get("desc"):
                st.markdown(f'<div style="font-size:0.83rem;color:#546E7A;margin-bottom:12px;">{data["desc"]}</div>', unsafe_allow_html=True)

            st.markdown(readiness_bar(data.get("readiness_pct", 0)), unsafe_allow_html=True)

            if get_savings_message and data.get("is_ready"):
                try:
                    savings = get_savings_message(sid, data.get("is_ready", False))
                    if savings:
                        st.markdown(f'<div class="savings-banner">{savings}</div>', unsafe_allow_html=True)
                except Exception:
                    pass

            if data.get("next_step"):
                st.markdown(f"""
                <div class="next-banner">
                    <div class="next-banner-label">Следующий шаг</div>
                    <div class="next-banner-text">{data['next_step']}</div>
                </div>""", unsafe_allow_html=True)

            if data.get("explanation"):
                st.markdown(
                    f'<div style="font-size:0.8rem;color:#E65100;margin:4px 0 10px;padding:8px 12px;background:#FFF3E0;border-radius:6px;border-left:3px solid #FF8F00;">{data["explanation"]}</div>',
                    unsafe_allow_html=True,
                )

            st.markdown('<div class="section-heading">AI-сводка</div>', unsafe_allow_html=True)
            if st.session_state.ai_summary:
                st.markdown(f'<div class="ai-summary">{st.session_state.ai_summary}</div>', unsafe_allow_html=True)
            else:
                col_btn, col_hint = st.columns([2, 5])
                with col_btn:
                    if st.button("Сгенерировать сводку"):
                        with st.spinner("Генерирую..."):
                            st.session_state.ai_summary = format_answer(data)
                        st.rerun()
                with col_hint:
                    st.markdown('<span style="color:#78909C;font-size:0.78rem;">Краткое AI-объяснение</span>', unsafe_allow_html=True)

            st.markdown("---")
            left_col, right_col = st.columns([3, 2])

            with left_col:
                render_path(data.get("path_to_service", []))
                st.markdown('<div class="section-heading">Документы</div>', unsafe_allow_html=True)
                render_doc_chips(data.get("has_docs", []), data.get("missing_docs", []))
                if data.get("has_docs") or data.get("missing_docs"):
                    render_checklist_copy(
                        data.get("service_name", ""),
                        data.get("has_docs", []),
                        data.get("missing_docs", []),
                    )
                if data.get("blocking_services"):
                    st.markdown('<div class="section-heading">Необходимые услуги</div>', unsafe_allow_html=True)
                    for b in data["blocking_services"]:
                        name = b["name"] if isinstance(b, dict) else b
                        st.markdown(f'<span class="chip chip-missing">✗ {name}</span>', unsafe_allow_html=True)
                elif data.get("depends_on"):
                    st.markdown('<div class="section-heading">Связанные услуги</div>', unsafe_allow_html=True)
                    for dep in data["depends_on"]:
                        name = dep["name"] if isinstance(dep, dict) else dep
                        st.markdown(f'<span class="chip chip-neutral">→ {name}</span>', unsafe_allow_html=True)
                if data.get("шаги"):
                    with st.expander("Пошаговая инструкция", expanded=True):
                        render_steps(data["шаги"])

            with right_col:
                st.markdown('<div class="section-heading">Детали</div>', unsafe_allow_html=True)
                render_info_row("", "Срок",      data.get("срок", "—"))
                render_info_row("", "Стоимость", data.get("стоимость", "—"))
                render_info_row("", "Место",     data.get("место", "—"))
                render_info_row("", "Часы",      data.get("work_hours", "—"))
                if data.get("org"):
                    st.markdown('<div class="section-heading">Организации</div>', unsafe_allow_html=True)
                    for org in data["org"]:
                        st.markdown(f"""
                        <div class="org-card">
                            <div style="font-size:0.83rem;color:#0C2D6B;font-weight:500;">{org['name']}</div>
                            <div style="font-size:0.72rem;color:#78909C;margin-top:3px;">{org.get('address','')}</div>
                        </div>""", unsafe_allow_html=True)
                if data.get("тарифы"):
                    render_tariffs(data["тарифы"])
                if data.get("procedures"):
                    st.markdown('<div class="section-heading">Процедуры</div>', unsafe_allow_html=True)
                    for p in data["procedures"]:
                        name = p["name"] if isinstance(p, dict) else p
                        st.markdown(f'<span class="chip chip-neutral">⚙ {name}</span>', unsafe_allow_html=True)

with tab_chat:
    st.markdown("""
    <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;
                color:#0C2D6B;margin-bottom:4px;">Чат-помощник</div>
    <div style="font-size:0.83rem;color:#546E7A;margin-bottom:20px;border-bottom:2px solid #C9A84C;padding-bottom:12px;">
        Задайте вопрос о госуслугах. Отвечаю на основе графа знаний КР и помню контекст разговора.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="chat-label">Вы</div>'
                    f'<div class="chat-msg-user">{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="chat-label">GovNav</div>'
                    f'<div class="chat-msg-assistant">{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")
    user_question = st.text_input(
        "Ваш вопрос:",
        key="chat_input",
        placeholder="Например: можно ли получить загранпаспорт без родителей?",
    )

    col_ask, col_clear = st.columns([3, 1])
    with col_ask:
        ask_clicked = st.button("Спросить", key="ask_btn")
    with col_clear:
        if st.button("Очистить", key="clear_btn"):
            st.session_state.chat_history = []
            st.rerun()

    if ask_clicked and user_question.strip():
        if chat_answer and BACKEND_OK:
            with st.spinner("Ищу ответ..."):
                answer = chat_answer(
                    user_question,
                    st.session_state.user_docs,
                    history=st.session_state.chat_history,
                )
        else:
            sid = detect_service(user_question)
            if sid:
                d = analyze_service(sid, st.session_state.user_docs)
                answer = format_answer(d)
            else:
                answer = "Не удалось найти ответ. Попробуйте уточнить вопрос."

        st.session_state.chat_history.append({"role": "user",      "content": user_question})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        if len(st.session_state.chat_history) > 20:
            st.session_state.chat_history = st.session_state.chat_history[-20:]
        st.rerun()

with tab_form:
    st.markdown("""
    <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;
                color:#0C2D6B;margin-bottom:4px;">Заполнить заявление STI-163</div>
    <div style="font-size:0.83rem;color:#546E7A;margin-bottom:20px;border-bottom:2px solid #C9A84C;padding-bottom:12px;">
        Я задам несколько вопросов, чтобы сформировать готовое заявление в PDF.
    </div>
    """, unsafe_allow_html=True)

    form_fields = [
        {"key": "inn", "question": "Ваш ИНН (12 цифр):", "type": "text", "placeholder": "000102030405"},
        {"key": "fio", "question": "Ваше ФИО (как в паспорте):", "type": "text", "placeholder": "Иванов Иван Иванович"},
        {"key": "tax_authority", "question": "Код налоговой инспекции (например, 001):", "type": "text", "placeholder": "001"},
        {"key": "address_reg", "question": "Адрес регистрации (где прописаны):", "type": "text", "placeholder": "г. Бишкек, ул. Ленина, д. 10, кв. 5"},
        {"key": "phone", "question": "Контактный телефон:", "type": "text", "placeholder": "+996 700 123456"},
        {"key": "email", "question": "Email:", "type": "text", "placeholder": "user@example.com"},
        {"key": "is_ip", "question": "Вы регистрируетесь как ИП? (да/нет)", "type": "bool", "placeholder": ""},
    ]

    if not st.session_state.form_data:
        st.session_state.form_data = {}
        st.session_state.form_step = 0

    if st.session_state.form_step < len(form_fields):
        field = form_fields[st.session_state.form_step]
        key = field["key"]
        question = field["question"]
        with st.form(key=f"form_step_{st.session_state.form_step}"):
            if field["type"] == "text":
                value = st.text_input(question, placeholder=field["placeholder"])
            else:
                value = st.radio(question, ["да", "нет"], index=0) == "да"
            submitted = st.form_submit_button("Далее")
            if submitted:
                st.session_state.form_data[key] = value
                st.session_state.form_step += 1
                st.rerun()
    else:
        st.success("Все данные собраны!")
        st.markdown("**Проверьте введённую информацию:**")
        st.json(st.session_state.form_data)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Сгенерировать PDF", type="primary"):
                try:
                    pdf_buffer = fill_sti_163(st.session_state.form_data)
                    st.download_button(
                        label="Скачать заявление STI-163",
                        data=pdf_buffer,
                        file_name=f"STI163_{st.session_state.form_data.get('inn', '')}.pdf",
                        mime="application/pdf",
                    )
                except Exception as e:
                    st.error(f"Ошибка: {e}")
        with col2:
            if st.button("Начать заново"):
                st.session_state.form_data = {}
                st.session_state.form_step = 0
                st.rerun()

with tab_about:
    st.markdown("""
    <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;
                color:#0C2D6B;margin-bottom:4px;">О проекте</div>
    <div style="font-size:0.83rem;color:#546E7A;margin-bottom:20px;border-bottom:2px solid #C9A84C;padding-bottom:12px;">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-lead">
        <strong>Path KG</strong> — AI-навигатор по государственным услугам Кыргызстана,
        построенный на технологии <strong>Knowledge Graph</strong>. В отличие от обычных языковых
        моделей, система отвечает только на основе верифицированных данных из граф-базы данных —
        без галлюцинаций.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-card-title">Knowledge Graph</div>
            <div class="tech-card-desc">
                Услуги, документы, организации и зависимости хранятся как граф.
                Данные обновляются без переобучения модели.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-card-title">Без галлюцинаций</div>
            <div class="tech-card-desc">
                LLM отвечает только на основе данных из графа.
                Если данных нет — система честно говорит об этом.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-card-title">Актуальные данные</div>
            <div class="tech-card-desc">
                Сроки, стоимость, адреса актуальны на март 2026.
                Обновление — правка узла в графе, не переобучение.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:28px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Масштаб и импакт</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="impact-row">
        <div class="impact-item">
            <div class="impact-num">7М<span>+</span></div>
            <div class="impact-label">граждан КР — потенциальная аудитория</div>
        </div>
        <div class="impact-item">
            <div class="impact-num">8</div>
            <div class="impact-label">ключевых услуг в MVP</div>
        </div>
        <div class="impact-item">
            <div class="impact-num">0<span>%</span></div>
            <div class="impact-label">галлюцинаций — каждый ответ верифицирован</div>
        </div>
        <div class="impact-item">
            <div class="impact-num">200<span>+</span></div>
            <div class="impact-label">услуг КР готовы к интеграции в граф</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Как это работает</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#FFFFFF;border:1px solid #DDE3EE;border-radius:12px;padding:8px 20px;margin-bottom:24px;">
        <div class="how-step">
            <div class="how-step-num">1</div>
            <div>
                <div class="how-step-title">Запрос на естественном языке</div>
                <div class="how-step-desc">Вы пишете «Как открыть ИП в Бишкеке?» на кыргызском или русском.</div>
            </div>
        </div>
        <div class="how-step">
            <div class="how-step-num">2</div>
            <div>
                <div class="how-step-title">Трансляция в граф-запрос</div>
                <div class="how-step-desc">LLM переводит запрос в обход графа знаний — проверяет узлы и зависимости.</div>
            </div>
        </div>
        <div class="how-step">
            <div class="how-step-num">3</div>
            <div>
                <div class="how-step-title">Обход графа зависимостей</div>
                <div class="how-step-desc">Система проверяет наличие ID-карты, прописки, требований ГНС/МЦР.</div>
            </div>
        </div>
        <div class="how-step">
            <div class="how-step-num">4</div>
            <div>
                <div class="how-step-title">Персональный маршрут</div>
                <div class="how-step-desc">Вы получаете пошаговый чеклист с адресами, стоимостью, сроками и ссылками на онлайн-формы.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)