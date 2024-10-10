
 const side_bar=document.getElementById('side_bar');


function open_close_sidebar(to_do)
       {
            const side_bar_is_open=to_do=='open';
            if(side_bar_is_open)
            {
                side_bar.style.width='0vw';
            }
            else
            {
                   side_bar.style.width='10vw';
            }
       }

function open_close_delete_form(element)
    {
        console.log('hi')
        element.querySelector('form').style.display=element.querySelector('form').style.display==='block'?'none':'block';
    }
    function ask_for_user_deletion(button)
    {
          button.style.opacity='50%'; button.style.zIndex='-55';
        const ajax={type:'POST',url:'http://127.0.0.1:8000/users/ask_for_user_deletion',headers:{'X-csrftoken':csrf_token},contentType:false,
        processData:false
        }
        $.ajax(ajax).then(res=>{

            open_close_alert(true,res.status=='succeed'?'Email Sent Successfully':'Failed to send the email');
            button.style.opacity='100%'; button.style.zIndex='1';

        }).catch(res=>{
            open_close_alert(true,'Failed to send the email');
            button.style.opacity='100%'; button.style.zIndex='1';
        })

    }
    function delete_user(frm)
    {
        const frm_data=new FormData(frm);
        const ajax={type:'POST',url:'http://127.0.0.1:8000/users/delete_user',data:frm_data,headers:{'X-csrftoken':csrf_token},contentType:false,
        processData:false}
        $.ajax(ajax).then(res=>{
           if(res.status=='succeed')
           {
               window.open('http://127.0.0.1:8000/users/show-chat-groups' )
           }
           else
           {
               open_close_alert(true,'user not found')
           }
        })
    }