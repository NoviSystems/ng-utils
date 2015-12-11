
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
                // Use a separate object to hold bound methods, as
                // we don't want to overwrite the unbound methods.
                const unbound = this.constructor.super.options.methods;
                const bound = {};

                for (const key of Object.keys(unbound))
                    bound[key] = unbound[key].bind(this);

                return bound;
            },
        },
    });
}


if (window.Vue) {
    window.Vue.use(install);
}
