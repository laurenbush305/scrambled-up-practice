const http=require("http");
const SCORE_URL="https://raw.githubusercontent.com/laurenbush305/scrambled-up-practice/trivia-cockpit-644/dst-host/scores.json";
const server=http.createServer(async(req,res)=>{
  res.setHeader("Access-Control-Allow-Origin","*");
  res.setHeader("Cache-Control","no-store, no-cache, must-revalidate");
  if(req.url.startsWith("/health")){res.writeHead(200,{"Content-Type":"text/plain"});return res.end("ok");}
  if(req.url.startsWith("/scores")){
    try{
      const r=await fetch(SCORE_URL+"?t="+Date.now(),{cache:"no-store",headers:{"User-Agent":"dst-score-api"}});
      const body=await r.text();
      res.writeHead(r.ok?200:r.status,{"Content-Type":"application/json; charset=utf-8"});
      return res.end(body);
    }catch(e){res.writeHead(502,{"Content-Type":"application/json"});return res.end(JSON.stringify({error:"score fetch failed"}));}
  }
  res.writeHead(404,{"Content-Type":"text/plain"});res.end("not found");
});
server.listen(process.env.PORT||10000,"0.0.0.0");