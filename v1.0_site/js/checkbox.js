$(function() {
  var chk = $('#check');
  var btn = $('#_check');

  chk.on('change', function() {
    btn.prop("disabled", !this.checked);//true: disabled, false: enabled
  }).trigger('change'); //page load trigger event
})
