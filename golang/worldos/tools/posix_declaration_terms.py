"""Whole-concept names for the native user-space interface.

Project proposals, not official terminology or native-speaker certification.
Abbreviations are expanded by their present role; no word-by-word fallback,
country prefixes, or automatic transliteration for missing languages.
"""

GROUPS = {}


def group(category, keys, **rows):
    keys = keys.split()
    for language, row in rows.items():
        if len(row.split('|')) != len(keys):
            raise ValueError((category, language, len(keys), len(row.split('|'))))
    GROUPS[category] = (keys, rows)


group('network-declaration',
    'in_addr_t in_port_t in_addr sockaddr_in s_addr sin_family sin_port sin_addr sin_zero '
    'sa_family_t sockaddr sa_family sa_data socklen_t AF_UNSPEC AF_INET PF_INET SOCK_STREAM '
    'SOCK_DGRAM SHUT_RD SHUT_WR SHUT_RDWR IPPROTO_IP IPPROTO_UDP INADDR_ANY INADDR_LOOPBACK '
    'hostlong hostshort netlong netshort',
    en='internetwork_address_value_type|transport_port_number_type|internetwork_address|internetwork_endpoint_address|address_value|internetwork_address_family|transport_port_number|internetwork_address_field|address_padding|address_family_type|endpoint_address|endpoint_address_family|address_payload|address_length_type|unspecified_address_family|internetwork_address_family_code|internetwork_protocol_family|stream_endpoint|datagram_endpoint|stop_receiving|stop_sending|stop_both_directions|default_internetwork_protocol|user_datagram_protocol|any_local_address|loopback_address|host_order_32_bit_value|host_order_16_bit_value|network_order_32_bit_value|network_order_16_bit_value',
    ko='상호연결망주소값형|통신창구번호형|상호연결망주소|상호연결망끝점주소|주소값|연결망주소계열|통신창구번호|연결망주소내용|주소맞춤채움|주소계열형|통신끝점주소|끝점주소계열|주소자료|주소길이형|주소계열미지정|상호연결망주소계열|상호연결망규약계열|자료흐름끝점|자료전문끝점|수신중단|송신중단|양방향중단|상호연결망기본규약|사용자자료전문규약|모든지역주소|자기되돌림주소|기계순서32이진자리값|기계순서16이진자리값|통신망순서32이진자리값|통신망순서16이진자리값',
    ja='相互接続網番地値型|通信窓口番号型|相互接続網番地|相互接続網端点番地|番地値|接続網番地系統|通信窓口番号|接続網番地内容|番地の埋合せ|番地系統型|通信端点番地|端点番地系統|番地資料|番地長型|番地系統未指定|相互接続網番地系統|相互接続網規約系統|資料流端点|資料電文端点|受信停止|送信停止|双方向停止|相互接続網基本規約|利用者資料電文規約|全ての局所番地|自己折返し番地|機械順32二進桁値|機械順16二進桁値|通信網順32二進桁値|通信網順16二進桁値',
    ja_Hira='そうごせつぞくもうばんちちがた|つうしんまどぐちばんごうがた|そうごせつぞくもうばんち|そうごせつぞくもうたんてんばんち|ばんちち|せつぞくもうばんちけいとう|つうしんまどぐちばんごう|せつぞくもうばんちないよう|ばんちのうめあわせ|ばんちけいとうがた|つうしんたんてんばんち|たんてんばんちけいとう|ばんちしりょう|ばんちちょうがた|ばんちけいとうみしてい|そうごせつぞくもうばんちけいとう|そうごせつぞくもうきやくけいとう|しりょうりゅうたんてん|しりょうでんぶんたんてん|じゅしんていし|そうしんていし|そうほうこうていし|そうごせつぞくもうきほんきやく|りようしゃしりょうでんぶんきやく|すべてのきょくしょばんち|じこおりかえしばんち|きかいじゅん32にしんけたち|きかいじゅん16にしんけたち|つうしんもうじゅん32にしんけたち|つうしんもうじゅん16にしんけたち',
    zh_Hans='互联网络地址值类型|通信端口编号类型|互联网络地址|互联网络端点地址|地址值|互联地址族|通信端口编号|互联地址内容|地址填充区|地址族类型|通信端点地址|端点地址族|地址数据|地址长度类型|未指定地址族|互联网络地址族|互联网络协议族|数据流端点|数据报端点|停止接收|停止发送|停止双向通信|互联网络基本协议|用户数据报协议|任意本地地址|本机回环地址|主机顺序32位值|主机顺序16位值|网络顺序32位值|网络顺序16位值',
    zh_Hant='互聯網路位址值型別|通訊埠編號型別|互聯網路位址|互聯網路端點位址|位址值|互聯位址族|通訊埠編號|互聯位址內容|位址填補區|位址族型別|通訊端點位址|端點位址族|位址資料|位址長度型別|未指定位址族|互聯網路位址族|互聯網路協定族|資料流端點|資料報端點|停止接收|停止傳送|停止雙向通訊|互聯網路基本協定|使用者資料報協定|任意本機位址|本機迴送位址|主機順序32位值|主機順序16位值|網路順序32位值|網路順序16位值',
    de='Typ des Netzverbundadresswerts|Typ der Kommunikationsportnummer|Netzverbundadresse|Netzverbundendpunktadresse|Adresswert|Netzverbundadressfamilie|Kommunikationsportnummer|Netzverbundadressinhalt|Adressauffüllung|Adressfamilientyp|Kommunikationsendpunktadresse|Endpunktadressfamilie|Adressdaten|Adresslängentyp|nicht festgelegte Adressfamilie|Netzverbundadressfamilienkennung|Netzverbundprotokollfamilie|Datenstromendpunkt|Datagrammendpunkt|Empfang beenden|Senden beenden|beide Richtungen beenden|Netzverbundgrundprotokoll|Benutzerdatagrammprotokoll|beliebige lokale Adresse|Rückschleifenadresse|32 Bit Wert in Rechnerreihenfolge|16 Bit Wert in Rechnerreihenfolge|32 Bit Wert in Netzreihenfolge|16 Bit Wert in Netzreihenfolge',
    fr='type de valeur adresse interréseau|type de numéro de port de communication|adresse interréseau|adresse du point de communication interréseau|valeur adresse|famille adresse interréseau|numéro de port de communication|contenu adresse interréseau|remplissage adresse|type de famille adresse|adresse du point de communication|famille adresse du point|données adresse|type de longueur adresse|famille adresse non spécifiée|code de famille adresse interréseau|famille de protocoles interréseau|point de flux de données|point de datagrammes|arrêter réception|arrêter émission|arrêter les deux sens|protocole interréseau de base|protocole de datagrammes utilisateur|toute adresse locale|adresse de bouclage|valeur de 32 bits en ordre machine|valeur de 16 bits en ordre machine|valeur de 32 bits en ordre réseau|valeur de 16 bits en ordre réseau',
    es='tipo de valor de dirección entre redes|tipo de número de puerto de comunicación|dirección entre redes|dirección de extremo entre redes|valor de dirección|familia de direcciones entre redes|número de puerto de comunicación|contenido de dirección entre redes|relleno de dirección|tipo de familia de direcciones|dirección de extremo de comunicación|familia de direcciones del extremo|datos de dirección|tipo de longitud de dirección|familia de direcciones sin especificar|código de familia de direcciones entre redes|familia de protocolos entre redes|extremo de flujo de datos|extremo de datagramas|detener recepción|detener envío|detener ambos sentidos|protocolo básico entre redes|protocolo de datagramas de usuario|cualquier dirección local|dirección de retorno local|valor de 32 bits en orden de máquina|valor de 16 bits en orden de máquina|valor de 32 bits en orden de red|valor de 16 bits en orden de red',
    pt='tipo do valor de endereço entre redes|tipo do número de porta de comunicação|endereço entre redes|endereço do extremo entre redes|valor do endereço|família de endereços entre redes|número de porta de comunicação|conteúdo do endereço entre redes|preenchimento do endereço|tipo da família de endereços|endereço do extremo de comunicação|família de endereços do extremo|dados do endereço|tipo do comprimento do endereço|família de endereços não especificada|código da família de endereços entre redes|família de protocolos entre redes|extremo de fluxo de dados|extremo de datagramas|parar receção|parar envio|parar ambos os sentidos|protocolo básico entre redes|protocolo de datagramas do utilizador|qualquer endereço local|endereço de retorno local|valor de 32 bits na ordem da máquina|valor de 16 bits na ordem da máquina|valor de 32 bits na ordem da rede|valor de 16 bits na ordem da rede',
    ru='тип значения межсетевого адреса|тип номера порта связи|межсетевой адрес|адрес межсетевой конечной точки|значение адреса|семейство межсетевых адресов|номер порта связи|содержимое межсетевого адреса|заполнение адреса|тип семейства адресов|адрес конечной точки связи|семейство адресов конечной точки|данные адреса|тип длины адреса|семейство адресов не задано|код семейства межсетевых адресов|семейство межсетевых протоколов|конечная точка потока данных|конечная точка датаграмм|остановить приём|остановить передачу|остановить оба направления|основной межсетевой протокол|протокол пользовательских датаграмм|любой местный адрес|адрес обратной петли|32 разрядное значение в машинном порядке|16 разрядное значение в машинном порядке|32 разрядное значение в сетевом порядке|16 разрядное значение в сетевом порядке',
    ar='نوع قيمة عنوان الشبكات المترابطة|نوع رقم منفذ الاتصال|عنوان الشبكات المترابطة|عنوان نقطة اتصال الشبكات المترابطة|قيمة العنوان|عائلة عناوين الشبكات المترابطة|رقم منفذ الاتصال|محتوى عنوان الشبكات المترابطة|حشو العنوان|نوع عائلة العناوين|عنوان نقطة الاتصال|عائلة عناوين نقطة الاتصال|بيانات العنوان|نوع طول العنوان|عائلة عناوين غير محددة|رمز عائلة عناوين الشبكات المترابطة|عائلة بروتوكولات الشبكات المترابطة|نقطة تدفق البيانات|نقطة رزم البيانات|إيقاف الاستقبال|إيقاف الإرسال|إيقاف الاتجاهين|بروتوكول الشبكات المترابطة الأساسي|بروتوكول رزم المستخدم|أي عنوان محلي|عنوان الحلقة المحلية|قيمة من 32 بت بترتيب الآلة|قيمة من 16 بت بترتيب الآلة|قيمة من 32 بت بترتيب الشبكة|قيمة من 16 بت بترتيب الشبكة',
    hi='अंतरजाल पता मान प्रकार|संचार द्वार संख्या प्रकार|अंतरजाल पता|अंतरजाल छोर पता|पता मान|अंतरजाल पता परिवार|संचार द्वार संख्या|अंतरजाल पता सामग्री|पता पूरण|पता परिवार प्रकार|संचार छोर पता|छोर पता परिवार|पता आँकड़े|पता लंबाई प्रकार|अनिर्दिष्ट पता परिवार|अंतरजाल पता परिवार संकेत|अंतरजाल नियम परिवार|आँकड़ा प्रवाह छोर|आँकड़ा संदेश छोर|प्राप्ति रोकें|प्रेषण रोकें|दोनों दिशाएँ रोकें|मूल अंतरजाल नियम|उपयोगकर्ता आँकड़ा संदेश नियम|कोई भी स्थानीय पता|स्वयं वापसी पता|यंत्र क्रम में 32 द्विआधारी अंकों का मान|यंत्र क्रम में 16 द्विआधारी अंकों का मान|जाल क्रम में 32 द्विआधारी अंकों का मान|जाल क्रम में 16 द्विआधारी अंकों का मान',
    ta='பிணையங்களிடை முகவரி மதிப்பு வகை|தொடர்பு வாயில் எண் வகை|பிணையங்களிடை முகவரி|பிணையங்களிடை முனை முகவரி|முகவரி மதிப்பு|பிணையங்களிடை முகவரிக் குடும்பம்|தொடர்பு வாயில் எண்|பிணையங்களிடை முகவரி உள்ளடக்கம்|முகவரி நிரப்பு|முகவரிக் குடும்ப வகை|தொடர்பு முனை முகவரி|முனை முகவரிக் குடும்பம்|முகவரித் தரவு|முகவரி நீள வகை|குறிப்பிடாத முகவரிக் குடும்பம்|பிணையங்களிடை முகவரிக் குடும்பக் குறியீடு|பிணையங்களிடை நெறிமுறைக் குடும்பம்|தரவு ஓட்ட முனை|தரவுச் செய்தி முனை|பெறுதலை நிறுத்து|அனுப்புதலை நிறுத்து|இரு திசைகளையும் நிறுத்து|அடிப்படைப் பிணையங்களிடை நெறிமுறை|பயனர் தரவுச் செய்தி நெறிமுறை|எந்த உள்ளூர் முகவரியும்|தன்னிடமே திரும்பும் முகவரி|பொறி வரிசையில் 32 இரும இலக்க மதிப்பு|பொறி வரிசையில் 16 இரும இலக்க மதிப்பு|பிணைய வரிசையில் 32 இரும இலக்க மதிப்பு|பிணைய வரிசையில் 16 இரும இலக்க மதிப்பு')

