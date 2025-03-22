/** @type {import('tailwindcss').Config} */
export default {
    content: ["./src/**/*.{js,jsx,ts,tsx}"],
    theme: {
      extend: {
        fontFamily: {
          gothic: ["UnifrakturMaguntia", "cursive"],
          elegant: ["Cinzel", "serif"],
        },
        colors: {
          dark: "#0a000f",
          blood: "#8b0000",
          ember: "#ff4444",
        },
        boxShadow: {
          demon: "0px 0px 20px #ff0000",
        },
      },
    },
    plugins: [],
  };
  