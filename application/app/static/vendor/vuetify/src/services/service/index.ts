// Contracts
import { VuetifyServiceContract } from 'app/static/vendor/vuetify/types/services'

// Types
import Vue from 'vue'

export class Service implements VuetifyServiceContract {
  framework = {}

  init (root: Vue, ssrContext?: object) {}
}
