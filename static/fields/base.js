
import $ from 'bootstrap';
import Vue from 'vue';


export default Vue.extend({
    props: ['label', 'help-text', 'required', 'errors'],

    data: function() {
        return {
            inputId: null,
            hasError: false,
        };
    },

    attached: function() {
        const $input = $(this.$el).find('input, textarea, select');
        $input.addClass('form-control');
        this.inputId = $input.attr('id');
    },

    computed: {
        labelClasses: function() {
            const classes = ['control-label'];
            if (this.required)
                classes.push('required');
            return classes;
        },

        hasError: function() {
            return this.errors !== undefined && this.errors.length === 0;
        },
    },
});
