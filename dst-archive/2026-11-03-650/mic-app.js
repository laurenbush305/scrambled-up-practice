let stages=[],step=0;
const $=id=>document.getElementById(id);
const plain=s=>String(s??"");
const removeCorrect=s=>plain(s).replace(/\s*\(CORRECT\)/g,"").trim();
const pron=s=>s?'<div class="pron">PRONOUNCE · '+s+'</div>':"";
const say=s=>'<div class="read"><div class="read-tag">READ ALOUD</div>'+s+'</div>';
function rules(){return say('Again, welcome to Dirty South Trivia! For those who haven\'t played before, here\'s how tonight works.<p>For most rounds, I\'ll give you eight questions at once. Write your answers on one slip, put your dirty team name at the top, and bring your sheet up to me when you\'re finished.</p><p>Each team gets ONE Joker. To double your score for a round, circle the DST logo at the top of that round\'s answer sheet. Jokers are allowed in Rounds ONE through FOUR only. No Jokers in Round Five, Guess Who, or Round Six.</p><p>I\'ll explain Guess Who when we get there. Let\'s get into it!</p>');}
function answer(s,q,i){
 if(s.title==="In The Middle")return 'Number '+(i+1)+' is '+MIC.r2A[i];
 if(s.title==="Random"&&i===0)return 'Number one is capital, or capital city.';
 if(s.title==="Random"&&i===6)return 'Number seven is five: Alaska, California, Hawaii, Oregon, and Washington.';
 if(s.title==="One Simple Word"&&i===7)return 'Number eight is man. Rain Man, Iron Man, Inside Man, and Yes Man.';
 if(s.title==="What Year Is It, Anyway?"&&i===7)return 'Number eight is 2019! All seven of those events happened in 2019.';
 const a=removeCorrect(q[2]);
 return 'Number '+(i+1)+(a.match(/^[A-D]\. /)?': The correct answer is ':' is ')+a+'.';
}
function question(n,wording,hint,reveal){return '<article class="q"><div class="qhead">READ ALOUD · QUESTION '+n+'</div><div class="question">'+wording+'</div>'+pron(hint)+'<details class="answer"><summary>REVEAL ANSWER · READ ALOUD</summary><div class="answertext">'+reveal+'</div></details></article>';}
function render(){
 if(!stages.length)return;step=Math.max(0,Math.min(stages.length-1,step));const s=stages[step],name=s.title;
 const rm=String(s.label||"").match(/ROUND ([1-6])/);
 const roundNow=$("round-now");
 if(rm){roundNow.textContent='ROUND '+rm[1];roundNow.classList.remove('nonround');}
 else{roundNow.textContent=s.label||'SHOW';roundNow.classList.add('nonround');}
 $("progress").textContent='STEP '+(step+1)+' OF '+stages.length;
 $("category").textContent=s.category?'CATEGORY: '+s.category:name;
 let out="";
 if(name==="How tonight works")out=rules();
 else if(MIC.intro[name])out=say(MIC.intro[name]);
 else if(name==="Winners + goodnight")out=say('Thank you so much for coming out tonight! Please remember to tip your waitstaff and your trivia host. We\'ll see you next week!<p>Dirty South Trivia is hiring hosts. If you\'d like to live out your Alex Trebek fantasies, you can apply at DirtySouthTrivia.com.</p>');
 else if(s.say||s.read)out=say(s.say||s.read);
 if(s.qs)s.qs.forEach((q,i)=>{
  const n=i+1,net=name==="Random"&&n===1,middle=name==="In The Middle",last=name==="What Year Is It, Anyway?"&&n===8;
  const wording=net?'Question one is our internet-only question. Go to DirtySouthTrivia.com, find this week\'s internet question, and write your answer on your sheet. I\'ll let you look that up yourselves!':
    middle?'Number '+n+': '+MIC.r2Q[i]:
    last?'Now think back over those seven questions. Every event you just answered happened in the same year. For number eight, what year ties them all together?':q[1];
  out+=question(n,wording,MIC.qPron[name]?.[i]||"",answer(s,q,i));
 });
 if(s.video){
   out+='<p><a class="btn" href="https://www.youtube.com/watch?v=GQfyedmHxFw" target="_blank" rel="noopener">OPEN KNOCKOFFS VIDEO ↗</a></p>';
   (s.answers||[]).forEach((q,i)=>{
     const ans=q[1].replace(' —',' from ');
     out+='<article class="q"><div class="qhead">VIDEO ANSWER '+(i+1)+'</div>'+pron(MIC.videoPron[i])+
     '<details class="answer"><summary>REVEAL ANSWER · READ ALOUD</summary><div class="answertext">Number '+(i+1)+' is '+ans+'.</div></details></article>';
   });
 }
 if(s.clues){
   s.clues.forEach((c,i)=>{
     let txt=c[1];
     if(i===1)txt='My favorite doll is named Marie Antoinette and, thanks to my brother, I had her head removed with a guillotine.';
     out+='<article class="q"><div class="qhead">READ ALOUD · '+c[0]+' POINT CLUE</div><div class="question">'+txt+'</div>'+
     pron(MIC.cluePron[i])+(i<4?'<div class="timing">WAIT ONE MINUTE before next clue. Same person, one guess per team.</div>':'')+'</article>';
   });
   out+='<details class="answer"><summary>REVEAL · GUESS WHO ANSWER</summary><div class="answertext">The answer is Wednesday Addams.</div>'+pron('Wednesday Addams: WENZ-day AD-umz')+'</details>';
 }
 if(name==="What Year Is It, Anyway?")out+=say("That’s our final round! When you’re finished, please bring your answer sheets and pens up to me. Thank you!");
 if(name==="Tiebreaker")out+=pron("Neil Armstrong: NEEL ARM-strong · Buzz Aldrin: BUHZ AL-drin")+'<details class="answer"><summary>REVEAL TIEBREAKER ANSWER</summary><div class="answertext">The answer is 19 minutes.</div></details>';
 $("stage-body").innerHTML=out;
 $("back").disabled=step===0;$("next").disabled=step===stages.length-1;
 $("back").textContent=step===0?'← BACK':'← '+stages[step-1].title;
 $("next").textContent=step===stages.length-1?'DONE ✓':stages[step+1].title+' →';
 localStorage.setItem("dstMic650Step",String(step));window.scrollTo(0,0);
}
function show(id){
 for(const section of document.querySelectorAll('main>section'))section.classList.toggle('hidden',section.id!==id);
 for(const tab of document.querySelectorAll("[data-tab]"))tab.classList.toggle('active',tab.dataset.tab===id);
 if(id!=='host'){
  const frame=$(id==='score'?'scoreframe':'extrasframe');
  const where=id==='score'?'score':'extras';
  try{if(typeof frame.contentWindow.showView==='function')frame.contentWindow.showView(where);}catch(e){}
  frame.addEventListener('load',()=>{try{if(typeof frame.contentWindow.showView==='function')frame.contentWindow.showView(where);}catch(e){}},{once:true});
 }
 window.scrollTo(0,0);
}
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>show(b.dataset.tab));
$("back").onclick=()=>{step--;render();};
$("next").onclick=()=>{step++;render();};
fetch('./original-cockpit.html',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Source unavailable');return r.text();}).then(s=>{
const m=s.match(/const stages=(.*?);\nlet stage=/s);if(!m)throw Error('Round data not found');
stages=JSON.parse(m[1]);step=Number(localStorage.getItem('dstMic650Step')||0);render();
}).catch(()=>{$("stage-body").textContent="Could not load the original quiz data. Refresh or open the original Word document in the reference section.";});
