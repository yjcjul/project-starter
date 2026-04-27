# 學校伺服器規格表（供廠商確認 Windows Server 相容性）

> 📅 日期：2026-04-17
> 🏫 臺中市立黎明國民中學

---

## 需求說明

我們需要確認以下伺服器可以安裝的 **Windows Server** 及 **VMware ESXi** 最高版本，
主要用途為 **DataCore SANsymphony 儲存虛擬化** 及 **VMware 虛擬化平台**。

---

## 伺服器規格（相容性判斷用）

| # | 機型 | 數量 | CPU | 預計用途 | 需確認 |
|:--:|------|:--:|-----|---------|--------|
| 1 | **Dell R760** | 2 | Intel Xeon **6526Y** ×2 | 1台 DataCore (Win Server) / 1台 ESXi | Win Server 2022/2025? ESXi 8? |
| 2 | **Dell R740xd** | 1 | Intel Xeon Silver **4210** ×2 | DataCore Mirror (Win Server) | Win Server 2022/2025? |
| 3 | **Dell R730xd** | 2 | **待確認** | 備用（封存） | — |
| 4 | **Dell R660** | 1 | Intel Xeon Silver **4514Y** ×2 | ESXi 主機 | ESXi 8? |
| 5 | **Dell R630 #1** | 1 | Intel Xeon **E5-2697 v3** ×2 | ESXi 主機 | ESXi 8 或 7? Win Server 2022 或 2019? |
| 6 | **Dell R630 #2** | 1 | Intel Xeon **E5-2687W v4** ×2 | 備用（封存） | Win Server 2022 或 2019? |

> 合計 8 台。#3 和 #6 目前規劃為封存備用，但仍請協助確認可安裝的 OS 版本，以備將來需要時使用。

---

## 另外請協助確認

### Windows Server
1. **Windows Server 2022 Standard 授權**需要幾份？（我們需要 2 台安裝 DataCore）
2. 如果可以安裝 **Windows Server 2025**，建議用 2022 還是 2025？
3. 授權是否為 **OEM / Retail / VL（大量授權）**？學校是否有教育優惠？

### VMware ESXi
我們已有授權：**VMware vSphere 4 Essentials PROMO Bundle**（3 hosts, Subscription 2024/05~2027/05）

4. 以下機型可以安裝 **ESXi 8.0** 嗎？
   - Dell R760（Xeon 6526Y）→ 預計裝 ESXi 8
   - Dell R660（Silver 4514Y）→ 預計裝 ESXi 8
   - Dell R630（E5-2697 v3）→ **較舊 CPU，ESXi 8 是否支援？若不支援，ESXi 7.0 可以嗎？**
5. 我們的授權限制 **每顆 CPU 最多 6 核心**，這 3 台機型是否會受到影響？
6. 授權 2027/05 到期後，**續約費用大約多少？**是否有其他方案建議？

---

## 聯絡資訊

學校：臺中市立黎明國民中學
