/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        forthing: {
          black: "#222223",
          darkGray: "#4B4F54",
          gray: "#75787B",
          lightGray: "#A0A3A6",
          red: "#DD0A14",
          redHover: "#BE0811",
          cardBg: "#1C1C1D",
          surface: "#2A2D30",
          border: "#3D4145"
        }
      },
      fontFamily: {
        sans: ['"Inter"', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        display: ['"Montserrat"', '"Inter"', 'sans-serif']
      },
      letterSpacing: {
        widestAutomotive: '0.2em',
      }
    },
  },
  plugins: [],
}
