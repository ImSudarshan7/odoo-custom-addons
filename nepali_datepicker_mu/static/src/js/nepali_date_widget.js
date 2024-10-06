odoo.define('nepali_datepicker_mu.nepali_date_widget', function (require) {
    var Model = require('web.Model');
    var core = require('web.core');
    var ListView = core.view_registry.get('list')
    var FieldDate = core.form_widget_registry.get('date');
    var datepicker = require('web.datepicker');
    var formats = require('web.formats');
    var data = require('web.data');
    var time = require('web.time');
    var res_users = new Model("res.users");
    var _t = core._t;
    var calendar1;
    var lang = '';
    var date_format = '';
    res_users.call("datepicker_localization", []).then(function (result) {
        lang = result['lang'];
        date_format = result['date_format'];
        date_format = date_format.replace(/%(.)/g, "$1$1").toLowerCase();
        ;
    });
//    ListView.List.include({
//        convert_gregorian_nepali: function (text) {
//            if (text) {
//                text = moment(text, date_format)._i;
//                if (text.indexOf('-') != -1) {
//                    text_split = text.split('-');
//                    year = parseInt(text_split[0]);
//                    month = parseInt(text_split[1]);
//                    day = parseInt(text_split[2]);
//                    calendar = $.calendars.instance('gregorian');
//                    calendar1 = $.calendars.instance('nepali');
//                    var jd = $.calendars.instance('gregorian').toJD(year, month, day);
//                    var date = $.calendars.instance('nepali').fromJD(jd);
//                }
//                if (text.indexOf('/') != -1) {
//                    text_split = text.split('/');
//                    year = parseInt(text_split[2]);
//                    month = parseInt(text_split[0]);
//                    day = parseInt(text_split[1]);
//                    calendar = $.calendars.instance('gregorian');
//                    calendar1 = $.calendars.instance('nepali');
//                    var jd = calendar.toJD(year, month, day);
//                    var date = calendar1.fromJD(jd);
//                }
//                return (calendar1.formatDate('M d, yyyy', date));
//            }
//            return '';
//        },
//        render_cell: function (record, column) {
//            var value;
//            if (column.type === 'date' || column.type === 'datetime') {
//                return column.format(record.toForm().data, {
//                        model: this.dataset.model,
//                        id: record.get('id')
//                    }) + "&nbsp; &nbsp; &nbsp;" + this.convert_gregorian_nepali(column.format(record.toForm().data, {
//                        model: this.dataset.model,
//                        id: record.get('id')
//                    }));
//            }
//            else if (column.type === 'reference') {
//                value = record.get(column.id);
//                var ref_match;
//                if (value && (ref_match = /^([\w\.]+),(\d+)$/.exec(value))) {
//                    var model = ref_match[1],
//                        id = parseInt(ref_match[2], 10);
//                    new data.DataSet(this.view, model).name_get([id]).done(function (names) {
//                        if (!names.length) {
//                            return;
//                        }
//                        record.set(column.id + '__display', names[0][1]);
//                    });
//                }
//            } else if (column.type === 'many2one') {
//                value = record.get(column.id);
//
//                if (typeof value === 'number' || value instanceof Number) {
//
//                    new data.DataSet(this.view, column.relation)
//                        .name_get([value]).done(function (names) {
//                        if (!names.length) {
//                            return;
//                        }
//                        record.set(column.id, names[0]);
//                    });
//                }
//            } else if (column.type === 'many2many') {
//                value = record.get(column.id);
//                if (value instanceof Array && !_.isEmpty(value)
//                    && !record.get(column.id + '__display')) {
//                    var ids;
//                    if (value[0] instanceof Array) {
//                        _.each(value, function (command) {
//                            switch (command[0]) {
//                                case 4:
//                                    ids.push(command[1]);
//                                    break;
//                                case 5:
//                                    ids = [];
//                                    break;
//                                case 6:
//                                    ids = command[2];
//                                    break;
//                                default:
//                                    throw new Error(_.str.sprintf(_t("Unknown m2m command %s"), command[0]));
//                            }
//                        });
//                    } else {
//                        ids = value;
//                    }
//                    new Model(column.relation)
//                        .call('name_get', [ids, this.dataset.get_context()]).done(function (names) {
//
//                        record.set(column.id + '__display',
//                            _(names).pluck(1).join(', '));
//                        record.set(column.id, ids);
//                    });
//                    record.set(column.id, false);
//                }
//            }
//            return column.format(record.toForm().data, {
//                model: this.dataset.model,
//                id: record.get('id')
//            });
//        },
//    });
    datepicker.DateWidget.include({
		start: function() {
	        var def = new $.Deferred();
	        this.$input = this.$el.find('input.o_datepicker_input');
	        this.$input_picker = this.$el.find('input.oe_datepicker_container');
	        this.$input_nepali = this.$el.find('input.oe_nepali');
	        $(this.$input_nepali).val('');

        	this.$input.datetimepicker(this.options);
        	this.picker = this.$input.data('DateTimePicker');
        	this.set_readonly(false);
        	this.set_value(false);

	        this.$input = this.$el.find('input.oe_simple_date');

	        var self = this;
	        function convert_to_nepali(date) {
	            console.log("change_datetime")
	            if (date.length == 0) {
	                return false
	            }
	            var jd = $.calendars.instance('nepali').toJD(parseInt(date[0].year()),parseInt(date[0].month()),parseInt(date[0].day()));
	            var date = $.calendars.instance('gregorian').fromJD(jd);

	            var old_date = self.$el.find('input.oe_simple_date').val();
	            var hour = 00;
	            var minute = 00;
	            var second = 00;
	            if(old_date && (typeof old_date === "string")){
			            var old_time = old_date.split(' ');
			            if(old_time.length > 1 && old_time[1]){
			            	var time = old_time[1].split(':')
				            if (time.length > 2){
					            hour = time[0];
					            minute = time[1];
					            second = time[2];
				            }
			            }
	            }
	            var date_value = new Date(parseInt(date.year()),parseInt(date.month())-1,parseInt(date.day()),parseInt(hour),parseInt(minute),parseInt(second));
	            self.$el.find('input.oe_simple_date').val(self.formatClient(date_value, self.type_of_date));
	            self.change_datetime();
	        }
            $(this.$input_nepali).calendarsPicker({
                calendar: $.calendars.instance('nepali'),
                dateFormat: 'M d, yyyy',
                onSelect: convert_to_nepali,
            })
	    },
	    formatClient: function (value, type) {
	        var l10n = _t.database.parameters;
	        var date_format = time.strftime_to_moment_format((type === 'datetime')? (l10n.date_format + ' ' + l10n.time_format) : l10n.date_format)
	        return moment(value).format(date_format);
	    },
        convert_gregorian_nepali: function (text) {
            if (text) {
                text = moment(text, date_format)._i;
                if (text.indexOf('-') != -1) {
                    text_split = text.split('-');
                    year = parseInt(text_split[0]);
                    month = parseInt(text_split[1]);
                    day = parseInt(text_split[2]);
                    calendar = $.calendars.instance('gregorian');
                    calendar1 = $.calendars.instance('nepali');
                    var jd = calendar.toJD(year, month, day);
                    var date = calendar1.fromJD(jd);
                }
                if (text.indexOf('/') != -1) {
                    text_split = text.split('/');
                    year = parseInt(text_split[2]);
                    month = parseInt(text_split[0]);
                    day = parseInt(text_split[1]);
                    calendar = $.calendars.instance('gregorian');
                    calendar1 = $.calendars.instance('nepali');
                    var jd = calendar.toJD(year, month, day);
                    var date = calendar1.fromJD(jd);
                }
                m = (date.month() >= 10 ? date.month() : "0" + date.month());
                d = (date.day() >= 10 ? date.day() : "0" + date.day());

                $(this.$input_nepali).val(calendar1.formatDate('M d, yyyy', date));

                $(".o_datepicker input:last").click(function (event) {
                    event.stopPropagation();
                    $('.oe_nepali').calendarsPicker({
                        calendar: $.calendars.instance('nepali', lang),
                        dateFormat: 'M d, yyyy',
                        onSelect: true,
                    });
                });
                $(this.$input_nepali).calendarsPicker({
                    calendar: $.calendars.instance('nepali', lang),
                    dateFormat: 'M d, yyyy',
                    onSelect: true,
                });
            }
        },

        set_value: function (value) {
            this._super(value);
            $(this.$input_nepali).val('')
            this.convert_gregorian_nepali(value);
            this.$input.val(value ? this.format_client(value) : '');
        },
        set_value_from_ui: function () {
            //this._super();
            var value = this.$input.val() || false;
            this.value = this.parse_client(value);
            this.set_value(this.value);
            this.convert_gregorian_nepali(this.value);
        },
        set_readonly: function (readonly) {
            this._super(readonly);
            this.$input_nepali.prop('readonly', this.readonly);
        },
		change_datetime: function(e) {
	        if(this.is_valid()) {
		        this.set_value_from_ui();
		        this.trigger("datetime_changed");

		        // Prevent to stop auto close filter popup to reopen
		        var $el = this.$el;
		        setTimeout(function(){
		            if ($el.closest('.o_filters_menu').length){
		                $el.closest('.o_filters_menu').parent().addClass('open');
		                $el.closest('.o_filters_menu').addClass('open');
		                if($el.closest('.o_filters_menu').find('.o_add_filter').length){
		                	if($el.closest('.o_filters_menu').find('.o_add_filter').hasClass('o_closed_menu')){
		                		$el.closest('.o_filters_menu').find('.o_add_filter').trigger('click');
		                	}
		                }
		            }
		        }, 400);
			}
	    },
    });

    FieldDate.include({
	    render_value: function () {
	        if (this.get("effective_readonly")) {
	            this.$el.text(formats.format_value(this.get('value'), this, ''));

	            var date_value = $(this.$el).text();
	            var nepali_date = this.convert_gregorian_nepali(date_value)
	            this.$el.append("<div><span class='oe_nepali'>"+nepali_date+"</span></div>");
	        } else {
	            this.datewidget.set_value(this.get('value'));
	        }
	    },
	    convert_gregorian_nepali: function(text) {
	        if (text) {
	            var cal_greg = $.calendars.instance('gregorian');
	            var cal_nepali = $.calendars.instance('nepali');
	            if (text.indexOf('-')!= -1){
	                var text_split = text.split('-');
	                var year = parseInt(text_split[0]);
	                var month = parseInt(text_split[1]);
	                var day = parseInt(text_split[2]);

	                var jd = cal_greg.toJD(year,month,day);
	                var date = cal_nepali.fromJD(jd);
	                var m = (date.month() >=10 ? date.month():"0"+date.month());
	                var d = (date.day() >=10 ? date.day():"0"+date.day());
	                return cal_nepali.formatDate('M d, yyyy', date);
	            }

	            if(text.indexOf('/')!= -1){
	                var text_split = text.split('/');
	                var year = parseInt(text_split[2]);
	                var month = parseInt(text_split[0]);
	                var day = parseInt(text_split[1]);

	                var jd = cal_greg.toJD(year,month,day);
	                var date = cal_nepali.fromJD(jd);
	                var m = (date.month() >=10 ? date.month():"0"+date.month());
	                var d = (date.day() >=10 ? date.day():"0"+date.day());
	                return cal_nepali.formatDate('M d, yyyy', date);
	            }
	        }
	    },
	});

});