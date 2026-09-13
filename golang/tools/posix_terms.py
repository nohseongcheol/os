"""Function-level proposals: current operation takes priority over literal roots.

These are project proposals, not standardized or native-speaker-certified names.
No automatic word-order translation. Missing terms remain explicitly pending.
"""
BASE_FUNCTION_KEYS = ('_exit read write close lseek fork execve getpid getppid getuid geteuid getgid getegid '
 'access chdir getcwd dup dup2 fsync sync isatty brk sbrk waitpid wait open creat fcntl '
 'stat lstat fstat uname htons ntohs htonl ntohl socket bind connect listen accept '
 'getsockname getpeername send recv sendto recvfrom shutdown setsockopt').split()

FUNCTION_ROWS = {
 'ko': '즉시끝내기|읽기|쓰기|닫기|자료위치옮기기|실행과정갈라내기|실행내용바꾸기|실행과정번호얻기|부모실행과정번호얻기|사용자번호얻기|유효사용자번호얻기|무리번호얻기|유효무리번호얻기|접근권한확인하기|작업목록바꾸기|작업목록경로얻기|열린자료참조복제하기|지정번호로열린자료참조복제하기|자료철기록맞추기|모든기록맞추기|단말인지확인하기|동적기억끝정하기|동적기억끝옮기기|지정자식기다리기|자식기다리기|열기|자료철만들기|자료철제어하기|자료철상태|연결자체상태얻기|열린자료철상태얻기|체제정보얻기|통신망순서로16자리바꾸기|기계순서로16자리바꾸기|통신망순서로32자리바꾸기|기계순서로32자리바꾸기|통신끝점만들기|지역주소맺기|상대끝점잇기|연결요청받을준비하기|연결요청받기|지역끝점주소얻기|상대끝점주소얻기|보내기|받기|목적지로보내기|보낸곳과함께받기|통신방향닫기|통신끝점설정하기',
 'ja': '直ちに終了する|読む|書く|閉じる|読み書き位置を移す|実行過程を分岐する|実行内容を置き換える|実行過程番号を得る|親実行過程番号を得る|利用者番号を得る|実効利用者番号を得る|所属組番号を得る|実効所属組番号を得る|利用権限を調べる|作業目録を変える|作業目録の経路を得る|開いた文書の参照を複製する|指定番号に文書参照を複製する|文書の記録を同期する|全ての記録を同期する|端末か調べる|動的記憶の終端を定める|動的記憶の終端を移す|指定した子を待つ|子を待つ|開く|文書を作る|文書を制御する|文書状態|連結自体の状態を得る|開いた文書の状態を得る|体系情報を得る|通信網順に16桁を変える|機械順に16桁を変える|通信網順に32桁を変える|機械順に32桁を変える|通信端点を作る|局所番地を結ぶ|相手端点につなぐ|接続要求に備える|接続要求を受け入れる|局所端点の番地を得る|相手端点の番地を得る|送る|受け取る|宛先に送る|送信元と共に受け取る|通信方向を閉じる|通信端点を設定する',
 'zh_Hans': '立即结束|读取|写入|关闭|移动读写位置|分出子进程|替换执行内容|取得进程编号|取得父进程编号|取得用户编号|取得有效用户编号|取得组编号|取得有效组编号|检查访问权限|切换工作目录|取得工作目录路径|复制打开文件引用|按指定编号复制文件引用|同步文件记录|同步全部记录|检查是否终端|设定动态存储末端|移动动态存储末端|等待指定子进程|等待子进程|打开|创建文件|控制文件|文件状态|取得链接自身状态|取得打开文件状态|取得系统信息|转为网络次序16位|转为主机次序16位|转为网络次序32位|转为主机次序32位|创建通信端点|绑定本地地址|连接对端|准备接收连接|接受连接|取得本地端点地址|取得对端地址|发送|接收|向目的地址发送|接收并取得来源地址|关闭通信方向|设置通信端点选项',
 'zh_Hant': '立即結束|讀取|寫入|關閉|移動讀寫位置|分出子行程|替換執行內容|取得行程編號|取得父行程編號|取得使用者編號|取得有效使用者編號|取得群組編號|取得有效群組編號|檢查存取權限|切換工作目錄|取得工作目錄路徑|複製開啟檔案參照|按指定編號複製檔案參照|同步檔案記錄|同步全部記錄|檢查是否終端|設定動態記憶末端|移動動態記憶末端|等待指定子行程|等待子行程|開啟|建立檔案|控制檔案|檔案狀態|取得連結自身狀態|取得開啟檔案狀態|取得系統資訊|轉為網路次序16位|轉為主機次序16位|轉為網路次序32位|轉為主機次序32位|建立通訊端點|繫結本地位址|連接對端|準備接收連線|接受連線|取得本地端點位址|取得對端位址|傳送|接收|向目的位址傳送|接收並取得來源位址|關閉通訊方向|設定通訊端點選項',
 'de': 'sofort beenden|lesen|schreiben|schließen|Dateiposition verschieben|Prozess verzweigen|Programmbild ersetzen|Prozesskennung ermitteln|Elternprozesskennung ermitteln|Benutzerkennung ermitteln|wirksame Benutzerkennung ermitteln|Gruppenkennung ermitteln|wirksame Gruppenkennung ermitteln|Zugriffsrechte prüfen|Arbeitsverzeichnis wechseln|Arbeitsverzeichnispfad ermitteln|offenen Dateiverweis duplizieren|Dateiverweis auf Kennung duplizieren|Dateidaten synchronisieren|alle Dateidaten synchronisieren|Terminal prüfen|Speicherende setzen|Speicherende verschieben|bestimmtes Kind abwarten|Kind abwarten|öffnen|Datei anlegen|Dateizugriff steuern|Dateizustand|Verknüpfungszustand ermitteln|Zustand offener Datei ermitteln|Systeminformationen ermitteln|16 Bit in Netzreihenfolge|16 Bit in Rechnerreihenfolge|32 Bit in Netzreihenfolge|32 Bit in Rechnerreihenfolge|Kommunikationsendpunkt anlegen|lokale Adresse zuordnen|Gegenstelle verbinden|Verbindungsannahme vorbereiten|Verbindung annehmen|lokale Endpunktadresse ermitteln|Gegenstellenadresse ermitteln|senden|empfangen|an Zieladresse senden|mit Absenderadresse empfangen|Übertragungsrichtung schließen|Endpunktoption setzen',
 'fr': 'terminer immédiatement|lire|écrire|fermer|déplacer la position de fichier|dédoubler le processus|remplacer le programme exécuté|obtenir identifiant du processus|obtenir identifiant du parent|obtenir identifiant utilisateur|obtenir identifiant utilisateur effectif|obtenir identifiant du groupe|obtenir identifiant du groupe effectif|vérifier les droits accès|changer le répertoire courant|obtenir le chemin du répertoire courant|dupliquer la référence de fichier ouvert|dupliquer la référence vers un numéro|synchroniser les données du fichier|synchroniser toutes les données|vérifier si terminal|fixer la fin de mémoire dynamique|déplacer la fin de mémoire dynamique|attendre un enfant désigné|attendre un enfant|ouvrir|créer un fichier|contrôler le fichier|état du fichier|obtenir état du lien même|obtenir état du fichier ouvert|obtenir informations du système|convertir 16 bits vers ordre réseau|convertir 16 bits vers ordre machine|convertir 32 bits vers ordre réseau|convertir 32 bits vers ordre machine|créer un point de communication|associer une adresse locale|connecter au correspondant|préparer accueil des connexions|accepter une connexion|obtenir adresse locale|obtenir adresse du correspondant|envoyer|recevoir|envoyer vers une adresse|recevoir avec adresse source|fermer un sens de communication|régler une option du point',
 'es': 'terminar inmediatamente|leer|escribir|cerrar|mover posición del archivo|bifurcar proceso|sustituir programa en ejecución|obtener identificador de proceso|obtener identificador del padre|obtener identificador de usuario|obtener identificador efectivo de usuario|obtener identificador de grupo|obtener identificador efectivo de grupo|comprobar permisos de acceso|cambiar directorio de trabajo|obtener ruta del directorio de trabajo|duplicar referencia de archivo abierto|duplicar referencia al número indicado|sincronizar datos del archivo|sincronizar todos los datos|comprobar si es terminal|fijar fin de memoria dinámica|mover fin de memoria dinámica|esperar hijo indicado|esperar hijo|abrir|crear archivo|controlar archivo|estado del archivo|obtener estado del enlace mismo|obtener estado del archivo abierto|obtener información del sistema|convertir 16 bits a orden de red|convertir 16 bits a orden de máquina|convertir 32 bits a orden de red|convertir 32 bits a orden de máquina|crear extremo de comunicación|asociar dirección local|conectar con extremo remoto|preparar recepción de conexiones|aceptar conexión|obtener dirección local|obtener dirección remota|enviar|recibir|enviar a destino|recibir con dirección de origen|cerrar sentido de comunicación|configurar opción del extremo',
 'hi': 'तुरंत समाप्त करना|पढ़ना|लिखना|बंद करना|पठन लेखन स्थिति बदलना|संतान प्रक्रिया बनाना|निष्पादन सामग्री बदलना|प्रक्रिया पहचान पाना|जनक प्रक्रिया पहचान पाना|उपयोगकर्ता पहचान पाना|प्रभावी उपयोगकर्ता पहचान पाना|समूह पहचान पाना|प्रभावी समूह पहचान पाना|पहुँच अनुमति जाँचना|कार्य निर्देशिका बदलना|कार्य निर्देशिका पथ पाना|खुली संचिका संदर्भ की प्रतिलिपि बनाना|नियत क्रमांक पर संचिका संदर्भ प्रतिलिपि बनाना|संचिका अभिलेख समकालित करना|सभी अभिलेख समकालित करना|अंतक है या नहीं जाँचना|गतिशील स्मृति अंत निर्धारित करना|गतिशील स्मृति अंत बदलना|नियत संतान की प्रतीक्षा करना|संतान की प्रतीक्षा करना|खोलना|संचिका बनाना|संचिका नियंत्रित करना|संचिका स्थिति|कड़ी की अपनी स्थिति पाना|खुली संचिका स्थिति पाना|प्रणाली जानकारी पाना|16 अंकों को संजाल क्रम में बदलना|16 अंकों को यंत्र क्रम में बदलना|32 अंकों को संजाल क्रम में बदलना|32 अंकों को यंत्र क्रम में बदलना|संचार छोर बनाना|स्थानीय पता बाँधना|दूसरे छोर से जुड़ना|जुड़ाव अनुरोध के लिए तैयार होना|जुड़ाव स्वीकार करना|स्थानीय छोर पता पाना|दूसरे छोर का पता पाना|भेजना|प्राप्त करना|गंतव्य पर भेजना|प्रेषक पते सहित प्राप्त करना|संचार दिशा बंद करना|संचार छोर विकल्प निर्धारित करना',
}

