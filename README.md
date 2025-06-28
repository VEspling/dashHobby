# E-Ink Dashboard for Pi Zero W

## Översikt
Visar batteristatus (BMS), solcellsstatus (MPPT), klocka och IP på en 5.79" Waveshare E-Ink-display.

## Tjänst (Systemd)
```bash
sudo ln -s /home/dietpi/repos/hobby/eink-status.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable eink-status.service
sudo systemctl start eink-status.service
```

## Kommandon
- Starta displayloop manuellt:
  ```bash
  python3 startup_status.py
  ```
- Kör BMS-avläsning:
  ```bash
  node bms_reader_debug.js
  ```
- Kör MPPT-avläsning:
  ```bash
  python3 mppt_reader.py
  ```
