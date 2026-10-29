"""Function-based proposals. A proposal is not a verified historical coinage.

We preserve complete words and established concept boundaries. Missing words
are reported, not manufactured from English letter names or language prefixes.
"""
import json
import importlib.util
from pathlib import Path
import unicodedata
import keyword
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
RESERVED = set(keyword.kwlist) | set('''abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null auto extern register signed sizeof struct typedef union unsigned inline restrict _Alignas _Alignof _Atomic _Bool _Complex _Generic _Imaginary _Noreturn _Static_assert _Thread_local alignas alignof asm bool constexpr const_cast decltype delete dynamic_cast explicit export false friend mutable namespace noexcept nullptr operator reinterpret_cast static_assert static_cast template thread_local true typeid typename using virtual wchar_t'''.split())


@lru_cache(maxsize=8)
def frozen_json(relative):
    """Use one dictionary snapshot throughout a generation/audit invocation."""
    return json.loads((ROOT/relative).read_text())

# Match the meaning in the current kernel, not unrelated gettext homonyms.
CONCEPTS = {
    '동작':'action','주소':'address','인수':'arguments','단추':'button','닫기':'close',
    '명령':'command','연결':'connect','현재값':'current','자료':'data','전문':'datagram',
    '오류':'error','사건':'event','예외':'exception','실행하기':'execute','파일':'file',
    '초기화':'initialize','글표지':'label','줄':'line','불러오기':'load','이름':'name',
    '열기':'open','출력':'output','경로':'path','위치':'position','실행과정':'process',
    '읽기':'read','결과':'result','시작':'run','저장하기':'save','설정':'settings',
    '크기':'size','원문':'source','중지':'stop','터미널':'terminal','글':'text',
    '창':'window','작업가닥':'worker','쓰기':'write',
}

