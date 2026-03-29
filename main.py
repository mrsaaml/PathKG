import json
import os
from groq import Groq
from dotenv import load_dotenv
from k_g import (
    get_plan, G,
    get_full_dependency_chain,
    get_levels,
    get_next_unblocked,
    get_path_to_service,
    get_life_situations,
)

__all__ = [
    "detect_service", "analyze_service", "format_answer",
    "get_next_step", "get_plan", "SERVICES",
    "chat_answer", "get_life_situations", "get_savings_message",
]

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY"))

SERVICES = {
    "s_ip_register":      "Регистрация ИП",
    "s_id_first":         "ID-карта (паспорт 16 лет)",
    "s_zagran_get":       "Загранпаспорт",
    "s_propiska_online":  "Прописка онлайн через Тундук",
    "s_propiska_offline": "Прописка в ЦОН",
    "s_birth_reg":        "Свидетельство о рождении",
    "s_ecp":              "Облачная ЭЦП",
    "s_balagа_benefit":   "Пособие Балага сүйүнчү",
}

# Среднее время (часов) которое тратит человек без навигатора
SERVICE_TIME_COST: dict[str, float] = {
    "s_zagran_get":       3.0,
    "s_id_first":         2.5,
    "s_propiska_online":  0.5,
    "s_propiska_offline": 2.0,
    "s_birth_reg":        1.5,
    "s_ip_register":      2.0,
    "s_ecp":              1.0,
    "s_balagа_benefit":   1.0,
}

# ── Ключевые слова: русский + кыргызский ──────────────────
KEYWORDS: dict[str, list[str]] = {
    "s_zagran_get": [
        "загранпаспорт", "загран", "заграничный", "загран паспорт",
        "чет элке паспорт", "чет өлкөгө", "загранпаспорт алуу",
    ],
    "s_id_first": [
        "id-карта", "ид карта", "удостоверение", "id карта",
        "инсандык күбөлүк", "паспорт алуу", "ид-карта",
    ],
    "s_ip_register": [
        "ип", "индивидуальный предприниматель", "открыть бизнес", "регистрация ип",
        "жеке ишкер", "бизнес ачуу", "жеке предприниматель",
    ],
    "s_propiska_online": [
        "прописка онлайн", "прописаться онлайн", "тундук прописка",
        "тундук аркылуу каттоо", "онлайн каттоо",
    ],
    "s_propiska_offline": [
        "прописка цон", "прописка лично", "прописаться цон",
        "цонго каттоо", "жеке каттоо",
    ],
    "s_birth_reg": [
        "рождение", "свидетельство о рождении", "регистрация ребёнка",
        "туулган", "туулгандыгын каттоо", "балага свидетельство",
    ],
    "s_ecp": [
        "эцп", "электронная подпись", "цифровая подпись", "облачная эцп",
        "электрондук кол", "электрондук колтамга",
    ],
    "s_balagа_benefit": [
        "балага сүйүнчү", "пособие рождение", "выплата ребёнок",
        "сүйүнчү", "балага жардам", "пособие при рождении",
    ],
}

DOC_ALIASES: dict[str, list[str]] = {
    "id-карта (паспорт)":             ["id", "ид", "id карта", "ид карта", "id-карта", "удостоверение", "паспорт", "инсандык"],
    "медсправка о рождении (№103/у)": ["медсправка", "справка о рождении", "103/у", "справка роддом"],
    "свидетельство о браке":          ["свидетельство о браке", "брак", "никях", "нике"],
    "техпаспорт/договор на жильё":    ["техпаспорт", "договор аренды", "договор купли", "документы на жильё", "правоустанавливающий"],
    "заявление sti-163":              ["заявление", "sti-163", "форма sti"],
    "свидетельство о рождении":       ["свидетельство о рождении", "свидетельство рождения", "св-во о рождении", "туулгандык"],
    "id-карта / паспорт родителя":    ["паспорт родителя", "id родителя", "удостоверение родителя"],
    "нотариальное согласие родителя": ["согласие родителя", "нотариальное согласие", "согласие на выезд", "согласие"],
    "облачная эцп":                   ["эцп", "электронная подпись", "цифровая подпись", "электрондук кол"],
}

