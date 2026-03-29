# k_g.py — Knowledge Graph + Reasoning Engine
# Актуально на 26 марта 2026

import networkx as nx

G = nx.DiGraph()

LAST_UPDATED = "2026-03-26"

# ════════════════════════════════════════════════════════════
# УСЛУГИ (8 услуг для MVP)
# ════════════════════════════════════════════════════════════

G.add_node("s_birth_reg",
    name="Регистрация рождения ребёнка",
    type="service",
    status_digital="Full",
    срок="1–3 дня",
    стоимость="0 сом (бесплатно)",
    место="portal.tunduk.kg / Tunduk app / ЗАГС / ЦОН",
    work_hours="24/7 онлайн",
    desc="Государственная регистрация рождения + получение свидетельства и ПИН ребёнка. Можно сразу оформить пособие «Балага сүйүнчү».",
    шаги=[
        "Получите электронную медсправку о рождении (форма №103/у) из роддома.",
        "Зайдите в приложение Tunduk или на portal.tunduk.kg.",
        "Подайте заявление (рекомендуется онлайн).",
        "Приложите свидетельство о браке родителей при наличии.",
        "Получите свидетельство о рождении и ПИН ребёнка.",
    ],
    special_cases=(
        "Если родители не в браке — отцовство устанавливается отдельно через ЗАГС. "
        "Если роды были дома — нужна справка от медработника или свидетелей. "
        "Регистрацию можно сделать в течение 3 месяцев бесплатно, после — через суд."
    ),
    тарифы=None,
    last_updated=LAST_UPDATED,
    category="Семья",
    pos=(0.20, 0.15),
)

G.add_node("s_balagа_benefit",
    name="Пособие «Балага сүйүнчү»",
    type="service",
    status_digital="Full",
    срок="до 10 рабочих дней",
    стоимость="0 сом (получаете выплату)",
    место="portal.tunduk.kg / Соцфонд",
    work_hours="24/7 онлайн",
    desc="Единовременное пособие при рождении ребёнка. Выплачивается после регистрации рождения через Tunduk.",
    шаги=[
        "Зарегистрируйте рождение ребёнка (услуга выше).",
        "В приложении Tunduk подайте заявление на пособие.",
        "Укажите банковский счёт для получения выплаты.",
        "Получите выплату на счёт в течение 10 рабочих дней.",
    ],
    special_cases=(
        "Пособие назначается на каждого ребёнка, включая двойню. "
        "Размер пособия зависит от очерёдности рождения ребёнка."
    ),
    тарифы=None,
    last_updated=LAST_UPDATED,
    category="Семья",
    pos=(0.20, 0.05),
)

G.add_node("s_ecp",
    name="Облачная ЭЦП (электронная подпись)",
    type="service",
    status_digital="Full",
    срок="в день обращения",
    стоимость="от 200 сом/год",
    место="Tunduk app / ЦОН",
    work_hours="09:00–18:00 (ЦОН) / 24/7 онлайн продление",
    desc="Электронная цифровая подпись для подписания заявлений онлайн. Обязательна для прописки через Tunduk и многих других услуг.",
    шаги=[
        "Установите приложение Tunduk.",
        "Пройдите идентификацию по ID-карте и биометрии.",
        "Получите облачную ЭЦП (активируется сразу).",
        "Ежегодно продлевайте подпись онлайн.",
    ],
    special_cases=(
        "Без ЭЦП нельзя сделать прописку онлайн через Tunduk. "
        "ЭЦП работает только при наличии действующей ID-карты. "
        "Иностранным гражданам ЭЦП не выдаётся."
    ),
    тарифы=[
        {"срок": "1 год",  "цена": "200 сом"},
        {"срок": "2 года", "цена": "350 сом"},
    ],
    last_updated=LAST_UPDATED,
    category="Документы",
    pos=(0.35, 0.15),
)

