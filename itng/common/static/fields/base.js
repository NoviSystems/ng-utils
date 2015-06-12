
import $ from 'bootstrap';
import _ from 'underscore';
import Vue from 'vue';


var Field = Vue.extend({
    paramAttributes: ['label', 'help-text', 'required', 'errors'],
    inherit: true,

    data: function () {
        return {
            inputId: null,
            hasError: false,
        }
    },

    attached: function () {
        var $input = $(this.$el).find('input');
        $input.addClass('form-control');
        this.inputId = $input.attr('id');
        this.hasError = !_.isEmpty(this.errors);
    },
})

export default Field;
