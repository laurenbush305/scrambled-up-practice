const http=require("http");
const BASE="https://raw.githubusercontent.com/laurenbush305/scrambled-up-practice/trivia-cockpit-644/";
const SCORE_FILES={"pub646-20261020":"dst-host/scores.json","pub648-20261027":"dst-archive/2026-10-27-648/scores.json"};
const server=http.createServer(async(req,res)=>{
  res.setHeader("Access-Control-Allow-Origin","*");
  res.setHeader("Cache-Control","no-store, no-cache, must-revalidate");
  if(req.url.startsWith("/health")){res.writeHead(200,{"Content-Type":"text/plain"});return res.end("ok");}
  if(req.url.startsWith("/scores")){
    try{
      const url=new URL(req.url,"http://localhost");
      const quiz=url.searchParams.get("quiz")||"pub646-20261020";
      if(!Object.prototype.hasOwnProperty.call(SCORE_FILES,quiz)){res.writeHead(404,{"Content-Type":"application/json"});return res.end(JSON.stringify({error:"Unknown quiz"}));}
      const r=await fetch(BASE+SCORE_FILES[quiz]+"?t="+Date.now(),{cache:"no-store",headers:{"User-Agent":"dst-score-api"}});
      const body=await r.text();
      res.writeHead(r.ok?200:r.status,{"Content-Type":"application/json; charset=utf-8"});
      return res.end(body);
    }catch(e){res.writeHead(502,{"Content-Type":"application/json"});return res.end(JSON.stringify({error:"score fetch failed"}));}
  }
  res.writeHead(404,{"Content-Type":"text/plain"});res.end("not found");
});
server.listen(process.env.PORT||10000,"0.0.0.0");