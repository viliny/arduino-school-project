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
						<div id='manualContainer'>
							<h1>Käyttöohjeet</h1>
							<p class='manualText'>
								Remote Monitoring mahdollistaa ilman kosteusprosentin, lämpötilan ja vedenpinnan korkeuden seuraamisen
								testiympäristössä. Järjestelmä lähettää myös hälytyksiä sähköpostiin, jos olosuhteet muuttuvat käyttäjän
								asettamien raja-arvojen ulkopuolelle.
							</p>
							<h3>Käyttöliittymä</h3>
							<p class='manualText'>
								Käyttöliittymä avautuu normaalisti seurantatietokoneen käynnistyessä. Jos käyttöliittymä halutaan välillä sulkea,
								sen saa takaisin käynnistämällä tietokoneen selaimen.
							</p>
							<h4>Päänäkymä</h4>
							<p class='manualText'>
								Päänäkymässä voi lisätä testilaitteita ja seurata testilaitteiden arvoja. Laitteen lisääminen tapahtuu
								painamalla "Lisää uusi" -kentässä olevaa '+' -symbolia. Tämän jälkeen syötetään avautuneeseen ikkunaan
								laitteen ID-numero, joka löytyy testilaitteen kyljestä. Voit myös nimetä laitteen haluamallasi tavalla.
								</br></br>
								Laitteen lisättyäsi pystyt seuraamaan laitteen nimellä otsikoidusta kentästä laitteen viimeisimpiä mittausarvoja.
								Jos arvot ovat käyttäjän asettamien raja-arvojen ulkopuolella, fontin väri vaihtuu punaiseksi.
								</br></br>
								Laitteen poistaminen tapahtuu otsikkokentässä olevaa rastia painamalla. Huomioithan, että laitteen poistaminen
								poistaa myös laitteella mitatun testidatan tietokannasta!
							</p>
							<h4>Tilastot</h4>
							<p class='manualText'>
								Tilastot sivulla voi luoda graafisia kaavioita testiympäristön kosteudesta ja lämpötilasta, sekä viedä testidatan
								csv-tiedostoksi.
								</br></br>
								Valitse vetovalikosta haluamasi testilaite. Valitse aloitus- ja lopetuspäivämäärät päivämääränvalitsimilla ja paina
								sen jälkeen "Luo Tilasto" -nappia. Jos valitsemallasi aikavälillä on testausdataa, tulee näytölle näkyviin 
								viivadiagrammi kyseisen aikavälin olosuhteista. Voit zoomata dataa maalaamalla hiirellä haluamasi aikaväli.
								</br></br>
								Kun haluat viedä valitsemasi testidatan .csv-tiedostoksi, paina "vie" -nappia, jonka jälkeen selain tallentaa tiedoston
								tietokoneelle. Huomaathan, että tämä tyhjentää datan tietokannasta, joten on suositeltavaa viedä data .csv:ksi vasta,
								kun kyseinen testijakso on saatu päätökseen.
							</p>
							<h4>Asetukset</h4>
							<p class='manualText'>
								Asetukset sivulla saa määriteltyä sähköpostiosoitteen, johon mahdolliset hälytykset tulevat, sekä raja-arvot kosteudelle,
								lämpötilalle ja kannen maksimiaukioloajalle. Asetuksien tallentaminen tapahtuu "Päivitä asetukset" -nappia painamalla.
							</p>
							<h4>Logi</h4>
							<p class='manualText'>
								Logi näyttää testilaitteiden status-tietoja. Logista näet esimerkiksi viimeisimmät hälytykset ja onnistuneet datan noudot
								testilaitteilta.</br></br>
								Voit suodattaa logiin näkymään vain tietyn testilaitteen, tai kaikki. Voit vaihtaa login järjestystä klikkaamalla otsikkokenttiä.
								Näin saat vaihdettua myös järjestyksen nousevasta laskevaan ja päinvastoin.
							</p>
							<h4>Käyttöohjeet</h4>
							<p class='manualText'>
								Käyttöohjeet sivu sisältää tämän käyttöohjeen.
							</p>
							<h3>Testilaite</h3>
							<p class='manualText'>
								Testilaite mittaa testiympäristön olosuhteita ja lähettää datan tietokoneelle, jossa data tallennetaan tietokantaan.
								Laite toimii langattomasti ja virransyöttö tapahtuu akkuvarmistetulla langattomalla induktiopiirillä.
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div id='footer'>Remote monitoring || prototype 2016</div>
	</body>
</html>
