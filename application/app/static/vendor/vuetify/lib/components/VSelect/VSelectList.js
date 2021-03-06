// Styles
import "../../../src/components/VCard/VCard.sass"; // Components

import VSimpleCheckbox from '../VCheckbox/VSimpleCheckbox';
import VDivider from '../VDivider';
import VSubheader from '../VSubheader';
import { VList, VListItem, VListItemAction, VListItemContent, VListItemTitle } from '../VList'; // Directives

import ripple from '../../directives/ripple'; // Mixins

import Colorable from '../../mixins/colorable';
import Themeable from '../../mixins/themeable'; // Helpers

import { escapeHTML, getPropertyFromItem } from '../../util/helpers'; // Types

import mixins from '../../util/mixins';
/* @vue/component */

export default mixins(Colorable, Themeable).extend({
  name: 'v-select-list',
  // https://github.com/vuejs/vue/issues/6872
  directives: {
    ripple
  },
  props: {
    action: Boolean,
    dense: Boolean,
    hideSelected: Boolean,
    items: {
      type: Array,
      default: () => []
    },
    itemDisabled: {
      type: [String, Array, Function],
      default: 'disabled'
    },
    itemText: {
      type: [String, Array, Function],
      default: 'text'
    },
    itemValue: {
      type: [String, Array, Function],
      default: 'value'
    },
    noDataText: String,
    noFilter: Boolean,
    searchInput: {
      default: null
    },
    selectedItems: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    parsedItems() {
      return this.selectedItems.map(item => this.getValue(item));
    },

    tileActiveClass() {
      return Object.keys(this.setTextColor(this.color).class || {}).join(' ');
    },

    staticNoDataTile() {
      const tile = {
        attrs: {
          role: undefined
        },
        on: {
          mousedown: e => e.preventDefault()
        }
      };
      return this.$createElement(VListItem, tile, [this.genTileContent(this.noDataText)]);
    }

  },
  methods: {
    genAction(item, inputValue) {
      return this.$createElement(VListItemAction, [this.$createElement(VSimpleCheckbox, {
        props: {
          color: this.color,
          value: inputValue
        },
        on: {
          input: () => this.$emit('select', item)
        }
      })]);
    },

    genDivider(props) {
      return this.$createElement(VDivider, {
        props
      });
    },

    genFilteredText(text) {
      text = text || '';
      if (!this.searchInput || this.noFilter) return escapeHTML(text);
      const {
        start,
        middle,
        end
      } = this.getMaskedCharacters(text);
      return `${escapeHTML(start)}${this.genHighlight(middle)}${escapeHTML(end)}`;
    },

    genHeader(props) {
      return this.$createElement(VSubheader, {
        props
      }, props.header);
    },

    genHighlight(text) {
      return `<span class="v-list-item__mask">${escapeHTML(text)}</span>`;
    },

    genLabelledBy(item) {
      const text = escapeHTML(this.getText(item).split(' ').join('-').toLowerCase());
      return `${text}-list-item-${this._uid}`;
    },

    getMaskedCharacters(text) {
      const searchInput = (this.searchInput || '').toString().toLocaleLowerCase();
      const index = text.toLocaleLowerCase().indexOf(searchInput);
      if (index < 0) return {
        start: '',
        middle: text,
        end: ''
      };
      const start = text.slice(0, index);
      const middle = text.slice(index, index + searchInput.length);
      const end = text.slice(index + searchInput.length);
      return {
        start,
        middle,
        end
      };
    },

    genTile(item, disabled = null, value = false) {
      if (!value) value = this.hasItem(item);

      if (item === Object(item)) {
        disabled = disabled !== null ? disabled : this.getDisabled(item);
      }

      const tile = {
        attrs: {
          // Default behavior in list does not
          // contain aria-selected by default
          'aria-selected': String(value),
          'aria-labelledby': this.genLabelledBy(item),
          role: 'option'
        },
        on: {
          mousedown: e => {
            // Prevent onBlur from being called
            e.preventDefault();
          },
          click: () => disabled || this.$emit('select', item)
        },
        props: {
          activeClass: this.tileActiveClass,
          disabled,
          ripple: true,
          inputValue: value
        }
      };

      if (!this.$scopedSlots.item) {
        return this.$createElement(VListItem, tile, [this.action && !this.hideSelected && this.items.length > 0 ? this.genAction(item, value) : null, this.genTileContent(item)]);
      }

      const parent = this;
      const scopedSlot = this.$scopedSlots.item({
        parent,
        item,
        attrs: { ...tile.attrs,
          ...tile.props
        },
        on: tile.on
      });
      return this.needsTile(scopedSlot) ? this.$createElement(VListItem, tile, scopedSlot) : scopedSlot;
    },

    genTileContent(item) {
      const innerHTML = this.genFilteredText(this.getText(item));
      return this.$createElement(VListItemContent, [this.$createElement(VListItemTitle, {
        attrs: {
          id: this.genLabelledBy(item)
        },
        domProps: {
          innerHTML
        }
      })]);
    },

    hasItem(item) {
      return this.parsedItems.indexOf(this.getValue(item)) > -1;
    },

    needsTile(slot) {
      return slot.length !== 1 || slot[0].componentOptions == null || slot[0].componentOptions.Ctor.options.name !== 'v-list-item';
    },

    getDisabled(item) {
      return Boolean(getPropertyFromItem(item, this.itemDisabled, false));
    },

    getText(item) {
      return String(getPropertyFromItem(item, this.itemText, item));
    },

    getValue(item) {
      return getPropertyFromItem(item, this.itemValue, this.getText(item));
    }

  },

  render() {
    const children = [];

    for (const item of this.items) {
      if (this.hideSelected && this.hasItem(item)) continue;
      if (item == null) children.push(this.genTile(item));else if (item.header) children.push(this.genHeader(item));else if (item.divider) children.push(this.genDivider(item));else children.push(this.genTile(item));
    }

    children.length || children.push(this.$slots['no-data'] || this.staticNoDataTile);
    this.$slots['prepend-item'] && children.unshift(this.$slots['prepend-item']);
    this.$slots['append-item'] && children.push(this.$slots['append-item']);
    return this.$createElement('div', {
      staticClass: 'v-select-list v-card',
      class: this.themeClasses
    }, [this.$createElement(VList, {
      attrs: {
        id: this.$attrs.id,
        role: 'listbox',
        tabindex: -1
      },
      props: {
        dense: this.dense
      }
    }, children)]);
  }

});
//# sourceMappingURL=VSelectList.js.map