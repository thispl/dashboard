import frappe
from frappe.utils import cint, flt

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
}

def resolve_month(month):
    if not month:
        return None
    if isinstance(month, int) or (isinstance(month, str) and str(month).isdigit()):
        return cint(month)
    return MONTH_MAP.get(str(month).strip().lower(), None)

def get_mpd_doc(site=None, month=None, year=None):
    conditions = ["1=1"]
    values = {}

    if site:
        conditions.append("site = %(site)s")
        values["site"] = site

    month_num = resolve_month(month)
    if month_num:
        conditions.append("MONTH(posting_date) = %(month)s")
        values["month"] = month_num

    if year:
        conditions.append("YEAR(posting_date) = %(year)s")
        values["year"] = cint(year)

    docs = frappe.db.sql(f"""
        SELECT name
        FROM `tabMonthly Progress Data`
        WHERE {" AND ".join(conditions)}
        ORDER BY creation DESC
        LIMIT 1
    """, values, as_dict=True)

    if not docs:
        return None
    return frappe.get_doc("Monthly Progress Data", docs[0].name)

def format_room_occupancy(doc):
    if not doc or not getattr(doc, "occupancy_report", None):
        return None

    buildings = []
    total_rooms = []
    occupied_rooms = []
    vacant_rooms = []
    occupancy_percent = []

    for row in doc.occupancy_report:
        buildings.append(row.building_number or "")
        total_rooms.append(cint(row.total_rooms or 0))
        occupied_rooms.append(cint(row.occupied_rooms or 0))
        vacant_rooms.append(cint(row.vacant_rooms or 0))
        occupancy_percent.append(round(flt(row.occupancy_ or 0), 2))

    if doc.total_rooms_occupancy_wise:
        buildings.append("TOTAL")
        total_rooms.append(cint(doc.total_rooms_occupancy_wise or 0))
        occupied_rooms.append(cint(doc.total_occupied_rooms or 0))
        vacant_rooms.append(cint(doc.total_vacant_rooms or 0))
        occupancy_percent.append(round(flt(doc.total_occupancy_percentage or 0), 2))

    return {
        "buildings": buildings,
        "totalRooms": total_rooms,
        "occupiedRooms": occupied_rooms,
        "vacantRooms": vacant_rooms,
        "occupancyPercent": occupancy_percent,
        "overallOccupancy": round(flt(doc.total_occupancy_percentage or 0), 2)
    }

def format_water_consumption(doc):
    if not doc or not getattr(doc, "water_consumption", None):
        return None

    categories = []
    raw_data = []
    sweet_data = []

    for row in doc.water_consumption:
        if row.date:
            date_str = str(row.date)
            # Take DD portion (e.g., '01', '02')
            categories.append(date_str[8:10] if len(date_str) >= 10 else date_str)
        else:
            categories.append("")

        raw_data.append(round(flt(row.raw_water or 0), 2))
        sweet_data.append(round(flt(row.sweet_water or 0), 2))

    raw_total = sum(raw_data)
    sweet_total = sum(sweet_data)

    return [{
        "series": [
            {"name": "RAW Water", "data": raw_data},
            {"name": "Sweet Water", "data": sweet_data}
        ],
        "categories": categories,
        "totals": {
            "raw": round(raw_total, 2),
            "sweet": round(sweet_total, 2)
        }
    }]

def format_room_occupancy_typewise(doc):
    if not doc or not getattr(doc, "occupancy_category_report", None):
        return None
    records = []
    for row in doc.occupancy_category_report:
        records.append({
            "category": row.category or "",
            "total": cint(flt(row.total_rooms or 0)),
            "occupied": cint(flt(row.occupied_rooms or 0)),
            "vacant": cint(flt(row.vacant_rooms or 0)),
            "occupancy": round(flt(row.occupancy_ or 0), 2)
        })
    return records

def format_monthwise_pmi_cm_wr(doc):
    if not doc or not getattr(doc, "overall_summary", None):
        return None
    by_month = {}
    for row in doc.overall_summary:
        m = (row.month or "").strip()
        if not m:
            continue
        if m not in by_month:
            by_month[m] = {"month": m, "PM": 0, "CM": 0, "WR": 0}
        t = (row.type or "").strip().upper()
        if t in by_month[m]:
            by_month[m][t] = cint(flt(row.accomplished or 0))
    return list(by_month.values())

