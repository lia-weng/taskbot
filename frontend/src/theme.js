import { createTheme } from "@mui/material/styles"

// Define Tailwind colors
const tailwindColors = {
  sky900: "#0c4a6e",
  sky800: "#075985",
  sky600: "#0284c7",
  gray600: "#4b5563",
}

const theme = createTheme({
  palette: {
    primary: {
      main: tailwindColors.sky800,
      light: tailwindColors.sky600,
      dark: tailwindColors.sky900,
      contrastText: "#fff",
    },
    // Additional palette options can be added here
  },
  // Other theme customizations can be added here
})

export default theme
