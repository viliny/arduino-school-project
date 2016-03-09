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
					$('#deviceSelect').append("<option value='" + this.deviceId + "'>" + this.deviceName + "</option>");
					
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
					if(!data)
					{
						$(boxContent).html("<table style='width: 100%;' class='dataTable'><tr style='width: 100%;' class='punainen' ><td style='width: 100%;'>Laitteella ei ole dataa</td></tr></table>");
					}else{
					var time = new Date(data.measureTime * 1000);
					var h = time.getHours();
					var m = time.getMinutes();
					var formattedTime = leadingZeros(h)+":"+leadingZeros(m);
					
					if(data.lidSwitchOpen > 0)
						var kansi = 'auki';
					else
						var kansi = 'kiinni';
						
					if(data.batteryStatus > 100)
					{
						var battery = 'Lataa';
						var batLine = "<tr><td class='right'>Virtalähde:</td><td>"+battery+"</td></tr>";
					}else
					{
						var battery = data.batteryStatus + " %";
						var batLine = "<tr class='punainen'><td class='right'>Virtalähde:</td><td>"+battery+"</td></tr>";
					}
						
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
						output += batLine;
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
					}				
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
			
				$("#deviceSelect option[value='" + deviceId + "']").remove();
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

$('#chartSubmit').click(function(){
	var deviceId = $("#deviceSelect").val();
	var deviceName = $("#deviceSelect option:selected").text();
	var startTime = $( "#startTime" ).val();
	var endTime = $("#endTime").val();
	var humidityPoints = [];
	var tempPoints = [];
	
	if(startTime == "" || endTime == "" || deviceId == "")
	{
		$('#noData-message').html("<p>Valitse laite ja aikaväli!</p>");
		$('#noData-message').dialog({
			modal: true,
			buttons: {
				'Ok': function() {
					$(this).dialog("close");
				}
			}		
		});

	}else{
		$.ajax({
				method: 'POST',
				url: "ajax.php",
				dataType: "json",
				data: {mode: 'getChart', deviceId: deviceId,startTime: startTime,endTime: endTime},
				success: function(data){
					
					if(data.length == 0)
					{
						$('#noData-message').html("<p>Laitteessa \"" + deviceName + "\" ei ole dataa valitsemallasi aikavälillä</p>");
						$('#noData-message').dialog({
							modal: true,
							buttons: {
								'Ok': function() {
									$(this).dialog("close");
								}
							}		
						});
						$('#chartContainer').fadeOut('slow');
						$('#exportToCsv').fadeOut('slow');
					}else{
						
						$('#chartContainer').fadeIn('slow');
						$('#exportToCsv').fadeIn('slow');
						var chart = new CanvasJS.Chart("chartContainer",
						{
							zoomEnabled: true,
							backgroundColor: "rgba(255,255,255,0.9)",
							
							axisX: {
								labelFontSize: 13,
								labelAngle: 45
							},
							title:{
									text: deviceName + ":n tilastot"  
									},
							data: [
								{    
									showInLegend: true,    
									legendText: "Kosteus %",
									type: "line",
									dataPoints: []
								},
								{    
									showInLegend: true,   
									legendText: "Lämpötila °C", 
									type: "line",
									dataPoints: []
								}
							]
						});
						
					$(data).each(function(){
						var date = new Date( this.measureTime * 1000);
						var min = date.getMinutes();
						min = leadingZeros(min);
						var h = date.getHours();
						h= leadingZeros(h);
						var d = date.getDate();
						var month = date.getMonth();
						var year = date.getFullYear();
						humidityPoints.push({ label: d +"." + month + ". - " + h + ":" + min, y: this.humidity});
						tempPoints.push({ label: d +"." + month + ". - " + h + ":" + min, y: this.temp });
					});
					
						chart.options.data[0].dataPoints = humidityPoints;
						chart.options.data[1].dataPoints = tempPoints;
						chart.render();
					}
				}
			});	//ajaxin päättävä
		}
});


exportToCsv = function(){
	
	var deviceId = $("#deviceSelect").val();
	var startTime = $( "#startTime" ).val();
	var endTime = $("#endTime").val();
	var deviceName = $("#deviceSelect option:selected").text();

		$('#exportToCsv-message').html("<p>Tietojen vieminen .csv:ksi poistaa laitteen \"" + deviceName + "\" tiedot järjestelmästä</p>");
		$('#exportToCsv-message').dialog({
		modal: true,
			buttons: {
				'Vie': function() {
					
					 window.location.href = 'export.php?deviceId=' + deviceId + "&startTime=" +startTime + "&endTime=" +endTime;
					$(this).dialog("close");

				},
				'Peruuta': function() {
					$(this).dialog("close");
				}		
		}
	});
}

}); //document readyn päättävä
