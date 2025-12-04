const { createClient } = require('@sanity/client');
const fs = require('fs');
const path = require('path');

// Initialize connection
const client = createClient({
  projectId: process.env.SANITY_PROJECT_ID,
  dataset: 'production',
  apiVersion: '2023-05-03',
  token: process.env.SANITY_TOKEN,
  useCdn: false,
});

// Load the local JSON data
const dbPath = path.join(__dirname, 'src/data/calculators.json');
if (!fs.existsSync(dbPath)) {
  console.error("❌ ERROR: src/data/calculators.json not found!");
  process.exit(1);
}

const rawData = fs.readFileSync(dbPath, 'utf8');
const calculators = JSON.parse(rawData);
console.log(`🚀 Preparing to migrate ${calculators.length} calculators to Sanity...`);

const migrate = async () => {
  const transaction = client.transaction();
  calculators.forEach((calc) => {
    const docId = `calculator-${calc.slug}`;
    const doc = {
      _id: docId,
      _type: 'calculator',
      title: calc.title,
      slug: { _type: 'slug', current: calc.slug },
      logic_type: calc.logic_type,
      type: calc.type,
      icon: calc.icon,
      description: calc.description,
      intro: calc.intro,
      inputs: calc.inputs,
      content_us: {
        meta_title: calc.meta_title_us,
        h1_title: calc.h1_title_us,
        article_body_raw: calc.article_body_us,
      },
      content_uk: { meta_title: "", h1_title: "", article_body_raw: "" },
      content_in: { meta_title: "", h1_title: "", article_body_raw: "" },
      content_ae: { meta_title: "", h1_title: "", article_body_raw: "" },
    };
    transaction.createOrReplace(doc);
    console.log(`📦 Staged: ${calc.title}`);
  });

  console.log('⚡ Uploading to Sanity Content Lake...');
  try {
    await transaction.commit();
    console.log('✅ MIGRATION SUCCESSFUL.');
  } catch (err) {
    console.error('❌ Migration Failed:', err.message);
  }
};

migrate();
