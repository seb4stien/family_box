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

			<ng-view></ng-view>

		</div>

	</body>
</html>

