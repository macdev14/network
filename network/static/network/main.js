

function load_posts()
{
    let post = document.getElementById('posts');
    post.style.display = 'block';
    fetch('api/post/all').then((response)=>response.json()).then( (object)=>{
        document.getElementById('posts').innerHTML = '';
        object.map((value, index)=>{
            console.log(value);
            
            return document.getElementById('posts').innerHTML+=`
<div class="row">
    <div class="col-xl-12">            
            <div class="card">
                <div class="card-body">
                    <div class="card-title">
                        <h4>${value.title}</h4>
                      </div>
                      <p>${value.description}</p>
                      <p>Posted by: <span onclick=load_profile(${value.user.id})>${value.user.username}</span></p>

                        ${ (value.edit)? 

                      `<button class="btn btn-primary" onclick=edit_post(${value.id}) style="float:center">
                       Edit
                    </button>
                    <br/>
                    <button class="btn btn-danger" onclick=delete_post(${value.id}) style="float:right">
                        Delete
                     </button>
                     <br/>` : ''
                        
                    }   
                     ${

                        (value.liked) ? `
                        <div class="unlike" onclick="unlike(${value.id})"> 
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#dc143c" class="bi bi-heart-fill" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                          </svg>
                        </div>` : `<div class="like" onclick="like(${value.id})"> 
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                      </svg>
                    </div>`
                     }
                    
                    
                </div>
            </div>
    </div>
</div>`

        })

    
}
)

}



function load_following_posts()
{
    let post = document.getElementById('posts');
    post.style.display = 'block';
    fetch('api/post/following').then((response)=>response.json()).then( (object)=>{
        document.getElementById('posts').innerHTML = '';
        object.map((value, index)=>{
            console.log(value);
            
            return document.getElementById('posts').innerHTML+=`
<div class="row">
    <div class="col-xl-12">            
            <div class="card">
                <div class="card-body">
                    <div class="card-title">
                        <h4>${value.title}</h4>
                      </div>
                      <p>${value.description}</p>
                      <p>Posted by: <span onclick=load_profile(${value.user.id})>${value.user.username}</span></p>

                        ${ (value.edit)? 

                      `<button class="btn btn-primary" onclick=edit_post(${value.id}) style="float:center">
                       Edit
                    </button>
                    <br/>
                    <button class="btn btn-danger" onclick=delete_post(${value.id}) style="float:right">
                        Delete
                     </button>
                     <br/>` : ''
                        
                    }
                   
                     ${

                        (value.liked) ? `
                        <div class="unlike" onclick="unlike(${value.id})"> 
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#dc143c" class="bi bi-heart-fill" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                          </svg>
                        </div>` : `<div class="like" onclick="like(${value.id})"> 
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                      </svg>
                    </div>`
                     }
                    
                    
                </div>
            </div>
    </div>
</div>`

        })

    
}
)

}



function load_profile(id)
{
    fetch('api/post/profile/'+id).then((response)=>response.json()).then( (object)=>{
        document.getElementById('post-form').style.display = 'none';
        document.getElementById('posts').innerHTML = '';
        console.log(object)
        object['data'].map((value, index)=>{
            console.log(value);
            
            return document.getElementById('posts').innerHTML+=`
<div class="row">
    <div class="col-xl-12">            
            <div class="card">
                <div class="card-body">
                    <div class="card-title">
                        <h4>${value.title}</h4>
                      </div>
                      <p>${value.description}</p>
                      <p>Posted by: <span onclick=load_profile(${value.user.id})>${value.user.username}</span></p>

                        ${ (value.edit)? 

                      `<button class="btn btn-primary" onclick=edit_post(${value.id}) style="float:center">
                       Edit
                    </button>
                    <br/>
                    <button class="btn btn-danger" onclick=delete_post(${value.id}) style="float:right">
                        Delete
                     </button>
                     <br/>` : ''
                        
                    }
                   
                     ${

                        (value.liked) ? `
                        <div class="unlike" onclick="unlike(${value.id})"> 
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#dc143c" class="bi bi-heart-fill" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                          </svg>
                        </div>` : `<div class="like" onclick="like(${value.id})"> 
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                      </svg>
                    </div>`
                     }
                    
                    
                </div>
            </div>
    </div>
</div>`

        })

    
}
)

}









function delete_post(id){
  

    fetch('api/post/delete', {

        method: 'POST',
        body: JSON.stringify({
            id:id
        }
        )
    }
    ).then(response=>response.json()).then((response)=>{
        load_posts()
    }).catch(e=>console.log(e))




}

function edit_post(id){
    let post = document.getElementById('posts');
    post.style.display = 'none';
    let postform = document.getElementById('post-form');
    postform.style.display = 'block';

    let following_post = document.getElementsByClassName('following-post')

    let body_post = document.getElementById('postbody')
    let title_post = document.getElementById('posttitle')
    let submitpost = document.getElementById('submitpost')
    submitpost.value="Edit"

    fetch('api/post/update/'+id).then(response=>response.json()).then((response)=>{
        body_post.value=response.description;
        title_post.value=response.title;
       

    }).catch(e=>console.log(e))


    submitpost.onclick = () => {
    return fetch('api/post/update/'+id,{
        method: 'PUT',
        body: JSON.stringify({
            title:title_post.value,
            description: body_post.value
        })
    }).then((response)=>response.json()).then(
        (r)=>{console.log(r);
            return load_posts()}).catch(
                (e)=>{return console.log(e); 
                    })
    }


}


function create_post(){
    let post = document.getElementsByClassName('post');

    let following_post = document.getElementsByClassName('following-post')

    let body_post = document.getElementById('postbody')
    let title_post = document.getElementById('posttitle')
    let submitpost = document.getElementById('submitpost')

    return fetch('api/post/add',{
        method: 'POST',
        body: JSON.stringify({
            title:title_post.value,
            description: body_post.value
        })
    })
    .then((response)=>response.json()).then(
        (r)=>{console.log(r);
            body_post.value='';
            title_post.value='';
            return load_posts()})
            .catch(
                (e)=>{return console.log(e); 
                    })
    // document.querySelector('#post-form').onsubmit  = (event)=>{event.preventDefault();return sendMail()};
}


function like(id){
    

    return fetch('api/post/update/'+id,{
        method: 'PUT',
        body: JSON.stringify({
            like: true
        })
    })
    .then((response)=>response.json()).then((r)=>{console.log(r); return load_posts();} ).catch((e)=>alert(e.error))
    // document.querySelector('#post-form').onsubmit  = (event)=>{event.preventDefault();return sendMail()};
}


function unlike(id){
    

    return fetch('api/post/update/'+id,{
        method: 'PUT',
        body: JSON.stringify({
            unlike: true
        })
    })
    .then((response)=>response.json()).then((res)=>{
        // alert(res.message);
        console.log(res); 
        return load_posts()
    }).catch((e)=>{console.log(e);alert(e);})
    // document.querySelector('#post-form').onsubmit  = (event)=>{event.preventDefault();return sendMail()};
    
}




document.addEventListener('DOMContentLoaded', (e)=> load_posts(e))