group('scalar-type',
    'size_t ssize_t ptrdiff_t off_t pid_t uid_t gid_t mode_t dev_t ino_t nlink_t time_t blksize_t blkcnt_t '
    'int8_t uint8_t int16_t uint16_t int32_t uint32_t int64_t uint64_t intptr_t uintptr_t',
    en='object_size_type|signed_size_type|pointer_difference_type|file_offset_type|process_identifier_type|user_identifier_type|group_identifier_type|file_mode_type|device_identifier_type|file_serial_number_type|hard_link_count_type|time_value_type|block_size_type|block_count_type|signed_8_bit_integer|unsigned_8_bit_integer|signed_16_bit_integer|unsigned_16_bit_integer|signed_32_bit_integer|unsigned_32_bit_integer|signed_64_bit_integer|unsigned_64_bit_integer|pointer_sized_signed_integer|pointer_sized_unsigned_integer',
    ko='크기형|부호있는크기형|주소차이형|자료위치형|실행과정번호형|사용자번호형|무리번호형|자료철방식형|장치번호형|자료철고유번호형|직접연결수형|시각값형|구획크기형|구획수형|부호있는8이진자리정수|부호없는8이진자리정수|부호있는16이진자리정수|부호없는16이진자리정수|부호있는32이진자리정수|부호없는32이진자리정수|부호있는64이진자리정수|부호없는64이진자리정수|주소크기부호있는정수|주소크기부호없는정수',
    ja='大きさ型|符号付き大きさ型|番地差型|文書位置型|実行過程番号型|利用者番号型|所属組番号型|文書方式型|装置番号型|文書固有番号型|直接連結数型|時刻値型|区画長型|区画数型|符号付き8二進桁整数|符号なし8二進桁整数|符号付き16二進桁整数|符号なし16二進桁整数|符号付き32二進桁整数|符号なし32二進桁整数|符号付き64二進桁整数|符号なし64二進桁整数|番地幅符号付き整数|番地幅符号なし整数',
    ja_Hira='おおきさがた|ふごうつきおおきさがた|ばんちさがた|ぶんしょいちがた|じっこうかていばんごうがた|りようしゃばんごうがた|しょぞくくみばんごうがた|ぶんしょほうしきがた|そうちばんごうがた|ぶんしょこゆうばんごうがた|ちょくせつれんけつすうがた|じこくちがた|くかくちょうがた|くかくすうがた|ふごうつき8にしんけたせいすう|ふごうなし8にしんけたせいすう|ふごうつき16にしんけたせいすう|ふごうなし16にしんけたせいすう|ふごうつき32にしんけたせいすう|ふごうなし32にしんけたせいすう|ふごうつき64にしんけたせいすう|ふごうなし64にしんけたせいすう|ばんちはばふごうつきせいすう|ばんちはばふごうなしせいすう',
    zh_Hans='大小类型|有符号大小类型|指针差类型|文件位置类型|进程编号类型|用户编号类型|组编号类型|文件模式类型|设备编号类型|文件唯一编号类型|硬链接数量类型|时间值类型|块大小类型|块数量类型|有符号8位整数|无符号8位整数|有符号16位整数|无符号16位整数|有符号32位整数|无符号32位整数|有符号64位整数|无符号64位整数|地址宽度有符号整数|地址宽度无符号整数',
    zh_Hant='大小型別|有號大小型別|指標差型別|檔案位置型別|行程編號型別|使用者編號型別|群組編號型別|檔案模式型別|裝置編號型別|檔案唯一編號型別|硬連結數量型別|時間值型別|區塊大小型別|區塊數量型別|有號8位整數|無號8位整數|有號16位整數|無號16位整數|有號32位整數|無號32位整數|有號64位整數|無號64位整數|位址寬度有號整數|位址寬度無號整數')

