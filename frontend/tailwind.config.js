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
          fontWeight: "600", // semibold
          fontSize: "1rem", // base font size
          "@screen md": {
            fontSize: "1.25rem", // xl for medium screens and up
          },
        },
        ".subtitle": {
          color: "#075985", // sky-800
          fontWeight: "700", // bold
          fontSize: "1.5rem", // 2xl base font size
          "@screen md": {
            fontSize: "1.875rem", // 3xl for medium screens and up
          },
        },
      })
    },
  ],
}