# Whole-role proposals for the kernel and public example API.
KEYS = '핵심 보드 단말 명령해석기 기억파일 되돌림망 흐름통신 줄편집 화면마당 셸입출력 사용자 자바가상기계 도구시작 자바컴파일러 자바도구 꾸러미 예제꾸러미 한국어 자체 출력예제 파일예제 네트워크예제 그래픽예제 창예제 예제규약 출력 줄쓰기 수쓰기 파일읽기 파일쓰기 파일지우기 글길이 길이 값 수 번호 조건 확인 검사 참인지 문자 정수읽기 바이트수 부호화 입력흐름 출력흐름 연결통로 전문통로 대기시간 보내기 받기 입력 종단 보낼글 실행인수 입력칸 화면일정 실행할일 동작받이 동작알림 나중에실행 실행하기 동작받기 알림 명령글 글읽기 글쓰기 자리정하기 담기 보이기 살아있는가 기다리기 시작하기 양보하기 사각형 화면 인사창 이름입력 인사말 인사횟수 창열기 인사하기 운영체제 실행환경 자신 함수 기존인수 사이 끝 글부호화 글해독 명령인수 운영체제오류 운영호출 설명 전문통신열기 전문보내기 바깥전문보내기 전문받기 통신닫기 네모그리기 화면크기 그림기다리기 밀리초'.split()
ROWS = {
 'en':'Kernel|Board|TerminalIO|CommandInterpreter|MemoryFiles|LoopbackNetwork|StreamNetwork|LineEditor|Desktop|ShellIO|User|JavaMachine|ToolEntry|JavaCompiler|JavaTools|Bundle|ExampleBundle|English|Native|OutputExample|FileExample|NetworkExample|GraphicsExample|WindowExample|ExampleABI|Output|writeLine|writeNumber|readFile|writeFile|removeFile|textLength|lengthValue|value|number|index|condition|verify|Checks|require|Characters|parseInteger|byteCount|encode|InputStream|OutputStream|Connection|DatagramChannel|timeout|send|receive|inputValue|endpoint|message|Arguments|TextField|EventQueue|RunnableTask|ActionReceiver|ActionNotice|invokeLater|executeTask|receiveAction|notice|commandText|readText|writeText|setBounds|addElement|showWindow|isAlive|await|startTask|yieldTask|rectangle|Screen|greetingWindow|nameField|greeting|greetingCount|openWindow|greet|OperatingSystem|Runtime|selfValue|functionValue|legacyArguments|separator|ending|encodeText|decodeText|commandArguments|SystemError|invokeSystem|description|openDatagram|sendDatagram|sendExternalDatagram|receiveDatagram|closeNetwork|drawRectangle|screenSize|waitForDrawing|milliseconds',
 'ja':'中核|基板|端末入出力|命令解釈器|記憶内文書|折返し通信網|流れ通信|行編集器|画面広場|命令入出力|利用者|ジャバ仮想機械|道具入口|ジャバ翻訳器|ジャバ道具|包み|用例集|日本語|自前|出力例|文書例|通信例|描画例|窓例|用例規約|出力|一行書く|数を書く|文書を読む|文書に書く|文書を消す|文字数|長さ|値|数|番号|条件|確かめる|検査|真を確かめる|文字|整数を読む|バイト数|符号化|入力の流れ|出力の流れ|接続路|電文路|待ち時間|送る|受け取る|入力|終端|送る文|実行引数|入力欄|画面予定|実行する仕事|動作受け手|動作通知|後で実行|実行する|動作を受ける|通知|命令文|文字を読む|文字を書く|位置を決める|加える|表示する|動作中か|待つ|動かす|譲る|長方形|画面|挨拶窓|名前入力|挨拶文|挨拶回数|窓を開く|挨拶する|基本ソフト|実行環境|自身|関数|従来の引数|区切り|末尾|文字を符号化|文字を復号|命令引数|基本ソフトの誤り|基本機能を呼ぶ|説明|電文路を開く|電文を送る|外へ電文を送る|電文を受ける|通信を閉じる|長方形を描く|画面の大きさ|描画を待つ|ミリ秒',
 'zh_Hans':'内核|主板|终端输入输出|命令解释器|内存文件|回环网络|流通信|行编辑器|桌面|命令输入输出|用户|爪哇虚拟机|工具入口|爪哇编译器|爪哇工具|包裹|示例集|中文|自有|输出示例|文件示例|网络示例|绘图示例|窗口示例|示例约定|输出|写行|写数|读取文件|写入文件|删除文件|文本长度|长度|值|数|编号|条件|确认|检查|确认真值|字符|读取整数|字节数|编码|输入流|输出流|连接通道|报文通道|等待时间|发送|接收|输入|端点|待发文本|运行参数|输入框|画面调度|可执行任务|动作接收器|动作通知|稍后执行|执行任务|接收动作|通知|命令文本|读取文本|写入文本|设置位置|添加元素|显示|仍在运行|等待|启动任务|让行|矩形|屏幕|问候窗口|姓名输入|问候语|问候次数|打开窗口|问候|操作系统|运行环境|自身|函数|已有参数|分隔|末尾|文本编码|文本解码|命令参数|系统错误|系统调用|说明|打开报文通道|发送报文|发送外部报文|接收报文|关闭通信|绘制矩形|屏幕大小|等待绘图|毫秒',
}

