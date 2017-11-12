var tvApp = angular.module('tvApp', ['ui.router']);

tvApp.config(['$stateProvider', function($stateProvider) {
	$stateProvider
		.state('home', {'url': '/', templateUrl: 'partials/home.html'})
		.state('start', {'url': '/start', templateUrl: 'partials/start.html'})
		.state('video-player', {'url': '/video-player/{video}', controller: 'playerController', templateUrl: 'partials/video-player.html'})
		.state('photo-viewer', {'url': '/photo-viewer', templateUrl: 'partials/photo-viewer.html'})
		.state('stop', {'url': '/stop', templateUrl: 'partials/stop.html'})
		.state('help', {'url': '/help', templateUrl: 'partials/help.html'})
}]);

tvApp.controller('playerController', ['$scope', '$http', '$window', '$stateParams',
		function($scope, $http, $window, $stateParams) {
			$scope.method = 'GET';
			$scope.url = '/';

			var catalog = [
					'Un village français'
					];

			var detailedCatalog = {
					'/Un village français': ['Saison 1', 'Saison 2'],
					'/Un village français/Saison 1': ['Episode 1'],
					'/Un village français/Saison 2': ['Episode 2']
			}

			if ($stateParams.video == '') {
				$scope.videos = catalog;
			} else {
				if (detailedCatalog[$stateParams.video]) {
					$scope.parentVideo = $stateParams.video;
					$scope.videos = detailedCatalog[$stateParams.video];
				} else {
					$scope.videos = 'player';
					$scope.parentVideo = $stateParams.video;
					$scope.player = true;
				}
			}

			$scope.playerCommand = function(command, args) {
				$scope.code = null;
				$scope.response = null;
				$scope.command = command;

				if (command == "play") {
					$scope.url = "/play?file=" + args;
				} else if (command == "status") {
					$scope.url = "/status";
				} else if (command == "tvon") {
					$scope.url= "/api/turn-tv-on.php";
				} else {
					$scope.url = "/command/" + command;
				}

				$http({method: $scope.method, url: $scope.url}).
					then(function(response) {
						$scope.status = response.status;
						$scope.data = response.data;
					}, function(response) {
						$scope.data = response.data || 'Request failed';
						$scope.status = response.status;
					});
			};
		}]);