group('structure-field',
    'st_dev st_ino st_mode st_nlink st_uid st_gid st_rdev st_size st_blksize st_blocks '
    'st_atime st_atimensec st_mtime st_mtimensec st_ctime st_ctimensec '
    'utsname sysname nodename release version machine',
    en='containing_device|file_serial_number|file_kind_and_permissions|hard_link_count|owner_user_identifier|owner_group_identifier|represented_device|file_size|preferred_io_block_size|allocated_block_count|last_access_time|last_access_nanoseconds|last_content_change_time|last_content_change_nanoseconds|last_status_change_time|last_status_change_nanoseconds|system_identity|system_name|node_name|system_release|system_version|machine_kind',
    ko='소속장치번호|자료철고유번호|자료철종류와권한|직접연결수|소유사용자번호|소유무리번호|가리키는장치번호|자료철크기|권장입출력구획크기|할당구획수|마지막접근시각|마지막접근십억분초|마지막내용변경시각|마지막내용변경십억분초|마지막상태변경시각|마지막상태변경십억분초|체제정보|체제이름|기계이름|체제배포판|체제개정판|기계종류',
    ja='所属装置番号|文書固有番号|文書種類と権限|直接連結数|所有利用者番号|所有組番号|表す装置番号|文書の大きさ|推奨入出力区画長|割当区画数|最終参照時刻|最終参照十億分秒|最終内容変更時刻|最終内容変更十億分秒|最終状態変更時刻|最終状態変更十億分秒|体系情報|体系名|機械名|体系配布版|体系改訂版|機械種類',
    ja_Hira='しょぞくそうちばんごう|ぶんしょこゆうばんごう|ぶんしょしゅるいとけんげん|ちょくせつれんけつすう|しょゆうりようしゃばんごう|しょゆうくみばんごう|あらわすそうちばんごう|ぶんしょのおおきさ|すいしょうにゅうしゅつりょくくかくちょう|わりあてくかくすう|さいしゅうさんしょうじこく|さいしゅうさんしょうじゅうおくぶんびょう|さいしゅうないようへんこうじこく|さいしゅうないようへんこうじゅうおくぶんびょう|さいしゅうじょうたいへんこうじこく|さいしゅうじょうたいへんこうじゅうおくぶんびょう|たいけいじょうほう|たいけいめい|きかいめい|たいけいはいふばん|たいけいかいていばん|きかいしゅるい',
    zh_Hans='所属设备编号|文件唯一编号|文件类型与权限|硬链接数量|所有者用户编号|所有者组编号|代表设备编号|文件大小|建议读写块大小|已分配块数量|最后访问时间|最后访问纳秒|最后内容修改时间|最后内容修改纳秒|最后状态变更时间|最后状态变更纳秒|系统身份信息|系统名称|节点名称|系统发行版|系统修订版|机器类型',
    zh_Hant='所屬裝置編號|檔案唯一編號|檔案類型與權限|硬連結數量|擁有者使用者編號|擁有者群組編號|代表裝置編號|檔案大小|建議讀寫區塊大小|已配置區塊數量|最後存取時間|最後存取奈秒|最後內容修改時間|最後內容修改奈秒|最後狀態變更時間|最後狀態變更奈秒|系統身分資訊|系統名稱|節點名稱|系統發行版|系統修訂版|機器類型')

