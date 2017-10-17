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

self.sendQuestion = function(query){
	
	$http.post("/ask", query)
    .then(function(d) {
            
		self.addToChat(d['text'], "chatbox1", "chatbox2");
		self.speak(d['audio']);
    });	
	
}

self.sendAudio = function(query){
	
	$http.post("/stt", query)
    .then(function(d) {
            
		self.addToChat(d, "chatbox2", "chatbox1");
		self.sendQuestion(d);

    });	
	
}

self.speak = function(audio) {
	
	//TODO
	
}


self.addToChat = function(t, i, j){
	
	var br = document.createElement('br');
	
	var div = document.createElement('div');
	div.className = 'list-group';

    var div2 = document.createElement('div');
	div.className = 'list-group-item clearfix';
	
	

	var text = document.createTextNode(t);
	
	
	div2.appendChild(text);
	
	div.appendChild(div2);

    document.getElementById(i).appendChild(div);
	document.getElementById(j).appendChild(br);
	document.getElementById(j).appendChild(br);
	document.getElementById(j).appendChild(br);
}
	
});