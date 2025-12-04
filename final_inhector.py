import os

# --- FILE 1: THE MATH LIBRARY (Logic) ---
math_lib_code = r"""/**
 * Financial Math Library V8
 */

export const formatNumber = (numStr) => {
  if (!numStr) return '';
  const clean = String(numStr).replace(/,/g, '').replace(/[^0-9.]/g, '');
  const parts = clean.split('.');
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return parts.join('.');
};

export const cleanVal = (val) => {
  if (!val) return 0;
  return parseFloat(String(val).replace(/,/g, '')) || 0;
};

export const calculateLoan = (P, r, n, extraMonthly = 0) => {
  let balance = P;
  let totalInterest = 0;
  let months = 0;

  let monthlyPI = 0;
  if (r === 0) monthlyPI = P / n;
  else monthlyPI = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);

  const actualMonthly = monthlyPI + extraMonthly;

  while(balance > 0 && months < 1200) { 
      const interest = balance * r;
      let principal = actualMonthly - interest;

      if (balance < principal) principal = balance;

      totalInterest += interest;
      balance -= principal;
      months++;
  }
  return { totalInterest, months, monthlyPI };
};

export const calculateGrowth = (P, r, t, contrib) => {
    const n = 12;
    const ratePerPeriod = r / n;
    const totalPeriods = t * n;

    const fvPrincipal = P * Math.pow(1 + ratePerPeriod, totalPeriods);
    const fvContrib = contrib * ((Math.pow(1 + ratePerPeriod, totalPeriods) - 1) / ratePerPeriod);

    const totalVal = fvPrincipal + fvContrib;
    const totalContrib = P + (contrib * totalPeriods);
    const interest = totalVal - totalContrib;

    return { totalVal, totalContrib, interest };
};

export const getAmortizationData = (balance, rate, monthlyPayment, startYear) => {
    let currentBalance = balance;
    let yearTotalInterest = 0;
    let yearTotalPrincipal = 0;
    let currentYear = startYear;
    const data = [];

    for (let i = 1; i <= 3600; i++) { 
       if (currentBalance <= 0) break;
       const interestPayment = currentBalance * rate;
       let principalPayment = monthlyPayment - interestPayment;

       if (currentBalance < principalPayment) principalPayment = currentBalance;

       yearTotalInterest += interestPayment;
       yearTotalPrincipal += principalPayment;
       currentBalance -= principalPayment;

       if (i % 12 === 0 || currentBalance <= 0) {
          data.push({
              year: currentYear,
              interest: yearTotalInterest,
              principal: yearTotalPrincipal,
              balance: Math.max(0, currentBalance)
          });
          yearTotalInterest = 0; currentYear++;
       }
    }
    return data;
};
"""

