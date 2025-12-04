import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://calc-empire.com', 

  server: {
    host: '0.0.0.0',
    port: 5000,
  },

  vite: {
    server: {
      host: '0.0.0.0',
      allowedHosts: [
        'localhost',
        '.replit.dev'
      ]
    }
  },

  integrations: [
    tailwind(), 
    sitemap()
  ],

  compressHTML: true,
});