EXAMPLE_KEYS='한국어 자체 출력예제 파일예제 네트워크예제 그래픽예제 창예제'.split()
EXAMPLES={
 'fr':'français|natif|ExempleSortie|ExempleFichier|ExempleRéseau|ExempleDessin|ExempleFenêtre',
 'de':'Deutsch|Eigen|Ausgabebeispiel|Dateibeispiel|Netzbeispiel|Zeichenbeispiel|Fensterbeispiel',
 'es':'español|propio|EjemploSalida|EjemploArchivo|EjemploRed|EjemploDibujo|EjemploVentana',
 'pt':'português|nativo|ExemploSaída|ExemploFicheiro|ExemploRede|ExemploDesenho|ExemploJanela',
 'it':'italiano|nativo|EsempioUscita|EsempioFile|EsempioRete|EsempioDisegno|EsempioFinestra',
 'ru':'русский|свой|ПримерВывода|ПримерФайла|ПримерСети|ПримерРисования|ПримерОкна',
 'uk':'українська|своє|ПрикладВиводу|ПрикладФайлу|ПрикладМережі|ПрикладМалювання|ПрикладВікна',
 'ar':'عربي|ذاتي|مثالطباعة|مثالملف|مثالشبكة|مثالرسم|مثالنافذة',
 'he':'עברית|עצמי|דוגמתפלט|דוגמתקובץ|דוגמתרשת|דוגמתציור|דוגמתחלון',
 'hi':'हिंदी|निज|लेखनउदाहरण|संचिकाउदाहरण|जालउदाहरण|चित्रउदाहरण|खिड़कीउदाहरण',
 'bn':'বাংলা|নিজ|মুদ্রণনমুনা|ফাইলনমুনা|নেটওয়ার্ক|অঙ্কননমুনা|জানালানমুনা',
 'ne':'नेपाली|निज|लेखनउदाहरण|फाइलउदाहरण|सञ्जालउदाहरण|चित्रउदाहरण|झ्यालउदाहरण',
 'tr':'Türkçe|Öz|ÇıktıÖrneği|DosyaÖrneği|AğÖrneği|ÇizimÖrneği|PencereÖrneği',
 'vi':'TiếngViệt|Riêng|VíDụXuất|VíDụTệp|VíDụMạng|VíDụVẽ|VíDụCửaSổ',
 'th':'ไทย|เอง|พิมพ์|แฟ้ม|เครือข่าย|วาดภาพ|หน้าต่าง',
 'id':'Indonesia|Asli|ContohKeluaran|ContohBerkas|ContohJaringan|ContohGambar|ContohJendela',
 'ms_Latn':'Melayu|Asli|ContohKeluaran|ContohFail|ContohRangkaian|ContohLukisan|ContohTetingkap',
 'nl':'Nederlands|Eigen|Uitvoervoorbeeld|Bestandsvoorbeeld|Netwerkvoorbeeld|Tekenvoorbeeld|Venstervoorbeeld',
 'pl':'polski|własny|PrzykładWyjścia|PrzykładPliku|PrzykładSieci|PrzykładRysunku|PrzykładOkna',
 'sv':'svenska|eget|Utdataexempel|Filexempel|Nätverksexempel|Ritexempel|Fönsterexempel',
 'fi':'suomi|oma|Tulostusesimerkki|Tiedostoesimerkki|Verkkoesimerkki|Piirtoesimerkki|Ikkunaesimerkki',
 'da':'dansk|eget|Uddataeksempel|Fileksempel|Netværkseksempel|Tegneeksempel|Vindueseksempel',
 'nb':'norsk|eget|Utdataeksempel|Fileksempel|Nettverkseksempel|Tegneeksempel|Vinduseksempel',
 'cs':'čeština|vlastní|UkázkaVýstupu|UkázkaSouboru|UkázkaSítě|UkázkaKreslení|UkázkaOkna',
 'sk':'slovenčina|vlastné|UkážkaVýstupu|UkážkaSúboru|UkážkaSiete|UkážkaKreslenia|UkážkaOkna',
 'hu':'magyar|saját|KimenetiPélda|FájlPélda|HálózatiPélda|RajzPélda|AblakPélda',
 'ro':'română|propriu|ExempluIeșire|ExempluFișier|ExempluRețea|ExempluDesen|ExempluFereastră',
 'el':'ελληνικά|ίδιο|ΠαράδειγμαΕξόδου|ΠαράδειγμαΑρχείου|ΠαράδειγμαΔικτύου|ΠαράδειγμαΣχεδίου|ΠαράδειγμαΠαραθύρου',
 'fa':'فارسی|بومی|نمونهچاپ|نمونهپرونده|نمونهشبکه|نمونهنقاشی|نمونهپنجره',
 'ur':'اردو|اپنا|چھپائیمثال|فائلمثال|نیٹورکمثال|تصویرمثال|کھڑکیمثال',
 'zh_Hant':'中文|自有|輸出範例|檔案範例|網路範例|繪圖範例|視窗範例',
 'ca':'català|propi|ExempleSortida|ExempleFitxer|ExempleXarxa|ExempleDibuix|ExempleFinestra',
 'et':'eesti|oma|VäljundiNäide|FailiNäide|VõrguNäide|JooniseNäide|AknaNäide',
 'hr':'hrvatski|vlastiti|PrimjerIspisa|PrimjerDatoteke|PrimjerMreže|PrimjerCrtanja|PrimjerProzora',
 'sl':'slovenščina|lastno|PrimerIzpisa|PrimerDatoteke|PrimerOmrežja|PrimerRisanja|PrimerOkna',
 'is':'íslenska|eigin|Úttaksdæmi|Skráardæmi|Netdæmi|Teiknidæmi|Gluggadæmi',
 'lt':'lietuvių|savas|IšvestiesPavyzdys|FailoPavyzdys|TinkloPavyzdys|PiešimoPavyzdys|LangoPavyzdys',
 'lv':'latviešu|savs|IzvadesPiemērs|DatnesPiemērs|TīklaPiemērs|ZīmējumaPiemērs|LogaPiemērs',
}