# --- FILE 2: THE UI COMPONENT (Interface) ---
component_code = r"""---
// src/components/CalculatorForm.astro
interface Props {
  calculator: any;
  currency: string;
}

const { calculator, currency } = Astro.props;
const { logic_type, inputs, extras = [] } = calculator;

// SSR Defaults
let initialResult = "0";
let initialPayoff = "Dec, 2055"; 
if (logic_type === 'loan') { initialResult = "2,385.42"; } 
---

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<div class="bg-white dark:bg-gray-800 p-6 lg:p-8 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 max-w-6xl mx-auto mt-8 grid lg:grid-cols-12 gap-8 print:shadow-none print:border-none print:mt-0 print:block">

  {/* LEFT COLUMN: INPUTS */}
  <div class="lg:col-span-5 space-y-6 print:hidden">
    <div class="flex items-center gap-3 mb-4 border-b border-gray-100 dark:border-gray-700 pb-4">
      <span class="text-3xl">{calculator.icon}</span>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">{calculator.title}</h2>
    </div>

    <form id="calc-form" class="space-y-5" data-logic={logic_type} data-currency={currency}>

      {/* SECTION 1: CORE INPUTS */}
      {['loan', 'growth'].includes(logic_type) && (
        <div class="space-y-4">
          <div>
            <label class="label">{inputs.p_label}</label>
            <div class="relative">
              <span class="currency-symbol">{currency}</span>
              <input type="text" inputmode="decimal" id="input_p" placeholder="400,000" class="input-field pl-8 comma-input" required />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label">{inputs.r_label}</label>
              <div class="relative">
                <input type="number" id="input_r" placeholder="5.5" step="0.01" class="input-field pr-8" required />
                <span class="absolute right-3 top-3 text-gray-400 font-bold">%</span>
              </div>
            </div>
            <div>
              <label class="label">{inputs.t_label}</label>
              <input type="number" id="input_t" placeholder="30" class="input-field" required />
            </div>
          </div>

          {/* Start Date */}
          <div>
            <label class="label">Start Date</label>
            <input type="month" id="input_date" class="input-field" value={new Date().toISOString().slice(0, 7)} />
          </div>
        </div>
      )}

      {/* SECTION 2: EXTRAS (Toggleable) */}
      {extras && extras.length > 0 && (
        <div class="bg-gray-50 dark:bg-gray-900/50 p-4 rounded-xl border border-gray-100 dark:border-gray-700">
          <label class="flex items-center gap-2 cursor-pointer mb-4">
            <input type="checkbox" id="toggle-extras" class="w-4 h-4 text-blue-600 rounded" checked />
            <span class="text-sm font-bold text-gray-700 dark:text-gray-300 select-none">Include Taxes & Fees</span>
          </label>

          <div id="extras-container" class="grid grid-cols-1 gap-3 transition-all">
            {extras.map((field) => (
              <div class="grid grid-cols-2 gap-2 items-center">
                <label class="text-xs font-semibold text-gray-600 dark:text-gray-400">\${field.label}</label>
                <div class="relative">
                   <span class="absolute left-2 top-2 text-gray-400 text-xs">\${currency}</span>
                   <input 
                    type="text" 
                    inputmode="decimal"
                    id={\`extra_\${field.id}\`} 
                    placeholder={field.default.toLocaleString()} 
                    class="input-field pl-5 py-1.5 text-sm comma-input" 
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Inputs for Simple Calcs */}
      {['roi', 'profit', 'simple_diff', 'percentage'].includes(logic_type) && (
        <div class="grid grid-cols-1 gap-4">
          <div><label class="label">\$ {inputs.c_label || inputs.v1_label}</label><input type="text" inputmode="decimal" id="input_v1" class="input-field comma-input" /></div>
          <div><label class="label">\$ {inputs.v_label || inputs.v2_label}</label><input type="text" inputmode="decimal" id="input_v2" class="input-field comma-input" /></div>
        </div>
      )}

      <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-6 rounded-xl transition-all shadow-lg hover:shadow-green-500/30 transform hover:-translate-y-0.5 text-lg flex justify-center items-center gap-2">
        <span>Calculate</span> 🚀
      </button>
    </form>
  </div>

  {/* RIGHT COLUMN: DASHBOARD */}
  <div class="lg:col-span-7 flex flex-col gap-6 print:col-span-12 print:w-full">

    {/* 1. Summary Card */}
    <div class="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm print:bg-white print:border-black">
      <div class="flex justify-between items-end border-b border-gray-200 dark:border-gray-700 pb-4 mb-4">
        <div>
          <p class="text-xs uppercase tracking-widest font-bold text-gray-500">Monthly Payment</p>
          <div class="text-5xl font-black text-green-600 dark:text-green-400 tracking-tight mt-1 print:text-black" id="final-result">
            {logic_type === 'loan' ? currency + initialResult : initialResult}
          </div>
        </div>
        <div class="text-right hidden sm:block print:block">
          <p class="text-xs font-bold text-gray-400">PAYOFF DATE</p>
          <p class="text-xl font-bold text-gray-800 dark:text-white print:text-black" id="res-date">{initialPayoff}</p>
        </div>
      </div>

      <div class="grid sm:grid-cols-2 gap-6">
        <div class="space-y-2 text-sm">
          <div class="flex justify-between"><span class="text-gray-500">Principal</span><span class="font-bold dark:text-white print:text-black" id="res-loan">--</span></div>
          <div class="flex justify-between"><span class="text-gray-500">Total Interest</span><span class="font-bold text-red-500 print:text-black" id="res-interest">--</span></div>
          <div class="flex justify-between"><span class="text-gray-500">Total Taxes/Fees</span><span class="font-bold text-orange-500 print:text-black" id="res-tax">--</span></div>
          <div class="flex justify-between border-t border-gray-200 pt-2 mt-1"><span class="font-bold text-gray-700 dark:text-gray-300 print:text-black">Total Cost</span><span class="font-bold dark:text-white print:text-black" id="res-total">--</span></div>
        </div>
        <div class="h-32 relative flex justify-center">
          <canvas id="myChart"></canvas>
        </div>
      </div>

      {/* Share Actions (Hidden on Print) */}
      <div class="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700 flex gap-3 print:hidden">
        <button id="share-btn" class="flex-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 py-2 rounded-lg text-sm font-bold hover:bg-gray-50 transition-colors flex justify-center items-center gap-2">
           🔗 Copy Link
        </button>
        <button id="print-btn-action" class="flex-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 py-2 rounded-lg text-sm font-bold hover:bg-gray-50 transition-colors flex justify-center items-center gap-2">
           🖨️ Save PDF
        </button>
      </div>
    </div>

    {/* 💡 SMART ADVISOR */}
    {logic_type === 'loan' && (
      <div id="smart-advisor" class="hidden bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800/50 rounded-xl p-5 shadow-sm animate-fade-in print:hidden">
        <div class="flex items-center gap-2 mb-3">
          <span class="text-xl">💡</span>
          <h3 class="font-bold text-amber-900 dark:text-amber-100">Smart Savings Recommendations</h3>
        </div>
        <div class="grid sm:grid-cols-2 gap-4">
          <button id="sim-extra" class="text-left p-3 bg-white dark:bg-gray-800 rounded-lg border border-amber-100 hover:border-amber-400 transition-all hover:shadow-md group">
            <p class="text-xs text-gray-500 font-bold uppercase mb-1">Pay +100 {currency}/mo</p>
            <p class="text-sm text-gray-700 dark:text-gray-300">
              Save <span class="font-bold text-green-600" id="save-amount-1">--</span> in interest.
            </p>
            <span class="text-xs text-blue-600 font-medium mt-2 block group-hover:underline">Simulate this →</span>
          </button>
          <button id="sim-term" class="text-left p-3 bg-white dark:bg-gray-800 rounded-lg border border-amber-100 hover:border-amber-400 transition-all hover:shadow-md group">
            <p class="text-xs text-gray-500 font-bold uppercase mb-1" id="label-term-2">Shorter Term</p>
            <p class="text-sm text-gray-700 dark:text-gray-300">
              Save <span class="font-bold text-green-600" id="save-amount-2">--</span> total.
            </p>
            <span class="text-xs text-blue-600 font-medium mt-2 block group-hover:underline">Apply this →</span>
          </button>
        </div>
      </div>
    )}

    {/* Amortization Table */}
    <div id="amortization-container" class="hidden bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden print:border print:block">
      <div class="bg-gray-100 dark:bg-gray-900 px-6 py-3 border-b border-gray-200 dark:border-gray-700 font-bold text-gray-700 dark:text-gray-300 flex justify-between items-center print:bg-white print:text-black">
        <span>Yearly Amortization</span>
      </div>
      <div class="max-h-64 overflow-y-auto no-scrollbar print:max-h-none print:overflow-visible">
        <table class="w-full text-sm text-left">
          <thead class="text-xs text-gray-500 uppercase bg-gray-50 dark:bg-gray-900 sticky top-0 print:static">
            <tr>
              <th class="px-4 py-2">Year</th>
              <th class="px-4 py-2">Interest</th>
              <th class="px-4 py-2">Principal</th>
              <th class="px-4 py-2">Balance</th>
            </tr>
          </thead>
          <tbody id="amortization-body" class="divide-y divide-gray-100 dark:divide-gray-800"></tbody>
        </table>
      </div>
    </div>

  </div>
</div>

<style>
  .label { @apply block text-xs font-bold text-gray-600 dark:text-gray-400 mb-1 uppercase tracking-wide; }
  .input-field { @apply w-full px-3 py-2.5 border-2 border-gray-200 dark:border-gray-600 rounded-lg focus:ring-0 focus:border-green-500 bg-white dark:bg-gray-800 dark:text-white transition-colors outline-none font-bold text-gray-700; }
  .currency-symbol { @apply absolute left-3 top-3 text-gray-400 text-sm font-bold; }
  .animate-fade-in { animation: fadeIn 0.5s ease-out forwards; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

  @media print {
    body * { visibility: hidden; }
    #calc-form, #calc-form * { display: none !important; }
    #smart-advisor { display: none !important; }
    .print\:hidden { display: none !important; }

    /* Only show results and table */
    main, main * { visibility: visible; }
    main { position: absolute; left: 0; top: 0; width: 100%; margin: 0; padding: 0; }
    .lg\:col-span-7 { width: 100% !important; margin: 0 !important; }
  }
</style>

<script>
  import { calculateLoan, calculateGrowth, cleanVal, formatNumber, getAmortizationData } from '../lib/financial-math.js';

  let chartInstance = null;
  const form = document.getElementById('calc-form');
  const resultEl = document.getElementById('final-result');
  const toggleExtras = document.getElementById('toggle-extras');
  const extrasContainer = document.getElementById('extras-container');
  const smartAdvisor = document.getElementById('smart-advisor');

  // --- URL PERSISTENCE ---
  function updateURL() {
    const params = new URLSearchParams();
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        if(input.value && input.type !== 'checkbox' && input.type !== 'submit') {
            params.set(input.id, input.value);
        }
    });
    window.history.replaceState({}, '', `${location.pathname}?\${params}`);
  }

  function loadFromURL() {
    const params = new URLSearchParams(window.location.search);
    if(params.toString()) {
        params.forEach((val, key) => {
            const el = document.getElementById(key);
            if(el) el.value = val;
        });
        // Auto-run if data present
        setTimeout(() => form.dispatchEvent(new Event('submit')), 100);
    }
  }

  // --- EVENT LISTENERS ---
  if(toggleExtras) {
    toggleExtras.addEventListener('change', (e) => {
        // @ts-ignore
        extrasContainer.style.display = e.target.checked ? 'grid' : 'none';
    });
  }

  document.querySelectorAll('.comma-input').forEach(input => {
    input.addEventListener('input', (e) => { 
        // @ts-ignore
        e.target.value = formatNumber(e.target.value); 
    });
  });

  document.getElementById('print-btn-action')?.addEventListener('click', () => window.print());

  document.getElementById('share-btn')?.addEventListener('click', () => {
      updateURL();
      navigator.clipboard.writeText(window.location.href);
      alert("Link copied! You can now share this calculation.");
  });

  if (form) {
    form.addEventListener('submit', () => updateURL());
    loadFromURL();

    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const logic = form.dataset.logic;
      const currency = form.dataset.currency;
      const fmt = (n) => n.toLocaleString('en-US', { maximumFractionDigits: 0 });
      const getVal = (id) => cleanVal(document.getElementById(id)?.value);

      if (logic === 'loan') {
        let price = getVal('input_p');
        const down = getVal('extra_down') || getVal('input_down');
        const trade = getVal('extra_trade');
        const rAnnual = getVal('input_r');
        const r = rAnnual / 100 / 12;
        const years = getVal('input_t');
        const n = years * 12;
        const loanAmount = price - down - trade;

        const base = calculateLoan(loanAmount, r, n, 0);

        const monthlyTax = getVal('extra_tax') / 12;
        const monthlyIns = getVal('extra_ins') / 12;
        const monthlyHOA = getVal('extra_hoa');
        const totalExtras = monthlyTax + monthlyIns + monthlyHOA;
        const totalMonthly = base.monthlyPI + totalExtras;
        const totalPaid = (base.monthlyPI * n) + (totalExtras * n); 

        const dateInput = (document.getElementById('input_date') as HTMLInputElement).value;
        const startDate = new Date(dateInput + "-01");
        const payoffDate = new Date(startDate);
        payoffDate.setMonth(startDate.getMonth() + n);

        resultEl.textContent = currency + totalMonthly.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        document.getElementById('res-loan').textContent = currency + fmt(loanAmount);
        document.getElementById('res-interest').textContent = currency + fmt(base.totalInterest);
        document.getElementById('res-tax').textContent = currency + fmt(totalExtras * n);
        document.getElementById('res-total').textContent = currency + fmt(totalPaid);
        document.getElementById('res-date').textContent = payoffDate.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });

        renderChart([base.monthlyPI, monthlyTax, monthlyIns, monthlyHOA], ['P&I', 'Tax', 'Ins', 'HOA'], ['#16a34a', '#3b82f6', '#f59e0b', '#ef4444']);

        const amortData = getAmortizationData(loanAmount, r, base.monthlyPI, startDate.getFullYear());
        renderAmortizationTable(amortData);

        // Smart Advisor Logic
        smartAdvisor.classList.remove('hidden');
        const sim1 = calculateLoan(loanAmount, r, n, 100);
        const save1 = base.totalInterest - sim1.totalInterest;

        document.getElementById('save-amount-1').textContent = currency + fmt(save1);

        document.getElementById('sim-extra').onclick = (e) => {
            e.preventDefault();
            alert(`Paying 100 more saves you ${currency}${fmt(save1)}!`);
        };

        const newYears = Math.max(1, years - 5);
        const sim2 = calculateLoan(loanAmount, r, newYears * 12, 0);
        const save2 = base.totalInterest - sim2.totalInterest;

        document.getElementById('label-term-2').textContent = `Shorten to ${newYears} Years`;
        document.getElementById('save-amount-2').textContent = currency + fmt(save2);

        document.getElementById('sim-term').onclick = (e) => {
            e.preventDefault();
            (document.getElementById('input_t') as HTMLInputElement).value = String(newYears);
            form.dispatchEvent(new Event('submit')); 
        };
      }
      else if (logic === 'growth') {
          const P = getVal('input_p');
          const r = getVal('input_r') / 100;
          const t = getVal('input_t');
          const contrib = getVal('extra_contrib');
          const growth = calculateGrowth(P, r, t, contrib);

          resultEl.textContent = currency + fmt(growth.totalVal);
          renderChart([P + (contrib * t * 12), growth.totalVal - (P + (contrib * t * 12))], ['Principal', 'Interest'], ['#3b82f6', '#10b981']);
      }
      else {
         const v1 = getVal('input_v1') || getVal('input_p');
         const v2 = getVal('input_v2');
         let res = 0;
         if (logic === 'roi') res = ((v2 - v1) / v1) * 100;
         if (logic === 'profit') res = ((v2 - v1) / v2) * 100;
         if (logic === 'percentage') res = v1 * (v2/100);
         if (logic === 'simple_diff') res = v1 - v2;

         let resStr = res.toLocaleString('en-US', { minimumFractionDigits: 2 });
         if (['roi', 'profit'].includes(logic)) resStr += "%";
         else resStr = currency + resStr;
         resultEl.textContent = resStr;
      }
    });
  }

  function renderAmortizationTable(data) {
    const tbody = document.getElementById('amortization-body');
    tbody.innerHTML = ''; 
    document.getElementById('amortization-container').classList.remove('hidden');

    data.forEach(row => {
       const html = `
        <tr class="bg-white dark:bg-gray-800 border-b border-gray-100 dark:border-gray-700">
            <td class="px-4 py-3 font-medium text-gray-900 dark:text-white">\${row.year}</td>
            <td class="px-4 py-3 text-red-500">\${Math.round(row.interest).toLocaleString()}</td>
            <td class="px-4 py-3 text-green-600">\${Math.round(row.principal).toLocaleString()}</td>
            <td class="px-4 py-3 text-gray-500">\${Math.round(row.balance).toLocaleString()}</td>
        </tr>
       `;
       tbody.innerHTML += html;
    });
  }

  function renderChart(data, labels, colors) {
    const ctx = document.getElementById('myChart');
    if (chartInstance) chartInstance.destroy();
    const d = [], l = [], c = [];
    data.forEach((v, i) => { if(v > 0) { d.push(v); l.push(labels[i]); c.push(colors[i]); } });
    // @ts-ignore
    chartInstance = new Chart(ctx, {
      type: 'doughnut',
      data: { labels: l, datasets: [{ data: d, backgroundColor: c, borderWidth: 0, hoverOffset: 4 }] },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, cutout: '75%' }
    });
  }
</script>