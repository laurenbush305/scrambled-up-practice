const http=require('http');
const fs=require('fs');
const path=require('path');

const PORT=process.env.PORT||10000;
const USER=process.env.COCKPIT_USER||'lauren';
const PASS=process.env.COCKPIT_PASS||'change-me';
const DATA_B64=process.env.WARM_POOL_B64||'';

function authorized(req){
  const h=req.headers.authorization||'';
  if(!h.startsWith('Basic ')) return false;
  try{
    const [u,p]=Buffer.from(h.slice(6),'base64').toString('utf8').split(':');
    return u===USER && p===PASS;
  }catch(e){return false;}
}
function auth(res){
  res.writeHead(401,{'WWW-Authenticate':'Basic realm="Captain Decatur GOTV Coach"','Content-Type':'text/plain; charset=utf-8','Cache-Control':'no-store'});
  res.end('Authentication required.');
}
function send(res,status,type,body,headers={}){
  res.writeHead(status,Object.assign({'Content-Type':type,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','X-Frame-Options':'DENY'},headers));
  res.end(body);
}
const server=http.createServer((req,res)=>{
  if(req.url==='/health'){return send(res,200,'text/plain; charset=utf-8','ok');}
  if(!authorized(req)) return auth(res);
  if(req.url==='/api/warm-pool'){
    let json='{"sourceTotal":84,"loadedCount":0,"contacts":[]}';
    try{ if(DATA_B64) json=Buffer.from(DATA_B64,'base64').toString('utf8'); }catch(e){}
    return send(res,200,'application/json; charset=utf-8',json);
  }
  if(req.url==='/' || req.url.startsWith('/?')){
    try{
      const html=fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
      return send(res,200,'text/html; charset=utf-8',html);
    }catch(e){ return send(res,500,'text/plain; charset=utf-8','App file unavailable.');}
  }
  return send(res,404,'text/plain; charset=utf-8','Not found');
});
server.listen(PORT,'0.0.0.0',()=>console.log('Captain Decatur GOTV Coach listening on '+PORT));