def format_pm_overall(doc):
    if not doc or not getattr(doc, "pm", None):
        return None
    categories = []
    planned = []
    completed = []
    outstanding = []
    for row in doc.pm:
        categories.append(row.subject or "")
        planned.append(cint(flt(row.planned or 0)))
        completed.append(cint(flt(row.completed or 0)))
        outstanding.append(round(flt(row.outstanding or 0), 2))

    total_planned = sum(planned)
    total_completed = sum(completed)
    rate = f"{(total_completed / total_planned * 100):.2f} %" if total_planned else "0 %"
    return [{
        "series": [
            {"name": "Planned", "data": planned},
            {"name": "Completed", "data": completed},
            {"name": "Outstanding", "data": outstanding}
        ],
        "categories": categories,
        "completion_rate": rate,
        "totals": {
            "Planned": str(total_planned),
            "Completed": str(total_completed)
        }
    }]

def format_cm_wr(rows):
    if not rows:
        return None
    subjects = []
    scheduled = []
    accomplished = []
    percentage = []
    for row in rows:
        subjects.append(row.subject or "")
        s = cint(flt(row.scheduled or 0))
        a = cint(flt(row.accomplished or 0))
        scheduled.append(s)
        accomplished.append(a)
        percentage.append(round(flt(row.outstanding or 0), 2))

    total_sch = sum(scheduled)
    total_acc = sum(accomplished)
    rate = f"{(total_acc / total_sch * 100):.2f} %" if total_sch else "0 %"
    return [{
        "subjects": subjects,
        "scheduled": scheduled,
        "accomplished": accomplished,
        "percentage": percentage,
        "completion_rate": rate,
        "totals": {
            "scheduled": str(total_sch),
            "accomplished": str(total_acc)
        }
    }]

def format_meals(doc):
    return [
        {"meal": "Breakfast", "count": cint(flt(doc.breakfast or 0))},
        {"meal": "Lunch", "count": cint(flt(doc.lunch or 0))},
        {"meal": "Dinner", "count": cint(flt(doc.dinner or 0))},
    ]

def format_laundry(doc):
    return [{"name": "Laundry", "data": str(cint(flt(doc.laundry or 0)))}]

def format_catering_laundry_weekwise(doc):
    if not doc or not getattr(doc, "catering_and_laundry_services", None):
        return None
    w1, w2, w3, w4 = [], [], [], []
    for r in doc.catering_and_laundry_services:
        w1.append(round(flt(r.week_1 or 0), 2))
        w2.append(round(flt(r.week_2 or 0), 2))
        w3.append(round(flt(r.week_3 or 0), 2))
        w4.append(round(flt(r.week_4 or 0), 2))
    return [
        {"name": "Week 1", "data": w1},
        {"name": "Week 2", "data": w2},
        {"name": "Week 3", "data": w3},
        {"name": "Week 4", "data": w4}
    ]

def format_gasoline(doc):
    if not doc or not getattr(doc, "gasoline_consumption", None):
        return None
    cats = []
    g91 = []
    diesel = []
    for r in doc.gasoline_consumption:
        cats.append(str(r.date)[8:10] if r.date and len(str(r.date)) >= 10 else str(r.date or ""))
        g91.append(round(flt(r.gasoline_91 or 0), 2))
        diesel.append(round(flt(r.diesel or 0), 2))
    return [{
        "series": [
            {"name": "GASOLINE 91", "data": g91},
            {"name": "Diesel", "data": diesel}
        ],
        "categories": cats,
        "totals": {
            "gasoline91": round(sum(g91), 2),
            "diesel": round(sum(diesel), 2)
        }
    }]

def format_electricity(doc):
    if not doc or not getattr(doc, "energy_management", None):
        return None
    cats = []
    units = []
    for r in doc.energy_management:
        cats.append(str(r.date)[8:10] if r.date and len(str(r.date)) >= 10 else str(r.date or ""))
        units.append(round(flt(r.unit_consumed or 0), 2))
    return [{
        "series": [{"name": "Electricity Consumption", "data": units}],
        "categories": cats,
        "totals": {"electricity": round(sum(units), 2)}
    }]

