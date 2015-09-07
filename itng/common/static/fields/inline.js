
import BaseField from 'fields/base';
import template from 'fields/templates/inline.html!text';


export default BaseField.extend({
    props: ['label', 'help-text', 'required', 'errors', 'label-class', 'input-class'],
    template: template,

    data: function() {
        return {
            inputId: null,
            hasError: false,
            labelClass: 'col-md-3 col-sm-5',
            inputClass: 'col-md-9 col-sm-7',
        };
    },
});
