var profile_card_html = `<div class="card">
  <img src="some_image.jpg" alt=" " style="width:100%">
  <p class="title" style="color: grey;font-size: 30px;">{0}</p>
	<a href={1}><i class="fa fa-envelope"></i></a> 
	<p hidden>{2}</p>
	{3}
  <p><button class="galleries-btn">Galleries</button></p>
</div>`;

var gallery_html = `<div class="card">
  <img src="some_image.jpg" alt=" " style="width:100%">
  <div class="title" style="color: grey;font-size: 30px;">{0}<i class="fa fa-images"></i></div>	
  <p><button class="gallery-btn">View</button></p>
</div>`;

var image_content_html = `<div class="block">
    <div class="image-container">
       <span class="helper"></span>
      <img class="image" src={0} />
    </div>
    <div class="comments-container">
      <div class="comment-title">
        <h1>Comments</h1>
        <h2>{1}</h2>
        
      </div>
      <div class="form" align="center">
         <input type="text" id="comment_input" name="comment" placeholder="Add a new comment" >
          <button class="add_comment-btn">Add</button>
      </div>
      <div class="comments">
    	{2}
      </div>
    </div>
  </div>`;
   
var comment_html = `<div id={0} class="comment">
        <h4>{1}</h4>
        <p>{2}</p>
        <p hidden>{3}</p>
        {4}
 </div>`

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

