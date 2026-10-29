"""Whole-command functional naming proposals, independent of source identifiers.

Standard command spellings remain accepted. A missing translation is explicit;
no unrelated language is substituted for a country's selected language.
"""
import json
import unicodedata

KEYS='ipconfig ip ping route netstat ps top free df uptime poweroff help'.split()
ROWS={
 'ko':'아이피설정|아이피|응답시험|경로표|통신현황|작업목록|작업현황|기억현황|저장현황|가동시간|전원끄기|도움말',
 'en':'address-settings|address|echo-test|routes|connections|processes|activity|memory|storage|running-time|shut-down|assistance',
 'ja':'通信設定|通信番地|応答試験|経路表|通信状況|作業一覧|稼働状況|記憶状況|保存容量|稼働時間|電源を切る|使い方',
 'zh_Hans':'网络设置|网络地址|回声测试|路由表|网络状态|进程列表|运行概况|内存状态|存储容量|运行时间|关机|帮助',
 'zh_Hant':'網路設定|網路位址|回聲測試|路由表|網路狀態|行程列表|執行概況|記憶體狀態|儲存容量|運作時間|關機|說明',
 'de':'Adresskonfiguration|Netzadresse|Antworttest|Wegetabelle|Netzverbindungen|Prozessliste|Aktivitätsübersicht|Speicherbelegung|Dateisystembelegung|Laufzeit|Ausschalten|Hilfe',
 'fr':'configurer-ip|adresse-ip|tester-écho|routes|connexions|processus|activité|mémoire|stockage|durée-active|éteindre|aide',
 'es':'configurar-ip|dirección-ip|probar-eco|rutas|conexiones|procesos|actividad|memoria|almacenamiento|tiempo-activo|apagar|ayuda',
 'pt':'configurar-ip|endereço-ip|testar-eco|rotas|ligações|processos|atividade|memória|armazenamento|tempo-ativo|desligar|ajuda',
 'it':'configura-ip|indirizzo-ip|prova-eco|percorsi|connessioni|processi|attività|memoria|archiviazione|tempo-attivo|spegni|aiuto',
 'nl':'ip-instellen|netwerkadres|antwoordtest|routes|verbindingen|processen|activiteit|geheugen|opslag|bedrijfstijd|uitschakelen|hulp',
 'ru':'настройка-ip|сетевой-адрес|проверка-отклика|маршруты|соединения|процессы|обзор-работы|память|хранилище|время-работы|выключить|справка',
 'uk':'налаштування-ip|мережева-адреса|перевірка-відгуку|маршрути|з’єднання|процеси|огляд-роботи|пам’ять|сховище|час-роботи|вимкнути|довідка',
 'be':'наладка-ip|сеткавы-адрас|праверка-водгуку|маршруты|злучэнні|працэсы|агляд-працы|памяць|сховішча|час-працы|выключыць|даведка',
 'bg':'настройка-ip|мрежов-адрес|проверка-отговор|маршрути|връзки|процеси|преглед-работа|памет|хранилище|време-работа|изключване|помощ',
 'ar':'إعداد-الشبكة|عنوان-الشبكة|اختبار-الصدى|المسارات|الاتصالات|العمليات|مراقبة-النشاط|الذاكرة|التخزين|مدة-التشغيل|إيقاف-التشغيل|مساعدة',
 'he':'הגדרות-רשת|כתובת-רשת|בדיקת-הד|נתיבים|חיבורים|תהליכים|פעילות|זיכרון|אחסון|זמן-פעולה|כיבוי|עזרה',
 'fa':'تنظیم-شبکه|نشانی-شبکه|آزمون-پژواک|مسیرها|اتصال‌ها|فرایندها|فعالیت|حافظه|ذخیره‌سازی|زمان-کار|خاموش|راهنما',
 'ur':'نیٹ-ترتیب|نیٹ-پتا|جواب-آزمائش|راستے|رابطے|عمل|سرگرمی|حافظہ|ذخیرہ|چلنے-کا-وقت|بند-کریں|مدد',
 'hi':'जाल-विन्यास|जाल-पता|प्रतिध्वनि-जाँच|मार्ग|प्रक्रिया-संपर्क|प्रक्रियाएँ|कार्य-स्थिति|स्मृति|भंडारण|कार्य-अवधि|बंद-करें|सहायता',
 'bn':'নেট-বিন্যাস|নেট-ঠিকানা|প্রতিধ্বনি-পরীক্ষা|পথ|সংযোগ|প্রক্রিয়া|কাজের-অবস্থা|স্মৃতি|সংরক্ষণ|চলমান-সময়|বন্ধ-করুন|সাহায্য',
 'ne':'सञ्जाल-विन्यास|सञ्जाल-ठेगाना|प्रतिध्वनि-परीक्षण|मार्ग|जडान|प्रक्रिया|कार्य-स्थिति|स्मृति|भण्डारण|चल्ने-अवधि|बन्द-गर्नुहोस्|सहायता',
 'tr':'ip-ayarları|ağ-adresi|yankı-sınaması|yollar|bağlantılar|süreçler|etkinlik|bellek|depolama|çalışma-süresi|kapat|yardım',
 'vi':'cấu-hình-ip|địa-chỉ-mạng|thử-phản-hồi|đường-đi|kết-nối|tiến-trình|hoạt-động|bộ-nhớ|lưu-trữ|thời-gian-chạy|tắt-máy|trợ-giúp',
 'th':'ตั้งค่าไอพี|ที่อยู่ไอพี|ทดสอบตอบกลับ|เส้นทาง|การเชื่อมต่อ|กระบวนการ|สถานะงาน|หน่วยความจำ|พื้นที่เก็บข้อมูล|เวลาทำงาน|ปิดเครื่อง|ช่วยเหลือ',
 'id':'atur-ip|alamat-ip|uji-gema|rute|koneksi|proses|aktivitas|memori|penyimpanan|waktu-aktif|matikan|bantuan',
 'ms_Latn':'tetapan-ip|alamat-ip|uji-gema|laluan|sambungan|proses|aktiviti|ingatan|storan|masa-aktif|matikan|bantuan',
 'pl':'ustawienia-ip|adres-sieci|test-echa|trasy|połączenia|procesy|aktywność|pamięć|miejsce|czas-pracy|wyłącz|pomoc',
 'cs':'nastavení-ip|síťová-adresa|zkouška-odezvy|trasy|spojení|procesy|činnost|paměť|úložiště|doba-běhu|vypnout|nápověda',
 'sk':'nastavenie-ip|sieťová-adresa|skúška-odozvy|trasy|spojenia|procesy|činnosť|pamäť|úložisko|doba-behu|vypnúť|pomoc',
 'sv':'ip-inställningar|nätadress|svarstest|rutter|anslutningar|processer|aktivitet|minne|lagring|drifttid|stäng-av|hjälp',
 'fi':'ip-asetukset|verkko-osoite|kaikutesti|reitit|yhteydet|prosessit|toiminta|muisti|tallennustila|käyntiaika|sammuta|ohje',
 'da':'ip-indstillinger|netadresse|svartest|ruter|forbindelser|processer|aktivitet|hukommelse|lagerplads|driftstid|sluk|hjælp',
 'nb':'ip-innstillinger|nettadresse|svartest|ruter|forbindelser|prosesser|aktivitet|minne|lagringsplass|oppetid|slå-av|hjelp',
 'is':'ip-stillingar|netfang|bergmálspróf|leiðir|tengingar|ferli|virkni|minni|geymsla|keyrslutími|slökkva|hjálp',
 'fo':'ip-stillingar|netadressa|svarroynd|leiðir|sambond|tilgongdir|virksemi|minni|goymsla|koyritíð|sløkk|hjálp',
 'hu':'ip-beállítás|hálózati-cím|visszhangpróba|útvonalak|kapcsolatok|folyamatok|tevékenység|memória|tárhely|üzemidő|kikapcsolás|súgó',
 'ro':'configurare-ip|adresă-ip|test-ecou|rute|conexiuni|procese|activitate|memorie|stocare|timp-activ|oprire|ajutor',
 'el':'ρύθμιση-ip|διεύθυνση-ip|δοκιμή-ηχούς|διαδρομές|συνδέσεις|διεργασίες|δραστηριότητα|μνήμη|αποθήκευση|χρόνος-λειτουργίας|τερματισμός|βοήθεια',
 'ca':'configuració-ip|adreça-ip|prova-eco|rutes|connexions|processos|activitat|memòria|emmagatzematge|temps-actiu|apagar|ajuda',
 'et':'ip-seaded|võrguaadress|kajakatse|marsruudid|ühendused|protsessid|tegevus|mälu|salvestusruum|tööaeg|lülita-välja|abi',
 'lv':'ip-iestatījumi|tīkla-adrese|atbalss-pārbaude|maršruti|savienojumi|procesi|darbība|atmiņa|krātuve|darbības-laiks|izslēgt|palīdzība',
 'lt':'ip-nustatymai|tinklo-adresas|aido-bandymas|maršrutai|ryšiai|procesai|veikla|atmintis|saugykla|veikimo-laikas|išjungti|pagalba',
 'hr':'ip-postavke|mrežna-adresa|provjera-odziva|putovi|veze|procesi|aktivnost|memorija|pohrana|vrijeme-rada|isključi|pomoć',
 'sl':'ip-nastavitve|omrežni-naslov|preizkus-odziva|poti|povezave|procesi|dejavnost|pomnilnik|shramba|čas-delovanja|izklopi|pomoč',
 'sr_Cyrl':'ип-поставке|мрежна-адреса|провера-одзива|путање|везе|процеси|активност|меморија|складиште|време-рада|искључи|помоћ',
 'sr_Latn':'ip-postavke|mrežna-adresa|provera-odziva|putanje|veze|procesi|aktivnost|memorija|skladište|vreme-rada|isključi|pomoć',
 'bs_Cyrl':'ип-поставке|мрежна-адреса|провјера-одзива|путање|везе|процеси|активност|меморија|похрана|вријеме-рада|искључи|помоћ',
 'mk':'ип-поставки|мрежна-адреса|проверка-одговор|патеки|врски|процеси|активност|меморија|складирање|време-работа|исклучи|помош',
 'sq':'konfigurim-ip|adresë-ip|provë-jehone|rrugët|lidhjet|proceset|veprimtaria|kujtesa|ruajtja|koha-aktive|fik|ndihmë',
 'az_Latn':'ip-ayarları|şəbəkə-ünvanı|əks-səda-sınağı|marşrutlar|bağlantılar|proseslər|fəaliyyət|yaddaş|saxlama|işləmə-müddəti|söndür|kömək',
 'uz_Latn':'ip-sozlamalari|tarmoq-manzili|aks-sado-sinovi|yo‘nalishlar|ulanishlar|jarayonlar|faoliyat|xotira|saqlash|ishlash-vaqti|o‘chirish|yordam',
 'tk_Latn':'ip-sazlamalary|tor-salgysy|ýaň-synagy|ugurlar|baglanyşyklar|prosesler|işjeňlik|ýat|saklaýyş|iş-wagty|öçürmek|kömek',
 'ky_Cyrl':'ip-жөндөөлөр|тармак-дареги|жаңырык-сыноо|багыттар|байланыштар|процесстер|иш-аракет|эс-тутум|сактагыч|иштөө-убактысы|өчүрүү|жардам',
 'tg_Cyrl':'танзими-ip|суроғаи-шабака|санҷиши-акси-садо|масирҳо|пайвастҳо|равандҳо|фаъолият|хотира|захирагоҳ|вақти-кор|хомӯш-кардан|ёрӣ',
 'mn_Cyrl':'ip-тохиргоо|сүлжээний-хаяг|цуурай-шалгалт|маршрут|холболтууд|процессууд|ажиллагаа|санах-ой|хадгалалт|ажилласан-хугацаа|унтраах|тусламж',
 'ka':'ip-გამართვა|ქსელის-მისამართი|ექოს-შემოწმება|მარშრუტები|კავშირები|პროცესები|აქტივობა|მეხსიერება|საცავი|მუშაობის-დრო|გამორთვა|დახმარება',
 'hy':'ip-կարգավորում|ցանցի-հասցե|արձագանքի-ստուգում|երթուղիներ|կապեր|գործընթացներ|գործունեություն|հիշողություն|պահեստ|աշխատանքի-ժամանակ|անջատել|օգնություն',
 'am':'አይፒ-ቅንብር|የመረብ-አድራሻ|የምላሽ-ሙከራ|መንገዶች|ግንኙነቶች|ሂደቶች|እንቅስቃሴ|ማህደረ-ትውስታ|ማከማቻ|የሥራ-ጊዜ|አጥፋ|እገዛ',
 'sw':'usanidi-ip|anwani-ip|jaribio-mwangwi|njia|miunganisho|michakato|shughuli|kumbukumbu|hifadhi|muda-kazi|zima|msaada',
 'so':'habayn-ip|cinwaan-ip|tijaabi-jawaab|waddooyin|xiriirro|hawlo|dhaqdhaqaaq|xusuus|kayd|muddada-shaqo|dami|caawin',
 'ht':'konfigirasyon-ip|adrès-ip|tès-eko|wout|koneksyon|pwosesis|aktivite|memwa|espas-depo|tan-aktif|etenn|èd',
 'pap':'konfigurashon-ip|adres-ip|prueba-eko|rutan|konekshonnan|prosesonan|aktividat|memoria|espasio|tempu-aktivo|paga|yudansa',
 'mg':'fikirakirana-ip|adiresy-ip|fitsapana-valiny|lalana|fifandraisana|dingana|hetsika|fitadidiana|fitahirizana|fotoana-niasana|vonoy|fanampiana',
 'rw':'igenamiterere-ip|aderesi-ip|igerageza-igisubizo|inzira|amasano|ibikorwa|imikorere|ububiko-bwibuka|ububiko|igihe-cyakazi|zimya|ubufasha',
 'rn':'itunganywa-ip|aderesi-ip|igerageza-inyishu|inzira|amasano|ibikorwa|imikorere|ububiko-bwibuka|ububiko|igihe-cakazi|zimya|imfashanyo',
 'st':'litlhophiso-ip|aterese-ip|teko-karabo|litsela|likhokahano|mesebetsi|tšebetso|mohopolo|polokelo|nako-tshebetso|tima|thuso',
 'mt':'issettjar-ip|indirizz-ip|test-eku|rotot|konnessjonijiet|proċessi|attività|memorja|ħażna|ħin-attiv|itfi|għajnuna',
 'bi':'setem-ip|adres-ip|traem-ansa|rod|koneksen|wok|lukluk-wok|memori|ples-blong-fael|taem-blong-wok|satem|help',
 'tpi':'setim-ip|adres-ip|traim-bekim|rot|koneksen|wok|lukim-wok|memori|ples-bilong-fail|taim-bilong-wok|pasim|helpim',
 'sn':'gadziriro-ip|kero-ip|edza-mhinduro|nzira|zvibatanidzo|mabasa|zviitiko|ndangariro|chengetedzo|nguva-yebasa|dzima|rubatsiro',
 'sm':'faatulagaga-ip|tuatusi-ip|suʻe-tali|ala|fesootaʻiga|galuega|tulaga-galuega|manatua|teuina|taimi-galue|tape|fesoasoani',
 'to':'fokotuʻutuʻu-ip|tuʻasila-ip|sivi-tali|hala|fetuʻutaki|ngaahi-ngāue|tuʻunga-ngāue|manatu|tauhi|taimi-ngāue|tamateʻi|tokoni',
 'gn':'ñemboheko-ip|kundaharape-ip|mbohovái-jehecha|tape|joaju|tembiapo|tembiapo-reko|manduʻa|ñongatu|tembiapo-aravo|mbogue|pytyvõ',
}
# These short forms are retained as proposals rather than borrowing a different
# country's complete vocabulary. Remaining entries keep the standard command.
PARTIAL={
 'dv':{'help':'އެހީ','poweroff':'ނިއްވާ','free':'މެމޮރީ'},
 'dz':{'help':'གྲོགས་རམ','poweroff':'གློག་བསད','free':'དྲན་ཚད'},
 'km':{'help':'ជំនួយ','poweroff':'បិទម៉ាស៊ីន','ipconfig':'កំណត់បណ្ដាញ','ip':'អាសយដ្ឋាន','ping':'សាកល្បងចម្លើយ','route':'ផ្លូវ','netstat':'ការតភ្ជាប់','ps':'ដំណើរការ','top':'សកម្មភាព','free':'អង្គចងចាំ','df':'ទំហំផ្ទុក','uptime':'រយៈពេលដំណើរការ'},
 'lo':{'help':'ຊ່ວຍເຫຼືອ','poweroff':'ປິດເຄື່ອງ','ipconfig':'ຕັ້ງຄ່າເຄືອຂ່າຍ','ip':'ທີ່ຢູ່','ping':'ທົດສອບຕອບກັບ','route':'ເສັ້ນທາງ','netstat':'ການເຊື່ອມຕໍ່','ps':'ຂະບວນການ','top':'ກິດຈະກຳ','free':'ຄວາມຈຳ','df':'ພື້ນທີ່ເກັບ','uptime':'ເວລາເຮັດວຽກ'},
 'my':{'help':'အကူအညီ','poweroff':'စက်ပိတ်','ipconfig':'ကွန်ရက်ချိန်ညှိ','ip':'ကွန်ရက်လိပ်စာ','ping':'တုံ့ပြန်မှုစမ်းသပ်','route':'လမ်းကြောင်း','netstat':'ချိတ်ဆက်မှု','ps':'လုပ်ငန်းစဉ်','top':'လုပ်ဆောင်မှု','free':'မှတ်ဉာဏ်','df':'သိုလှောင်နေရာ','uptime':'အလုပ်လုပ်ချိန်'},
 'si':{'help':'උදව්','poweroff':'වසාදමන්න','ipconfig':'ජාලසැකසුම්','ip':'ජාලලිපිනය','ping':'ප්‍රතිචාරපරීක්ෂාව','route':'මාර්ග','netstat':'සම්බන්ධතා','ps':'ක්‍රියාවලි','top':'ක්‍රියාකාරකම්','free':'මතකය','df':'ගබඩාව','uptime':'ක්‍රියාකාලය'},
 'ti':{'help':'ሓገዝ','poweroff':'ኣጥፍእ','ip':'ኣድራሻ','free':'ዝኽሪ','df':'መኽዘን','route':'መንገዲ'},
 'kl':{'help':'ikiorsiissut','poweroff':'qaminneq','free':'eqqaamasaq'},
 'wo':{'help':'ndimbal','poweroff':'fay','route':'yoon','ps':'liggéey','top':'melo-liggéey','uptime':'diiru-liggéey'},
 'pau':{},
 'tvl':{'help':'fesoasoani','poweroff':'tamate'},
}
DESCRIPTIONS={
 'en':['IPv4 settings: address, netmask, gateway','IPv4 interface and route tools','ICMP echo and round-trip time','Connected network and default route','TCP/UDP sockets and traffic','Kernel tasks and user processes','Refresh tasks and memory; q or Ctrl+C quits','Actual kernel pools and user mappings','RAM filesystem capacity and file slots','Time since boot','Stop the OS; RAM files are not preserved','Commands and local names'],
 'ko':['IPv4 주소·가림·관문 조회 및 설정','IPv4 인터페이스와 경로 관리','ICMP 응답과 왕복 시간 확인','직접 연결망과 기본 관문 조회','TCP·UDP 끝점과 송수신 통계','커널 작업과 사용자 실행과정 목록','작업·기억 현황 갱신; q 또는 Ctrl+C로 끝내기','실제 커널 기억 공간과 사용자 매핑 사용량','RAM 파일시스템 용량·파일 칸 사용량','부팅 후 가동 시간','운영체제 종료; RAM 자료는 보존되지 않음','명령어와 현지어 이름 안내'],
 'ja':['IPv4 の番地・マスク・ゲートウェイ設定','IPv4 の接続口と経路','ICMP 応答と往復時間','接続先の網と既定経路','TCP/UDP の接続と通信量','中核の作業と利用者の実行過程','作業と記憶の表示更新; q / Ctrl+C で終了','中核の記憶領域と利用者の割当量','RAM 文書領域の容量と使用枠','起動からの時間','電源を切る; RAM 文書は消えます','命令と日本語の名前'],
 'zh_Hans':['IPv4 地址、子网掩码与网关设置','IPv4 接口与路由工具','ICMP 回声与往返时间','直连网络与默认路由','TCP/UDP 连接与流量','内核任务与用户进程','刷新任务和内存; q 或 Ctrl+C 退出','实际内核内存池与用户映射','RAM 文件系统容量和文件槽','启动后的运行时间','关闭系统; RAM 文件不会保留','命令与中文名称'],
 'zh_Hant':['IPv4 位址、子網路遮罩與閘道設定','IPv4 介面與路由工具','ICMP 回聲與往返時間','直接連線網路與預設路由','TCP/UDP 連線與流量','核心工作與使用者行程','更新工作和記憶體; q 或 Ctrl+C 離開','實際核心記憶體池與使用者映射','RAM 檔案系統容量和檔案槽','啟動後的運作時間','關閉系統; RAM 檔案不會保留','命令與中文名稱'],
}


