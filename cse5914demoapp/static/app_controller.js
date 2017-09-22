var app = angular.module('myApp', ['ngAnimate']);
app.controller('ctrl', function($http, $scope) {
	
	var self = this;
	self.recipes = [];
	
    self.ingredients = [];
	self.imageFile = "";
	self.selectedRecipe = {};
	self.newIngredient = "";
	
	
self.getIngredients = function(){
	
	$http.post("/processImage", self.imagefile)
    .then(function(d) {
        self.ingredients = self.ingredients.concat(d.data);
    });	

	
}

self.removeIngredient = function(id){
	
	self.ingredients.splice(id, 1);
	
}

self.addIngredient= function(){
	
	self.ingredients.push(self.newIngredient);
	self.newIngredient = "";
	self.postIngredients();
}

self.getRecipes = function(){
      
	$http.get("/getRecipes")
    .then(function(d) {
        self.recipes = self.recipes.concat(d.data);
		for(var i =0; i < self.recipes.length; i++){
			self.recipes[i].style = " " + (i + 2) + "s;";
		}

    });	
	
}

self.getSelected = function(){
      
	$http.get("/getSelected")
    .then(function(d) {
        
		self.selectedRecipe = d.data;

    });	
	
}

self.postIngredients = function(){
	
	$http.post("/postIngredients", self.ingredients)
    .then(function(d) {
        

    });	
	
}

self.selectRecipe = function(id){
	
	self.selectedRecipe = self.recipes[id];
	
	$http.post("/selectRecipe", self.selectedRecipe)
    .then(function(d) {
        

    });	
	
}
	
});