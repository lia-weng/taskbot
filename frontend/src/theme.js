import { createTheme } from "@mui/material/styles"

// Define Tailwind colors
const tailwindColors = {
  sky800: "#075985", // Tailwind sky-800 color
  sky600: "#0284c7", // Tailwind sky-600 color
  gray600: "#4b5563", // Tailwind gray-600 color
}

const theme = createTheme({
  palette: {
    primary: {
      main: tailwindColors.sky800,
    },
    secondary: {
      main: tailwindColors.sky600,
    },
    text: {
      primary: tailwindColors.gray600, // Example usage for text color
    },
    // Additional palette options can be added here
  },
  // Other theme customizations can be added here
})

export default theme
