$(function() {
  $('.ui.dropdown').dropdown();
  $('input').popup({on: 'focus'});
  $('.message .close').on('click', function() {
    $(this).closest('.message').fadeOut('slow');
  });
})