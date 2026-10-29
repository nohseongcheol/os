#!/usr/bin/env python3
"""Freeze provenance-aware naming proposals; generation uses only the snapshot."""
import gettext
import importlib.util
import json
from pathlib import Path
import re
import unicodedata
import xml.etree.ElementTree as ET
from naming_review import apply_terms
ROOT = Path(__file__).resolve().parents[1]
KEYS = 'action address api append arguments button choose chooser class close command compile connect current data datagram directory error event exception execute file initialize key label line load messages mode name open output panel parser path port position process read reader remove result run save seek settings size source split stop sync terminal text thread toolbar window worker workspace write'.split()
DIRECT = {
'en': 'action|address|SystemCalls|append|arguments|button|choose|chooser|className|close|command|compile|connect|current|data|datagram|directory|error|event|exception|execute|file|initialize|key|label|line|load|messages|mode|name|open|output|panel|parser|path|port|position|process|read|reader|remove|result|run|save|seek|settings|size|source|split|stop|sync|terminal|text|thread|toolbar|window|worker|Workspace|write',
'ko': '동작|주소|체계호출|덧붙이기|인수|단추|고르기|고름창|자료형이름|닫기|명령|번역하기|연결하기|현재값|자료|독립전문|자료목록|오류|사건|예외|실행하기|자료파일|초기화하기|열쇠|표시말|줄|불러오기|안내말|방식|이름|열기|출력|판|문장해석기|경로|통신문|위치|실행과정|읽기|읽는이|지우기|결과|가동하기|저장하기|위치옮기기|설정|크기|원문|나누기|멈추기|기록맞추기|명령창|글|실행가닥|도구막대|창|작업가닥|작업마당|쓰기',
'ja': '動作|住所|体系呼出し|追記する|引数|押し釦|選ぶ|選択窓|型名|閉じる|命令|翻訳する|接続する|現在値|資料|独立電文|資料目録|誤り|出来事|例外|実行する|文書|初期化する|鍵|表示語|行|読み込む|案内文|方式|名前|開く|出力|区画|構文解析器|経路|通信口|位置|実行過程|読む|読取り器|削除する|結果|起動する|保存する|位置を移す|設定|大きさ|原文|分ける|止める|記録を同期する|命令窓|文字列|実行の糸|道具欄|窓|作業の糸|作業場|書く',
'de': 'Aktion|Adresse|Systemaufrufe|anhängen|Argumente|Schaltfläche|auswählen|Auswahlfenster|Klassenname|schließen|Befehl|übersetzen|verbinden|aktuell|Daten|Datagramm|Verzeichnis|Fehler|Ereignis|Ausnahme|ausführen|Datei|vorbereiten|Schlüssel|Beschriftung|Zeile|laden|Meldungen|Modus|Name|öffnen|Ausgabe|Bereich|Syntaxleser|Pfad|Anschluss|Position|Prozess|lesen|Leser|entfernen|Ergebnis|starten|speichern|positionieren|Einstellungen|Größe|Quelltext|teilen|anhalten|abgleichen|Befehlsfenster|Text|Ausführungsfaden|Werkzeugleiste|Fenster|Arbeitsfaden|Arbeitsplatz|schreiben',
'fr': 'action|adresse|AppelsSystème|ajouter|arguments|bouton|choisir|sélecteur|nomClasse|fermer|commande|compiler|connecter|courant|données|datagramme|répertoire|erreur|événement|exception|exécuter|fichier|initialiser|clé|étiquette|ligne|charger|messages|mode|nom|ouvrir|sortie|panneau|analyseur|chemin|port|position|processus|lire|lecteur|supprimer|résultat|lancer|enregistrer|positionner|réglages|taille|source|séparer|arrêter|synchroniser|terminal|texte|fil|barreOutils|fenêtre|filTravail|Atelier|écrire',
'es': 'acción|dirección|LlamadasSistema|añadir|argumentos|botón|elegir|selector|nombreClase|cerrar|orden|compilar|conectar|actual|datos|datagrama|directorio|error|suceso|excepción|ejecutar|archivo|inicializar|clave|etiqueta|línea|cargar|mensajes|modo|nombre|abrir|salida|panel|analizador|ruta|puerto|posición|proceso|leer|lector|eliminar|resultado|iniciar|guardar|posicionar|ajustes|tamaño|fuente|separar|detener|sincronizar|terminal|texto|hilo|barraHerramientas|ventana|hiloTrabajo|Taller|escribir',
'ar': 'إجراء|عنوان|نداءاتالنظام|إلحاق|وسائط|زر|اختيار|منتقي|اسمالصنف|إغلاق|أمر|ترجمة|اتصال|حالي|بيانات|رزمةمستقلة|دليل|خطأ|حدث|استثناء|تنفيذ|ملف|تهيئة|مفتاح|تسمية|سطر|تحميل|رسائل|نمط|اسم|فتح|مخرجات|لوحة|محلل|مسار|منفذ|موضع|عملية|قراءة|قارئ|إزالة|نتيجة|تشغيل|حفظ|نقلالموضع|إعدادات|حجم|مصدر|تقسيم|إيقاف|مزامنة|طرفية|نص|خيط|شريطالأدوات|نافذة|خيطالعمل|ورشة|كتابة',
'hi': 'क्रिया|पता|तंत्रआह्वान|जोड़ें|तर्क|बटन|चुनें|चयनक|वर्गनाम|बंदकरें|आदेश|संकलन|जोड़ना|वर्तमान|आँकड़े|स्वतंत्रसंदेश|निर्देशिका|त्रुटि|घटना|अपवाद|निष्पादन|संचिका|आरंभ|कुंजी|लेबल|पंक्ति|लोडकरें|संदेश|विधि|नाम|खोलें|निर्गम|पट्ट|विश्लेषक|पथ|द्वार|स्थान|प्रक्रिया|पढ़ें|पाठक|हटाएँ|परिणाम|चलाएँ|सहेजें|स्थानबदलें|विन्यास|आकार|स्रोत|विभाजन|रोकें|समक्रमण|आदेशपटल|पाठ|सूत्र|उपकरणपट्टी|खिड़की|कार्यसूत्र|कार्यशाला|लिखें',
'zh': '动作|地址|系统调用|追加|参数|按钮|选择|选择器|类名|关闭|命令|编译|连接|当前|数据|独立报文|目录|错误|事件|异常|执行|文件|初始化|键|标签|行|加载|消息|方式|名称|打开|输出|面板|解析器|路径|端口|位置|进程|读取|读取器|删除|结果|运行|保存|定位|设置|大小|源文|分割|停止|同步|终端|文本|线程|工具栏|窗口|工作线程|工作坊|写入',
'zh_Hant': '動作|位址|系統呼叫|附加|引數|按鈕|選擇|選擇器|類別名稱|關閉|命令|編譯|連線|目前|資料|獨立電文|目錄|錯誤|事件|例外|執行|檔案|初始化|鍵|標籤|列|載入|訊息|方式|名稱|開啟|輸出|面板|剖析器|路徑|通訊埠|位置|行程|讀取|讀取器|刪除|結果|運行|儲存|定位|設定|大小|原文|分割|停止|同步|終端|文字|執行緒|工具列|視窗|工作執行緒|工作坊|寫入',
}
ALIASES = {'arguments':'arguments','current':'current','directory':'path','file':'file_name','line':'input_line','name':'name','output':'output','path':'path','position':'position','process':'process','read':'read','size':'size','source':'source_file','text':'text','thread':'thread','write':'write','command':'command','api':'system_call','workspace':'user_space','error':'error_number','terminal':'shell_name','append':'append','remove':'free_memory','split':'split_arguments','datagram':'udp','parser':'command_source'}
# Only exact concept matches are imported; memory release is not file removal.
for key in ['remove', 'datagram', 'parser', 'workspace', 'error', 'split']: ALIASES.pop(key, None)
ENGLISH = {'api':'System calls','workspace':'Workspace','class':'Class name','seek':'Seek','sync':'Synchronize','worker':'Worker','chooser':'File chooser','initialize':'Initialize','append':'Append'}
def identifier(value):
    value=unicodedata.normalize('NFC', value)
    value=re.sub(r'\s*\([_&]?[A-Za-z]\)\s*', '', value).replace('_','').replace('&','')
    value=''.join(c if (unicodedata.category(c)[0] in 'LMN' or c=='_') else '_' for c in value)
    value=re.sub('_+', '_', value).strip('_')
    if not value or unicodedata.category(value[0])[0] not in 'L': value='v_'+value
    return value