ABI_KEYS='같음 입출력예외 내용비우기 다시시도오류 망차례정수 망차례짧은수 받은수 없으면만들기 오류번호 응답 인수수 인터넷주소 인터넷주소갈래 인터넷통신주소 읽고쓰기 읽은글 자료전문받기 자료전문보내기 자체예제규약머리 전문전송규약 전문통신 접속번호 주소갈래 주소값 창구 처음기준 통신규약 통신종단점만들기 통신주소 통신주소묶기 파일규약 파일닫기 파일열기 파일위치옮기기 파일자료쓰기 파일자료읽기 화면규약 정수 화면구성요소 동작맡기기 일어난곳 보이는가 사건처리중인가'.split()
ABI_ROWS={
 'en':'equalText|InputOutputException|TruncateContents|TryAgainError|networkInteger|networkShort|receivedCount|CreateIfMissing|errorNumber|reply|argumentCount|InternetAddress|InternetFamily|InternetSocketAddress|ReadWrite|readTextValue|receiveDatagramData|sendDatagramData|NativeExampleHeader|DatagramProtocol|DatagramSocket|portNumber|addressFamily|addressValue|portValue|FromBeginning|NetworkABI|createEndpoint|SocketAddress|bindAddress|FileABI|closeFile|openFile|seekFile|writeFileData|readFileData|ScreenABI|Integer|ScreenElement|setActionReceiver|eventSource|isVisible|isEventDispatching',
 'ja':'同じ文字列|入出力例外|内容を空にする|再試行の誤り|網順序の整数|網順序の短整数|受信数|無ければ作る|誤り番号|返答|引数の数|インターネット番地|インターネット族|インターネット端点番地|読書両用|読んだ文|電文資料を受ける|電文資料を送る|自前用例宣言|電文転送規約|電文通信|接続番号|番地の族|番地値|通信口|先頭基準|通信規約|通信端点を作る|通信番地|通信番地を結ぶ|文書規約|文書を閉じる|文書を開く|文書位置を移す|文書資料を書く|文書資料を読む|画面規約|整数|画面構成要素|動作を任せる|発生元|表示中か|事件処理中か',
 'zh_Hans':'文本相同|输入输出异常|清空内容|重试错误|网络序整数|网络序短整数|接收数量|不存在则创建|错误编号|应答|参数数量|互联网地址|互联网地址族|互联网通信地址|读写|已读文本|接收报文数据|发送报文数据|自有示例声明|报文传输协议|报文通信|连接编号|地址族|地址值|端口|起始位置|通信约定|创建通信端点|通信地址|绑定通信地址|文件约定|关闭文件|打开文件|移动文件位置|写文件数据|读文件数据|屏幕约定|整数|屏幕元素|设置动作接收器|事件来源|是否显示|是否正在处理事件',
}

