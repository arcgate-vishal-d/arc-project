
function anchorTagSubmit(ele) {
         var kk = document.getElementsByClassName('timeee');
         form_selected = ele.closest('form');
         var timeNext = new Date().getTime() 
         timePassed = ((timeNext - startQuestion)/1000)/60
         newDuration = (duration - timePassed)
         for(let i = 0 ; i <kk.length ; i++){
             document.getElementsByClassName('timeee')[i].value = newDuration;
         }
         form_selected.submit();
         }
