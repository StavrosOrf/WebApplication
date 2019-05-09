var friends = get_friends();

String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

var profile_card_html = `<div class="card">
  <img src="some_image.jpg" alt=" " style="width:100%">
  <p class="title" style="color: grey;font-size: 30px;">{0}</p>
	<a href={1}><i class="fa fa-envelope"></i></a> 
	{2}
  <p><button class="galleries-btn" onClick="render_galleries();">Galleries</button></p>
</div>`;

var profile_section_html = `<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.2/css/all.css" integrity="sha384-oS3vJWv+0UjzBfQzYUhtDYW+Pj2yciDJxpsK1OYPAYjqT085Qq/1cq5FLXAZQ7Ay" crossorigin="anonymous">
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

{0}
</body>
</html>`;

function get_my_email(){
	my_email = "ckarageorgkaneen@gmail.com";//sessionStorage.getItem('my_email');
	return my_email;
}

function get_user_name(email){
	// Ajax call
	name = "Christos KK";
	return name;
}

function get_user(email){
	name = get_user_name(email);
	return {name: name, email: email};
}

function make_profile_card_html(user){
	var is_user_added = true;
	var name = user.name;
	var email = user.email;
	var mail_to_email = "mailto:" + email;
	var friend_btn_html = is_user_added?
		'<a href="#"><i class="fa fa-user-minus"></i></a>':
		'<a href="#"><i class="fa fa-user-plus"></i></a>';
	return profile_card_html.format(name, mail_to_email, friend_btn_html)
}

function render_profile_UI(user){
	fd_profile_card_html = make_profile_card_html(user);
	return profile_section_html.format(fd_profile_card_html);
}

function get_galleries(){
	// Ajax call
	return "";
}

function make_pretty_galleries_UI(galleries){
	return "Galleries";
}

function render_galleries(){
	var galleries = get_galleries();
  	var galleries_html = make_pretty_galleries_UI(galleries);
	$("#content").html(galleries_html)
}

function get_friends(){
	// Ajax call
	friends = [
		{
			name: "Kostas A",
			email: "kostas@a.com"
		},

		{
			name: "Elena B",
			email: "elena@b.com"
		},

		{
			name: "Kapoios Allos",
			email: "kapoios@allos.com"
		}
	];

	return friends;
}

function render_friends_UI(friends){
	friend_profiles_html = '';
	friends.forEach(function (friend) {
    	friend_profiles_html += make_profile_card_html(friend);
	});

	return profile_section_html.format(friend_profiles_html);
}

$(document).ready(function(){
  $(".menu-button").click(function(){
    $(".menu-bar").toggleClass( "open" );
})

$(".profile-button").click(function(){
	var my_email = get_my_email();
	var my_user = get_user(my_email);
  	var my_profile_UI_html = render_profile_UI(my_user);
	$("#content").html(my_profile_UI_html);
})
  
$(".galleries-button").click(function(){
	render_galleries();
})

$(".friends-button").click(function(){ 
	var friends_UI_html = render_friends_UI(friends);
	$("#content").html(friends_UI_html);
})
  
})
