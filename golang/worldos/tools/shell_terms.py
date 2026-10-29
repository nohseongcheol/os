"""Explicit whole-phrase project proposals, never a certificate of fluency.

Missing languages keep English functional identifiers with pending status.
Do not translate POSIX functions, struct members, C keywords or CPU registers.
"""
FUNCTION_KEYS = ('shell_name text_length text_equal write_text write_integer write_error read_line '
                 'split_arguments print_help command_echo command_pwd command_cat command_stat '
                 'command_pid command_uname command_run command_udp command_source command_matches run_input').split()
FUNCTIONS = {
 'en': 'command interpreter|text length|texts equal|write text|write integer|report error|read input line|split arguments|show help|print arguments|show working directory|display file contents|show file information|show process identifiers|show system identity|run program|test datagram loopback|interpret command file|command matches|interpret input',
 'ko': '명령해석기|문자열 길이|문자열 일치|문자열 쓰기|정수 쓰기|오류 알리기|입력줄 읽기|인수 나누기|도움말 표시|인수 출력|현재 경로 표시|파일 내용 표시|파일 정보 표시|실행과정 번호 표시|운영체제 정보 표시|프로그램 실행|자료전문 되돌림 시험|명령파일 해석|명령 일치|입력 해석',
 'ja': '命令解釈器|文字列長|文字列一致|文字列を書き出す|整数を書き出す|誤りを知らせる|入力行を読む|引数を分ける|使い方を示す|引数を表示する|現在の場所を示す|文書の内容を表示する|文書の情報を示す|実行過程の番号を示す|基本体系の情報を示す|実行形式を起動する|独立電文の折り返しを試す|命令文書を解釈する|命令が一致する|入力を解釈する',
 'zh_Hans': '命令解释器|文本长度|文本相同|写出文本|写出整数|报告错误|读取输入行|拆分参数|显示帮助|显示参数|显示当前目录|显示文件内容|显示文件信息|显示进程编号|显示系统信息|运行程序|测试数据报回送|解释命令文件|命令匹配|解释输入',
 'zh_Hant': '命令解譯器|文字長度|文字相同|寫出文字|寫出整數|回報錯誤|讀取輸入列|拆分引數|顯示說明|顯示引數|顯示目前目錄|顯示檔案內容|顯示檔案資訊|顯示行程編號|顯示系統資訊|執行程式|測試資料報回送|解譯命令檔案|命令相符|解譯輸入',
 'de': 'Befehlsauswerter|Textlänge|Texte gleich|Text schreiben|Ganzzahl schreiben|Fehler melden|Eingabezeile lesen|Argumente trennen|Hilfe anzeigen|Argumente ausgeben|Arbeitsverzeichnis anzeigen|Dateiinhalt anzeigen|Dateiinformationen anzeigen|Prozesskennungen anzeigen|Systemkennung anzeigen|Programm ausführen|Datagrammrücklauf prüfen|Befehlsdatei auswerten|Befehl stimmt überein|Eingabe auswerten',
 'fr': 'interpréteur de commandes|longueur du texte|textes identiques|écrire le texte|écrire un entier|signaler une erreur|lire une ligne|séparer les arguments|afficher l’aide|afficher les arguments|afficher le répertoire courant|afficher le contenu du fichier|afficher les informations du fichier|afficher les identifiants des processus|afficher l’identité du système|exécuter un programme|tester le retour du datagramme|interpréter un fichier de commandes|commande correspondante|interpréter l’entrée',
 'es': 'intérprete de órdenes|longitud del texto|textos iguales|escribir texto|escribir entero|informar del error|leer línea de entrada|separar argumentos|mostrar ayuda|mostrar argumentos|mostrar directorio actual|mostrar contenido del archivo|mostrar información del archivo|mostrar identificadores de procesos|mostrar identidad del sistema|ejecutar programa|probar retorno del datagrama|interpretar archivo de órdenes|coincide la orden|interpretar entrada',
 'pt': 'interpretador de comandos|comprimento do texto|textos iguais|escrever texto|escrever inteiro|comunicar erro|ler linha de entrada|separar argumentos|mostrar ajuda|mostrar argumentos|mostrar diretório atual|mostrar conteúdo do ficheiro|mostrar informações do ficheiro|mostrar identificadores de processos|mostrar identidade do sistema|executar programa|testar retorno do datagrama|interpretar ficheiro de comandos|comando corresponde|interpretar entrada',
 'it': 'interprete dei comandi|lunghezza del testo|testi uguali|scrivi testo|scrivi intero|segnala errore|leggi riga di ingresso|separa argomenti|mostra aiuto|mostra argomenti|mostra cartella corrente|mostra contenuto del file|mostra informazioni del file|mostra identificatori dei processi|mostra identità del sistema|esegui programma|verifica ritorno del datagramma|interpreta file di comandi|comando corrispondente|interpreta ingresso',
 'ru': 'интерпретатор команд|длина текста|тексты равны|вывести текст|вывести целое число|сообщить об ошибке|прочитать строку ввода|разделить аргументы|показать справку|вывести аргументы|показать текущий каталог|показать содержимое файла|показать сведения о файле|показать номера процессов|показать сведения о системе|запустить программу|проверить возврат датаграммы|исполнить командный файл|команда совпадает|разобрать ввод',
 'uk': 'інтерпретатор команд|довжина тексту|тексти однакові|вивести текст|вивести ціле число|повідомити про помилку|прочитати рядок введення|розділити аргументи|показати довідку|вивести аргументи|показати поточний каталог|показати вміст файла|показати відомості про файл|показати номери процесів|показати відомості про систему|запустити програму|перевірити повернення датаграми|виконати командний файл|команда збігається|розібрати введення',
 'ar': 'مفسر الأوامر|طول النص|تساوي النصين|كتابة النص|كتابة عدد صحيح|الإبلاغ عن خطأ|قراءة سطر الإدخال|فصل المعاملات|عرض المساعدة|عرض المعاملات|عرض المجلد الحالي|عرض محتوى الملف|عرض معلومات الملف|عرض معرفات العمليات|عرض هوية النظام|تشغيل البرنامج|اختبار إرجاع حزمة البيانات|تفسير ملف الأوامر|مطابقة الأمر|تفسير الإدخال',
 'tr': 'komut yorumlayıcı|metin uzunluğu|metinler eşit|metin yaz|tam sayı yaz|hata bildir|girdi satırını oku|bağımsız değişkenleri ayır|yardım göster|bağımsız değişkenleri göster|çalışma dizinini göster|dosya içeriğini göster|dosya bilgilerini göster|süreç kimliklerini göster|sistem kimliğini göster|programı çalıştır|veri birimi geri dönüşünü sına|komut dosyasını yorumla|komut eşleşiyor|girdiyi yorumla',
 'vi': 'bộ thông dịch lệnh|độ dài văn bản|văn bản bằng nhau|ghi văn bản|ghi số nguyên|báo lỗi|đọc dòng nhập|tách đối số|hiện trợ giúp|hiện đối số|hiện thư mục hiện tại|hiện nội dung tệp|hiện thông tin tệp|hiện mã tiến trình|hiện thông tin hệ thống|chạy chương trình|thử gói dữ liệu vòng về|thông dịch tệp lệnh|lệnh trùng khớp|thông dịch đầu vào',
 'id': 'penafsir perintah|panjang teks|teks sama|tulis teks|tulis bilangan bulat|laporkan galat|baca baris masukan|pisahkan argumen|tampilkan bantuan|tampilkan argumen|tampilkan direktori kerja|tampilkan isi berkas|tampilkan informasi berkas|tampilkan pengenal proses|tampilkan identitas sistem|jalankan program|uji pengembalian datagram|tafsirkan berkas perintah|perintah cocok|tafsirkan masukan',
 'ms_Latn': 'pentafsir perintah|panjang teks|teks sama|tulis teks|tulis nombor bulat|laporkan ralat|baca baris masukan|pisahkan argumen|paparkan bantuan|paparkan argumen|paparkan direktori semasa|paparkan kandungan fail|paparkan maklumat fail|paparkan pengenal proses|paparkan identiti sistem|jalankan atur cara|uji pengembalian datagram|tafsirkan fail perintah|perintah sepadan|tafsirkan masukan',
 'pl': 'interpretator poleceń|długość tekstu|teksty równe|wypisz tekst|wypisz liczbę całkowitą|zgłoś błąd|odczytaj wiersz wejścia|rozdziel argumenty|pokaż pomoc|wypisz argumenty|pokaż katalog roboczy|pokaż zawartość pliku|pokaż informacje o pliku|pokaż identyfikatory procesów|pokaż tożsamość systemu|uruchom program|sprawdź powrót datagramu|interpretuj plik poleceń|polecenie pasuje|interpretuj wejście',
 'nl': 'opdrachtvertolker|tekstlengte|teksten gelijk|tekst schrijven|geheel getal schrijven|fout melden|invoerregel lezen|argumenten scheiden|hulp tonen|argumenten tonen|werkmap tonen|bestandsinhoud tonen|bestandsinformatie tonen|procesnummers tonen|systeemidentiteit tonen|programma uitvoeren|terugkeer van datagram testen|opdrachtbestand vertolken|opdracht komt overeen|invoer vertolken',
 'sv': 'kommandotolk|textlängd|texter lika|skriv text|skriv heltal|rapportera fel|läs inmatningsrad|dela upp argument|visa hjälp|visa argument|visa arbetskatalog|visa filinnehåll|visa filinformation|visa processidentifierare|visa systemidentitet|kör program|prova datagrammets återföring|tolka kommandofil|kommando stämmer|tolka inmatning',
 'fi': 'komentotulkki|tekstin pituus|tekstit samat|kirjoita teksti|kirjoita kokonaisluku|ilmoita virhe|lue syöterivi|erota argumentit|näytä ohje|näytä argumentit|näytä työhakemisto|näytä tiedoston sisältö|näytä tiedoston tiedot|näytä prosessitunnukset|näytä järjestelmätiedot|suorita ohjelma|testaa tietosähkeen palautus|tulkitse komentotiedosto|komento täsmää|tulkitse syöte',
 'cs': 'interpret příkazů|délka textu|texty stejné|vypsat text|vypsat celé číslo|ohlásit chybu|číst vstupní řádek|rozdělit argumenty|zobrazit nápovědu|vypsat argumenty|zobrazit pracovní adresář|zobrazit obsah souboru|zobrazit informace o souboru|zobrazit identifikátory procesů|zobrazit identitu systému|spustit program|ověřit návrat datagramu|interpretovat příkazový soubor|příkaz odpovídá|interpretovat vstup',
 'hi': 'आदेश व्याख्याकार|पाठ की लंबाई|पाठ समान हैं|पाठ लिखना|पूर्णांक लिखना|त्रुटि बताना|निवेश पंक्ति पढ़ना|तर्क अलग करना|सहायता दिखाना|तर्क दिखाना|वर्तमान निर्देशिका दिखाना|संचिका की सामग्री दिखाना|संचिका की जानकारी दिखाना|प्रक्रिया क्रमांक दिखाना|प्रणाली की पहचान दिखाना|कार्यक्रम चलाना|स्वतंत्र संदेश की वापसी जाँचना|आदेश संचिका का अर्थ निकालना|आदेश मेल खाता है|निवेश का अर्थ निकालना',
 'bn': 'আদেশ ব্যাখ্যাকারী|পাঠের দৈর্ঘ্য|পাঠ সমান|পাঠ লেখা|পূর্ণসংখ্যা লেখা|ত্রুটি জানানো|নিবেশের পঙ্‌ক্তি পড়া|আর্গুমেন্ট আলাদা করা|সহায়তা দেখানো|আর্গুমেন্ট দেখানো|বর্তমান নির্দেশিকা দেখানো|নথির বিষয়বস্তু দেখানো|নথির তথ্য দেখানো|প্রক্রিয়ার পরিচয় দেখানো|ব্যবস্থার পরিচয় দেখানো|কার্যক্রম চালানো|স্বতন্ত্র বার্তার প্রত্যাবর্তন পরীক্ষা|আদেশ নথি ব্যাখ্যা করা|আদেশ মিলে যায়|নিবেশ ব্যাখ্যা করা',
 'ta': 'கட்டளை விளக்கி|உரையின் நீளம்|உரைகள் சமம்|உரையை எழுது|முழு எண்ணை எழுது|பிழையை அறிவி|உள்ளீட்டு வரியைப் படி|செயலுருபுகளைப் பிரி|உதவியைக் காட்டு|செயலுருபுகளைக் காட்டு|நடப்பு அடைவைக் காட்டு|கோப்பின் உள்ளடக்கத்தைக் காட்டு|கோப்பின் தகவலைக் காட்டு|செயல்முறை அடையாளங்களைக் காட்டு|அமைப்பின் அடையாளத்தைக் காட்டு|நிரலை இயக்கு|தனிச் செய்தியின் மீள்வரவைச் சோதி|கட்டளைக் கோப்பை விளக்கு|கட்டளை பொருந்துகிறது|உள்ளீட்டை விளக்கு',
 'ur': 'حکم کی تشریح کرنے والا|متن کی لمبائی|متن برابر ہیں|متن لکھنا|صحیح عدد لکھنا|خرابی بتانا|اندراج کی سطر پڑھنا|دلائل الگ کرنا|مدد دکھانا|دلائل دکھانا|موجودہ فہرست دکھانا|فائل کا مواد دکھانا|فائل کی معلومات دکھانا|عمل کی شناخت دکھانا|نظام کی شناخت دکھانا|پروگرام چلانا|آزاد پیغام کی واپسی جانچنا|احکامات کی فائل کی تشریح کرنا|حکم ملتا ہے|اندراج کی تشریح کرنا',
}