group('interface-constant',
    'NULL EXIT_SUCCESS EXIT_FAILURE STDIN_FILENO STDOUT_FILENO STDERR_FILENO '
    'F_OK R_OK W_OK X_OK SEEK_SET SEEK_CUR SEEK_END '
    'O_RDONLY O_WRONLY O_RDWR O_ACCMODE O_CREAT O_EXCL O_TRUNC O_APPEND O_DIRECTORY '
    'F_DUPFD F_GETFD F_SETFD F_GETFL F_SETFL FD_CLOEXEC WNOHANG WIFEXITED WEXITSTATUS '
    'S_IFMT S_IFDIR S_IFCHR S_IFREG S_IRUSR S_IWUSR S_IXUSR S_IRGRP S_IWGRP S_IXGRP S_IROTH S_IWOTH S_IXOTH S_ISDIR S_ISCHR S_ISREG',
    en='null_pointer|successful_exit|failed_exit|standard_input_descriptor|standard_output_descriptor|standard_error_descriptor|test_existence|test_read_permission|test_write_permission|test_execute_permission|offset_from_start|offset_from_current|offset_from_end|open_read_only|open_write_only|open_read_write|access_mode_mask|create_if_missing|require_new_file|truncate_existing_file|append_at_end|require_directory|duplicate_descriptor|read_descriptor_flags|set_descriptor_flags|read_file_status_flags|set_file_status_flags|close_on_program_replacement|do_not_wait_if_unready|exited_normally|extract_exit_status|file_kind_mask|directory_kind|character_device_kind|regular_file_kind|owner_read_permission|owner_write_permission|owner_execute_permission|group_read_permission|group_write_permission|group_execute_permission|others_read_permission|others_write_permission|others_execute_permission|is_directory_mode|is_character_device_mode|is_regular_file_mode',
    ko='빈주소|성공종료|실패종료|표준입력번호|표준출력번호|표준오류출력번호|존재확인|읽기권한확인|쓰기권한확인|실행권한확인|처음기준위치|현재기준위치|끝기준위치|읽기전용열기|쓰기전용열기|읽고쓰기열기|접근방식가림값|없으면만들기|새자료철만허용|기존내용비우기|끝에덧붙이기|목록만허용|서술번호복제|서술번호표시얻기|서술번호표시설정|자료철상태표시얻기|자료철상태표시설정|실행내용교체때닫기|준비안되면기다리지않기|정상종료인지확인|종료값꺼내기|자료철종류가림값|목록종류|문자장치종류|일반자료철종류|소유자읽기권한|소유자쓰기권한|소유자실행권한|소유무리읽기권한|소유무리쓰기권한|소유무리실행권한|나머지읽기권한|나머지쓰기권한|나머지실행권한|목록방식인지확인|문자장치방식인지확인|일반자료철방식인지확인',
    ja='空番地|成功終了|失敗終了|標準入力番号|標準出力番号|標準誤り出力番号|存在確認|読取権限確認|書込権限確認|実行権限確認|先頭基準位置|現在基準位置|末尾基準位置|読取専用で開く|書込専用で開く|読書両用で開く|利用方式抽出値|無ければ作る|新規文書のみ許す|既存内容を空にする|末尾へ追加する|目録のみ許す|記述番号複製|記述番号標識取得|記述番号標識設定|文書状態標識取得|文書状態標識設定|実行内容置換時に閉じる|未準備なら待たない|正常終了判定|終了値取出し|文書種類抽出値|目録種類|文字装置種類|通常文書種類|所有者読取権限|所有者書込権限|所有者実行権限|所属組読取権限|所属組書込権限|所属組実行権限|他者読取権限|他者書込権限|他者実行権限|目録方式判定|文字装置方式判定|通常文書方式判定',
    ja_Hira='からばんち|せいこうしゅうりょう|しっぱいしゅうりょう|ひょうじゅんにゅうりょくばんごう|ひょうじゅんしゅつりょくばんごう|ひょうじゅんあやまりしゅつりょくばんごう|そんざいかくにん|よみとりけんげんかくにん|かきこみけんげんかくにん|じっこうけんげんかくにん|せんとうきじゅんいち|げんざいきじゅんいち|まつびきじゅんいち|よみとりせんようでひらく|かきこみせんようでひらく|よみかきりょうようでひらく|りようほうしきちゅうしゅつち|なければつくる|しんきぶんしょのみゆるす|きぞんないようをからにする|まつびへついかする|もくろくのみゆるす|きじゅつばんごうふくせい|きじゅつばんごうひょうしきしゅとく|きじゅつばんごうひょうしきせってい|ぶんしょじょうたいひょうしきしゅとく|ぶんしょじょうたいひょうしきせってい|じっこうないようちかんじにとじる|みじゅんびならまたない|せいじょうしゅうりょうはんてい|しゅうりょうちとりだし|ぶんしょしゅるいちゅうしゅつち|もくろくしゅるい|もじそうちしゅるい|つうじょうぶんしょしゅるい|しょゆうしゃよみとりけんげん|しょゆうしゃかきこみけんげん|しょゆうしゃじっこうけんげん|しょぞくくみよみとりけんげん|しょぞくくみかきこみけんげん|しょぞくくみじっこうけんげん|たしゃよみとりけんげん|たしゃかきこみけんげん|たしゃじっこうけんげん|もくろくほうしきはんてい|もじそうちほうしきはんてい|つうじょうぶんしょほうしきはんてい',
    zh_Hans='空地址|成功退出|失败退出|标准输入编号|标准输出编号|标准错误输出编号|检查存在|检查读权限|检查写权限|检查执行权限|从起点定位|从当前位置定位|从末尾定位|只读打开|只写打开|读写打开|访问模式掩码|不存在则创建|仅允许新文件|清空原有内容|在末尾追加|仅允许目录|复制描述编号|取得描述编号标志|设置描述编号标志|取得文件状态标志|设置文件状态标志|替换程序时关闭|未就绪则不等待|检查正常退出|提取退出值|文件类型掩码|目录类型|字符设备类型|普通文件类型|所有者读权限|所有者写权限|所有者执行权限|所属组读权限|所属组写权限|所属组执行权限|其他人读权限|其他人写权限|其他人执行权限|检查目录模式|检查字符设备模式|检查普通文件模式',
    zh_Hant='空位址|成功結束|失敗結束|標準輸入編號|標準輸出編號|標準錯誤輸出編號|檢查存在|檢查讀取權限|檢查寫入權限|檢查執行權限|從起點定位|從目前位置定位|從末尾定位|唯讀開啟|唯寫開啟|讀寫開啟|存取模式遮罩|不存在則建立|僅允許新檔案|清空原有內容|在末尾附加|僅允許目錄|複製描述編號|取得描述編號旗標|設定描述編號旗標|取得檔案狀態旗標|設定檔案狀態旗標|替換程式時關閉|未就緒則不等待|檢查正常結束|提取結束值|檔案類型遮罩|目錄類型|字元裝置類型|一般檔案類型|擁有者讀取權限|擁有者寫入權限|擁有者執行權限|所屬群組讀取權限|所屬群組寫入權限|所屬群組執行權限|其他人讀取權限|其他人寫入權限|其他人執行權限|檢查目錄模式|檢查字元裝置模式|檢查一般檔案模式')

