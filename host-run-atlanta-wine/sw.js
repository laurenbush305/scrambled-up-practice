const CACHE="host-run-ux-navigation-v12";
const CORE=[
  "./","./index.html","./manifest.json","./icon.svg",
  "./assets/route-map.jpg","./assets/olympic-rings.jpg","./assets/freedom-fighters-mural.jpg",
  "./assets/sun-dial.jpg","./assets/lumen-lounge.jpg","./assets/red-phone-booth.jpg","./assets/atalian.jpg","./assets/white-oak.jpg",
  "./assets/champagne.jpg","./assets/sauvignon-blanc.jpg","./assets/chardonnay-chablis.jpg","./assets/rose.jpg","./assets/pinot-noir.jpg","./assets/cabernet-sauvignon.jpg"
];
self.addEventListener("install",e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting())));
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET")return;
  e.respondWith(fetch(e.request).then(r=>{
    const copy=r.clone();caches.open(CACHE).then(c=>c.put(e.request,copy));return r;
  }).catch(()=>caches.match(e.request).then(r=>r||caches.match("./index.html"))));
});