FIELD_KEYS = 'text length left right position value input_line arguments argument_count file_name file_descriptor bytes_read path status command capacity current output quote character'.split()
FIELDS = {
 'en': 'text|length|left|right|position|value|input line|arguments|argument count|file name|file descriptor|bytes read|path|status|command|capacity|current|output|quote|character',
 'ko': '문자열|길이|왼쪽|오른쪽|위치|값|입력줄|인수들|인수 개수|파일 이름|파일 서술번호|읽은 바이트수|경로|상태|명령|수용량|현재 위치|출력 위치|따옴표|문자',
 'ja': '文字列|長さ|左|右|位置|値|入力行|引数列|引数の数|文書名|文書記述番号|読んだ八桁組の数|経路|状態|命令|容量|現在位置|出力位置|引用符|文字',
 'zh_Hans': '文本|长度|左侧|右侧|位置|数值|输入行|参数列表|参数个数|文件名|文件描述符|已读字节数|路径|状态|命令|容量|当前位置|输出位置|引号|字符',
 'zh_Hant': '文字|長度|左側|右側|位置|數值|輸入列|引數列表|引數個數|檔名|檔案描述元|已讀位元組數|路徑|狀態|命令|容量|目前位置|輸出位置|引號|字元',
 'de': 'Text|Länge|links|rechts|Position|Wert|Eingabezeile|Argumente|Argumentanzahl|Dateiname|Dateideskriptor|gelesene Bytes|Pfad|Status|Befehl|Kapazität|aktuelle Position|Ausgabeposition|Anführungszeichen|Zeichen',
 'fr': 'texte|longueur|gauche|droite|position|valeur|ligne d’entrée|arguments|nombre d’arguments|nom du fichier|descripteur de fichier|octets lus|chemin|état|commande|capacité|position courante|position de sortie|guillemet|caractère',
 'es': 'texto|longitud|izquierda|derecha|posición|valor|línea de entrada|argumentos|cantidad de argumentos|nombre del archivo|descriptor del archivo|octetos leídos|ruta|estado|orden|capacidad|posición actual|posición de salida|comilla|carácter',
 'pt': 'texto|comprimento|esquerda|direita|posição|valor|linha de entrada|argumentos|número de argumentos|nome do ficheiro|descritor do ficheiro|octetos lidos|caminho|estado|comando|capacidade|posição atual|posição de saída|aspas|caráter',
 'it': 'testo|lunghezza|sinistra|destra|posizione|valore|riga di ingresso|argomenti|numero di argomenti|nome del file|descrittore del file|ottetti letti|percorso|stato|comando|capacità|posizione corrente|posizione di uscita|virgolette|carattere',
 'ru': 'текст|длина|слева|справа|позиция|значение|строка ввода|аргументы|число аргументов|имя файла|дескриптор файла|прочитанные байты|путь|состояние|команда|вместимость|текущая позиция|позиция вывода|кавычка|символ',
 'uk': 'текст|довжина|ліворуч|праворуч|позиція|значення|рядок введення|аргументи|кількість аргументів|ім’я файла|дескриптор файла|прочитані байти|шлях|стан|команда|місткість|поточна позиція|позиція виведення|лапки|символ',
 'ar': 'النص|الطول|اليسار|اليمين|الموضع|القيمة|سطر الإدخال|المعاملات|عدد المعاملات|اسم الملف|واصف الملف|البايتات المقروءة|المسار|الحالة|الأمر|السعة|الموضع الحالي|موضع الإخراج|علامة الاقتباس|المحرف',
 'tr': 'metin|uzunluk|sol|sağ|konum|değer|girdi satırı|bağımsız değişkenler|bağımsız değişken sayısı|dosya adı|dosya tanımlayıcısı|okunan baytlar|yol|durum|komut|kapasite|geçerli konum|çıktı konumu|tırnak|karakter',
 'vi': 'văn bản|độ dài|trái|phải|vị trí|giá trị|dòng nhập|đối số|số đối số|tên tệp|bộ mô tả tệp|số byte đã đọc|đường dẫn|trạng thái|lệnh|sức chứa|vị trí hiện tại|vị trí xuất|dấu ngoặc kép|ký tự',
 'id': 'teks|panjang|kiri|kanan|posisi|nilai|baris masukan|argumen|jumlah argumen|nama berkas|deskriptor berkas|byte terbaca|jalur|status|perintah|kapasitas|posisi saat ini|posisi keluaran|tanda kutip|karakter',
 'ms_Latn': 'teks|panjang|kiri|kanan|kedudukan|nilai|baris masukan|argumen|bilangan argumen|nama fail|pemerihal fail|bait dibaca|laluan|keadaan|perintah|kapasiti|kedudukan semasa|kedudukan keluaran|tanda petik|aksara',
 'pl': 'tekst|długość|lewy|prawy|pozycja|wartość|wiersz wejścia|argumenty|liczba argumentów|nazwa pliku|deskryptor pliku|odczytane bajty|ścieżka|stan|polecenie|pojemność|bieżąca pozycja|pozycja wyjścia|cudzysłów|znak',
 'nl': 'tekst|lengte|links|rechts|positie|waarde|invoerregel|argumenten|aantal argumenten|bestandsnaam|bestandsdescriptor|gelezen bytes|pad|toestand|opdracht|capaciteit|huidige positie|uitvoerpositie|aanhalingsteken|teken',
 'sv': 'text|längd|vänster|höger|position|värde|inmatningsrad|argument|antal argument|filnamn|filbeskrivare|lästa byte|sökväg|tillstånd|kommando|kapacitet|aktuell position|utmatningsposition|citattecken|tecken',
 'fi': 'teksti|pituus|vasen|oikea|paikka|arvo|syöterivi|argumentit|argumenttien määrä|tiedoston nimi|tiedostokuvaaja|luetut tavut|polku|tila|komento|kapasiteetti|nykyinen paikka|tulostuspaikka|lainausmerkki|merkki',
 'cs': 'text|délka|levý|pravý|pozice|hodnota|vstupní řádek|argumenty|počet argumentů|název souboru|deskriptor souboru|přečtené bajty|cesta|stav|příkaz|kapacita|aktuální pozice|výstupní pozice|uvozovka|znak',
 'hi': 'पाठ|लंबाई|बायाँ|दायाँ|स्थान|मान|निवेश पंक्ति|तर्क सूची|तर्कों की संख्या|संचिका का नाम|संचिका विवरणक|पढ़े गए बाइट|पथ|स्थिति|आदेश|क्षमता|वर्तमान स्थान|निर्गम स्थान|उद्धरण चिह्न|वर्ण',
 'bn': 'পাঠ|দৈর্ঘ্য|বাঁদিক|ডানদিক|অবস্থান|মান|নিবেশের পঙ্‌ক্তি|আর্গুমেন্ট তালিকা|আর্গুমেন্ট সংখ্যা|নথির নাম|নথি নির্দেশক|পঠিত বাইট|পথ|অবস্থা|আদেশ|ধারণক্ষমতা|বর্তমান অবস্থান|নির্গমের অবস্থান|উদ্ধৃতি চিহ্ন|অক্ষর',
 'ta': 'உரை|நீளம்|இடது|வலது|இடம்|மதிப்பு|உள்ளீட்டு வரி|செயலுருபுகள்|செயலுருபுகளின் எண்ணிக்கை|கோப்பின் பெயர்|கோப்பு விவரிப்பி|படித்த எண்மிகள்|பாதை|நிலை|கட்டளை|கொள்ளளவு|நடப்பு இடம்|வெளியீட்டு இடம்|மேற்கோள் குறி|எழுத்து',
 'ur': 'متن|لمبائی|بایاں|دایاں|مقام|قدر|اندراج کی سطر|دلائل|دلائل کی تعداد|فائل کا نام|فائل کا وصف کنندہ|پڑھے گئے بائٹ|راستہ|حالت|حکم|گنجائش|موجودہ مقام|اخراج کا مقام|اقتباس کی علامت|حرف',
}

