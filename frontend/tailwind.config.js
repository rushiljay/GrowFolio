// tailwind.config.js
const {nextui} = require("@nextui-org/react");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  darkMode: "class",
  plugins: [
    nextui({
      themes: {
        light: {
          colors: {
            default: {
              DEFAULT: "#000000",
              foreground: "#ffffff",
            },
            focus: "#F8B324",
            primary: {
              DEFAULT: "#F8B324",
              foreground: "#ffffff",
            },
          },
        },
      },
    }),
  ],
};