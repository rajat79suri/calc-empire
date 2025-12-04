# Astro.js Project

## Overview
A minimal Astro.js project initialized with the empty (minimal) starter template. This serves as a clean foundation for building static or server-rendered websites.

## Project Structure
```
/
├── public/          # Static assets (served as-is)
├── src/
│   ├── lib/
│   │   └── github.ts  # GitHub client helper
│   └── pages/       # File-based routing
│       └── index.astro
├── astro.config.mjs # Astro configuration
├── package.json
└── tsconfig.json
```

## Development
- **Dev Server**: `npm run dev` - Runs on port 5000
- **Build**: `npm run build` - Creates production build in `dist/`
- **Preview**: `npm run preview` - Preview production build locally

## Configuration
- Server configured to bind to `0.0.0.0:5000` for Replit compatibility
- TypeScript support enabled

## Integrations
- **GitHub**: Connected via Replit integration. Use `getUncachableGitHubClient()` from `src/lib/github.ts` to interact with GitHub repositories.

## Recent Changes
- December 3, 2025: Added GitHub integration with Octokit client
- December 2, 2025: Initial project setup with minimal template
