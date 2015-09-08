
/**
 * Provides a $super handler for accessing parent methods from a subclass.
 *
 * Example:
 *
 *     const Parent = Vue.extend({
 *         methods:{
 *             doTheThing: function(){
 *                 console.log('performing a parental action');
 *             }
 *         }
 *     })
 *
 *     const Child = Parent.extend({
 *         methods:{
 *             doTheThing: function(){
 *                 this.$super.doTheThing();
 *                 console.log('doing a childlike thing');
 *             }
 *         }
 *     })
 */
export default function install(Vue) {
    Object.defineProperties(Vue.prototype, {
        $super: {
            get: function() {
                const methods = this.constructor.super.options.methods;

                for (const key of Object.keys(methods))
                    methods[key] = methods[key].bind(this);

                return methods;
            },
        },
    });
}


if (window.Vue) {
    window.Vue.use(install);
}
