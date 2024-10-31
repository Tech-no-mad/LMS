import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from '../components/UserLogin.vue'
import LibrarianLogin from '../components/LibrarianLogin.vue'
import Start from '@/components/Start.vue'
import UserReg from '@/components/UserReg.vue'
import DeleteUser from '@/components/DeleteUser.vue'
import UpdateUser from '@/components/UpdateUser.vue'
import Dummy from '@/components/Dummy.vue'
import LibDash from '@/components/LibDashboard.vue'
import AddSec from '@/components/SectionAdd.vue'
import MAddSec from '@/components/Mod_SecAdd.vue'
import EditSec from '@/components/EditSec.vue'
import AddBook from '@/components/BookAdd.vue'
import BookDisplay from '@/components/BookDisplay.vue'
import EditBook from '@/components/EditBook.vue'
import ReportLib from '@/components/ReportLib.vue'
import UserDashboard from '@/components/UserDashboard.vue'
import Mybooks from '@/components/MyBooks.vue'
import Requests from '@/components/RequestsPage.vue'


const routes = [
  {
    path: '/',
    name: 'start',
    component: Start // Set start.vue as the default component
  },
  {
    path: '/user-login',
    name: 'user-login',
    component: UserLogin,
    meta: {libnav:false, showNavbar: true }
  },
  {
    path: '/register', // This is the path for the UserReg component
    name: 'UserReg',
    component: UserReg,
    meta: {libnav:false, showNavbar: true }
  },
  {
    path: '/user-dashboard',
    name: 'user-dashboard',
    component: UserDashboard,
    meta: {libnav:false, showNavbar: true }
  },
  {
    path: '/librarian-login',
    name: 'librarian-login',
    component: LibrarianLogin,
    meta: { showNavbar: false,libnav:true }
  },
  {
    path: '/delete-user',
    name: 'DeleteUser',
    component: DeleteUser,
    meta: {libnav:false, showNavbar: true } // Adjust the path as necessary
  },
  {
    path: '/update-user',
    name: 'UpdateUser',
    component: UpdateUser,
    meta: {libnav:false, showNavbar: true } // Adjust the path as necessary
  },
  {
    path: '/up-del',
    name: 'Dummy',
    component: Dummy,
    meta: {libnav:false, showNavbar: true }
  },
  {
    path: '/my-books',
    name: 'MyBooks',
    component: Mybooks,
    meta: {libnav:false, showNavbar: true }
  },
  {
    path: '/libdash',
    name: 'LibDash',
    component: LibDash,
    meta: { showNavbar: false,libnav:true }
  },
  {
    path: '/add-section',
    name: 'add-section',
    component: AddSec,
    meta: { showNavbar: false,libnav:true }
  },
  {
    path: '/mod-add-section',
    name: 'mod-add-section',
    component: MAddSec,
    meta: { showNavbar: false,libnav:true }
  },
  {
    path: '/edit-section',
    name: 'edit-section',
    component: EditSec,
    meta: { showNavbar: false,libnav:true }
  },
  {
    path: '/add-book',
    name: 'add-book',
    component: AddBook,
    meta: { showNavbar: false,libnav:true }
  },
  {
    path: '/display-book',
    name: 'display-book',
    component: BookDisplay,
    meta: { showNavbar: false,libnav:true }
  },
  
  {
    path: '/edit-book',
    name: 'edit-book',
    component: EditBook,
    meta: { showNavbar: false,libnav:true }
  },

  {
    path: '/report',
    name: 'report-all',
    component: ReportLib,
    meta: { showNavbar: false,libnav:true }
  },
  {
    path: '/requests',
    name: 'requests-page',
    component: Requests,
    meta: { showNavbar: false,libnav:true }
  },

 
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