def format_sewage(doc):
    if not doc or not getattr(doc, "sewage_water_and_garbage", None):
        return None
    dates = []
    caps = []
    for r in doc.sewage_water_and_garbage:
        dates.append(str(r.date)[8:10] if r.date and len(str(r.date)) >= 10 else str(r.date or ""))
        caps.append(round(flt(r.sewage_water or 0), 2))
    return [{
        "dates": dates,
        "capacities": caps,
        "totals": str(round(sum(caps), 2))
    }]

def format_garbage(doc):
    if not doc or not getattr(doc, "sewage_water_and_garbage", None):
        return None
    dates = []
    caps = []
    for r in doc.sewage_water_and_garbage:
        dates.append(str(r.date)[8:10] if r.date and len(str(r.date)) >= 10 else str(r.date or ""))
        caps.append(round(flt(r.garbage_collection or 0), 2))
    return [{
        "dates": dates,
        "capacities": caps,
        "totals": str(round(sum(caps), 2))
    }]

def format_saudisation(doc):
    if not doc or not getattr(doc, "saudisation", None):
        return None
    funcs = []
    totals = []
    nationals = []
    percentages = []
    for r in doc.saudisation:
        funcs.append(r.functions or "")
        t = cint(flt(r.total or 0))
        n = cint(flt(r.saudi_nationals or 0))
        totals.append(t)
        nationals.append(n)
        percentages.append(f"{(n / t * 100):.1f}" if t else "0.0")
    total_sum = sum(totals)
    nationals_sum = sum(nationals)
    return [{
        "functions": funcs,
        "total": totals,
        "nationals": nationals,
        "total_sum": total_sum,
        "nationals_sum": nationals_sum,
        "percentage": percentages
    }]

def format_manpower_summary(doc):
    if not doc or not getattr(doc, "manpower_summary", None):
        return None
    funcs = []
    ind = []
    act = []
    for r in doc.manpower_summary:
        funcs.append(r.function or "")
        ind.append(cint(flt(r.indicative or 0)))
        act.append(cint(flt(r.actual or 0)))
    return [{
        "functions": funcs,
        "indicative": ind,
        "actual": act
    }]

def format_manpower_details(doc):
    if not doc or not getattr(doc, "manpower_detailed", None):
        return None
    cats = []
    ind = []
    act = []
    for r in doc.manpower_detailed:
        cats.append(r.function or "")
        ind.append(cint(flt(r.indicative or 0)))
        act.append(cint(flt(r.actual or 0)))
    return [{
        "categories": cats,
        "series": [
            {"name": "Indicative", "data": ind},
            {"name": "Actual", "data": act}
        ],
        "totals": {
            "indicative": sum(ind),
            "actual": sum(act)
        }
    }]

def format_safety_environment(doc):
    if not doc or not getattr(doc, "safety_and_environment_checklist", None):
        return None
    cats = []
    app = []
    act = []
    pct = []
    for r in doc.safety_and_environment_checklist:
        cats.append(r.summary_of_scores_and_percentage or "")
        a = cint(flt(r.applicable or 0))
        c = cint(flt(r.actual or 0))
        p = round(flt(r.satisfactory_rating or 0), 2)
        app.append(a)
        act.append(c)
        pct.append(p)
    return [{
        "categories": cats,
        "applicable": app,
        "actual": act,
        "percentage": pct,
        "totals": {
            "applicable": str(sum(app)),
            "actual": str(sum(act)),
            "percentage": str(round(sum(act) / sum(app) * 100, 2) if sum(app) else 0)
        }
    }]

def format_safety_training(doc):
    if not doc or not getattr(doc, "training_on", None):
        return None
    topics = []
    app = []
    act = []
    pct = []
    for r in doc.training_on:
        topics.append(r.training_on or "")
        p = round(flt(r.planned or 0), 2)
        c_val = str(r.conducted or 0).replace(',', '').strip()
        c = round(float(c_val) if c_val.replace('.', '', 1).isdigit() else 0.0, 2)
        ac = round(flt(r.achieved_ or 0), 2)
        app.append(p)
        act.append(c)
        pct.append(ac)
    return [{
        "topics": topics,
        "applicable": app,
        "actual": act,
        "percent": pct
    }]

