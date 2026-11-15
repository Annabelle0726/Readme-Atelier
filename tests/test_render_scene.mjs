// Optional integration check: node tests/test_render_scene.mjs .work/render-runtime
import assert from 'node:assert/strict';
import {mkdtemp,writeFile,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const runtime=process.argv[2];
if(!runtime)throw new Error('Pass the optional Playwright runtime directory as the first argument.');
const directory=await mkdtemp(path.join(tmpdir(),'readme-scene-test-'));
const source=path.join(directory,'scene.html');
const frames=path.join(directory,'frames'),still=path.join(directory,'still');
const render=(args)=>spawnSync(process.execPath,[path.join(root,'skills/readme-atelier/scripts/render_scene.mjs'),
  '--input',source,'--runtime',path.resolve(runtime),...args],{encoding:'utf8'});
try{
  await writeFile(source,`<!doctype html><html><body style="margin:0"><svg id="scene" xmlns="http://www.w3.org/2000/svg" width="200" height="100"><rect width="200" height="100" fill="#fcf6ec"/><circle id="dot" cy="50" r="12" fill="#641322"/></svg><script>window.readmeAtelier={ready:true,duration:1,renderAt(t){document.getElementById('dot').setAttribute('cx',20+160*t);}};</script></body></html>`);
  let result=render(['--out',frames,'--width','200','--height','100','--fps','2']);
  assert.equal(result.status,0,result.stderr);
  const manifest=JSON.parse(await readFile(path.join(frames,'manifest.json'),'utf8'));
  assert.deepEqual(manifest.frames.map(f=>f.time),[0,0.5]);
  assert.deepEqual([manifest.width,manifest.height,manifest.duration],[200,100,1]);
  const first=await readFile(path.join(frames,manifest.frames[0].file));
  const second=await readFile(path.join(frames,manifest.frames[1].file));
  assert.notDeepEqual(first,second,'Distinct times must produce distinct pixels.');
  result=render(['--out',still,'--width','200','--height','100','--time','0.5']);
  assert.equal(result.status,0,result.stderr);
  assert.deepEqual(await readFile(path.join(still,'still.png')),second,'Still and sequence exports must agree at the same timestamp.');
  result=render(['--out',frames]);
  assert.notEqual(result.status,0);
  assert.match(result.stderr,/must be empty/);
  assert.deepEqual(await readFile(path.join(frames,manifest.frames[0].file)),first,'Refused overwrite must preserve existing frames.');
  result=render(['--out',path.join(directory,'invalid'),'--time','2']);
  assert.notEqual(result.status,0);
  assert.match(result.stderr,/exceeds scene duration/);
  await writeFile(source,`<!doctype html><html><body style="margin:0"><div id="scene" style="width:190.25px;height:90.25px;background:#641322"></div><script>window.readmeAtelier={ready:true,duration:1,renderAt(){}};</script></body></html>`);
  const fractional=path.join(directory,'fractional');
  result=render(['--out',fractional,'--width','200','--height','100','--time','0']);
  assert.equal(result.status,0,result.stderr);
  const fractionManifest=JSON.parse(await readFile(path.join(fractional,'manifest.json'),'utf8'));
  const fractionPng=await readFile(path.join(fractional,'still.png'));
  assert.deepEqual([fractionManifest.width,fractionManifest.height],[fractionPng.readUInt32BE(16),fractionPng.readUInt32BE(20)],'Manifest dimensions must match actual pixels when CSS sizes are fractional.');
  console.log('PASS: frame timing, changing pixels, deterministic still, overwrite protection, time bounds, fractional dimensions.');
}finally{
  // Only the temporary directory returned by mkdtemp above is removed.
  await rm(directory,{recursive:true,force:true});
}
