"""WorldOS project proposals, not official terminology or native-speaker certification.

Whole phrases are intentional: do not word-for-word translate an English order.
Blank/unlisted entries require linguistic review. Technical identity lives in the
concept keys and the original-source mapping, not in a fabricated translation.
"""

CORE_KEYS = 'internet ethernet_frame pointer register bus mouse widget heap stack page_directory page_frame bitmap boot_record fat_parameters elf list_node source_port destination_port'.split()
CORE = {
    'en': 'interconnected network|shared medium network frame|address reference|register|shared transfer bus|pointing device|screen element|dynamic memory|stack storage|page directory|physical page|allocation bitmap|master boot record|file system parameters|executable and linkable format|list node|source port number|destination port number',
    'ko': '상호연결망|공유매체망전송틀|주소참조|저장기|공용전송로|위치입력기|화면요소|동적기억공간|쌓임공간|기억쪽상위표|물리기억쪽|사용표시표|주시동기록|파일체계매개변수|실행연결형식|연결항목|출발지통신접속번호|목적지통신접속번호',
    'ja': '相互接続網|共有媒体網伝送枠|番地参照|値保持器|共用伝送路|位置入力装置|画面要素|動的記憶領域|積重ね記憶領域|記憶頁上位表|物理記憶頁|割当ビット表|主起動記録|ファイル体系設定値|実行連結形式|連結要素|送信元接続番号|宛先接続番号',
    'zh_Hans': '互联网络|共享介质网络帧|地址引用|寄存器|共享传输总线|指向设备|界面元素|动态存储区|栈存储区|页目录|物理页|分配位图|主引导记录|文件系统参数|可执行与可链接格式|链表节点|源端口号|目标端口号',
    'zh_Hant': '互聯網路|共享媒介網路框|位址參照|暫存器|共用傳輸匯流排|指向裝置|介面元素|動態記憶區|堆疊記憶區|頁目錄|實體頁|配置位元圖|主開機紀錄|檔案系統參數|可執行與可連結格式|鏈結串列節點|來源通訊埠號|目的通訊埠號',
    'de': 'Netzverbund|Rahmen des gemeinsamen Übertragungsnetzes|Adressverweis|Register|gemeinsamer Übertragungsweg|Zeigegerät|Bildschirmelement|dynamischer Speicher|Stapelspeicher|Seitenverzeichnis|physische Speicherseite|Belegungsbitkarte|Hauptstartdatensatz|Dateisystemparameter|ausführbares und bindbares Format|Listenknoten|Quellportnummer|Zielportnummer',
    'fr': 'réseau interconnecté|trame du réseau à support partagé|référence mémoire|registre|voie de transmission partagée|dispositif de pointage|élément graphique|mémoire dynamique|mémoire de pile|répertoire de pages|page physique|carte des allocations|enregistrement principal de démarrage|paramètres du système de fichiers|format exécutable et liable|maillon de liste|numéro du port source|numéro du port destination',
    'es': 'red interconectada|trama de la red de medio compartido|referencia de memoria|registro|vía de transmisión compartida|dispositivo señalador|elemento de pantalla|memoria dinámica|memoria de pila|directorio de páginas|página física|mapa de asignación|registro principal de arranque|parámetros del sistema de archivos|formato ejecutable y enlazable|nodo de lista|número del puerto de origen|número del puerto de destino',
    'pt': 'rede interligada|quadro da rede de meio partilhado|referência de memória|registo|via de transmissão partilhada|dispositivo apontador|elemento de ecrã|memória dinâmica|memória de pilha|diretório de páginas|página física|mapa de alocação|registo principal de arranque|parâmetros do sistema de ficheiros|formato executável e ligável|nó da lista|número da porta de origem|número da porta de destino',
    'it': 'rete interconnessa|trama della rete a mezzo condiviso|riferimento di memoria|registro|via di trasmissione condivisa|dispositivo di puntamento|elemento grafico|memoria dinamica|memoria a pila|indice delle pagine|pagina fisica|mappa di allocazione|record principale di avvio|parametri del file system|formato eseguibile e collegabile|nodo della lista|numero della porta sorgente|numero della porta di destinazione',
    'ru': 'объединённая сеть|кадр сети с общей средой|ссылка на адрес|регистр|общая шина передачи|устройство указания|элемент экрана|динамическая память|стековая память|каталог страниц|физическая страница|карта занятости|главная загрузочная запись|параметры файловой системы|исполняемый и компонуемый формат|узел списка|номер порта отправителя|номер порта получателя',
    'uk': 'обʼєднана мережа|кадр мережі зі спільним середовищем|посилання на адресу|регістр|спільна шина передавання|вказівний пристрій|елемент екрана|динамічна памʼять|стекова памʼять|каталог сторінок|фізична сторінка|карта зайнятості|головний завантажувальний запис|параметри файлової системи|виконуваний і компонований формат|вузол списку|номер порту відправника|номер порту одержувача',
    'ar': 'شبكة مترابطة|إطار شبكة ذات وسط مشترك|مرجع عنوان|مسجل|مسار نقل مشترك|جهاز تأشير|عنصر شاشة|ذاكرة ديناميكية|ذاكرة مكدس|دليل الصفحات|صفحة فعلية|خريطة التخصيص|سجل الإقلاع الرئيسي|معلمات نظام الملفات|صيغة التنفيذ والربط|عقدة قائمة|رقم منفذ المصدر|رقم منفذ الوجهة',
    'tr': 'ağlar arası ağ|ortak ortam ağ çerçevesi|adres başvurusu|yazmaç|ortak aktarım yolu|işaretleme aygıtı|ekran öğesi|dinamik bellek|yığın belleği|sayfa dizini|fiziksel sayfa|ayırma bit eşlemi|ana önyükleme kaydı|dosya sistemi parametreleri|çalıştırılabilir ve bağlanabilir biçim|liste düğümü|kaynak kapı numarası|hedef kapı numarası',
    'vi': 'mạng liên kết|khung mạng dùng chung môi trường truyền|tham chiếu địa chỉ|thanh ghi|đường truyền dùng chung|thiết bị trỏ|thành phần màn hình|bộ nhớ động|bộ nhớ ngăn xếp|thư mục trang|trang vật lý|bản đồ cấp phát|bản ghi khởi động chính|tham số hệ thống tệp|định dạng thực thi và liên kết|nút danh sách|số cổng nguồn|số cổng đích',
    'id': 'jaringan saling terhubung|bingkai jaringan media bersama|acuan alamat|register|jalur transmisi bersama|perangkat penunjuk|unsur layar|memori dinamis|memori tumpukan|direktori halaman|halaman fisik|peta alokasi|rekaman awal utama|parameter sistem berkas|format eksekusi dan penautan|simpul daftar|nomor porta sumber|nomor porta tujuan',
    'ms_Latn': 'rangkaian saling terhubung|bingkai rangkaian medium bersama|rujukan alamat|daftar|laluan penghantaran bersama|peranti penuding|unsur skrin|ingatan dinamik|ingatan tindanan|direktori halaman|halaman fizikal|peta peruntukan|rekod but utama|parameter sistem fail|format pelaksanaan dan pemautan|nod senarai|nombor port sumber|nombor port destinasi',
    'pl': 'sieć połączonych sieci|ramka sieci o wspólnym medium|odwołanie do adresu|rejestr|wspólna magistrala transmisji|urządzenie wskazujące|element ekranu|pamięć dynamiczna|pamięć stosu|katalog stron|strona fizyczna|mapa zajętości|główny rekord rozruchowy|parametry systemu plików|format wykonywalny i konsolidowalny|węzeł listy|numer portu źródłowego|numer portu docelowego',
    'nl': 'verbonden netwerk|frame van het gedeelde medium netwerk|adresverwijzing|register|gedeelde overdrachtsweg|aanwijsapparaat|schermelement|dynamisch geheugen|stapelgeheugen|paginamap|fysieke pagina|toewijzingskaart|hoofdopstartrecord|bestandssysteemparameters|uitvoerbaar en koppelbaar formaat|lijstknooppunt|bronpoortnummer|doelpoortnummer',
    'sv': 'sammankopplat nät|ram i nät med delat medium|adressreferens|register|gemensam överföringsväg|pekdon|skärmelement|dynamiskt minne|stackminne|sidkatalog|fysisk sida|tilldelningskarta|huvudstartpost|filsystemsparametrar|körbart och länkbart format|listnod|källportnummer|målportnummer',
    'fi': 'verkkojen verkko|jaetun siirtotien verkkokehys|osoiteviite|rekisteri|yhteinen siirtoväylä|osoitinlaite|näyttöelementti|dynaaminen muisti|pinomuisti|sivuhakemisto|fyysinen sivu|varausbittikartta|pääkäynnistystietue|tiedostojärjestelmän parametrit|suoritettava ja linkitettävä muoto|listasolmu|lähdeportin numero|kohdeportin numero',
    'cs': 'propojená síť|rámec sítě se sdíleným médiem|odkaz na adresu|registr|sdílená přenosová sběrnice|polohovací zařízení|prvek obrazovky|dynamická paměť|paměť zásobníku|adresář stránek|fyzická stránka|mapa obsazení|hlavní spouštěcí záznam|parametry souborového systému|spustitelný a spojitelný formát|uzel seznamu|číslo zdrojového portu|číslo cílového portu',
}

