var app = angular.module('myApp', ['ngAnimate']);
app.controller('ctrl', function($http, $scope) {
	
	var self = this;
	self.recipes = [];
	
    self.ingredients = {};
	self.imageFile = "";
	self.selectedRecipe = {};
	
	
self.getIngredients = function(){
	
	$http.post("/processImage", self.imagefile)
    .then(function(d) {
        self.ingredients = self.ingredients.concat(d);
    });	

	
}

self.getRecipes = function(){
   
	self.ingredients = {"ingredients":["a","b","c"]};
	$http.post("/getRecipes", self.ingredients)
    .then(function(d) {
        self.recipes = self.recipes.concat(d.data);
		for(var i =0; i < self.recipes.length; i++){
			self.recipes[i].style = " " + (i + 2) + "s;";
		}

    });	
	
}

self.selectRecipe = function(id){
	
	self.selectedRecipe = self.recipes[id];
	
}
	
});