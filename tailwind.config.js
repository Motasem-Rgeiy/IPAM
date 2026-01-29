/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./templates/**/*.html",
      "./**/templates/**/*.html", // Picks up templates in app folders
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}