HELP = {
 'ko':'F9 또는 Shift+Space를 누르면 한국어 두벌식 입력으로 전환합니다.',
 'ja':'F9 または Shift+Space で日本語入力に切り替わります。',
 'zh_Hans':'按 F9 或 Shift+Space 可切换到中文拼音输入。',
 'zh':'按 F9 或 Shift+Space 可切换到中文拼音输入。',
 'zh_Hant':'按 F9 或 Shift+Space 可切換到中文拼音輸入。',
 'en':'Press F9 or Shift+Space to switch to the English keyboard.',
 'de':'F9 oder Shift+Space schaltet zur deutschen Tastatur um.',
 'fr':'F9 ou Shift+Space active la saisie en français.',
 'es':'F9 o Shift+Space activa la escritura en español.',
 'pt':'F9 ou Shift+Space ativa a escrita em português.',
 'it':'F9 o Shift+Space attiva la scrittura in italiano.',
 'ru':'F9 или Shift+Space включает ввод на русском языке.',
 'uk':'F9 або Shift+Space вмикає введення українською мовою.',
 'ar':'اضغط F9 أو Shift+Space للتبديل إلى الكتابة بالعربية.',
 'he':'לחצו F9 או Shift+Space כדי לעבור להקלדה בעברית.',
 'hi':'F9 या Shift+Space दबाने पर हिन्दी में लिख सकते हैं।',
 'bn':'F9 অথবা Shift+Space চাপলে বাংলায় লেখা যাবে।',
 'ne':'F9 वा Shift+Space थिच्दा नेपालीमा लेख्न सकिन्छ।',
 'tr':'F9 veya Shift+Space ile Türkçe girişe geçebilirsiniz.',
 'vi':'Nhấn F9 hoặc Shift+Space để chuyển sang nhập tiếng Việt.',
 'th':'กด F9 หรือ Shift+Space เพื่อเปลี่ยนเป็นการพิมพ์ภาษาไทย',
 'id':'Tekan F9 atau Shift+Space untuk mengetik dalam bahasa Indonesia.',
 'ms_Latn':'Tekan F9 atau Shift+Space untuk menaip dalam bahasa Melayu.',
 'nl':'Met F9 of Shift+Space schakelt u over naar Nederlands typen.',
 'pl':'F9 lub Shift+Space przełącza na pisanie po polsku.',
 'sv':'F9 eller Shift+Space växlar till svensk inmatning.',
 'fi':'F9 tai Shift+Space vaihtaa suomenkieliseen näppäimistöön.',
 'da':'F9 eller Shift+Space skifter til dansk indtastning.',
 'nb':'F9 eller Shift+Space bytter til norsk inntasting.',
 'cs':'F9 nebo Shift+Space přepne na české zadávání.',
 'sk':'F9 alebo Shift+Space prepne na slovenské zadávanie.',
 'hu':'Az F9 vagy a Shift+Space magyar bevitelre vált.',
 'ro':'F9 sau Shift+Space activează introducerea în limba română.',
 'el':'Πατήστε F9 ή Shift+Space για πληκτρολόγηση στα ελληνικά.',
 'fa':'با F9 یا Shift+Space به نوشتن فارسی بروید.',
 'ur':'اردو میں لکھنے کے لیے F9 یا Shift+Space دبائیں۔',
}
GREETINGS = {'ko':'안녕하세요','ja':'こんにちは','zh_Hans':'你好','zh_Hant':'您好','en':'Hello','de':'Guten Tag','fr':'Bonjour','es':'Hola','pt':'Olá','it':'Ciao','ru':'Здравствуйте','uk':'Вітаю','ar':'مرحبا','he':'שלום','hi':'नमस्ते','bn':'নমস্কার','ne':'नमस्ते','tr':'Merhaba','vi':'Xin chào','th':'สวัสดี','id':'Halo','ms_Latn':'Selamat datang','nl':'Hallo','pl':'Witaj','sv':'Hej','fi':'Hei','da':'Hej','nb':'Hei','el':'Γεια σας','fa':'سلام','ur':'سلام','am':'ሰላም','ti':'ሰላም','ka':'გამარჯობა','hy':'Բարեւ','my':'မင်္ဂလာပါ','km':'សួស្តី','lo':'ສະບາຍດີ','si':'ආයුබෝවන්'}
LAYOUTS = {'am':('et',''),'ti':('et',''),'ar':('ara',''),'az_Latn':('az','latin'),'be':('by',''),'bg':('bg',''),'bn':('bd',''),'bs_Cyrl':('rs',''),'ca':('es','cat'),'cs':('cz',''),'da':('dk',''),'de':('de',''),'dv':('mv',''),'dz':('bt',''),'el':('gr',''),'es':('es',''),'et':('ee',''),'fa':('ir',''),'fi':('fi',''),'fo':('fo',''),'fr':('fr',''),'gn':('latam',''),'he':('il',''),'hi':('in',''),'hr':('hr',''),'hu':('hu',''),'hy':('am',''),'is':('is',''),'it':('it',''),'ka':('ge',''),'kl':('dk',''),'km':('kh',''),'ky_Cyrl':('kg',''),'lo':('la',''),'lt':('lt',''),'lv':('lv',''),'mk':('mk',''),'mn_Cyrl':('mn',''),'mt':('mt',''),'my':('mm',''),'nb':('no',''),'ne':('np',''),'nl':('nl',''),'pl':('pl',''),'pt':('pt',''),'ro':('ro',''),'ru':('ru',''),'si':('lk',''),'sk':('sk',''),'sl':('si',''),'sq':('al',''),'sr_Cyrl':('rs',''),'sr_Latn':('rs','latin'),'sv':('se',''),'tg_Cyrl':('tj',''),'th':('th',''),'tk_Latn':('tm',''),'tr':('tr',''),'uk':('ua',''),'ur':('pk',''),'uz_Latn':('uz','latin'),'vi':('vn',''),'zh_Hant':('tw','')}


