var Subjects = require('./models/SubjectViews');
var fs = require('fs');
var csv = require('fast-csv');
// var sbux = require('././sbux.csv');
module.exports = function(app) {

	// server routes ===========================================================
	// handle things like api calls
	// authentication routes	
	// sample api route
 app.get('/api/data', function(req, res) {
  // file = fs.readFileSync('sbux.csv');
  // use mongoose to get all nerds in the database

  //   Subjects.find({}, {'_id': 0, 'school_state': 1, 'resource_type': 1, 'poverty_level': 1, 'date_posted': 1, 'total_donations': 1, 'funding_status': 1, 'grade_level': 1}, function(err, subjectDetails) {
  //   // Subjects.find({}, {'_id': 0, 'Text': 1, 'Retweets': 1, 'Mentions': 1, 'Date': 1, 'Favorites': 1, 'Geo': 1, 'Username': 1, 'Hashtages': 1}, function(err, subjectDetails) {
  //  // if there is an error retrieving, send the error. 
  //      // nothing after res.send(err) will execute
  //  if (err) 
  //  res.send(err);
  //   res.json(subjectDetails); // return all nerds in JSON format
  // });

    var sbux = [];
    console.log(sbux.length);
    fs.createReadStream("sbux.csv")
    .pipe(csv())
    .on("data", function(data){
        sbux.push(data.slice(0,2));
        // console.log(sbux.length);
        // console.log(data);
    })
    .on("end", function(){
        console.log(sbux.length);
        res.send(sbux);
        // res.send(sbux);
        console.log("done");
    });

    // console.log('sbux.length');
 });

 



 // frontend routes =========================================================
 app.get('*', function(req, res) {
  res.sendfile('./public/login.html');
 });
}