ACTION_KEYS = 'append prepend insert_at toggle_bit set_coordinates allocate_memory free_memory file_read file_write'.split()
ACTIONS = {
    'en': 'append to list|prepend to list|insert at index|toggle allocation bit|set local coordinates|allocate memory|release memory|read file|write file',
    'ko': '맨뒤에추가|맨앞에추가|지정위치에삽입|사용표시뒤집기|지역좌표설정|기억공간할당|기억공간해제|파일읽기|파일쓰기',
    'ja': '末尾に追加|先頭に追加|指定位置に挿入|割当ビットを反転|局所座標を設定|記憶領域を確保|記憶領域を解放|ファイルを読む|ファイルに書く',
    'zh_Hans': '追加到表尾|添加到表头|在指定位置插入|反转分配位|设置局部坐标|分配内存|释放内存|读取文件|写入文件',
    'zh_Hant': '附加至串列尾端|加入至串列開頭|在指定位置插入|反轉配置位元|設定局部座標|配置記憶體|釋放記憶體|讀取檔案|寫入檔案',
    'de': 'am Listenende anfügen|am Listenanfang einfügen|an Position einfügen|Belegungsbit umkehren|lokale Koordinaten setzen|Speicher reservieren|Speicher freigeben|Datei lesen|Datei schreiben',
    'fr': 'ajouter en fin de liste|ajouter en tête de liste|insérer à la position|inverser le bit de réservation|définir les coordonnées locales|allouer la mémoire|libérer la mémoire|lire le fichier|écrire le fichier',
    'es': 'añadir al final de la lista|añadir al inicio de la lista|insertar en la posición|invertir el bit de asignación|establecer las coordenadas locales|asignar memoria|liberar memoria|leer archivo|escribir archivo',
    'pt': 'adicionar ao fim da lista|adicionar ao início da lista|inserir na posição|inverter o bit de alocação|definir coordenadas locais|alocar memória|libertar memória|ler ficheiro|escrever ficheiro',
    'it': 'aggiungi in fondo alla lista|aggiungi in testa alla lista|inserisci alla posizione|inverti il bit di allocazione|imposta le coordinate locali|alloca memoria|libera memoria|leggi file|scrivi file',
    'ru': 'добавить в конец списка|добавить в начало списка|вставить по индексу|инвертировать бит занятости|задать локальные координаты|выделить память|освободить память|прочитать файл|записать файл',
    'uk': 'додати в кінець списку|додати на початок списку|вставити за індексом|інвертувати біт зайнятості|задати локальні координати|виділити памʼять|звільнити памʼять|прочитати файл|записати файл',
    'ar': 'إضافة إلى نهاية القائمة|إضافة إلى بداية القائمة|إدراج عند الفهرس|عكس بت التخصيص|تعيين الإحداثيات المحلية|تخصيص الذاكرة|تحرير الذاكرة|قراءة الملف|كتابة الملف',
    'tr': 'listenin sonuna ekle|listenin başına ekle|dizine göre araya ekle|ayırma bitini tersle|yerel koordinatları ayarla|bellek ayır|belleği serbest bırak|dosya oku|dosya yaz',
    'vi': 'thêm vào cuối danh sách|thêm vào đầu danh sách|chèn tại chỉ số|đảo bit cấp phát|đặt tọa độ cục bộ|cấp phát bộ nhớ|giải phóng bộ nhớ|đọc tệp|ghi tệp',
    'id': 'tambah di akhir daftar|tambah di awal daftar|sisipkan pada indeks|balik bit alokasi|atur koordinat lokal|alokasikan memori|bebaskan memori|baca berkas|tulis berkas',
    'ms_Latn': 'tambah di hujung senarai|tambah di awal senarai|sisip pada indeks|songsangkan bit peruntukan|tetapkan koordinat setempat|peruntukkan ingatan|bebaskan ingatan|baca fail|tulis fail',
    'pl': 'dodaj na końcu listy|dodaj na początku listy|wstaw pod indeksem|odwróć bit zajętości|ustaw współrzędne lokalne|przydziel pamięć|zwolnij pamięć|odczytaj plik|zapisz plik',
    'nl': 'achteraan toevoegen|vooraan toevoegen|op positie invoegen|toewijzingsbit omkeren|lokale coördinaten instellen|geheugen toewijzen|geheugen vrijgeven|bestand lezen|bestand schrijven',
    'sv': 'lägg till sist i listan|lägg till först i listan|infoga vid index|invertera tilldelningsbit|ange lokala koordinater|tilldela minne|frigör minne|läs fil|skriv fil',
    'fi': 'lisää listan loppuun|lisää listan alkuun|lisää indeksin kohdalle|käännä varausbitti|aseta paikalliset koordinaatit|varaa muistia|vapauta muisti|lue tiedosto|kirjoita tiedosto',
    'cs': 'přidat na konec seznamu|přidat na začátek seznamu|vložit na pozici|obrátit bit obsazení|nastavit místní souřadnice|přidělit paměť|uvolnit paměť|číst soubor|zapsat soubor',
}

