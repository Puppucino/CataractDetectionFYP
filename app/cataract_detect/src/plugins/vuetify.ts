/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          background: '#f5faff',
          surface: '#ffffff',
          primary: '#0a4d6e',
          secondary: '#1abc9c',
          accent: '#1976d2',
          error: '#e53935',
          info: '#2196f3',
          success: '#43a047',
          warning: '#fbc02d',
        },
      },
    },
  },
})