SERVICE_COMPLETION_SIGNALS: dict[str, list[str]] = {
    "s_id_first":         ["id-карта (паспорт)", "id карта", "удостоверение", "паспорт", "id", "инсандык"],
    "s_birth_reg":        ["свидетельство о рождении", "свидетельство рождения", "туулгандык"],
    "s_ip_register":      ["свидетельство ип", "регистрация ип", "жеке ишкер"],
    "s_propiska_online":  ["прописка", "зарегистрирован", "каттоо"],
    "s_propiska_offline": ["прописка", "зарегистрирован", "каттоо"],
    "s_ecp":              ["эцп", "электронная подпись", "электрондук кол", "облачная эцп"],
    "s_balagа_benefit":   ["балага сүйүнчү", "пособие получено", "сүйүнчү"],
}


# ═══════════════════════════════════════════════════
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ═══════════════════════════════════════════════════

def _fuzzy_match(a: str, b: str, threshold: int = 75) -> bool:
    """Простой fuzzy match без зависимостей — через общие n-граммы."""
    a, b = a.lower().strip(), b.lower().strip()
    if a in b or b in a:
        return True
    # Биграммы
    def bigrams(s):
        return set(s[i:i+2] for i in range(len(s)-1))
    bg_a, bg_b = bigrams(a), bigrams(b)
    if not bg_a or not bg_b:
        return False
    overlap = len(bg_a & bg_b)
    score = overlap / max(len(bg_a), len(bg_b)) * 100
    return score >= threshold


def _doc_matches(doc_name: str, user_lower: list[str]) -> bool:
    doc_lower = doc_name.lower().strip()
    for alias in DOC_ALIASES.get(doc_lower, []):
        if any(_fuzzy_match(alias, ud) for ud in user_lower):
            return True
    return any(_fuzzy_match(doc_lower, ud) for ud in user_lower)


def _service_completed(service_id: str, user_lower: list[str]) -> bool:
    signals = SERVICE_COMPLETION_SIGNALS.get(service_id, [])
    if any(any(_fuzzy_match(sig, ud) for ud in user_lower) for sig in signals):
        return True
    required = [
        nbr for _, nbr, d in G.edges(service_id, data=True)
        if d["relation"] == "REQUIRES_DOC"
    ]
    if not required:
        return False
    return all(_doc_matches(G.nodes[doc_id].get("name", ""), user_lower) for doc_id in required)


def _get_all_deps_recursive(service_id: str) -> set[str]:
    deps, stack, visited = set(), [service_id], set()
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        for _, nbr, data in G.edges(current, data=True):
            if data["relation"] == "DEPENDS_ON" and nbr not in deps:
                deps.add(nbr)
                stack.append(nbr)
    return deps


def _keyword_detect(question: str) -> str | None:
    q = question.lower().strip()
    for service_id, keywords in KEYWORDS.items():
        if any(kw in q for kw in keywords):
            return service_id
    return None


# ═══════════════════════════════════════════════════
# МЕТРИКА ЭКОНОМИИ
# ═══════════════════════════════════════════════════

def get_savings_message(service_id: str, is_ready: bool) -> str:
    """Возвращает строку «Вы сэкономили X часов» если пользователь готов."""
    if not is_ready:
        return ""
    hours = SERVICE_TIME_COST.get(service_id, 1.5)
    trips = 1
    if hours >= 2:
        trips = 1
    h_str = f"{hours:.0f}" if hours == int(hours) else f"{hours:.1f}"
    return f"⏱ Вы сэкономили ~{h_str} ч и {trips} поездку в ЦОН — пришли подготовленными."


# ═══════════════════════════════════════════════════
# 1. DETECT SERVICE
# ═══════════════════════════════════════════════════