PATH_KEYS = 'tools boot user_space implementation tests headers link_layout compile_kernel log_decoder structure_offsets system_call startup error_number file_control file_status'.split()
PATHS = {
    'en': 'tools|machine boot|user space|implementation|tests|headers|link layout|compile kernel|decode serial log|structure offsets|system call|startup|error number|file control|file status',
    'ko': '도구|기계시동|사용자영역|구현|시험|머리파일|연결배치|핵심컴파일|직렬기록해석|구조변위|체계호출|시동|오류번호|파일제어|파일상태',
    'ja': '補助道具|機械起動|利用者領域|実装|試験|宣言集|連結配置|中核翻訳|直列記録解析|構造変位|体系呼出し|起動|エラー番号|ファイル制御|ファイル状態',
    'zh_Hans': '工具|机器启动|用户空间|实现|测试|头文件|链接布局|编译内核|解析串行日志|结构偏移|系统调用|启动|错误编号|文件控制|文件状态',
    'zh_Hant': '工具|機器啟動|使用者空間|實作|測試|標頭檔|連結配置|編譯核心|解析序列紀錄|結構位移|系統呼叫|啟動|錯誤編號|檔案控制|檔案狀態',
    'de': 'Werkzeuge|Maschinenstart|Benutzerbereich|Implementierung|Prüfungen|Deklarationen|Bindungsanordnung|Kern übersetzen|serielles Protokoll auswerten|Strukturversätze|Systemaufruf|Start|Fehlernummer|Dateisteuerung|Dateistatus',
    'fr': 'outils|démarrage machine|espace utilisateur|implémentation|essais|déclarations|plan de liaison|compiler le noyau|décoder le journal série|décalages de structure|appel système|démarrage|numéro erreur|contrôle de fichier|état de fichier',
    'es': 'herramientas|arranque de máquina|espacio de usuario|implementación|pruebas|declaraciones|disposición de enlace|compilar núcleo|interpretar registro serie|desplazamientos de estructura|llamada al sistema|arranque|número de error|control de archivo|estado de archivo',
    'pt': 'ferramentas|arranque da máquina|espaço do utilizador|implementação|testes|declarações|disposição de ligação|compilar núcleo|interpretar registo série|deslocamentos de estrutura|chamada ao sistema|arranque|número de erro|controlo de ficheiro|estado de ficheiro',
    'it': 'strumenti|avvio macchina|spazio utente|implementazione|prove|dichiarazioni|disposizione di collegamento|compila nucleo|decodifica registro seriale|scostamenti di struttura|chiamata di sistema|avvio|numero di errore|controllo file|stato file',
    'ru': 'инструменты|запуск машины|пространство пользователя|реализация|испытания|объявления|схема компоновки|собрать ядро|разобрать последовательный журнал|смещения структуры|системный вызов|запуск|номер ошибки|управление файлом|состояние файла',
    'uk': 'інструменти|запуск машини|простір користувача|реалізація|випробування|оголошення|схема компонування|зібрати ядро|розібрати послідовний журнал|зсуви структури|системний виклик|запуск|номер помилки|керування файлом|стан файла',
    'ar': 'أدوات|إقلاع الآلة|فضاء المستخدم|تنفيذ|اختبارات|تصريحات|تخطيط الربط|ترجمة النواة|تحليل السجل التسلسلي|إزاحات البنية|نداء النظام|بدء التشغيل|رقم الخطأ|التحكم بالملف|حالة الملف',
    'tr': 'araçlar|makine başlatma|kullanıcı alanı|gerçekleme|sınamalar|bildirimler|bağlama düzeni|çekirdek derle|seri kaydı çözümle|yapı uzaklıkları|sistem çağrısı|başlatma|hata numarası|dosya denetimi|dosya durumu',
    'vi': 'công cụ|khởi động máy|không gian người dùng|triển khai|kiểm thử|khai báo|bố trí liên kết|biên dịch nhân|giải mã nhật ký nối tiếp|độ lệch cấu trúc|lời gọi hệ thống|khởi động|mã lỗi|điều khiển tệp|trạng thái tệp',
    'id': 'alat|awal mesin|ruang pengguna|implementasi|pengujian|deklarasi|tata letak penautan|kompilasi inti|urai catatan serial|ofset struktur|panggilan sistem|awal|nomor galat|kendali berkas|status berkas',
    'ms_Latn': 'alat|permulaan mesin|ruang pengguna|pelaksanaan|ujian|pengisytiharan|susun atur pautan|kompilasi teras|hurai log bersiri|anjakan struktur|panggilan sistem|permulaan|nombor ralat|kawalan fail|status fail',
    'pl': 'narzędzia|rozruch maszyny|przestrzeń użytkownika|implementacja|testy|deklaracje|układ konsolidacji|kompiluj jądro|odczytaj dziennik szeregowy|przesunięcia struktury|wywołanie systemowe|rozruch|numer błędu|sterowanie plikiem|stan pliku',
    'nl': 'hulpmiddelen|machineopstart|gebruikersruimte|implementatie|tests|declaraties|koppelindeling|kern compileren|serieel logboek ontleden|structuurverplaatsingen|systeemaanroep|opstart|foutnummer|bestandsbesturing|bestandsstatus',
    'sv': 'verktyg|maskinstart|användarutrymme|implementation|tester|deklarationer|länkningslayout|kompilera kärnan|tolka seriell logg|strukturförskjutningar|systemanrop|start|felnummer|filstyrning|filstatus',
    'fi': 'työkalut|koneen käynnistys|käyttäjätila|toteutus|testit|esittelyt|linkitysasettelu|käännä ydin|tulkitse sarjaloki|rakenteen siirtymät|järjestelmäkutsu|käynnistys|virhenumero|tiedoston ohjaus|tiedoston tila',
    'cs': 'nástroje|spuštění stroje|uživatelský prostor|implementace|zkoušky|deklarace|rozvržení spojování|přeložit jádro|zpracovat sériový záznam|posuny struktury|systémové volání|spuštění|číslo chyby|řízení souboru|stav souboru',
}

