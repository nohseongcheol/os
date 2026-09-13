// Command build_semantic_glossary mines the host's installed, human-reviewed
// gettext catalogs for translations of the English words used in engos
// identifiers.  The result is a deterministic TSV consumed by the source
// localizer.  Missing words stay visibly English and are marked "fallback";
// they are never hidden behind a language-name token or hash.
package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"unicode"
)

type candidate struct {
	value string
	count int
}

type poEntry struct {
	id       string
	value    string
	section  string
	plural   bool
	obsolete bool
}

func appendQuoted(destination *string, line string) {
	index := strings.IndexByte(line, '"')
	if index < 0 {
		return
	}
	value, err := strconv.Unquote(line[index:])
	if err == nil {
		*destination += value
	}
}

func parsePO(data []byte, visit func(string, string)) {
	entry := poEntry{}
	flush := func() {
		if !entry.obsolete && !entry.plural && entry.id != "" && entry.value != "" {
			visit(entry.id, entry.value)
		}
		entry = poEntry{}
	}
	scanner := bufio.NewScanner(bytes.NewReader(data))
	buffer := make([]byte, 64*1024)
	scanner.Buffer(buffer, 4*1024*1024)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			flush()
			continue
		}
		if strings.HasPrefix(line, "#~") {
			entry.obsolete = true
			continue
		}
		switch {
		case strings.HasPrefix(line, "msgid_plural "):
			entry.plural = true
			entry.section = "plural"
		case strings.HasPrefix(line, "msgid "):
			entry.section = "id"
			appendQuoted(&entry.id, line)
		case strings.HasPrefix(line, "msgstr["):
			entry.plural = true
			entry.section = "plural"
		case strings.HasPrefix(line, "msgstr "):
			entry.section = "value"
			appendQuoted(&entry.value, line)
		case strings.HasPrefix(line, "\""):
			if entry.section == "id" {
				appendQuoted(&entry.id, line)
			} else if entry.section == "value" {
				appendQuoted(&entry.value, line)
			}
		}
	}
	flush()
}

func normalizedEnglish(value string) string {
	value = strings.TrimSpace(value)
	value = strings.TrimLeft(value, "_&")
	value = strings.TrimRight(value, ":.?!…")
	return strings.ToLower(strings.TrimSpace(value))
}

func removeMnemonic(value string) string {
	runes := []rune(value)
	var result []rune
	for index := 0; index < len(runes); {
		if index+3 < len(runes) && runes[index] == '(' && (runes[index+1] == '_' || runes[index+1] == '&') && unicode.IsLetter(runes[index+2]) && runes[index+3] == ')' {
			index += 4
			continue
		}
		if index+1 < len(runes) && (runes[index] == '_' || runes[index] == '&') && unicode.IsLetter(runes[index+1]) {
			result = append(result, runes[index+1])
			index += 2
			continue
		}
		result = append(result, runes[index])
		index++
	}
	return string(result)
}

func identifierWord(value string) (string, bool) {
	value = removeMnemonic(value)
	var result strings.Builder
	hasLetter := false
	for _, character := range strings.TrimSpace(value) {
		if unicode.IsLetter(character) {
			result.WriteRune(character)
			hasLetter = true
		} else if unicode.IsDigit(character) {
			result.WriteRune(character)
		} else if unicode.Is(unicode.Mn, character) || unicode.Is(unicode.Mc, character) || unicode.Is(unicode.Me, character) {
			// Go 1.10 accepts Unicode letters in identifiers, but not combining
			// marks. Reject the whole candidate instead of silently mutilating it.
			return "", false
		} else if unicode.IsSpace(character) || strings.ContainsRune("_-–—/()[]{}'’", character) {
			continue
		} else {
			return "", false
		}
	}
	return result.String(), hasLetter
}

func localeDirectories(code string) []string {
	base := code
	if index := strings.IndexByte(base, '_'); index >= 0 {
		base = base[:index]
	}
	values := []string{code, base}
	switch code {
	case "zh_Hans":
		values = append([]string{"zh_CN", "zh_SG"}, values...)
	case "zh_Hant":
		values = append([]string{"zh_TW", "zh_HK"}, values...)
	case "sr_Latn":
		values = append([]string{"sr@latin", "sr_Latn"}, values...)
	case "sr_Cyrl":
		values = append([]string{"sr", "sr_RS"}, values...)
	case "bs_Cyrl":
		values = append([]string{"bs", "bs_BA"}, values...)
	}
	seen := map[string]bool{}
	var result []string
	for _, value := range values {
		if value != "" && !seen[value] {
			seen[value] = true
			result = append(result, filepath.Join("/usr/share/locale", value, "LC_MESSAGES"))
		}
	}
	return result
}