G.add_node("s_propiska_online",
    name="Прописка онлайн через Tunduk",
    type="service",
    status_digital="Full",
    срок="моментально (до 24 часов)",
    стоимость="0 сом (бесплатно)",
    место="Мобильное приложение Tunduk",
    work_hours="24/7",
    desc="Онлайн-регистрация по месту жительства через облачную ЭЦП.",
    шаги=[
        "Собственник выбирает объект недвижимости в Tunduk.",
        "Вводит ПИН регистрируемого и проходит фотоидентификацию.",
        "Подписывает заявление облачной ЭЦП.",
        "Регистрируемый подтверждает заявление.",
        "Прописка оформляется моментально.",
    ],
    special_cases=(
        "Собственник жилья обязательно должен иметь ЭЦП. "
        "Если жильё в совместной собственности — нужно согласие всех владельцев. "
        "Для прописки ребёнка до 14 лет присутствие ребёнка не требуется."
    ),
    тарифы=None,
    last_updated=LAST_UPDATED,
    category="Документы",
    pos=(0.45, 0.15),
)

G.add_node("s_propiska_offline",
    name="Прописка лично в ЦОН",
    type="service",
    status_digital="Offline",
    срок="в день обращения",
    стоимость="300–500 сом",
    место="ЦОН по месту жительства",
    work_hours="09:00–18:00",
    desc="Регистрация по месту жительства с личным посещением ЦОН.",
    шаги=[
        "Подготовьте оригиналы документов на жильё.",
        "Обратитесь лично в ЦОН.",
        "Заполните заявление и оплатите услугу.",
        "Прописка оформляется в день обращения.",
    ],
    special_cases=(
        "Если нет ЭЦП или смартфона — это единственный вариант прописки. "
        "Для несовершеннолетних необходимо присутствие родителя или опекуна."
    ),
    тарифы=None,
    last_updated=LAST_UPDATED,
    category="Документы",
    pos=(0.55, 0.15),
)

G.add_node("s_id_first",
    name="ID-карта впервые (с 16 лет)",
    type="service",
    status_digital="Partial",
    срок="12 рабочих дней (стандарт)",
    стоимость="1 103 сом (стандарт)",
    место="ГУ «Кызмат» (ЦОН)",
    work_hours="09:00–18:00",
    desc="Первичное получение биометрической ID-карты гражданина Кыргызской Республики.",
    шаги=[
        "Подготовьте свидетельство о рождении.",
        "Возьмите документ одного из родителей для подтверждения гражданства.",
        "Обратитесь лично в ЦОН с заявителем.",
        "Пройдите биометрию (фото + отпечатки).",
        "Оплатите госпошлину и получите ID-карту.",
    ],
    special_cases=(
        "Гражданин обязан получить ID-карту в течение 3 месяцев после достижения 16 лет. "
        "Если свидетельство о рождении утеряно — сначала восстановить его через ЗАГС. "
        "Иностранцы, имеющие вид на жительство, получают отдельный вид документа."
    ),
    тарифы=[
        {"срок": "12 рабочих дней", "цена": "1 103 сом"},
        {"срок": "8 рабочих дней",  "цена": "2 720 сом"},
        {"срок": "4 рабочих дня",   "цена": "3 302 сом"},
        {"срок": "2 рабочих дня",   "цена": "3 808 сом"},
        {"срок": "3 часа (Бишкек)", "цена": "8 177 сом"},
    ],
    last_updated=LAST_UPDATED,
    category="Документы",
    pos=(0.50, 0.75),
)

G.add_node("s_zagran_get",
    name="Загранпаспорт (общегражданский)",
    type="service",
    status_digital="Partial",
    срок="18 рабочих дней (стандарт)",
    стоимость="2 981 сом (стандарт)",
    место="ГУ «Кызмат» (ЦОН / Мини-ЦОН)",
    work_hours="09:00–18:00",
    desc="Оформление заграничного паспорта. Для детей до 16 лет возможно оформление с согласием одного родителя.",
    шаги=[
        "Наличие действующей ID-карты (для лиц 16+ лет).",
        "Для детей: свидетельство о рождении + согласие родителей.",
        "Обратитесь в ЦОН и пройдите биометрию.",
        "Оплатите госпошлину и получите загранпаспорт.",
    ],
    special_cases=(
        "Для детей до 16 лет достаточно согласия одного родителя через электронный нотариат. "
        "Если второй родитель против выезда — вопрос решается через суд. "
        "При наличии судимости или долгов — могут отказать в выдаче. "
        "Действует 10 лет для взрослых, 5 лет для детей до 16."
    ),
    тарифы=[
        {"срок": "18 рабочих дней", "цена": "2 981 сом"},
        {"срок": "8 рабочих дней",  "цена": "4 343 сом"},
        {"срок": "4 рабочих дня",   "цена": "5 024 сом"},
        {"срок": "2 рабочих дня",   "цена": "5 485 сом"},
        {"срок": "3 часа (Бишкек)", "цена": "10 363 сом"},
    ],
    last_updated=LAST_UPDATED,
    category="Документы",
    pos=(0.80, 0.75),
)

