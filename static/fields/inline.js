
import BaseField from './base';
import template from './templates/inline.html!text';


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
    computed: {
        labelClasses: function() {
            const classes = ['control-label'];
            if (this.required)
                classes.push('required');

            if (Array.isArray(this.labelClass))
                classes.push(...this.labelClass);
            else
                classes.push(this.labelClass);

            return classes;
        },
    },
});
