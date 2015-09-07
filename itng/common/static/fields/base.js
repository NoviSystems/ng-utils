
import $ from 'bootstrap';
import _ from 'underscore';
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
        const $input = $(this.$el).find('input');
        $input.addClass('form-control');
        this.inputId = $input.attr('id');
    },

    computed: {
        hasError: function() {
            return !_.isEmpty(this.errors);
        },
    },
});
