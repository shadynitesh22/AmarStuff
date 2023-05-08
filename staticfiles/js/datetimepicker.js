$(function () {
  $("#date").datepicker();
});

$(function () {
  $("#time").timepicker();
});

$('.datepicker').datepicker({
    format: 'mm/dd/yyyy',
    startDate: '-3d'
});