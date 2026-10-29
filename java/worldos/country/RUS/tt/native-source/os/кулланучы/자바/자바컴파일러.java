// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java чыганак_агач -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] чыганак = new int[16384], 출력 = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], токен_урнаштыру = new int[2048], токен_озынлык = new int[2048];
    static int[] константа_VALUE = new int[4096], константа_OFFSET = new int[512];
    static int[] 문자 = new int[512], файл_исем_СМС = new int[64];
    static int[] 삽입코드 = new int[16];
    static int чыганак_үлчәмен_үзгәртү, токен_COUNT, урнаштыру, CODE_үлчәмен_үзгәртү, константа_үлчәмен_үзгәртү, константа_COUNT = 1, 출력크기, символ_озынлык;
    static boolean Хата;
    static int класс_токен, класс_константа, 부모상수, CODE_константа;
    static int[] ысул_кертү_исем = new int[32], ысул_кайтару = new int[32], ысул_аргумент_COUNT = new int[32];
    static int[] ысул_аргумент_исем = new int[512], ысул_аргумент_TYPE = new int[512];
    static int[] 함수본문 = new int[32], ысул_тәмамлау = new int[32], ысул_CODE = new int[32];
    static int[] ысул_озынлык = new int[32], 함수지역 = new int[32], ысул_исем_константа = new int[32], 함수서술 = new int[32];
    static int[] ысул_керү = new int[32];
    static int ысул_COUNT, 현재함수, локаль_COUNT, 깊이, 식깊이;
    static int[] локаль_исем = new int[128], локаль_TYPE = new int[128], 지역깊이 = new int[128];

    static void эштән_туктау_VALUE(String 이유) {
        if (!Хата) {
            кулланучы.язу("javac error: "); кулланучы.язу(이유);
            кулланучы.язу(" at line ");
            int юл = 1, 끝 = урнаштыру < токен_COUNT ? токен_урнаштыру[урнаштыру] : чыганак_үлчәмен_үзгәртү;
            for (int 수 = 0; 수 < 끝; 수++) if (чыганак[수] == 10) юл++;
            자바도구.수쓰기(юл); кулланучы.язу_символ_VALUE(10);
        }
        Хата = true;
    }
    static boolean символ_VALUE_068c2631(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean сан_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= токен_COUNT || 나 >= токен_COUNT || токен_озынлык[가] != токен_озынлык[나]) return false;
        for (int 수 = 0; 수 < токен_озынлык[가]; 수++) if (чыганак[токен_урнаштыру[가] + 수] != чыганак[токен_урнаштыру[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int токен_VALUE, String Word_СМС) {
        if (токен_VALUE < 0 || токен_VALUE >= токен_COUNT || токен_озынлык[токен_VALUE] != Word_СМС.length()) return false;
        for (int 수 = 0; 수 < Word_СМС.length(); 수++) if (чыганак[токен_урнаштыру[токен_VALUE] + 수] != Word_СМС.charAt(수)) return false;
        return true;
    }
    static int 종류() { return урнаштыру < токен_COUNT ? 토큰종류[урнаштыру] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; урнаштыру++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) эштән_туктау_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_СМС) { if (!Word_VALUE(урнаштыру, Word_СМС)) return false; урнаштыру++; return true; }
    static void 말요구(String Word_СМС) { if (!TAKE_Word(Word_СМС)) эштән_туктау_VALUE(Word_СМС); }
    static int күрсәткеч_VALUE() {
        int үлчәм = урнаштыру;
        if (종류() != 256) эштән_туктау_VALUE("identifier required"); else урнаштыру++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int эшләтү = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - эшләтү == токен_озынлык[үлчәм];
                for (int оя_кертү = эшләтү; 같음 && оя_кертү < 수; оя_кертү++) if (예약어.charAt(оя_кертү) != чыганак[токен_урнаштыру[үлчәм] + оя_кертү - эшләтү]) 같음 = false;
                if (같음) эштән_туктау_VALUE("reserved word cannot be an identifier");
                эшләтү = 수 + 1;
            }
        }
        return үлчәм;
    }
    static void кисү_VALUE() {
        int 수 = 0;
        while (수 < чыганак_үлчәмен_үзгәртү && !Хата) {
            int VALUE = чыганак[수], эшләтү = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < чыганак_үлчәмен_үзгәртү && чыганак[수 + 1] == '/') {
                while (수 < чыганак_үлчәмен_үзгәртү && чыганак[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < чыганак_үлчәмен_үзгәртү && чыганак[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < чыганак_үлчәмен_үзгәртү && !(чыганак[수] == '*' && чыганак[수 + 1] == '/')) 수++;
                if (수 + 1 >= чыганак_үлчәмен_үзгәртү) { эштән_туктау_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (символ_VALUE_068c2631(VALUE)) { 종류 = 256; while (수 < чыганак_үлчәмен_үзгәртү && 문자이름규칙.이어진글자(чыганак[수])) 수++; }
            else if (сан_VALUE(VALUE)) { 종류 = 257; while (수 < чыганак_үлчәмен_үзгәртү && сан_VALUE(чыганак[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < чыганак_үлчәмен_үзгәртү && чыганак[수] != VALUE && чыганак[수] != 10 && чыганак[수] != 13) {
                    if (чыганак[수] == '\\') 수++;
                    수++;
                }
                if (수 >= чыганак_үлчәмен_үзгәртү || чыганак[수] != VALUE) { эштән_туктау_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < чыганак_үлчәмен_үзгәртү) {
                    int Киләсе_элемент = чыганак[수];
                    if (VALUE == '=' && Киләсе_элемент == '=') 종류 = 300;
                    if (VALUE == '!' && Киләсе_элемент == '=') 종류 = 301;
                    if (VALUE == '<' && Киләсе_элемент == '=') 종류 = 302;
                    if (VALUE == '>' && Киләсе_элемент == '=') 종류 = 303;
                    if (VALUE == '&' && Киләсе_элемент == '&') 종류 = 304;
                    if (VALUE == '|' && Киләсе_элемент == '|') 종류 = 305;
                    if (VALUE == '+' && Киләсе_элемент == '+') 종류 = 306;
                    if (VALUE == '-' && Киләсе_элемент == '-') 종류 = 307;
                    if (VALUE == '+' && Киләсе_элемент == '=') 종류 = 308;
                    if (VALUE == '-' && Киләсе_элемент == '=') 종류 = 309;
                    if (VALUE == '*' && Киләсе_элемент == '=') 종류 = 310;
                    if (VALUE == '/' && Киләсе_элемент == '=') 종류 = 311;
                    if (VALUE == '%' && Киләсе_элемент == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (токен_COUNT == 토큰종류.length - 1) { эштән_туктау_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[токен_COUNT] = 종류; токен_урнаштыру[токен_COUNT] = эшләтү; токен_озынлык[токен_COUNT++] = 수 - эшләтү;
        }
    }
    static void язу_константа_байт(int VALUE) {
        if (константа_үлчәмен_үзгәртү == константа_VALUE.length) { эштән_туктау_VALUE("constant pool too large"); return; }
        константа_VALUE[константа_үлчәмен_үзгәртү++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { язу_константа_байт(VALUE >> 8); язу_константа_байт(VALUE); }
    static int теркәлү_константа(int эшләтү) {
        for (int 수 = 1; 수 < константа_COUNT; 수++) {
            int 앞 = константа_OFFSET[수], озынлык_VALUE = (수 + 1 < константа_COUNT ? константа_OFFSET[수 + 1] : эшләтү) - 앞;
            if (озынлык_VALUE != константа_үлчәмен_үзгәртү - эшләтү) continue;
            boolean 같음 = true;
            for (int оя_кертү = 0; оя_кертү < озынлык_VALUE; оя_кертү++) if (константа_VALUE[앞 + оя_кертү] != константа_VALUE[эшләтү + оя_кертү]) 같음 = false;
            if (같음) { константа_үлчәмен_үзгәртү = эшләтү; return 수; }
        }
        if (константа_COUNT == константа_OFFSET.length) { эштән_туктау_VALUE("too many constants"); return 0; }
        константа_OFFSET[константа_COUNT] = эшләтү;
        return константа_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (символ_озынлык == 문자.length) { эштән_туктау_VALUE("text too long"); return; }
        문자[символ_озынлык++] = VALUE;
    }
    static void 말추가(String Word_СМС) { for (int 수 = 0; 수 < Word_СМС.length(); 수++) 글추가(Word_СМС.charAt(수)); }
    static int символ_константа() {
        int эшләтү = константа_үлчәмен_үзгәртү; язу_константа_байт(1); 상짧(0);
        for (int 수 = 0; 수 < символ_озынлык; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) язу_константа_байт(VALUE);
            else if (VALUE < 2048) { язу_константа_байт(192 | VALUE >> 6); язу_константа_байт(128 | VALUE & 63); }
            else { язу_константа_байт(224 | VALUE >> 12); язу_константа_байт(128 | VALUE >> 6 & 63); язу_константа_байт(128 | VALUE & 63); }
        }
        if (Хата) return 0;
        int озынлык_VALUE = константа_үлчәмен_үзгәртү - эшләтү - 3;
        константа_VALUE[эшләтү + 1] = озынлык_VALUE >> 8; константа_VALUE[эшләтү + 2] = озынлык_VALUE & 255;
        return теркәлү_константа(эшләтү);
    }
    static int Word_константа(String Word_СМС) { символ_озынлык = 0; 말추가(Word_СМС); return символ_константа(); }
    static int токен_константа(int токен_VALUE) {
        символ_озынлык = 0;
        for (int 수 = 0; 수 < токен_озынлык[токен_VALUE]; 수++) 글추가(чыганак[токен_урнаштыру[токен_VALUE] + 수]);
        return символ_константа();
    }
    static int Белешмәлекләр(int 종류, int 가, int 나) {
        int эшләтү = константа_үлчәмен_үзгәртү; язу_константа_байт(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return теркәлү_константа(эшләтү);
    }
    static int 외부참조(int 종류, String биләүче_VALUE, String исем, String 서술) {
        int биләүче_күрсәткеч = Белешмәлекләр(7, Word_константа(биләүче_VALUE), 0);
        int исем_COUNT = Word_константа(исем), формат_COUNT = Word_константа(서술);
        return Белешмәлекләр(종류, биләүче_күрсәткеч, Белешмәлекләр(12, исем_COUNT, формат_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_үлчәмен_үзгәртү == CODE_VALUE.length) { эштән_туктау_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_үлчәмен_үзгәртү++] = VALUE & 255;
    }
    static void команда(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int эшләтү = константа_үлчәмен_үзгәртү; язу_константа_байт(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        команда(19, теркәлү_константа(эшләтү));
    }
    static int тармак(int команда) { int үлчәм = CODE_үлчәмен_үзгәртү; команда(команда, 0); return үлчәм; }
    static void бәйләү_VALUE(int тармак, int максат_кыйммәт_объект) {
        if (Хата) return;
        int 거리 = максат_кыйммәт_объект - тармак;
        if (거리 < -32768 || 거리 > 32767 || тармак < 0 || тармак + 2 >= CODE_үлчәмен_үзгәртү) { эштән_туктау_VALUE("invalid branch"); return; }
        CODE_VALUE[тармак + 1] = 거리 >> 8 & 255; CODE_VALUE[тармак + 2] = 거리 & 255;
    }
    static void 비교값(int команда) {
        int TRUE_VALUE = тармак(команда); 내보내기(3); int 끝 = тармак(167);
        бәйләү_VALUE(TRUE_VALUE, CODE_үлчәмен_үзгәртү); 내보내기(4); бәйләү_VALUE(끝, CODE_үлчәмен_үзгәртү);
    }
    static int формат_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        эштән_туктау_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void өстәү_формат(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Процесс_VALUE_кертү 본문은 хост javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Татарча");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("예외") || TAKE_Word("실행예외") || TAKE_Word("입출력예외") || TAKE_Word("대기시간초과예외") || TAKE_Word("주소확인예외") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("잘못된인수예외") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("빈참조예외") || TAKE_Word("산술예외") || TAKE_Word("상태예외") || TAKE_Word("형변환예외") || TAKE_Word("음수배열크기예외") || TAKE_Word("МАССИВ_Store_эштән_туктау") || TAKE_Word("가닥상태예외") || TAKE_Word("대기중단예외")) return;
        эштән_туктау_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(урнаштыру, "Татарча")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) эштән_туктау_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); класс_токен = күрсәткеч_VALUE();
        класс_константа = Белешмәлекләр(7, токен_константа(класс_токен), 0);
        부모상수 = Белешмәлекләр(7, Word_константа("java/lang/Object"), 0); CODE_константа = Word_константа("Code"); 요구('{');
        while (!Хата && 종류() != '}') {
            if (ысул_COUNT == 32) { эштән_туктау_VALUE("too many methods"); break; }
            int керү_кертү = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int ФУНКЦИЯ_VALUE = ысул_COUNT++;
            ысул_керү[ФУНКЦИЯ_VALUE] = керү_кертү | 8;
            ысул_кайтару[ФУНКЦИЯ_VALUE] = формат_VALUE(); ысул_кертү_исем[ФУНКЦИЯ_VALUE] = күрсәткеч_VALUE(); 요구('(');
            for (int 앞 = 0; 앞 < ФУНКЦИЯ_VALUE; 앞++) if (이름같음(ысул_кертү_исем[앞], ысул_кертү_исем[ФУНКЦИЯ_VALUE])) эштән_туктау_VALUE("duplicate method (overloading unsupported)");
            while (!Хата && 종류() != ')') {
                int 수 = ысул_аргумент_COUNT[ФУНКЦИЯ_VALUE];
                if (수 == 16) { эштән_туктау_VALUE("too many parameters"); break; }
                int TYPE_VALUE = формат_VALUE(); if (TYPE_VALUE == 0) эштән_туктау_VALUE("void parameter");
                ысул_аргумент_TYPE[ФУНКЦИЯ_VALUE * 16 + 수] = TYPE_VALUE; ысул_аргумент_исем[ФУНКЦИЯ_VALUE * 16 + 수] = күрсәткеч_VALUE();
                ысул_аргумент_COUNT[ФУНКЦИЯ_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!Хата && 받기(','));
            }
            함수본문[ФУНКЦИЯ_VALUE] = урнаштыру; 요구('{');
            int 중첩 = 1;
            while (урнаштыру < токен_COUNT && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                урнаштыру++;
            }
            if (중첩 != 0) эштән_туктау_VALUE("unclosed method body");
            ысул_тәмамлау[ФУНКЦИЯ_VALUE] = урнаштыру;
            ысул_исем_константа[ФУНКЦИЯ_VALUE] = токен_константа(ысул_кертү_исем[ФУНКЦИЯ_VALUE]);
            символ_озынлык = 0; 글추가('(');
            for (int 수 = 0; 수 < ысул_аргумент_COUNT[ФУНКЦИЯ_VALUE]; 수++) өстәү_формат(ысул_аргумент_TYPE[ФУНКЦИЯ_VALUE * 16 + 수]);
            글추가(')'); өстәү_формат(ысул_кайтару[ФУНКЦИЯ_VALUE]); 함수서술[ФУНКЦИЯ_VALUE] = символ_константа();
        }
        요구('}'); if (урнаштыру != токен_COUNT) эштән_туктау_VALUE("extra input after class");
    }
    static int FIND_локаль(int исем) {
        for (int 수 = локаль_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(локаль_исем[수], исем)) return 수;
        эштән_туктау_VALUE("unknown variable"); return 0;
    }
    static int өстәү_локаль(int исем, int TYPE_VALUE) {
        for (int 수 = 0; 수 < локаль_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(локаль_исем[수], исем)) эштән_туктау_VALUE("duplicate local variable");
        if (локаль_COUNT == 128) { эштән_туктау_VALUE("too many locals"); return 0; }
        локаль_исем[локаль_COUNT] = исем; локаль_TYPE[локаль_COUNT] = TYPE_VALUE; 지역깊이[локаль_COUNT] = 깊이;
        return локаль_COUNT++;
    }
    static boolean бөтен_сан_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(локаль_TYPE[수] <= 2 || локаль_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void язу_локаль(int 수) { 내보내기(локаль_TYPE[수] <= 2 || локаль_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void раслау_TYPE(int фактик_мәгълүмат, int 기대) { if (фактик_мәгълүмат != 기대 && !(фактик_мәгълүмат == 5 && 기대 == 1)) эштән_туктау_VALUE("type mismatch"); }
    static void 문자읽기(int токен_VALUE) {
        символ_озынлык = 0; int эшләтү = токен_урнаштыру[токен_VALUE] + 1, 끝 = токен_урнаштыру[токен_VALUE] + токен_озынлык[токен_VALUE] - 1;
        while (эшләтү < 끝 && !Хата) {
            int VALUE = чыганак[эшләтү++];
            if (VALUE == '\\') {
                if (эшләтү == 끝) { эштән_туктау_VALUE("invalid escape"); break; }
                VALUE = чыганак[эшләтү++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') эштән_туктау_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int бүлү_бөтен_сан(int токен_VALUE, boolean 음수) {
        if (токен_озынлык[токен_VALUE] > 1 && чыганак[токен_урнаштыру[токен_VALUE]] == '0') эштән_туктау_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < токен_озынлык[токен_VALUE]; 수++) {
            int сан_элемент = чыганак[токен_урнаштыру[токен_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && сан_элемент > (음수 ? 8 : 7)) эштән_туктау_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - сан_элемент;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = формат_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { эштән_туктау_VALUE("only file streams supported by new in source"); return 0; }
            String биләүче_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            команда(187, Белешмәлекләр(7, Word_константа(биләүче_VALUE), 0)); 내보내기(89);
            요구('('); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) эштән_туктау_VALUE("input stream constructor arguments"); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 2); 이어 = true; }
            요구(')');
            команда(183, 외부참조(10, биләүче_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = аңлатма_VALUE_eb3593ac(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(бүлү_бөтен_сан(урнаштыру++, false)); return 1; }
        if (종류() == 258) { 문자읽기(урнаштыру++); команда(19, Белешмәлекләр(8, символ_константа(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(урнаштыру++); if (символ_озынлык != 1) эштән_туктау_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Татарча")) {
            요구('.'); 말요구("자체"); 요구('.');
            String биләүче_VALUE = "", ысул_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, үлчәм = 0;
            if (TAKE_Word("출력")) {
                биләүче_VALUE = "Татарча/자체/출력"; 요구('.');
                if (TAKE_Word("язу_юл")) { ысул_VALUE = "язу_юл"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("язу")) { ысул_VALUE = "язу"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { ысул_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else эштән_туктау_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                биләүче_VALUE = "Татарча/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("озынлык_VALUE")) { ысул_VALUE = "озынлык_VALUE"; 서술 = "(Ljava/lang/String;)I"; үлчәм = 1; }
                else if (TAKE_Word("символ_коды_COUNT")) { ысул_VALUE = "символ_коды_COUNT"; 서술 = "(Ljava/lang/String;)I"; үлчәм = 1; }
                else if (TAKE_Word("бүлү_бөтен_сан")) { ысул_VALUE = "бүлү_бөтен_сан"; 서술 = "(Ljava/lang/String;)I"; үлчәм = 1; }
                else if (TAKE_Word("язу_бөтен_сан_VALUE")) { ысул_VALUE = "язу_бөтен_сан_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; үлчәм = 3; }
                else if (TAKE_Word("같음")) { ысул_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; үлчәм = 2; }
                else if (TAKE_Word("өстәү_СМС")) { ысул_VALUE = "өстәү_СМС"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; үлчәм = 3; }
                else if (TAKE_Word("кисү_VALUE")) { ысул_VALUE = "кисү_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; үлчәм = 3; }
                else эштән_туктау_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Birem")) {
                биләүче_VALUE = "Татарча/자체/Birem"; 요구('.'); 가 = 3;
                if (TAKE_Word("읽기")) { ысул_VALUE = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; үлчәм = 3; }
                else if (TAKE_Word("язу")) { ысул_VALUE = "язу"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else эштән_туктау_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                биләүче_VALUE = "Татарча/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { ысул_VALUE = "너비"; 서술 = "()I"; үлчәм = 1; }
                else if (TAKE_Word("높이")) { ысул_VALUE = "높이"; 서술 = "()I"; үлчәм = 1; }
                else if (TAKE_Word("사각형")) { ысул_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("지우기")) { ысул_VALUE = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { ысул_VALUE = "기다리기"; 서술 = "()V"; }
                else эштән_туктау_VALUE("unknown Korean framebuffer method");
            } else эштән_туктау_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) раслау_TYPE(аңлатма_VALUE_eb3593ac(), 가);
            if (나 != 0) { 요구(','); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 나); }
            if (다 != 0) { 요구(','); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 다); }
            if (라 != 0) { 요구(','); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 라); }
            if (마 != 0) { 요구(','); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 마); }
            요구(')'); команда(184, 외부참조(10, биләүче_VALUE, ысул_VALUE, 서술)); return үлчәм;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 3); 요구(')');
            команда(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int исем = күрсәткеч_VALUE();
        if (받기('(')) {
            int ФУНКЦИЯ_VALUE = -1;
            for (int 수 = 0; 수 < ысул_COUNT; 수++) if (이름같음(исем, ысул_кертү_исем[수])) ФУНКЦИЯ_VALUE = 수;
            if (ФУНКЦИЯ_VALUE < 0) { эштән_туктау_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!Хата && 종류() != ')') {
                if (수 >= ысул_аргумент_COUNT[ФУНКЦИЯ_VALUE]) { эштән_туктау_VALUE("too many arguments"); break; }
                раслау_TYPE(аңлатма_VALUE_eb3593ac(), ысул_аргумент_TYPE[ФУНКЦИЯ_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != ысул_аргумент_COUNT[ФУНКЦИЯ_VALUE]) эштән_туктау_VALUE("argument count mismatch");
            команда(184, Белешмәлекләр(10, класс_константа, Белешмәлекләр(12, ысул_исем_константа[ФУНКЦИЯ_VALUE], 함수서술[ФУНКЦИЯ_VALUE])));
            return ысул_кайтару[ФУНКЦИЯ_VALUE];
        }
        int локаль_даирә = FIND_локаль(исем), TYPE_VALUE = локаль_TYPE[локаль_даирә]; 지역읽기(локаль_даирә);
        while (!Хата) {
            if (받기('[')) { раслау_TYPE(TYPE_VALUE, 4); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String биләүче_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); команда(182, 외부참조(10, биләүче_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); команда(182, 외부참조(10, биләүче_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 1); 요구(')'); команда(182, 외부참조(10, биләүче_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { эштән_туктау_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { раслау_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); команда(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { эштән_туктау_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { раслау_TYPE(단항(), 2); 비교값(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(бүлү_бөтен_сан(урнаштыру++, true));
            else { раслау_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { раслау_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!Хата && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int кодлау_VALUE = 종류(); урнаштыру++; раслау_TYPE(TYPE_VALUE, 1); раслау_TYPE(단항(), 1);
            내보내기(кодлау_VALUE == '*' ? 104 : кодлау_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!Хата && (종류() == '+' || 종류() == '-')) {
            int кодлау_VALUE = 종류(); урнаштыру++; int 경계 = CODE_үлчәмен_үзгәртү, Артка_VALUE_TYPE = 곱식();
            if (кодлау_VALUE == '+' && (TYPE_VALUE == 3 || Артка_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, Артка_VALUE_TYPE); TYPE_VALUE = 3; }
            else { раслау_TYPE(TYPE_VALUE, 1); раслау_TYPE(Артка_VALUE_TYPE, 1); 내보내기(кодлау_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) эштән_туктау_VALUE("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Артка_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 булдыру 코드를 삽입한다.
        // RIGHT аңлатма_VALUE_eb3593ac 내부의 тиңдәш_VALUE тармак 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_үлчәмен_үзгәртү;
        команда(187, Белешмәлекләр(7, Word_константа("java/lang/StringBuilder"), 0)); 내보내기(89);
        команда(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); команда(182, 붙임참조(앞형));
        if (Хата) return;
        int озынлык_VALUE = CODE_үлчәмен_үзгәртү - 끝;
        for (int 수 = 0; 수 < озынлык_VALUE; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + озынлык_VALUE] = CODE_VALUE[수];
        for (int 수 = 0; 수 < озынлык_VALUE; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        команда(182, 붙임참조(Артка_VALUE_TYPE)); команда(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int TYPE_VALUE = 합식();
        while (!Хата && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int кодлау_VALUE = 종류(); урнаштыру++; раслау_TYPE(TYPE_VALUE, 1); раслау_TYPE(합식(), 1);
            비교값(кодлау_VALUE == '<' ? 161 : кодлау_VALUE == '>' ? 163 : кодлау_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = 비교식();
        while (!Хата && (종류() == 300 || 종류() == 301)) {
            int кодлау_VALUE = 종류(); урнаштыру++; int Артка_VALUE_TYPE = 비교식();
            if (TYPE_VALUE == 0 || Артка_VALUE_TYPE == 0) эштән_туктау_VALUE("void expression");
            if (!(бөтен_сан_TYPE(TYPE_VALUE) && бөтен_сан_TYPE(Артка_VALUE_TYPE))) раслау_TYPE(Артка_VALUE_TYPE, TYPE_VALUE);
            비교값((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (кодлау_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!Хата && 받기(304)) {
            раслау_TYPE(TYPE_VALUE, 2); int 가 = тармак(153); раслау_TYPE(동등식(), 2); int 나 = тармак(153);
            내보내기(4); int 끝 = тармак(167); бәйләү_VALUE(가, CODE_үлчәмен_үзгәртү); бәйләү_VALUE(나, CODE_үлчәмен_үзгәртү); 내보내기(3); бәйләү_VALUE(끝, CODE_үлчәмен_үзгәртү); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int аңлатма_VALUE_eb3593ac() {
        int TYPE_VALUE = 논리곱();
        while (!Хата && 받기(305)) {
            раслау_TYPE(TYPE_VALUE, 2); int 가 = тармак(154); раслау_TYPE(논리곱(), 2); int 나 = тармак(154);
            내보내기(3); int 끝 = тармак(167); бәйләү_VALUE(가, CODE_үлчәмен_үзгәртү); бәйләү_VALUE(나, CODE_үлчәмен_үзгәртү); 내보내기(4); бәйләү_VALUE(끝, CODE_үлчәмен_үзгәртү); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void бирем_VALUE(boolean 선언허용) {
        if (Word_VALUE(урнаштыру, "int") || Word_VALUE(урнаштыру, "boolean") || Word_VALUE(урнаштыру, "String") || Word_VALUE(урнаштыру, "char")
            || Word_VALUE(урнаштыру, "FileInputStream") || Word_VALUE(урнаштыру, "FileOutputStream")) {
            if (!선언허용) эштән_туктау_VALUE("declaration not allowed here");
            int TYPE_VALUE = формат_VALUE(), исем = күрсәткеч_VALUE(); 요구('='); раслау_TYPE(аңлатма_VALUE_eb3593ac(), TYPE_VALUE);
            язу_локаль(өстәү_локаль(исем, TYPE_VALUE)); return;
        }
        int исем = күрсәткеч_VALUE(), локаль_даирә = FIND_локаль(исем);
        if (받기('=')) { раслау_TYPE(аңлатма_VALUE_eb3593ac(), локаль_TYPE[локаль_даирә]); язу_локаль(локаль_даирә); }
        else if (종류() >= 308 && 종류() <= 312) {
            int кодлау_VALUE = 종류(); урнаштыру++; 지역읽기(локаль_даирә); int 경계 = CODE_үлчәмен_үзгәртү, Артка_VALUE_TYPE = аңлатма_VALUE_eb3593ac();
            if (кодлау_VALUE == 308 && локаль_TYPE[локаль_даирә] == 3) 결합(경계, 3, Артка_VALUE_TYPE);
            else {
                раслау_TYPE(локаль_TYPE[локаль_даирә], 1); раслау_TYPE(Артка_VALUE_TYPE, 1);
                내보내기(кодлау_VALUE == 308 ? 96 : кодлау_VALUE == 309 ? 100 : кодлау_VALUE == 310 ? 104 : кодлау_VALUE == 311 ? 108 : 112);
                if (локаль_TYPE[локаль_даирә] == 5) 내보내기(146);
            }
            язу_локаль(локаль_даирә);
        }
        else if (종류() == 306 || 종류() == 307) {
            раслау_TYPE(локаль_TYPE[локаль_даирә], 1); 내보내기(132); 내보내기(локаль_даирә); 내보내기(종류() == 306 ? 1 : 255); урнаштыру++;
            if (локаль_TYPE[локаль_даирә] == 5) { 지역읽기(локаль_даирә); 내보내기(146); язу_локаль(локаль_даирә); }
        } else эштән_туктау_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        команда(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean Буш_аргумент = 종류() == ')';
        int TYPE_VALUE = Буш_аргумент ? 0 : аңлатма_VALUE_eb3593ac(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !Буш_аргумент)) эштән_туктау_VALUE("unsupported print argument");
        команда(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean аңлатма_VALUE() {
        if (Хата) return false;
        if (깊이 > 32) { эштән_туктау_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean кайтару_үлчәм = false;
            while (!Хата && 종류() != '}') { if (кайтару_үлчәм) эштән_туктау_VALUE("unreachable statement"); кайтару_үлчәм = аңлатма_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < локаль_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return кайтару_үлчәм;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : аңлатма_VALUE_eb3593ac(); раслау_TYPE(TYPE_VALUE, ысул_кайтару[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 2); 요구(')'); int FALSE_VALUE = тармак(153);
            깊이++; boolean 가 = идарә_аңлатма(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = тармак(167); бәйләү_VALUE(FALSE_VALUE, CODE_үлчәмен_үзгәртү); 깊이++; boolean 나 = идарә_аңлатма(); 깊이--; бәйләү_VALUE(끝, CODE_үлчәмен_үзгәртү); return 가 && 나; }
            бәйләү_VALUE(FALSE_VALUE, CODE_үлчәмен_үзгәртү); return false;
        }
        if (TAKE_Word("while")) {
            int эшләтү = CODE_үлчәмен_үзгәртү; 요구('('); раслау_TYPE(аңлатма_VALUE_eb3593ac(), 2); 요구(')'); int 끝 = тармак(153);
            깊이++; идарә_аңлатма(); 깊이--; бәйләү_VALUE(тармак(167), эшләтү); бәйләү_VALUE(끝, CODE_үлчәмен_үзгәртү); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') бирем_VALUE(true); 요구(';');
            int шарт = CODE_үлчәмен_үзгәртү; if (종류() == ';') 내보내기(4); else раслау_TYPE(аңлатма_VALUE_eb3593ac(), 2); 요구(';');
            int 끝 = тармак(153), төп_текст = тармак(167), яңарту = CODE_үлчәмен_үзгәртү;
            if (종류() != ')') бирем_VALUE(false); 요구(')'); бәйләү_VALUE(тармак(167), шарт); бәйләү_VALUE(төп_текст, CODE_үлчәмен_үзгәртү);
            идарә_аңлатма(); бәйләү_VALUE(тармак(167), яңарту); бәйләү_VALUE(끝, CODE_үлчәмен_үзгәртү);
            for (int 수 = 0; 수 < локаль_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(урнаштыру, "System")) { 화면출력(); return false; }
        if (종류() == 256 && урнаштыру + 1 < токен_COUNT && (토큰종류[урнаштыру + 1] == '(' || 토큰종류[урнаштыру + 1] == '.')) {
            int TYPE_VALUE = аңлатма_VALUE_eb3593ac(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        бирем_VALUE(true); 요구(';'); return false;
    }
    static boolean идарә_аңлатма() {
        if (Word_VALUE(урнаштыру, "int") || Word_VALUE(урнаштыру, "boolean") || Word_VALUE(урнаштыру, "char") || Word_VALUE(урнаштыру, "String")
            || Word_VALUE(урнаштыру, "FileInputStream") || Word_VALUE(урнаштыру, "FileOutputStream")) эштән_туктау_VALUE("local declaration requires braces");
        return аңлатма_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) эштән_туктау_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void язу_класс() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(константа_COUNT);
        for (int 수 = 0; 수 < константа_үлчәмен_үзгәртү; 수++) 출바(константа_VALUE[수]);
        출짧(0x21); 출짧(класс_константа); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(ысул_COUNT);
        for (int 수 = 0; 수 < ысул_COUNT; 수++) {
            출짧(ысул_керү[수]); 출짧(ысул_исем_константа[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_константа);
            출정(12 + ысул_озынлык[수]); 출짧(128); 출짧(함수지역[수]); 출정(ысул_озынлык[수]);
            for (int оя_кертү = 0; оя_кертү < ысул_озынлык[수]; оя_кертү++) 출바(CODE_VALUE[ысул_CODE[수] + оя_кертү]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int эшләтү() {
        if (кулланучы.인수개수() == 1 && 자바도구.같음(кулланучы.인수(0), "-version")) {
            кулланучы.язу("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (кулланучы.인수개수() != 1) { кулланучы.язу("Usage: javac FILE.java\n"); return 2; }
        int исем_үлчәмен_үзгәртү = 자바도구.исем(файл_исем_СМС, кулланучы.인수(0));
        if (исем_үлчәмен_үзгәртү < 6 || исем_үлчәмен_үзгәртү > 62 || файл_исем_СМС[исем_үлчәмен_үзгәртү - 5] != '.' || файл_исем_СМС[исем_үлчәмен_үзгәртү - 4] != 'j'
            || файл_исем_СМС[исем_үлчәмен_үзгәртү - 3] != 'a' || файл_исем_СМС[исем_үлчәмен_үзгәртү - 2] != 'v' || файл_исем_СМС[исем_үлчәмен_үзгәртү - 1] != 'a') {
            кулланучы.язу("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        чыганак_үлчәмен_үзгәртү = кулланучы.파일읽기(файл_исем_СМС, чыганак);
        if (чыганак_үлчәмен_үзгәртү < 0) { кулланучы.язу("javac: cannot read source: "); 자바도구.수쓰기(чыганак_үлчәмен_үзгәртү); кулланучы.язу_символ_VALUE(10); return 1; }
        чыганак_үлчәмен_үзгәртү = 자바도구.원문해독(чыганак, чыганак_үлчәмен_үзгәртү);
        if (чыганак_үлчәмен_үзгәртү < 0) { кулланучы.язу("javac error: invalid UTF-8 source\n"); return 1; }
        кисү_VALUE(); if (!Хата) 선언읽기();
        if (!Хата) {
            if (токен_озынлык[класс_токен] != исем_үлчәмен_үзгәртү - 5) эштән_туктау_VALUE("class name must match file name");
            for (int 수 = 0; 수 < исем_үлчәмен_үзгәртү - 5; 수++) if (чыганак[токен_урнаштыру[класс_токен] + 수] != файл_исем_СМС[수]) эштән_туктау_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < ысул_COUNT && !Хата; 현재함수++) {
            урнаштыру = 함수본문[현재함수]; ысул_CODE[현재함수] = CODE_үлчәмен_үзгәртү; локаль_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < ысул_аргумент_COUNT[현재함수]; 수++) өстәү_локаль(ысул_аргумент_исем[현재함수 * 16 + 수], ысул_аргумент_TYPE[현재함수 * 16 + 수]);
            boolean кайтару_үлчәм = аңлатма_VALUE();
            if (!кайтару_үлчәм && ысул_кайтару[현재함수] != 0) эштән_туктау_VALUE("missing return");
            // тармак 뒤의 합류 지점은 반드시 фактик_мәгълүмат 명령이어야 한다 (버전 49 검증기).
            if (ысул_кайтару[현재함수] == 0) 내보내기(177);
            else { boolean бөтен_сан = ысул_кайтару[현재함수] <= 2 || ысул_кайтару[현재함수] == 5; 내보내기(бөтен_сан ? 3 : 1); 내보내기(бөтен_сан ? 172 : 176); }
            if (урнаштыру != ысул_тәмамлау[현재함수]) эштән_туктау_VALUE("invalid method body");
            함수지역[현재함수] = локаль_COUNT; ысул_озынлык[현재함수] = CODE_үлчәмен_үзгәртү - ысул_CODE[현재함수];
        }
        if (Хата) return 1;
        язу_класс(); if (Хата) return 1;
        файл_исем_СМС[исем_үлчәмен_үзгәртү - 4] = 'c'; файл_исем_СМС[исем_үлчәмен_үзгәртү - 3] = 'l'; файл_исем_СМС[исем_үлчәмен_үзгәртү - 2] = 'a';
        файл_исем_СМС[исем_үлчәмен_үзгәртү - 1] = 's'; файл_исем_СМС[исем_үлчәмен_үзгәртү] = 's'; файл_исем_СМС[исем_үлчәмен_үзгәртү + 1] = 0;
        int үлчәм = кулланучы.язу_файл(файл_исем_СМС, 출력, 출력크기);
        if (үлчәм < 0) { кулланучы.язу("javac: cannot save class: "); 자바도구.수쓰기(үлчәм); кулланучы.язу_символ_VALUE(10); return 1; }
        кулланучы.язу("Compiled: "); for (int 수 = 0; файл_исем_СМС[수] != 0; 수++) кулланучы.язу_символ_VALUE(файл_исем_СМС[수]);
        кулланучы.язу(" (JVM class version 49)\n"); return 0;
    }
}
