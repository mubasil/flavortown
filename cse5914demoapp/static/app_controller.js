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
	self.queryText = "";
    self.recording = false;
    self.token = ""
    self.ready = false;

self.getIngredients = function(){
	
	$http.post("/processImage", self.imagefile)
    .then(function(d) {
        self.ingredients = self.ingredients.concat(d.data);
    });	

	
}

self.stream;

self.buttClick =  function() {
  
	if(recording){
		self.stopRecording();
	
	} else{
	
		self.startRecording();
	}
  
}

self.startRecording = function() {
   document.getElementById("mySpan").textContent = "...";

   setTimeout(function() {
          console.log('ready');
          document.getElementById("speakButton").classList.remove("btn-success");
          document.getElementById("speakButton").classList.add("btn-warning");

    }, 2000);
    
   recording = true;
    fetch('/api/speech-to-text/token')
  .then(function(response) {
      return response.text();
  }).then(function (token) {
    self.token = token;
    stream = WatsonSpeech.SpeechToText.recognizeMicrophone({
        token: token,
        outputElement: false
    });

    stream.setEncoding('utf8');
    
    
    stream.on('data', function(data) {
      console.log(data);
      if (data.toLowerCase().indexOf("chef") != -1){
            document.getElementById("qbox").value = data.substring(data.toLowerCase().indexOf("chef") + 5, data.indexOf("."));
            self.sendQuestion();
        }
    });
    
    stream.on('error', function(err) {
        console.log(err);
    });


  }).catch(function(error) {
      console.log(error);
  });
	
    
}
self.stopRecording =  function() {
  
  	document.getElementById("mySpan").textContent = "Speak";
    self.ready = true;
    stream.stop();
    recording = false;
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
	$http.get("/getRecipes")
    .then(function(d) {
        self.recipes = self.recipes.concat(d.data['exact']);
		self.nearRecipes = self.nearRecipes.concat(d.data['near']);
		self.loadingR = false;
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

self.sendQuestion = function(){
	
	if (self.queryText === ""){
		self.queryText = document.getElementById("qbox").value;
	}
	var query = {textInfo:self.queryText};
	self.queryText = "";
	document.getElementById("qbox").value = "";
	self.addToChat(query.textInfo, "chatbox2", "chatbox1");

	console.log(query);
	$http.post("/ask", query)
    .then(function(d) {
		d = d['data'];
        console.log(d);
		self.addToChat(d['text'], "chatbox1", "chatbox2");
		var speakingText = d['text']
		if(speakingText.includes('http')){
			speakingText = "I found this video. It might be helpful."
		}
        
        function voiceStartCallback() {
            document.getElementById("speakButton").classList.remove("btn-warning");
          document.getElementById("speakButton").classList.add("btn-success");

        }
         
        function voiceEndCallback() {
            document.getElementById("speakButton").classList.remove("btn-success");
          document.getElementById("speakButton").classList.add("btn-warning");
        }
         
        var parameters = {
            onstart: voiceStartCallback,
            onend: voiceEndCallback
        }
 
		responsiveVoice.speak(speakingText, "US English Female", parameters);
    });	
	
}


self.getAudio = function(query){
	
	var q = {textInfo:query};

	$http.post("/tts", q)
    .then(function(d) {
           
		console.log(d);
		var audio = new Audio(d);
		audio.play();
		
    });	
	
}



self.sendAudio = function(query){
	
	$http.post("/stt", query)
    .then(function(d) {
            
		self.queryText = d;
		
    });	
	
}


self.speak = function(audio) {
	
	//TODO
	
}


self.addToChat = function(t, i, j){
	
	var brs = document.createElement('div');
	
	var div = document.createElement('div');
	div.className = 'list-group';

    var div2 = document.createElement('div');
	div.className = 'list-group-item clearfix';
	
	

	//var text = document.createTextNode(t);
	
	
	//div2.appendChild(text);
	
	div2.innerHTML = t;
	
	div.appendChild(div2);

    document.getElementById(i).appendChild(div);
	
	for(var i = div.offsetHeight; i > 0; i -= 20){
		brs.appendChild(document.createElement('br'));
	}
	
	document.getElementById(j).appendChild(brs);
	var scrolly = document.getElementById('scrolly');
	scrolly.scrollTop = scrolly.scrollHeight;
}
	
});