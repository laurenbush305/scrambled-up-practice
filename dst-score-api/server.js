const http=require("http");
const BASE="https://raw.githubusercontent.com/laurenbush305/scrambled-up-practice/trivia-cockpit-644/";
const LIVE654="https://laurenbush305.github.io/scrambled-up-practice/trivia/current/scores.json";
const SCORE_FILES={"pub646-20261020":"dst-host/scores.json","pub648-20261027":"dst-archive/2026-10-27-648/scores.json","pub650-20261103":"dst-archive/2026-11-03-650/scores.json","pub652-20261110":"dst-archive/2026-11-10-652/scores.json","pub654-20261117":"dst-archive/2026-11-17-654/scores.json"};
const server=http.createServer(async(req,res)=>{
  res.setHeader("Access-Control-Allow-Origin","*");
  res.setHeader("Cache-Control","no-store, no-cache, must-revalidate");
  if(req.url.startsWith("/health")){res.writeHead(200,{"Content-Type":"text/plain"});return res.end("ok");}
  if(req.url.startsWith("/scores")){
    try{
      const url=new URL(req.url,"http://localhost");
      const quiz=url.searchParams.get("quiz")||"pub646-20261020";
      if(!Object.prototype.hasOwnProperty.call(SCORE_FILES,quiz)){res.writeHead(404,{"Content-Type":"application/json"});return res.end(JSON.stringify({error:"Unknown quiz"}));}
      const stamp=Date.now();
      const sources=[BASE+SCORE_FILES[quiz]+"?t="+stamp];
      if(quiz==="pub654-20261117")sources.push(LIVE654+"?t="+stamp);
      const results=await Promise.allSettled(sources.map(async src=>{
        const r=await fetch(src,{cache:"no-store",headers:{"User-Agent":"dst-score-api","Cache-Control":"no-cache"}});
        if(!r.ok)throw new Error("HTTP "+r.status);
        const body=await r.text();
        const data=JSON.parse(body);
        return {body,data};
      }));
      const candidates=results.filter(x=>x.status==="fulfilled").map(x=>x.value);
      if(!candidates.length)throw new Error("No score source available");
      candidates.sort((a,b)=>Number(b.data.revision||0)-Number(a.data.revision||0));
      const best=candidates[0];
      res.writeHead(200,{"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store, no-cache, must-revalidate"});
      return res.end(best.body);
    }catch(e){res.writeHead(502,{"Content-Type":"application/json"});return res.end(JSON.stringify({error:"score fetch failed"}));}
  }
  res.writeHead(404,{"Content-Type":"text/plain"});res.end("not found");
});
server.listen(process.env.PORT||10000,"0.0.0.0");
