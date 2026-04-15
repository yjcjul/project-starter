# Aruba AP Ansible Deploy

> 使用 Ansible 自動化部署與管理學校 50 台 Aruba AP（AP505/AP305），包含 VLAN 規劃與 Aruba Controller 整合

- **類型**：混合專案（程式碼 + 技術文件）
- **建立日期**：2026-04-15
- **技術棧**：Ansible, Aruba Controller, VLAN

---

## 📁 資料夾結構

```
aruba-ap-ansible-deploy/
├── ansible/
│   ├── inventory/        # 📋 設備清單
│   ├── playbooks/        # 🎯 Ansible Playbooks
│   ├── roles/            # 🔧 Ansible Roles
│   ├── group_vars/       # 📊 群組變數
│   └── host_vars/        # 📊 主機變數
├── docs/
│   ├── notes/            # 📝 學習筆記
│   ├── decisions/        # 📋 決策記錄 (ADR)
│   └── discussion-log.md # 💬 討論記錄
├── configs/              # 📄 設定檔備份
└── README.md
```

## 🎯 專案目標

1. 使用 Ansible 自動化配置 50 台 Aruba AP
2. 規劃每台 AP 獨立 VLAN
3. 整合 Aruba Controller 集中管理
4. 建立可重複使用的自動化部署流程

## 📋 設備清單

| 型號 | 數量 | 說明 |
|------|------|------|
| Aruba AP505 | TBD | Wi-Fi 6 AP |
| Aruba AP305 | TBD | Wi-Fi 5 AP |
| Aruba Controller | 1 | 集中管理控制器 |

## 🚀 快速開始

```bash
# 1. 安裝 Ansible
pip install ansible

# 2. 安裝 Aruba 模組
ansible-galaxy collection install arubanetworks.aos_switch
ansible-galaxy collection install arubanetworks.aoscx

# 3. 執行部署（待完成）
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml
```

## 📋 文件索引

| 文件 | 說明 |
|------|------|
| [討論記錄](./docs/discussion-log.md) | 與 AI 的討論與需求釐清 |
| [Ansible 學習筆記](./docs/notes/ansible-basics.md) | Ansible 基礎概念與設定 |
| [VLAN 規劃](./docs/notes/vlan-planning.md) | VLAN 架構規劃 |
| [決策記錄](./docs/decisions/) | 重要技術決策 ADR |

## ⚠️ 待釐清事項

- [ ] 學校網路拓撲架構
- [ ] 現有 VLAN 配置詳情
- [ ] AP 部署位置與命名規則
- [ ] Controller 型號與版本

---