.galleries-btn, .gallery-btn {
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

.block {
  border: 5px outset blue ;
  border-radius: 10px;
  background-color: white;
  width: 70%;
  height:500px;
  margin:auto;
  margin-bottom:20px;
  margin-top:10px;
}
.image-container {
  float: left;
  width:60%;
  height:90%;
  border-radius: 5px;
  border-right:5px solid;
  border-bottom:solid blue; 
  background-color: white;
  height:500px;


}
.comm-button{
  border-radius: 50%;
}
.image{
  max-width:95%;
  max-height:99%;
  border-radius: 5px;
  border:0.5px solid;
  background-color: white;
  margin:auto;
  vertical-align: middle
}
.helper {
  display: inline-block;
  height: 100%;
  vertical-align: middle;
}

.form{
  background-color: gray;
  border-top:solid;
  border-bottom:solid;
  padding:5px
}
.comments-container {
  
  background-color: white;
  border: 1px solid gray;
 
  overflow-y:scroll;
  overflow-x:hidden;
  height:500px;

}
.comment-title{
  overflow-x:hidden;
  background-color: #3399ff;
  text-align:center;
}
.comment{
   padding-left:10px;
  border-bottom:1px solid blue;
  border-top:0.5px solid blue;
}
.background {
  background-color: white;
}

</style>
</head>
<body>
{0}
</body>
</html>`;

$(document).ready(function(){
	String.prototype.format = function() {
	  a = this;
	  for (k in arguments) {
	    a = a.replace("{" + k + "}", arguments[k])
	  }
	  return a
	}

	function get_my_email(){
		my_email = "some@email.com";//localStorage.getItem('my_email');
		return my_email;
	}

	function get_user_name(email){
		// Ajax call
		name = "Christos KK";
		return name;
	}

	function get_user(email){
		name = get_user_name(email);
		return {"name": name, "email": email};
	}

	function get_friends(){

	  	var data = JSON.stringify({my_email:get_my_email()});
		//AJAX CALL,  GETT ALL FRIENDS
		var settings = {
		  "async": true,
		  "crossDomain": true,
		  "url": "http://localhost:4010/api/friends",
		  "method": "POST",
		  "headers": {
		    "Content-Type": "application/json",
		    "Authorization": auth_token
		  },
		  "processData": false,
		  "data": data
		};

		$.ajax(settings).done(function (response) {
		  //console.log(response);
		  my_friends = response['friends'];
		})
		.fail(function (response) {
		      var message= response['responseJSON']['message'];
		        if (message != null){
		            console.log(message);
		        }else{
		            console.log("Bad request");
		        }
		});

		return my_friends;
	}

	function get_galleries(email){
		// Ajax call
		galleries = [
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

		return galleries;
	}

	function get_images(glr_name, email){
		// Ajax call
		images = [
			{
				name: "cat1",
				link: "https://news.nationalgeographic.com/content/dam/news/2018/05/17/you-can-train-your-cat/02-cat-training-NationalGeographic_1484324.ngsversion.1526587209178.adapt.1900.1.jpg"
			},
			{
				name: "cat2",
				link: "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80"
			},
			{
				name: "cat3",
				link: "https://www.humanesociety.org/sites/default/files/styles/400x400/public/2018/06/cat-217679.jpg?h=c4ed616d&itok=H0FcH69a"
			}
		];

		return images;
	}

	function get_comments(email, glr_name, image_name){
		// Ajax call
		comments = [
			{
				id: "1",
				user_name: "bob87",
				comment: "kjalskdjflkjlkjlkajlskdfj",
				email: "sdfg@dfgs.com"
			},
			{
				id: "2",
				user_name: "mary_3245",
				comment: "Hello tlkalsdfiaower",
				email: "iouo@nmn.com"
			},
			{
				id: "3",
				user_name: "jackson5",
				comment: "iuqeords.mn",
				email: "okojoi@nm.com"
			},
			{
				id: "2435",
				user_name: "mary_3245",
				comment: "Hello tlkalsdfiaower",
				email: "some@email.com"
			},
			{
				id: "2354",
				user_name: "jackson5",
				comment: "iuqeords.mn",
				email: "okojoi@nm.com"
			}
		];

		return comments;
	}
	
	target = {
		email: "default_target_email",
		glr_name: "default_target_glr_name",
		image_name: "default_image_name"
	};

	var auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzd29yZCI6IjEiLCJlbWFpbCI6IjEifQ.0KD7aL3DNXPLYV2KOFhCkE59m7V3rBrM-pJFaVPy8k4";//"Bearer " +localStorage.getItem('token');

	var my_email = get_my_email();	
	var my_user = get_user(my_email);
	var my_friends = get_friends();
	var my_galleries = get_galleries();

	function set_target_email(email){
		target.email = email;
	}

	function set_target_glr_name(name){
		target.glr_name = name;
	}

	function make_profile_card_html(user){
		var is_user_added = true;
		var friend_btn_html = (user.email == my_email)?
								'':(is_user_added?
									'<a href="#"><i class="fa fa-user-minus"></i></a>':
									'<a href="#"><i class="fa fa-user-plus"></i></a>');
		return profile_card_html.format(user.name, 
										"mailto:" + user.email, 
										user.email,
										friend_btn_html);
	}

	function render_my_profile_UI(){
		var my_profile_card_html = make_profile_card_html(my_user);
		var my_profile_html = content_section_html.format(my_profile_card_html)
		$("#content").html(my_profile_html);
	}

	function make_comment_html(comment_json){
		var my_email = get_my_email();
		var remove_btn_html = (my_email == comment_json.email)?
			'<button class="remove_comment-btn">Remove</button>':
			'';
		return comment_html.format(comment_json.id, 
								   comment_json.user_name, 
								   comment_json.comment, 
								   comment_json.email,
								   remove_btn_html);
	}

	function add_comment(comment){
		// var my_email = get_my_email();
		// target_email
		// target_glr_name
		// target_image_name
		// comment
		// Ajax call to save @ backend

		comment_html = make_comment_html(comment_json);
		$('.comments').append(comments_html);
	}

	function make_image_comments_html(comments){
		var comments_html = '';
		comments.forEach(function(comment){
			comments_html += make_comment_html(comment);
		})
		return comments_html;
	}

	function make_image_html(email, image, glr_name){
		var comments = get_comments(email, glr_name, image.name);
		var comments_html = make_image_comments_html(comments);
		return image_content_html.format(image.link, image.name, comments_html);
	}

	function make_gallery_images_UI(email, images, glr_name){
		var glr_images_html = '';
		images.forEach(function(image){
			glr_images_html += make_image_html(target.email, image, target.glr_name);
		})
		return glr_images_html;
	}

	function render_gallery_images_UI(){
		var images = get_images(target.glr_name, target.email);
		var gallery_images_html = make_gallery_images_UI(target.email, images, target.glr_name);
		content_html = content_section_html.format(gallery_images_html);
		$("#content").html(content_html);
	}

	function make_gallery_html(gallery, email){
		return gallery_html.format(gallery.name);
	}

	function make_galleries_UI(galleries, email){
		var galleries_html = '';
		galleries.forEach(function(gallery){
			galleries_html += make_gallery_html(gallery, email);
		});
		return galleries_html;
	}

	function render_galleries_UI(){
		var galleries = get_galleries(target.email);
	  	var galleries_html = make_galleries_UI(galleries, target.email);
		var galleries_UI_html = content_section_html.format(galleries_html);
		$("#content").html(galleries_UI_html);
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
		var my_friends_UI_html = content_section_html.format(my_friends_html);
		$("#content").html(my_friends_UI_html);
	}

	$(".menu-btn").click(function(){
		$(".menu-bar").toggleClass( "open" );
	})

	$(".my_profile-btn").click(function(){
		render_my_profile_UI();
	})

	$(".my_friends-btn").click(function(){ 
		render_my_friends_UI();
	})
	  
	$(".my_galleries-btn").click(function(){
		render_galleries_UI();
	})

	// Since these buttons are added dynamically
	// Event delegation is used to register the event handler
	$(document).on('click', ".galleries-btn", function(event) {
		email = $(this).parent().parent().children()[3].innerHTML;
		console.log(email);
		set_target_email(email);
		render_galleries_UI();
	});

	$(document).on('click', ".gallery-btn", function() {
		glr_name = $(this).parent().parent().children()[1].innerText;
		console.log(glr_name);
		set_target_glr_name(glr_name);
		render_gallery_images_UI();
	});

	
	$(document).on('click', ".add_comment-btn", function() {
		var comment = $('#comment_input').val();
		add_comment(comment);
		alert("Comment-added");
	});

	$(document).on('click', ".remove_comment-btn", function() {
		alert("Comment-removed");
	});

	$(".logout").click(function(){ 
	  var my_email = localStorage.getItem('my_email');
	  var auth_token = "Bearer " +localStorage.getItem('token');
	  //AJAX CALL, TO LOGOUT USER 

	  var settings = {
	  "async": true,
	  "crossDomain": true,
	  "url": "http://localhost:4020/api/logout/"+my_email,
	  "method": "GET",
	  "headers": {
	    "Authorization": auth_token
	  }
	}

	$.ajax(settings).done(function (response) {
	  console.log(response);
	  localStorage.removeItem('token');
	  localStorage.removeItem('my_email');
	  alert("Succesfully logged out");
	  window.location.href = "http://localhost:4000/login";
	})
	.fail(function (response) {
	      $("#body").hide();
	      var message= response['responseJSON']['message'];
	        if (message != null){
	            alert(message);
	        }else{
	            console.log("Bad request");
	        }
	        localStorage.removeItem('token');
	  		localStorage.removeItem('my_email');
	        window.location.href = "http://localhost:4000/login";
	});;

	})
})
