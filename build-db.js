const fs = require('fs');
const path = require('path');

const calculators = [
  {
    slug: "mortgage-calculator",
    title: "Mortgage Calculator",
    logic_type: "loan",
    type: "real-estate",
    icon: "🏠",
    description: "Calculate monthly mortgage payments including principal and interest.",
    intro: "Estimate your monthly mortgage payments effectively.",
    inputs: { p_label: "Loan Amount", r_label: "Interest Rate (%)", t_label: "Loan Term (Years)" },
    meta_title_us: "US Mortgage Calculator",
    h1_title_us: "US Mortgage Calculator",
    article_body_us: "<h2>Mortgage Guide</h2><p>Enter loan details to calculate payments.</p>"
  },
  {
    slug: "car-loan-calculator",
    title: "Car Loan Calculator",
    logic_type: "loan",
    type: "auto",
    icon: "🚗",
    description: "Calculate monthly car payments.",
    intro: "Find out your dream car monthly cost.",
    inputs: { p_label: "Car Price", r_label: "Interest Rate (%)", t_label: "Loan Term (Years)" },
    meta_title_us: "Car Loan Calculator",
    h1_title_us: "Car Loan Calculator",
    article_body_us: "<p>Simple car loan calculation.</p>"
  },
  {
    slug: "personal-loan-calculator",
    title: "Personal Loan Calculator",
    logic_type: "loan",
    type: "personal",
    icon: "💸",
    description: "Estimate personal loan payments.",
    intro: "Plan your loan repayment.",
    inputs: { p_label: "Loan Amount", r_label: "Interest Rate (%)", t_label: "Term (Years)" },
    meta_title_us: "Personal Loan Calculator",
    h1_title_us: "Personal Loan Calculator",
    article_body_us: "<p>Personal loan details.</p>"
  },
  {
    slug: "roi-calculator",
    title: "ROI Calculator",
    logic_type: "roi",
    type": "business",
    icon: "📈",
    description: "Calculate Return on Investment.",
    intro": "Measure investment profitability.",
    inputs: { c_label: "Total Invested", v_label: "Returned Amount" },
    meta_title_us: "ROI Calculator",
    h1_title_us: "ROI Calculator",
    article_body_us: "<p>ROI calculation details.</p>"
  },
  {
    slug: "profit-margin-calculator",
    title: "Profit Margin Calculator",
    logic_type: "profit",
    type: "business",
    icon: "💼",
    description: "Calculate net profit margin.",
    intro: "Determine profit percentage.",
    inputs: { c_label: "Cost of Goods", v_label: "Selling Price" },
    meta_title_us: "Profit Margin Calculator",
    h1_title_us: "Profit Margin Calculator",
    article_body_us: "<p>Profit margin details.</p>"
  },
  {
    slug: "compound-interest-calculator",
    title: "Compound Interest Calculator",
    logic_type: "growth",
    type: "savings",
    icon: "💰",
    description: "Calculate compound interest.",
    intro: "See how money grows over time.",
    inputs: { p_label: "Principal", r_label: "Annual Rate (%)", t_label: "Time (Years)" },
    meta_title_us: "Compound Interest Calculator",
    h1_title_us": "Compound Interest Calculator",
    article_body_us": "<p>Compound interest details.</p>"
  },
  {
    slug: "inflation-calculator",
    title: "Inflation Calculator",
    logic_type: "growth",
    type: "economic",
    icon: "📉",
    description": "Calculate future value with inflation.",
    intro: "Estimate purchasing power over time.",
    inputs: { p_label: "Current Cost", r_label: "Inflation Rate (%)", t_label: "Years" },
    meta_title_us: "Inflation Calculator",
    h1_title_us: "Inflation Calculator",
    article_body_us": "<p>Inflation details.</p>"
  },
  {
    slug: "savings-goal-calculator",
    title: "Savings Goal Calculator",
    logic_type": "growth",
    type": "savings",
    icon": "🎯",
    description": "Plan savings goals.",
    intro: "Calculate savings growth.",
    inputs: { p_label: "Starting Balance", r_label: "Interest Rate (%)", t_label: "Years to Goal" },
    meta_title_us": "Savings Goal Calculator",
    h1_title_us": "Savings Goal Calculator",
    article_body_us": "<p>Savings goal details.</p>"
  },
  {
    slug": "net-worth-calculator",
    title": "Net Worth Calculator",
    logic_type": "simple_diff",
    type": "personal",
    icon": "🏦",
    description": "Assets minus Liabilities.",
    intro": "Determine financial net worth.",
    inputs": { v1_label: "Total Assets", v2_label": "Total Liabilities" },
    meta_title_us": "Net Worth Calculator",
    h1_title_us": "Net Worth Calculator",
    article_body_us": "<p>Net worth details.</p>"
  },
  {
    slug": "debt-payoff-calculator",
    title": "Debt Payoff Calculator",
    logic_type": "loan",
    type": "debt",
    icon": "💳",
    description": "Plan debt freedom.",
    intro": "Estimate payoff time.",
    inputs": { p_label: "Debt Balance", r_label: "Interest Rate (%)", t_label": "Months to Pay" },
    meta_title_us": "Debt Payoff Calculator",
    h1_title_us": "Debt Payoff Calculator",
    article_body_us": "<p>Debt payoff details.</p>"
  },
  {
    slug": "401k-calculator",
    title": "401k Calculator",
    logic_type": "growth",
    type": "retirement",
    icon": "👴",
    description": "Estimate retirement savings.",
    intro": "Project 401k balance.",
    inputs": { p_label": "Current Balance", r_label: "Annual Return (%)", t_label": "Years to Retire" },
    meta_title_us": "401k Calculator",
    h1_title_us": "401k Calculator",
    article_body_us": "<p>Retirement details.</p>"
  },
  {
    slug": "college-savings-calculator",
    title": "College Savings Calculator",
    logic_type": "growth",
    type": "savings",
    icon": "🎓",
    description": "Plan for tuition.",
    intro": "Save for education.",
    inputs": { p_label": "Current Savings", r_label": "Annual Return (%)", t_label": "Years until College" },
    meta_title_us": "College Savings Calculator",
    h1_title_us": "College Savings Calculator",
    article_body_us": "<p>College savings details.</p>"
  },
  {
    slug": "rental-yield-calculator",
    title": "Rental Yield Calculator",
    logic_type": "roi",
    type": "real-estate",
    icon": "🔑",
    description": "Calculate property yield.",
    intro": "Analyze rental profitability.",
    inputs": { c_label: "Property Cost", v_label": "Annual Rent" },
    meta_title_us": "Rental Yield Calculator",
    h1_title_us": "Rental Yield Calculator",
    article_body_us": "<p>Rental yield details.</p>"
  },
  {
    slug": "cash-flow-calculator",
    title": "Cash Flow Calculator",
    logic_type": "simple_diff",
    type": "business",
    icon": "📊",
    description": "Income minus Expenses.",
    intro": "Analyze cash flow.",
    inputs": { v1_label: "Total Income", v2_label": "Total Expenses" },
    meta_title_us": "Cash Flow Calculator",
    h1_title_us": "Cash Flow Calculator",
    article_body_us": "<p>Cash flow details.</p>"
  },
  {
    slug": "debt-to-income-ratio-calculator",
    title": "DTI Calculator",
    logic_type": "percentage",
    type": "personal",
    icon": "⚖️",
    description": "Calculate DTI ratio.",
    intro": "Check borrowing eligibility.",
    inputs": { v1_label: "Monthly Debt", v2_label": "Monthly Income" },
    meta_title_us": "DTI Calculator",
    h1_title_us": "DTI Calculator",
    article_body_us": "<p>DTI details.</p>"
  },
  {
    slug": "stock-return-calculator",
    title": "Stock Return Calculator",
    logic_type": "roi",
    type": "investing",
    icon": "🐂",
    description": "Calculate stock profits.",
    intro": "Measure stock returns.",
    inputs": { c_label: "Buy Price", v_label": "Sell Price" },
    meta_title_us": "Stock Return Calculator",
    h1_title_us": "Stock Return Calculator",
    article_body_us": "<p>Stock return details.</p>"
  },
  {
    slug": "tax-equivalent-yield-calculator",
    title": "Tax Equivalent Yield",
    logic_type": "percentage",
    type": "investing",
    icon": "🏛️",
    description": "Compare tax-free yields.",
    intro": "Calculate taxable equivalent yield.",
    inputs": { v1_label: "Tax-Free Yield", v2_label": "Tax Rate (decimal)" },
    meta_title_us": "Tax Equivalent Yield",
    h1_title_us": "TEY Calculator",
    article_body_us": "<p>TEY details.</p>"
  },
  {
    slug": "present-value-calculator",
    title": "Present Value Calculator",
    logic_type": "growth",
    type": "investing",
    icon": "🕰️",
    description": "Calculate PV of money.",
    intro": "Value of future cash today.",
    inputs": { p_label: "Future Value", r_label: "Discount Rate (%)", t_label": "Years" },
    meta_title_us": "Present Value Calculator",
    h1_title_us": "PV Calculator",
    article_body_us": "<p>PV details.</p>"
  },
  {
    slug": "future-value-calculator",
    title": "Future Value Calculator",
    logic_type": "growth",
    type": "investing",
    icon": "🚀",
    description": "Calculate FV of money.",
    intro": "Estimate future investment value.",
    inputs": { p_label: "Present Value", r_label: "Rate (%)", t_label": "Years" },
    meta_title_us": "Future Value Calculator",
    h1_title_us": "Future Value Calculator",
    article_body_us": "<p>FV details.</p>"
  },
  {
    slug": "tip-calculator",
    title": "Tip Calculator",
    logic_type": "percentage",
    type": "personal",
    icon": "🍽️",
    description": "Calculate tips.",
    intro": "Determine tip and total.",
    inputs": { v1_label: "Bill Amount", v2_label": "Tip %" },
    meta_title_us": "Tip Calculator",
    h1_title_us": "Tip Calculator",
    article_body_us": "<p>Tip details.</p>"
  }
];

// Ensure directory exists
const dataDir = path.join(__dirname, 'src', 'data');
if (!fs.existsSync(dataDir)){
    fs.mkdirSync(dataDir, { recursive: true });
}

// Write file
const filePath = path.join(dataDir, 'calculators.json');
fs.writeFileSync(filePath, JSON.stringify(calculators, null, 2));

console.log("✅ JSON Rebuilt Successfully: src/data/calculators.json");
```

**Step 3: Run the Fix**
Run these two commands in your Shell.

```bash
node build-db.js
npm run build