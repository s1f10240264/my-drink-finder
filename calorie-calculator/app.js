"use strict";
const $=id=>document.getElementById(id);
let customs=[];
const fmt=n=>(Math.round(n*10)/10).toLocaleString('ja-JP',{maximumFractionDigits:1});
function resetOptions(){
const cat=$('category').value;const previous=$('drink').value;
const choices=DRINKS.filter(d=>cat==='all'||cat===d.group);
$('drink').replaceChildren();
for(const d of choices){const o=document.createElement('option');o.value=d.id;o.textContent=d.name;$('drink').append(o)}
if(choices.some(d=>d.id===previous))$('drink').value=previous;
render();
}
function current(){return DRINKS.find(d=>d.id===$('drink').value)}
function render(){
const d=current();if(!d)return;
$('result-drink').textContent=d.name;
const unknown=customs.some(c=>c.delta===null);
const sum=customs.reduce((s,c)=>s+(c.delta??0),0);
const valid=!unknown&&d.kcal+sum>=0;
$('kcal-total').textContent=valid?fmt(d.kcal+sum):'—';
$('kcal-caption').textContent=valid?'合計カロリー':'確認待ち';
$('kcal-diff').textContent=unknown?'未確認のカスタムがあります':!valid?'合計がマイナスになるため再確認してください':sum===0?'変更なし':(sum>0?'+':'')+fmt(sum)+' kcal の変化';
const list=$('custom-list');list.replaceChildren();customs.forEach((c,i)=>{const div=document.createElement('div');div.className='custom-row';const info=document.createElement('div');info.textContent=c.type;const sub=document.createElement('span');sub.textContent=c.delta===null?'増減カロリー：未確認':(c.delta>=0?'+':'')+fmt(c.delta)+' kcal';info.append(sub);const btn=document.createElement('button');btn.type='button';btn.textContent='削除 ×';btn.setAttribute('aria-label',c.type+' を削除');btn.addEventListener('click',()=>{customs.splice(i,1);render()});div.append(info,btn);list.append(div)});
const summary=$('summary');summary.replaceChildren();const base=document.createElement('p');base.textContent='通常：'+fmt(d.kcal)+' kcal';summary.append(base);
if(customs.length){const ul=document.createElement('ul');customs.forEach(c=>{const li=document.createElement('li');li.textContent=c.type+'：'+(c.delta===null?'未確認':(c.delta>=0?'+':'')+fmt(c.delta)+' kcal');ul.append(li)});summary.append(ul)}
$('calc-status').textContent=unknown?'すべてのカスタム増減が分かると合計が表示されます。':'過去の画像をもとにした参考値です。';
}
$('category').addEventListener('change',resetOptions);
$('drink').addEventListener('change',()=>{customs=[];render()});
$('add-custom').addEventListener('click',()=>{
const input=$('custom-delta');const text=input.value.trim();
const parsed=text===''?null:Number(text);
if(parsed!==null&&(!Number.isFinite(parsed)||Math.abs(parsed)>5000)){alert('増減カロリーを確認してください。');return}
customs.push({type:$('custom-type').value,delta:parsed});
input.value='';render();
});
$('reset').addEventListener('click',()=>{customs=[];$('category').value='all';resetOptions();$('drink').value=DRINKS[0].id;render()});
$('copy').addEventListener('click',async()=>{
const d=current(),unknown=customs.some(c=>c.delta===null),sum=customs.reduce((a,c)=>a+(c.delta??0),0);
const total=unknown||d.kcal+sum<0?'未確認':fmt(d.kcal+sum)+' kcal';
const lines=['☕ '+d.name,'Tall / Hot・通常 '+fmt(d.kcal)+' kcal',...customs.map(c=>c.type+'：'+(c.delta===null?'未確認':fmt(c.delta)+' kcal')),'カスタム後：'+total,'※過去の投稿資料をもとにした参考値。現行公式値未照合。'];
try{await navigator.clipboard.writeText(lines.join('\n'));$('calc-status').textContent='結果をコピーしたよ ♡'}catch{$('calc-status').textContent='コピーできませんでした。ブラウザの許可を確認してね。'}
});
resetOptions();
