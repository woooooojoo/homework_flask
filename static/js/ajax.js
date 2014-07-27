$(document).ready(function(){
	$('#email').change(function(){
		var email=$('#email').val();
		
		$.ajax({
			url:'/email_check',
			type:'POST',
			data:{"email":email},
			success:function(response){
				var result = $.parseJSON(response);
				console.log(result['message']);
				$("#emailalready").show();

			},
			error:function(){
				console.log('error');
			},
			complete:function(){
				console.log('complete');
			}
		});
	});

});