GREETINGS['zh'] = GREETINGS['zh_Hans']


@lru_cache(maxsize=None)
def names(language, include_snapshot=True):
    if language=='ko': return {}
    # Reuse the project's explicit default-script glossary for untagged
    # editions. Explicit alternatives (zh_Hant, ms_Arab, etc.) stay separate.
    alias={'zh':'zh_Hans','ms':'ms_Latn'}.get(language)
    if alias:return dict(names(alias, include_snapshot))
    dictionaries=frozen_json('naming/terms.json')
    code={'zh_Hans':'zh'}.get(language,language)
    terms=dictionaries.get(code,dictionaries.get(code.split('_')[0],{}))
    result={key:terms[concept]['identifier'] for key,concept in CONCEPTS.items() if concept in terms and terms[concept]['status']!='untranslated'}
    # Reuse whole-role proposals from the existing Go edition, never its
    # mechanically split identifier word dictionary (e.g. an unrelated "a").
    source=ROOT/'native/inputs/naming_lexicon.py'
    spec=importlib.util.spec_from_file_location('worldos_lexicon',str(source))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    if language in module.PATHS:
        row=dict(zip(module.PATH_KEYS,module.PATHS[language].split('|')))
        for old,key in {'도구':'tools','부팅':'boot','사용자':'user_space','시험':'tests','포함':'headers','배치':'link_layout'}.items():
            result[old]='_'.join(row[key].split())
    if language in ROWS:
        values=ROWS[language].split('|')
        assert len(values)==len(KEYS),(language,len(values),len(KEYS))
        result.update(zip(KEYS,values))
    if language in EXAMPLES:
        values=EXAMPLES[language].split('|');assert len(values)==len(EXAMPLE_KEYS)
        result.update(zip(EXAMPLE_KEYS,values))
    if language in ABI_ROWS:
        values=ABI_ROWS[language].split('|');assert len(values)==len(ABI_KEYS),(language,len(values),len(ABI_KEYS))
        result.update(zip(ABI_KEYS,values))
    additions = ROOT/'native/inputs/java-migration-terms.json'
    if additions.is_file():
        result.update(frozen_json('native/inputs/java-migration-terms.json').get(language, {}))
    if language=='uk':result['출력']='Вивід'
    if language=='bn':result['출력']='নির্গম'
    # A GUI's current Process and a kernel's numeric current value are
    # different roles. Whole-role overrides avoid recycling unrelated senses.
    reviewed=frozen_json('naming/functional-review.json')
    result.update(reviewed['languages'].get(language,reviewed['languages'].get(code,{})).get('native_roles',{}))
    from country_naming import additions
    # Existing, reviewed role names take precedence. New names are complete
    # source identifiers, not substring translations or English fallbacks.
    for old,new in additions(language).items():
        result.setdefault(old,new)
    # Whole functional names are frozen after collection. Offline builds and
    # distribution never depend on a translation service being reachable.
    snapshot = 'native/inputs/localized-roles/' + language + '.json'
    if include_snapshot and (ROOT / snapshot).is_file():
        result.update(frozen_json(snapshot)['names'])
    # Prevent global name merging; an uncertain second synonym stays unchanged.
    seen=set(); unique={}
    for old,new in result.items():
        # Python normalizes identifiers (including import names) to NFKC.
        # Paths and every language's references must use that same spelling.
        new=unicodedata.normalize('NFKC',new)
        if new in seen or new in {'char','class','int','double','float','long','short','byte','void','auto','default','switch','do','if','else','try','except','self','null','true','false'}:continue
        if new.isidentifier():unique[old]=new;seen.add(new)
    return unique
