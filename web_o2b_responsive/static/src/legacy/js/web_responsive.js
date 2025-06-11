/* Copyright 2018 Tecnativa - Jairo Llopis
 * Copyright 2021 ITerra - Sergey Shebanin
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define("web_o2b_responsive", function (require) {
    "use strict";

    const config = require("web.config");
    const core = require("web.core");
    const FormRenderer = require("web.FormRenderer");
    const RelationalFields = require("web.relational_fields");
    const ViewDialogs = require("web.view_dialogs");
    const ListRenderer = require("web.ListRenderer");
    const CalendarRenderer = require("web.CalendarRenderer");
    var rpc = require('web.rpc');

    const _t = core._t;

    // Fix for iOS Safari to set correct viewport height
    // https://github.com/Faisal-Manzer/postcss-viewport-height-correction
    function setViewportProperty(doc) {
        function handleResize() {
            requestAnimationFrame(function updateViewportHeight() {
                doc.style.setProperty("--vh100", doc.clientHeight + "px");
            });
        }
        handleResize();
        return handleResize;
    }
    window.addEventListener(
        "resize",
        _.debounce(setViewportProperty(document.documentElement), 100)
    );

    RelationalFields.FieldStatus.include({
        /**
         * Fold all on mobiles.
         *
         * @override
         */
        _setState: function () {
            this._super.apply(this, arguments);
            if (config.device.isMobile) {
                _.map(this.status_information, (value) => {
                    value.fold = true;
                });
            }
        },
    });

    // Sticky Column Selector
    ListRenderer.include({
        _renderView: function () {
            var expire_date = $.ajax({
                type: 'GET',
                url: '/get/expire_date/',
                headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
               
                async: false,
                dataType: 'json',
                data: {},
                done: function(results) {
                    return results;
                },
            }).responseJSON;
            var expire_values = $.ajax({
                type: 'GET',
                url: '/get/expire_values/',
                headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
               
                async: false,
                dataType: 'json',
                data: {},
                done: function(results) {
                    return results;
                },
            }).responseJSON;

            rpc.query({
                model: 'upgrade.database',
                method: 'get_param_values',
                args: [1]
            }).then(function(subscription_id){
                if((subscription_id === 'trial' && expire_values && expire_values != true && 'diffdays' in expire_values)){
                    $('.renew_form').removeClass('display');
                    $('.oe_register').removeClass('display');
                    $('.trialdb').removeClass('display');
                    $('.diffdays').text(expire_values.diffdays);
                }else if((subscription_id !== 'trial' && expire_values && expire_values != true && 'diffdays' in expire_values && 'period' in expire_values && expire_values.period === 'monthly' && expire_values.diffdays <= 15)){
                    $('.renew_form').removeClass('display');
                    $('.livedb').removeClass('display');
                    $('.diffdays').text(expire_values.diffdays);
                    $('.oe_renew').removeClass('display');
                }else if((subscription_id !== 'trial' && expire_values && expire_values != true && 'diffdays' in expire_values && 'period' in expire_values && expire_values.period === 'annually' && expire_values.diffdays <= 30)){
                    $('.renew_form').removeClass('display');
                    $('.livedb').removeClass('display');
                    $('.diffdays').text(expire_values.diffdays);
                    $('.oe_renew').removeClass('display');
                }else if(subscription_id === 'trial' && expire_values){
                    $('.o_main_navbar').addClass('displ');
                    $('.o_action_manager').addClass('displcontent');
                    $('.o_action').addClass('displcontent');
                    $('.o_user_menu').addClass('displuser');
                    $('.o_navbar_apps_menu').addClass('displuser');
                    $('.o_navbar_apps_menu').attr('id', 'displuser');
                    $('.renew_form').removeClass('display');
                    $('.trialdbexpired').removeClass('display');
                    $('.oe_register').removeClass('display');
                }else if(expire_values && expire_values === true){
                    var navc = $('.o_menu_apps')[0].childNodes[0].children;
                    navc[0].click();
                    $('.o_main_navbar').addClass('displ');
                    $('.o_action_manager').addClass('displcontent');
                    $('.o_user_menu').addClass('displuser');
                    $('.o_menu_apps').addClass('displuser');
                    $('.renew_form').removeClass('display');
                    $('.dbexpired').removeClass('display');
                    $('.oe_renew').removeClass('display');
                }

                if ((subscription_id !== 'trial' && expire_values && expire_values != true && 'ext_apps' in expire_values && 'ext_users' in expire_values)){
                    if (expire_values.ext_apps === 'yes' && expire_values.ext_users === 'yes'){
                        $('.extappuser').removeClass('display');
                    }else if (expire_values.ext_apps === 'yes' && expire_values.ext_users === 'no'){
                        $('.extapp').removeClass('display');
                    }else if (expire_values.ext_apps === 'no' && expire_values.ext_users === 'yes'){
                        $('.extuser').removeClass('display');
                    }
                }
                                  
            });
            return this._super.apply(this, arguments).then(() => {
                const $col_selector = this.$el.find(
                    ".o_optional_columns_dropdown_toggle"
                );
                if ($col_selector.length !== 0) {
                    const $th = this.$el.find("thead>tr:first>th:last");
                    $col_selector.appendTo($th);
                }
            });
        },

        _onToggleOptionalColumnDropdown: function (ev) {
            // FIXME: For some strange reason the 'stopPropagation' call
            // in the main method don't work. Invoking here the same method
            // does the expected behavior... O_O!
            // This prevents the action of sorting the column from being
            // launched.
            ev.stopPropagation();
            this._super.apply(this, arguments);
        },
    });

    // Responsive view "action" buttons
    FormRenderer.include({
        /**
         * @override
         */
        on_attach_callback: function () {
            this._super.apply(this, arguments);
            core.bus.on("UI_CONTEXT:IS_SMALL_CHANGED", this, () => {
                this._applyFormSizeClass();
                this._render();
            });
        },
        /**
         * @override
         */
        on_detach_callback: function () {
            core.bus.off("UI_CONTEXT:IS_SMALL_CHANGED", this);
            this._super.apply(this, arguments);
        },
        /**
         * In mobiles, put all statusbar buttons in a dropdown.
         *
         * @override
         */
        _renderHeaderButtons: function () {
            const $buttons = this._super.apply(this, arguments);
            if (
                !config.device.isMobile ||
                $buttons.children("button:not(.o_invisible_modifier)").length <= 2
            ) {
                return $buttons;
            }

            // $buttons must be appended by JS because all events are bound
            const $dropdown = $(
                core.qweb.render("web_o2b_responsive.MenuStatusbarButtons")
            );
            $buttons.addClass("dropdown-menu").appendTo($dropdown);
            return $dropdown;
        },
    });

    /**
     * Directly open popup dialog in mobile for search.
     */
    RelationalFields.FieldMany2One.include({
        start: function () {
            var superRes = this._super.apply(this, arguments);
            if (config.device.isMobile) {
                this.$input.prop("readonly", true);
            }
            return superRes;
        },
        // --------------------------------------------------------------------------
        // Private
        // --------------------------------------------------------------------------

        /**
         * @private
         * @override
         */
        _bindAutoComplete: function () {
            if (!config.device.isMobile) {
                return this._super.apply(this, arguments);
            }
        },

        /**
         * @private
         * @override
         */
        _getSearchCreatePopupOptions: function () {
            const options = this._super.apply(this, arguments);
            _.extend(options, {
                on_clear: () => this.reinitialize(false),
            });
            return options;
        },

        /**
         * @private
         * @override
         */
        _toggleAutoComplete: function () {
            if (config.device.isMobile) {
                this._searchCreatePopup("search");
            } else {
                return this._super.apply(this, arguments);
            }
        },
    });

    /**
     * Support for Clear button in search popup.
     */
    ViewDialogs.SelectCreateDialog.include({
        init: function () {
            this._super.apply(this, arguments);
            this.on_clear =
                this.options.on_clear ||
                function () {
                    return undefined;
                };
        },
        /**
         * @override
         */
        _prepareButtons: function () {
            this._super.apply(this, arguments);
            if (config.device.isMobile && this.options.disable_multiple_selection) {
                this.__buttons.push({
                    text: _t("Clear"),
                    classes: "btn-secondary o_clear_button",
                    close: true,
                    click: function () {
                        this.on_clear();
                    },
                });
            }
        },
    });

    CalendarRenderer.include({
        /**
         * @override
         */
        on_attach_callback: function () {
            this._super.apply(this, arguments);
            core.bus.on("UI_CONTEXT:IS_SMALL_CHANGED", this, () => {
                // Hack to force calendar to reload their options and rerender
                this.calendar.setOption("locale", moment.locale());
            });
        },
        /**
         * @override
         */
        on_detach_callback: function () {
            core.bus.off("UI_CONTEXT:IS_SMALL_CHANGED", this);
            this._super.apply(this, arguments);
        },
        /**
         * @override
         */
        _getFullCalendarOptions: function () {
            const options = this._super.apply(this, arguments);
            Object.defineProperty(options.views.dayGridMonth, "columnHeaderFormat", {
                get() {
                    return config.device.isMobile ? "ddd" : "dddd";
                },
            });
            return options;
        },
    });
});
