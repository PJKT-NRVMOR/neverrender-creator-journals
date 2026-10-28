export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        themePrimary: '#ff007f', // Neon Pink
        themeSecondary: '#00ffff', // Cyber Cyan
        themeTertiary: '#ffbf00', // Laser Amber
        themeQuaternary: '#3a0088', // Midnight Purple
      },
      fontFamily: {
        terminal: ['"Share Tech Mono"', 'monospace'],
      }
    },
  },
  plugins: [],
}