FUNCTION_ROWS.update({
 'pt': 'terminar imediatamente|ler|escrever|fechar|mover posição do ficheiro|bifurcar processo|substituir programa em execução|obter identificador do processo|obter identificador do processo pai|obter identificador do utilizador|obter identificador efetivo do utilizador|obter identificador do grupo|obter identificador efetivo do grupo|verificar permissões de acesso|mudar diretório de trabalho|obter caminho do diretório de trabalho|duplicar referência de ficheiro aberto|duplicar referência para número indicado|sincronizar dados do ficheiro|sincronizar todos os dados|verificar se é terminal|definir fim da memória dinâmica|mover fim da memória dinâmica|aguardar filho indicado|aguardar filho|abrir|criar ficheiro|controlar ficheiro|estado do ficheiro|obter estado da ligação em si|obter estado do ficheiro aberto|obter informações do sistema|converter 16 bits para ordem da rede|converter 16 bits para ordem da máquina|converter 32 bits para ordem da rede|converter 32 bits para ordem da máquina|criar extremo de comunicação|associar endereço local|ligar ao extremo remoto|preparar receção de ligações|aceitar ligação|obter endereço do extremo local|obter endereço do extremo remoto|enviar|receber|enviar para destino|receber com endereço de origem|fechar sentido de comunicação|definir opção do extremo',
 'ru': 'немедленно завершить|читать|писать|закрыть|переместить позицию файла|создать дочерний процесс|заменить исполняемую программу|получить номер процесса|получить номер родительского процесса|получить номер пользователя|получить действующий номер пользователя|получить номер группы|получить действующий номер группы|проверить права доступа|сменить рабочий каталог|получить путь рабочего каталога|дублировать ссылку на открытый файл|дублировать ссылку под заданным номером|согласовать данные файла|согласовать все данные|проверить является ли терминалом|задать конец динамической памяти|сместить конец динамической памяти|ждать указанного потомка|ждать потомка|открыть|создать файл|управлять файлом|состояние файла|получить состояние самой ссылки|получить состояние открытого файла|получить сведения о системе|перевести 16 разрядов в сетевой порядок|перевести 16 разрядов в машинный порядок|перевести 32 разряда в сетевой порядок|перевести 32 разряда в машинный порядок|создать оконечную точку связи|привязать местный адрес|соединить с другой стороной|подготовить приём соединений|принять соединение|получить местный адрес точки|получить адрес другой стороны|отправить|получить|отправить по адресу|получить с адресом отправителя|закрыть направление связи|задать настройку точки связи',
 'ar': 'إنهاء فوري|قراءة|كتابة|إغلاق|نقل موضع الملف|إنشاء عملية فرعية|استبدال البرنامج الجاري|جلب معرف العملية|جلب معرف العملية الأم|جلب معرف المستخدم|جلب معرف المستخدم الفعلي|جلب معرف المجموعة|جلب معرف المجموعة الفعلي|فحص صلاحيات الوصول|تغيير دليل العمل|جلب مسار دليل العمل|نسخ مرجع الملف المفتوح|نسخ مرجع الملف إلى رقم محدد|مزامنة بيانات الملف|مزامنة جميع البيانات|فحص كون الوصف طرفية|تعيين نهاية الذاكرة المتغيرة|نقل نهاية الذاكرة المتغيرة|انتظار العملية الفرعية المحددة|انتظار عملية فرعية|فتح|إنشاء ملف|التحكم في الملف|حالة الملف|جلب حالة الرابط نفسه|جلب حالة الملف المفتوح|جلب معلومات النظام|تحويل 16 خانة إلى ترتيب الشبكة|تحويل 16 خانة إلى ترتيب الآلة|تحويل 32 خانة إلى ترتيب الشبكة|تحويل 32 خانة إلى ترتيب الآلة|إنشاء نقطة اتصال|ربط عنوان محلي|الاتصال بالطرف المقابل|تهيئة استقبال الاتصالات|قبول اتصال|جلب عنوان النقطة المحلية|جلب عنوان الطرف المقابل|إرسال|استقبال|إرسال إلى وجهة|استقبال مع عنوان المصدر|إغلاق اتجاه الاتصال|ضبط خيار نقطة الاتصال',
 'ta': 'உடனே முடி|படி|எழுது|மூடு|கோப்பின் படிப்பிடத்தை நகர்த்து|சேய் செயல்முறையை உருவாக்கு|இயங்கும் நிரலை மாற்று|செயல்முறை அடையாளத்தைப் பெறு|தாய் செயல்முறை அடையாளத்தைப் பெறு|பயனர் அடையாளத்தைப் பெறு|நடப்பு உரிமைப் பயனர் அடையாளத்தைப் பெறு|குழு அடையாளத்தைப் பெறு|நடப்பு உரிமைக் குழு அடையாளத்தைப் பெறு|அணுகல் உரிமையைச் சோதி|பணி அடைவை மாற்று|பணி அடைவின் பாதையைப் பெறு|திறந்த கோப்பின் குறிப்பை நகலெடு|குறித்த எண்ணுக்கு கோப்புக் குறிப்பை நகலெடு|கோப்பின் பதிவை ஒத்திசை|அனைத்துப் பதிவுகளையும் ஒத்திசை|முனையமா எனச் சோதி|மாறும் நினைவக முடிவை அமை|மாறும் நினைவக முடிவை நகர்த்து|குறித்த சேய்க்குக் காத்திரு|சேய்க்குக் காத்திரு|திற|கோப்பை உருவாக்கு|கோப்பைக் கட்டுப்படுத்து|கோப்பு நிலை|இணைப்பின் சொந்த நிலையைப் பெறு|திறந்த கோப்பின் நிலையைப் பெறு|அமைப்புத் தகவலைப் பெறு|16 இரும இலக்கங்களை வலை வரிசைக்கு மாற்று|16 இரும இலக்கங்களைப் பொறி வரிசைக்கு மாற்று|32 இரும இலக்கங்களை வலை வரிசைக்கு மாற்று|32 இரும இலக்கங்களைப் பொறி வரிசைக்கு மாற்று|தொடர்பு முனையை உருவாக்கு|உள்ளக முகவரியைப் பிணை|எதிர் முனையுடன் இணை|இணைப்புகளை ஏற்கத் தயாராகு|இணைப்பை ஏற்றுக்கொள்|உள்ளக முனையின் முகவரியைப் பெறு|எதிர் முனையின் முகவரியைப் பெறு|அனுப்பு|பெறு|இலக்கிற்கு அனுப்பு|அனுப்பிய முகவரியுடன் பெறு|தொடர்புத் திசையை மூடு|தொடர்பு முனையின் விருப்பத்தை அமை',
})