def module(name):
    spec=importlib.util.spec_from_file_location(name,str(ROOT/'naming/upstream'/ (name+'.py')))
    result=importlib.util.module_from_spec(spec); spec.loader.exec_module(result);return result

def collect():
    languages={l.get('type') for t in ET.parse(str(ROOT/'vendor/cldr48-supplementalData.xml')).findall('.//territoryInfo/territory') for l in t}
    languages.update(DIRECT)
    proposed={}
    for module_name,groups in [('shell_terms',[('FIELDS','FIELD_KEYS'),('FUNCTIONS','FUNCTION_KEYS'),('HOST','HOST_KEYS')]),('naming_lexicon',[('PATHS','PATH_KEYS'),('ACTIONS','ACTION_KEYS')]),('variant_terms',[('ROWS','KEYS')])]:
        data=module(module_name)
        for values,keys in groups:
            rows=getattr(data,values,{})
            for lang,row in rows.items():
                if isinstance(row,str):
                    proposed.setdefault(lang,{}).update(dict(zip(getattr(data,keys),row.split('|'))))
    output={}
    for lang in sorted(languages):
        base=lang.split('_')[0]; lookup={'zh':'zh_Hans','sr':'sr_Cyrl','az':'az_Latn','ky':'ky_Cyrl','uz':'uz_Latn','mn':'mn_Cyrl'}.get(lang,lang)
        catalogues=[]
        for root in ['/usr/share/locale','/usr/share/locale-langpack']:
            for local in ([lang] if '_' in lang else [lang, base]):
                folder=Path(root)/local/'LC_MESSAGES'
                if folder.exists():
                    for path in sorted(folder.glob('*.mo')):
                        try:
                            with path.open('rb') as stream: catalogues.append((str(path),gettext.GNUTranslations(stream)))
                        except (OSError,ValueError,IndexError,UnicodeError): pass
        rows={};used=set()
        for key in KEYS:
            text=None; origin=None
            if lang in DIRECT:
                assert len(DIRECT[lang].split('|'))==len(KEYS),lang
                text=DIRECT[lang].split('|')[KEYS.index(key)];origin='WorldOS functional naming proposal 2026-09-13'
            elif ALIASES.get(key) in proposed.get(lookup,{}):
                text=proposed[lookup][ALIASES[key]];origin='WorldOS prior functional naming proposal (naming/upstream)'
            else:
                queries=[ENGLISH.get(key,key.capitalize()),key.capitalize(),key.upper(),key]
                for source,cat in catalogues:
                    for query in queries:
                        for marked in [query,'_'+query,query+'…',query+'...']:
                            value=cat.gettext(marked)
                            if value != marked and '<' not in value and '%' not in value and '\n' not in value and len(value)<70:
                                text=value;origin='GNU gettext catalogue '+source;break
                        if text:break
                    if text:break
            status='proposal' if text else 'untranslated'
            if not text:text=DIRECT['en'].split('|')[KEYS.index(key)];origin='English fallback; language review required'
            symbol=identifier(text)
            # A concept suffix resolves homonyms without silently aliasing distinct operations.
            suffix=2;original=symbol
            while symbol in used or symbol in {'class','int','new','return','switch','public','private','static','void','package','import','do','try','throw','throws','null','true','false','this','super','default','interface','enum','var','record','yield','long','byte','short','boolean','double','float','char','if','else','for','while','break','continue','case','catch','finally','final','instanceof','synchronized','transient','volatile','abstract','native','assert','const','goto','implements','extends','protected'}:
                symbol=original+'_'+str(suffix);suffix+=1
            used.add(symbol)
            rows[key]={'text':text,'identifier':symbol,'status':status,'source':origin,'native_review':'pending'}
        output[lang]=rows
    output=apply_terms(output)
    (ROOT/'naming/terms.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Naming snapshots:',len(output),'languages')
if __name__=='__main__':collect()
