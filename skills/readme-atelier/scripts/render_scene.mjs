#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

const help = `Render a deterministic README scene to PNG frames.
Setup in an optional local runtime: npm install --prefix .work/render-runtime playwright
Install its browser: node .work/render-runtime/node_modules/playwright/cli.js install chromium
Usage:
  node render_scene.mjs --input scene.html --out frames --runtime .work/render-runtime
  node render_scene.mjs --input scene.html --out still --time 9 --selector '#scene'
Options: --width 960 --height 640 --fps 12 --duration 12 --time 9
         --selector '#scene' --runtime <package-directory> --browser <executable>
Input may be a local HTML path or an explicit http(s) URL. The page must expose
window.readmeAtelier.ready, .duration and .renderAt(seconds). Existing output
files are never replaced. Full animations write manifest.json; stills write still.png.
`;

async function main() {
  const args = process.argv.slice(2);
  if (!args.length || args.includes('--help')) { console.log(help); return; }
  const allowed = new Set(['input','out','width','height','fps','duration','time','selector','runtime','browser']);
  const opts = {};
  for(let i=0;i<args.length;i+=2){
    const key=args[i].replace(/^--/,'');
    if(!args[i].startsWith('--')||!allowed.has(key)||args[i+1]===undefined) throw new Error(`Invalid argument: ${args[i]}`);
    opts[key]=args[i+1];
  }
  if(!opts.input||!opts.out) throw new Error('--input and --out are required.');
  const number=(key,fallback,min,max)=>{
    const n=Number(opts[key]??fallback);
    if(!Number.isFinite(n)||n<min||n>max)throw new Error(`Invalid --${key}: ${opts[key]}`);
    return n;
  };
  const width=number('width',960,100,3840),height=number('height',640,100,3840);
  if(!Number.isInteger(width)||!Number.isInteger(height))throw new Error('Viewport dimensions must be integers.');
  const fps=number('fps',12,1,50);
  const time=opts.time===undefined?null:number('time',0,0,120);
  const out=path.resolve(opts.out);
  await fs.mkdir(out,{recursive:true});
  if((await fs.readdir(out)).length)throw new Error('Output directory must be empty; use a fresh export directory.');
  const require=createRequire(path.resolve(opts.runtime??process.cwd(),'package.json'));
  let chromium;
  try { ({chromium}=require('playwright')); }
  catch { throw new Error('Playwright not found. Pass --runtime pointing to its package directory. See --help.'); }
  const browser=await chromium.launch({headless:true,...(opts.browser?{executablePath:path.resolve(opts.browser)}:{})});
  const errors=[];
  try{
    const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1,reducedMotion:'reduce'});
    page.on('pageerror',e=>errors.push(e.message));
    await page.addInitScript(()=>{window.__README_EXPORT__=true;});
    const url=/^https?:\/\//.test(opts.input)?opts.input:pathToFileURL(path.resolve(opts.input)).href;
    await page.goto(url,{waitUntil:'load'});
    await page.waitForFunction(()=>window.readmeAtelier?.ready===true,{},{timeout:15000});
    const sceneDuration=await page.evaluate(()=>window.readmeAtelier.duration);
    if(!Number.isFinite(sceneDuration)||sceneDuration<=0||sceneDuration>120)throw new Error('Scene duration must be in (0, 120] seconds.');
    const duration=number('duration',sceneDuration,0.01,sceneDuration);
    if(time!==null&&time>sceneDuration)throw new Error('--time exceeds scene duration.');
    const target=page.locator(opts.selector??'#scene');
    if(await target.count()!==1)throw new Error('Scene selector must match exactly one element.');
    const count=time===null?Math.ceil(duration*fps):1;
    const frames=[];
    let capturedSize;
    for(let i=0;i<count;i++){
      const t=time??i/fps;
      await page.evaluate(async seconds=>{await window.readmeAtelier.renderAt(seconds);await document.fonts.ready;},t);
      if(errors.length)throw new Error(errors.join('\n'));
      const file=time===null?`frame-${String(i).padStart(5,'0')}.png`:'still.png';
      const png=await target.screenshot({path:path.join(out,file),animations:'disabled'});
      // Fractional CSS bounds can round differently from the actual PNG crop.
      const size=[png.readUInt32BE(16),png.readUInt32BE(20)];
      if(capturedSize&&(size[0]!==capturedSize[0]||size[1]!==capturedSize[1]))throw new Error('Scene dimensions changed during capture; use a fixed export layout.');
      capturedSize=size;
      frames.push({file,time:t});
    }
    const manifest={schemaVersion:1,fps,duration:time===null?duration:0,width:capturedSize[0],height:capturedSize[1],frames};
    await fs.writeFile(path.join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
    console.log(JSON.stringify({out,frameCount:count,width:manifest.width,height:manifest.height,duration:manifest.duration}));
  }finally{await browser.close();}
}
main().catch(error=>{console.error(error.message);process.exitCode=1;});
