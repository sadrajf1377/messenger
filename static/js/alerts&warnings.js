



function open_close_warning(open,message=null)
   {
       //width: 30vw;height: 20vh;

  if(open)
  {
    warning_form.style.height='20vh';
      warning_form.style.width='30vw';
      warning_form.querySelector('p#message').innerText=message;

  }
  else
  {
    warning_form.style.height='0%'
      warning_form.style.width='0%'
  }
   }
   function open_close_alert(open,message=null)
   {

   alert_div.querySelector('div#message').innerText=open?message:'';
    alert_div.style.display=open?'block':'none';
   }
function open_pop_up(url,window_name)
       {
          window.open(url,window_name,'height=500,width=500,left=100,top=100');
       }