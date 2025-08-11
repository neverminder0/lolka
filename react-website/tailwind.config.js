/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#7C3AED',
          50: '#F3F0FF',
          100: '#E9E5FF',
          200: '#D6CCFF',
          300: '#BBA8FF',
          400: '#9B7AFF',
          500: '#7C3AED',
          600: '#6B21E5',
          700: '#5B15D1',
          800: '#4C0FB5',
          900: '#410A99',
        },
        secondary: {
          DEFAULT: '#22D3EE',
          50: '#F0FDFF',
          100: '#CCFBF1',
          200: '#99F6E4',
          300: '#5EEAD4',
          400: '#2DD4BF',
          500: '#22D3EE',
          600: '#06B6D4',
          700: '#0891B2',
          800: '#0E7490',
          900: '#155E75',
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
}