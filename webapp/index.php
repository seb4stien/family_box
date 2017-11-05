<!doctype html>
<html lang="en">
	<head>
		<title>Regarder une vidéo</title>

		<meta name="mobile-web-app-capable" content="yes">
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<link rel="manifest" href="manifest.json">

		<link rel="stylesheet" href="vendor/bootstrap-4.0.0/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">

		<script src="vendor/angular-1.6.6/angular.min.js"></script>
		<script src="vendor/angular-1.6.6/angular-route.min.js"></script>
		<script src="js/player.js"></script>
	</head>
	<body ng-app="playerApp">
		<div class="container-fluid" ng-controller="playerController" style="border: 1px solid black; padding: 0px">
			<nav class="navbar navbar-dark bg-dark">
				<b><a class="navbar-brand" href="/">Contrôle de la TV</a></b>
				<ul class="navbar-nav">
					<li class="nav-item"><a class="nav-link" href="#">aide</a></li>
				</ul>
			</nav>

			<div class="row" style="height: 400px">
				<div class="col-sm">
					<div class="card">
						<div class="card-header text-center">
							étape {{ step }} sur {{ tv.nb_steps }} : {{ tv[step].label }}
						</div>
						<div class="card-body text-center" ng-if="tv[step].image">
							<img src="assets/{{ tv[step].image }}" height="300px" />
						</div>
						<div class="card-body text-center" ng-if="tv[step].tvon">
							<button class="btn btn-success" ng-click="playerCommand('tvon')">Appuyer sur ce bouton pour démarrer</button>
						</div>
						<p class="text-center" ng-if="status == 200 && command == 'tvon'">
						Le système démarre. Si rien ne se passe dans 10s c'est que c'est cassé.
						</p>
						<div class="card-body text-center" ng-if="tv[step].player">
							<ul>
								<li>Un village français : saison 1 épisode 1 <button class="btn-sm btn-primary" ng-click="playerCommand('play', 'test.mp4')">lecture</button></li>
								<li>Un village français : saison 1 épisode 2 <button class="btn-sm btn-primary" ng-click="playerCommand('play', 'test.mp4')">lecture</button></li>
							</ul>
							<p class="text-center">
							<button class="btn-sm btn-primary" ng-click="playerCommand('pause')">pause / lecture</button>
							<button class="btn-sm btn-danger" ng-click="playerCommand('stop')">stop</button>
							</p>

							<p ng-if="status == 200 && command == 'play'">
							La lecture de la vidéo va commencer.
							</p>
							<p ng-if="status == 400 && command == 'play'">
							Une vidéo est déjà en cours de lecture, faire stop d'abord.
							</p>
							<p ng-if="status == 200 && command == 'stop'">
							La vidéo est arrêtée. Appuyer sur la touche TV de la télécommande pour remettre la télé.
							</p>

						</div>
					</div>
				</div>
			</div>

			<p class="text-center">
			A tout moment il est possible d'afficher la télé en appuyant sur la touche TV de la télécommande.
			</p>

			<div class="row">
				<div class="col-sm" ng-if="istep > 1">
					<a href="?{{ istep - 1}}" class="btn btn-primary">appuyer ici pour revenir à l'étape précédente</a>
				</div>
				<div class="col-sm">
				</div>
				<div class="col-sm text-right" ng-if="istep < tv.nb_steps">
					<a href="?{{ istep + 1}}" class="btn btn-primary">appuyer ici pour passer à l'étape suivante</a>
				</div>
			</div>

		</div>

	</body>
</html>

