// usage: node render.js in.svg out.png targetWidth
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{
 const args=process.argv.slice(2);const b=await chromium.launch();
 for(let i=0;i<args.length;i+=3){
  const [inp,out,tw]=[args[i],args[i+1],+args[i+2]];
  const src=fs.readFileSync(inp,'utf8');
  const m=src.match(/viewBox="([\d.\s-]+)"/);const vb=m[1].trim().split(/\s+/).map(Number);
  const w=vb[2],h=vb[3];const dsf=tw/w;
  const ctx=await b.newContext({viewport:{width:Math.ceil(w),height:Math.ceil(h)},deviceScaleFactor:dsf});
  const p=await ctx.newPage();const errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('requestfailed',r=>errs.push('FAIL '+r.url()));
  await p.goto('file://'+require('path').resolve(inp));
  await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);
  await p.screenshot({path:out,clip:{x:0,y:0,width:w,height:h},omitBackground:false});
  if(errs.length)console.log(inp,errs);
  await ctx.close();
 }
 await b.close();
})();