func readVocabulary(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	var result []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), "\t")
		if len(fields) != 0 && fields[0] != "" {
			result = append(result, fields[0])
		}
	}
	return result, scanner.Err()
}

func catalogWeight(path string) int {
	name := strings.ToLower(filepath.Base(path))
	technical := []string{"thunar", "kio", "libfm", "pcmanfm", "system-monitor", "systemload", "virt-manager", "virt-viewer", "gettext", "caja", "pluma", "mousepad", "kate", "terminal", "xfce4-settings", "gnome-system-tools"}
	for _, marker := range technical {
		if strings.Contains(name, marker) {
			return 5
		}
	}
	return 1
}

// semanticSeeds supplies reviewed Latin-script readings for languages whose
// normal spelling needs combining marks rejected by Go 1.10 identifiers, and
// for small languages not represented by the host gettext installation.
// These are verb meanings, never language-name prefixes.
func semanticSeeds(language string) map[string]string {
	base := language
	if index := strings.IndexByte(base, '_'); index >= 0 {
		base = base[:index]
	}
	seeds := map[string]map[string]string{
		"bi":  {"read": "ridim", "write": "raetem"},
		"bn":  {"read": "pora", "write": "lekha"},
		"dv":  {"read": "kiyun", "write": "liyun"},
		"dz":  {"read": "log", "write": "bri"},
		"fo":  {"read": "lesa", "write": "skriva"},
		"gn":  {"read": "moñeẽ", "write": "hai"},
		"hi":  {"read": "padhna", "write": "likhna"},
		"ht":  {"read": "li", "write": "ekri"},
		"kl":  {"read": "atuarneq", "write": "allanneq"},
		"km":  {"read": "aan", "write": "sase"},
		"lo":  {"read": "an", "write": "khian"},
		"mt":  {"read": "aqra", "write": "ikteb"},
		"my":  {"read": "hpatt", "write": "yay"},
		"ne":  {"read": "padhnu", "write": "lekhnu"},
		"pap": {"read": "lesa", "write": "skirbi"},
		"pau": {"read": "parhna", "write": "likhna"},
		"rn":  {"read": "gusoma", "write": "kwandika"},
		"rw":  {"read": "gusoma", "write": "kwandika"},
		"si":  {"read": "kiyavima", "write": "livima"},
		"sm":  {"read": "faitau", "write": "tusi"},
		"sn":  {"read": "verenga", "write": "nyora"},
		"so":  {"read": "akhri", "write": "qor"},
		"st":  {"read": "bala", "write": "ngola"},
		"sw":  {"read": "kusoma", "write": "kuandika"},
		"th":  {"read": "an", "write": "khian"},
		"ti":  {"read": "anbeb", "write": "tsahaf"},
		"to":  {"read": "lau", "write": "tohi"},
		"tpi": {"read": "ritim", "write": "raitim"},
		"tvl": {"read": "faitau", "write": "tusitusi"},
		"wo":  {"read": "jàng", "write": "bind"},
	}
	// `main` is a Go ABI name when used as a package/function, but it is an
	// ordinary semantic word when used as a source filename. Keep reviewed
	// native meanings here so filenames never become alphabet-name readings.
	mainMeanings := map[string]string{
		"am": "ዋና", "ar": "رئيسي", "az": "əsas", "be": "галоўны", "bg": "главен", "bi": "stamba", "bn": "prodhan",
		"bs": "главни", "ca": "principal", "cs": "hlavní", "da": "hoved", "de": "Haupt", "el": "κύριο",
		"dv": "maigandu", "dz": "gtsowo", "es": "principal", "et": "peamine", "fa": "اصلی", "fi": "pää", "fo": "høvuð", "fr": "principal", "gn": "tenondegua",
		"he": "ראשי", "hi": "mukhya", "hr": "glavni", "ht": "prensipal", "hu": "fő", "hy": "գլխավոր",
		"id": "utama", "is": "aðal", "it": "principale", "ja": "主要", "ka": "მთავარი", "kl": "pingaarneq", "km": "chambang",
		"ko": "주요", "ky": "негизги", "lo": "lak", "lt": "pagrindinis", "lv": "galvenais", "mg": "fototra", "mk": "главен", "mn": "үндсэн", "my": "ahtika",
		"ms": "utama", "mt": "ewlieni", "nb": "hoved", "ne": "mukhya", "nl": "hoofd", "pap": "prinsipal",
		"pl": "główny", "pt": "principal", "rn": "nyamukuru", "ro": "principal", "ru": "главный", "rw": "nyamukuru",
		"si": "pradhana", "sk": "hlavný", "sl": "glavni", "sm": "autū", "sn": "chikuru", "so": "weyn", "sq": "kryesor", "sr": "главни",
		"st": "sehlooho", "sv": "huvud", "sw": "kuu", "tg": "асосӣ", "th": "lak", "ti": "ዋና", "to": "tefito", "tpi": "nambawan",
		"tk": "esasy", "tr": "ana", "uk": "головний", "ur": "بنیادی", "uz": "asosiy", "vi": "chính", "wo": "bumag",
		"zh": "主要",
	}
	if meaning := mainMeanings[base]; meaning != "" {
		if base == "sr" && strings.Contains(language, "Latn") {
			meaning = "glavni"
		}
		if seeds[base] == nil {
			seeds[base] = map[string]string{}
		}
		seeds[base]["main"] = meaning
	}
	core := map[string]map[string]string{
		"ja": {
			"main": "主要", "constant": "定数", "assembly": "アセンブリ",
			"common": "共通", "console": "コンソール", "driver": "ドライバー", "keyboard": "キーボード", "mouse": "マウス", "timer": "タイマー",
			"file": "ファイル", "system": "システム", "memory": "メモリ", "manager": "管理者", "multi": "複数", "tasking": "タスク管理", "task": "タスク",
			"paging": "ページ管理", "page": "ページ", "physical": "物理", "call": "呼出し", "process": "プロセス", "scheduler": "スケジューラ", "thread": "スレッド",
			"text": "テキスト", "mode": "モード", "virtual": "仮想", "interrupt": "割込み", "gate": "ゲート", "port": "ポート", "widget": "画面要素",
			"ethernet": "イーサネット", "frame": "フレーム", "util": "汎用", "list": "一覧", "array": "配列", "network": "ネットワーク", "socket": "ソケット",
			"header": "ヘッダ", "section": "区画", "link": "連結", "map": "対応表", "partition": "区分", "operation": "操作", "type": "型",
			"read": "読込み", "write": "書込み", "open": "開く", "close": "閉じる", "create": "作成", "delete": "削除", "load": "読込み", "user": "利用者", "kernel": "中核", "pending": "保留", "event": "事象", "events": "事象一覧",
			"resolve": "解決", "copy": "複製", "on": "時", "fault": "障害", "data": "データ", "byte": "バイト", "word": "語", "serial": "直列", "register": "レジスタ", "attribute": "属性", "controller": "制御器", "queue": "待ち行列", "only": "専用",
		},
		"fr": {
			"main": "principal", "constant": "constante", "assembly": "assembleur",
			"common": "commun", "console": "console", "driver": "pilote", "keyboard": "clavier", "mouse": "souris", "timer": "minuterie",
			"file": "fichier", "system": "système", "memory": "mémoire", "manager": "gestionnaire", "multi": "multiple", "tasking": "gestionTâches", "task": "tâche",
			"paging": "pagination", "page": "page", "physical": "physique", "call": "appel", "process": "processus", "scheduler": "ordonnanceur", "thread": "filExécution",
			"text": "texte", "mode": "mode", "virtual": "virtuel", "interrupt": "interruption", "gate": "porte", "port": "port", "widget": "composant",
			"ethernet": "ethernet", "frame": "trame", "util": "utilitaire", "list": "liste", "array": "tableau", "network": "réseau", "socket": "priseRéseau",
			"header": "enTête", "section": "section", "link": "lien", "map": "carte", "partition": "partition", "operation": "opération", "type": "type",
			"read": "lire", "write": "écrire", "open": "ouvrir", "close": "fermer", "create": "créer", "delete": "supprimer", "load": "charger", "user": "utilisateur", "kernel": "noyau", "pending": "attente", "event": "événement", "events": "événements",
			"resolve": "résoudre", "copy": "copier", "on": "sur", "fault": "défaut", "data": "données", "byte": "octet", "word": "mot", "serial": "série", "register": "registre", "attribute": "attribut", "controller": "contrôleur", "queue": "fileAttente", "only": "seulement",
		},
		"de": {
			"main": "Haupt", "constant": "Konstante", "assembly": "Assembler",
			"common": "gemeinsam", "console": "Konsole", "driver": "Treiber", "keyboard": "Tastatur", "mouse": "Maus", "timer": "Zeitgeber",
			"file": "Datei", "system": "System", "memory": "Speicher", "manager": "Verwalter", "multi": "mehrfach", "tasking": "Aufgabenverwaltung", "task": "Aufgabe",
			"paging": "Seitenverwaltung", "page": "Seite", "physical": "physisch", "call": "Aufruf", "process": "Prozess", "scheduler": "Planer", "thread": "Ausführungsfaden",
			"text": "Text", "mode": "Modus", "virtual": "virtuell", "interrupt": "Unterbrechung", "gate": "Tor", "port": "Anschluss", "widget": "Steuerelement",
			"ethernet": "Ethernet", "frame": "Rahmen", "util": "Hilfswerkzeug", "list": "Liste", "array": "Feld", "network": "Netzwerk", "socket": "Netzanschluss",
			"header": "Kopf", "section": "Abschnitt", "link": "Verknüpfung", "map": "Abbildung", "partition": "Partition", "operation": "Vorgang", "type": "Typ",
			"read": "Lesen", "write": "Schreiben", "open": "Öffnen", "close": "Schließen", "create": "Erstellen", "delete": "Löschen", "load": "Laden", "user": "Benutzer", "kernel": "Kern", "pending": "ausstehend", "event": "Ereignis", "events": "Ereignisse",
			"resolve": "Auflösen", "copy": "Kopieren", "on": "bei", "fault": "Fehler", "data": "Daten", "byte": "Byte", "word": "Wort", "serial": "seriell", "register": "Register", "attribute": "Attribut", "controller": "Steuerung", "queue": "Warteschlange", "only": "nur",
		},
		"es": {
			"main": "principal", "constant": "constante", "assembly": "ensamblador",
			"common": "común", "console": "consola", "driver": "controlador", "keyboard": "teclado", "mouse": "ratón", "timer": "temporizador",
			"file": "archivo", "system": "sistema", "memory": "memoria", "manager": "gestor", "multi": "múltiple", "tasking": "gestiónTareas", "task": "tarea",
			"paging": "paginación", "page": "página", "physical": "físico", "call": "llamada", "process": "proceso", "scheduler": "planificador", "thread": "hilo",
			"text": "texto", "mode": "modo", "virtual": "virtual", "interrupt": "interrupción", "gate": "puerta", "port": "puerto", "widget": "componente",
			"ethernet": "ethernet", "frame": "trama", "util": "utilidad", "list": "lista", "array": "matriz", "network": "red", "socket": "conectorRed",
			"header": "encabezado", "section": "sección", "link": "enlace", "map": "mapa", "partition": "partición", "operation": "operación", "type": "tipo",
			"read": "leer", "write": "escribir", "open": "abrir", "close": "cerrar", "create": "crear", "delete": "eliminar", "load": "cargar", "user": "usuario", "kernel": "núcleo", "pending": "pendiente", "event": "evento", "events": "eventos",
			"resolve": "resolver", "copy": "copiar", "on": "al", "fault": "fallo", "data": "datos", "byte": "octeto", "word": "palabra", "serial": "serie", "register": "registro", "attribute": "atributo", "controller": "controlador", "queue": "cola", "only": "solo",
		},
		"pt": {
			"main": "principal", "constant": "constante", "assembly": "montador",
			"common": "comum", "console": "console", "driver": "controlador", "keyboard": "teclado", "mouse": "rato", "timer": "temporizador",
			"file": "ficheiro", "system": "sistema", "memory": "memória", "manager": "gestor", "multi": "múltiplo", "tasking": "gestãoTarefas", "task": "tarefa",
			"paging": "paginação", "page": "página", "physical": "físico", "call": "chamada", "process": "processo", "scheduler": "escalonador", "thread": "fluxoExecução",
			"text": "texto", "mode": "modo", "virtual": "virtual", "interrupt": "interrupção", "gate": "porta", "port": "porto", "widget": "componente",
			"ethernet": "ethernet", "frame": "quadro", "util": "utilitário", "list": "lista", "array": "matriz", "network": "rede", "socket": "conectorRede",
			"header": "cabeçalho", "section": "secção", "link": "ligação", "map": "mapa", "partition": "partição", "operation": "operação", "type": "tipo",
			"read": "ler", "write": "escrever", "open": "abrir", "close": "fechar", "create": "criar", "delete": "eliminar", "load": "carregar", "user": "utilizador", "kernel": "núcleo", "pending": "pendente", "event": "evento", "events": "eventos",
			"resolve": "resolver", "copy": "copiar", "on": "ao", "fault": "falha", "data": "dados", "byte": "octeto", "word": "palavra", "serial": "série", "register": "registo", "attribute": "atributo", "controller": "controlador", "queue": "fila", "only": "somente",
		},
		"ar": {
			"main": "رئيسي", "constant": "ثابت", "assembly": "تجميع",
			"common": "مشترك", "console": "طرفية", "driver": "مشغل", "keyboard": "لوحةمفاتيح", "mouse": "فأرة", "timer": "مؤقت",
			"file": "ملف", "system": "نظام", "memory": "ذاكرة", "manager": "مدير", "multi": "متعدد", "tasking": "إدارةمهام", "task": "مهمة",
			"paging": "إدارةصفحات", "page": "صفحة", "physical": "مادي", "call": "نداء", "process": "عملية", "scheduler": "مجدول", "thread": "خيطتنفيذ",
			"text": "نص", "mode": "وضع", "virtual": "افتراضي", "interrupt": "مقاطعة", "gate": "بوابة", "port": "منفذ", "widget": "عنصرواجهة",
			"ethernet": "إيثرنت", "frame": "إطار", "util": "أداة", "list": "قائمة", "array": "مصفوفة", "network": "شبكة", "socket": "مقبس",
			"header": "ترويسة", "section": "قسم", "link": "رابط", "map": "خريطة", "partition": "تجزئة", "operation": "تشغيل", "type": "نوع",
			"read": "قراءة", "write": "كتابة", "open": "فتح", "close": "إغلاق", "create": "إنشاء", "delete": "حذف", "load": "تحميل", "user": "مستخدم", "kernel": "نواة", "pending": "معلق", "event": "حدث", "events": "أحداث",
			"resolve": "حل", "copy": "نسخ", "on": "عند", "fault": "خلل", "data": "بيانات", "byte": "بايت", "word": "كلمة", "serial": "تسلسلي", "register": "سجل", "attribute": "خاصية", "controller": "متحكم", "queue": "طابور", "only": "فقط",
		},
		"ru": {
			"main": "главный", "constant": "константа", "assembly": "ассемблер",
			"common": "общий", "console": "консоль", "driver": "драйвер", "keyboard": "клавиатура", "mouse": "мышь", "timer": "таймер",
			"file": "файл", "system": "система", "memory": "память", "manager": "диспетчер", "multi": "много", "tasking": "управлениеЗадачами", "task": "задача",
			"paging": "управлениеСтраницами", "page": "страница", "physical": "физический", "call": "вызов", "process": "процесс", "scheduler": "планировщик", "thread": "поток",
			"text": "текст", "mode": "режим", "virtual": "виртуальный", "interrupt": "прерывание", "gate": "шлюз", "port": "порт", "widget": "элемент",
			"ethernet": "эфирнаяСеть", "frame": "кадр", "util": "утилита", "list": "список", "array": "массив", "network": "сеть", "socket": "сокет",
			"header": "заголовок", "section": "раздел", "link": "ссылка", "map": "карта", "partition": "разделДиска", "operation": "операция", "type": "тип",
			"read": "читать", "write": "писать", "open": "открыть", "close": "закрыть", "create": "создать", "delete": "удалить", "load": "загрузить", "user": "пользователь", "kernel": "ядро", "pending": "ожидающий", "event": "событие", "events": "события",
			"resolve": "разрешить", "copy": "копировать", "on": "при", "fault": "ошибка", "data": "данные", "byte": "байт", "word": "слово", "serial": "последовательный", "register": "регистр", "attribute": "атрибут", "controller": "контроллер", "queue": "очередь", "only": "только",
		},
		"zh_Hans": {
			"main": "主要", "constant": "常量", "assembly": "汇编",
			"common": "通用", "console": "控制台", "driver": "驱动程序", "keyboard": "键盘", "mouse": "鼠标", "timer": "定时器", "file": "文件", "system": "系统", "memory": "内存",
			"manager": "管理器", "multi": "多重", "tasking": "任务管理", "task": "任务", "paging": "分页管理", "page": "页", "physical": "物理", "call": "调用", "process": "进程",
			"scheduler": "调度器", "thread": "线程", "text": "文本", "mode": "模式", "virtual": "虚拟", "interrupt": "中断", "gate": "入口", "port": "端口", "widget": "控件",
			"ethernet": "以太网", "frame": "帧", "util": "工具", "list": "列表", "array": "数组", "network": "网络", "socket": "套接字", "header": "头部", "section": "区段",
			"link": "链接", "map": "映射", "partition": "分区", "operation": "操作", "type": "类型", "read": "读取", "write": "写入", "open": "打开", "close": "关闭",
			"create": "创建", "delete": "删除", "load": "加载", "user": "用户", "kernel": "内核", "pending": "待处理", "event": "事件", "events": "事件集",
			"resolve": "解决", "copy": "复制", "on": "时", "fault": "故障", "data": "数据", "byte": "字节", "word": "字", "serial": "串行", "register": "寄存器", "attribute": "属性", "controller": "控制器", "queue": "队列", "only": "仅用",
		},
		"zh_Hant": {
			"main": "主要", "constant": "常數", "assembly": "組合語言",
			"common": "通用", "console": "控制台", "driver": "驅動程式", "keyboard": "鍵盤", "mouse": "滑鼠", "timer": "計時器", "file": "檔案", "system": "系統", "memory": "記憶體",
			"manager": "管理器", "multi": "多重", "tasking": "工作管理", "task": "工作", "paging": "分頁管理", "page": "頁", "physical": "物理", "call": "呼叫", "process": "程序",
			"scheduler": "排程器", "thread": "執行緒", "text": "文字", "mode": "模式", "virtual": "虛擬", "interrupt": "中斷", "gate": "入口", "port": "連接埠", "widget": "元件",
			"ethernet": "乙太網路", "frame": "框架", "util": "工具", "list": "清單", "array": "陣列", "network": "網路", "socket": "通訊端", "header": "標頭", "section": "區段",
			"link": "連結", "map": "對映", "partition": "分割區", "operation": "操作", "type": "類型", "read": "讀取", "write": "寫入", "open": "開啟", "close": "關閉",
			"create": "建立", "delete": "刪除", "load": "載入", "user": "使用者", "kernel": "核心", "pending": "待處理", "event": "事件", "events": "事件集",
			"resolve": "解決", "copy": "複製", "on": "時", "fault": "故障", "data": "資料", "byte": "位元組", "word": "字", "serial": "串列", "register": "暫存器", "attribute": "屬性", "controller": "控制器", "queue": "佇列", "only": "僅用",
		},
	}
	lookup := base
	if strings.HasPrefix(language, "zh_Hans") || strings.HasPrefix(language, "zh_Hant") {
		lookup = language
	}
	if additions := core[lookup]; additions != nil {
		if seeds[base] == nil {
			seeds[base] = map[string]string{}
		}
		for word, translated := range additions {
			seeds[base][word] = translated
		}
	}
	return seeds[base]
}