HOST_KEYS = 'build_shell source_file object_file executable_file include_directory startup_object library_file linker_file'.split()
HOST = {
 'en': 'build command interpreter|source file|object file|executable file|header directory|startup object|library file|link layout file',
 'ko': '명령해석기 만들기|원문 파일|기계코드 파일|실행 파일|선언파일 경로|시동 기계코드|함수모음 파일|연결배치 파일',
 'ja': '命令解釈器を組み立てる|原文書|機械語文書|実行文書|宣言集の場所|起動機械語|関数集文書|連結配置文書',
 'zh_Hans': '构建命令解释器|源文件|目标文件|可执行文件|头文件目录|启动目标文件|库文件|链接布局文件',
 'zh_Hant': '建置命令解譯器|原始檔|目的檔|執行檔|標頭檔目錄|啟動目的檔|函式庫檔|連結配置檔',
 'de': 'Befehlsauswerter erstellen|Quelldatei|Objektdatei|ausführbare Datei|Deklarationsverzeichnis|Startobjekt|Bibliotheksdatei|Bindungsdatei',
 'fr': 'construire l’interpréteur|fichier source|fichier objet|fichier exécutable|répertoire des déclarations|objet de démarrage|fichier bibliothèque|fichier de liaison',
 'es': 'construir intérprete|archivo fuente|archivo objeto|archivo ejecutable|directorio de declaraciones|objeto de arranque|archivo de biblioteca|archivo de enlace',
 'pt': 'construir interpretador|ficheiro fonte|ficheiro objeto|ficheiro executável|diretório de declarações|objeto de arranque|ficheiro de biblioteca|ficheiro de ligação',
 'it': 'costruisci interprete|file sorgente|file oggetto|file eseguibile|cartella delle dichiarazioni|oggetto di avvio|file di libreria|file di collegamento',
 'ru': 'собрать интерпретатор|исходный файл|объектный файл|исполняемый файл|каталог объявлений|стартовый объект|файл библиотеки|файл компоновки',
 'uk': 'зібрати інтерпретатор|початковий файл|об’єктний файл|виконуваний файл|каталог оголошень|початковий об’єкт|файл бібліотеки|файл компонування',
 'ar': 'بناء مفسر الأوامر|ملف المصدر|ملف الكائن|الملف التنفيذي|مجلد التصريحات|كائن بدء التشغيل|ملف المكتبة|ملف الربط',
 'tr': 'komut yorumlayıcıyı derle|kaynak dosya|nesne dosyası|çalıştırılabilir dosya|bildirim dizini|başlangıç nesnesi|kitaplık dosyası|bağlama dosyası',
 'vi': 'dựng bộ thông dịch|tệp nguồn|tệp đối tượng|tệp thực thi|thư mục khai báo|đối tượng khởi động|tệp thư viện|tệp liên kết',
 'id': 'bangun penafsir perintah|berkas sumber|berkas objek|berkas eksekusi|direktori deklarasi|objek awal|berkas pustaka|berkas penautan',
 'ms_Latn': 'bina pentafsir perintah|fail sumber|fail objek|fail boleh laksana|direktori pengisytiharan|objek permulaan|fail pustaka|fail pautan',
 'pl': 'zbuduj interpretator|plik źródłowy|plik obiektowy|plik wykonywalny|katalog deklaracji|obiekt startowy|plik biblioteki|plik konsolidacji',
 'nl': 'opdrachtvertolker bouwen|bronbestand|objectbestand|uitvoerbaar bestand|declaratiemap|opstartobject|bibliotheekbestand|koppelbestand',
 'sv': 'bygg kommandotolk|källfil|objektfil|körbar fil|deklarationskatalog|startobjekt|biblioteksfil|länkningsfil',
 'fi': 'rakenna komentotulkki|lähdetiedosto|kohdetiedosto|suoritettava tiedosto|esittelyhakemisto|käynnistyskohde|kirjastotiedosto|linkitystiedosto',
 'cs': 'sestavit interpret|zdrojový soubor|objektový soubor|spustitelný soubor|adresář deklarací|spouštěcí objekt|soubor knihovny|soubor sestavení',
 'hi': 'आदेश व्याख्याकार बनाना|स्रोत संचिका|वस्तु संचिका|निष्पादन संचिका|घोषणा निर्देशिका|आरंभ वस्तु|पुस्तकालय संचिका|संयोजन संचिका',
 'bn': 'আদেশ ব্যাখ্যাকারী নির্মাণ|উৎস নথি|অবজেক্ট নথি|নির্বাহযোগ্য নথি|ঘোষণার নির্দেশিকা|প্রারম্ভিক অবজেক্ট|সংগ্রহশালা নথি|সংযোগ নথি',
 'ta': 'கட்டளை விளக்கியை உருவாக்கு|மூலக் கோப்பு|பொருட் கோப்பு|இயக்கக் கோப்பு|அறிவிப்பு அடைவு|தொடக்கப் பொருள்|நூலகக் கோப்பு|இணைப்புக் கோப்பு',
 'ur': 'حکم کا مفسر بنانا|ماخذ فائل|آبجیکٹ فائل|قابل اجرا فائل|اعلانات کی فہرست|ابتدائی آبجیکٹ|کتب خانے کی فائل|ربط کی فائل',
}

