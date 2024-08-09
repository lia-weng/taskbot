module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [
    function ({ addUtilities }) {
      addUtilities({
        ".big-text": {
          color: "#4b5563", // gray-600
          fontSize: "1.25rem", // xl
          fontWeight: "600", // semibold
        },
      })
    },
  ],
}