group('error-code',
    'EPERM ENOENT ESRCH EINTR EIO E2BIG ENOEXEC EBADF ECHILD EAGAIN ENOMEM EACCES EFAULT '
    'EBUSY EEXIST ENODEV ENOTDIR EISDIR EINVAL ENFILE EMFILE ENOTTY EFBIG ENOSPC ESPIPE '
    'EROFS ERANGE ENOSYS EMSGSIZE EPROTONOSUPPORT EOPNOTSUPP EAFNOSUPPORT EADDRINUSE ENETUNREACH ENOTCONN',
    en='operation_not_permitted|file_or_directory_missing|process_missing|operation_interrupted|input_output_error|argument_list_too_large|invalid_executable_format|invalid_file_descriptor|no_child_process|temporarily_unavailable|insufficient_memory|permission_denied|invalid_memory_address|resource_busy|file_already_exists|device_missing|not_a_directory|is_a_directory|invalid_argument|system_file_limit|process_file_limit|inappropriate_device_operation|file_too_large|no_storage_space|cannot_seek_stream|read_only_filesystem|value_out_of_range|function_not_implemented|message_too_large|protocol_not_supported|operation_not_supported|address_family_not_supported|address_already_in_use|network_unreachable|endpoint_not_connected',
    ko='오류허용되지않은동작|오류자료철이나목록없음|오류실행과정없음|오류동작중단됨|오류입출력실패|오류전달목록너무큼|오류실행형식잘못됨|오류서술번호잘못됨|오류자식실행과정없음|오류잠시사용불가|오류기억공간부족|오류접근권한없음|오류기억주소잘못됨|오류자원사용중|오류자료철이미있음|오류장치없음|오류목록아님|오류목록임|오류전달값잘못됨|오류체제열린자료철한도|오류과정열린자료철한도|오류장치에맞지않는동작|오류자료철너무큼|오류저장공간부족|오류흐름위치이동불가|오류읽기전용자료체계|오류값범위벗어남|오류기능미구현|오류전문너무큼|오류규약지원안함|오류동작지원안함|오류주소계열지원안함|오류주소이미사용중|오류통신망도달불가|오류끝점연결안됨',
    ja='誤り操作不許可|誤り文書又は目録なし|誤り実行過程なし|誤り操作中断|誤り入出力失敗|誤り引数一覧過大|誤り実行形式不正|誤り記述番号不正|誤り子実行過程なし|誤り一時利用不可|誤り記憶不足|誤り利用権限なし|誤り記憶番地不正|誤り資源使用中|誤り文書既存|誤り装置なし|誤り目録でない|誤り目録である|誤り引数不正|誤り体系文書数上限|誤り過程文書数上限|誤り装置不適合操作|誤り文書過大|誤り保存領域不足|誤り流れ位置移動不可|誤り読取専用文書体系|誤り値範囲外|誤り機能未実装|誤り電文過大|誤り規約非対応|誤り操作非対応|誤り番地系統非対応|誤り番地使用中|誤り通信網到達不可|誤り端点未接続',
    ja_Hira='あやまりそうさふきょか|あやまりぶんしょまたはもくろくなし|あやまりじっこうかていなし|あやまりそうさちゅうだん|あやまりにゅうしゅつりょくしっぱい|あやまりひきすういちらんかだい|あやまりじっこうけいしきふせい|あやまりきじゅつばんごうふせい|あやまりこじっこうかていなし|あやまりいちじりようふか|あやまりきおくぶそく|あやまりりようけんげんなし|あやまりきおくばんちふせい|あやまりしげんしようちゅう|あやまりぶんしょきそん|あやまりそうちなし|あやまりもくろくでない|あやまりもくろくである|あやまりひきすうふせい|あやまりたいけいぶんしょすうじょうげん|あやまりかていぶんしょすうじょうげん|あやまりそうちふてきごうそうさ|あやまりぶんしょかだい|あやまりほぞんりょういきぶそく|あやまりながれいちいどうふか|あやまりよみとりせんようぶんしょたいけい|あやまりちはんいがい|あやまりきのうみじっそう|あやまりでんぶんかだい|あやまりきやくひたいおう|あやまりそうさひたいおう|あやまりばんちけいとうひたいおう|あやまりばんちしようちゅう|あやまりつうしんもうとうたつふか|あやまりたんてんみせつぞく',
    zh_Hans='错误操作不允许|错误文件或目录不存在|错误进程不存在|错误操作被中断|错误输入输出失败|错误参数列表过大|错误执行格式无效|错误描述编号无效|错误没有子进程|错误暂时不可用|错误内存不足|错误没有访问权限|错误内存地址无效|错误资源使用中|错误文件已存在|错误设备不存在|错误不是目录|错误是目录|错误参数无效|错误系统文件数量上限|错误进程文件数量上限|错误设备不适用操作|错误文件过大|错误存储空间不足|错误数据流不可定位|错误只读文件系统|错误数值超出范围|错误功能未实现|错误报文过大|错误不支持协议|错误不支持操作|错误不支持地址族|错误地址已占用|错误网络不可达|错误端点未连接',
    zh_Hant='錯誤操作不允許|錯誤檔案或目錄不存在|錯誤行程不存在|錯誤操作被中斷|錯誤輸入輸出失敗|錯誤引數列表過大|錯誤執行格式無效|錯誤描述編號無效|錯誤沒有子行程|錯誤暫時無法使用|錯誤記憶體不足|錯誤沒有存取權限|錯誤記憶體位址無效|錯誤資源使用中|錯誤檔案已存在|錯誤裝置不存在|錯誤不是目錄|錯誤是目錄|錯誤引數無效|錯誤系統檔案數量上限|錯誤行程檔案數量上限|錯誤裝置不適用操作|錯誤檔案過大|錯誤儲存空間不足|錯誤資料流無法定位|錯誤唯讀檔案系統|錯誤數值超出範圍|錯誤功能未實作|錯誤訊息過大|錯誤不支援協定|錯誤不支援操作|錯誤不支援位址族|錯誤位址已占用|錯誤網路無法到達|錯誤端點未連接')

