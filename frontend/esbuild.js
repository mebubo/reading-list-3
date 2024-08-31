import * as esbuild from 'esbuild'

esbuild
  .build({
    entryPoints: [
      "./src/background.ts",
      "./src/content.ts",
      "./src/popup.tsx",
    ],
    bundle: true,
    minify: false,
    sourcemap: process.env.NODE_ENV !== "production",
    target: ["chrome120", "firefox110"],
    outdir: "./public/extension/",
    define: {
      "process.env.NODE_ENV": `"${process.env.NODE_ENV}"`
    }
  })
  .catch(() => process.exit(1))
