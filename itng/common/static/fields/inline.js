
import BaseField from 'fields/base';
import template from 'fields/templates/inline.html!text';


export default BaseField.extend({
    props: {
        label: {default: ''},
        required: {default: true},
        errors: {default: ''},
        'help-text': {default: ''},
        'label-class': {default: () => ['col-md-3', 'col-sm-5']},
        'input-class': {default: () => ['col-md-9', 'col-sm-7']},
    },
    template: template,

    data: function() {
        return {
            inputId: null,
            hasError: false,
        };
    },
});
