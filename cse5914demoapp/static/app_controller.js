var app = angular.module('myApp', []);
app.controller('ctrl', function($http) {
	
	var self = this;
	self.recipes = [];
	
    self.ingredients = {};
	self.imageFile = "";
	self.activeRecipe = {};
	
	getRecipes();
	
function getIngredients(){
	
	$http.post("/processImage", self.imagefile)
    .then(function(d) {
        self.ingredients = self.ingredients.concat(d);
    });	

	
}
function getRecipes() {
   
	self.ingredients = {"ingredients":["a","b","c"]};
	$http.post("/getRecipes", self.ingredients)
    .then(function(d) {
		console.log(d);
        //self.recipes = self.recipes.concat(d);
    });	
	
}
function selectRecipe(id){
	
	self.activeRecipe = self.recipes[id];
	
}
	
});