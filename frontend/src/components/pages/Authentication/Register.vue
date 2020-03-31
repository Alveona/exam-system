<template>
  <div class="l-auth-container">
    <!--
    <div class="authTitle">
        <v-card-text>
          <h2 class="display-3 text-lg-center">Service Title</h2>
        </v-card-text>
    </div>
  -->


    <div class="l-signup">
      <v-form ref="validSignUp">

        <v-layout row justify-space-around>
          <v-flex xs12>
            <p class="title text-md-center mt-2" px-3><span class="light-blue--text text--lighten-1">Регистрация профиля</span></p>
          </v-flex>
        </v-layout>
        <v-text-field label="Логин"
                      v-model="newUser.username"
                      prepend-icon="account_box"
                      :rules="rules"
                      required
                      color="light-blue lighten-1">
        </v-text-field>

        <v-text-field label="Пароль"
                      v-model="newUser.password"
                      prepend-icon="lock"
                      :rules="rules"
                      :append-icon="signUpPasswordVisible ? 'visibility' : 'visibility_off'"
                      :append-icon-cb="() => (signUpPasswordVisible = !signUpPasswordVisible)"
                      :type="signUpPasswordVisible ? 'text' : 'password'"
                      color="light-blue lighten-1"
                      required>
        </v-text-field>

        <v-text-field label="Имя"
                      v-model="newUser.name"
                      prepend-icon="account_circle"
                      :rules="rules"
                      required
                      color="light-blue lighten-1">
        </v-text-field>

        <v-text-field label="Фамилия"
                      v-model="newUser.surname"
                      prepend-icon="account_circle"
                      :rules="rules"
                      required
                      color="light-blue lighten-1">
        </v-text-field>

        <v-text-field label="Место учебы\работы"
                      v-model="newUser.activity"
                      prepend-icon="domain"
                      color="light-blue lighten-1">
        </v-text-field>

        <v-text-field label="Телефон"
                      v-model="newUser.phone"
                      prepend-icon="phone"
                      color="light-blue lighten-1">
        </v-text-field>

        <v-btn block color="light-blue lighten-1" @click.native="submitSignUp()">Зарегистрироваться</v-btn>
        <v-btn block flat color="light-blue lighten-1" @click.native="goBack()">< Назад к авторизации</v-btn>
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
        validSignUp: false,
        signUpPasswordVisible: false,
        timeout: 6000,
        rules: [ (value) => !!value || 'Это обязательное поле' ],
        newUser: {
          username: '',
          password: '',
          name: '',
          surname: '',
          activity: '',
          group: '',
          phone: null,
          image: null
        },
        message: ''
      }
    },
    methods: {
      submitSignUp () {
        if (!this.$refs.validSignUp.validate())
        {
          this.snackbar = true
          this.message = 'Не все обязательные поля были заполнены.'
          return
        }
        Authentication.signup(this, this.newUser, '/')
      },
      goBack() {
        router.push('/login')
      },
    }
  }
</script>

<style lang="scss">
  @import "./../../../assets/styles";

  .l-auth {
    background-color: $background-color;
    padding: 15px;
    margin: 45px auto;
    min-width: 272px;
    max-width: 320px;
    animation: bounceIn 1s forwards ease;

    label,input, .icon {
      color: #29b6f6!important;
    }

  }

  .l-signup {
    @extend .l-auth;
    animation: slideInFromLeft 1s forwards ease;
    box-shadow: 0 8px 8px 2px #999999;
  }
  .v-text-field__slot>label{
    color: #29b6f6 !important;
  }
</style>