def detect_service(user_question: str) -> str | None:
    prompt = f"""Пользователь спрашивает: "{user_question}"

Определи, о какой госуслуге Кыргызстана идёт речь.
Используй этот список ID:
{json.dumps(SERVICES, ensure_ascii=False)}

Ответь ТОЛЬКО идентификатором (например: s_ip_register).
Если ничего не подходит — ответь: none.
Никаких лишних слов."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=20,
        )
        result = response.choices[0].message.content.strip().lower()
        if result in SERVICES:
            return result
        return _keyword_detect(user_question)
    except Exception as e:
        print(f"[detect_service] LLM недоступен: {e}. Keyword fallback.")
        return _keyword_detect(user_question)


# ═══════════════════════════════════════════════════
# 2. ANALYZE SERVICE
# ═══════════════════════════════════════════════════

def analyze_service(service_id: str, user_docs: list[str]) -> dict:
    plan = get_plan(service_id)
    if "error" in plan:
        return {"error": plan["error"]}

    user_lower = [d.lower().strip() for d in user_docs]

    required_docs = [d["name"] for d in plan.get("документы", [])]
    has_docs, missing_docs = [], []
    for doc in required_docs:
        (has_docs if _doc_matches(doc, user_lower) else missing_docs).append(doc)

    blocking_services = []
    for dep in plan.get("зависит_от", []):
        dep_id = dep.get("id", "")
        if dep_id and not _service_completed(dep_id, user_lower):
            blocking_services.append({
                "name":       dep["name"],
                "id":         dep_id,
                "примечание": dep.get("примечание", ""),
            })

    all_dep_ids   = _get_all_deps_recursive(service_id)
    full_chain    = get_full_dependency_chain(service_id)
    levels        = get_levels(service_id)
    path_to_svc   = get_path_to_service(service_id)

    completed_deps = sum(1 for dep_id in all_dep_ids if _service_completed(dep_id, user_lower))
    total_deps     = len(all_dep_ids)
    procedures     = [p["name"] for p in plan.get("процедуры", [])]

    is_ready     = (len(missing_docs) == 0 and len(blocking_services) == 0)
    total        = len(required_docs) + total_deps
    met          = len(has_docs) + completed_deps
    readiness_pct = int(met / total * 100) if total > 0 else 100

    smart_next = get_next_unblocked(service_id, user_docs)
    if smart_next:
        step_place = smart_next.get("место", "")
        next_step = (
            f"Получите: {smart_next['name']} → {step_place}"
            if step_place else f"Получите: {smart_next['name']}"
        )
    elif blocking_services:
        next_step = f"Сначала оформите: {blocking_services[0]['name']}"
    elif missing_docs:
        next_step = f"Подготовьте документ: {missing_docs[0]}"
    elif is_ready:
        next_step = f"Всё готово — обратитесь в: {plan.get('место', 'организацию')}"
    else:
        next_step = "Уточните требования в организации"

    explanation   = _build_explanation(service_id, blocking_services, missing_docs, smart_next, plan)
    savings_msg   = get_savings_message(service_id, is_ready)

    return {
        "plan":              plan,
        "service_name":      plan.get("name", ""),
        "required_docs":     required_docs,
        "has_docs":          has_docs,
        "missing_docs":      missing_docs,
        "depends_on":        [d["name"] for d in plan.get("зависит_от", [])],
        "blocking_services": blocking_services,
        "procedures":        procedures,
        "full_chain":        full_chain,
        "all_dep_ids":       list(all_dep_ids),
        "levels":            levels,
        "smart_next":        smart_next,
        "path_to_service":   path_to_svc,
        "explanation":       explanation,
        "is_ready":          is_ready,
        "readiness_pct":     readiness_pct,
        "confidence":        "high" if required_docs else "medium",
        "next_step":         next_step,
        "savings_msg":       savings_msg,                    # ← новое
        "special_cases":     plan.get("special_cases", ""), # ← новое
        "org":               plan.get("организация", []),
        "шаги":              plan.get("шаги", []),
        "тарифы":            plan.get("тарифы"),
        "срок":              plan.get("срок", "—"),
        "стоимость":         plan.get("стоимость", "—"),
        "место":             plan.get("место", "—"),
        "work_hours":        plan.get("work_hours", "—"),
        "digital_status":    plan.get("digital_status", ""),
        "desc":              plan.get("desc", ""),
        "category":          plan.get("category", ""),
        "last_updated":      plan.get("last_updated", ""),
    }


def _build_explanation(service_id, blocking_services, missing_docs, smart_next, plan) -> str:
    svc_name = plan.get("name", "услуга")
    if blocking_services:
        blocker_id = blocking_services[0].get("id", "")
        edge_note = ""
        if blocker_id:
            for _, nbr, d in G.edges(service_id, data=True):
                if nbr == blocker_id and d.get("note"):
                    edge_note = d["note"]
                    break
        if edge_note:
            return f"«{svc_name}» недоступен: {edge_note}"
        return f"Для получения «{svc_name}» сначала необходимо оформить: «{blocking_services[0]['name']}»"
    if missing_docs:
        return f"Не хватает документа: «{missing_docs[0]}»"
    if smart_next:
        return smart_next.get("reason", "")
    return ""


# ═══════════════════════════════════════════════════
# 3. FORMAT ANSWER — LLM SUMMARY
# ═══════════════════════════════════════════════════

def format_answer(data: dict) -> str:
    if "error" in data:
        return "Не удалось найти данные по этой услуге."

    summary_data = {
        "услуга":        data.get("service_name"),
        "срок":          data.get("срок"),
        "стоимость":     data.get("стоимость"),
        "место":         data.get("место"),
        "готовность":    f"{data.get('readiness_pct', 0)}%",
        "не хватает":    data.get("missing_docs", []),
        "блокирует":     [b["name"] for b in data.get("blocking_services", [])],
        "объяснение":    data.get("explanation", ""),
        "путь":          data.get("path_to_service", []),
        "следующий_шаг": data.get("next_step"),
        "особые_случаи": data.get("special_cases", ""),
    }

    prompt = f"""Ты — AI-навигатор GovNav KG по госуслугам Кыргызстана.

