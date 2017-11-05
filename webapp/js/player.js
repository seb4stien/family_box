angular.module('playerApp', ['ngRoute'])
.config(['$sceDelegateProvider', '$routeProvider', function($sceDelegateProvider, $routeProvider) {
	$sceDelegateProvider.resourceUrlWhitelist([
			'self'
	]);
}])
.controller('playerController', ['$scope', '$http', '$window',
		function($scope, $http, $window) {
			$scope.method = 'GET';
			$scope.url = '/';

			$scope.tv = {
				'nb_steps': 2,
				'1': {
					label: 'Démarrer le système',
					tvon: true
				},
				'2': {
					label: 'Sélectionner une vidéo et appuyer sur lecture',
					player: true
				}
			};

			var step = $window.location.search;
			if (!step) {
				step = 1;
			} else {
				step = step.substr(1,1);
			}

			$scope.step = step;
			$scope.istep = parseInt(step);

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
