
import $ from 'bootstrap';
import _ from 'underscore';
import Vue from 'vue';


export default Vue.extend({
    props: ['label', 'help-text', 'required', 'errors'],

    data: function () {
        return {
            inputId: null,
            hasError: false,
        };
    },

    attached: function () {
        var $input = $(this.$el).find('input');
        $input.addClass('form-control');
        this.inputId = $input.attr('id');
        this.hasError = !_.isEmpty(this.errors);
    },
});