func main() {
	language := flag.String("language", "", "CLDR language code")
	vocabulary := flag.String("vocabulary", "/home/user/worldos/식별자-영어-어휘.tsv", "identifier vocabulary TSV")
	output := flag.String("output", "", "output glossary TSV")
	flag.Parse()
	if *language == "" || *output == "" {
		fmt.Fprintln(os.Stderr, "usage: build_semantic_glossary -language CODE -output FILE")
		os.Exit(2)
	}
	words, err := readVocabulary(*vocabulary)
	if err != nil {
		panic(err)
	}
	seeds := semanticSeeds(*language)
	wanted := map[string]bool{}
	for _, word := range words {
		wanted[word] = true
	}
	// These words can be introduced while expanding compound source paths
	// (filesystem -> file_system, for example). Query and record them even when
	// they did not appear as standalone identifiers in the original tree.
	semanticPathWords := []string{
		"assembly", "common", "console", "constant", "driver", "keyboard", "mouse", "timer",
		"file", "system", "memory", "manager", "multi", "tasking", "task", "paging", "page",
		"physical", "call", "process", "scheduler", "thread", "text", "mode", "virtual",
		"interrupt", "gate", "port", "widget", "ethernet", "frame", "util", "list", "array",
		"network", "socket", "header", "section", "link", "map", "partition", "operation", "type",
		"read", "write", "open", "close", "create", "delete", "load", "user", "kernel", "main",
		"master", "slave", "primary", "secondary", "programmable", "prefetch", "extended", "stack",
		"pointer", "global", "descriptor", "address", "device", "central", "processing", "unit",
		"peripheral", "component", "interconnect", "provider", "protocol", "raw", "source", "destination",
		"number", "connect", "send", "receive", "temporary", "checksum", "remote", "local", "media",
		"access", "control", "message", "gateway", "broadcast", "request", "echo", "reply", "route",
		"flag", "offset", "command", "when", "internet", "datagram", "backend", "available", "capable", "depth",
		"register", "reset", "video", "graphics", "bus", "hardware", "software", "word", "dword",
		"payload", "order", "io", "ip", "mac", "next", "hop",
	}
	for _, word := range semanticPathWords {
		if !wanted[word] {
			words = append(words, word)
			wanted[word] = true
		}
	}
	// Some source terms are uncommon as standalone UI labels. Search reviewed
	// catalogs through meaning-equivalent English labels instead of inventing a
	// target-script pronunciation. Alias keys are query-only and are never
	// emitted as source vocabulary.
	semanticAliases := map[string]string{
		"primary": "main", "principal": "main",
	}
	for alias := range semanticAliases {
		wanted[alias] = true
	}
	for word := range seeds {
		if !wanted[word] {
			words = append(words, word)
			wanted[word] = true
		}
	}
	sort.Strings(words)
	counts := map[string]map[string]int{}
	catalogCount := 0
	for _, directory := range localeDirectories(*language) {
		files, _ := filepath.Glob(filepath.Join(directory, "*.mo"))
		sort.Strings(files)
		for _, file := range files {
			data, commandErr := exec.Command("msgunfmt", file).Output()
			if commandErr != nil {
				continue
			}
			catalogCount++
			weight := catalogWeight(file)
			parsePO(data, func(id, translated string) {
				word := normalizedEnglish(id)
				if !wanted[word] {
					return
				}
				target := word
				if semanticAliases[word] != "" {
					target = semanticAliases[word]
				}
				value, valid := identifierWord(translated)
				if !valid || value == "" || strings.EqualFold(value, word) {
					return
				}
				if counts[target] == nil {
					counts[target] = map[string]int{}
				}
				counts[target][value] += weight
			})
		}
	}
	if err := os.MkdirAll(filepath.Dir(*output), 0755); err != nil {
		panic(err)
	}
	file, err := os.Create(*output)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	writer := bufio.NewWriter(file)
	defer writer.Flush()
	fmt.Fprintln(writer, "english\tlocalized\tsource\tevidence_count")
	translatedCount := 0
	englishLanguage := *language == "en" || strings.HasPrefix(*language, "en_")
	for _, word := range words {
		choice := candidate{value: word}
		for value, count := range counts[word] {
			if count > choice.count || count == choice.count && (choice.value == word || len([]rune(value)) < len([]rune(choice.value))) || count == choice.count && len([]rune(value)) == len([]rune(choice.value)) && value < choice.value {
				choice = candidate{value: value, count: count}
			}
		}
		source := "fallback-English"
		if seed := seeds[word]; seed != "" {
			choice.value = seed
			source = "curated-seed"
			translatedCount++
		} else if englishLanguage {
			source = "native-English"
			translatedCount++
		} else if choice.count != 0 {
			source = "gettext"
			translatedCount++
		}
		fmt.Fprintf(writer, "%s\t%s\t%s\t%d\n", word, choice.value, source, choice.count)
	}
	fmt.Fprintf(os.Stderr, "%s: catalogs=%d translated=%d/%d\n", *language, catalogCount, translatedCount, len(words))
}