G.add_node("s_ip_register",
    name="Регистрация ИП",
    type="service",
    status_digital="Full",
    срок="до 3 рабочих дней",
    стоимость="0 сом (бесплатно)",
    место="cabinet.salyk.kg / ГНС",
    work_hours="09:00–18:00",
    desc="Постановка на налоговый учёт как индивидуального предпринимателя.",
    шаги=[
        "Подготовьте ID-карту (для граждан КР).",
        "Заполните заявление STI-163 онлайн через cabinet.salyk.kg.",
        "Для иностранцев потребуются дополнительные документы.",
        "Получите свидетельство о регистрации ИП.",
    ],
    special_cases=(
        "Иностранным гражданам нужен вид на жительство или разрешение на работу. "
        "Несовершеннолетние от 16 лет могут зарегистрировать ИП с согласия родителей. "
        "После регистрации в течение 30 дней нужно выбрать налоговый режим."
    ),
    тарифы=None,
    last_updated=LAST_UPDATED,
    category="Бизнес",
    pos=(0.20, 0.50),
)

# ════════════════════════════════════════════════════════════
# ЖИЗНЕННЫЕ СИТУАЦИИ — верхний уровень навигации
# ════════════════════════════════════════════════════════════

_life_situations = [
    ("ls_new_baby", {
        "name": "Родился ребёнок",
        "type": "life_situation",
        "emoji": "👶",
        "desc": "Регистрация рождения, пособие, прописка ребёнка",
        "services": ["s_birth_reg", "s_balagа_benefit", "s_propiska_online"],
    }),
    ("ls_travel", {
        "name": "Выезд за рубеж",
        "type": "life_situation",
        "emoji": "✈️",
        "desc": "Загранпаспорт для взрослых и детей",
        "services": ["s_id_first", "s_zagran_get"],
    }),
    ("ls_business", {
        "name": "Открыть бизнес",
        "type": "life_situation",
        "emoji": "🏢",
        "desc": "Регистрация ИП онлайн через ГНС",
        "services": ["s_id_first", "s_ip_register"],
    }),
    ("ls_move", {
        "name": "Переезд / новая прописка",
        "type": "life_situation",
        "emoji": "🏠",
        "desc": "Прописка онлайн или через ЦОН",
        "services": ["s_ecp", "s_propiska_online", "s_propiska_offline"],
    }),
    ("ls_first_id", {
        "name": "Исполнилось 16 лет",
        "type": "life_situation",
        "emoji": "🪪",
        "desc": "Первая ID-карта гражданина КР",
        "services": ["s_id_first"],
    }),
]

for node_id, attrs in _life_situations:
    G.add_node(node_id, **attrs)

# ════════════════════════════════════════════════════════════
# ДОКУМЕНТЫ
# ════════════════════════════════════════════════════════════

_docs = [
    ("d_med_birth",      {"name": "Медсправка о рождении (№103/у)", "type": "document", "note": "Электронная из роддома"}),
    ("d_birth_cert",     {"name": "Свидетельство о рождении",       "type": "document"}),
    ("d_id_card",        {"name": "ID-карта (паспорт)",             "type": "document"}),
    ("d_parent_id",      {"name": "ID-карта / паспорт родителя",    "type": "document", "note": "Для подтверждения гражданства"}),
    ("d_marriage_cert",  {"name": "Свидетельство о браке",          "type": "document"}),
    ("d_pravoust",       {"name": "Техпаспорт / Договор на жильё",  "type": "document"}),
    ("d_application",    {"name": "Заявление STI-163",              "type": "document"}),
    ("d_parent_consent", {"name": "Нотариальное согласие родителя", "type": "document", "note": "Можно одного через электронный нотариат"}),
]

