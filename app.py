from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Sample recommendations maintained manually. Verify availability/customization with official menus before sharing.
DRINKS = [
 {'id':'latte','name':'スターバックス ラテ','kind':'coffee','temps':['ice','hot'],'sweet':'low','moods':['relax','light'],'milk':True,'custom':'無脂肪乳に変更','notes':'エスプレッソの香りとミルクの味わい。甘さ控えめが好みの人に。','tags':['コーヒー','定番'],'icon':'☕','order':'スターバックス ラテを無脂肪乳に変更でお願いします。'},
 {'id':'caramel','name':'キャラメル マキアート','kind':'coffee','temps':['ice','hot'],'sweet':'sweet','moods':['treat','relax'],'milk':True,'custom':'キャラメルソース多め','notes':'コーヒー感と甘さの両方を楽しみたい日に。','tags':['甘め','ご褒美'],'icon':'🍮','order':'キャラメル マキアートをキャラメルソース多めでお願いします。'},
 {'id':'matcha','name':'抹茶 ティー ラテ','kind':'tea','temps':['ice','hot'],'sweet':'sweet','moods':['treat','relax'],'milk':True,'custom':'オーツミルクに変更','notes':'香り豊かな抹茶をまろやかに楽しめる一杯。','tags':['抹茶','まろやか'],'icon':'🍵','order':'抹茶 ティー ラテをオーツミルクに変更でお願いします。'},
 {'id':'yuzu','name':'ゆず シトラス & ティー','kind':'tea','temps':['ice'],'sweet':'fresh','moods':['refresh','light'],'milk':False,'custom':'パッションティーに変更','notes':'柑橘のすっきりした味が好きな日に。','tags':['さっぱり','フルーティー'],'icon':'🍋','order':'アイスのゆず シトラス & ティーをパッションティーに変更でお願いします。'},
 {'id':'vanilla','name':'バニラ クリーム フラペチーノ','kind':'no-coffee','temps':['ice'],'sweet':'sweet','moods':['treat'],'milk':True,'custom':'チョコレートソース追加','notes':'デザート感のある甘いドリンクでひと休み。','tags':['フラペチーノ','甘党'],'icon':'🍨','order':'バニラ クリーム フラペチーノにチョコレートソース追加でお願いします。'},
 {'id':'hojicha','name':'ほうじ茶 ティー ラテ','kind':'tea','temps':['hot'],'sweet':'low','moods':['relax','light'],'milk':True,'custom':'オールミルク（お湯なし）','notes':'ほうじ茶の香ばしさでほっと落ち着きたいとき。','tags':['香ばしい','ティー'],'icon':'🫖','order':'ホットのほうじ茶 ティー ラテをオールミルクでお願いします。'},
 {'id':'moca','name':'カフェ モカ','kind':'coffee','temps':['ice','hot'],'sweet':'sweet','moods':['treat','relax'],'milk':True,'custom':'チョコレートソース追加（提供可否は要確認）','notes':'チョコレートの甘さとコーヒーの苦みの組み合わせ。','tags':['チョコ','コーヒー'],'icon':'🍫','order':'カフェ モカを、可能であればチョコレートソース追加でお願いします。'},
 {'id':'chai','name':'チャイ ティー ラテ','kind':'tea','temps':['ice','hot'],'sweet':'sweet','moods':['relax','treat'],'milk':True,'custom':'オーツミルクに変更','notes':'スパイスの香りと甘みを楽しみたい日に。','tags':['スパイス','ミルク'],'icon':'🧡','order':'チャイ ティー ラテをオーツミルクに変更でお願いします。'},
 {'id':'passion','name':'アイスティー（パッション）','kind':'tea','temps':['ice'],'sweet':'fresh','moods':['refresh','light'],'milk':False,'custom':'そのまま（カスタムなし）','notes':'軽やかな気分に合う、すっきりしたティー。','tags':['さっぱり','ノンミルク'],'icon':'🌺','order':'アイスティー（パッション）をお願いします。'},
 {'id':'coffee','name':'ドリップ コーヒー','kind':'coffee','temps':['ice','hot'],'sweet':'low','moods':['light','relax'],'milk':False,'custom':'そのまま（カスタムなし）','notes':'コーヒーそのものの味を楽しみたい日に。','tags':['シンプル','甘さなし'],'icon':'☕','order':'ドリップ コーヒーをお願いします。'}
]

