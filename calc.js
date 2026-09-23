// GrateHeat energy model (single-case version of model.py, using the middle value of every range).
// Change the inputs with the sliders on the page. Everything else is fixed below.

export const FIXED = {
  keep: 0.75,     // share of airflow left after adding the coil
  avail: 0.85,    // share of hours the module is running
  Tg: 18,         // deep tunnel temperature in winter, C
  k: 0.45,        // how much tunnel air follows street air in winter
  dTs: 6,         // summer tunnel air above street, C
  eps: 0.6,       // coil effectiveness
  eta: 0.5,       // heat pump quality (share of the ideal Carnot limit)
  etaStore: 0.55, // share of summer heat recovered from boreholes
  pumpKW: 0.5,    // loop pump per module, kW
  supplyC: 55,    // hot water temperature, C
  boilerEff: 0.8,
  schoolHeatMWh: 969, // useful heat for the median near-tunnel school (LL84 2024)
};
// Central Park 1991-2020 monthly mean temperatures (F)
const TF = [33.7, 35.9, 42.8, 53.7, 63.2, 72.0, 77.5, 76.1, 69.2, 57.9, 48.0, 39.1];
const TC = TF.map(f => (f - 32) * 5 / 9);
const DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
const HEAT = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0.55, 1, 1];      // Oct 15 - Apr 30
const SUMMER = [0, 0, 0, 0, 0, 0.5, 1, 1, 0.5, 0, 0, 0];   // Jun 15 - Sep 15
const EF = { gas: 53.11, oil: 74.21, elec: 0.288962 };     // kg CO2e per MMBtu / per kWh (NYC LL97)

function cop(Tevap, eta) {
  const Th = FIXED.supplyC + 5 + 273.15, Tc = Tevap + 273.15;
  return eta * Th / (Th - Tc);
}

export function run({ speed = 1.2, area = 5, outShare = 0.5, modules = 4, fuel = 'oil', elecPrice = 0.22, bank = true,
                      gasPrice = 12.0 / 1.037, oilPrice = 4.0 / 0.1385 } = {}) {
  const F = FIXED;
  const mdot = 1.2 * area * speed * outShare * F.keep; // kg/s of tunnel air through the coil
  let heat = 0, elec = 0, elecAshp = 0;
  const monthly = [];
  for (let m = 0; m < 12; m++) {
    let q = 0, qa = 0;
    if (HEAT[m]) {
      const h = DAYS[m] * 24 * HEAT[m] * F.avail;
      const Tt = F.Tg + F.k * (TC[m] - F.Tg);
      const Tev = Math.max(Tt - 12, 1.0);          // coil kept above freezing
      const qsrc = mdot * 1.005 * F.eps * (Tt - Tev);
      const c = cop(Tev, F.eta);
      const qdel = qsrc * c / (c - 1);
      const ca = cop(TC[m] - 10, F.eta) * (TC[m] < 5 ? 0.9 : 1);
      heat += qdel * h / 1000; elec += (qdel / c + F.pumpKW) * h / 1000; elecAshp += (qdel / ca) * h / 1000;
      q = qdel * h / 1000;
      monthly.push({ m, tunnelC: Tt, cop: c, copAshp: ca, heat: q });
    } else monthly.push({ m, heat: 0 });
  }
  let bankHeat = 0, bankElec = 0, summerCoolKW = 0;
  if (bank) {
    let stored = 0;
    for (let m = 0; m < 12; m++) if (SUMMER[m]) {
      const h = DAYS[m] * 24 * SUMMER[m] * F.avail;
      const Tt = TC[m] + F.dTs;
      stored += mdot * 1.005 * F.eps * Math.max(Tt - 16, 0) * h / 1000;
      bankElec += F.pumpKW * h / 1000;
    }
    const cb = cop(8, F.eta);
    bankHeat = stored * F.etaStore * cb / (cb - 1);
    bankElec += bankHeat / cb;
    summerCoolKW = mdot * 1.005 * F.eps * Math.max(TC[6] + F.dTs - 16, 0);
  }
  const perModule = heat + bankHeat, perModuleElec = elec + bankElec;
  const total = perModule * modules, totalElec = perModuleElec * modules;
  const used = Math.min(total, F.schoolHeatMWh);
  const fuelMMBtu = used / F.boilerEff * 3.412;
  const elecUsedKWh = totalElec * (total ? used / total : 0) * 1000;
  const co2 = (fuelMMBtu * EF[fuel] - elecUsedKWh * EF.elec) / 1000; // t/yr
  const fuelCostPerMWh = 3.412 / F.boilerEff * (fuel === 'oil' ? oilPrice : gasPrice);
  const ghCostPerMWh = perModuleElec / perModule * 1000 * elecPrice;
  const ashpCostPerMWh = elecAshp / heat * 1000 * elecPrice;
  const savingPerModule = (fuelCostPerMWh - ghCostPerMWh) * perModule;
  return {
    mdot, perModule, winterHeat: heat, bankHeat, total, share: used / F.schoolHeatMWh,
    scop: perModule / perModuleElec, scopAshp: heat / elecAshp, co2,
    ghCostPerMWh, ashpCostPerMWh, fuelCostPerMWh, savingPerModule, breakEven20: savingPerModule * 20,
    extraVsAshp20: (ashpCostPerMWh - ghCostPerMWh) * perModule * 20, summerCoolKW, monthly,
  };
}
