/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        cpip: {
          emerald: "#20785A",
          teal: "#2D7478",
          cobalt: "#456FA3",
        },
      },
    },
  },
  plugins: [],
};
