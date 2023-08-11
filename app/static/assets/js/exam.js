 // typing test time
 let endtimer = false
 function endtime(){
     var date = new Date().getTime()/1000;
     $("#endgame").val(date);
     endtimer = true
 }

 function nextTyping(){
     if(!endtimer) {
         endtime()
     updateDuration()
     }
 };

let start_timer = false
 function start_time(){
     var start = new Date().getTime()/1000;
     var next_btn = new Date().getTime()/1000
     $("#start").val(start);
     start_timer = true
 };
 
 $("#txtAnswer").click(function(){
      if (!start_timer) start_time();
 })
  
 // exam timer
 let duration = $("#hdnDuration").val()  // test total time

 // countdown timer working wuth duration save duration on next click
 function startTimer(duration, display) {
 var start = new Date().getTime(),
     diff,
     minutes,
     seconds;
 function timer() {
     // get the number of seconds that have elapsed since function called
     diff = duration - (((new Date().getTime() - start) / 1000) | 0);
     if (diff <= 0){  
     $.ajax({
         url: "/time_out",
         type: "GET",
         data:"response_data"
     })
         .done(function (response) {
         if (response){
             window.location='/thank_you'
         }
         });
     }

     hours = (diff % (60 * 60 * 24)) / (60 * 60) | 0;
     minutes = (diff % (60 * 60)) / ( 60) | 0;
     seconds = (diff % 60) | 0;

     hours = hours < 10 ? "0" + hours : hours;
     minutes = minutes < 10 ? "0" + minutes : minutes;
     seconds = seconds < 10 ? "0" + seconds : seconds;

     display.textContent = hours + ":" + minutes + ":" + seconds; 

     if (diff <= 0) {
         start = new Date().getTime() + 1000;
     }
 };

 timer();
 setInterval(timer, 1000);
 return diff
}
var startQuestion = new Date().getTime() 
window.onload = function () {
 var fiveMinutes = 60 * duration,
     display = document.querySelector('#timer');
 startTimer(fiveMinutes, display);
};

function updateDuration() {
 var timeNext = new Date().getTime() 
 timePassed = ((timeNext - startQuestion)/1000)/60
 newDuration = (duration - timePassed)
 $("#hdnDuration").val(newDuration);
}

// disable back button
history.pushState(null, document.title, location.href);
window.addEventListener('popstate', function (event)
{
history.pushState(null, document.title, location.href);
});

function confirm_save(){
    setTimeout(function() {
        button = $('#btnnext').removeAttr('disabled')
            submit.removeAttr('disabled');
        },3000);

}
