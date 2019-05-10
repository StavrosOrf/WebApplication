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

function get_galleries(email){
	// Ajax call
	images = [
		{
			name: "Cats"
		},
		{
			name: "Dogs"
		},
		{
			name: "Turtles"
		}
	];

	return images;
}

var my_email = get_my_email();	
var my_user = get_user(my_email);
var my_friends = get_friends();
var my_galleries = get_galleries();

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
  <p><button class="galleries-btn" onClick={3}>Galleries</button></p>
</div>`;

var gallery_html = `<div class="card">
  <img src="some_image.jpg" alt=" " style="width:100%">
  <div class="title" style="color: grey;font-size: 30px;">{0} <i class="fa fa-images"></i></div>	
  <p><button class="view_gallery_images-btn" onClick={1}>View</button></p>
</div>`;
   

var content_section_html = `<!DOCTYPE html>
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

.galleries-btn, .view_gallery_images-btn {
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

function make_profile_card_html(user){
	var is_user_added = true;
	var name = user.name;
	var email = user.email;
	var mail_to_email_str = "mailto:" + email;
	var friend_btn_html = is_user_added?
		'<a href="#"><i class="fa fa-user-minus"></i></a>':
		'<a href="#"><i class="fa fa-user-plus"></i></a>';
	var render_glrs_UI_func_str = "render_galleries_UI(" + email + ");"
	return profile_card_html.format(name, 
									mail_to_email_str, 
									friend_btn_html, 
									render_glrs_UI_func_str);
}

function render_my_profile_UI(){
	var my_profile_card_html = make_profile_card_html(my_user);
	return content_section_html.format(my_profile_card_html);
}

function make_image_html(image){
	var img_name = image.name;
	var img_link = image.link;
}

function make_gallery_images_UI(images){
	var glr_images_html = '';
	images.forEach(function(image){
		glr_images_html += make_image_html(image);
	})
	return glr_images_html;
}

function render_gallery_images_UI(glr_name, email){
	var images = get_images(glr_name, email);
	var gallery_images_html = make_gallery_images_UI(images);
	return content_section_html.format(gallery_images_html);
}

function make_gallery_html(gallery, email){
	var glr_name = gallery.name;
	var view_glr_imgs_func_str = "render_gallery_images_UI("+glr_name+","+email+");";
	return gallery_html.format(glr_name, view_glr_imgs_func_str);
}

function make_galleries_UI(galleries, email){
	var galleries_html = '';
	galleries.forEach(function(gallery){
		galleries_html += make_gallery_html(gallery, email);
	});
	return galleries_html;
}

function render_galleries_UI(email){
	var galleries = get_galleries(email);
  	var galleries_html = make_galleries_UI(galleries, email);
	return content_section_html.format(galleries_html);
}

function make_my_friends_UI(){
	var my_friends_html = '';
	my_friends.forEach(function(friend){
    	my_friends_html += make_profile_card_html(friend);
	});
	return my_friends_html;
}

function render_my_friends_UI(){
	var my_friends_html = make_my_friends_UI();
	return content_section_html.format(my_friends_html);
}

$(document).ready(function(){
  $(".menu-button").click(function(){
    $(".menu-bar").toggleClass( "open" );
})

$(".profile-button").click(function(){
	var my_profile_UI_html = render_my_profile_UI();
	$("#content").html(my_profile_UI_html);
})
  
$(".galleries-button").click(function(){
  	var my_galleries_UI_html = render_galleries_UI(my_email);
	$("#content").html(my_galleries_UI_html);
})

$(".friends-button").click(function(){ 
	var my_friends_UI_html = render_my_friends_UI();
	$("#content").html(my_friends_UI_html);
})
  
})
