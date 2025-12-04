const {defineField, defineType} = require('sanity')

module.exports = defineType({
  name: 'calculator',
  title: 'Calculator',
  type: 'document',
  fields: [
    defineField({
      name: 'title',
      title: 'Calculator Name',
      type: 'string',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'slug',
      title: 'URL Slug',
      type: 'slug',
      options: {
        source: 'title',
        maxLength: 96,
      },
    }),
    defineField({
      name: 'type',
      title: 'Calculator Logic Family',
      type: 'string',
      options: {
        list: [
          { title: 'Mortgage / Loan', value: 'mortgage' },
          { title: 'Profit Margin', value: 'profit-margin' },
          { title: 'ROI', value: 'roi' },
          { title: 'Auto Loan', value: 'auto-loan' },
        ],
      },
    }),
    defineField({
      name: 'description',
      title: 'SEO Description',
      type: 'text',
      rows: 3,
    }),
  ],
})