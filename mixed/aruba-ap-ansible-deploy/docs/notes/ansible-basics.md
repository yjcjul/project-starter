# Ansible 基礎學習筆記

> 建立日期：2026-04-15

---

## 🎯 什麼是 Ansible？

Ansible 是一個**無代理（Agentless）**的自動化工具，主要用於：
- 配置管理（Configuration Management）
- 應用程式部署（Application Deployment）
- 網路自動化（Network Automation）

### 核心優勢

| 特點 | 說明 |
|------|------|
| 無代理 | 不需要在目標設備安裝任何軟體 |
| SSH/API | 透過 SSH 或 REST API 連接設備 |
| YAML | 使用易讀的 YAML 格式定義任務 |
| 冪等性 | 重複執行結果一致，不會重複配置 |

---

## 📁 Ansible 核心組件

```
ansible-project/
├── ansible.cfg           # Ansible 配置檔
├── inventory/            # 設備清單
│   └── hosts.yml
├── playbooks/            # 劇本（任務腳本）
│   └── deploy.yml
├── roles/                # 角色（可重用模組）
│   └── aruba_ap/
├── group_vars/           # 群組變數
│   └── all.yml
└── host_vars/            # 主機變數
    └── ap-001.yml
```

### 1. Inventory（設備清單）

定義要管理的設備列表：

```yaml
# inventory/hosts.yml
all:
  children:
    aruba_aps:
      hosts:
        ap-001:
          ansible_host: 192.168.1.101
          vlan_id: 101
        ap-002:
          ansible_host: 192.168.1.102
          vlan_id: 102
      vars:
        ansible_network_os: arubanetworks.aoscx.aoscx
        ansible_connection: network_cli
```

### 2. Playbook（劇本）

定義要執行的任務：

```yaml
# playbooks/deploy.yml
---
- name: 配置 Aruba AP
  hosts: aruba_aps
  gather_facts: no
  
  tasks:
    - name: 設定 AP 主機名稱
      arubanetworks.aoscx.aoscx_config:
        lines:
          - hostname {{ inventory_hostname }}
          
    - name: 配置 VLAN
      arubanetworks.aoscx.aoscx_vlan:
        vlan_id: "{{ vlan_id }}"
        name: "AP_{{ inventory_hostname }}"
        state: present
```

### 3. Variables（變數）

```yaml
# group_vars/all.yml
---
# 全域變數
controller_ip: 192.168.1.1
domain_name: school.local

# VLAN 範圍
vlan_start: 101
vlan_end: 150
```

---

## 🔧 Aruba 專用 Ansible Collections

### 安裝方式

```bash
# AOS-CX 交換器（新一代）
ansible-galaxy collection install arubanetworks.aoscx

# AOS-Switch（傳統）
ansible-galaxy collection install arubanetworks.aos_switch

# Aruba Central（雲端管理）
ansible-galaxy collection install arubanetworks.aruba_central
```

### 常用模組

| Collection | 模組 | 用途 |
|------------|------|------|
| aoscx | aoscx_vlan | VLAN 管理 |
| aoscx | aoscx_interface | 介面配置 |
| aoscx | aoscx_config | 通用配置 |
| aos_switch | aos_switch_vlan | 傳統交換器 VLAN |

---

## 📝 基本執行流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  撰寫       │    │  執行       │    │  驗證       │
│  Playbook   │ → │  Ansible    │ → │  結果       │
│  (YAML)     │    │  命令       │    │  (Check)    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 常用命令

```bash
# 測試連線
ansible all -i inventory/hosts.yml -m ping

# 執行 playbook
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml

# 預演模式（不實際執行）
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml --check

# 限定特定主機
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml --limit ap-001

# 顯示詳細輸出
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -vvv
```

---

## 🎓 學習資源

- [Ansible 官方文件](https://docs.ansible.com/)
- [Aruba Ansible Collections](https://github.com/aruba/aoscx-ansible-collection)
- [Aruba Developer Hub](https://developer.arubanetworks.com/)

---

## 📋 待補充

- [ ] 實際 Aruba Controller 配置範例
- [ ] VLAN 自動化腳本
- [ ] 錯誤處理與回滾機制

---
