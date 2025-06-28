const noble = require('@abandonware/noble');
const fs = require('fs');
const { execSync } = require('child_process');
const Database = require('better-sqlite3');
const db = new Database('eink_data.db');

const SERVICE_UUID = 'ff00';
const RX_CHAR = 'ff01';
const TX_CHAR = 'ff02';

function parseCellData(data) {
    const buffer = Buffer.from(data);
    const voltages = {};
    if (buffer.length >= 20) {
        for (let i = 0; i < 4; i++) {
            const raw = buffer.readUInt16BE(3 + i * 2);
            voltages[`cell${i}`] = (raw / 1000).toFixed(3);
        }
    }
    return { cells: voltages };
}

noble.on('stateChange', async state => {
    if (state === 'poweredOn') {
        console.log("🔍 Scanning...");
        noble.startScanning();
    }
});

noble.on('discover', async peripheral => {
    if (peripheral.advertisement.localName?.includes("BMS")) {
        console.log("✅ Found BMS. Connecting...");
        noble.stopScanning();

        const connectAndRead = async () => {
            try {
                await peripheral.connectAsync();
                const { characteristics } = await peripheral.discoverSomeServicesAndCharacteristicsAsync([SERVICE_UUID], [TX_CHAR, RX_CHAR]);
                const tx = characteristics.find(c => c.uuid === TX_CHAR);
                const rx = characteristics.find(c => c.uuid === RX_CHAR);

                await rx.subscribeAsync();
                rx.on('data', async (data) => {
                    const parsed = parseCellData(data);
                    const json = JSON.stringify(parsed);
                    const stmt = db.prepare("INSERT INTO bms_data (data) VALUES (?)");
                    stmt.run(json);
                    console.log("✅ BMS-data sparad:", json);
                    await peripheral.disconnectAsync();
                    process.exit(0);
                });

                const request = Buffer.from("dda50300fffd77", "hex");
                await tx.writeAsync(request, false);
            } catch (err) {
                console.error("❌ Error:", err.message);
                process.exit(1);
            }
        };

        connectAndRead();
    }
});