def format_safety(doc):
    if not doc or not getattr(doc, "safety", None):
        return None
    labels = [
        "Fatal", "Permanent Total Disabilities", "Permanent Partial Disabilities",
        "Lost Workday Cases", "Restricted Workday Cases", "Medical Treatment Cases",
        "First Aid Cases", "Near Miss", "Lost Workdays", "Restricted Workdays"
    ]
    counts_map = {row.injuiry_recorded.strip().lower(): cint(flt(row.count or 0)) for row in doc.safety if row.injuiry_recorded}
    series = [counts_map.get(lbl.lower(), 0) for lbl in labels]
    return [{
        "series": series,
        "labels": labels
    }]

def format_total_activities(doc):
    if not doc or not getattr(doc, "total_activities", None):
        return None
    records = []
    for r in doc.total_activities:
        records.append({
            "label": r.activity or "",
            "value": cint(flt(r.total_activities_done or 0))
        })
    return records

@frappe.whitelist(allow_guest=True)
def get_sandbox_data(site=None, month=None, year=None):
    doc = get_mpd_doc(site, month, year)
    if not doc:
        return {
            "has_data": False,
            "message": f"No Monthly Progress Data found for {site} - {month} {year}",
            "room_occupancy": None,
            "water_consumption": None
        }

    return {
        "has_data": True,
        "doc_name": doc.name,
        "site": doc.site,
        "posting_date": str(doc.posting_date),
        "room_occupancy": format_room_occupancy(doc),
        "water_consumption": format_water_consumption(doc)
    }

@frappe.whitelist(allow_guest=True)
def get_mpd_kpi(month=None, year=None, site=None):
    doc = get_mpd_doc(site, month, year)
    if not doc:
        return []

    result = []
    for row in doc.kpi_title:
        result.append({
            "kpi_title": row.kpi_title,
            "performance_measure": row.performance_measure,
            "achieved": row.achieved
        })
    return result

@frappe.whitelist(allow_guest=True)
def get_test_chart_data(site=None, month=None, year=None, chart_type=None):
    doc = get_mpd_doc(site, month, year)
    if not doc:
        return {
            "status": "error",
            "message": f"No Monthly Progress Data found for {site} - {month} {year}",
            "data": None
        }

    chart_type = (chart_type or "").strip().lower()

    # Maintenance
    if chart_type == "room_occupancy":
        data = format_room_occupancy(doc)
        return {"status": "success", "doc_name": doc.name, "data": [data] if data else None}

    elif chart_type == "room_occupancy_typewise":
        data = format_room_occupancy_typewise(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "monthwise_overall_pmi_cm_wr":
        data = format_monthwise_pmi_cm_wr(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "overall_scheduled_vs_accomplished":
        data = format_pm_overall(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "cm_overall_scheduled_accomplished":
        data = format_cm_wr(doc.cm)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "wr_overall_schedule":
        data = format_cm_wr(doc.wr)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "meals":
        data = format_meals(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "laundry":
        data = format_laundry(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "catering_laundry_service":
        data = format_catering_laundry_weekwise(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    # Operations
    elif chart_type == "water_consumption":
        data = format_water_consumption(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "gasoline_consumption":
        data = format_gasoline(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "electricity_consumption":
        data = format_electricity(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "sewage_water_consumption":
        data = format_sewage(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "garbage_collection":
        data = format_garbage(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    # HR
    elif chart_type == "kpi_performance_measure":
        kpis = []
        for row in doc.kpi_title:
            kpis.append({
                "title": row.kpi_title,
                "performanceMeasure": row.performance_measure,
                "achieved": row.achieved
            })
        return {"status": "success", "doc_name": doc.name, "data": kpis}

    elif chart_type == "manpower_saudi_national":
        data = format_saudisation(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "manpower_summary":
        data = format_manpower_summary(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "manpower_details":
        data = format_manpower_details(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    # Safety
    elif chart_type == "safety":
        data = format_safety(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "safety_and_environment":
        data = format_safety_environment(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "safety_training_on":
        data = format_safety_training(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    elif chart_type == "total_activities_done":
        data = format_total_activities(doc)
        return {"status": "success", "doc_name": doc.name, "data": data}

    return {"status": "error", "message": f"Unsupported chart type: {chart_type}", "data": None}