for node_id, attrs in _docs:
    G.add_node(node_id, **attrs)

# ════════════════════════════════════════════════════════════
# ПРОЦЕДУРЫ
# ════════════════════════════════════════════════════════════

_procedures = [
    ("dep_biometry",        {"name": "Биометрия (фото + отпечатки)", "type": "procedure"}),
    ("dep_cloud_ecp",       {"name": "Облачная ЭЦП",                 "type": "procedure"}),
    ("dep_parent_presence", {"name": "Присутствие родителей",        "type": "procedure"}),
]

for node_id, attrs in _procedures:
    G.add_node(node_id, **attrs)

# ════════════════════════════════════════════════════════════
# ОРГАНИЗАЦИИ
# ════════════════════════════════════════════════════════════

_orgs = [
    ("o_kyzmat", {"name": "ГУ «Кызмат» (ЦОН / ЗАГС)", "type": "org", "address": "Любой ближайший ЦОН"}),
    ("o_tunduk", {"name": "Платформа Tunduk",           "type": "org", "address": "portal.tunduk.kg / Tunduk app"}),
    ("o_gns",    {"name": "ГНС (Налоговая служба)",     "type": "org", "address": "cabinet.salyk.kg"}),
    ("o_socfond",{"name": "Социальный фонд КР",         "type": "org", "address": "ssf.gov.kg"}),
]

for node_id, attrs in _orgs:
    G.add_node(node_id, **attrs)

# ════════════════════════════════════════════════════════════
# РЁБРА (СВЯЗИ)
# ════════════════════════════════════════════════════════════

