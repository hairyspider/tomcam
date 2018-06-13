const http = require('http');
const fs = require('fs');

const hostname = '127.0.0.1';
const port = 3000;

var sqlite3 = require('sqlite3').verbose();

var prefix = "scripts"
if (process.argv.length>2)
{
  prefix = process.argv[2];
  console.log(`using argument to set db: ${prefix}`); 
}
else
{
  console.log(`using default path for database`);
}

var dbpath = `${prefix}\\sensors.db`;

var db = new sqlite3.cached.Database(dbpath);

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  switch (req.url)
  {
    case "/sensors":
      getSensors(res);  
      break;
    case "/events":
      getEvents(res);
      break;
    
    default:
      if (req.url == "/")
      {
        res.setHeader('content-type', 'text/html');
        fs.createReadStream(`${prefix}\\dashboard.html`).pipe(res);
      }
      else
      {
        pathname = `${prefix}${req.url}`;
        console.log(pathname);
        fs.exists(pathname, function (exist)
        {
          if (!exist)
          {
            res.statusCode="404";
          }
          else
          {
            if (fs.statSync(pathname).isFile())
              fs.createReadStream(pathname).pipe(res);
            else
              res.statusCode="404";
              
          }
        });

      }
      
  }
  
});

server.listen(port, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

function getSensors(res)
{
  var sql = "select round(temperature,1) as t, round(pressure,0) as p, round(moisture, 1) as m, time from sensors where julianday()-julianday(time)<2;";
  console.log(sql);
  db.all(sql, function(err, rows) {
    var o = {};
    o.requestTime=Date.now();
    o.data = rows;

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(o));
  });
}

function getEvents(res)
{
  var sql = "select events.description as d, events.time as t, eventtype.type as n  from events inner join eventtype on eventtype.id = events.typeid where julianday()-julianday(time)<2 order by events.id desc;";
  console.log(sql)
  db.all(sql, function(err, rows) {
    
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(rows));
  });

}

