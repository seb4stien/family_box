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

tvApp.controller('playerController', ['$scope', '$http', '$window', '$stateParams', '$state',
		function($scope, $http, $window, $stateParams, $state) {
			$scope.method = 'GET';
			$scope.url = '/';
			$scope.pause = false;

			if ($stateParams.video) {
					video = $stateParams.video;
					if (video.charAt(0) == '/') {
							video = $stateParams.video.substr(1);
					}

					if (detailedCatalog[video]) {
							$scope.videoPath = video;
							$scope.videos = detailedCatalog[video];
					} else {
							$scope.videos = 'player';
							$scope.videoPath = $stateParams.video;
							$scope.playerCommand('play', video);
					}
			} else {
					$scope.videos = catalog;
			}

			$scope.playerCommand = function(command, args) {
				$scope.code = null;
				$scope.response = null;
				$scope.command = command;

				if (command == "play") {
					$scope.url = "/play?file=" + args + '.mp4';
				} else if (command == "pause") {
					$scope.url = "/command/pause";
					if ($scope.pause == true) {
						$scope.pause = false;
					} else {
						$scope.pause = true;
					}
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

						if ($scope.command == 'stop') {
								path = $scope.videoPath.match('(.*)/')[1];
								$state.go('video-player', {'video': path});
						}
					}, function(response) {
						$scope.data = response.data || 'Request failed';
						$scope.status = response.status;
					});
			};
		}]);
