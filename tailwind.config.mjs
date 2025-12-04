/** @type {import('tailwindcss').Config} */
export default {
  // 1. Scan these files for Tailwind classes
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],

  // 2. Enable Dark Mode via class strategy (we toggle .dark on <html>)
  darkMode: 'class', 

  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}