_edges = [
    # Регистрация рождения
    ("s_birth_reg", "d_med_birth",      "REQUIRES_DOC", "Электронная справка из роддома"),
    ("s_birth_reg", "d_marriage_cert",  "REQUIRES_DOC", "Свидетельство о браке при наличии"),
    ("o_tunduk",    "s_birth_reg",      "PLATFORM",     ""),
    ("o_kyzmat",    "s_birth_reg",      "ISSUES",       ""),

    # Пособие Балага сүйүнчү — зависит от регистрации рождения
    ("s_balagа_benefit", "s_birth_reg",    "DEPENDS_ON", "Сначала зарегистрировать рождение"),
    ("s_balagа_benefit", "d_birth_cert",   "REQUIRES_DOC", ""),
    ("o_tunduk",         "s_balagа_benefit","PLATFORM",   ""),
    ("o_socfond",        "s_balagа_benefit","ISSUES",     ""),

    # ЭЦП
    ("s_ecp",   "d_id_card",    "REQUIRES_DOC", "Действующая ID-карта"),
    ("s_ecp",   "dep_biometry", "INCLUDES",     ""),
    ("o_tunduk","s_ecp",        "PLATFORM",     ""),
    ("o_kyzmat","s_ecp",        "ISSUES",       ""),

    # Прописка онлайн — требует ЭЦП
    ("s_propiska_online", "s_ecp",        "DEPENDS_ON", "Нужна облачная ЭЦП собственника"),
    ("s_propiska_online", "d_pravoust",   "REQUIRES_DOC", ""),
    ("s_propiska_online", "dep_cloud_ecp","REQUIRES",   "Облачная ЭЦП"),
    ("o_tunduk",          "s_propiska_online", "PLATFORM", ""),

    # Прописка оффлайн
    ("s_propiska_offline", "d_pravoust",  "REQUIRES_DOC", ""),
    ("o_kyzmat",           "s_propiska_offline", "ISSUES", ""),

    # ID-карта впервые
    ("s_id_first", "d_birth_cert",      "REQUIRES_DOC", ""),
    ("s_id_first", "d_parent_id",       "REQUIRES_DOC", ""),
    ("s_id_first", "d_parent_consent",  "REQUIRES_DOC", "При необходимости"),
    ("s_id_first", "dep_biometry",      "INCLUDES",     ""),
    ("o_kyzmat",   "s_id_first",        "ISSUES",       ""),

    # Загранпаспорт
    ("s_zagran_get", "s_id_first",       "DEPENDS_ON",   "Требуется действующая ID-карта"),
    ("s_zagran_get", "d_id_card",        "REQUIRES_DOC", ""),
    ("s_zagran_get", "d_birth_cert",     "REQUIRES_DOC", "Для детей до 16 лет"),
    ("s_zagran_get", "d_parent_consent", "REQUIRES_DOC", "Согласие родителей"),
    ("s_zagran_get", "dep_biometry",     "INCLUDES",     ""),
    ("o_kyzmat",     "s_zagran_get",     "ISSUES",       ""),

    # Регистрация ИП
    ("s_ip_register", "d_id_card",      "REQUIRES_DOC", ""),
    ("s_ip_register", "d_application",  "REQUIRES_DOC", ""),
    ("o_gns",         "s_ip_register",  "ISSUES",       ""),
    ("o_tunduk",      "s_ip_register",  "PLATFORM",     "cabinet.salyk.kg"),

    # Жизненные ситуации → услуги
    ("ls_new_baby",  "s_birth_reg",        "INCLUDES_SERVICE", ""),
    ("ls_new_baby",  "s_balagа_benefit",   "INCLUDES_SERVICE", ""),
    ("ls_new_baby",  "s_propiska_online",  "INCLUDES_SERVICE", ""),
    ("ls_travel",    "s_id_first",         "INCLUDES_SERVICE", ""),
    ("ls_travel",    "s_zagran_get",       "INCLUDES_SERVICE", ""),
    ("ls_business",  "s_id_first",         "INCLUDES_SERVICE", ""),
    ("ls_business",  "s_ip_register",      "INCLUDES_SERVICE", ""),
    ("ls_move",      "s_ecp",              "INCLUDES_SERVICE", ""),
    ("ls_move",      "s_propiska_online",  "INCLUDES_SERVICE", ""),
    ("ls_move",      "s_propiska_offline", "INCLUDES_SERVICE", ""),
    ("ls_first_id",  "s_id_first",         "INCLUDES_SERVICE", ""),
]

for src, dst, rel, note in _edges:
    G.add_edge(src, dst, relation=rel, note=note)

# ════════════════════════════════════════════════════════════
# get_plan — базовый план по услуге
# ════════════════════════════════════════════════════════════

def get_plan(service_id: str) -> dict:
    if service_id not in G:
        return {"error": f"Услуга '{service_id}' не найдена в графе"}

    node = G.nodes[service_id]

    res = {
        "name":           node.get("name"),
        "срок":           node.get("срок", "—"),
        "стоимость":      node.get("стоимость", "—"),
        "место":          node.get("место", "—"),
        "work_hours":     node.get("work_hours", "—"),
        "desc":           node.get("desc", ""),
        "digital_status": node.get("status_digital"),
        "шаги":           node.get("шаги", []),
        "тарифы":         node.get("тарифы", None),
        "special_cases":  node.get("special_cases", ""),
        "pos":            node.get("pos", (0.5, 0.5)),
        "category":       node.get("category", ""),
        "last_updated":   node.get("last_updated", ""),
        "документы":      [],
        "зависит_от":     [],
        "процедуры":      [],
        "организация":    [],
    }

    for _, nbr, data in G.edges(service_id, data=True):
        rel  = data["relation"]
        note = data.get("note", "")
        entry = {
            "id":         nbr,
            "name":       G.nodes[nbr].get("name", nbr),
            "примечание": note,
        }
        if rel == "REQUIRES_DOC":
            res["документы"].append(entry)
        elif rel == "DEPENDS_ON":
            res["зависит_от"].append(entry)
        elif rel in ("INCLUDES", "REQUIRES"):
            res["процедуры"].append(entry)

    for u, _, data in G.in_edges(service_id, data=True):
        if data["relation"] in ("ISSUES", "PLATFORM"):
            res["организация"].append({
                "name":    G.nodes[u].get("name", u),
                "address": G.nodes[u].get("address", ""),
                "note":    data.get("note", ""),
                "role":    data["relation"],
            })

    return res


