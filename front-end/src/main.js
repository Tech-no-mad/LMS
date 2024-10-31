import { createApp } from 'vue'
import App from './App.vue'
import navbar from '@/components/Navbar.vue'
import userlogin from '@/components/UserLogin.vue'
import liblogin from '@/components/LibrarianLogin.vue'
import start from '@/components/Start.vue'
import deleteuser from '@/components/DeleteUser.vue'
import updateuser from '@/components/UpdateUser.vue'
import dummy from '@/components/Dummy.vue'
import libdash from '@/components/LibDashboard.vue'
import libnav from '@/components/LibNavBar.vue'
import secadd from '@/components/SectionAdd.vue'
import modsecadd from '@/components/Mod_SecAdd.vue'
import secedit from '@/components/EditSec.vue'
import addbook from '@/components/BookAdd.vue'
import bookdisplay from '@/components/BookDisplay.vue'
import userdashboard from '@/components/UserDashboard.vue'
import mybooks from '@/components/MyBooks.vue'
import requests from './components/RequestsPage.vue'

import router from './router'
import store from '@/store.js'

const app = createApp(App)

app.component('nav-bar',navbar)
app.component('lib-nav',libnav)
app.component('user-login',userlogin)
app.component('librarian-login',liblogin)
app.component('start-page',start)
app.component('delete-user',deleteuser)
app.component('update-user',updateuser)
app.component('dummy-cmp',dummy)
app.component('lib-dash',libdash)
app.component('sec-add',secadd)
app.component('mod_secadd',modsecadd)
app.component('edit-sec',secedit)
app.component('add-book',addbook)
app.component('book-display',bookdisplay)
app.component('user-dashboard',userdashboard)
app.component('my-books',mybooks)
app.component('requests-page',requests)


app.use(router)
app.use(store)

app.mount('#app')
