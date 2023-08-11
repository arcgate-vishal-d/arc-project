$('.header-toggle').click(function(){
  $(this).toggleClass('one');
  var chkClass = $(this).hasClass('one');

  $('.navbar').slideToggle('fast');
  // $('.navbar').fadeToggle('fast');
    
  if(chkClass == true){
    $('.container-fluid.mt80').animate({'margin-top':'0'},1000);    
  }

  else{
    $('.container-fluid.mt80').animate({'margin-top':'30'},1000);    
  }
});
