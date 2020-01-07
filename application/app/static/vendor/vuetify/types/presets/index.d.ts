import { Breakpoint } from 'app/static/vendor/vuetify/types/services/breakpoint'
import { Icons } from 'app/static/vendor/vuetify/types/services/icons'
import { Lang } from 'app/static/vendor/vuetify/types/services/lang'
import { Theme } from 'app/static/vendor/vuetify/types/services/theme'

export interface VuetifyPreset {
  [name: string]: any

  breakpoint?: Partial<Breakpoint>
  icons?: Partial<Icons>
  lang?: Partial<Lang>
  theme?: { [P in keyof Theme]?: Partial<Theme[P]> }
}
