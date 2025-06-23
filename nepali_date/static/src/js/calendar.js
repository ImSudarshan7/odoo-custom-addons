odoo.define('nepali_date.config', function(require) {
    "use strict"; 
    var rpc = require('web.rpc')
    var date_mode
    var date_format
    var report_date_mode

    var mode = rpc.query({
              model: 'ir.config_parameter',
              method: 'get_param',
              args: ['nepali_date.default_datepicker']
          }).then(function (res) {
              date_mode = res;
          });
 
    console.log('Prajwal')
    var format = rpc.query({
              model: 'ir.config_parameter',
              method: 'get_param',
              args: ['nepali_date.date_format']
          }).then(function (res) {
              date_format = res;
              console.log(date_format)
          });

    var date_mode = rpc.query({
              model: 'ir.config_parameter',
              method: 'get_param',
              args: ['nepali_date.report.date_mode']
          }).then(function (res) {
              report_date_mode = res;
          });

    var config = {
      'date_mode': date_mode,
      'date_format': date_format,
      'report_date_mode': report_date_mode,
    };

    return config;
});