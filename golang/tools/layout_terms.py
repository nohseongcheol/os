"""Reviewed whole-role proposals for edition-local management file names.

These are project names, not official/native-speaker-certified terminology.
Unsupported languages retain explicitly labelled English management names;
they never inherit Korean names or invented phonetic transcriptions.
"""
KEYS = '''소스 이름대응표.tsv 파일대응표.tsv 용어사전.tsv 용어근거.tsv
새명명-식별자.tsv 새명명-경로.tsv 새명명-용어.tsv 명명검토대기.tsv 명명검증.json 나라언어.md
문자대응.json 문자빌드.py 빌드규칙.mk 식별자대응.tsv 문자판안내.md 원본자료
이름대응.tsv 파일대응.tsv 기능범위.tsv 보존식별자.tsv 선언용어근거.tsv
사용자영역선언대응.tsv 셸이름대응.tsv 명령대응.tsv'''.split()

ROWS = {
    'en': 'source|name-correspondence|file-correspondence|glossary|term-evidence|revised-identifiers|revised-paths|revised-terms|naming-review-pending|naming-audit|edition-language|script-mapping|script-build|build-rules|identifier-mapping|script-edition-guide|inherited-material|identifier-correspondence|file-path-correspondence|feature-scope|preserved-identifiers|declaration-term-evidence|userspace-declaration-correspondence|build-shell-identifier-correspondence|command-correspondence',
    'ko': '원문|이름대응표|파일대응표|용어사전|용어근거|새명명-식별자|새명명-경로|새명명-용어|명명검토대기|명명검증|나라언어|문자대응|문자판구축|구축규칙|식별자대응|문자판안내|원본자료|이름대응|파일대응|기능범위|보존식별자|선언용어근거|사용자영역선언대응|구축명령식별자대응|명령대응',
    'zh_Hans': '源代码|名称对应表|文件对应表|术语词表|术语依据|修订标识符|修订路径|修订术语|待审命名|命名核验|版本语言|文字映射|文字构建|构建规则|标识符映射|文字版本指南|继承资料|标识符对应|文件路径对应|功能范围|保留标识符|声明术语依据|用户空间声明对应|构建脚本标识符对应|命令对应',
    'zh_Hant': '原始碼|名稱對照表|檔案對照表|術語詞表|術語依據|修訂識別字|修訂路徑|修訂術語|待審命名|命名核驗|版本語言|文字對映|文字建置|建置規則|識別字對映|文字版本指南|承襲資料|識別字對照|檔案路徑對照|功能範圍|保留識別字|宣告術語依據|使用者空間宣告對照|建置指令稿識別字對照|命令對照',
    'ja': '原始記述|名前対応表|資料対応表|用語集|用語の根拠|改訂識別子|改訂経路|改訂用語|命名の検討待ち|命名検証|版の言語|文字対応|文字版構築|構築規則|識別子対応|文字版案内|継承資料|識別名対応|資料経路対応|機能範囲|保持識別子|宣言用語の根拠|利用者領域宣言対応|構築手順識別子対応|命令対応',
    'ja_Hira': 'げんしきじゅつ|なまえたいおうひょう|しりょうたいおうひょう|ようごしゅう|ようごのこんきょ|かいていしきべつし|かいていけいろ|かいていようご|めいめいのけんとうまち|めいめいけんしょう|はんのげんご|もじたいおう|もじはんこうちく|こうちくきそく|しきべつしたいおう|もじはんあんない|けいしょうしりょう|しきべつめいたいおう|しりょうけいろたいおう|きのうはんい|ほじしきべつし|せんげんようごのこんきょ|りようしゃりょういきせんげんたいおう|こうちくてじゅんしきべつしたいおう|めいれいたいおう',
    'de': 'Quelltext|Namenszuordnung|Dateizuordnung|Begriffsverzeichnis|Begriffsbelege|überarbeitete-Bezeichner|überarbeitete-Pfade|überarbeitete-Begriffe|offene-Namensprüfung|Namensprüfung|Ausgabesprache|Schriftzuordnung|Schriftfassung-erstellen|Erstellungsregeln|Bezeichnerabbildung|Anleitung-zur-Schriftfassung|übernommene-Unterlagen|Bezeichnerzuordnung|Dateipfadzuordnung|Funktionsumfang|beibehaltene-Bezeichner|Belege-der-Deklarationsbegriffe|Benutzerbereichsdeklarationen-Zuordnung|Erstellungsskript-Bezeichnerzuordnung|Befehlszuordnung',
    'fr': 'code-source|correspondance-des-noms|correspondance-des-fichiers|glossaire|justification-des-termes|identifiants-révisés|chemins-révisés|termes-révisés|noms-à-examiner|vérification-des-noms|langue-de-la-version|correspondance-des-écritures|construction-de-la-version-écrite|règles-de-construction|table-des-identifiants|guide-de-la-version-écrite|documents-hérités|correspondance-des-identifiants|correspondance-des-chemins|périmètre-fonctionnel|identifiants-conservés|justification-des-termes-de-déclaration|correspondance-des-déclarations-utilisateur|correspondance-des-identifiants-du-script-de-construction|correspondance-des-commandes',
    'es': 'código-fuente|correspondencia-de-nombres|correspondencia-de-archivos|glosario|fundamento-de-términos|identificadores-revisados|rutas-revisadas|términos-revisados|nombres-pendientes-de-revisión|verificación-de-nombres|idioma-de-la-edición|correspondencia-de-escrituras|construcción-de-la-edición-escrita|reglas-de-construcción|tabla-de-identificadores|guía-de-la-edición-escrita|documentos-heredados|correspondencia-de-identificadores|correspondencia-de-rutas|alcance-funcional|identificadores-conservados|fundamento-de-términos-de-declaración|correspondencia-de-declaraciones-de-usuario|correspondencia-de-identificadores-del-guion-de-construcción|correspondencia-de-órdenes',
    'pt': 'código-fonte|correspondência-de-nomes|correspondência-de-ficheiros|glossário|fundamentação-dos-termos|identificadores-revistos|caminhos-revistos|termos-revistos|nomes-por-rever|verificação-de-nomes|língua-da-edição|correspondência-de-escritas|construção-da-edição-escrita|regras-de-construção|tabela-de-identificadores|guia-da-edição-escrita|documentos-herdados|correspondência-de-identificadores|correspondência-de-caminhos|âmbito-funcional|identificadores-mantidos|fundamentação-dos-termos-de-declaração|correspondência-de-declarações-do-utilizador|correspondência-de-identificadores-do-roteiro-de-construção|correspondência-de-comandos',
    'it': 'codice-sorgente|corrispondenza-dei-nomi|corrispondenza-dei-file|glossario|motivazione-dei-termini|identificatori-rivisti|percorsi-rivisti|termini-rivisti|nomi-da-esaminare|verifica-dei-nomi|lingua-dell-edizione|corrispondenza-delle-scritture|costruzione-dell-edizione-scritta|regole-di-costruzione|tabella-degli-identificatori|guida-all-edizione-scritta|documenti-ereditati|corrispondenza-degli-identificatori|corrispondenza-dei-percorsi|ambito-funzionale|identificatori-conservati|motivazione-dei-termini-di-dichiarazione|corrispondenza-delle-dichiarazioni-utente|corrispondenza-degli-identificatori-dello-script-di-costruzione|corrispondenza-dei-comandi',
    'ru': 'исходный-код|соответствие-имён|соответствие-файлов|словарь-терминов|обоснование-терминов|уточнённые-идентификаторы|уточнённые-пути|уточнённые-термины|имена-на-рассмотрении|проверка-именования|язык-редакции|соответствие-письменностей|сборка-письменной-редакции|правила-сборки|таблица-идентификаторов|руководство-письменной-редакции|унаследованные-материалы|соответствие-идентификаторов|соответствие-путей-файлов|область-функций|сохранённые-идентификаторы|обоснование-терминов-объявлений|соответствие-объявлений-пользовательской-области|соответствие-идентификаторов-сценария-сборки|соответствие-команд',
    'ar': 'النص-المصدري|مطابقة-الأسماء|مطابقة-الملفات|مسرد-المصطلحات|مسوغات-المصطلحات|المعرفات-المنقحة|المسارات-المنقحة|المصطلحات-المنقحة|أسماء-بانتظار-المراجعة|التحقق-من-التسمية|لغة-الإصدار|مطابقة-أنظمة-الكتابة|بناء-الإصدار-الكتابي|قواعد-البناء|جدول-المعرفات|دليل-الإصدار-الكتابي|المواد-الموروثة|مطابقة-المعرفات|مطابقة-مسارات-الملفات|نطاق-الوظائف|المعرفات-المحفوظة|مسوغات-مصطلحات-التصريح|مطابقة-تصريحات-حيز-المستخدم|مطابقة-معرفات-نص-البناء|مطابقة-الأوامر',
    'hi': 'मूल-पाठ|नाम-संगति-सारणी|संचिका-संगति-सारणी|शब्दावली|शब्द-चयन-आधार|संशोधित-पहचानकर्ता|संशोधित-पथ|संशोधित-शब्द|समीक्षाधीन-नाम|नामकरण-जाँच|संस्करण-भाषा|लिपि-संगति|लिपि-संस्करण-निर्माण|निर्माण-नियम|पहचानकर्ता-सारणी|लिपि-संस्करण-मार्गदर्शिका|प्राप्त-मूल-सामग्री|पहचानकर्ता-संगति|संचिका-पथ-संगति|कार्य-सीमा|संरक्षित-पहचानकर्ता|घोषणा-शब्द-चयन-आधार|उपयोगकर्ता-क्षेत्र-घोषणा-संगति|निर्माण-निर्देश-पहचानकर्ता-संगति|आदेश-संगति',
    'ta': 'மூல-உரை|பெயர்-ஒப்புமை-அட்டவணை|கோப்பு-ஒப்புமை-அட்டவணை|கலைச்சொல்-அகராதி|சொல்-தேர்வு-ஆதாரம்|திருத்திய-அடையாளங்காட்டிகள்|திருத்திய-பாதைகள்|திருத்திய-சொற்கள்|மதிப்பாய்வுக்கான-பெயர்கள்|பெயரிடல்-சரிபார்ப்பு|பதிப்பின்-மொழி|எழுத்துமுறை-ஒப்புமை|எழுத்துமுறைப்-பதிப்பு-உருவாக்கம்|உருவாக்க-விதிகள்|அடையாளங்காட்டி-அட்டவணை|எழுத்துமுறைப்-பதிப்பு-வழிகாட்டி|பெறப்பட்ட-மூலப்பொருட்கள்|அடையாளங்காட்டி-ஒப்புமை|கோப்புப்-பாதை-ஒப்புமை|செயல்பாட்டு-வரம்பு|தக்கவைத்த-அடையாளங்காட்டிகள்|அறிவிப்புச்-சொல்-ஆதாரம்|பயனர்-வெளி-அறிவிப்பு-ஒப்புமை|உருவாக்க-நிரல்-அடையாளங்காட்டி-ஒப்புமை|கட்டளை-ஒப்புமை',
}


def proposals(language):
    base = language if language.startswith(('ja_', 'zh_')) else language.split('_')[0]
    base = 'ja' if base == 'ja_Jpan' else base
    selected = 'ja_Hira' if base == 'ja_Kana' else base
    status = 'project-proposal' if selected in ROWS else 'pending-language-review'
    values = ROWS.get(selected, ROWS['en']).split('|')
    if len(values) != len(KEYS):
        raise ValueError(('management-role-count', language, len(values), len(KEYS)))
    if base == 'ja_Kana':
        values = [''.join(chr(ord(c) + 96) if '\u3041' <= c <= '\u3096' else c for c in v) for v in values]
    from pathlib import Path
    names = {old: value + Path(old).suffix for old, value in zip(KEYS, values)}
    if len(set(names.values())) != len(names):
        raise ValueError('Management name collision: ' + language)
    for name in names.values():
        if len(name.encode('utf-8')) > 250 or '/' in name or '\\' in name or name in ('.', '..'):
            raise ValueError('Unsafe/overlong management name: ' + name)
    return names, status
