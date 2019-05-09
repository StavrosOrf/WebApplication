$(document).ready(function(){
  $(".menu-button").click(function(){
    $(".menu-bar").toggleClass( "open" );
})

$(".profile-button").click(function(){
  $("#content").html("<h1>Profile</h1>")
})
  
$(".galleries-button").click(function(){
  $("#content").html("<h1>My Galleries</h1>")
})

$(".friends-button").click(function(){
  $("#content").html("<h1>My Friends</h1>")
})
  
})