Данные из графа знаний:
{json.dumps(summary_data, ensure_ascii=False, indent=2)}

Напиши КРАТКУЮ сводку (3-4 предложения):
- Что это за услуга и зачем нужна
- Готов ли пользователь (если есть "блокирует" или "объяснение" — используй их дословно)
- Один конкретный следующий шаг
- Если есть особые случаи — упомяни кратко

Без эмодзи. Без повтора шагов. Только суть."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Ты эксперт по госуслугам КР. Отвечай строго на основе переданных данных. Без галлюцинаций."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        if data.get("is_ready"):
            return (
                f"{data.get('service_name')} — вы готовы к получению услуги. "
                f"Срок: {data.get('срок')}. Стоимость: {data.get('стоимость')}. "
                f"{data.get('next_step')}."
            )
        return (
            f"{data.get('service_name')} — пока недоступно. "
            f"{data.get('explanation') or 'Не хватает необходимых документов.'} "
            f"Следующий шаг: {data.get('next_step')}."
        )


# ═══════════════════════════════════════════════════
# 4. GET NEXT STEP
# ═══════════════════════════════════════════════════

def get_next_step(data: dict) -> str:
    return data.get("next_step", "Уточните требования на месте")


# ═══════════════════════════════════════════════════
# 5. GET SERVICE INFO (для чата)
# ═══════════════════════════════════════════════════

def get_service_info(service_id: str) -> dict:
    plan = get_plan(service_id)
    if "error" in plan:
        return {"error": plan["error"]}
    return {
        "name":          plan.get("name", ""),
        "стоимость":     plan.get("стоимость", "—"),
        "срок":          plan.get("срок", "—"),
        "место":         plan.get("место", "—"),
        "work_hours":    plan.get("work_hours", "—"),
        "desc":          plan.get("desc", ""),
        "digital_status":plan.get("digital_status", ""),
        "шаги":          plan.get("шаги", []),
        "тарифы":        plan.get("тарифы", []),
        "special_cases": plan.get("special_cases", ""),
    }


# ═══════════════════════════════════════════════════
# 6. CHAT ANSWER — с историей разговора
# ═══════════════════════════════════════════════════

def _is_pure_factual(lower_input: str) -> str | None:
    """
    Возвращает тип если вопрос — чистый фактический запрос одного поля.
    Только для вопросов типа «сколько стоит» / «где» / «когда работает».
    Любой вопрос с доп. контекстом (если, у меня, могу ли) → None → LLM.
    """
    # Если есть признаки сложного вопроса — сразу в LLM
    complex_signals = [
        "если", "у меня", "могу", "можно", "разрешено", "имею право",
        "без", "с кредитом", "с долгом", "иностранец", "несовершеннолетний",
        "ребёнок", "родитель", "против", "запрет", "арест", "судимость",
        "почему", "зачем", "как долго", "стоит ли", "лучше", "хуже",
        "мүмкүнбү", "болобу", "эгер",
    ]
    if any(s in lower_input for s in complex_signals):
        return None

    if any(w in lower_input for w in ["стоимость", "цена", "сколько стоит", "платить", "оплата", "канча турат"]):
        return "cost"
    if any(w in lower_input for w in ["срок", "сколько дней", "сколько времени", "канча күн"]) and "как" not in lower_input:
        return "duration"
    if any(w in lower_input for w in ["где находится", "адрес", "куда идти", "кайда"]):
        return "location"
    if any(w in lower_input for w in ["часы работы", "когда работает", "режим работы", "график"]):
        return "hours"
    return None