PARTIAL_FUNCTIONS = {
 'sr_Cyrl': {'read': 'читати', 'write': 'писати', 'open': 'отворити', 'close': 'затворити'},
 'sr_Latn': {'read': 'čitati', 'write': 'pisati', 'open': 'otvoriti', 'close': 'zatvoriti'},
 'bs_Cyrl': {'read': 'читати', 'write': 'писати', 'open': 'отворити', 'close': 'затворити'},
 'bs_Latn': {'read': 'čitati', 'write': 'pisati', 'open': 'otvoriti', 'close': 'zatvoriti'},
}

# Explicit readings of complete technical phrases, not individual-kanji guesses.
JAPANESE_FUNCTION_READINGS = 'ただちにしゅうりょうする|よむ|かく|とじる|よみかきいちをうつす|じっこうかていをぶんきする|じっこうないようをおきかえる|じっこうかていばんごうをえる|おやじっこうかていばんごうをえる|りようしゃばんごうをえる|じっこうりようしゃばんごうをえる|しょぞくくみばんごうをえる|じっこうしょぞくくみばんごうをえる|りようけんげんをしらべる|さぎょうもくろくをかえる|さぎょうもくろくのけいろをえる|ひらいたぶんしょのさんしょうをふくせいする|していばんごうにぶんしょさんしょうをふくせいする|ぶんしょのきろくをどうきする|すべてのきろくをどうきする|たんまつかしらべる|どうてききおくのしゅうたんをさだめる|どうてききおくのしゅうたんをうつす|していしたこをまつ|こをまつ|ひらく|ぶんしょをつくる|ぶんしょをせいぎょする|ぶんしょじょうたい|れんけつじたいのじょうたいをえる|ひらいたぶんしょのじょうたいをえる|たいけいじょうほうをえる|つうしんもうじゅんに16けたをかえる|きかいじゅんに16けたをかえる|つうしんもうじゅんに32けたをかえる|きかいじゅんに32けたをかえる|つうしんたんてんをつくる|きょくしょばんちをむすぶ|あいてたんてんにつなぐ|せつぞくようきゅうにそなえる|せつぞくようきゅうをうけいれる|きょくしょたんてんのばんちをえる|あいてたんてんのばんちをえる|おくる|うけとる|あてさきにおくる|そうしんもととともにうけとる|つうしんほうこうをとじる|つうしんたんてんをせっていする'

