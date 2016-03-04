
import Vue from 'vue';
import template from './templates/height.html!text';


export default Vue.extend({
    props: ['model'],
    template: template,

    data: function() {
        return {
            feet: this.model ? Math.trunc(this.model / 12) : '',
            inches: this.model ? this.model % 12 : '',
        };
    },

    watch: {
        feet: function(value) {
            this.model = (12 * value) + this.inches;
        },

        inches: function(value) {
            this.model = (12 * this.feet) + value;
        },

        model: function(value) {
            const inputHeight = (12 * this.feet) + this.inches;

            // Compare the new model height to the computed height from the field inputs.
            // If they're the same, this indicates that the model was set by the input
            // watchers. If it's a different value, this implies that the value was
            // changed externally by the parent Vue or otherwise.
            if (value !== inputHeight) {
                this.feet = Math.trunc(this.model / 12);
                this.inches = this.model % 12;
            }
        },
    },
});