group('integer-limit',
    'CHAR_BIT SCHAR_MIN SCHAR_MAX UCHAR_MAX CHAR_MIN CHAR_MAX SHRT_MIN SHRT_MAX USHRT_MAX '
    'INT_MIN INT_MAX UINT_MAX LONG_MIN LONG_MAX ULONG_MAX LLONG_MIN LLONG_MAX ULLONG_MAX',
    en='bits_per_byte|signed_char_minimum|signed_char_maximum|unsigned_char_maximum|char_minimum|char_maximum|short_integer_minimum|short_integer_maximum|unsigned_short_maximum|integer_minimum|integer_maximum|unsigned_integer_maximum|long_integer_minimum|long_integer_maximum|unsigned_long_maximum|long_long_integer_minimum|long_long_integer_maximum|unsigned_long_long_maximum',
    ko='여덟자리묶음의이진자리수|부호있는문자정수최솟값|부호있는문자정수최댓값|부호없는문자정수최댓값|문자정수최솟값|문자정수최댓값|짧은정수최솟값|짧은정수최댓값|부호없는짧은정수최댓값|정수최솟값|정수최댓값|부호없는정수최댓값|긴정수최솟값|긴정수최댓값|부호없는긴정수최댓값|아주긴정수최솟값|아주긴정수최댓값|부호없는아주긴정수최댓값',
    ja='八桁組の二進桁数|符号付き文字整数最小値|符号付き文字整数最大値|符号なし文字整数最大値|文字整数最小値|文字整数最大値|短整数最小値|短整数最大値|符号なし短整数最大値|整数最小値|整数最大値|符号なし整数最大値|長整数最小値|長整数最大値|符号なし長整数最大値|長長整数最小値|長長整数最大値|符号なし長長整数最大値',
    ja_Hira='はちけたぐみのにしんけたすう|ふごうつきもじせいすうさいしょうち|ふごうつきもじせいすうさいだいち|ふごうなしもじせいすうさいだいち|もじせいすうさいしょうち|もじせいすうさいだいち|たんせいすうさいしょうち|たんせいすうさいだいち|ふごうなしたんせいすうさいだいち|せいすうさいしょうち|せいすうさいだいち|ふごうなしせいすうさいだいち|ちょうせいすうさいしょうち|ちょうせいすうさいだいち|ふごうなしちょうせいすうさいだいち|ちょうちょうせいすうさいしょうち|ちょうちょうせいすうさいだいち|ふごうなしちょうちょうせいすうさいだいち',
    zh_Hans='每字节位数|有符号字符整数最小值|有符号字符整数最大值|无符号字符整数最大值|字符整数最小值|字符整数最大值|短整数最小值|短整数最大值|无符号短整数最大值|整数最小值|整数最大值|无符号整数最大值|长整数最小值|长整数最大值|无符号长整数最大值|长长整数最小值|长长整数最大值|无符号长长整数最大值',
    zh_Hant='每位元組位元數|有號字元整數最小值|有號字元整數最大值|無號字元整數最大值|字元整數最小值|字元整數最大值|短整數最小值|短整數最大值|無號短整數最大值|整數最小值|整數最大值|無號整數最大值|長整數最小值|長整數最大值|無號長整數最大值|長長整數最小值|長長整數最大值|無號長長整數最大值')

group('implementation-helper',
    'SC0 SC1 SC2 SC3 SYS_socketcall argc args_fail args_pass bss_zeroed byte bytes checks client '
    'cloexec_fail cloexec_pass copy cwd decoded expected_errno failed_with failure failures first '
    'i iteration length_of loaded memory old parent pass passed posix_compile_test posix_test_heap '
    'posix_test_process private_value reap_nohang report root s say second server server_address '
    'source_length spin spins start target test_dup_and_fcntl test_identity test_open_and_io '
    'test_paths test_terminal_and_uname text_equal text_length waited',
    en='syscall_without_arguments|syscall_with_one_argument|syscall_with_two_arguments|syscall_with_three_arguments|socket_call_number|argument_count|argument_test_failure|argument_test_success|uninitialized_data_was_zeroed|byte_value|byte_array|check_count|client_endpoint|close_on_exec_failure|close_on_exec_success|copied_value|working_directory|decoded_value|expected_error_number|failed_with_error|failure_flag|failure_count|first_item|item_index|iteration_number|length_of_text|loaded_value|memory_region|previous_value|parent_process|test_pass|passed_test|interface_compile_test|heap_behavior_test|process_behavior_test|process_private_value|reap_without_waiting|report_result|root_path|examined_data|write_message|second_item|server_endpoint|server_endpoint_address|source_address_size|spin_iteration|spin_count|starting_position|target_value|test_descriptor_duplication_and_control|test_process_identity|test_open_and_io|test_path_operations|test_terminal_and_system_identity|text_is_equal|text_byte_length|waited_process',
    ko='인수없는체계호출|인수하나체계호출|인수둘체계호출|인수셋체계호출|통신끝점체계호출번호|인수수|인수검사실패|인수검사성공|초기값없는자료영채움|여덟자리묶음값|여덟자리묶음배열|검사수|요청끝점|실행교체때닫기실패|실행교체때닫기성공|복사값|작업목록|해석값|예상오류번호|해당오류로실패했는지|실패여부|실패수|첫째항목|항목순번|반복차례|문자열길이구하기|불러온값|기억영역|이전값|부모과정|검사통과|통과여부|선언번역시험|동적기억동작시험|실행과정동작시험|과정전용값|기다림없이자식회수|결과알리기|뿌리경로|검사자료|전문쓰기|둘째항목|응답끝점|응답끝점주소|출발주소크기|회전차례|회전수|시작위치|대상값|서술번호복제와제어시험|실행주체시험|열기와입출력시험|경로동작시험|단말과체제정보시험|문자열같은지|문자열묶음길이|기다린과정')

