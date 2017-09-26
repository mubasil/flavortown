var app = angular.module('myApp', ['ngAnimate']);
app.controller('ctrl', function($http, $scope) {
	
	var self = this;
	self.recipes = [];
	self.nearRecipes = [];
	self.loadingR = true;
	self.loadingN = true;
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
    
	self.loadingR = true;
	$http.get("/getExactRecipes")
    .then(function(d) {
        self.recipes = self.recipes.concat(d.data);
		self.loadingR = false;
    });	
	
	$http.get("/getNearRecipes")
    .then(function(d) {
        self.nearRecipes = self.nearRecipes.concat(d.data);

		self.loadingN=false;

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
                    window.location='/page/recipe'

    });	
	
}

self.selectNearRecipe = function(id){
	
	self.selectedRecipe = self.nearRecipes[id];
	
	$http.post("/selectRecipe", self.selectedRecipe)
    .then(function(d) {
                    window.location='/page/recipe'


    });	
	
}
	
});