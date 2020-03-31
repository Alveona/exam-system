<template>
  <div class="l-auth-container">
    <!--
    <div class="authTitle">
        <v-card-text>
          <h2 class="display-3 text-lg-center">Service Title</h2>
        </v-card-text>
    </div>
  -->
    <div class="l-auth">
      <v-form v-model="validLogin">
        <v-layout row justify-space-around>
          <v-flex xs12>
            <p class="title text-md-center" px-3><span class="light-blue--text text--lighten-1">Вход</span></p>
          </v-flex>
        </v-layout>
        <v-text-field label="Логин"
                      v-model="credentials.username"
                      prepend-icon="account_box"
                      :rules="rules"
                      required
                      color="light-blue lighten-1"
                      class="error-text">
        </v-text-field>

        <v-text-field label="Пароль"
                      v-model="credentials.password"
                      prepend-icon="lock"
                      :rules="rules"
                      :append-icon="loginPasswordVisible ? 'visibility' : 'visibility_off'"
                      :append-icon-cb="() => (loginPasswordVisible = !loginPasswordVisible)"
                      :type="loginPasswordVisible ? 'text' : 'password'"
                      color="light-blue lighten-1"
                      required>
        </v-text-field>

        <v-btn block color="light-blue lighten-1" @click.native="submitAuthentication()">Войти</v-btn>
        <v-btn block flat color="light-blue lighten-1" @click.native="goToRegister()">Создать аккаунт</v-btn>
      </v-form>
    </div>

    <v-snackbar :timeout="timeout"
                bottom="bottom"
                color="red lighten-1"
                v-model="snackbar">
      {{ message }}
    </v-snackbar>
  </div>
</template>

<script>
  import Authentication from '@/components/pages/Authentication'
  import router from '@/router'
  export default {
    data () {
      return {
        snackbar: false,
        validLogin: false,
        loginPasswordVisible: false,
        timeout: 6000,
        rules: [ (value) => !!value || 'Это обязательное поле' ],
        credentials: {
          username: '',
          password: ''
        },
        message: ''
      }
    },
    methods: {
      submitAuthentication () {
        Authentication.authenticate(this, this.credentials, '/')
      },
      goToRegister() {
        router.push('/register')
      },
    }
  }
</script>

<style lang="scss">
  @import "./../../../assets/styles";

  .l-auth {
    background-color: $background-color;
    padding: 15px;
    margin: 125px auto;
    min-width: 272px;
    max-width: 320px;
    animation: bounceIn 1s forwards ease;
    box-shadow: 0 8px 8px 2px #999999;

    label,input, .icon {
      color: #29b6f6!important;
    }

  }

  .v-text-field__slot>label{
    color: #29b6f6 !important;
  }
</style>
