const noble = require('@abandonware/noble');
const fs = require('fs');

function log(msg) {
  console.log(msg);
}

async function connectToBMS(peripheral) {
  try {
    await peripheral.connectAsync();
    log("🔌 Connected");

    const { characteristics } = await peripheral.discoverSomeServicesAndCharacteristicsAsync(
      ['ff00'],
      ['ff01', 'ff02']
    );

    log("📥 Subscribed to RX notifications");
    const rx = characteristics.find(c => c.uuid === 'ff01');
    const tx = characteristics.find(c => c.uuid === 'ff02');

    if (!rx || !tx) {
      throw new Error("Could not find required RX/TX characteristics");
    }

    let received = false;

    rx.on('data', (data) => {
      if (!received) {
        log("📨 RX data: " + data.toString('hex'));
        received = true;
        peripheral.disconnectAsync();
      }
    });

    await rx.subscribeAsync();

    const request = Buffer.from("dda503fffd77", "hex");
    await tx.writeAsync(request, false);
  } catch (err) {
    log("❌ BMS error: " + err.message);
    process.exit(0);
  }
}

noble.on('stateChange', async (state) => {
  if (state === 'poweredOn') {
    log("🔍 Scanning...");
    noble.startScanningAsync([], false);
  }
});

noble.on('discover', async (peripheral) => {
  if (peripheral.advertisement.localName && peripheral.advertisement.localName.includes("xiaoxiang")) {
    noble.stopScanningAsync();
    log("✅ Found BMS. Connecting...");
    await connectToBMS(peripheral);
  }
});
