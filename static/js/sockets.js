



function add_socket(group_title,group_id) {

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        +group_id
        + '/'
    );
    chatSocket.onopen = function (e) {
        console.log('Connected!');
    };

    chatSocket.onclose = function (e) {
        console.log('Disconnected!');
    };
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('recieved a socket message',data);
        const function_type = data.function;
        switch (function_type) {
            case 'add_message': {
                add_message(group_id, data.message, data.username, data.url, data.file_url,'new',false,'{{ user.username }}'!=data.username,
                data.message_id);
            }
                break;
            case 'delete_message': {
                delete_message(data.group_id, data.message_id,data.old_new);
            }
                break;
            case 'announce':
            {
                const doc=document.getElementById('tab'+group_id);
                const el=`<div style="width: fit-content;height: fit-content; align-self: center;z-index: 1" >
            <p style="font-size:1vw;background-color:dodgerblue;float: right;margin-right: 50%;box-shadow: 3px 3px 3px dodgerblue">
                ${data.message}
                </p>
        </div>`;
              doc.innerHTML+=el;
            }break;
        }


    }
    console.log(group_id);
    chat_sockets[group_id] = chatSocket;
    console.log(chat_sockets);



}
function start_private_socket()
{
const pv_socket=new WebSocket(
        'ws://'
            + window.location.host
            + '/ws/private_consumer/'

    );
    pv_socket.onmessage=function (e){
        const data=JSON.parse(e.data);
        console.log(data);
        switch (data.function_type)
        {
            case 'message':{}break;
            case 'add_to_group':{
                console.log(data)
                const list=groups_lists;
                const div=document.createElement('div'); div.innerText=data.group_name;
                console.log(data);
                div.onmouseenter=function (){hover_element(div,'on','');}
                div.onmouseleave=function (){hover_element(div,'off','');}
                div.onclick=function (){change_selected_message_group(data.group_id);}

                add_socket(data.group_name,data.group_id);
                const messages_panel=document.createElement('div');
                messages_panel.id=`tab${data.group_id}`;
                 messages_panel.className='chat_messages';
                document.getElementById('message_groups_tabs').appendChild(messages_panel);
                const button=document.createElement('button'); button.className='leave_group';
                if(data.group_type =='many'){
                    button.innerText='leave_group';button.onclick=function () {
                        open_close_warning(true, `do you want to leave ${data.group_name}`);
                        war_form_action_button.addEventListener('click', function () {
                            leave_group(data.group_id, data.group_type)
                        });
                    }}

                else {button.onclick=function (){open_close_warning(true,`do you want to remove ${data.group_name} chats?`);
                    war_form_action_button.onclick=function (){leave_group(data.group_id,data.group_type)}
                   } ;button.innerText='delete_chat'}
                div.appendChild(button);
                 list.appendChild(div);
            };
            case 'recieve_message':
            {
                console.log('recived a message');
                recieve_data_from_user(data);
            }break;
            case 'alert':
            {
                open_close_alert(true,data.message)
            }break;
            case 'change_message_status':
            {
                console.log(tabs_container.querySelector(`#tab${data.data.g_id}`));
             document.getElementById(data.data.m_id)
                 .querySelector('.seen_status').src='/static/imgs/check_blue.png';
            }break;


        }
    }
    }
     function send_message()
        {

var message_form=document.getElementById('message_form');
const form_data=new FormData(message_form);
form_data.append('group_id',selected_socket_index);
 $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/receive_messages',
            data: form_data,
            headers: {
                'X-CSRFToken': csrf_token
            },
            processData: false,
            contentType: false,
            success: function(response) {

            },
            error: function(error) {
                console.error('Error sending message:', error);
            }
        }).then(
            result=>{
                 selected_socket.send(JSON.stringify({
        'my_dict': {'type':'chat_message','message':result.message,'username':'{{ user.username }}','avatar_url':'{{ user.get_avatar }}',
                     'file_url':result.file_url,'destination':'group','message_id':result.message_id}
    }));
            }
 );
}

function send_delete_message(group_id,message_id,old_new)
        {

        const dict={'type':'delete_message',
        'group_id':group_id
        ,'message_id':message_id,'destination':'group','old_new':old_new};
        selected_socket.send(JSON.stringify({
                'my_dict':dict

            }));
        }



function create_new_group(form=null,user_name=null)
        {
             const usernames_list = [];
             let group_name='';
             let group_type='';
            if(form) {
                const usernames = form.querySelector('.selected_usernames').querySelectorAll('div');

                group_name = form.querySelector('input#new_group_name').value;
                for (username of usernames) {
                    usernames_list.push(username.innerText);
                }
                group_type='many'

            }
            else
            {
                usernames_list.push(user_name);
                group_type='two';
                group_name=`{{ user.username }},${user_name}`;
            }
             pv_socket.send(JSON.stringify({
                    'function_type': 'create_group',
                    'usernames': usernames_list,
                    'group_name': group_name,
                    'group_type':group_type
                }));
        }


        function delete_message(id,message_id,old_new)
        {
        const doc=tabs_container.querySelector(`#tab${id}`);
        const par=doc.querySelector(`.${old_new}_messages`);
        for(const el of par.childNodes)
        {
        if(el.id===message_id)
        { el.remove();
        break;
        }
        }


        }

function leave_group(group_id,group_type)
        {
            chat_sockets[group_id].send(JSON.stringify({'my_dict':{'type':'leave_group','group_id':group_id,'destination':'self','group_type':group_type}}));
            open_close_warning(false)
           groups_lists.querySelector(`#group${group_id}`).remove()
             const group_tab=document.getElementById('tab'+group_id); group_tab.remove();
        }

        function send_message_to_user(form)
       {
           const target_user=form.querySelector('#target_user').value;
           pv_socket.send(JSON.stringify({'function_type':'talk_to_a_user','message':form.querySelector('#inp_message').value
           ,'target_username':target_user}))
       }
       function recieve_data_from_user(data) {

         console.log(`message is:  ${data}`);
       }