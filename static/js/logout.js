

function login(){
			
    if (getCookie('user') != ''){
        html = `

        <a href="#" class="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true"
                         aria-expanded="false">Account</a>
                        <ul class="dropdown-menu">
                            <li class="nav-item"><a class="nav-link" href="http://localhost:5000/profile">Profile</a></li>
                            <li class="nav-item"><div onclick=logout()><a class="nav-link" href="http://localhost:5000/">Logout</a></div></li>
                            
                        </ul>
        `
        
        $('#login').html(html)

    }
}

function logout(){
    data = getCookie('user')
    setCookie('user', data, -1)
}