def profile(language):
    values=ROWS.get(language)
    aliases=dict(zip(KEYS,values.split('|'))) if values else dict(zip(KEYS,KEYS))
    aliases.update(PARTIAL.get(language,{}))
    if values:assert len(values.split('|'))==len(KEYS),language
    aliases={key:unicodedata.normalize('NFC',value) for key,value in aliases.items()}
    for key,value in aliases.items():
        assert value and not any(c.isspace() or c in "'\"$;|&<>\\" for c in value),(language,key,value)
        assert len(value.encode())<=62,(language,key,value)
    assert len(set(aliases.values()))==len(KEYS),language
    pending=[] if language in ('en','und') else [key for key in KEYS if aliases[key]==key]
    return {'aliases':aliases,'descriptions':DESCRIPTIONS.get(language,DESCRIPTIONS['en']),
            'pending':pending,'status':'functional-proposals; native-speaker review pending',
            'description_language':language if language in DESCRIPTIONS else 'en'}


def source(language):
    data=profile(language);aliases=data['aliases'];lines=['public final class 관리명령 {',
        '    static String 완성어() { return '+json.dumps(' '.join(aliases[k] for k in KEYS if aliases[k]!=k),ensure_ascii=False)+'; }',
        '    static String 말(int 번호) {']
    for index,key in enumerate(KEYS[:-1]):lines.append('        if (번호=='+str(index)+') return '+json.dumps(aliases[key],ensure_ascii=False)+';')
    lines+=['        return '+json.dumps(aliases[KEYS[-1]],ensure_ascii=False)+';','    }','    static String 설명(int 번호) {']
    for index,description in enumerate(data['descriptions'][:-1]):lines.append('        if (번호=='+str(index)+') return '+json.dumps(description,ensure_ascii=False)+';')
    lines+=['        return '+json.dumps(data['descriptions'][-1],ensure_ascii=False)+';','    }','}']
    return '\n'.join(lines)+'\n'
