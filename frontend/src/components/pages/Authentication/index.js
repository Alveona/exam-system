import Axios from 'axios'
import router from '@/router'

const TestingSystemAPI = 'http://10.0.1.5:8000'

export default {
  user: { authenticated: false },

  authenticate (context, credentials, redirect) {
    Axios.post(`${TestingSystemAPI}/token-auth/`, credentials)
        .then(({data}) => {
          context.$cookie.set('token', data.token, '1D')
          //context.$cookie.set('user_id', data.user._id, '1D')
          context.validLogin = true

          this.user.authenticated = true

          if (redirect) router.push(redirect)
        }).catch(error => {
          context.snackbar = true
          context.message = 'Неверный логин или пароль'
        })
  },

  signup (context, credentials, redirect) {
    Axios.post(`${TestingSystemAPI}/api/accounts/register/`, credentials)
        .then(() => {
          context.validSignUp = true

          this.authenticate(context, credentials, redirect)
        }).catch(error => {
          context.snackbar = true
          context.message = 'Не удалось зарегистрироваться'
        })
  },

  signout (context, redirect) {
    context.$cookie.delete('token')
    context.$cookie.delete('user_id')
    this.user.authenticated = false

    if (redirect) router.push(redirect)
  },

  checkAuthentication () {
    const token = document.cookie
    this.user.authenticated = !!token
  },

  getAuthenticationHeader (context) {
    return `JWT ${context.$cookie.get('token')}`
  }
}