COMMANDS = dict(zip('help echo pwd cat stat pid uname run udp source'.split(),
                    'print_help command_echo command_pwd command_cat command_stat command_pid command_uname command_run command_udp command_source'.split()))
# These builtins have no distinct private function; their aliases are explicit.
EXTRA_COMMANDS = {
 'en': ('change_directory', 'leave'), 'ko': ('경로이동', '나가기'),
 'ja': ('場所を変える', '終了'), 'zh_Hans': ('切换目录', '退出'), 'zh_Hant': ('切換目錄', '離開'),
 'de': ('Verzeichnis_wechseln', 'beenden'), 'fr': ('changer_de_répertoire', 'quitter'),
 'es': ('cambiar_directorio', 'salir'), 'pt': ('mudar_diretório', 'sair'),
 'it': ('cambia_cartella', 'esci'), 'ru': ('сменить_каталог', 'выйти'),
 'uk': ('змінити_каталог', 'вийти'), 'ar': ('تغيير_المجلد', 'خروج'),
 'tr': ('dizin_değiştir', 'çık'), 'vi': ('đổi_thư_mục', 'thoát'),
 'id': ('ubah_direktori', 'keluar'), 'ms_Latn': ('tukar_direktori', 'keluar'),
 'pl': ('zmień_katalog', 'wyjdź'), 'nl': ('map_wisselen', 'verlaten'),
 'sv': ('byt_katalog', 'avsluta'), 'fi': ('vaihda_hakemistoa', 'poistu'),
 'cs': ('změnit_adresář', 'ukončit'), 'hi': ('निर्देशिका_बदलना', 'बाहर'),
 'bn': ('নির্দেশিকা_বদলানো', 'প্রস্থান'), 'ta': ('அடைவை_மாற்று', 'வெளியேறு'),
 'ur': ('فہرست_بدلنا', 'خروج'),
}