BASE_LOCAL_KEYS = ('fd buf count offset whence status path argv envp mode size result oldfd newfd st '
 'address current requested increment pid options oflag args cmd argument name number '
 'a1 a2 a3 a4 a5 a6 a b c n m call arguments value domain type protocol length flags '
 'backlog how level option_name option_value option_len address_length address_len '
 'buffer message dest_addr dest_len socket_call errno environ').split()
LOCAL_ROWS = {
 'ko': '자료철서술번호|완충영역|여덟자리묶음수|위치차이|위치기준|끝난상태|경로|인수목록|환경목록|접근방식|크기|결과|기존서술번호|새서술번호|상태자료|주소|현재끝|요청끝|증가량|실행과정번호|선택사항|열기선택|가변인수|제어명령|인수값|체제자료|호출번호|첫째인수|둘째인수|셋째인수|넷째인수|다섯째인수|여섯째인수|전달값묶음|둘째값|셋째값|호출종류|검사방식|통신호출번호|전달인수목록|값|주소계열|끝점종류|통신규약|길이|처리표시|대기한도|닫을방향|설정수준|설정이름|설정값|설정크기|주소길이|주소크기|자료완충영역|전문|목적지주소|목적지주소길이|통신끝점호출하기|오류번호|환경변수목록',
 'ja': '文書記述番号|緩衝領域|八桁組数|位置差|位置基準|終了状態|経路|引数一覧|環境一覧|利用方式|大きさ|結果|旧記述番号|新記述番号|状態資料|番地|現在終端|要求終端|増分|実行過程番号|選択事項|開く際の指定|可変引数|制御命令|引数値|体系資料|呼出番号|第一引数|第二引数|第三引数|第四引数|第五引数|第六引数|受渡値組|第二値|第三値|呼出種類|検査方式|通信呼出番号|受渡引数一覧|値|番地系統|端点種類|通信規約|長さ|処理指定|待機上限|閉じる方向|設定階層|設定名|設定値|設定長|番地長|番地寸法|資料緩衝領域|電文|宛先番地|宛先番地長|通信端点を呼び出す|誤り番号|環境変数一覧',
 'zh_Hans': '文件描述编号|缓冲区域|字节数|位移|位置基准|结束状态|路径|参数列表|环境列表|访问方式|大小|结果|原描述编号|新描述编号|状态资料|地址|当前末端|请求末端|增量|进程编号|选项|打开选项|可变参数|控制命令|参数值|系统资料|调用编号|第一参数|第二参数|第三参数|第四参数|第五参数|第六参数|传值数组|第二值|第三值|调用种类|检查方式|通信调用编号|传入参数列表|值|地址族|端点类型|通信协议|长度|处理标志|等待上限|关闭方向|设置层级|选项名|选项值|选项长度|地址长度|地址大小|数据缓冲区域|报文|目的地址|目的地址长度|调用通信端点|错误编号|环境变量列表',
 'zh_Hant': '檔案描述編號|緩衝區域|位元組數|位移|位置基準|結束狀態|路徑|引數列表|環境列表|存取方式|大小|結果|原描述編號|新描述編號|狀態資料|位址|目前末端|要求末端|增量|行程編號|選項|開啟選項|可變引數|控制命令|引數值|系統資料|呼叫編號|第一引數|第二引數|第三引數|第四引數|第五引數|第六引數|傳值陣列|第二值|第三值|呼叫種類|檢查方式|通訊呼叫編號|傳入引數列表|值|位址族|端點類型|通訊協定|長度|處理旗標|等待上限|關閉方向|設定層級|選項名稱|選項值|選項長度|位址長度|位址大小|資料緩衝區域|訊息|目的位址|目的位址長度|呼叫通訊端點|錯誤編號|環境變數列表',
}
JAPANESE_LOCAL_READINGS = 'ぶんしょきじゅつばんごう|かんしょうりょういき|はちけたぐみすう|いちさ|いちきじゅん|しゅうりょうじょうたい|けいろ|ひきすういちらん|かんきょういちらん|りようほうしき|おおきさ|けっか|きゅうきじゅつばんごう|しんきじゅつばんごう|じょうたいしりょう|ばんち|げんざいしゅうたん|ようきゅうしゅうたん|ぞうぶん|じっこうかていばんごう|せんたくじこう|ひらくさいのしてい|かへんひきすう|せいぎょめいれい|ひきすうち|たいけいしりょう|よびだしばんごう|だいいちひきすう|だいにひきすう|だいさんひきすう|だいよんひきすう|だいごひきすう|だいろくひきすう|うけわたしあたいぐみ|だいにち|だいさんち|よびだししゅるい|けんさほうしき|つうしんよびだしばんごう|うけわたしひきすういちらん|あたい|ばんちけいとう|たんてんしゅるい|つうしんきやく|ながさ|しょりしてい|たいきじょうげん|とじるほうこう|せっていかいそう|せっていめい|せっていち|せっていちょう|ばんちちょう|ばんちすんぽう|しりょうかんしょうりょういき|でんぶん|あてさきばんち|あてさきばんちちょう|つうしんたんてんをよびだす|あやまりばんごう|かんきょうへんすういちらん'

