const express = require("express");
const path = require('path');
const bodyParser = require("body-parser");
const PORT = process.env.PORT || 3001;
const app = express();

const { MongoClient } = require("mongodb");
const client = new MongoClient(process.env.FR_URI);
client.connect();
const db = client.db('leaderboards');

app.use(express.static(path.resolve(__dirname, './frontend/build')));
app.use(bodyParser.json());

app.get("/api", (req, res) => {
    console.log("GET request");
    db.collection('original_map').find({time: {$gte:0}}, {_id: 0, name:1, time:1, collectibles:1, date:1}).sort({time: 1}).toArray().then((records, err) => {
      if (err) throw err;
      console.log(records);
      res.json(records);
    });
});

app.get('*', (req, res) => {
  res.sendFile(path.resolve(__dirname, './frontend/build', 'index.html'));
});

app.post("/api", (req, res) => {
  console.log("POST request");
  console.log(req.body);
  // reject POSTs with missing/incorrect values
  if (!('name' in req.body) || !('collectibles' in req.body) || !('time' in req.body)){
    res.sendStatus(400);
    console.log("REJECTED");
    return;
  }
  if ((req.body["name"].length <= 0) || 
      (Number(req.body["collectibles"]) < 0) ||
      (Number(req.body["time"]) < 0)) {
        res.sendStatus(400);
        return;
      }

  req.body["date"] = new Date();
  req.body["date"] = req.body["date"].toISOString().substring(0,10);
  req.body["collectibles"] = Number(req.body["collectibles"]);
  req.body["time"] = Number(req.body["time"]);
  req.body["time"] = Math.floor(req.body["time"] * 1000) / 1000;

  res.sendStatus(200);
  console.log("ACCEPTED");
  db.collection('original_map').insertOne(req.body, (err, result) => {
    if (err) throw err;
  })
});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});