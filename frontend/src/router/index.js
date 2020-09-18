import Vue from 'vue'
import Router from 'vue-router'
import MainPage from '../components/MainPage'
import LogIn from '../components/LogIn'
import ForgetPassword from '../components/ForgetPassword'
import SpeakerAnalyse from '../components/SpeakerAnalyse'
import YearWordCloud from '../components/yearWordCloud'
import PeopleWordCloud from '../components/peopleWordCloud'
import PartyWordCloud from '../components/partyWordCloud'
import SpeakerChoice from '../components/SpeakerChoice'
import PartyChoice from '../components/PartyChoice'
import SpeakerChoiceCloud from '../components/SpeakerChoice-cloud'
import PartyChoiceCloud from '../components/PartyChoice-cloud'
import TFAnalyseYear from '../components/TFAnalyse-year'
import TFAnalyseLocation from '../components/TFAnalyse-location'
import PartyAnalyse from '../components/PartyAnalyse'
import NewsPresent from '../components/NewsPresent'
import ModelComparison from '../components/ModelComparison'
import NewsAnalysis from '../components/NewsAnalysis'
import Search from "../components/Search";
import axios from 'axios'
import VueAxios from 'vue-axios'
import qs from 'qs'
import Register from "../components/Register";
import Training from "../components/Training";
import Horizontal from "../components/Horizontal";

axios.defaults.headers.post['Content-Type'] = 'application/json';
Vue.prototype.$qs = qs;
Vue.use(VueAxios, axios);
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/', component: MainPage, meta: {
      }
    },
    {path: '/login', component: LogIn},
    {path: '/reset', component: ForgetPassword},
    {path: '/register', component: Register},
    {
      path: '/speaker', component: SpeakerAnalyse, meta: {
        required: true,
      }
    },
    {
      path: '/yearWordCloud', component: YearWordCloud, meta: {
        required: true,
      }
    },
    {
      path: '/peopleWordCloud', component: PeopleWordCloud, meta: {
        required: true,
      }
    },
    {
      path: '/partyWordCloud', component: PartyWordCloud, meta: {
        required: true,
      }
    },
    {
      path: '/speakerChoice', component: SpeakerChoice, meta: {
        required: true,
      }
    },
    {
      path: '/partyChoice', component: PartyChoice, meta: {
        required: true,
      }
    },
    {
      path: '/choiceClouds', component: SpeakerChoiceCloud, meta: {
        required: true,
      }
    },
    {
      path: '/choiceCloudp', component: PartyChoiceCloud, meta: {
        required: true,
      }
    },
    {
      path: '/location', component: TFAnalyseLocation, meta: {
        required: true,
      }
    },
    {
      path: '/year', component: TFAnalyseYear, meta: {
        required: true,
      }
    },
    {
      path: '/party', component: PartyAnalyse, meta: {
        required: true,
      },
    },
    {
      path: '/newsPresent', component: NewsPresent, meta: {
        required: true,
      },
    },
    {
      path: '/modelComparison', component: ModelComparison, meta: {
        required: true,
      },
    },
    {
      path: '/newsAnalysis', component: NewsAnalysis, meta: {
        required: true,
      },
    },
    {
      path: '/searchCenter', component: Search, meta: {
        required: true,
      },
    },
    {
      path: '/train', component: Training, meta: {
        required: true,
      },
    },
    {
      path: '/vis/horizontal', component: Horizontal, meta: {
        required: true,
      },
    }
  ],
  mode: 'history'
})
