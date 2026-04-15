# 🗂 專案管理工具包

團隊協作用的 VS Code + GitHub 專案分類管理系統。

## 📁 整體結構

```
projects/
├── new-project.sh              # ✅ 一鍵建立新專案腳本
├── _workspace.code-workspace   # VS Code 多專案工作區
├── _base/                      # 🏫 共用知識庫（學校基礎環境資訊）
├── templates/                  # 各類型模板（請勿修改）
│   ├── docs/                   # 📄 文件筆記型模板
│   ├── code/                   # 💻 程式開發型模板
│   └── mixed/                  # 🔀 兩者混合型模板
├── docs/                       # 📄 文件筆記型專案放這
├── code/                       # 💻 程式開發型專案放這
└── mixed/                      # 🔀 混合型專案放這
```

## 🚀 快速開始

### 第一次設定

```bash
# 1. 給腳本執行權限
chmod +x new-project.sh

# 2. 用 VS Code 開啟 workspace
code _workspace.code-workspace
```

### 建立新專案

```bash
bash new-project.sh
```

依照提示：
1. 選擇專案類型（docs / code / mixed）
2. 輸入專案名稱（英文）
3. 輸入主題標籤
4. 輸入描述

腳本會自動：
- ✅ 建立對應的資料夾結構與模板
- ✅ 更新 `_workspace.code-workspace`
- ✅ 初始化 Git

### 推送到 GitHub

```bash
cd docs/你的專案名稱   # 或 code/ mixed/

# 在 GitHub 建立 repo 後：
git remote add origin https://github.com/你的帳號/repo名稱.git
git push -u origin main
```

## 🏷 GitHub Repo 命名規則

| 類型 | 前綴 | 範例 |
|------|------|------|
| 📄 文件筆記 | `docs-` | `docs-product-spec` |
| 💻 程式開發 | `code-` | `code-auth-service` |
| 🔀 兩者混合 | `proj-` | `proj-onboarding` |

## 🔌 建議安裝的 VS Code 套件

| 套件 | 用途 |
|------|------|
| Markdown All in One | Markdown 編輯增強 |
| GitHub Markdown Preview | 預覽效果與 GitHub 一致 |
| GitLens | Git 歷史與協作 |
| Todo Tree | 追蹤 TODO / FIXME |
| Error Lens | 即時顯示錯誤 |
