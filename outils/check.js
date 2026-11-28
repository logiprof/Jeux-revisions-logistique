/* check.js <dossier_jeu> : vérifie data.js (nombre d'épreuves, types, % de cas, champs, images, bonne réponse trop longue, image de titre 16:5). */
global.window={};require(process.argv[2]+'/data.js');const fs=require('fs');
const {OBJ,META}=window;let bad=[];
const req={qcm:['q','a'],case:['s','q','a'],tf:['q','v'],fill:['q','a'],multi:['q','good','bad'],num:['q','n','tol','u'],match:['q','p'],sort:['q','c','it'],order:['q','a'],odd:['q','a'],pickimg:['q','a']};
OBJ.forEach(o=>{const ty={};let cs=0;o.ch.forEach((c,i)=>{ty[c.k]=(ty[c.k]||0)+1;if(c.k=='case')cs++;
 (req[c.k]||['??']).forEach(f=>{if(c[f]===undefined)bad.push(o.code+'#'+i+' manque '+f)});
 if(!c.ex||!c.ref)bad.push(o.code+'#'+i+' ex/ref');
 if(c.k=='tf'&&typeof c.v!=='boolean')bad.push(o.code+'#'+i+' v');
 if(c.k=='fill'&&!c.q.includes('___'))bad.push(o.code+'#'+i+' ___');
 if(c.k=='num'&&!Number.isInteger(c.n))bad.push(o.code+'#'+i+' num int');
 if(c.img&&!META.imgs[c.img])bad.push('img '+c.img);
 if(c.k=='pickimg')c.a.forEach(k=>{if(!META.imgs[k])bad.push('pick '+k)});
 if(['qcm','case'].includes(c.k)&&c.a.length!==4)bad.push(o.code+'#'+i+' 4 options');
 if(['qcm','case'].includes(c.k)){const L=c.a.map(x=>x.length);if(L[0]===Math.max(...L)&&L[0]>1.25*L.slice(1).reduce((a,b)=>a+b)/3)bad.push(o.code+'#'+i+' bonne réponse nettement la plus longue: '+c.a[0])}
 if(c.k=='sort')c.it.forEach(t=>{if(t[1]>=c.c.length)bad.push('sort idx')});
});
 const n=o.ch.length;const need=['match','sort','order','odd'].filter(t=>!ty[t]);
 console.log(o.code,n,'épreuves,',Object.keys(ty).length,'types,',Math.round(100*cs/n)+'% cas',need.length?'MANQUE '+need:'',JSON.stringify(ty));
 if(n<25||n>35)bad.push(o.code+' nombre');if(cs/n<.3)bad.push(o.code+' cas');});
Object.values(META.imgs).forEach(m=>{if(!fs.existsSync(process.argv[2]+'/'+m.src))bad.push('fichier '+m.src)});
if(!META.cover||!META.cover.src)bad.push('META.cover manquant (image de titre 16:5)');else if(!fs.existsSync(process.argv[2]+'/'+META.cover.src))bad.push('fichier '+META.cover.src);else{try{const b=fs.readFileSync(process.argv[2]+'/'+META.cover.src);let i=2;while(i<b.length){if(b[i]!==0xFF)break;const m=b[i+1],L=b.readUInt16BE(i+2);if(m>=0xC0&&m<=0xC3){const h=b.readUInt16BE(i+5),w=b.readUInt16BE(i+7);if(Math.abs(w/h-3.2)>0.02)bad.push('cover pas en 16:5 : '+w+'x'+h);break}i+=2+L}}catch(e){}}
console.log(bad.length?bad.join('\n'):'OK');
