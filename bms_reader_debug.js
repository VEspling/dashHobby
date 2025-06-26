const noble = require("@abandonware/noble");
const fs = require("fs");

const BMS_MAC = "a4:c1:37:34:25:db".toLowerCase();
const SERVICE_UUID = "0000ff00-0000-1000-8000-00805f9b34fb";
const TX_CHAR = "ff02";
const RX_CHAR = "ff01";

const request04 = Buffer.from("dda50400fffc77", "hex");

noble.on("stateChange", async (state) => {
  if (state === "poweredOn") {
    console.log("🔍 Scanning...");
    noble.startScanning([], false);
  }
});

noble.on("discover", async (peripheral) => {
  if (peripheral.address.toLowerCase() === BMS_MAC) {
    console.log("✅ Found BMS. Connecting...");
    noble.stopScanning();
    await peripheral.connectAsync();

    const { characteristics } = await peripheral.discoverSomeServicesAndCharacteristicsAsync(
      [SERVICE_UUID],
      [TX_CHAR, RX_CHAR]
    );

    const rx = characteristics.find((c) => c.uuid === RX_CHAR);
    const tx = characteristics.find((c) => c.uuid === TX_CHAR);

    rx.on("data", (data) => {
      const voltages = {
        cell0: ((data[5] << 8) + data[6]) / 1000,
        cell1: ((data[7] << 8) + data[8]) / 1000,
        cell2: ((data[9] << 8) + data[10]) / 1000,
        cell3: ((data[11] << 8) + data[12]) / 1000,
      };
      const output = {
        bms: `V: ${voltages.cell0.toFixed(2)}V`,
      };
      const statusPath = "status.json";
      let current = {};
      try {
        current = JSON.parse(fs.readFileSync(statusPath));
      } catch {}
      fs.writeFileSync(statusPath, JSON.stringify({ ...current, ...output }, null, 2));
      peripheral.disconnect();
      process.exit();
    });

    await rx.subscribeAsync();
    await tx.writeAsync(request04, false);
  }
});
