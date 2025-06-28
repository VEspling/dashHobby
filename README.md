# dashHobby

E-Ink-baserad lokal dashboard för att övervaka batteri- och solstatus från JBD/Overkill BMS samt Victron SmartSolar MPPT, designad för Raspberry Pi Zero 2 W.

---

## 🗄️ Databasstruktur (`eink_data.db`)

Databasen innehåller två tabeller:

### `bms_data`

| Kolumn      | Typ     | Beskrivning                          |
|-------------|---------|--------------------------------------|
| `id`        | INTEGER | Primärnyckel                         |
| `timestamp` | TEXT    | Tidpunkt då datan sparades (UTC)     |
| `data`      | TEXT    | JSON med cellspänningar m.m.         |

### `mppt_data`

| Kolumn      | Typ     | Beskrivning                          |
|-------------|---------|--------------------------------------|
| `id`        | INTEGER | Primärnyckel                         |
| `timestamp` | TEXT    | Tidpunkt då datan sparades (UTC)     |
| `data`      | TEXT    | JSON med info om MPPT-enhet          |

---

## ⚙️ Skript och funktioner

### `init_db.py`

Initierar databasen med tabellerna ovan.

```bash
python3 init_db.py
```

---

### `bms_reader_debug.js`

Läser data från JBD/Overkill BMS via BLE, tolkar cellspänningar och sparar JSON till databasen.

```bash
node bms_reader_debug.js
```

**Exempel på sparad data (`bms_data.data`):**

```json
{
  "cells": {
    "cell0": "3.38",
    "cell1": "3.384",
    "cell2": "3.386",
    "cell3": "3.388"
  }
}
```

---

### `mppt_reader.py`

Söker efter Victron SmartSolar via BLE och sparar info om enheten till databasen.

```bash
python3 mppt_reader.py
```

**Exempel på sparad data (`mppt_data.data`):**

```json
{
  "device": "SmartSolar HQ2234K9G26",
  "address": "E0:86:25:EA:F5:C0",
  "timestamp": "2025-06-29T14:33:10.928755"
}
```

---

### `startup_status.py`

Visar status på E-Ink-displayen:
- Tid och nätverksnamn
- IP-adress
- Databasstatus
- Senaste kända värden från BMS och MPPT

Skriptet kör även `bms_reader_debug.js` och `mppt_reader.py` automatiskt.

---

## 🔄 Automatisk uppstart

Systemd-tjänst: `eink-status.service`  
Symlinkad i `/etc/systemd/system/eink-status.service`  
Ursprungsfil i projektmappen: `/home/dietpi/repos/dashHobby/eink-status.service`

```ini
[Unit]
Description=E-Ink Startup Status Display
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/dietpi/repos/dashHobby/startup_status.py
WorkingDirectory=/home/dietpi/repos/dashHobby
StandardOutput=journal
StandardError=journal
Restart=always
User=dietpi
Group=dietpi

[Install]
WantedBy=multi-user.target
```

**Aktivera tjänsten:**

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable eink-status.service
sudo systemctl start eink-status.service
```

---

## 📁 Projektstruktur

```text
dashHobby/
├── bms_reader_debug.js
├── eink-status.service
├── eink_data.db (genereras)
├── init_db.py
├── mppt_reader.py
├── startup_status.py
├── status.json (genereras)
└── waveshare_epd_py/
    └── epd5in79.py + epdconfig.py + drivrutiner
```

---

## 🧪 Utveckling och testning

- Projektet kan testas både på Raspberry Pi Zero 2 W och i Termux (med proot).
- Statusdata lagras i SQLite och används för visning på displayen.
- Testdata kan användas vid avsaknad av hårdvara för utveckling.

---

## 📌 TODO & Planerade funktioner

- [x] E-Ink-display visar klocka och IP
- [x] BMS-data inhämtas och visas
- [x] MPPT-enhet identifieras
- [x] Systemd-tjänst för automatiserad start
- [ ] MPPT-data utökas med spänning/ström via BLE
- [ ] Historik och loggning via webbgränssnitt
- [ ] OTA-uppdatering och fjärrstyrning (eventuellt)

---