PATH_KEYS = 'include src tests unistd errno fcntl stat socket syscall crt0 linker probe'.split()
PATH_ROWS = {
 'ko': '선언|구현|시험|입출력과실행|오류번호|자료철제어|자료철상태|통신끝점|체계호출|시작|연결배치|현지어호출시험',
 'ja': '宣言|実装|試験|入出力と実行|誤り番号|文書制御|文書状態|通信端点|体系呼出|起動|連結配置|母語呼出試験',
 'ja_Hira': 'せんげん|じっそう|しけん|にゅうしゅつりょくとじっこう|あやまりばんごう|ぶんしょせいぎょ|ぶんしょじょうたい|つうしんたんてん|たいけいよびだし|きどう|れんけつはいち|ぼごよびだししけん',
 'zh_Hans': '声明|实现|测试|输入输出与执行|错误编号|文件控制|文件状态|通信端点|系统调用|启动|链接布局|本语言调用测试',
 'zh_Hant': '宣告|實作|測試|輸入輸出與執行|錯誤編號|檔案控制|檔案狀態|通訊端點|系統呼叫|啟動|連結配置|本語言呼叫測試',
}


def checked(keys, row):
    values = row.split('|')
    if len(keys) != len(values):
        raise ValueError('Wrong terminology row width: %d != %d' % (len(keys), len(values)))
    return dict(zip(keys, values))


