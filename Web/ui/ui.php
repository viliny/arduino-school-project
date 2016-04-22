<!DOCTYPE html>
<html>
	<head>
		<meta charset='UTF-8'>
		<script type='text/javascript' src='jquery.js'></script>
		<script type='text/javascript' src='jquery-ui-1.11.4.custom/jquery-ui.js'></script>
		<script type='text/javascript' src='javascript.js'></script>
		<script type='text/javascript' src='jquery.canvasjs.min.js'></script>
		<title>RMC - Watching when you can not see!</title>
		<link rel='stylesheet' type='text/css' href='jquery-ui-1.11.4.custom/jquery-ui.css'>
		<link rel='stylesheet' type='text/css' href='style.css'>
	</head>
	<body>
		<div id='wrapper'>
			<div id='header'>
				<h1>Remote Monitoring</h1>
			</div>
			<div id='content'>
				<div id='menuContainer'>
					<ul id='menu'>
						<li style="background-image: url('images/Päänäkymä.png');" class='selected' >Päänäkymä</li>
						<li style="background-image: url('images/Tilastot.png');" >Tilastot</li>
						<li style="background-image: url('images/Asetukset.png');" >Asetukset</li>
						<li style="background-image: url('images/Log.png');" >Logi</li>
						<li style="background-image: url('images/Manual.png');">Käyttöohjeet</li>
					</ul>
				</div>
				<div id='mainContent'>
					<div class='views' id='mainView'></div>
					<div class='views' style='display: none' id='dataView'>
						<h1>Tilastot</h1>
						<div style='display: none' id='exportToCsv-message' title='Vie tiedot .csv tiedostoon'></div>
						<div style='display: none' id='noData-message' title='Virhe!'></div>
						<table id="chartOptions">
							<tr><td><select id='deviceSelect'>
										<option selected="true" disabled="disabled">Valitse Laite</option>
									</select></td><td><input type='text' id='startTime' value="Aloituspäivä"></td><td>-</td><td><input type='text' id='endTime' value="Lopetuspäivä"></td></tr>
									<tr><td colspan='4'><button id='chartSubmit' style="text-align: center">Luo Tilasto</button></td></tr>
						</table>
						 <div style='display: none;' id="chartContainer"></div><button id="exportToCsv" style="display: none" onClick="exportToCsv()">Export to .csv</button>
						 <table id='log'></table>
					</div>
					<div class='views' style='display: none' id='setupView'>
						<h1>Asetukset</h1>
						<div style='display: none' id='settingsUpdate-message' title='Asetukset päivitetty!'>
							<p>Asetukset päivitetty onnistuneesti!</p>
						</div>
						<table id='setupTable'>
							<tr>
								<td>Email</td><td><input type='text' id='emailField'></td>
							</tr>
							<tr>
								<td>Nimi</td><td><input type='text' id='nameField'></td>
							</tr>
							<tr>
								<td>Min-kosteus</td><td><input type='text' id='humidityTrshldField'></td>
							</tr>
							<tr>
								<td>Min-lämpötila</td><td><input type='text' id='tempTrshldField'></td>
							</tr>
							<tr>
								<td>kansi auki-max</td><td><input type='text' id='lidSwitchTrshldTimeField'></td>
							</tr>
							<tr>
								<td colspan='2'><button id='settingsSubmit'>Päivitä Asetukset</button></td>
							</tr>
						</table>
					</div>
					<div class='views' style='display: none' id='logView'>
						<h1>Logi</h1>
						<table id='logTable'>
							<tr>
								<th class='tableHeader'>Laite</th>
								<th class='tableHeader'>Tyyppi</th>
								<th class='tableHeader'>Viesti</th>
								<th class='tableHeader'>Aika</th>
							</tr>
							<tr>
								<td>
									<select id='deviceFilter'>
									</select>
								</td>
								<td>
									<select id='typeFilter'>
									</select>
								</td>
								<td>
								</td>
								<td>

								</td>
							</tr>
						</table>
					</div>
					<div class='views' style='display: none' id='manualView'>
						<h1>Käyttöohjeet</h1>
						
						
						
					</div>
				</div>
			</div>
		</div>
		<div id='footer'>Remote monitoring || prototype 2016</div>
	</body>
</html>
