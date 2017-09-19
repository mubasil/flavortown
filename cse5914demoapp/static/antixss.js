var app = angular.module("myApp", ["ngRoute"]);
app.config(function($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl : "main.html"
    })
    .when("/load", {
        templateUrl : "load.html"
    })
    .when("/camera", {
        templateUrl : "camera.html"
    });
});