PATH_KEYS = ('netinet in arpa inet stddef stdint sys types utsname wait compile exec_runtime '
             'exec_target fork_runtime heap_runtime runtime socket_runtime stdin_runtime').split()

GROUPS['implementation-helper'][1].update({
    'ja': '引数なし体系呼出し|引数一つ体系呼出し|引数二つ体系呼出し|引数三つ体系呼出し|通信端点体系呼出番号|引数の数|引数検査失敗|引数検査成功|未初期化資料の零埋め|八桁組値|八桁組配列|検査数|要求端点|実行置換時閉鎖失敗|実行置換時閉鎖成功|複写値|作業目録|解釈値|期待誤り番号|指定誤りによる失敗判定|失敗判定|失敗数|最初の項|項の添字|反復回数|文字列長を得る|読込値|記憶領域|以前の値|親過程|検査合格|合格判定|宣言翻訳試験|動的記憶動作試験|実行過程動作試験|過程専用値|待たずに子を回収|結果を報告|根の経路|検査資料|電文を書く|二番目の項|応答端点|応答端点番地|送信元番地長|回転回数|回転数|開始位置|対象値|記述番号複製と制御試験|実行主体試験|開閉入出力試験|経路操作試験|端末と体系情報試験|文字列一致判定|文字列組長|待った過程',
    'ja_Hira': 'ひきすうなしたいけいよびだし|ひきすうひとつたいけいよびだし|ひきすうふたつたいけいよびだし|ひきすうみっつたいけいよびだし|つうしんたんてんたいけいよびだしばんごう|ひきすうのかず|ひきすうけんさしっぱい|ひきすうけんさせいこう|みしょきかしりょうのれいうめ|はちけたぐみち|はちけたぐみはいれつ|けんさすう|ようきゅうたんてん|じっこうちかんじへいさしっぱい|じっこうちかんじへいさせいこう|ふくしゃち|さぎょうもくろく|かいしゃくち|きたいあやまりばんごう|していあやまりによるしっぱいはんてい|しっぱいはんてい|しっぱいすう|さいしょのこう|こうのそえじ|はんぷくかいすう|もじれつちょうをえる|よみこみち|きおくりょういき|いぜんのあたい|おやかてい|けんさごうかく|ごうかくはんてい|せんげんほんやくしけん|どうてききおくどうさしけん|じっこうかていどうさしけん|かていせんようち|またずにこをかいしゅう|けっかをほうこく|ねのけいろ|けんさしりょう|でんぶんをかく|にばんめのこう|おうとうたんてん|おうとうたんてんばんち|そうしんもとばんちちょう|かいてんかいすう|かいてんすう|かいしいち|たいしょうち|きじゅつばんごうふくせいとせいぎょしけん|じっこうしゅたいしけん|かいへいにゅうしゅつりょくしけん|けいろそうさしけん|たんまつとたいけいじょうほうしけん|もじれついっちはんてい|もじれつくみちょう|まったかてい',
    'zh_Hans': '无参数系统调用|单参数系统调用|双参数系统调用|三参数系统调用|通信端点系统调用编号|参数数量|参数检查失败|参数检查成功|未初始化数据清零|字节值|字节数组|检查次数|请求端点|程序替换时关闭失败|程序替换时关闭成功|复制值|工作目录|解码值|预期错误编号|检查是否指定错误|失败标志|失败次数|首项|项目索引|迭代次数|取得文本长度|加载值|内存区域|原有值|父进程|检查通过|通过标志|声明编译试验|动态内存行为试验|进程行为试验|进程私有值|不等待回收子进程|报告结果|根路径|受检数据|写出报文|第二项|响应端点|响应端点地址|来源地址大小|循环轮次|循环次数|起始位置|目标值|描述编号复制与控制试验|执行身份试验|打开与读写试验|路径操作试验|终端与系统信息试验|检查文本相等|文本字节长度|已等待进程',
    'zh_Hant': '無引數系統呼叫|單引數系統呼叫|雙引數系統呼叫|三引數系統呼叫|通訊端點系統呼叫編號|引數數量|引數檢查失敗|引數檢查成功|未初始化資料清零|位元組值|位元組陣列|檢查次數|請求端點|程式替換時關閉失敗|程式替換時關閉成功|複製值|工作目錄|解碼值|預期錯誤編號|檢查是否指定錯誤|失敗旗標|失敗次數|首項|項目索引|迭代次數|取得文字長度|載入值|記憶體區域|原有值|父行程|檢查通過|通過旗標|宣告編譯試驗|動態記憶體行為試驗|行程行為試驗|行程私有值|不等待回收子行程|報告結果|根路徑|受檢資料|寫出訊息|第二項|回應端點|回應端點位址|來源位址大小|迴圈輪次|迴圈次數|起始位置|目標值|描述編號複製與控制試驗|執行身分試驗|開啟與讀寫試驗|路徑操作試驗|終端與系統資訊試驗|檢查文字相等|文字位元組長度|已等待行程',
})
PATH_ROWS = {
    'en': 'internetwork|address|network_conversion|byte_order|basic_definitions|integer_types|system|data_types|system_identity|child_wait|compilation|program_replacement_test|replacement_target|process_fork_test|dynamic_memory_test|runtime_test|endpoint_test|standard_input_test',
    'ko': '상호연결망|주소|통신주소|여덟자리묶음순서|기본정의|정수형|체계|자료형|체제정보|자식대기|번역검사|실행내용교체시험|교체실행대상|실행과정분기시험|동적기억시험|실행시험|통신끝점시험|표준입력시험',
    'ja': '相互接続網|番地|通信番地|八桁組順序|基本定義|整数型|体系|資料型|体系情報|子の待機|翻訳検査|実行内容置換試験|置換実行対象|実行過程分岐試験|動的記憶試験|実行試験|通信端点試験|標準入力試験',
    'ja_Hira': 'そうごせつぞくもう|ばんち|つうしんばんち|はちけたぐみじゅんじょ|きほんていぎ|せいすうがた|たいけい|しりょうがた|たいけいじょうほう|このたいき|ほんやくけんさ|じっこうないようちかんしけん|ちかんじっこうたいしょう|じっこうかていぶんきしけん|どうてききおくしけん|じっこうしけん|つうしんたんてんしけん|ひょうじゅんにゅうりょくしけん',
    'zh_Hans': '互联网络|地址|通信地址|字节顺序|基本定义|整数类型|系统|数据类型|系统身份|子进程等待|编译检查|程序替换试验|替换执行目标|进程分支试验|动态内存试验|运行试验|通信端点试验|标准输入试验',
    'zh_Hant': '互聯網路|位址|通訊位址|位元組順序|基本定義|整數型別|系統|資料型別|系統身分|子行程等待|編譯檢查|程式替換試驗|替換執行目標|行程分支試驗|動態記憶體試驗|執行試驗|通訊端點試驗|標準輸入試驗',
    'de': 'Netzverbund|Adresse|Netzadressumwandlung|Bytereihenfolge|Grunddefinitionen|Ganzzahltypen|System|Datentypen|Systemkennung|Kindwartung|Übersetzungsprüfung|Programmwechselprüfung|Wechselziel|Prozessverzweigungsprüfung|Speicherprüfung|Laufzeitprüfung|Endpunktprüfung|Standardeingabeprüfung',
    'fr': 'interréseau|adresse|conversion des adresses|ordre des octets|définitions de base|types entiers|système|types de données|identité du système|attente des enfants|vérification de compilation|essai de remplacement du programme|cible de remplacement|essai de dédoublement du processus|essai de mémoire dynamique|essai en exécution|essai du point de communication|essai entrée standard',
    'es': 'entre redes|dirección|conversión de direcciones|orden de octetos|definiciones básicas|tipos enteros|sistema|tipos de datos|identidad del sistema|espera de hijos|prueba de compilación|prueba de sustitución del programa|destino de sustitución|prueba de bifurcación del proceso|prueba de memoria dinámica|prueba de ejecución|prueba de extremo|prueba de entrada estándar',
    'pt': 'entre redes|endereço|conversão de endereços|ordem de octetos|definições básicas|tipos inteiros|sistema|tipos de dados|identidade do sistema|espera de filhos|teste de compilação|teste de substituição do programa|destino de substituição|teste de bifurcação do processo|teste de memória dinâmica|teste de execução|teste do extremo|teste de entrada padrão',
    'ru': 'межсетевое взаимодействие|адрес|преобразование адресов|порядок байтов|основные определения|целочисленные типы|система|типы данных|сведения о системе|ожидание потомков|проверка компиляции|проверка замены программы|цель замены|проверка ветвления процесса|проверка динамической памяти|проверка выполнения|проверка конечной точки|проверка стандартного ввода',
    'ar': 'الشبكات المترابطة|العنوان|تحويل عناوين الاتصال|ترتيب الثمانيات|التعريفات الأساسية|أنواع الأعداد الصحيحة|النظام|أنواع البيانات|هوية النظام|انتظار العمليات الفرعية|فحص الترجمة|اختبار استبدال البرنامج|هدف الاستبدال|اختبار تفرع العملية|اختبار الذاكرة المتغيرة|اختبار التنفيذ|اختبار نقطة الاتصال|اختبار الإدخال القياسي',
    'hi': 'अंतरजाल|पता|संचार पता परिवर्तन|अष्टक क्रम|मूल परिभाषाएँ|पूर्णांक प्रकार|प्रणाली|आँकड़ा प्रकार|प्रणाली पहचान|संतान प्रतीक्षा|संकलन जाँच|कार्यक्रम प्रतिस्थापन परीक्षण|प्रतिस्थापन लक्ष्य|प्रक्रिया शाखा परीक्षण|गतिशील स्मृति परीक्षण|निष्पादन परीक्षण|संचार छोर परीक्षण|मानक निवेश परीक्षण',
    'ta': 'பிணையங்களிடை|முகவரி|தொடர்பு முகவரி மாற்றம்|எட்டு இரும இலக்கக் குழு வரிசை|அடிப்படை வரையறைகள்|முழுஎண் வகைகள்|அமைப்பு|தரவு வகைகள்|அமைப்பு அடையாளம்|சேய் காத்திருப்பு|தொகுப்பு சரிபார்ப்பு|நிரல் மாற்றச் சோதனை|மாற்ற இலக்கு|செயல்முறைக் கிளைச் சோதனை|இயங்குநிலை நினைவகச் சோதனை|இயக்கச் சோதனை|தொடர்பு முனைச் சோதனை|நிலையான உள்ளீட்டுச் சோதனை',
}