NETWORK_KEYS = 'ipv4 udp icmp ethernet_header ethernet_provider udp_socket udp_header ip_provider'.split()
NETWORK = {
    'en': 'interconnected network protocol 4|user datagram protocol|interconnected network control message protocol|shared medium network frame header|shared medium network frame provider|user datagram endpoint|user datagram header|interconnected network protocol provider',
    'ko': '상호연결망규약4|사용자자료전문규약|상호연결망제어전문규약|공유매체망전송틀머리부|공유매체망전송틀제공자|사용자자료전문종단점|사용자자료전문머리부|상호연결망규약제공자',
    'ja': '相互接続網規約4|利用者資料電文規約|相互接続網制御電文規約|共有媒体網伝送枠先頭部|共有媒体網伝送枠提供器|利用者資料電文通信端点|利用者資料電文先頭部|相互接続網規約提供器',
    'zh_Hans': '互联网络协议4|用户数据报协议|互联网络控制报文协议|共享介质网络帧头|共享介质网络帧提供器|用户数据报通信端点|用户数据报头|互联网络协议提供器',
    'zh_Hant': '互聯網路協定4|使用者資料報協定|互聯網路控制訊息協定|共享媒介網路框標頭|共享媒介網路框提供器|使用者資料報通訊端點|使用者資料報標頭|互聯網路協定提供器',
    'de': 'Netzverbundprotokoll4|Benutzerdatagrammprotokoll|Netzverbundsteuerprotokoll|Rahmenkopf des gemeinsamen Übertragungsnetzes|Rahmenanbieter des gemeinsamen Übertragungsnetzes|Benutzerdatagrammendpunkt|Benutzerdatagrammkopf|Netzverbundprotokollanbieter',
    'fr': 'protocole du réseau interconnecté 4|protocole des datagrammes utilisateur|protocole des messages de contrôle du réseau interconnecté|entête de trame du réseau à support partagé|fournisseur de trames du réseau à support partagé|point de communication des datagrammes utilisateur|entête des datagrammes utilisateur|fournisseur du protocole du réseau interconnecté',
    'es': 'protocolo de red interconectada 4|protocolo de datagramas de usuario|protocolo de mensajes de control de red interconectada|cabecera de trama de red de medio compartido|proveedor de tramas de red de medio compartido|extremo de comunicación de datagramas de usuario|cabecera de datagramas de usuario|proveedor del protocolo de red interconectada',
    'pt': 'protocolo de rede interligada 4|protocolo de datagramas do utilizador|protocolo de mensagens de controlo de rede interligada|cabeçalho de quadro de rede de meio partilhado|fornecedor de quadros de rede de meio partilhado|extremo de comunicação de datagramas do utilizador|cabeçalho de datagramas do utilizador|fornecedor do protocolo de rede interligada',
    'it': 'protocollo di rete interconnessa 4|protocollo dei datagrammi utente|protocollo dei messaggi di controllo della rete interconnessa|intestazione della trama di rete a mezzo condiviso|fornitore di trame di rete a mezzo condiviso|estremo di comunicazione dei datagrammi utente|intestazione dei datagrammi utente|fornitore del protocollo di rete interconnessa',
    'ru': 'протокол объединённой сети 4|протокол пользовательских датаграмм|протокол управляющих сообщений объединённой сети|заголовок кадра сети с общей средой|поставщик кадров сети с общей средой|конечная точка пользовательских датаграмм|заголовок пользовательской датаграммы|поставщик протокола объединённой сети',
    'uk': 'протокол обʼєднаної мережі 4|протокол користувацьких датаграм|протокол керувальних повідомлень обʼєднаної мережі|заголовок кадру мережі зі спільним середовищем|постачальник кадрів мережі зі спільним середовищем|кінцева точка користувацьких датаграм|заголовок користувацької датаграми|постачальник протоколу обʼєднаної мережі',
    'ar': 'بروتوكول الشبكة المترابطة 4|بروتوكول رزم المستخدم|بروتوكول رسائل التحكم بالشبكة المترابطة|ترويسة إطار الشبكة ذات الوسط المشترك|مزود إطارات الشبكة ذات الوسط المشترك|نقطة اتصال رزم المستخدم|ترويسة رزم المستخدم|مزود بروتوكول الشبكة المترابطة',
    'tr': 'ağlar arası ağ protokolü 4|kullanıcı veri birimi protokolü|ağlar arası ağ denetim iletisi protokolü|ortak ortam ağ çerçevesi başlığı|ortak ortam ağ çerçevesi sağlayıcısı|kullanıcı veri birimi iletişim uç noktası|kullanıcı veri birimi başlığı|ağlar arası ağ protokolü sağlayıcısı',
    'vi': 'giao thức mạng liên kết 4|giao thức gói tin người dùng|giao thức thông điệp điều khiển mạng liên kết|đầu khung mạng dùng chung môi trường truyền|bộ cung cấp khung mạng dùng chung môi trường truyền|điểm cuối gói tin người dùng|đầu gói tin người dùng|bộ cung cấp giao thức mạng liên kết',
    'id': 'protokol jaringan saling terhubung 4|protokol datagram pengguna|protokol pesan kendali jaringan saling terhubung|kepala bingkai jaringan media bersama|penyedia bingkai jaringan media bersama|titik akhir datagram pengguna|kepala datagram pengguna|penyedia protokol jaringan saling terhubung',
    'ms_Latn': 'protokol rangkaian saling terhubung 4|protokol datagram pengguna|protokol mesej kawalan rangkaian saling terhubung|pengepala bingkai rangkaian medium bersama|pembekal bingkai rangkaian medium bersama|titik akhir datagram pengguna|pengepala datagram pengguna|pembekal protokol rangkaian saling terhubung',
    'pl': 'protokół połączonych sieci 4|protokół datagramów użytkownika|protokół komunikatów sterujących połączonych sieci|nagłówek ramki sieci o wspólnym medium|dostawca ramek sieci o wspólnym medium|punkt końcowy datagramów użytkownika|nagłówek datagramu użytkownika|dostawca protokołu połączonych sieci',
    'nl': 'protocol voor verbonden netwerken 4|gebruikersdatagramprotocol|besturingsberichtprotocol voor verbonden netwerken|framekop van het gedeelde medium netwerk|frameleverancier van het gedeelde medium netwerk|gebruikersdatagrameindpunt|gebruikersdatagramkop|protocolleverancier voor verbonden netwerken',
    'sv': 'protokoll för sammankopplade nät 4|användardatagramprotokoll|styrmeddelandeprotokoll för sammankopplade nät|ramhuvud för nät med delat medium|ramleverantör för nät med delat medium|slutpunkt för användardatagram|huvud för användardatagram|protokolleverantör för sammankopplade nät',
    'fi': 'verkkojen yhdyskäytäntö 4|käyttäjän tietosähkeiden yhteyskäytäntö|verkkojen ohjausviestien yhteyskäytäntö|jaetun siirtotien verkkokehyksen otsake|jaetun siirtotien verkkokehysten tarjoaja|käyttäjän tietosähkeiden päätepiste|käyttäjän tietosähkeen otsake|verkkojen yhteyskäytännön tarjoaja',
    'cs': 'protokol propojených sítí 4|protokol uživatelských datagramů|protokol řídicích zpráv propojených sítí|hlavička rámce sítě se sdíleným médiem|poskytovatel rámců sítě se sdíleným médiem|koncový bod uživatelských datagramů|hlavička uživatelského datagramu|poskytovatel protokolu propojených sítí',
}

