




function new_group_pop_up_or_off()
   {
       const doc1=document.getElementById('new_group_users');
       const method=(doc1.className==='' ||doc1.className==='users_list_popoff')?'on':'off';
       switch (method)
       {

           case 'on':{doc1.style.display='block'; doc1.className='users_list_popup';}break;
           case 'off':{doc1.className='users_list_popoff';}break;
       }
   }

   function retrieve_groups(input)
   {

       if(input=='')
       {

           reset_groups()
           return;
       }
       $.get('http://127.0.0.1:8000/search_groups_users/'+input).then(res=>{

           console.log(res)
           for(const group_div of groups_lists.querySelectorAll('div'))
           {
               group_div.style.display=group_div.innerText.includes(input)?'block':'none';
           }
          for(const gr of res.result)
          {
              if(temp_groups.includes(gr[1])){continue;}
              const div = document.createElement('div');

                  div.innerText = gr[1];
                  div.setAttribute('data-type','temp');
                  const button = document.createElement('button');
                      button.className = 'join_group';
                  if(gr[0]=='group') {

                      button.addEventListener('click', function () {
                          join_group(gr[1],gr[2],'many')
                      });
                      // div.appendChild(button);
                      button.innerText = 'join_group';
                  }
                  else {
                      button.innerText = 'message';
                      button.addEventListener('click', function () {
                          create_new_group(form=null,user_name=gr[1]);
                      });

                  }
                  div.appendChild(button)
                      groups_lists.appendChild(div)
              temp_groups.push(gr[1]);
          }
       })
   }

   function reset_groups()
   {
      const groups=groups_lists.querySelectorAll('div[data-type=temp]');
      for(const gr of groups)
      {
          console.log('group is',gr)
          gr.remove();
          temp_groups.pop()
      }

      for(const group_div of groups_lists.querySelectorAll('div'))
           {
               group_div.style.display='block';
           }
   }

   function join_group(name,id,type)
   {

    const ajx={type:'POST',
        url:'http://127.0.0.1:8000/join/'+name,headers:{'X-csrftoken':csrf_token},
        contentType:false,processData: false};
       $.ajax(ajx).then(res=>{

           if(res.status=='succeed')
           {

               const group_name_div=document.createElement('div');
               group_name_div.addEventListener('click',function () {change_selected_message_group(id)})
               group_name_div.innerText=name;const button=document.createElement('button'); button.className='leave_group';
               button.innerText='Leave'; group_name_div.appendChild(button);
               button.addEventListener('click',function (){open_close_warning(true,`do you want to leave ${name} ?`);warning_form.querySelector('button#action')
                   .onclick=function () {
                   leave_group(id,type)
               }})

               add_socket(name,id);
               const group_messages_container=document.createElement('div');  group_messages_container.className='chat_messages';
               group_messages_container.id=`tab${id}`;
               tabs_container.appendChild(group_messages_container);
               groups_lists.appendChild(group_name_div)
               for(const message of res.messages)
               {
                   if(message[4]=='message') {
                       add_message(id, message[0], message[1], message[3], message[2],'old',message[4],message[5],message[6])
                   }
                   else
                   {
                        const el=`<div style="width: fit-content;height: fit-content; align-self: center;z-index: 1" >
            <p style="font-size:1vw;background-color:dodgerblue;float: right;margin-right: 50%;box-shadow: 3px 3px 3px dodgerblue">
                ${message[0]}
                </p>
        </div>`;
                        console.log('hi there')
              group_messages_container.innerHTML+=el;
                   }
               }

               setTimeout(()=>{
                  chat_sockets[id].send(JSON.stringify({'my_dict':{'type':'announce_joining','group_id':id,'destination':'self'}}))
               },500);
               reset_groups()



           }
       })

   }

   function move_message_header(id,button)
   {
       console.log(message_header,id)
       const par=button.parentElement;

       message_header[id]+=5;
       $.get(`http://127.0.0.1:8000/get_group_messages/${id}/${message_header[id]}`).then(res=>{

           if(res.status ==200) {

               for (const message of res.messages)
               {
                  add_message(id,message[0],message[1],message[2],message[3],'old',message[4],message[5],message[6])

               }
               par.appendChild(button)

                   }

       })
   }

function mark_as_seen(element)
    {
  const mark_message_form=new FormData();
    const mark_message_ajax={
    type:'post',processData:false,url:'http://127.0.0.1:8000/mark_as_seen',
    contentType:false,headers:{'X-csrftoken':csrf_token},data:mark_message_form
}
          mark_message_form.append('m_id',element.id);
          mark_message_form.append('group_id',element.getAttribute('data-parent'))
        $.ajax(mark_message_ajax).then(res=>{
            if(res.status=='succeed')
            {
               element.className='';
               observer.unobserve(element);
                pv_socket.send(JSON.stringify({'function_type':'saw_message','m_id':element.id,'g_id':element.getAttribute('data-parent'),
                        'target':res.username}))
               const gr_name= groups_lists.querySelector(`#group${element.id}`).innerText;
                let name='';
                const numbs='0123456789';
                for(const char of gr_name)
                {
                    if(numbs.includes(char)){break;}
                    name+=char;
                }
                let number=parseInt(gr_name.replace(name,''));
                groups_lists.querySelector(`#group${element.id}`).innerText=`${name} ${number.toString()}`;

            }

        })
        mark_message_form.delete('m_id');
           mark_message_form.delete('group_id');

    }

