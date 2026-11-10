/* Cafe pairing and reference calories: editorial suggestions, not an official Starbucks database. */
(() => {
const $=id=>document.getElementById(id);
const drinkProfiles={
'latte':{name:'スターバックス ラテ',taste:'mellow',pair:'バタースコッチドーナツ',why:'ミルクのまろやかさとバター風味の甘さが好相性。'},
'coffee':{name:'ドリップ コーヒー',taste:'roast',pair:'チョコレートチャンクスコーン',why:'コーヒーの香ばしさがチョコの甘さを引き立てます。'},
'matcha':{name:'抹茶 ティー ラテ',taste:'tea',pair:'ニューヨークチーズケーキ',why:'抹茶のほろ苦さとチーズのコクを楽しめます。'},
'caramel':{name:'キャラメル マキアート',taste:'sweet',pair:'シュガードーナツ',why:'キャラメルの香りとシンプルな甘さがなじみます。'},
'yuzu':{name:'ゆず シトラス & ティー',taste:'fresh',pair:'レモンケーキ',why:'柑橘の爽やかさを重ねて楽しむ組み合わせ。'}
};
const foodProfiles={
'choco':{name:'チョコレート系スイーツ',dr:'ドリップ コーヒー（深煎り系）',why:'深いコクとほろ苦さが、チョコの甘みをまとめます。'},
'cake':{name:'チーズケーキ',dr:'スターバックス ラテ',why:'エスプレッソとミルクのバランスが濃厚なチーズと合います。'},
'donut':{name:'ドーナツ',dr:'カフェ アメリカーノ',why:'軽やかな口当たりでドーナツの甘さを引き立てます。'},
'sandwich':{name:'サンドイッチ',dr:'ドリップ コーヒー（中煎り系）',why:'香ばしさとすっきりした後味が食事に合います。'},
'scone':{name:'スコーン',dr:'カフェ ミスト',why:'やわらかなミルクの風味と焼き菓子の香りがよく合います。'}
};
const coffeeProfiles={
'light':{name:'浅煎り・酸味を楽しむコーヒー',food:'フルーツ系の焼き菓子',why:'爽やかな酸味と果実の香りが響き合います。'},
'medium':{name:'中煎り・バランスのよいコーヒー',food:'バタースコーン',why:'ナッツのような香ばしさとバターの風味がなじみます。'},
'dark':{name:'深煎り・コクのあるコーヒー',food:'チョコレート系スイーツ',why:'力強いコクがチョコレートの甘さと好相性です。'}
};
const baseCalories=[
{name:'カモミール ティー',kcal:0},{name:'ゼンクラウド ウーロン',kcal:1},
{name:'ジョイフルメドレー ティー',kcal:2},{name:'カフェ アメリカーノ',kcal:11},
{name:'カプチーノ',kcal:119},{name:'カフェ ミスト',kcal:133},
{name:'アーモンドミルク ラテ',kcal:159},{name:'カモミール ティー ラテ',kcal:184},
{name:'ジョイフルメドレー ティー ラテ',kcal:186},{name:'イングリッシュ ブレックファスト ティー ラテ',kcal:189},
{name:'キャラメル マキアート',kcal:222},{name:'チャイ ティー ラテ',kcal:227},
{name:'抹茶 ティー ラテ',kcal:231},{name:'スターバックス ラテ',kcal:232},
{name:'ほうじ茶＆クラシック ティー ラテ',kcal:265}
];
function fillSelect(id,items,mapper){const el=$(id);if(!el)return;items.forEach(item=>{const o=document.createElement('option');const [v,label]=mapper(item);o.value=v;o.textContent=label;el.append(o)})}
fillSelect('pair-drink',Object.entries(drinkProfiles),([k,v])=>[k,v.name]);
fillSelect('pair-food',Object.entries(foodProfiles),([k,v])=>[k,v.name]);
fillSelect('pair-coffee',Object.entries(coffeeProfiles),([k,v])=>[k,v.name]);
fillSelect('cal-drink',baseCalories.map((d,i)=>[i,d]),([i,d])=>[i,d.name]);
const pairs=$('pair-result'),calResult=$('cal-result');
function renderPair(){const mode=$('pair-mode').value;const selected=mode==='drink'?drinkProfiles[$('pair-drink').value]:mode==='food'?foodProfiles[$('pair-food').value]:coffeeProfiles[$('pair-coffee').value];
if(!selected)return;
let headline=mode==='drink'?selected.pair:mode==='food'?selected.dr:selected.food;
pairs.replaceChildren();
const strong=document.createElement('strong');strong.textContent='おすすめ：'+headline;
const detail=document.createElement('p');detail.textContent=selected.why;
const note=document.createElement('small');note.textContent='※ 味わいに基づく提案です。商品・豆の取り扱いは店舗や時期により異なります。';
pairs.append(strong,detail,note);
}
function showPairControls(){const mode=$('pair-mode').value;['drink','food','coffee'].forEach(x=>{$('pair-'+x+'-wrap').hidden=x!==mode});renderPair()}
function renderCalories(){
const d=baseCalories[Number($('cal-drink').value)];
if(!d)return;
const change=$('cal-change').value;
calResult.replaceChildren();
const strong=document.createElement('strong');strong.textContent=change==='standard'?d.kcal+' kcal':'変更後カロリー：確認待ち';
const detail=document.createElement('p');detail.textContent=change==='standard'?d.name+'（Tall・ホット・画像掲載時の通常レシピ）':('通常レシピ：'+d.kcal+' kcal。変更後の正確な栄養値が未登録のため、差分は計算できません。');
const note=document.createElement('p');note.className='feature-small';note.textContent='出典：以前作成した「冬のスタバ HOTドリンク低カロリーランキング」画像。現行公式値との照合は未完了です。商品によって変更できないカスタムがあります。';
calResult.append(strong,detail,note);
}
$('pair-mode')?.addEventListener('change',showPairControls);
['pair-drink','pair-food','pair-coffee'].forEach(id=>$(id)?.addEventListener('change',renderPair));
$('cal-drink')?.addEventListener('change',renderCalories);
$('cal-change')?.addEventListener('change',renderCalories);
showPairControls();if($('cal-drink'))renderCalories();
})();