CATEGORIES = {key: category for category, (keys, _) in GROUPS.items() for key in keys}
KEYS = list(CATEGORIES)


def base_language(language):
    if language in ('ja_Hira', 'ja_Kana') or language.startswith('zh_'):
        return language
    return language.split('_')[0]


def explicit(language):
    base = base_language(language)
    selected = 'ja_Hira' if base == 'ja_Kana' else base
    names = {}
    for keys, rows in GROUPS.values():
        if selected in rows:
            values = rows[selected].split('|')
            if len(values) != len(keys):
                raise ValueError(('identifiers', selected, len(keys), len(values)))
            names.update(zip(keys, values))
    paths = {}
    if selected in PATH_ROWS:
        values = PATH_ROWS[selected].split('|')
        if len(values) != len(PATH_KEYS):
            raise ValueError(('paths', selected, len(values), len(PATH_KEYS)))
        paths.update(zip(PATH_KEYS, values))
    if base == 'ja_Kana':
        def kana(value):
            return ''.join(chr(ord(ch) + 0x60) if '\u3041' <= ch <= '\u3096' else ch for ch in value)
        names = {key: kana(value) for key, value in names.items()}
        paths = {key: kana(value) for key, value in paths.items()}
    return names, paths


def meanings():
    return {key: value for keys, rows in GROUPS.values()
            for key, value in zip(keys, rows['en'].split('|'))}
