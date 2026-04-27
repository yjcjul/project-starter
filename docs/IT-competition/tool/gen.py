#!/usr/bin/env python3
"""
資訊競賽文件生成工具
使用方式：
    python gen.py                    # 使用預設 winners.yaml
    python gen.py winners_116.yaml   # 指定其他年度檔案
"""

import sys
import os
import yaml
from jinja2 import Environment, FileSystemLoader

def load_data(yaml_path):
    with open(yaml_path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def render(env, template_name, out_path, **ctx):
    tpl = env.get_template(template_name)
    html = tpl.render(**ctx)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ {out_path}")

def gen_preliminary(data, out_dir, env):
    """生成複賽文件：座位表（每人一份）+ 公假單（每競賽項目一份）"""
    prelim = data.get("preliminary")
    if not prelim:
        return

    year   = data["year"]
    GRADE  = {"7": "七", "8": "八", "9": "九"}

    # ── 建立教室座位格（2D list，None 代表空位）──
    rows = prelim.get("room_rows", 2)
    cols = prelim.get("room_cols", 8)
    grid = [[None] * cols for _ in range(rows)]

    for ev in prelim.get("events", []):
        for s in ev.get("students", []):
            r, c = s.get("room_row", 1) - 1, s.get("room_col", 1) - 1
            if 0 <= r < rows and 0 <= c < cols:
                grid[r][c] = {
                    "name":    s["name"],
                    "class":   s["class"],
                    "seat_no": s["seat_no"],
                }

    # ── 為每位學生預算年級/班別 ──
    for ev in prelim.get("events", []):
        for s in ev.get("students", []):
            cls = s.get("class", "")
            s["grade_cn"]  = GRADE.get(cls[:1], cls[:1]) if cls else ""
            try:
                s["class_num"] = str(int(cls[1:])) if len(cls) > 1 else cls
            except ValueError:
                s["class_num"] = cls  # 佔位符直接顯示原值

    tmpl_seat  = env.get_template("複賽座位表.html")
    tmpl_leave = env.get_template("複賽公假單.html")

    print("  [複賽]")
    for ev in prelim.get("events", []):
        students = ev.get("students", [])
        if not students:
            continue

        # 座位表：每位學生一份（含第二頁比賽辦法）
        for s in students:
            fname = f"{year}年_複賽座位表_{s['name']}.html"
            html = tmpl_seat.render(
                year=year, school=data["school"],
                prelim=prelim, event=ev,
                student=s, room_grid=grid,
            )
            out = os.path.join(out_dir, fname)
            with open(out, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  ✅ {out}")

        # 公假單：同一競賽項目全部學生共一張
        fname = f"{year}年_複賽公假單_{ev['name']}.html"
        html = tmpl_leave.render(
            year=year, school=data["school"],
            prelim=prelim, event=ev,
        )
        out = os.path.join(out_dir, fname)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ {out}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "winners.yaml")

    print(f"📂 讀取資料：{yaml_path}")
    data = load_data(yaml_path)

    year = data["year"]
    out_dir = os.path.join(script_dir, f"output_{year}")
    os.makedirs(out_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader(os.path.join(script_dir, "templates")))

    # 建立家長會印領清冊 entries（學生列 + 去重後的指導老師列）
    # 同一老師指導同一競賽項目，只領一份獎金
    entries = []
    seen_teacher_events = {}  # (teacher, event) → prize
    for s in data["students"]:
        entries.append({
            "type": "student",
            "item": s["event"],
            "rank": s["rank"],
            "class": s["class"],
            "name": s["name"],
            "prize": s["prize"],
        })
        key = (s["teacher"], s["event"])
        if key not in seen_teacher_events:
            seen_teacher_events[key] = s["prize"]

    for (teacher, event), prize in seen_teacher_events.items():
        # 找對應的 rank
        rank = next((s["rank"] for s in data["students"] if s["teacher"] == teacher and s["event"] == event), "")
        entries.append({
            "type": "teacher",
            "item": event,
            "rank": rank,
            "class": "指導教師",
            "name": teacher,
            "prize": prize,
        })

    total = sum(e["prize"] for e in entries)

    ctx = dict(
        year=year,
        competition=data["competition"],
        doc_ref=data["doc_ref"],
        date=data["date"],
        school=data["school"],
        students=data["students"],
        teachers=data["teachers"],
        total=total,
    )

    print(f"\n📄 生成文件到：{out_dir}\n")

    # 1. 獎懲申請表（每位學生一份）
    for s in data["students"]:
        fname = f'{year}年_獎懲申請表_{s["name"]}.html'
        render(env, "獎懲申請表.html", os.path.join(out_dir, fname),
               student=s, **ctx)

    # 2. 敘獎擬議清冊
    render(env, "敘獎擬議清冊.html",
           os.path.join(out_dir, f"{year}年_敘獎擬議清冊.html"), **ctx)

    # 3. 家長會獎學金印領清冊
    ctx["total"] = total
    ctx["entries"] = entries
    render(env, "家長會獎學金印領清冊.html",
           os.path.join(out_dir, f"{year}年_家長會獎學金印領清冊.html"),
           **ctx)

    print(f"\n🎉 完成！請用瀏覽器開啟 {out_dir} 中的 .html 檔案，按 Ctrl+P 列印。")
    print("   建議列印設定：紙張 A4、縮放 100%、勾選「背景圖形」\n")

    # 4. 複賽文件（若 winners.yaml 有填 preliminary 區段才生成）
    gen_preliminary(data, out_dir, env)

if __name__ == "__main__":
    main()
