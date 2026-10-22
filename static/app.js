const form=document.querySelector('#quiz');
const cards=document.querySelector('#cards');
const results=document.querySelector('#results');
const STORAGE='mydrink-favorites-v2';
let catalog=[];
const getFavorites=()=>{try{const x=JSON.parse(localStorage.getItem(STORAGE)||'[]');return Array.isArray(x)?x:[]}catch{return []}};
const setFavorites=(ids)=>{try{localStorage.setItem(STORAGE,JSON.stringify(ids))}catch{};renderFavorites()};
const copyText=async text=>{try{await navigator.clipboard.writeText(text);return true}catch{const t=document.createElement('textarea');t.value=text;document.body.append(t);t.select();const done=document.execCommand('copy');t.remove();return done}};
const make=(tag,cls,text)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(text!==undefined)el.textContent=text;return el};
function renderFavorites(){const area=document.querySelector('#favorite-list');area.replaceChildren();const ids=getFavorites();if(!ids.length){area.append(make('p','','まだ保存したドリンクはありません。'));return}ids.forEach(id=>{const d=catalog.find(x=>x.id===id);if(!d)return;const item=make('div','favorite-item');const name=make('strong','',`${d.icon} ${d.name}`);const btn=make('button','','削除 ×');btn.onclick=()=>setFavorites(getFavorites().filter(x=>x!==id));item.append(name,btn);area.append(item)})}
function renderCards(drinks){catalog=[...new Map([...catalog,...drinks].map(x=>[x.id,x])).values()];cards.replaceChildren();drinks.forEach((d,index)=>{const c=make('article','card');c.append(make('div','rank',index===0?'✳ BEST MATCH':`RECOMMEND 0${index+1}`),make('div','symbol',d.icon),make('h3','',d.name));const tags=make('div','tags');d.tags.forEach(tag=>tags.append(make('span','tag',tag)));c.append(tags,make('p','',d.notes));const custom=make('div','custom');custom.append(make('strong','','おすすめカスタム'),document.createTextNode(d.custom));c.append(custom);const actions=make('div','actions');const copy=make('button','', '注文文をコピー ↗');copy.onclick=async()=>{const ok=await copyText(d.order);copy.textContent=ok?'コピーしたよ ✓':'コピーに失敗しました';setTimeout(()=>{copy.textContent='注文文をコピー ↗'},2400)};const fav=make('button','',getFavorites().includes(d.id)?'♥ 保存済み':'♡ 保存する');fav.onclick=()=>{const ids=getFavorites();setFavorites(ids.includes(d.id)?ids.filter(x=>x!==d.id):[...ids,d.id]);fav.textContent=getFavorites().includes(d.id)?'♥ 保存済み':'♡ 保存する'};actions.append(copy,fav);c.append(actions);cards.append(c)});results.hidden=false;renderFavorites();results.scrollIntoView({behavior:'smooth',block:'start'})}
form.addEventListener('submit',async e=>{e.preventDefault();const btn=form.querySelector('.submit');btn.disabled=true;btn.textContent='選んでいるよ…';try{const r=await fetch('/api/recommend',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(form)))});if(!r.ok)throw Error('通信に失敗');renderCards(await r.json())}catch{alert('診断できませんでした。接続を確認してもう一度試してね。')}finally{btn.disabled=false;btn.textContent='わたしの一杯を見つける →'}});
document.querySelector('#start').onclick=()=>document.querySelector('#diagnose').scrollIntoView({behavior:'smooth'});
document.querySelector('#retry').onclick=()=>document.querySelector('#diagnose').scrollIntoView({behavior:'smooth'});
document.querySelector('#share').onclick=async()=>{const data={title:'きょう、なに飲む？',text:'気分で選ぶドリンク＆カスタム診断',url:location.origin};if(navigator.share){try{await navigator.share(data)}catch{}}else{const ok=await copyText(data.url);alert(ok?'ページのURLをコピーしたよ！':'URLをコピーできませんでした')}};
fetch('/api/drinks').then(r=>r.json()).then(ds=>{catalog=ds;renderFavorites();renderLibrary()}).catch(()=>renderFavorites());

function renderLibrary(){
 const parent=document.querySelector('#library-list'); if(!parent)return;
 const get=id=>document.getElementById(id).value;
 const q=get('library-search').trim().toLowerCase(), kind=get('filter-kind'), sweet=get('filter-sweet'), temp=get('filter-temp'), origin=get('filter-origin');
 const budget=get('filter-budget'), cal=get('filter-cal'), fee=get('filter-free');
 const matches=catalog.filter(d=>{
  if(![d.name,d.custom,d.notes,...d.tags].join(' ').toLowerCase().includes(q))return false;
  if(kind!=='all'&&d.kind!==kind)return false;
  if(sweet!=='all'&&d.sweet!==sweet)return false;
  if(temp!=='all'&&!d.temps.includes(temp))return false;
  if(origin==='idea'&&!d.id.startsWith('idea-'))return false;
  if(origin==='existing'&&d.id.startsWith('idea-'))return false;
  if(budget!=='all'&&(d.price_yen===null||d.price_yen>Number(budget)))return false;
  if(cal!=='all'&&(d.calories_kcal===null||d.calories_kcal>Number(cal)))return false;
  if(fee==='zero'&&d.extra_fee_yen!==0)return false;
  return true;
 });
 parent.replaceChildren();
 if(!matches.length){const empty=make('div','empty-state','条件に一致する確認済みデータがありません。予算・カロリー・無料カスタムを「指定なし」にすると、未確認のレシピ案も見られます。');parent.append(empty)}
 matches.forEach(d=>{
  const c=make('article','library-item');
  const originText=d.id.startsWith('idea-')?'新規アイデア・未検証':'既存の候補・要確認';
  c.append(make('div','status-tag',originText),make('div','library-name',`${d.icon} ${d.name}`));
  c.append(make('p','library-custom',d.custom),make('p','',d.notes));
  const info=make('p','info-line',`価格：${d.price_yen===null?'未確認':d.price_yen+'円'} ／ カロリー：${d.calories_kcal===null?'未確認':d.calories_kcal+'kcal'} ／ 追加料金：${d.extra_fee_yen===null?'未確認':d.extra_fee_yen+'円'}`);c.append(info);
  const actions=make('div','actions');const b=make('button','secondary','注文文をコピー ↗');b.onclick=async()=>{b.textContent=await copyText(d.order)?'コピーしたよ ✓':'コピーできませんでした'};
  const f=make('button','secondary',getFavorites().includes(d.id)?'♥ 保存済み':'♡ 保存する');f.onclick=()=>{const ids=getFavorites();setFavorites(ids.includes(d.id)?ids.filter(x=>x!==d.id):[...ids,d.id]);f.textContent=getFavorites().includes(d.id)?'♥ 保存済み':'♡ 保存する'};
  actions.append(b,f);c.append(actions);parent.append(c);
 });
 document.querySelector('#library-count').textContent=`${matches.length} 件 / 全 ${catalog.length} 件`;
}
['library-search','filter-kind','filter-sweet','filter-temp','filter-origin','filter-budget','filter-cal','filter-free'].forEach(id=>document.getElementById(id).addEventListener('input',renderLibrary));
document.getElementById('clear-filters').onclick=()=>{document.getElementById('library-search').value='';['filter-kind','filter-sweet','filter-temp','filter-origin','filter-budget','filter-cal','filter-free'].forEach(id=>document.getElementById(id).value='all');renderLibrary()};