def katakana(text):
    return ''.join(chr(ord(ch) + 0x60) if '\u3041' <= ch <= '\u3096' else ch for ch in text)


def explicit(language):
    base = language if language.startswith('zh_') else language.split('_')[0]
    names = {}
    if base in FUNCTION_ROWS:
        names.update(checked(BASE_FUNCTION_KEYS, FUNCTION_ROWS[base]))
    if base in LOCAL_ROWS:
        names.update(checked(BASE_LOCAL_KEYS, LOCAL_ROWS[base]))
    # These locals also occur in test reports and scalar syscall macros.
    # Avoid assigning a system-identity-only or array-only meaning globally.
    if base == 'ko':
        names.update({'name': '이름', 'a': '전달값', 'count': '수량'})
    if base == 'ja':
        names.update({'name': '名前', 'a': '受渡値', 'count': '数量'})
    names.update(PARTIAL_FUNCTIONS.get(language, {}))
    paths = checked(PATH_KEYS, PATH_ROWS[base]) if base in PATH_ROWS else {}
    if language in ('ja_Hira', 'ja_Kana'):
        names = checked(BASE_FUNCTION_KEYS, JAPANESE_FUNCTION_READINGS)
        names.update(checked(BASE_LOCAL_KEYS, JAPANESE_LOCAL_READINGS))
        names.update({'name': 'なまえ', 'a': 'うけわたしあたい', 'count': 'すうりょう'})
        paths = checked(PATH_KEYS, PATH_ROWS['ja_Hira'])
        if language == 'ja_Kana':
            names = {k: katakana(v) for k, v in names.items()}
            paths = {k: katakana(v) for k, v in paths.items()}
    extra_names, extra_paths = library_explicit(language)
    names.update(extra_names)
    paths.update(extra_paths)
    declaration_names, declaration_paths = declaration_explicit(language)
    names.update(declaration_names)
    paths.update(declaration_paths)
    if base in ('zh_Hans', 'zh_Hant'):
        names['count'] = '数量' if base == 'zh_Hans' else '數量'
    return names, paths


from posix_library_terms import FUNCTION_KEYS as LIBRARY_FUNCTION_KEYS
from posix_library_terms import LOCAL_KEYS as LIBRARY_LOCAL_KEYS
from posix_library_terms import explicit as library_explicit
from posix_declaration_terms import explicit as declaration_explicit

FUNCTION_KEYS = BASE_FUNCTION_KEYS + LIBRARY_FUNCTION_KEYS
LOCAL_KEYS = BASE_LOCAL_KEYS + LIBRARY_LOCAL_KEYS
