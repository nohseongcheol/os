// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java извор_дрво -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] ИЗВОР = new int[16384], 출력 = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], токен_позиционирање = new int[2048], токен_должина = new int[2048];
    static int[] константа_VALUE = new int[4096], константа_OFFSET = new int[512];
    static int[] 문자 = new int[512], датотека_име_СМС = new int[64];
    static int[] 삽입코드 = new int[16];
    static int извор_големина, токен_COUNT, Позиција, CODE_големина, константа_големина, константа_COUNT = 1, 출력크기, знак_должина;
    static boolean ГРЕШКА;
    static int класа_токен, класа_константа, 부모상수, CODE_константа;
    static int[] метод_внес_име = new int[32], 함수반환 = new int[32], метод_аргумент_COUNT = new int[32];
    static int[] метод_аргумент_име = new int[512], метод_аргумент_TYPE = new int[512];
    static int[] метод_тело = new int[32], метод_крај = new int[32], метод_CODE = new int[32];
    static int[] метод_должина = new int[32], 함수지역 = new int[32], метод_име_константа = new int[32], 함수서술 = new int[32];
    static int[] метод_пристап = new int[32];
    static int метод_COUNT, 현재함수, локален_COUNT, 깊이, 식깊이;
    static int[] локален_име = new int[128], локален_TYPE = new int[128], 지역깊이 = new int[128];

    static void неуспех_VALUE(String 이유) {
        if (!ГРЕШКА) {
            корисник.Запиши("javac error: "); корисник.Запиши(이유);
            корисник.Запиши(" at line ");
            int ред = 1, 끝 = Позиција < токен_COUNT ? токен_позиционирање[Позиција] : извор_големина;
            for (int 수 = 0; 수 < 끝; 수++) if (ИЗВОР[수] == 10) ред++;
            자바도구.수쓰기(ред); корисник.запиши_знак_VALUE(10);
        }
        ГРЕШКА = true;
    }
    static boolean знак_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean цифра_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= токен_COUNT || 나 >= токен_COUNT || токен_должина[가] != токен_должина[나]) return false;
        for (int 수 = 0; 수 < токен_должина[가]; 수++) if (ИЗВОР[токен_позиционирање[가] + 수] != ИЗВОР[токен_позиционирање[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int токен_VALUE, String Word_СМС) {
        if (токен_VALUE < 0 || токен_VALUE >= токен_COUNT || токен_должина[токен_VALUE] != Word_СМС.length()) return false;
        for (int 수 = 0; 수 < Word_СМС.length(); 수++) if (ИЗВОР[токен_позиционирање[токен_VALUE] + 수] != Word_СМС.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Позиција < токен_COUNT ? 토큰종류[Позиција] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; Позиција++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) неуспех_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_СМС) { if (!Word_VALUE(Позиција, Word_СМС)) return false; Позиција++; return true; }
    static void 말요구(String Word_СМС) { if (!TAKE_Word(Word_СМС)) неуспех_VALUE(Word_СМС); }
    static int идентификатор_VALUE() {
        int мерка = Позиција;
        if (종류() != 256) неуспех_VALUE("identifier required"); else Позиција++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Изврши_2 = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Изврши_2 == токен_должина[мерка];
                for (int отвор_внес = Изврши_2; 같음 && отвор_внес < 수; отвор_внес++) if (예약어.charAt(отвор_внес) != ИЗВОР[токен_позиционирање[мерка] + отвор_внес - Изврши_2]) 같음 = false;
                if (같음) неуспех_VALUE("reserved word cannot be an identifier");
                Изврши_2 = 수 + 1;
            }
        }
        return мерка;
    }
    static void отсечи_VALUE() {
        int 수 = 0;
        while (수 < извор_големина && !ГРЕШКА) {
            int VALUE = ИЗВОР[수], Изврши_2 = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < извор_големина && ИЗВОР[수 + 1] == '/') {
                while (수 < извор_големина && ИЗВОР[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < извор_големина && ИЗВОР[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < извор_големина && !(ИЗВОР[수] == '*' && ИЗВОР[수 + 1] == '/')) 수++;
                if (수 + 1 >= извор_големина) { неуспех_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (знак_VALUE(VALUE)) { 종류 = 256; while (수 < извор_големина && 문자이름규칙.이어진글자(ИЗВОР[수])) 수++; }
            else if (цифра_VALUE(VALUE)) { 종류 = 257; while (수 < извор_големина && цифра_VALUE(ИЗВОР[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < извор_големина && ИЗВОР[수] != VALUE && ИЗВОР[수] != 10 && ИЗВОР[수] != 13) {
                    if (ИЗВОР[수] == '\\') 수++;
                    수++;
                }
                if (수 >= извор_големина || ИЗВОР[수] != VALUE) { неуспех_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < извор_големина) {
                    int Следно_ставка = ИЗВОР[수];
                    if (VALUE == '=' && Следно_ставка == '=') 종류 = 300;
                    if (VALUE == '!' && Следно_ставка == '=') 종류 = 301;
                    if (VALUE == '<' && Следно_ставка == '=') 종류 = 302;
                    if (VALUE == '>' && Следно_ставка == '=') 종류 = 303;
                    if (VALUE == '&' && Следно_ставка == '&') 종류 = 304;
                    if (VALUE == '|' && Следно_ставка == '|') 종류 = 305;
                    if (VALUE == '+' && Следно_ставка == '+') 종류 = 306;
                    if (VALUE == '-' && Следно_ставка == '-') 종류 = 307;
                    if (VALUE == '+' && Следно_ставка == '=') 종류 = 308;
                    if (VALUE == '-' && Следно_ставка == '=') 종류 = 309;
                    if (VALUE == '*' && Следно_ставка == '=') 종류 = 310;
                    if (VALUE == '/' && Следно_ставка == '=') 종류 = 311;
                    if (VALUE == '%' && Следно_ставка == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (токен_COUNT == 토큰종류.length - 1) { неуспех_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[токен_COUNT] = 종류; токен_позиционирање[токен_COUNT] = Изврши_2; токен_должина[токен_COUNT++] = 수 - Изврши_2;
        }
    }
    static void запиши_константа_бајт(int VALUE) {
        if (константа_големина == константа_VALUE.length) { неуспех_VALUE("constant pool too large"); return; }
        константа_VALUE[константа_големина++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { запиши_константа_бајт(VALUE >> 8); запиши_константа_бајт(VALUE); }
    static int регистрирај_константа(int Изврши_2) {
        for (int 수 = 1; 수 < константа_COUNT; 수++) {
            int предна_VALUE = константа_OFFSET[수], должина_VALUE = (수 + 1 < константа_COUNT ? константа_OFFSET[수 + 1] : Изврши_2) - предна_VALUE;
            if (должина_VALUE != константа_големина - Изврши_2) continue;
            boolean 같음 = true;
            for (int отвор_внес = 0; отвор_внес < должина_VALUE; отвор_внес++) if (константа_VALUE[предна_VALUE + отвор_внес] != константа_VALUE[Изврши_2 + отвор_внес]) 같음 = false;
            if (같음) { константа_големина = Изврши_2; return 수; }
        }
        if (константа_COUNT == константа_OFFSET.length) { неуспех_VALUE("too many constants"); return 0; }
        константа_OFFSET[константа_COUNT] = Изврши_2;
        return константа_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (знак_должина == 문자.length) { неуспех_VALUE("text too long"); return; }
        문자[знак_должина++] = VALUE;
    }
    static void 말추가(String Word_СМС) { for (int 수 = 0; 수 < Word_СМС.length(); 수++) 글추가(Word_СМС.charAt(수)); }
    static int знак_константа() {
        int Изврши_2 = константа_големина; запиши_константа_бајт(1); 상짧(0);
        for (int 수 = 0; 수 < знак_должина; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) запиши_константа_бајт(VALUE);
            else if (VALUE < 2048) { запиши_константа_бајт(192 | VALUE >> 6); запиши_константа_бајт(128 | VALUE & 63); }
            else { запиши_константа_бајт(224 | VALUE >> 12); запиши_константа_бајт(128 | VALUE >> 6 & 63); запиши_константа_бајт(128 | VALUE & 63); }
        }
        if (ГРЕШКА) return 0;
        int должина_VALUE = константа_големина - Изврши_2 - 3;
        константа_VALUE[Изврши_2 + 1] = должина_VALUE >> 8; константа_VALUE[Изврши_2 + 2] = должина_VALUE & 255;
        return регистрирај_константа(Изврши_2);
    }
    static int Word_константа(String Word_СМС) { знак_должина = 0; 말추가(Word_СМС); return знак_константа(); }
    static int токен_константа(int токен_VALUE) {
        знак_должина = 0;
        for (int 수 = 0; 수 < токен_должина[токен_VALUE]; 수++) 글추가(ИЗВОР[токен_позиционирање[токен_VALUE] + 수]);
        return знак_константа();
    }
    static int Референци(int 종류, int 가, int 나) {
        int Изврши_2 = константа_големина; запиши_константа_бајт(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return регистрирај_константа(Изврши_2);
    }
    static int надворешна_референца(int 종류, String сопственик_VALUE, String Име, String 서술) {
        int сопственик_идентификатор = Референци(7, Word_константа(сопственик_VALUE), 0);
        int име_COUNT = Word_константа(Име), формат_COUNT = Word_константа(서술);
        return Референци(종류, сопственик_идентификатор, Референци(12, име_COUNT, формат_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_големина == CODE_VALUE.length) { неуспех_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_големина++] = VALUE & 255;
    }
    static void Команда(int VALUE, int Аргументи) { 내보내기(VALUE); 내보내기(Аргументи >> 8); 내보내기(Аргументи); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Изврши_2 = константа_големина; запиши_константа_бајт(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Команда(19, регистрирај_константа(Изврши_2));
    }
    static int гранка(int Команда) { int мерка = CODE_големина; Команда(Команда, 0); return мерка; }
    static void Врска_VALUE(int гранка, int цел_објект) {
        if (ГРЕШКА) return;
        int 거리 = цел_објект - гранка;
        if (거리 < -32768 || 거리 > 32767 || гранка < 0 || гранка + 2 >= CODE_големина) { неуспех_VALUE("invalid branch"); return; }
        CODE_VALUE[гранка + 1] = 거리 >> 8 & 255; CODE_VALUE[гранка + 2] = 거리 & 255;
    }
    static void Споредба_VALUE(int Команда) {
        int TRUE_VALUE = гранка(Команда); 내보내기(3); int 끝 = гранка(167);
        Врска_VALUE(TRUE_VALUE, CODE_големина); 내보내기(4); Врска_VALUE(끝, CODE_големина);
    }
    static int формат_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        неуспех_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void додавање_формат(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws декларација. исклучок Процес_VALUE_внес 본문은 вдоми javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Македонски");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("исклучок") || TAKE_Word("실행예외") || TAKE_Word("В_И_исклучок") || TAKE_Word("почекај_TIMEOUT_исклучок") || TAKE_Word("адреса_LOOKUP_исклучок") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("неважечки_аргумент_исклучок") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_Референци_исклучок") || TAKE_Word("산술예외") || TAKE_Word("статус_исклучок") || TAKE_Word("TYPE_емитувај_исклучок") || TAKE_Word("음수배열크기예외") || TAKE_Word("низа_Store_неуспех") || TAKE_Word("нишка_статус_исклучок") || TAKE_Word("대기중단예외")) return;
        неуспех_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Позиција, "Македонски")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) неуспех_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); класа_токен = идентификатор_VALUE();
        класа_константа = Референци(7, токен_константа(класа_токен), 0);
        부모상수 = Референци(7, Word_константа("java/lang/Object"), 0); CODE_константа = Word_константа("Code"); 요구('{');
        while (!ГРЕШКА && 종류() != '}') {
            if (метод_COUNT == 32) { неуспех_VALUE("too many methods"); break; }
            int пристап_внес = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int ФУНКЦИЈА_VALUE = метод_COUNT++;
            метод_пристап[ФУНКЦИЈА_VALUE] = пристап_внес | 8;
            함수반환[ФУНКЦИЈА_VALUE] = формат_VALUE(); метод_внес_име[ФУНКЦИЈА_VALUE] = идентификатор_VALUE(); 요구('(');
            for (int предна_VALUE = 0; предна_VALUE < ФУНКЦИЈА_VALUE; предна_VALUE++) if (이름같음(метод_внес_име[предна_VALUE], метод_внес_име[ФУНКЦИЈА_VALUE])) неуспех_VALUE("duplicate method (overloading unsupported)");
            while (!ГРЕШКА && 종류() != ')') {
                int 수 = метод_аргумент_COUNT[ФУНКЦИЈА_VALUE];
                if (수 == 16) { неуспех_VALUE("too many parameters"); break; }
                int TYPE_VALUE = формат_VALUE(); if (TYPE_VALUE == 0) неуспех_VALUE("void parameter");
                метод_аргумент_TYPE[ФУНКЦИЈА_VALUE * 16 + 수] = TYPE_VALUE; метод_аргумент_име[ФУНКЦИЈА_VALUE * 16 + 수] = идентификатор_VALUE();
                метод_аргумент_COUNT[ФУНКЦИЈА_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!ГРЕШКА && 받기(','));
            }
            метод_тело[ФУНКЦИЈА_VALUE] = Позиција; 요구('{');
            int вгнездување_VALUE = 1;
            while (Позиција < токен_COUNT && вгнездување_VALUE > 0) {
                if (종류() == '{') вгнездување_VALUE++;
                if (종류() == '}') вгнездување_VALUE--;
                Позиција++;
            }
            if (вгнездување_VALUE != 0) неуспех_VALUE("unclosed method body");
            метод_крај[ФУНКЦИЈА_VALUE] = Позиција;
            метод_име_константа[ФУНКЦИЈА_VALUE] = токен_константа(метод_внес_име[ФУНКЦИЈА_VALUE]);
            знак_должина = 0; 글추가('(');
            for (int 수 = 0; 수 < метод_аргумент_COUNT[ФУНКЦИЈА_VALUE]; 수++) додавање_формат(метод_аргумент_TYPE[ФУНКЦИЈА_VALUE * 16 + 수]);
            글추가(')'); додавање_формат(함수반환[ФУНКЦИЈА_VALUE]); 함수서술[ФУНКЦИЈА_VALUE] = знак_константа();
        }
        요구('}'); if (Позиција != токен_COUNT) неуспех_VALUE("extra input after class");
    }
    static int FIND_локален(int Име) {
        for (int 수 = локален_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(локален_име[수], Име)) return 수;
        неуспех_VALUE("unknown variable"); return 0;
    }
    static int додавање_локален(int Име, int TYPE_VALUE) {
        for (int 수 = 0; 수 < локален_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(локален_име[수], Име)) неуспех_VALUE("duplicate local variable");
        if (локален_COUNT == 128) { неуспех_VALUE("too many locals"); return 0; }
        локален_име[локален_COUNT] = Име; локален_TYPE[локален_COUNT] = TYPE_VALUE; 지역깊이[локален_COUNT] = 깊이;
        return локален_COUNT++;
    }
    static boolean цел_број_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(локален_TYPE[수] <= 2 || локален_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void запиши_локален(int 수) { 내보내기(локален_TYPE[수] <= 2 || локален_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void провери_TYPE(int реален_податоци, int 기대) { if (реален_податоци != 기대 && !(реален_податоци == 5 && 기대 == 1)) неуспех_VALUE("type mismatch"); }
    static void 문자읽기(int токен_VALUE) {
        знак_должина = 0; int Изврши_2 = токен_позиционирање[токен_VALUE] + 1, 끝 = токен_позиционирање[токен_VALUE] + токен_должина[токен_VALUE] - 1;
        while (Изврши_2 < 끝 && !ГРЕШКА) {
            int VALUE = ИЗВОР[Изврши_2++];
            if (VALUE == '\\') {
                if (Изврши_2 == 끝) { неуспех_VALUE("invalid escape"); break; }
                VALUE = ИЗВОР[Изврши_2++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') неуспех_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int разложи_цел_број(int токен_VALUE, boolean 음수) {
        if (токен_должина[токен_VALUE] > 1 && ИЗВОР[токен_позиционирање[токен_VALUE]] == '0') неуспех_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < токен_должина[токен_VALUE]; 수++) {
            int цифра_ставка = ИЗВОР[токен_позиционирање[токен_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && цифра_ставка > (음수 ? 8 : 7)) неуспех_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - цифра_ставка;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = формат_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { неуспех_VALUE("only file streams supported by new in source"); return 0; }
            String сопственик_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Команда(187, Референци(7, Word_константа(сопственик_VALUE), 0)); 내보내기(89);
            요구('('); провери_TYPE(израз_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) неуспех_VALUE("input stream constructor arguments"); провери_TYPE(израз_VALUE(), 2); 이어 = true; }
            요구(')');
            Команда(183, надворешна_референца(10, сопственик_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = израз_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(разложи_цел_број(Позиција++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Позиција++); Команда(19, Референци(8, знак_константа(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Позиција++); if (знак_должина != 1) неуспех_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Македонски")) {
            요구('.'); 말요구("자체"); 요구('.');
            String сопственик_VALUE = "", метод_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, мерка = 0;
            if (TAKE_Word("출력")) {
                сопственик_VALUE = "Македонски/자체/출력"; 요구('.');
                if (TAKE_Word("запиши_ред")) { метод_VALUE = "запиши_ред"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Запиши")) { метод_VALUE = "Запиши"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { метод_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else неуспех_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                сопственик_VALUE = "Македонски/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("должина_VALUE")) { метод_VALUE = "должина_VALUE"; 서술 = "(Ljava/lang/String;)I"; мерка = 1; }
                else if (TAKE_Word("кодна_точка_COUNT")) { метод_VALUE = "кодна_точка_COUNT"; 서술 = "(Ljava/lang/String;)I"; мерка = 1; }
                else if (TAKE_Word("разложи_цел_број")) { метод_VALUE = "разложи_цел_број"; 서술 = "(Ljava/lang/String;)I"; мерка = 1; }
                else if (TAKE_Word("запиши_цел_број_VALUE")) { метод_VALUE = "запиши_цел_број_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; мерка = 3; }
                else if (TAKE_Word("같음")) { метод_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; мерка = 2; }
                else if (TAKE_Word("залепи_СМС")) { метод_VALUE = "залепи_СМС"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; мерка = 3; }
                else if (TAKE_Word("отсечи_VALUE")) { метод_VALUE = "отсечи_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; мерка = 3; }
                else неуспех_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Датотека")) {
                сопственик_VALUE = "Македонски/자체/Датотека"; 요구('.'); 가 = 3;
                if (TAKE_Word("Читај")) { метод_VALUE = "Читај"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; мерка = 3; }
                else if (TAKE_Word("Запиши")) { метод_VALUE = "Запиши"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else неуспех_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                сопственик_VALUE = "Македонски/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { метод_VALUE = "너비"; 서술 = "()I"; мерка = 1; }
                else if (TAKE_Word("높이")) { метод_VALUE = "높이"; 서술 = "()I"; мерка = 1; }
                else if (TAKE_Word("사각형")) { метод_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("избриши_внес")) { метод_VALUE = "избриши_внес"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { метод_VALUE = "기다리기"; 서술 = "()V"; }
                else неуспех_VALUE("unknown Korean framebuffer method");
            } else неуспех_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) провери_TYPE(израз_VALUE(), 가);
            if (나 != 0) { 요구(','); провери_TYPE(израз_VALUE(), 나); }
            if (다 != 0) { 요구(','); провери_TYPE(израз_VALUE(), 다); }
            if (라 != 0) { 요구(','); провери_TYPE(израз_VALUE(), 라); }
            if (마 != 0) { 요구(','); провери_TYPE(израз_VALUE(), 마); }
            요구(')'); Команда(184, надворешна_референца(10, сопственик_VALUE, метод_VALUE, 서술)); return мерка;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); провери_TYPE(израз_VALUE(), 3); 요구(')');
            Команда(184, надворешна_референца(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Име = идентификатор_VALUE();
        if (받기('(')) {
            int ФУНКЦИЈА_VALUE = -1;
            for (int 수 = 0; 수 < метод_COUNT; 수++) if (이름같음(Име, метод_внес_име[수])) ФУНКЦИЈА_VALUE = 수;
            if (ФУНКЦИЈА_VALUE < 0) { неуспех_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!ГРЕШКА && 종류() != ')') {
                if (수 >= метод_аргумент_COUNT[ФУНКЦИЈА_VALUE]) { неуспех_VALUE("too many arguments"); break; }
                провери_TYPE(израз_VALUE(), метод_аргумент_TYPE[ФУНКЦИЈА_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != метод_аргумент_COUNT[ФУНКЦИЈА_VALUE]) неуспех_VALUE("argument count mismatch");
            Команда(184, Референци(10, класа_константа, Референци(12, метод_име_константа[ФУНКЦИЈА_VALUE], 함수서술[ФУНКЦИЈА_VALUE])));
            return 함수반환[ФУНКЦИЈА_VALUE];
        }
        int локален_обем = FIND_локален(Име), TYPE_VALUE = локален_TYPE[локален_обем]; 지역읽기(локален_обем);
        while (!ГРЕШКА) {
            if (받기('[')) { провери_TYPE(TYPE_VALUE, 4); провери_TYPE(израз_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String сопственик_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Команда(182, надворешна_референца(10, сопственик_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Команда(182, надворешна_референца(10, сопственик_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); провери_TYPE(израз_VALUE(), 1); 요구(')'); Команда(182, надворешна_референца(10, сопственик_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { неуспех_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { провери_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Команда(182, надворешна_референца(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { неуспех_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { провери_TYPE(단항(), 2); Споредба_VALUE(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(разложи_цел_број(Позиција++, true));
            else { провери_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { провери_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!ГРЕШКА && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int кодирање_VALUE = 종류(); Позиција++; провери_TYPE(TYPE_VALUE, 1); провери_TYPE(단항(), 1);
            내보내기(кодирање_VALUE == '*' ? 104 : кодирање_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!ГРЕШКА && (종류() == '+' || 종류() == '-')) {
            int кодирање_VALUE = 종류(); Позиција++; int 경계 = CODE_големина, Назад_VALUE_TYPE = 곱식();
            if (кодирање_VALUE == '+' && (TYPE_VALUE == 3 || Назад_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, Назад_VALUE_TYPE); TYPE_VALUE = 3; }
            else { провери_TYPE(TYPE_VALUE, 1); провери_TYPE(Назад_VALUE_TYPE, 1); 내보내기(кодирање_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) неуспех_VALUE("unsupported concatenation type");
        return надворешна_референца(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int предна_VALUE_TYPE, int Назад_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 генерира 코드를 삽입한다.
        // RIGHT израз_VALUE 내부의 рамноправен_уред_VALUE гранка 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_големина;
        Команда(187, Референци(7, Word_константа("java/lang/StringBuilder"), 0)); 내보내기(89);
        Команда(183, надворешна_референца(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Команда(182, 붙임참조(предна_VALUE_TYPE));
        if (ГРЕШКА) return;
        int должина_VALUE = CODE_големина - 끝;
        for (int 수 = 0; 수 < должина_VALUE; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + должина_VALUE] = CODE_VALUE[수];
        for (int 수 = 0; 수 < должина_VALUE; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        Команда(182, 붙임참조(Назад_VALUE_TYPE)); Команда(182, надворешна_референца(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Споредба_израз() {
        int TYPE_VALUE = 합식();
        while (!ГРЕШКА && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int кодирање_VALUE = 종류(); Позиција++; провери_TYPE(TYPE_VALUE, 1); провери_TYPE(합식(), 1);
            Споредба_VALUE(кодирање_VALUE == '<' ? 161 : кодирање_VALUE == '>' ? 163 : кодирање_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Споредба_израз();
        while (!ГРЕШКА && (종류() == 300 || 종류() == 301)) {
            int кодирање_VALUE = 종류(); Позиција++; int Назад_VALUE_TYPE = Споредба_израз();
            if (TYPE_VALUE == 0 || Назад_VALUE_TYPE == 0) неуспех_VALUE("void expression");
            if (!(цел_број_TYPE(TYPE_VALUE) && цел_број_TYPE(Назад_VALUE_TYPE))) провери_TYPE(Назад_VALUE_TYPE, TYPE_VALUE);
            Споредба_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (кодирање_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!ГРЕШКА && 받기(304)) {
            провери_TYPE(TYPE_VALUE, 2); int 가 = гранка(153); провери_TYPE(동등식(), 2); int 나 = гранка(153);
            내보내기(4); int 끝 = гранка(167); Врска_VALUE(가, CODE_големина); Врска_VALUE(나, CODE_големина); 내보내기(3); Врска_VALUE(끝, CODE_големина); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int израз_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!ГРЕШКА && 받기(305)) {
            провери_TYPE(TYPE_VALUE, 2); int 가 = гранка(154); провери_TYPE(논리곱(), 2); int 나 = гранка(154);
            내보내기(3); int 끝 = гранка(167); Врска_VALUE(가, CODE_големина); Врска_VALUE(나, CODE_големина); 내보내기(4); Врска_VALUE(끝, CODE_големина); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void задача_VALUE(boolean Дозволи_декларација) {
        if (Word_VALUE(Позиција, "int") || Word_VALUE(Позиција, "boolean") || Word_VALUE(Позиција, "String") || Word_VALUE(Позиција, "char")
            || Word_VALUE(Позиција, "FileInputStream") || Word_VALUE(Позиција, "FileOutputStream")) {
            if (!Дозволи_декларација) неуспех_VALUE("declaration not allowed here");
            int TYPE_VALUE = формат_VALUE(), Име = идентификатор_VALUE(); 요구('='); провери_TYPE(израз_VALUE(), TYPE_VALUE);
            запиши_локален(додавање_локален(Име, TYPE_VALUE)); return;
        }
        int Име = идентификатор_VALUE(), локален_обем = FIND_локален(Име);
        if (받기('=')) { провери_TYPE(израз_VALUE(), локален_TYPE[локален_обем]); запиши_локален(локален_обем); }
        else if (종류() >= 308 && 종류() <= 312) {
            int кодирање_VALUE = 종류(); Позиција++; 지역읽기(локален_обем); int 경계 = CODE_големина, Назад_VALUE_TYPE = израз_VALUE();
            if (кодирање_VALUE == 308 && локален_TYPE[локален_обем] == 3) 결합(경계, 3, Назад_VALUE_TYPE);
            else {
                провери_TYPE(локален_TYPE[локален_обем], 1); провери_TYPE(Назад_VALUE_TYPE, 1);
                내보내기(кодирање_VALUE == 308 ? 96 : кодирање_VALUE == 309 ? 100 : кодирање_VALUE == 310 ? 104 : кодирање_VALUE == 311 ? 108 : 112);
                if (локален_TYPE[локален_обем] == 5) 내보내기(146);
            }
            запиши_локален(локален_обем);
        }
        else if (종류() == 306 || 종류() == 307) {
            провери_TYPE(локален_TYPE[локален_обем], 1); 내보내기(132); 내보내기(локален_обем); 내보내기(종류() == 306 ? 1 : 255); Позиција++;
            if (локален_TYPE[локален_обем] == 5) { 지역읽기(локален_обем); 내보내기(146); запиши_локален(локален_обем); }
        } else неуспех_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Команда(178, надворешна_референца(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean празно_аргумент = 종류() == ')';
        int TYPE_VALUE = празно_аргумент ? 0 : израз_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !празно_аргумент)) неуспех_VALUE("unsupported print argument");
        Команда(182, надворешна_референца(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean изјава_VALUE() {
        if (ГРЕШКА) return false;
        if (깊이 > 32) { неуспех_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!ГРЕШКА && 종류() != '}') { if (반환) неуспех_VALUE("unreachable statement"); 반환 = изјава_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < локален_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : израз_VALUE(); провери_TYPE(TYPE_VALUE, 함수반환[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); провери_TYPE(израз_VALUE(), 2); 요구(')'); int FALSE_VALUE = гранка(153);
            깊이++; boolean 가 = контрола_изјава(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = гранка(167); Врска_VALUE(FALSE_VALUE, CODE_големина); 깊이++; boolean 나 = контрола_изјава(); 깊이--; Врска_VALUE(끝, CODE_големина); return 가 && 나; }
            Врска_VALUE(FALSE_VALUE, CODE_големина); return false;
        }
        if (TAKE_Word("while")) {
            int Изврши_2 = CODE_големина; 요구('('); провери_TYPE(израз_VALUE(), 2); 요구(')'); int 끝 = гранка(153);
            깊이++; контрола_изјава(); 깊이--; Врска_VALUE(гранка(167), Изврши_2); Врска_VALUE(끝, CODE_големина); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') задача_VALUE(true); 요구(';');
            int услов = CODE_големина; if (종류() == ';') 내보내기(4); else провери_TYPE(израз_VALUE(), 2); 요구(';');
            int 끝 = гранка(153), основен_текст = гранка(167), освежи = CODE_големина;
            if (종류() != ')') задача_VALUE(false); 요구(')'); Врска_VALUE(гранка(167), услов); Врска_VALUE(основен_текст, CODE_големина);
            контрола_изјава(); Врска_VALUE(гранка(167), освежи); Врска_VALUE(끝, CODE_големина);
            for (int 수 = 0; 수 < локален_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Позиција, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Позиција + 1 < токен_COUNT && (토큰종류[Позиција + 1] == '(' || 토큰종류[Позиција + 1] == '.')) {
            int TYPE_VALUE = израз_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        задача_VALUE(true); 요구(';'); return false;
    }
    static boolean контрола_изјава() {
        if (Word_VALUE(Позиција, "int") || Word_VALUE(Позиција, "boolean") || Word_VALUE(Позиција, "char") || Word_VALUE(Позиција, "String")
            || Word_VALUE(Позиција, "FileInputStream") || Word_VALUE(Позиција, "FileOutputStream")) неуспех_VALUE("local declaration requires braces");
        return изјава_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) неуспех_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void запиши_класа() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(константа_COUNT);
        for (int 수 = 0; 수 < константа_големина; 수++) 출바(константа_VALUE[수]);
        출짧(0x21); 출짧(класа_константа); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(метод_COUNT);
        for (int 수 = 0; 수 < метод_COUNT; 수++) {
            출짧(метод_пристап[수]); 출짧(метод_име_константа[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_константа);
            출정(12 + метод_должина[수]); 출짧(128); 출짧(함수지역[수]); 출정(метод_должина[수]);
            for (int отвор_внес = 0; отвор_внес < метод_должина[수]; отвор_внес++) 출바(CODE_VALUE[метод_CODE[수] + отвор_внес]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Изврши_2() {
        if (корисник.인수개수() == 1 && 자바도구.같음(корисник.Аргументи(0), "-version")) {
            корисник.Запиши("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (корисник.인수개수() != 1) { корисник.Запиши("Usage: javac FILE.java\n"); return 2; }
        int име_големина = 자바도구.Име(датотека_име_СМС, корисник.Аргументи(0));
        if (име_големина < 6 || име_големина > 62 || датотека_име_СМС[име_големина - 5] != '.' || датотека_име_СМС[име_големина - 4] != 'j'
            || датотека_име_СМС[име_големина - 3] != 'a' || датотека_име_СМС[име_големина - 2] != 'v' || датотека_име_СМС[име_големина - 1] != 'a') {
            корисник.Запиши("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        извор_големина = корисник.파일읽기(датотека_име_СМС, ИЗВОР);
        if (извор_големина < 0) { корисник.Запиши("javac: cannot read source: "); 자바도구.수쓰기(извор_големина); корисник.запиши_знак_VALUE(10); return 1; }
        извор_големина = 자바도구.원문해독(ИЗВОР, извор_големина);
        if (извор_големина < 0) { корисник.Запиши("javac error: invalid UTF-8 source\n"); return 1; }
        отсечи_VALUE(); if (!ГРЕШКА) 선언읽기();
        if (!ГРЕШКА) {
            if (токен_должина[класа_токен] != име_големина - 5) неуспех_VALUE("class name must match file name");
            for (int 수 = 0; 수 < име_големина - 5; 수++) if (ИЗВОР[токен_позиционирање[класа_токен] + 수] != датотека_име_СМС[수]) неуспех_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < метод_COUNT && !ГРЕШКА; 현재함수++) {
            Позиција = метод_тело[현재함수]; метод_CODE[현재함수] = CODE_големина; локален_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < метод_аргумент_COUNT[현재함수]; 수++) додавање_локален(метод_аргумент_име[현재함수 * 16 + 수], метод_аргумент_TYPE[현재함수 * 16 + 수]);
            boolean 반환 = изјава_VALUE();
            if (!반환 && 함수반환[현재함수] != 0) неуспех_VALUE("missing return");
            // гранка 뒤의 합류 지점은 반드시 реален_податоци 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean цел_број = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(цел_број ? 3 : 1); 내보내기(цел_број ? 172 : 176); }
            if (Позиција != метод_крај[현재함수]) неуспех_VALUE("invalid method body");
            함수지역[현재함수] = локален_COUNT; метод_должина[현재함수] = CODE_големина - метод_CODE[현재함수];
        }
        if (ГРЕШКА) return 1;
        запиши_класа(); if (ГРЕШКА) return 1;
        датотека_име_СМС[име_големина - 4] = 'c'; датотека_име_СМС[име_големина - 3] = 'l'; датотека_име_СМС[име_големина - 2] = 'a';
        датотека_име_СМС[име_големина - 1] = 's'; датотека_име_СМС[име_големина] = 's'; датотека_име_СМС[име_големина + 1] = 0;
        int мерка = корисник.запиши_датотека(датотека_име_СМС, 출력, 출력크기);
        if (мерка < 0) { корисник.Запиши("javac: cannot save class: "); 자바도구.수쓰기(мерка); корисник.запиши_знак_VALUE(10); return 1; }
        корисник.Запиши("Compiled: "); for (int 수 = 0; датотека_име_СМС[수] != 0; 수++) корисник.запиши_знак_VALUE(датотека_име_СМС[수]);
        корисник.Запиши(" (JVM class version 49)\n"); return 0;
    }
}
