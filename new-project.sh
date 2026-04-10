#!/bin/bash
# ============================================================
#  new-project.sh — 一鍵建立新專案
#  用法：bash new-project.sh
# ============================================================

set -e

PROJECTS_ROOT="$(cd "$(dirname "$0")" && pwd)"
TEMPLATES_DIR="$PROJECTS_ROOT/templates"
WORKSPACE_FILE="$PROJECTS_ROOT/_workspace.code-workspace"

# ── 顏色輸出 ────────────────────────────────────────────────
GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🚀  新專案初始化工具             ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
echo ""

# ── 選擇專案類型 ─────────────────────────────────────────────
echo -e "${YELLOW}請選擇專案類型：${NC}"
echo "  1) 📄  文件筆記型  (docs)"
echo "  2) 💻  程式開發型  (code)"
echo "  3) 🔀  兩者混合型  (mixed)"
echo ""
read -rp "輸入數字 [1-3]：" TYPE_CHOICE

case "$TYPE_CHOICE" in
  1) TYPE="docs";  EMOJI="📄"; LABEL="文件筆記" ;;
  2) TYPE="code";  EMOJI="💻"; LABEL="程式開發" ;;
  3) TYPE="mixed"; EMOJI="🔀"; LABEL="兩者混合" ;;
  *) echo -e "${RED}無效選擇，結束。${NC}"; exit 1 ;;
esac

# ── 輸入專案名稱 ─────────────────────────────────────────────
echo ""
read -rp "請輸入專案名稱（英文，例如 my-project）：" PROJECT_NAME

if [[ -z "$PROJECT_NAME" ]]; then
  echo -e "${RED}專案名稱不能為空，結束。${NC}"; exit 1
fi

# 檢查是否已存在
PROJECT_DIR="$PROJECTS_ROOT/$TYPE/$PROJECT_NAME"
if [[ -d "$PROJECT_DIR" ]]; then
  echo -e "${RED}專案資料夾已存在：$PROJECT_DIR${NC}"; exit 1
fi

# ── 輸入主題標籤 ─────────────────────────────────────────────
echo ""
read -rp "請輸入主題標籤（可多個，空格分隔，例如 backend api）：" TAGS_INPUT
TAGS=($TAGS_INPUT)

# ── 輸入描述 ─────────────────────────────────────────────────
echo ""
read -rp "請輸入專案簡短描述：" DESCRIPTION

# ── 建立資料夾結構 ─────────────────────────────────────────────
echo ""
echo -e "${BLUE}🔨 建立專案結構...${NC}"

mkdir -p "$PROJECT_DIR"
cp -r "$TEMPLATES_DIR/$TYPE/." "$PROJECT_DIR/"

# ── 替換模板中的變數 ──────────────────────────────────────────
TODAY=$(date +%Y-%m-%d)
REPO_PREFIX="${TYPE}-${PROJECT_NAME}"

find "$PROJECT_DIR" -type f -name "*.md" | while read -r f; do
  sed -i \
    -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
    -e "s/{{DESCRIPTION}}/$DESCRIPTION/g" \
    -e "s/{{TYPE_LABEL}}/$LABEL/g" \
    -e "s/{{DATE}}/$TODAY/g" \
    -e "s/{{REPO_PREFIX}}/$REPO_PREFIX/g" \
    "$f"
done

# ── 更新 workspace 檔案 ────────────────────────────────────────
echo -e "${BLUE}📝 更新 workspace 設定...${NC}"

WORKSPACE_ENTRY="    { \"name\": \"${EMOJI} ${LABEL}｜${PROJECT_NAME}\", \"path\": \"./${TYPE}/${PROJECT_NAME}\" }"

if [[ -f "$WORKSPACE_FILE" ]]; then
  # 在 "folders": [ 之後插入新項目
  python3 - <<PYEOF
import json, sys

with open("$WORKSPACE_FILE", "r") as f:
    ws = json.load(f)

new_folder = {
    "name": "${EMOJI} ${LABEL}｜${PROJECT_NAME}",
    "path": "./${TYPE}/${PROJECT_NAME}"
}
ws["folders"].append(new_folder)

with open("$WORKSPACE_FILE", "w") as f:
    json.dump(ws, f, ensure_ascii=False, indent=2)

print("  workspace 已更新")
PYEOF
fi

# ── Git 初始化 ─────────────────────────────────────────────────
echo -e "${BLUE}🔧 初始化 Git...${NC}"
cd "$PROJECT_DIR"
git init -q
git add .
git commit -q -m "init: 初始化專案 $PROJECT_NAME"

# ── 完成 ───────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅  專案建立完成！                      ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  📁 位置：${YELLOW}$PROJECT_DIR${NC}"
echo -e "  🏷  類型：$EMOJI $LABEL"
echo -e "  📦 建議 GitHub Repo 名稱：${YELLOW}${REPO_PREFIX}${NC}"
echo ""
echo -e "${BLUE}下一步：${NC}"
echo "  1. 在 GitHub 建立 repo：$REPO_PREFIX"
echo "  2. git remote add origin https://github.com/你的帳號/$REPO_PREFIX.git"
echo "  3. git push -u origin main"
echo "  4. 用 VS Code 開啟 _workspace.code-workspace"
echo ""