# 以前のカスタム企画・会話で挙がったレシピ案。実投稿の確定リストではありません。
CUSTOM_RECIPES = [
 {'id': 'matcha-white', 'name': '抹茶 クリーム フラペチーノ', 'kind': 'no-coffee', 'temps': ['ice'], 'sweet': 'sweet', 'moods': ['treat'], 'milk': True, 'custom': 'ホワイトモカシロップへの変更・チョコチップ追加・抹茶パウダー多め・ホイップ多め', 'notes': '抹茶の苦みとホワイトチョコ風の甘さを楽しみたい人向け。', 'tags': ['ホワイトモカ風のチョコ抹茶', '過去の企画案'], 'icon': '🍵', 'order': '抹茶 クリーム フラペチーノを、ホワイトモカシロップへの変更・チョコチップ追加・抹茶パウダー多め・ホイップ多めでお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'dark-choco', 'name': 'ダーク モカ チップ フラペチーノ', 'kind': 'coffee', 'temps': ['ice'], 'sweet': 'sweet', 'moods': ['treat'], 'milk': True, 'custom': 'チョコレートソース追加・チョコチップ多め・ホイップ多め', 'notes': 'チョコの存在感を楽しみたい日に。', 'tags': ['濃厚チョコ尽くし', '過去の企画案'], 'icon': '🍫', 'order': 'ダーク モカ チップ フラペチーノを、チョコレートソース追加・チョコチップ多め・ホイップ多めでお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'dark-opera', 'name': 'ダーク モカ チップ フラペチーノ', 'kind': 'coffee', 'temps': ['ice'], 'sweet': 'sweet', 'moods': ['treat'], 'milk': True, 'custom': 'エスプレッソショット追加・チョコチップ追加・チョコレートソース追加', 'notes': 'コーヒーのほろ苦さとチョコの組み合わせ。', 'tags': ['オペラ風アレンジ', '過去の企画案'], 'icon': '🍰', 'order': 'ダーク モカ チップ フラペチーノを、エスプレッソショット追加・チョコチップ追加・チョコレートソース追加でお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'vanilla-cookie', 'name': 'バニラ クリーム フラペチーノ', 'kind': 'no-coffee', 'temps': ['ice'], 'sweet': 'sweet', 'moods': ['treat'], 'milk': True, 'custom': 'チョコチップ追加・チョコレートソース追加・ホイップ多め', 'notes': 'チョコ入りバニラデザートのような一杯。', 'tags': ['クッキー風チョコバニラ', '過去の企画案'], 'icon': '🍪', 'order': 'バニラ クリーム フラペチーノを、チョコチップ追加・チョコレートソース追加・ホイップ多めでお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'caramel-rich', 'name': 'キャラメル フラペチーノ', 'kind': 'coffee', 'temps': ['ice'], 'sweet': 'sweet', 'moods': ['treat'], 'milk': True, 'custom': 'キャラメルソース多め・ホイップ多め・シナモン追加', 'notes': 'キャラメルの香りをしっかり楽しみたい日に。', 'tags': ['キャラメルたっぷり', '過去の企画案'], 'icon': '🍮', 'order': 'キャラメル フラペチーノを、キャラメルソース多め・ホイップ多め・シナモン追加でお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'coffee-chip', 'name': 'コーヒー フラペチーノ', 'kind': 'coffee', 'temps': ['ice'], 'sweet': 'sweet', 'moods': ['treat'], 'milk': True, 'custom': 'エスプレッソショット追加・チョコチップ追加・ホイップ追加・チョコレートソース追加', 'notes': 'コーヒー感のあるデザート系アレンジ。', 'tags': ['チョコチップコーヒー', '過去の企画案'], 'icon': '☕', 'order': 'コーヒー フラペチーノを、エスプレッソショット追加・チョコチップ追加・ホイップ追加・チョコレートソース追加でお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'hojicha-caramel', 'name': 'ほうじ茶 & クラシックティー ラテ', 'kind': 'tea', 'temps': ['ice'], 'sweet': 'sweet', 'moods': ['relax'], 'milk': True, 'custom': 'キャラメルソース追加', 'notes': '香ばしいほうじ茶にキャラメルの甘さをプラス。', 'tags': ['ほうじ茶キャラメル', '過去の企画案'], 'icon': '🫖', 'order': 'ほうじ茶 & クラシックティー ラテを、キャラメルソース追加でお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'hojicha-white', 'name': 'ほうじ茶 & クラシックティー ラテ', 'kind': 'tea', 'temps': ['ice'], 'sweet': 'sweet', 'moods': ['treat'], 'milk': True, 'custom': 'ホワイトモカシロップ追加・ホイップ追加', 'notes': 'ほうじ茶をデザート感覚で味わいたいときに。', 'tags': ['ほうじ茶ホワイトモカ風', '過去の企画案'], 'icon': '🫖', 'order': 'ほうじ茶 & クラシックティー ラテを、ホワイトモカシロップ追加・ホイップ追加でお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'matcha-rich', 'name': '抹茶 ティー ラテ', 'kind': 'tea', 'temps': ['hot'], 'sweet': 'sweet', 'moods': ['relax'], 'milk': True, 'custom': '抹茶パウダー多め・ミルク多め（対応可否は店舗確認）', 'notes': '抹茶の風味を濃く楽しむアレンジ。', 'tags': ['抹茶濃いめ', '過去の企画案'], 'icon': '🍵', 'order': '抹茶 ティー ラテを、抹茶パウダー多め・ミルク多め（対応可否は店舗確認）でお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'matcha-shot', 'name': '抹茶 ティー ラテ', 'kind': 'tea', 'temps': ['hot'], 'sweet': 'low', 'moods': ['relax'], 'milk': True, 'custom': '抹茶パウダー多め・エスプレッソショット追加', 'notes': '甘さよりも苦みや香りを楽しみたい方向け。', 'tags': ['大人の抹茶ショット', '過去の企画案'], 'icon': '🍵', 'order': '抹茶 ティー ラテを、抹茶パウダー多め・エスプレッソショット追加でお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'white-cinnamon', 'name': 'ホワイト モカ', 'kind': 'coffee', 'temps': ['hot'], 'sweet': 'sweet', 'moods': ['relax'], 'milk': True, 'custom': 'シナモン追加・ホイップ多め', 'notes': '甘いミルクコーヒーにスパイスの香り。', 'tags': ['ホワイトモカシナモン', '過去の企画案'], 'icon': '🤍', 'order': 'ホワイト モカを、シナモン追加・ホイップ多めでお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'chai-cinnamon', 'name': 'チャイ ティー ラテ', 'kind': 'tea', 'temps': ['hot'], 'sweet': 'sweet', 'moods': ['relax'], 'milk': True, 'custom': 'シナモン追加・ホイップ追加', 'notes': 'スパイス好きのご褒美ティー。', 'tags': ['スパイス香るチャイ', '過去の企画案'], 'icon': '🧡', 'order': 'チャイ ティー ラテを、シナモン追加・ホイップ追加でお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'yuzu-honey', 'name': 'ゆず シトラス & ティー', 'kind': 'tea', 'temps': ['ice'], 'sweet': 'fresh', 'moods': ['refresh'], 'milk': True, 'custom': 'パッションティーに変更・はちみつ追加（提供方法は店舗確認）', 'notes': '柑橘と酸味を爽やかに楽しむアレンジ。', 'tags': ['はちみつシトラス', '過去の企画案'], 'icon': '🍋', 'order': 'ゆず シトラス & ティーを、パッションティーに変更・はちみつ追加（提供方法は店舗確認）でお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'yuzu-extra', 'name': 'ゆず シトラス & ティー', 'kind': 'tea', 'temps': ['ice'], 'sweet': 'fresh', 'moods': ['refresh'], 'milk': True, 'custom': 'シトラス果肉追加・氷少なめ', 'notes': '果肉感を楽しみたい人向け。', 'tags': ['ゆず果肉たっぷり', '過去の企画案'], 'icon': '🍊', 'order': 'ゆず シトラス & ティーを、シトラス果肉追加・氷少なめでお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
 {'id': 'mango-fruit', 'name': 'マンゴー パッション ティー フラペチーノ', 'kind': 'no-coffee', 'temps': ['ice'], 'sweet': 'fresh', 'moods': ['refresh'], 'milk': True, 'custom': 'パッションティー抜き（対応可否は店舗確認）', 'notes': 'マンゴーの甘さを主役にしたい日に。', 'tags': ['濃厚マンゴー', '過去の企画案'], 'icon': '🥭', 'order': 'マンゴー パッション ティー フラペチーノを、パッションティー抜き（対応可否は店舗確認）でお願いします。', 'source': '過去の投稿企画・相談', 'verification': '掲載カスタムや取り扱いは公式メニュー・店舗で確認してください'},
]
DRINKS.extend(CUSTOM_RECIPES)


# 追加の組み合わせ案。店頭・公式サイトでカスタム可能か確認できるまでは公開用の確定レシピとしない。
IDEA_VARIANTS = [('latte', 'オーツミルクに変更', 'まろやかオーツラテ'), ('latte', 'エスプレッソショット追加', 'コーヒー濃いめラテ'), ('latte', 'バニラシロップ追加', 'バニララテ風'), ('latte', 'キャラメルソース追加', 'キャラメルラテ風'), ('caramel', 'エスプレッソショット追加', 'ビターキャラメル'), ('caramel', 'オーツミルクに変更', 'オーツキャラメル'), ('caramel', 'キャラメルソース多め・ホイップ追加', 'デザートキャラメル'), ('matcha', '抹茶パウダー多め', '抹茶しっかり'), ('matcha', 'ホワイトモカシロップ追加', 'ホワイト抹茶'), ('matcha', '無脂肪乳に変更', 'すっきり抹茶'), ('yuzu', 'シトラス果肉少なめ', '果肉控えめシトラス'), ('yuzu', '氷少なめ', 'ゆず氷少なめ'), ('vanilla', 'チョコチップ追加', 'バニラチョコチップ'), ('vanilla', 'ホワイトモカシロップ追加', 'ホワイトバニラ'), ('vanilla', 'キャラメルソース追加', 'キャラメルバニラ'), ('hojicha', 'オーツミルクに変更', 'オーツほうじ茶'), ('hojicha', 'ホワイトモカシロップ追加', '甘めほうじ茶'), ('moca', '無脂肪乳に変更', 'すっきりカフェモカ'), ('moca', 'エスプレッソショット追加', '濃厚ビターモカ'), ('chai', 'シナモン追加', 'シナモンチャイ'), ('chai', '無脂肪乳に変更', '軽めチャイ'), ('passion', '氷少なめ', 'すっきりパッション'), ('coffee', 'エスプレッソショット追加', 'コーヒー好き向け'), ('coffee', 'ミルク追加', 'マイルドコーヒー'), ('matcha-white', 'チョコレートソース追加・抹茶パウダー多め', 'チョコ抹茶'), ('dark-choco', 'チョコレートソース多め', '追いチョコ'), ('vanilla-cookie', 'キャラメルソース追加・チョコチップ追加', 'キャラメルクッキー風'), ('yuzu-extra', 'シトラス果肉少なめ・氷少なめ', 'ゆず軽め'), ('white-cinnamon', 'オーツミルクに変更', 'オーツホワイトモカ'), ('caramel-rich', 'チョコレートソース追加', 'チョコキャラメル'), ('mango-fruit', 'シトラス果肉追加', 'マンゴーシトラス風'), ('matcha-rich', 'オーツミルクに変更', '香ばし抹茶')]
base_by_id={d['id']:d for d in DRINKS}
for i,(base_id,custom,label) in enumerate(IDEA_VARIANTS,1):
    d=base_by_id[base_id].copy()
    d.update(id=f'idea-{i:02d}', custom=custom,
        notes=f'{label}をイメージしたカスタム案。対応可否は店舗で確認してください。',
        tags=[label,'新しい組み合わせ案'], source='組み合わせの新規提案',
        verification='未検証：注文可否・料金・栄養情報を確認してください',
        order=f"{d['name']}を、{custom}でお願いできますか？")
    DRINKS.append(d)

# データ管理：正確な価格・カロリーを確認できたレシピだけ数値を入れる。
# 例: VERIFIED_DATA = {'latte': {'price_yen': 000, 'calories_kcal': 000, 'extra_fee_yen': 0}}
# ※未確認の数値は None のままにし、ユーザーに推定値を見せない。
VERIFIED_DATA = {}
for d in DRINKS:
    d['price_yen']=VERIFIED_DATA.get(d['id'],{}).get('price_yen')
    d['calories_kcal']=VERIFIED_DATA.get(d['id'],{}).get('calories_kcal')
    d['extra_fee_yen']=VERIFIED_DATA.get(d['id'],{}).get('extra_fee_yen')
    d['status']='確認待ち' if not VERIFIED_DATA.get(d['id']) else '数値確認済み'

ALLOWED = {'temp':{'ice','hot'},'sweet':{'sweet','low','fresh'},'kind':{'any','coffee','tea','no-coffee'},'mood':{'treat','refresh','relax','light'}}

def recommend_drinks(preferences):
    p = {k:v if v in ALLOWED[k] else ('any' if k=='kind' else next(iter(sorted(ALLOWED[k])))) for k,v in preferences.items() if k in ALLOWED}
    temp = p.get('temp','ice')
    kind = p.get('kind','any')
    options = [d for d in DRINKS if temp in d['temps']]
    # A chosen family is a firm preference when matching options exist.
    family = [d for d in options if d['kind']==kind]
    if kind != 'any' and family: options=family
    def score(d):
        return (6 if d['sweet']==p.get('sweet') else 0) + (4 if p.get('mood') in d['moods'] else 0) + (2 if kind != 'any' and d['kind']==kind else 0)
    ranked=sorted(options,key=lambda d:(-score(d), d['name']))[:3]
    return [dict(d,score=score(d),match=('好みにぴったり' if score(d)>=10 else '近いおすすめ')) for d in ranked]

@app.get('/')
def home():
    return render_template('index.html')

@app.post('/api/recommend')
def recommend():
    payload=request.get_json(silent=True)
    if not isinstance(payload,dict): return jsonify({'error':'回答を読み取れませんでした'}),400
    return jsonify(recommend_drinks(payload))

@app.get('/api/drinks')
def drinks():
    return jsonify(DRINKS)

if __name__ == '__main__':
    app.run(debug=True)
