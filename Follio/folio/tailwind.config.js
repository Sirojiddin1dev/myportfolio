/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.{html,js}','./node_modules/tw-elements/dist/js/**/*.js',
  ],
  theme: {
  
    extend: {
      spacing: {
        '5px': '5px',
      },
      textColor: ['current'],
    },
     
    screens: {
      '2xl': {'max': '1320px'},
      // => @media (max-width: 1535px) { ... }

      'xl': {'max': '1399px'},
      // => @media (max-width: 1279px) { ... }

      'lg': {'max': '1199px'},
      // => @media (max-width: 1023px) { ... }

      'md': {'max': '991px'},
      // => @media (max-width: 767px) { ... }

      'sm': {'max': '767px'},
      // => @media (max-width: 639px) { ... }

      'col': {'max': '567px'},
      // => @media (max-width: 320px) { ... }
    },
    fontFamily: {
      'base-font': ['Now'],
      'heading-font': ['Now'],
    },
  },

  plugins: [require("tw-elements/dist/plugin.cjs")],

}