import "../../../src/components/VIcon/VIcon.sass"; // Mixins

import BindsAttrs from '../../mixins/binds-attrs';
import Colorable from '../../mixins/colorable';
import Sizeable from '../../mixins/sizeable';
import Themeable from '../../mixins/themeable'; // Util

import { convertToUnit, keys, remapInternalIcon } from '../../util/helpers'; // Types

import Vue from 'vue';
import mixins from '../../util/mixins';
var SIZE_MAP;

(function (SIZE_MAP) {
  SIZE_MAP["xSmall"] = "12px";
  SIZE_MAP["small"] = "16px";
  SIZE_MAP["default"] = "24px";
  SIZE_MAP["medium"] = "28px";
  SIZE_MAP["large"] = "36px";
  SIZE_MAP["xLarge"] = "40px";
})(SIZE_MAP || (SIZE_MAP = {}));

function isFontAwesome5(iconType) {
  return ['fas', 'far', 'fal', 'fab'].some(val => iconType.includes(val));
}

function isSvgPath(icon) {
  return /^[mzlhvcsqta]\s*[-+.0-9][^mlhvzcsqta]+/i.test(icon) && /[\dz]$/i.test(icon) && icon.length > 4;
}

const VIcon = mixins(BindsAttrs, Colorable, Sizeable, Themeable
/* @vue/component */
).extend({
  name: 'v-icon',
  props: {
    dense: Boolean,
    disabled: Boolean,
    left: Boolean,
    right: Boolean,
    size: [Number, String],
    tag: {
      type: String,
      required: false,
      default: 'i'
    }
  },
  computed: {
    medium() {
      return false;
    }

  },
  methods: {
    getIcon() {
      let iconName = '';
      if (this.$slots.default) iconName = this.$slots.default[0].text.trim();
      return remapInternalIcon(this, iconName);
    },

    getSize() {
      const sizes = {
        xSmall: this.xSmall,
        small: this.small,
        medium: this.medium,
        large: this.large,
        xLarge: this.xLarge
      };
      const explicitSize = keys(sizes).find(key => sizes[key]);
      return explicitSize && SIZE_MAP[explicitSize] || convertToUnit(this.size);
    },

    // Component data for both font and svg icon.
    getDefaultData() {
      const hasClickListener = Boolean(this.listeners$.click || this.listeners$['!click']);
      const data = {
        staticClass: 'v-icon notranslate',
        class: {
          'v-icon--disabled': this.disabled,
          'v-icon--left': this.left,
          'v-icon--link': hasClickListener,
          'v-icon--right': this.right,
          'v-icon--dense': this.dense
        },
        attrs: {
          'aria-hidden': !hasClickListener,
          role: hasClickListener ? 'button' : null,
          ...this.attrs$
        },
        on: this.listeners$
      };
      return data;
    },

    applyColors(data) {
      data.class = { ...data.class,
        ...this.themeClasses
      };
      this.setTextColor(this.color, data);
    },

    renderFontIcon(icon, h) {
      const newChildren = [];
      const data = this.getDefaultData();
      let iconType = 'material-icons'; // Material Icon delimiter is _
      // https://material.io/icons/

      const delimiterIndex = icon.indexOf('-');
      const isMaterialIcon = delimiterIndex <= -1;

      if (isMaterialIcon) {
        // Material icon uses ligatures.
        newChildren.push(icon);
      } else {
        iconType = icon.slice(0, delimiterIndex);
        if (isFontAwesome5(iconType)) iconType = '';
      }

      data.class[iconType] = true;
      data.class[icon] = !isMaterialIcon;
      const fontSize = this.getSize();
      if (fontSize) data.style = {
        fontSize
      };
      this.applyColors(data);
      return h(this.tag, data, newChildren);
    },

    renderSvgIcon(icon, h) {
      const data = this.getDefaultData();
      data.class['v-icon--svg'] = true;
      data.attrs = {
        xmlns: 'http://www.w3.org/2000/svg',
        viewBox: '0 0 24 24',
        height: '24',
        width: '24',
        role: 'img',
        'aria-hidden': !this.attrs$['aria-label'],
        'aria-label': this.attrs$['aria-label']
      };
      const fontSize = this.getSize();

      if (fontSize) {
        data.style = {
          fontSize,
          height: fontSize,
          width: fontSize
        };
        data.attrs.height = fontSize;
        data.attrs.width = fontSize;
      }

      this.applyColors(data);
      return h('svg', data, [h('path', {
        attrs: {
          d: icon
        }
      })]);
    },

    renderSvgIconComponent(icon, h) {
      const data = this.getDefaultData();
      data.class['v-icon--is-component'] = true;
      const size = this.getSize();

      if (size) {
        data.style = {
          fontSize: size,
          height: size
        };
      }

      this.applyColors(data);
      const component = icon.component;
      data.props = icon.props;
      data.nativeOn = data.on;
      return h(component, data);
    }

  },

  render(h) {
    const icon = this.getIcon();

    if (typeof icon === 'string') {
      if (isSvgPath(icon)) {
        return this.renderSvgIcon(icon, h);
      }

      return this.renderFontIcon(icon, h);
    }

    return this.renderSvgIconComponent(icon, h);
  }

});
export default Vue.extend({
  name: 'v-icon',
  $_wrapperFor: VIcon,
  functional: true,

  render(h, {
    data,
    children
  }) {
    let iconName = ''; // Support usage of v-text and v-html

    if (data.domProps) {
      iconName = data.domProps.textContent || data.domProps.innerHTML || iconName; // Remove nodes so it doesn't
      // overwrite our changes

      delete data.domProps.textContent;
      delete data.domProps.innerHTML;
    }

    return h(VIcon, data, iconName ? [iconName] : children);
  }

});
//# sourceMappingURL=VIcon.js.map