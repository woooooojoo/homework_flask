$(document).ready(function(){
	$("#email").change(function(){
		if(!$('#email').val().match(/\w+(\@)\w+(.com|.ac.kr|.net)/))
		{
			$("#emailcheck").show();
		}
		else{
			$("#emailcheck").hide();
		}
	});
	$("#password").change(function(){
		if(!$('#password').val().match(/[a-z]/) || 
			!$('#password').val().match(/[A-Z]/)||
			!$('#password').val().match(/[0-9]/)||
			!$('#password').val().match(/\W+/) ||
			!$('#password').val().match(/.{8,20}/))
			{	
				$("#passwordcheck").show();
			}

		else{
			$("#passwordcheck").hide();
		}
	});
	$("#password_check").change(function(){
		if($('#password').val()!=$('#password_check').val())
			{	
				$("#password_checkcheck").show();
			}

		else{
			$("#password_checkcheck").hide();
		}
	});


	
	});