EXTRA_KEYS = ('INPUT_LINE_CAPACITY MAX_ARGUMENT_COUNT MAX_SCRIPT_DEPTH script_depth digit_text size number '
              'operation input_descriptor overflow buffer name child_pid wait_status receive_address source_address '
              'source_address_length received_data message_length message receive_socket send_socket received_length '
              'cleanup command_names command_aliases bytes_written').split()
EXTRA = {
 'de': 'Eingabezeilenkapazität|maximale Argumentanzahl|maximale Skriptverschachtelung|Skriptverschachtelungstiefe|Ziffernzeichen|Ziffernanzahl|vorzeichenloser Betrag|Operation|Eingabedeskriptor|ungültige Eingabezeile|Übertragungspuffer|Systemidentität|Kindprozesskennung|Beendigungsstatus des Kindprozesses|Empfängeradresse|Absenderadresse|Absenderadresslänge|empfangene Daten|Nachrichtenlänge in Bytes|Nachricht|Empfangssockel|Sendesockel|empfangene Byteanzahl|Sockel schließen|Grundbefehle|lokale Befehlsnamen|geschriebene Byteanzahl',
 'fr': 'capacité de la ligne d’entrée|nombre maximal d’arguments|imbrication maximale des scripts|profondeur d’imbrication des scripts|caractères des chiffres|nombre de chiffres|grandeur sans signe|opération|descripteur d’entrée|ligne d’entrée invalide|tampon de transfert|identité du système|identifiant du processus enfant|état de terminaison de l’enfant|adresse de réception|adresse de l’expéditeur|longueur de l’adresse de l’expéditeur|données reçues|longueur du message en octets|message|point de réception|point d’envoi|nombre d’octets reçus|fermer les points de communication|commandes de référence|alias locaux des commandes|nombre d’octets écrits',
 'es': 'capacidad de la línea de entrada|máximo de argumentos|máximo anidamiento de archivos de órdenes|profundidad de anidamiento|caracteres de los dígitos|cantidad de dígitos|magnitud sin signo|operación|descriptor de entrada|línea de entrada inválida|memoria intermedia de transferencia|identidad del sistema|identificador del proceso hijo|estado de terminación del hijo|dirección de recepción|dirección del remitente|longitud de la dirección del remitente|datos recibidos|longitud del mensaje en octetos|mensaje|extremo receptor|extremo emisor|cantidad de octetos recibidos|cerrar extremos de comunicación|órdenes de referencia|alias locales de órdenes|cantidad de octetos escritos',
 'pt': 'capacidade da linha de entrada|máximo de argumentos|máximo de níveis de comandos|profundidade dos níveis de comandos|caracteres dos algarismos|número de algarismos|magnitude sem sinal|operação|descritor de entrada|linha de entrada inválida|memória intermédia de transferência|identidade do sistema|identificador do processo filho|estado de terminação do filho|endereço de receção|endereço do remetente|comprimento do endereço do remetente|dados recebidos|comprimento da mensagem em octetos|mensagem|extremidade recetora|extremidade emissora|número de octetos recebidos|fechar extremidades de comunicação|comandos de referência|nomes locais dos comandos|número de octetos escritos',
 'it': 'capacità della riga di ingresso|numero massimo di argomenti|annidamento massimo dei comandi|profondità di annidamento dei comandi|caratteri delle cifre|numero di cifre|grandezza senza segno|operazione|descrittore di ingresso|riga di ingresso non valida|memoria intermedia di trasferimento|identità del sistema|identificatore del processo figlio|stato di terminazione del figlio|indirizzo ricevente|indirizzo del mittente|lunghezza dell’indirizzo del mittente|dati ricevuti|lunghezza del messaggio in ottetti|messaggio|estremità ricevente|estremità trasmittente|numero di ottetti ricevuti|chiudi estremità di comunicazione|comandi di riferimento|nomi locali dei comandi|numero di ottetti scritti',
 'ru': 'вместимость строки ввода|максимальное число аргументов|максимальная вложенность командных файлов|глубина вложенности командных файлов|символы цифр|число цифр|модуль без знака|операция|дескриптор ввода|недопустимая строка ввода|буфер передачи|сведения о системе|номер дочернего процесса|состояние завершения дочернего процесса|адрес получателя|адрес отправителя|длина адреса отправителя|принятые данные|длина сообщения в байтах|сообщение|приёмная конечная точка|передающая конечная точка|число принятых байтов|закрыть конечные точки|основные команды|местные имена команд|число записанных байтов',
 'uk': 'місткість рядка введення|максимальна кількість аргументів|максимальна вкладеність командних файлів|глибина вкладеності командних файлів|символи цифр|кількість цифр|модуль без знака|операція|дескриптор введення|неприпустимий рядок введення|буфер передавання|відомості про систему|номер дочірнього процесу|стан завершення дочірнього процесу|адреса отримувача|адреса відправника|довжина адреси відправника|отримані дані|довжина повідомлення в байтах|повідомлення|приймальна кінцева точка|передавальна кінцева точка|кількість отриманих байтів|закрити кінцеві точки|основні команди|місцеві назви команд|кількість записаних байтів',
 'ar': 'سعة سطر الإدخال|الحد الأقصى لعدد المعاملات|الحد الأقصى لتداخل ملفات الأوامر|عمق تداخل ملفات الأوامر|محارف الأرقام|عدد الخانات|المقدار بلا إشارة|العملية|واصف الإدخال|سطر إدخال غير صالح|مخزن النقل المؤقت|هوية النظام|معرف العملية الفرعية|حالة انتهاء العملية الفرعية|عنوان الاستقبال|عنوان المرسل|طول عنوان المرسل|البيانات المستلمة|طول الرسالة بالبايت|الرسالة|نقطة اتصال الاستقبال|نقطة اتصال الإرسال|عدد البايتات المستلمة|إغلاق نقاط الاتصال|الأوامر المرجعية|أسماء الأوامر المحلية|عدد البايتات المكتوبة',
 'tr': 'girdi satırı kapasitesi|en fazla bağımsız değişken sayısı|en fazla komut dosyası iç içeliği|komut dosyası iç içelik derinliği|rakam karakterleri|rakam sayısı|işaretsiz büyüklük|işlem|girdi tanımlayıcısı|geçersiz girdi satırı|aktarım ara belleği|sistem kimliği|çocuk süreç kimliği|çocuk sürecin sonlanma durumu|alıcı adresi|gönderen adresi|gönderen adresinin uzunluğu|alınan veri|iletinin bayt uzunluğu|ileti|alıcı iletişim ucu|gönderici iletişim ucu|alınan bayt sayısı|iletişim uçlarını kapat|temel komutlar|yerel komut adları|yazılan bayt sayısı',
 'vi': 'sức chứa dòng nhập|số đối số tối đa|độ lồng tệp lệnh tối đa|độ sâu lồng tệp lệnh|ký tự chữ số|số chữ số|độ lớn không dấu|thao tác|bộ mô tả đầu vào|dòng nhập không hợp lệ|bộ đệm truyền|thông tin hệ thống|mã tiến trình con|trạng thái kết thúc tiến trình con|địa chỉ nhận|địa chỉ bên gửi|độ dài địa chỉ bên gửi|dữ liệu đã nhận|độ dài thông điệp theo byte|thông điệp|đầu giao tiếp nhận|đầu giao tiếp gửi|số byte đã nhận|đóng các đầu giao tiếp|lệnh chuẩn|tên lệnh bản địa|số byte đã ghi',
 'id': 'kapasitas baris masukan|jumlah argumen maksimum|kedalaman berkas perintah maksimum|kedalaman berkas perintah|karakter digit|jumlah digit|besar tanpa tanda|operasi|deskriptor masukan|baris masukan tidak sah|penyangga transfer|identitas sistem|pengenal proses anak|status penghentian proses anak|alamat penerima|alamat pengirim|panjang alamat pengirim|data diterima|panjang pesan dalam byte|pesan|ujung komunikasi penerima|ujung komunikasi pengirim|jumlah byte diterima|tutup ujung komunikasi|perintah acuan|nama perintah setempat|jumlah byte ditulis',
 'ms_Latn': 'kapasiti baris masukan|bilangan argumen maksimum|kedalaman fail perintah maksimum|kedalaman fail perintah|aksara digit|bilangan digit|magnitud tanpa tanda|operasi|pemerihal masukan|baris masukan tidak sah|penimbal pemindahan|identiti sistem|pengenal proses anak|keadaan penamatan proses anak|alamat penerima|alamat penghantar|panjang alamat penghantar|data diterima|panjang mesej dalam bait|mesej|hujung komunikasi penerima|hujung komunikasi penghantar|bilangan bait diterima|tutup hujung komunikasi|perintah rujukan|nama perintah tempatan|bilangan bait ditulis',
 'pl': 'pojemność wiersza wejścia|maksymalna liczba argumentów|maksymalne zagnieżdżenie plików poleceń|głębokość zagnieżdżenia plików poleceń|znaki cyfr|liczba cyfr|wartość bez znaku|operacja|deskryptor wejścia|nieprawidłowy wiersz wejścia|bufor przesyłania|tożsamość systemu|identyfikator procesu potomnego|stan zakończenia procesu potomnego|adres odbiorcy|adres nadawcy|długość adresu nadawcy|odebrane dane|długość wiadomości w bajtach|wiadomość|punkt odbiorczy|punkt nadawczy|liczba odebranych bajtów|zamknij punkty komunikacji|polecenia podstawowe|lokalne nazwy poleceń|liczba zapisanych bajtów',
 'nl': 'capaciteit van invoerregel|maximaal aantal argumenten|maximale opdrachtnesting|diepte van opdrachtnesting|cijfertekens|aantal cijfers|grootte zonder teken|bewerking|invoerdescriptor|ongeldige invoerregel|overdrachtsbuffer|systeemidentiteit|nummer van kindproces|eindstatus van kindproces|ontvangstadres|afzenderadres|lengte van afzenderadres|ontvangen gegevens|berichtlengte in bytes|bericht|ontvangend communicatiepunt|verzendend communicatiepunt|aantal ontvangen bytes|communicatiepunten sluiten|basisopdrachten|lokale opdrachtnamen|aantal geschreven bytes',
 'sv': 'inmatningsradens kapacitet|högsta antal argument|högsta kommandonästling|kommandonästlingens djup|siffertecken|antal siffror|storlek utan tecken|åtgärd|inmatningsbeskrivare|ogiltig inmatningsrad|överföringsbuffert|systemidentitet|barnprocessens identifierare|barnprocessens avslutningsstatus|mottagaradress|avsändaradress|avsändaradressens längd|mottagna data|meddelandets längd i byte|meddelande|mottagande kommunikationspunkt|sändande kommunikationspunkt|antal mottagna byte|stäng kommunikationspunkter|grundkommandon|lokala kommandonamn|antal skrivna byte',
 'fi': 'syöterivin kapasiteetti|argumenttien enimmäismäärä|komentotiedostojen enimmäissisäkkäisyys|komentotiedostojen sisäkkäisyyssyvyys|numeromerkit|numeroiden määrä|etumerkitön suuruus|toiminto|syötekuvaaja|virheellinen syöterivi|siirtopuskuri|järjestelmätiedot|lapsiprosessin tunnus|lapsiprosessin päättymistila|vastaanottajan osoite|lähettäjän osoite|lähettäjän osoitteen pituus|vastaanotetut tiedot|viestin pituus tavuina|viesti|vastaanottava yhteyspiste|lähettävä yhteyspiste|vastaanotettujen tavujen määrä|sulje yhteyspisteet|peruskomennot|paikalliset komentonimet|kirjoitettujen tavujen määrä',
 'cs': 'kapacita vstupního řádku|maximální počet argumentů|maximální vnoření příkazových souborů|hloubka vnoření příkazových souborů|znaky číslic|počet číslic|velikost bez znaménka|operace|vstupní deskriptor|neplatný vstupní řádek|vyrovnávací paměť přenosu|identita systému|identifikátor potomka|stav ukončení potomka|adresa příjemce|adresa odesílatele|délka adresy odesílatele|přijatá data|délka zprávy v bajtech|zpráva|přijímací koncový bod|odesílací koncový bod|počet přijatých bajtů|zavřít komunikační body|základní příkazy|místní názvy příkazů|počet zapsaných bajtů',
 'hi': 'निवेश पंक्ति की क्षमता|तर्कों की अधिकतम संख्या|आदेश संचिकाओं का अधिकतम अंतःस्थापन|आदेश संचिकाओं की अंतःस्थापन गहराई|अंकों के वर्ण|अंकों की संख्या|चिह्न रहित परिमाण|क्रिया|निवेश विवरणक|अमान्य निवेश पंक्ति|स्थानांतरण का अस्थायी भंडार|प्रणाली की पहचान|संतति प्रक्रिया का क्रमांक|संतति प्रक्रिया की समाप्ति स्थिति|प्राप्तकर्ता का पता|प्रेषक का पता|प्रेषक के पते की लंबाई|प्राप्त आँकड़े|संदेश की बाइट लंबाई|संदेश|प्राप्ति संचार सिरा|प्रेषण संचार सिरा|प्राप्त बाइटों की संख्या|संचार सिरे बंद करना|आधार आदेश|स्थानीय आदेश नाम|लिखे गए बाइटों की संख्या',
 'bn': 'নিবেশ পঙ্‌ক্তির ধারণক্ষমতা|আর্গুমেন্টের সর্বোচ্চ সংখ্যা|আদেশ নথির সর্বোচ্চ অন্তর্ভুক্তি|আদেশ নথির অন্তর্ভুক্তির গভীরতা|অঙ্কের অক্ষর|অঙ্কের সংখ্যা|চিহ্নবিহীন পরিমাণ|ক্রিয়া|নিবেশ নির্দেশক|অবৈধ নিবেশ পঙ্‌ক্তি|স্থানান্তরের অস্থায়ী ভান্ডার|ব্যবস্থার পরিচয়|সন্তান প্রক্রিয়ার পরিচয়|সন্তান প্রক্রিয়ার সমাপ্তির অবস্থা|গ্রাহকের ঠিকানা|প্রেরকের ঠিকানা|প্রেরকের ঠিকানার দৈর্ঘ্য|প্রাপ্ত তথ্য|বার্তার বাইট দৈর্ঘ্য|বার্তা|গ্রহণের যোগাযোগ প্রান্ত|প্রেরণের যোগাযোগ প্রান্ত|প্রাপ্ত বাইটের সংখ্যা|যোগাযোগ প্রান্ত বন্ধ করা|মূল আদেশ|স্থানীয় আদেশের নাম|লিখিত বাইটের সংখ্যা',
 'ta': 'உள்ளீட்டு வரியின் கொள்ளளவு|செயலுருபுகளின் உச்ச எண்ணிக்கை|கட்டளைக் கோப்புகளின் உச்ச அடுக்கு|கட்டளைக் கோப்புகளின் அடுக்கு ஆழம்|இலக்க எழுத்துகள்|இலக்கங்களின் எண்ணிக்கை|குறியற்ற அளவு|செயல்|உள்ளீட்டு விவரிப்பி|செல்லாத உள்ளீட்டு வரி|பரிமாற்ற இடையகம்|அமைப்பின் அடையாளம்|சேய் செயல்முறையின் அடையாளம்|சேய் செயல்முறையின் முடிவு நிலை|பெறுநரின் முகவரி|அனுப்புநரின் முகவரி|அனுப்புநரின் முகவரி நீளம்|பெற்ற தரவு|செய்தியின் எண்மி நீளம்|செய்தி|பெறும் தொடர்பு முனை|அனுப்பும் தொடர்பு முனை|பெற்ற எண்மிகளின் எண்ணிக்கை|தொடர்பு முனைகளை மூடு|அடிப்படைக் கட்டளைகள்|உள்ளூர் கட்டளைப் பெயர்கள்|எழுதிய எண்மிகளின் எண்ணிக்கை',
 'ur': 'اندراج کی سطر کی گنجائش|دلائل کی زیادہ سے زیادہ تعداد|احکامات کی فائلوں کی زیادہ سے زیادہ تہیں|احکامات کی فائلوں کی تہہ کی گہرائی|ہندسوں کے حروف|ہندسوں کی تعداد|بغیر علامت مقدار|عمل|اندراج کا وصف کنندہ|غلط اندراج کی سطر|منتقلی کا عارضی ذخیرہ|نظام کی شناخت|ذیلی عمل کی شناخت|ذیلی عمل کے اختتام کی حالت|وصول کنندہ کا پتہ|بھیجنے والے کا پتہ|بھیجنے والے کے پتے کی لمبائی|موصولہ مواد|پیغام کی بائٹ لمبائی|پیغام|وصولی کا مواصلاتی سرا|ترسیل کا مواصلاتی سرا|موصولہ بائٹ کی تعداد|مواصلاتی سرے بند کرنا|بنیادی احکامات|احکامات کے مقامی نام|لکھے گئے بائٹ کی تعداد',
 'en': 'input line capacity|maximum argument count|maximum script nesting|script nesting depth|digit characters|digit count|unsigned magnitude|operation|input descriptor|line overflow|transfer buffer|system identity|child process identifier|child termination status|receiving endpoint address|sender endpoint address|sender address length|received data|message byte length|message|receiving socket|sending socket|received byte count|close sockets|canonical commands|native command aliases|written byte count',
 'ko': '입력줄 수용량|최대 인수 개수|최대 명령파일 중첩|명령파일 중첩 깊이|숫자 문자들|자릿수|부호없는 크기|실행 연산|입력 서술번호|입력줄 넘침|전달 완충공간|운영체제 식별정보|자식 실행과정 번호|자식 종료 상태|수신 접속점 주소|송신 접속점 주소|송신주소 길이|수신 자료|전문 바이트 길이|전문|수신 통신끝점|송신 통신끝점|수신 바이트수|통신끝점 닫기|기준 명령들|현지어 명령 별칭|쓴 바이트수',
 'ja': '入力行容量|最大引数数|命令文書の最大入れ子数|命令文書の入れ子の深さ|数字の文字列|桁数|符号なしの大きさ|処理|入力記述番号|入力行の超過|転送緩衝領域|体系識別情報|子実行過程の番号|子実行過程の終了状態|受信端点の番地|送信端点の番地|送信元番地の長さ|受信資料|電文の八桁組数|電文|受信通信端点|送信通信端点|受信八桁組数|通信端点を閉じる|基準命令|現地語命令別名|書き出した八桁組数',
 'zh_Hans': '输入行容量|最大参数个数|最大命令文件嵌套层数|命令文件嵌套深度|数字字符|数位个数|无符号数值|操作|输入描述符|输入行溢出|传输缓冲区|系统身份信息|子进程编号|子进程终止状态|接收端点地址|发送端点地址|发送地址长度|收到的数据|消息字节长度|消息|接收套接字|发送套接字|接收字节数|关闭套接字|基准命令|本地语言命令别名|已写字节数',
 'zh_Hant': '輸入列容量|最大引數個數|最大命令檔案巢狀層數|命令檔案巢狀深度|數字字元|數位個數|無號數值|操作|輸入描述元|輸入列溢位|傳輸緩衝區|系統識別資訊|子行程編號|子行程終止狀態|接收端點位址|傳送端點位址|傳送位址長度|收到的資料|訊息位元組長度|訊息|接收通訊端|傳送通訊端|接收位元組數|關閉通訊端|基準命令|本地語言命令別名|已寫位元組數',
}

