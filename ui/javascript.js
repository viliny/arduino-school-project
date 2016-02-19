//ui:n javascriptit ja jQueryt

$(document).ready(function(){
	
var menuselected = $('.selected');
var email;
var name;
var humidityTrshld;
var tempTrshld;
var lidSwitchTrshlTime;

	$('li').click(function(){
		$(menuselected).attr('class','');
		$(this).attr('class','selected');
		menuselected = this;
		
		if($(menuselected).text() == 'Päänäkymä')
		{
			$('#mainView').fadeIn('fast');
			$('#dataView').fadeOut('fast');
			$('#setupView').fadeOut('fast');
		}
		
		if($(menuselected).text() == 'Tilastot')
		{
			$('#mainView').fadeOut('fast');
			$('#dataView').fadeIn('fast');
			$('#setupView').fadeOut('fast');
		}
		
		if($(menuselected).text() == 'Asetukset')
		{
			$('#mainView').fadeOut('fast');
			$('#dataView').fadeOut('fast');
			$('#setupView').fadeIn('fast');
		}
	});
	
	
	
	load = function(){
		
		$.ajax({
			method: 'POST',
			url: "ajax.php",
			data: {mode: 'getSettings'},
			dataType: 'json',
			success: function(data){
				email = data.email;
				name = data.name;
				humidityTrshld = data.humidityTrshld;
				tempTrshld = data.tempTrshld;
				lidSwitchTrshldTime = data.lidSwitchTrshldTime;
				$('#emailField').val(email);
				$('#nameField').val(name);
				$('#humidityTrshldField').val(humidityTrshld);
				$('#tempTrshldField').val(tempTrshld);
				$('#lidSwitchTrshldTimeField').val(lidSwitchTrshldTime);
			}
			
		});
		
		$.ajax({
			method: 'POST',
			url: "ajax.php",
			data: {mode: 'updateDevices'},
			dataType: 'json',
			success: function(data){
				$('#mainView').html("<div id='addNew-message' style='display: none' title='Lisää uusi laite'><table id='addNewTable'><tr><td>ID:</td><td><input type='text' id='newIdField'></td></tr><tr><td>Nimi:</td><td><input type='text' id='newNameField'></td></tr></table></div><h1 class='mainViewHeader'>Päänäkymä</h1>");
				$('#mainView').append("<div id='deleteDialog' style='display: none' title='Poista laite'></div>");
				$(data).each(function(){
					if(this.error == 1)
					{
						$('#mainView').append(						
							"<div class='box'><div class='boxHeader alert'>" + this.deviceName + "<div onclick=\"deleteDevice('" + this.deviceName + "','" + this.deviceId +"',this)\" class='delete'>X</div></div><div class='boxContent' id='" + this.deviceId +"'></div></div>"
						);
					}else
					{
						$('#mainView').append(						
							"<div class='box'><div class='boxHeader'>" + this.deviceName + "<div onclick=\"deleteDevice('" + this.deviceName + "','" + this.deviceId +"',this)\" class='delete'>X</div></div><div class='boxContent' id='" + this.deviceId +"'></div></div>"
						);
					}
					updateDevice();
					$('#deviceSelect').append("<option val='" + this.deviceId + "'>" + this.deviceName + "</option>");
					
				});
				$('#mainView').append(
						"<div class='box'><div class='boxHeader'>Lisää uusi</div><div onClick='addNewDialog()' class='boxContent' id='addNew'>+</div></div>"
					);
				
				
				
			}
			
		});
		
	}
	
	
	
	
	updateDevice = function(){
		$('.box').each(function(){
			var boxContent = $(this).children('.boxContent');
			var id = $(boxContent).attr('id');
			if(id != 'addNew')
			{
			$.ajax({
				method: 'POST',
				url: "ajax.php",
				data: {mode: 'updateDevice', id: id},
				dataType: 'json',
				success: function(data){
					var time = new Date(data.measureTime * 1000);
					var h = time.getHours();
					var m = time.getMinutes();
					var formattedTime = leadingZeros(h)+":"+leadingZeros(m);
					
					if(data.lidSwitchOpen > 0)
						var kansi = 'auki';
					else
						var kansi = 'kiinni';
						
					if(data.waterLevelLow > 0)
						var vesi = 'matala!';
					else
						var vesi = 'ok';
					var output = "<table class='dataTable'>";
					
					if(data.humidity >= humidityTrshld)
						output += "<tr><td class='right'>Kosteus:</td><td>"+data.humidity+" %</td></tr>";
					else
						output += "<tr class='punainen'><td class='right'>Kosteus:</td><td>"+data.humidity+" %</td></tr>";
					if(data.temp >= tempTrshld)	
						output += "<tr><td class='right'>Lämpötila:</td><td>"+data.temp+" °C</td></tr>";
					else
						output += "<tr class='punainen'><td class='right'>Lämpötila:</td><td>"+data.temp+" °C</td></tr>";
					output += "<tr><td class='right'>Virtalähde:</td><td>"+data.batteryStatus+"</td></tr>";
					if(kansi == "kiinni")
						output += "<tr><td class='right'>Kansi:</td><td>"+kansi+"</td></tr>";
					else
						output += "<tr class='punainen'><td class='right'>Kansi:</td><td>"+kansi+"</td></tr>";
					if(vesi == 'ok')
						output += "<tr><td class='right'>Vedenpinta:</td><td>"+vesi+"</td></tr>";
					else
						output += "<tr class='punainen'><td class='right'>Vedenpinta:</td><td>"+vesi+"</td></tr>";
					output += "<tr><td class='right'>Klo:</td><td>"+formattedTime+"</td></tr>";
					output += "</table>";
					$(boxContent).html(output);
										
					}	//successin päättävä
			});	//ajaxin päättävä
		}//ifin päättävä	
		}); //eachin päättävä

	}

	
leadingZeros = function(n) //lisää puuttuvan nollan minuuttien/tuntien eteen jos yksinumeroinen
{
	if(n < 10)
	{
		n = '0' + n; 
	}	
	return n;
}


addNewDialog = function(){
			$("#addNew-message").dialog({
			modal: true,
			buttons: {
				'Lisää': function() {
					var deviceId = $("#newIdField").val();
					var deviceName = $("#newNameField").val();
					$.ajax({
					method: 'POST',
					url: "ajax.php",
					data: {mode: 'addNewDevice', deviceId: deviceId,deviceName: deviceName}
					});	//ajaxin päättävä
					
					location.reload();
				},
				'Peruuta': function() {
					$(this).dialog("close");
				}
				
		}
	}); //dialogin sulkeva
} // funktion sulkeva

deleteDevice = function(deviceName, deviceId, e)
{
	var box = $(e).parents(".box");
	$('#deleteDialog').html("<p>Poistetaanko laite " + deviceName + "</p>");
	$('#deleteDialog').dialog({
		modal: true,
			buttons: {
				'Poista': function() {
					$.ajax({
					method: 'POST',
					url: "ajax.php",
					data: {mode: 'deleteDevice', deviceId: deviceId}
					});	//ajaxin päättävä
					
					$(this).dialog("close");
					$(box).fadeOut('slow', function(){
					$(box).remove();
		});
			
				},
				'Peruuta': function() {
					$(this).dialog("close");
				}
				
		}
	}); //dialogin sulkeva
	
	
	

}

$('#settingsSubmit').click(function(){
	
	email = $('#emailField').val();
	name =  $('#nameField').val();
	humidityTrshld = $('#humidityTrshldField').val();
    tempTrshld = $('#tempTrshldField').val();
	lidSwitchTrshldTime = $('#lidSwitchTrshldTimeField').val();
	
	  $( "#settingsUpdate-message" ).dialog({
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });
	
	$.ajax({
				method: 'POST',
				url: "ajax.php",
				data: {mode: 'setSettings', email: email,name: name,humidityTrshld: humidityTrshld,tempTrshld: tempTrshld,lidSwitchTrshldTime: lidSwitchTrshldTime}
			});	//ajaxin päättävä
});

load();

setInterval(function(){updateDevice();},10000);


$(function() {
	$( "#startTime" ).datepicker();
    $( "#startTime" ).datepicker( "option", "dateFormat", "d.m.yy" );
});
  
$(function() {
    $( "#endTime" ).datepicker();
    $( "#endTime" ).datepicker( "option", "dateFormat", "d.m.yy" );
});

}); //document readyn päättävä
