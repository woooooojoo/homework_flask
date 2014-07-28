$(document).ready(function(){
	var p= new Pusher('e51a7de31250e2d1b3bd');
	var channel=p.subscribe('likelion');
	channel.bind('notification',function(data){
		alert(data.username + 'is Online.');
	});
	
	



	$("#chat_send").click(function(){
		
		var message = $('#message').val();

		$.ajax({
			url:'/chat',
			type:'POST',
			data:{"message":message},
			success:function(response){
				console.log("send")
			}


		});
	});


	channel.bind('chatting',function(data){
		$("p").append(data['username'] + ":" + data['message'] + "<br>");	
	});

});