import 'vuetify/styles' // Vuetify 스타일 추가
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2', // 기본 색상
          secondary: '#424242',
          accent: '#82B1FF',
          error: '#FF5252',
        },
      },
    },
  },
})
