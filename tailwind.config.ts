import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          purple: "#A855F7",
          green: "#00FF41",
        },
        dark: {
          bg: "#0a0a0a",
          surface: "#1a1a1a",
          border: "#2a2a2a",
        },
      },
      fontFamily: {
        mono: ["'Geist Mono'", "'Fira Code'", "monospace"],
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
export default config;