def vocabulary(language):
    result = {}
    for keys, source in [(FUNCTION_KEYS, FUNCTIONS), (FIELD_KEYS, FIELDS), (HOST_KEYS, HOST), (EXTRA_KEYS, EXTRA)]:
        if language in source:
            values = source[language].split('|')
            if len(values) != len(keys):
                raise ValueError('Bad shell terminology row: ' + language)
            result.update(zip(keys, values))
    stream_terms = {
        'en': ('input stream', 'input'), 'ko': ('입력자료흐름', '입력'),
        'ja': ('入力資料流', '入力'), 'zh_Hans': ('输入流', '输入'), 'zh_Hant': ('輸入串流', '輸入'),
        'de': ('Eingabestrom', 'Eingabe'), 'fr': ('flux d’entrée', 'entrée'),
        'es': ('flujo de entrada', 'entrada'), 'pt': ('fluxo de entrada', 'entrada'),
        'it': ('flusso di ingresso', 'ingresso'), 'ru': ('поток ввода', 'ввод'),
        'uk': ('потік введення', 'введення'), 'ar': ('تدفق الإدخال', 'الإدخال'),
        'tr': ('girdi akışı', 'girdi'), 'vi': ('luồng đầu vào', 'đầu vào'),
        'id': ('aliran masukan', 'masukan'), 'ms_Latn': ('aliran masukan', 'masukan'),
        'pl': ('strumień wejściowy', 'wejście'), 'nl': ('invoerstroom', 'invoer'),
        'sv': ('inmatningsström', 'inmatning'), 'fi': ('syötevirta', 'syöte'),
        'cs': ('vstupní proud', 'vstup'), 'hi': ('निवेश धारा', 'निवेश'),
        'bn': ('নিবেশের প্রবাহ', 'নিবেশ'), 'ta': ('உள்ளீட்டு ஓடை', 'உள்ளீடு'),
        'ur': ('اندراج کا بہاؤ', 'اندراج'),
    }
    if language in stream_terms:
        result.update(zip(('input_stream', 'input'), stream_terms[language]))
    # This helper counts encoded bytes, not Unicode characters or graphemes.
    byte_length_terms = {
        'en': 'text byte length', 'ko': '문자열 여덟자리묶음 길이',
        'ja': '文字列の八桁組数', 'zh_Hans': '文本字节长度', 'zh_Hant': '文字位元組長度',
        'de': 'Textlänge in Bytes', 'fr': 'longueur du texte en octets',
        'es': 'longitud del texto en octetos', 'pt': 'comprimento do texto em octetos',
        'it': 'lunghezza del testo in ottetti', 'ru': 'длина текста в байтах',
        'uk': 'довжина тексту в байтах', 'ar': 'طول النص بالبايت',
        'tr': 'metnin bayt uzunluğu', 'vi': 'độ dài văn bản theo byte',
        'id': 'panjang teks dalam byte', 'ms_Latn': 'panjang teks dalam bait',
        'pl': 'długość tekstu w bajtach', 'nl': 'tekstlengte in bytes',
        'sv': 'textlängd i byte', 'fi': 'tekstin pituus tavuina',
        'cs': 'délka textu v bajtech', 'hi': 'पाठ की बाइट लंबाई',
        'bn': 'পাঠের বাইট দৈর্ঘ্য', 'ta': 'உரையின் எண்மி நீளம்',
        'ur': 'متن کی بائٹ لمبائی',
    }
    if language in byte_length_terms:
        result['text_length'] = byte_length_terms[language]
    invalid_line_terms = {
        'en': 'invalid input line', 'ko': '잘못된 입력줄', 'ja': '不正な入力行',
        'zh_Hans': '无效输入行', 'zh_Hant': '無效輸入列',
    }
    if language in invalid_line_terms:
        result['overflow'] = invalid_line_terms[language]
    if language == 'ko':
        # Project neologisms: file as an organized collection (자료철), byte as
        # the current eight-binary-position unit. Do not merely respell English.
        result = {key: value.replace('파일', '자료철').replace('바이트', '여덟자리묶음').replace('기계코드', '기계명령')
                  for key, value in result.items()}
        result['command_run'] = '실행자료철 가동'
    return result