def lexicon():
    result = {}
    for keys, rows in ((CORE_KEYS, CORE), (ACTION_KEYS, ACTIONS), (PATH_KEYS, PATHS), (NETWORK_KEYS, NETWORK)):
        for language, text in rows.items():
            values = text.split('|')
            assert len(keys) == len(values), (language, len(keys), len(values))
            result.setdefault(language, {}).update(zip(keys, values))
    return result

# Exact complete source names: do not replace arbitrary substrings such as
# "frame" (network frame, physical page, and exception state are different).
IDENTIFIERS = {
    'PushBack': ('append', 'M'), 'PushFront': ('prepend', 'M'),
    'PushAt': ('insert_at', 'M'), 'UnsetBit': ('toggle_bit', 'M'),
    'ModelToScreen': ('set_coordinates', 'M'), 'Malloc': ('allocate_memory', 'M'),
    'ReadFile': ('file_read', 'M'), 'WriteFile': ('file_write', 'M'),
    'Node': ('list_node', 'T'), 'node': ('list_node', 'V'),
    'srcPort': ('source_port', 'V'), 'dstPort': ('destination_port', 'V'),
    'pageDir': ('page_directory', 'V'), 'bitmap': ('bitmap', 'V'),
    'TWidget': ('widget', 'T'), 'IWidget': ('widget', 'I'),
    'TMasterBootRecord': ('boot_record', 'T'), 'TBiosParameterBlock32': ('fat_parameters', 'T'),
    'pointer': ('pointer', 'V'), 'ptr': ('pointer', 'V'), 'stack': ('stack', 'V'),
    'bpb': ('fat_parameters', 'V'), 'mbr': ('boot_record', 'V'),
    'TEtherFrameHeader': ('ethernet_header', 'T'), 'TEtherFrameProvider': ('ethernet_provider', 'T'),
    'etherFrameProvider': ('ethernet_provider', 'V'),
    'TInternetProtocolProvider': ('ip_provider', 'T'), 'ipProvider': ('ip_provider', 'V'),
    'TInternetControlMessageProtocol': ('icmp', 'T'),
    'TUserDatagramProtocolHeader': ('udp_header', 'T'),
    'TUserDatagramProtocolSocket': ('udp_socket', 'T'),
}

# Original package paths, not translated words in unrelated strings.
PACKAGES = {
    'etherframe': 'ethernet_frame', 'widget': 'widget',
    'drivers/mouse': 'mouse', 'filesystem/elf': 'elf',
    'ipv4': 'ipv4', 'udp': 'udp', 'icmp': 'icmp',
}

RATIONALE = {
    'append': 'src/util/list/list.go: links after tail; back is not undo',
    'prepend': 'src/util/list/list.go: links before head',
    'insert_at': 'src/util/list/list.go: insertion at zero-based index',
    'toggle_bit': 'src/phymem/phymem.go: XOR; does not unconditionally clear the bit',
    'set_coordinates': 'src/widget/widget.go: assigns local x/y; no parent transform',
    'page_directory': 'src/paging/paging.go: upper-level page table, not a file directory',
    'page_frame': 'physical page, not an Ethernet frame or exception record',
    'ethernet_frame': 'Ethernet shared-medium history; not a claim that all modern links share a medium',
    'fat_parameters': 'FAT layout parameters, not a generic BIOS data block',
    'boot_record': 'boot code and partition metadata, not an audio recording',
    'elf': 'Executable AND Linkable Format; preserve both roles',
}