def chat_answer(user_input: str, user_docs: list[str], history: list[dict] | None = None) -> str:
    """
    Логика: быстрый ответ из графа ТОЛЬКО для чистых фактических запросов.
    Всё остальное — LLM с полным контекстом из графа + история.
    """
    lower_input = user_input.lower().strip()
    history = history or []

    service_id = detect_service(user_input)

    # Строим системный контекст из графа
    def _build_context(sid: str | None) -> str:
        if sid:
            info = get_service_info(sid)
            plan = get_plan(sid)
            docs = [d["name"] for d in plan.get("документы", [])]
            steps = info.get("шаги", [])
            special = info.get("special_cases", "")
            ctx = (
                f"Услуга: {info['name']}\n"
                f"Описание: {info['desc']}\n"
                f"Стоимость: {info['стоимость']} | Срок: {info['срок']}\n"
                f"Место: {info['место']} | Часы: {info['work_hours']}\n"
            )
            if docs:
                ctx += f"Документы: {', '.join(docs)}\n"
            if steps:
                ctx += "Шаги: " + "; ".join(f"{i+1}) {s}" for i, s in enumerate(steps)) + "\n"
            if special:
                ctx += f"\nОсобые случаи (важно!):\n{special}\n"
            return ctx
        else:
            # Нет конкретной услуги — даём общий список
            lines = ["Доступные госуслуги КР:"]
            for nid, node in G.nodes(data=True):
                if node.get("type") == "service":
                    lines.append(f"- {node['name']}: {node.get('desc','')[:80]}")
            return "\n".join(lines)

    # ── Быстрые ответы из графа (только чистые факты) ──────
    if service_id:
        info = get_service_info(service_id)
        if "error" not in info:
            fact_type = _is_pure_factual(lower_input)
            if fact_type == "cost":
                return f"**{info['name']}**\nСтоимость: {info['стоимость']}"
            if fact_type == "duration":
                return f"**{info['name']}**\nСрок: {info['срок']}"
            if fact_type == "location":
                return f"**{info['name']}**\nМесто: {info['место']}"
            if fact_type == "hours":
                return f"**{info['name']}**\nЧасы работы: {info['work_hours']}"

    # ── LLM — для всего остального ─────────────────────────
    context = _build_context(service_id)
    system_prompt = (
        "Ты — AI-помощник GovNav по госуслугам Кыргызстана. "
        "Отвечай точно и коротко (2-4 предложения). "
        "Используй только факты из контекста ниже. "
        "Если точного ответа нет — скажи честно и предложи обратиться в ЦОН.\n\n"
        f"{context}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        *history[-6:],
        {"role": "user", "content": user_input},
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        # Fallback без LLM
        if service_id:
            info = get_service_info(service_id)
            special = info.get("special_cases", "")
            if special:
                return f"Особые случаи для «{info['name']}»:\n{special}"
            return f"Обратитесь в {info.get('место', 'ЦОН')} для уточнения."
        return "Сейчас не могу ответить. Попробуйте использовать навигатор слева или обратитесь в ЦОН."


# ═══════════════════════════════════════════════════
# ТЕСТ
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== Тест 1: загранпаспорт, нет документов ===")
    sid = _keyword_detect("хочу загранпаспорт")
    data = analyze_service(sid, user_docs=[])
    print(f"Готовность:    {data['readiness_pct']}%")
    print(f"Не хватает:    {data['missing_docs']}")
    print(f"Блокирует:     {[b['name'] for b in data['blocking_services']]}")
    print(f"Следующий шаг: {data['next_step']}")
    print(f"Экономия:      {data['savings_msg']}")
    print()

    print("=== Тест 2: загранпаспорт, есть ID-карта ===")
    data2 = analyze_service(sid, user_docs=["id карта"])
    print(f"Готовность:    {data2['readiness_pct']}%")
    print(f"Экономия:      {data2['savings_msg']}")
    print()

    print("=== Тест 3: чат с историей ===")
    hist = [
        {"role": "user",      "content": "хочу загранпаспорт"},
        {"role": "assistant", "content": "Загранпаспорт оформляется в ЦОН, срок 18 дней."},
    ]
    print(chat_answer("а можно без родителей?", [], history=hist))
    print()

    print("=== Тест 4: кыргызский язык ===")
    print(detect_service("чет элке паспорт алгым келет"))