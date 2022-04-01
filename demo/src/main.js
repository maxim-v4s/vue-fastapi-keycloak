import Vue from 'vue'
import App from './App.vue'
import Keycloak from "keycloak-js";
import VueCookies from 'vue-cookies';

Vue.config.productionTip = false
Vue.use(VueCookies)

new Vue({
  render: h => h(App),
}).$mount('#app')

let initOptions = {
  url: 'http://0.0.0.0:8080/', realm: 'entropy_hub', clientId: 'fe-client', onLoad: 'login-required'
}

let keycloak = Keycloak(initOptions);

console.log(keycloak)

keycloak.init({ onLoad: initOptions.onLoad }).then((auth) => {
  console.log('auth: ', auth);
  if (!auth) {
    window.location.reload();
  } else {
    console.log("Authenticated");
    Vue.$cookies.set("test_token", keycloak.token)

    new Vue({
      el: '#app',
      render: h => h(App, { props: { keycloak: keycloak } }),
    })
  }

//Token Refresh
  setInterval(() => {
    keycloak.updateToken(70).then((refreshed) => {
      if (refreshed) {
        console.info('Token refreshed' + refreshed);
      } else {
        console.warn('Token not refreshed, valid for '
          + Math.round(keycloak.tokenParsed.exp + keycloak.timeSkew - new Date().getTime() / 1000) + ' seconds');
      }
    }).catch(() => {
      console.error('Failed to refresh token');
    });
  }, 100000)

}).catch((e) => {
  console.error(e)
  console.error("Authenticated Failed");
});

let func = () => {
  // console.log(Vue.$cookies.keys())
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer '+ Vue.$cookies.get("test_token")
    },
  };
  fetch('http://localhost:5000/user/', requestOptions)
    .then(async response => {
      const data = await response.json();
      console.log("from BE: ", data)
      // check for error response
      if (!response.ok) {
        // get error message from body or default to response status
        const error = (data && data.message) || response.status;
        return Promise.reject(error);
      }
    })
    .catch(error => {
      // this.errorMessage = error;
      console.error('There was an error!', error);
    });
}

setTimeout(func, 1000)
