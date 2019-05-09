var email = "ckarageorgkaneen@gmail.com";//sessionStorage.getItem('my_email');

function get_user_name(){
	// Ajax call
	name = "";
	return name;
}

function make_pretty_profile_UI(name){
	var mail_to_email = "mailto:" + email;
	
	return `<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 200px;
  margin: auto;
  text-align: center;
  font-family: arial;
}

.galleries-btn {
  border: none;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: #267fdd;
  text-align: center;
  cursor: pointer;
  width: 100%;
  font-size: 18px;
}

.fa {
  text-decoration: none;
  font-size: 22px;
  color: #267fdd;
}

.galleries-btn:hover, .fa:hover {
  opacity: 0.7;
}
</style>
</head>
<body>

<div class="card">
  <img src="some_image.jpg" alt="Profile" style="width:100%">
  <p class="title" style="color: grey;font-size: 30px;">${name}</p>
  <div>
	<a href=${mail_to_email}><i class="fa fa-envelope"></i></a> 
    <a href="#"><i class="fa fa-twitter"></i></a>  
    <a href="#"><i class="fa fa-linkedin"></i></a>   
    <a href="#"><i class="fa fa-facebook"></i></a> 
    <a href="#"><i class="fa fa-user-plus"></i></a> 
  </div>
  <p><button class="galleries-btn">Galleries</button></p>
</div>

</body>
</html>`;

}

function get_galleries(){
	// Ajax call
	return "";
}

function make_pretty_galleries_UI(galleries){
	return "Galleries";
}

function get_friends(){
	// Ajax call
}

function make_pretty_friends_UI(friends){
	return "Friends";
}

$(document).ready(function(){
  $(".menu-button").click(function(){
    $(".menu-bar").toggleClass( "open" );
})

$(".profile-button").click(function(){
	var name = "Christos KK";//get_user_name();
  	var profile_html = make_pretty_profile_UI(name);
	$("#content").html(profile_html);
})
  
$(".galleries-button").click(function(){
	var galleries = get_galleries();
  	var galleries_html = make_pretty_galleries_UI(galleries);
	$("#content").html(galleries_html)
})

$(".friends-button").click(function(){
    var friends = get_friends();
	var friends_html = make_pretty_friends_UI(friends);
	$("#content").html(friends_html)
})
  
})
