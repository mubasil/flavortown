var app = angular.module('myApp', ["ngTable", "ngResource"]);
app.controller('mainCtrl', function($scope, NgTableParams, $resource, $http) {
	
	var self = this;
	self.recipes = [];
	
    self.ingredients = [];
	self.imageFile = "";
	
function getIngredients(){
	
	$http.post("/processImage", self.imagefile)
    .then(function(d) {
        self.ingredients = self.ingredients.concat(d);
    });	

	
}
function getRecipes() {
    
	$http.post("/getRecipes", self.ingredients)
    .then(function(d) {
        self.recipes = self.recipes.concat(d);
    });	
	
}
	
});