function change_selected_message_group(id)
        {
            console.log('changed selected group was called for',id)
            if(cur_tab)
            {
                cur_users_list.style.opacity='0%';
                cur_tab.style.opacity='0%';

                cur_group.style.backgroundColor='white';

                cur_tab.style.zIndex='0';
                for(const el of cur_tab.querySelectorAll('.message_div'))
                {
                    observer.unobserve(el);
                }
            }

                cur_tab = tabs_container.querySelector(`#tab${id}`);
                cur_group = groups_lists.querySelector(`#group${id}`);
                cur_users_list = users_lists.querySelector(`#list${id}`);
                selected_socket_index = id;
                     for(const el of cur_tab.querySelectorAll('.message_div'))
                {
                    observer.observe(el);
                    console.log(el);
                }

                selected_socket = chat_sockets[id];
                     cur_tab.style.zIndex='2';
           cur_tab.style.opacity='100%';
            cur_users_list.style.opacity='100%';
            cur_group.style.backgroundColor='lightgray';

        }



        function add_message(id,message,username,url,file_url,old_new='old',is_seen,observe,message_id)
        {

        const doc=tabs_container.querySelector(`#tab${id}`).querySelector(`div.${old_new}_messages`);

       const file_url_to_add=file_url!='na'?`<br><a onclick="open_pop_up('${file_url}','blank');" > File </a>`:``;

       const is_mine=username===my_username;
       const div=document.createElement('div'); div.style.cssText=`width: fit-content;height: fit-content;
        ${is_mine?'align-self:flex-end':'align-self:flex-start'}`
       const img=document.createElement('img'); img.style.cssText=`height: 45px;width: 45px;object-fit: cover;border-radius: 50%;
            ${is_mine?'float:right': 'float:left'}`;
       img.src=`${url}`;
       const p=document.createElement('p'); p.style.cssText=`font-size:1vw;background-color:dodgerblue;`
             +`box-shadow: 3px 3px 3px dodgerblue;${is_mine?'float:right;margin-right: 10px;':'float:left;margin-left:10px;'};position:relative`;

       ;
       p.innerHTML=`${username} <br> ${message} <br> ${file_url_to_add} <br>`;
          if(is_mine)
        {
            const img=document.createElement('img');
            img.className='seen_status';
            img.style.cssText='width: 18px;height:18px;position: absolute;right: 0;bottom: 0';
                img.src = `/static/imgs/${is_seen?'check_blue.png':'check_trans.png'}`;
                const delete_message=document.createElement('img');
                delete_message.style.cssText='height:18px;width: 18px;position:absolute;top:-17%;right:-7%;z-index: 1';
                delete_message.onclick=function (){
                send_delete_message(id,message_id,'new')
                };
                p.appendChild(delete_message);

            p.appendChild(img);
        }
        else
        {
            if(observe) {
                div.className = 'message_div';

                div.setAttribute('data-parent', id);

                 observer.observe(div);
            }
        }
        div.id=message_id;
       div.appendChild(img);
       div.appendChild(p);
          doc.appendChild(div);

        }

function filter_users(username)
        {

            const box=document.getElementsByClassName('users_box')[0];
            box.innerHTML='';
            if(username===''){return;}
            box.innerHTML='';
            $.get(`http://127.0.0.1:8000/users/filter_users/${username}`).then(res=>{
             for(const usname of res.users)
             {
                 const my_div=document.createElement('div'); my_div.className="username"; my_div.onmouseleave=function (){hover_element(my_div
             ,'off','username');};
                 my_div.onmouseenter=function (){hover_element(my_div,'on','username');};
                 my_div.innerText=usname;
                  my_div.onclick=function (){console.log(this.innerText); add_or_remove_user(usname,'add');};
                  box.appendChild(my_div);

             }
            });
        }


function add_or_remove_user(username,add_or_remove)
        {
            const doc1=document.getElementsByClassName("selected_usernames")[0];
            switch (add_or_remove)
            {
                case 'add':
                {
                    if(doc1.querySelector(`#${username}`)!=undefined){return;}
                 const element=document.createElement('div'); element.style.cssText="height: 60%;width:fit-content;position: relative"; element.id=username;
                 element.innerText=username;
                 const img=document.createElement('img'); img.style.cssText="height: 10px;width: 10px;position: absolute;top:-22%;left:-10%";

                 img.src="/static/imgs/rejected.png";
                 element.appendChild(img);
                 doc1.appendChild(element);
                 img.onclick=function () {add_or_remove_user(username,'remove');}
                }break;
                case 'remove':
                {
                   doc1.querySelector(`#${username}`).remove();
                }break;
            }
        }

        function activate_the_first_group()
        {
        var tabs=document.getElementsByClassName('chat_messages');
        var lists=document.getElementsByClassName("users_list");
        console.log(lists)
        for(let i=0;i<tabs.length;i++){
           tabs[i].style.opacity=i==0?'100%':'0%';
            lists[i].style.opacity=i==0?'100%':'0%';
        }
        }