# ════════════════════════════════════════════════════════════
# get_life_situation — возвращает услуги для жизненной ситуации
# ════════════════════════════════════════════════════════════

def get_life_situations() -> list[dict]:
    """Все жизненные ситуации для онбординг-экрана."""
    result = []
    for node_id, data in G.nodes(data=True):
        if data.get("type") == "life_situation":
            result.append({
                "id":       node_id,
                "name":     data.get("name", ""),
                "emoji":    data.get("emoji", ""),
                "desc":     data.get("desc", ""),
                "services": data.get("services", []),
            })
    return result


# ════════════════════════════════════════════════════════════
# GRAPH REASONING FUNCTIONS
# ════════════════════════════════════════════════════════════

def get_full_dependency_chain(service_id: str) -> list:
    if service_id not in G:
        return []
    chain = []
    visited = set()

    def _walk(node_id: str, level: int):
        if node_id in visited:
            return
        visited.add(node_id)
        for _, nbr, data in G.edges(node_id, data=True):
            if data["relation"] == "DEPENDS_ON":
                chain.append({
                    "id":    nbr,
                    "name":  G.nodes[nbr].get("name", nbr),
                    "level": level,
                    "type":  G.nodes[nbr].get("type", ""),
                })
                _walk(nbr, level + 1)

    _walk(service_id, 1)
    return sorted(chain, key=lambda x: x["level"])


def get_levels(service_id: str) -> dict:
    if service_id not in G:
        return {}
    levels = {}
    for node in nx.ancestors(G, service_id):
        try:
            levels[node] = nx.shortest_path_length(G, node, service_id)
        except nx.NetworkXNoPath:
            pass
    return levels


def get_next_unblocked(service_id: str, user_has: list) -> dict | None:
    if service_id not in G:
        return None
    user_lower = [u.lower().strip() for u in user_has]

    def _has(node_id: str) -> bool:
        name = G.nodes[node_id].get("name", "").lower()
        return any(name in u or u in name for u in user_lower)

    chain = get_full_dependency_chain(service_id)
    for _, nbr, data in G.edges(service_id, data=True):
        if data["relation"] == "REQUIRES_DOC":
            chain.append({
                "id":    nbr,
                "name":  G.nodes[nbr].get("name", nbr),
                "level": 0,
                "type":  "document",
            })

    if not chain:
        return None

    for item in sorted(chain, key=lambda x: -x["level"]):
        if _has(item["id"]):
            continue
        node_deps = [
            nbr for _, nbr, d in G.edges(item["id"], data=True)
            if d["relation"] in ("DEPENDS_ON", "REQUIRES_DOC")
        ]
        if all(_has(dep) for dep in node_deps):
            node = G.nodes[item["id"]]
            return {
                "id":     item["id"],
                "name":   item["name"],
                "level":  item["level"],
                "место":  node.get("место", ""),
                "reason": f"Необходимо для: {G.nodes[service_id].get('name', service_id)}",
            }
    return None


def get_path_to_service(service_id: str) -> list:
    if service_id not in G:
        return []
    ancestors = nx.ancestors(G, service_id)
    if not ancestors:
        return [G.nodes[service_id].get("name", service_id)]
    sub = G.subgraph(ancestors | {service_id})
    try:
        path = nx.dag_longest_path(sub)
        return [G.nodes[n].get("name", n) for n in path if n in G.nodes]
    except Exception:
        return [G.nodes[service_id].get("name", service_id)]


# ════════════════════════════════════════════════════════════
# ВАЛИДАЦИЯ
# ════════════════════════════════════════════════════════════
for _node in G.nodes:
    if "name" not in G.nodes[_node]:
        raise AssertionError(f"[k_g] Узел '{_node}' не имеет атрибута 'name'")

print(f"✅ Knowledge Graph загружен успешно!")
print(f"   Узлов: {len(G.nodes)} | Связей: {len(G.edges)} | Актуально на: {LAST_UPDATED}")