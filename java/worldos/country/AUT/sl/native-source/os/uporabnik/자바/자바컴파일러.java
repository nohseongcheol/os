// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java vir_drevo -> 표준 버전 49 class prevajalnik. */
public final class 자바컴파일러 {
    static int[] VIR = new int[16384], Izpis = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], žeton_položaj = new int[2048], 토큰길이 = new int[2048];
    static int[] konstanta_VALUE = new int[4096], konstanta_odmik = new int[512];
    static int[] 문자 = new int[512], ime_datoteke_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int vir_spremeniti_velikost, žeton_COUNT, Položaj, CODE_spremeniti_velikost, konstanta_spremeniti_velikost, konstanta_COUNT = 1, 출력크기, 문자수;
    static boolean NAPAKA;
    static int Razred_žeton, Razred_konstanta, nadrejen_konstanta, CODE_konstanta;
    static int[] metoda_vnos_ime = new int[32], metoda_vrni = new int[32], metoda_argument_COUNT = new int[32];
    static int[] metoda_argument_ime = new int[512], metoda_argument_Tip = new int[512];
    static int[] metoda_telo = new int[32], metoda_končati_klic = new int[32], metoda_CODE = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], metoda_ime_konstanta = new int[32], 함수서술 = new int[32];
    static int[] metoda_dostop = new int[32];
    static int metoda_COUNT, sprotno_metoda, lokalen_krajeven_COUNT, 깊이, 식깊이;
    static int[] lokalen_krajeven_ime = new int[128], lokalen_krajeven_Tip = new int[128], 지역깊이 = new int[128];

    static void napaka_VALUE(String 이유) {
        if (!NAPAKA) {
            uporabnik.Pisanje("javac error: "); uporabnik.Pisanje(이유);
            uporabnik.Pisanje(" at line ");
            int Črtni = 1, 끝 = Položaj < žeton_COUNT ? žeton_položaj[Položaj] : vir_spremeniti_velikost;
            for (int 수 = 0; 수 < 끝; 수++) if (VIR[수] == 10) Črtni++;
            자바도구.수쓰기(Črtni); uporabnik.pisati_znak_VALUE(10);
        }
        NAPAKA = true;
    }
    static boolean znak_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean številka_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int SECOND_operand) {
        if (가 < 0 || SECOND_operand < 0 || 가 >= žeton_COUNT || SECOND_operand >= žeton_COUNT || 토큰길이[가] != 토큰길이[SECOND_operand]) return false;
        for (int 수 = 0; 수 < 토큰길이[가]; 수++) if (VIR[žeton_položaj[가] + 수] != VIR[žeton_položaj[SECOND_operand] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int žeton_VALUE, String Word_SMS) {
        if (žeton_VALUE < 0 || žeton_VALUE >= žeton_COUNT || 토큰길이[žeton_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (VIR[žeton_položaj[žeton_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Položaj < žeton_COUNT ? 토큰종류[Položaj] : 0; }
    static boolean sprejeti_sprejemati_prejeti_prejemati(int VALUE) { if (종류() != VALUE) return false; Položaj++; return true; }
    static void zahteva_VALUE(int VALUE) { if (!sprejeti_sprejemati_prejeti_prejemati(VALUE)) napaka_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Položaj, Word_SMS)) return false; Položaj++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) napaka_VALUE(Word_SMS); }
    static int identifikator_VALUE() {
        int REZULTAT = Položaj;
        if (종류() != 256) napaka_VALUE("identifier required"); else Položaj++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Zaženi = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Zaženi == 토큰길이[REZULTAT];
                for (int 칸 = Zaženi; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != VIR[žeton_položaj[REZULTAT] + 칸 - Zaženi]) 같음 = false;
                if (같음) napaka_VALUE("reserved word cannot be an identifier");
                Zaženi = 수 + 1;
            }
        }
        return REZULTAT;
    }
    static void rezati_VALUE() {
        int 수 = 0;
        while (수 < vir_spremeniti_velikost && !NAPAKA) {
            int VALUE = VIR[수], Zaženi = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < vir_spremeniti_velikost && VIR[수 + 1] == '/') {
                while (수 < vir_spremeniti_velikost && VIR[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < vir_spremeniti_velikost && VIR[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < vir_spremeniti_velikost && !(VIR[수] == '*' && VIR[수 + 1] == '/')) 수++;
                if (수 + 1 >= vir_spremeniti_velikost) { napaka_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (znak_VALUE(VALUE)) { 종류 = 256; while (수 < vir_spremeniti_velikost && 문자이름규칙.이어진글자(VIR[수])) 수++; }
            else if (številka_VALUE(VALUE)) { 종류 = 257; while (수 < vir_spremeniti_velikost && številka_VALUE(VIR[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < vir_spremeniti_velikost && VIR[수] != VALUE && VIR[수] != 10 && VIR[수] != 13) {
                    if (VIR[수] == '\\') 수++;
                    수++;
                }
                if (수 >= vir_spremeniti_velikost || VIR[수] != VALUE) { napaka_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < vir_spremeniti_velikost) {
                    int Naprej_element = VIR[수];
                    if (VALUE == '=' && Naprej_element == '=') 종류 = 300;
                    if (VALUE == '!' && Naprej_element == '=') 종류 = 301;
                    if (VALUE == '<' && Naprej_element == '=') 종류 = 302;
                    if (VALUE == '>' && Naprej_element == '=') 종류 = 303;
                    if (VALUE == '&' && Naprej_element == '&') 종류 = 304;
                    if (VALUE == '|' && Naprej_element == '|') 종류 = 305;
                    if (VALUE == '+' && Naprej_element == '+') 종류 = 306;
                    if (VALUE == '-' && Naprej_element == '-') 종류 = 307;
                    if (VALUE == '+' && Naprej_element == '=') 종류 = 308;
                    if (VALUE == '-' && Naprej_element == '=') 종류 = 309;
                    if (VALUE == '*' && Naprej_element == '=') 종류 = 310;
                    if (VALUE == '/' && Naprej_element == '=') 종류 = 311;
                    if (VALUE == '%' && Naprej_element == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (žeton_COUNT == 토큰종류.length - 1) { napaka_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[žeton_COUNT] = 종류; žeton_položaj[žeton_COUNT] = Zaženi; 토큰길이[žeton_COUNT++] = 수 - Zaženi;
        }
    }
    static void pisati_konstanta_bajt(int VALUE) {
        if (konstanta_spremeniti_velikost == konstanta_VALUE.length) { napaka_VALUE("constant pool too large"); return; }
        konstanta_VALUE[konstanta_spremeniti_velikost++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { pisati_konstanta_bajt(VALUE >> 8); pisati_konstanta_bajt(VALUE); }
    static int register_konstanta(int Zaženi) {
        for (int 수 = 1; 수 < konstanta_COUNT; 수++) {
            int sprednja_VALUE = konstanta_odmik[수], 길이 = (수 + 1 < konstanta_COUNT ? konstanta_odmik[수 + 1] : Zaženi) - sprednja_VALUE;
            if (길이 != konstanta_spremeniti_velikost - Zaženi) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (konstanta_VALUE[sprednja_VALUE + 칸] != konstanta_VALUE[Zaženi + 칸]) 같음 = false;
            if (같음) { konstanta_spremeniti_velikost = Zaženi; return 수; }
        }
        if (konstanta_COUNT == konstanta_odmik.length) { napaka_VALUE("too many constants"); return 0; }
        konstanta_odmik[konstanta_COUNT] = Zaženi;
        return konstanta_COUNT++;
    }
    static void dodati_SMS(int VALUE) {
        if (문자수 == 문자.length) { napaka_VALUE("text too long"); return; }
        문자[문자수++] = VALUE;
    }
    static void dodati_Word(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) dodati_SMS(Word_SMS.charAt(수)); }
    static int znak_konstanta() {
        int Zaženi = konstanta_spremeniti_velikost; pisati_konstanta_bajt(1); 상짧(0);
        for (int 수 = 0; 수 < 문자수; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) pisati_konstanta_bajt(VALUE);
            else if (VALUE < 2048) { pisati_konstanta_bajt(192 | VALUE >> 6); pisati_konstanta_bajt(128 | VALUE & 63); }
            else { pisati_konstanta_bajt(224 | VALUE >> 12); pisati_konstanta_bajt(128 | VALUE >> 6 & 63); pisati_konstanta_bajt(128 | VALUE & 63); }
        }
        if (NAPAKA) return 0;
        int 길이 = konstanta_spremeniti_velikost - Zaženi - 3;
        konstanta_VALUE[Zaženi + 1] = 길이 >> 8; konstanta_VALUE[Zaženi + 2] = 길이 & 255;
        return register_konstanta(Zaženi);
    }
    static int Word_konstanta(String Word_SMS) { 문자수 = 0; dodati_Word(Word_SMS); return znak_konstanta(); }
    static int žeton_konstanta(int žeton_VALUE) {
        문자수 = 0;
        for (int 수 = 0; 수 < 토큰길이[žeton_VALUE]; 수++) dodati_SMS(VIR[žeton_položaj[žeton_VALUE] + 수]);
        return znak_konstanta();
    }
    static int Gradiva(int 종류, int 가, int SECOND_operand) {
        int Zaženi = konstanta_spremeniti_velikost; pisati_konstanta_bajt(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SECOND_operand);
        return register_konstanta(Zaženi);
    }
    static int zunanji_Gradiva(int 종류, String lastnik_VALUE, String Ime, String 서술) {
        int lastnik_identifikator = Gradiva(7, Word_konstanta(lastnik_VALUE), 0);
        int ime_COUNT = Word_konstanta(Ime), oblika_COUNT = Word_konstanta(서술);
        return Gradiva(종류, lastnik_identifikator, Gradiva(12, ime_COUNT, oblika_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_spremeniti_velikost == CODE_VALUE.length) { napaka_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_spremeniti_velikost++] = VALUE & 255;
    }
    static void Ukaz(int VALUE, int Argumenti) { 내보내기(VALUE); 내보내기(Argumenti >> 8); 내보내기(Argumenti); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Zaženi = konstanta_spremeniti_velikost; pisati_konstanta_bajt(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Ukaz(19, register_konstanta(Zaženi));
    }
    static int veja(int Ukaz) { int REZULTAT = CODE_spremeniti_velikost; Ukaz(Ukaz, 0); return REZULTAT; }
    static void Povezava_VALUE(int veja, int cilj_predmet) {
        if (NAPAKA) return;
        int 거리 = cilj_predmet - veja;
        if (거리 < -32768 || 거리 > 32767 || veja < 0 || veja + 2 >= CODE_spremeniti_velikost) { napaka_VALUE("invalid branch"); return; }
        CODE_VALUE[veja + 1] = 거리 >> 8 & 255; CODE_VALUE[veja + 2] = 거리 & 255;
    }
    static void Primerjava_VALUE(int Ukaz) {
        int TRUE_VALUE = veja(Ukaz); 내보내기(3); int 끝 = veja(167);
        Povezava_VALUE(TRUE_VALUE, CODE_spremeniti_velikost); 내보내기(4); Povezava_VALUE(끝, CODE_spremeniti_velikost);
    }
    static int oblika_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (sprejeti_sprejemati_prejeti_prejemati('[')) { zahteva_VALUE(']'); return 4; } return 3; }
        napaka_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Dodaj_oblika(int Tip_VALUE) {
        if (Tip_VALUE == 0) dodati_SMS('V');
        if (Tip_VALUE == 1) dodati_SMS('I');
        if (Tip_VALUE == 2) dodati_SMS('Z');
        if (Tip_VALUE == 3) dodati_Word("Ljava/lang/String;");
        if (Tip_VALUE == 4) dodati_Word("[Ljava/lang/String;");
        if (Tip_VALUE == 5) dodati_SMS('C');
        if (Tip_VALUE == 6) dodati_Word("Ljava/io/FileInputStream;");
        if (Tip_VALUE == 7) dodati_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklaracija. izjema Proces_VALUE_vnos 본문은 gostiti javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("slovenščina");
        if (한국어묶음) { zahteva_VALUE('.'); 말요구("lastno"); zahteva_VALUE('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("izjema") || TAKE_Word("실행예외") || TAKE_Word("V_I_izjema") || TAKE_Word("počakaj_TIMEOUT_izjema") || TAKE_Word("naslov_LOOKUP_izjema") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("neveljaven_argument_izjema") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_Gradiva_izjema") || TAKE_Word("산술예외") || TAKE_Word("stanje_izjema") || TAKE_Word("Tip_pretvorba_izjema") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_napaka") || TAKE_Word("nit_stanje_izjema") || TAKE_Word("대기중단예외")) return;
        napaka_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Položaj, "slovenščina")) 예외이름읽기();
            else {
                말요구("java"); zahteva_VALUE('.'); 말요구("io"); zahteva_VALUE('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) napaka_VALUE("unsupported import");
            }
            zahteva_VALUE(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); Razred_žeton = identifikator_VALUE();
        Razred_konstanta = Gradiva(7, žeton_konstanta(Razred_žeton), 0);
        nadrejen_konstanta = Gradiva(7, Word_konstanta("java/lang/Object"), 0); CODE_konstanta = Word_konstanta("Code"); zahteva_VALUE('{');
        while (!NAPAKA && 종류() != '}') {
            if (metoda_COUNT == 32) { napaka_VALUE("too many methods"); break; }
            int dostop_vnos = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = metoda_COUNT++;
            metoda_dostop[FUNCTION_VALUE] = dostop_vnos | 8;
            metoda_vrni[FUNCTION_VALUE] = oblika_VALUE(); metoda_vnos_ime[FUNCTION_VALUE] = identifikator_VALUE(); zahteva_VALUE('(');
            for (int sprednja_VALUE = 0; sprednja_VALUE < FUNCTION_VALUE; sprednja_VALUE++) if (이름같음(metoda_vnos_ime[sprednja_VALUE], metoda_vnos_ime[FUNCTION_VALUE])) napaka_VALUE("duplicate method (overloading unsupported)");
            while (!NAPAKA && 종류() != ')') {
                int 수 = metoda_argument_COUNT[FUNCTION_VALUE];
                if (수 == 16) { napaka_VALUE("too many parameters"); break; }
                int Tip_VALUE = oblika_VALUE(); if (Tip_VALUE == 0) napaka_VALUE("void parameter");
                metoda_argument_Tip[FUNCTION_VALUE * 16 + 수] = Tip_VALUE; metoda_argument_ime[FUNCTION_VALUE * 16 + 수] = identifikator_VALUE();
                metoda_argument_COUNT[FUNCTION_VALUE]++;
                if (!sprejeti_sprejemati_prejeti_prejemati(',')) break;
            }
            zahteva_VALUE(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!NAPAKA && sprejeti_sprejemati_prejeti_prejemati(','));
            }
            metoda_telo[FUNCTION_VALUE] = Položaj; zahteva_VALUE('{');
            int ugnezdenje_VALUE = 1;
            while (Položaj < žeton_COUNT && ugnezdenje_VALUE > 0) {
                if (종류() == '{') ugnezdenje_VALUE++;
                if (종류() == '}') ugnezdenje_VALUE--;
                Položaj++;
            }
            if (ugnezdenje_VALUE != 0) napaka_VALUE("unclosed method body");
            metoda_končati_klic[FUNCTION_VALUE] = Položaj;
            metoda_ime_konstanta[FUNCTION_VALUE] = žeton_konstanta(metoda_vnos_ime[FUNCTION_VALUE]);
            문자수 = 0; dodati_SMS('(');
            for (int 수 = 0; 수 < metoda_argument_COUNT[FUNCTION_VALUE]; 수++) Dodaj_oblika(metoda_argument_Tip[FUNCTION_VALUE * 16 + 수]);
            dodati_SMS(')'); Dodaj_oblika(metoda_vrni[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = znak_konstanta();
        }
        zahteva_VALUE('}'); if (Položaj != žeton_COUNT) napaka_VALUE("extra input after class");
    }
    static int FIND_lokalen_krajeven(int Ime) {
        for (int 수 = lokalen_krajeven_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokalen_krajeven_ime[수], Ime)) return 수;
        napaka_VALUE("unknown variable"); return 0;
    }
    static int Dodaj_lokalen_krajeven(int Ime, int Tip_VALUE) {
        for (int 수 = 0; 수 < lokalen_krajeven_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokalen_krajeven_ime[수], Ime)) napaka_VALUE("duplicate local variable");
        if (lokalen_krajeven_COUNT == 128) { napaka_VALUE("too many locals"); return 0; }
        lokalen_krajeven_ime[lokalen_krajeven_COUNT] = Ime; lokalen_krajeven_Tip[lokalen_krajeven_COUNT] = Tip_VALUE; 지역깊이[lokalen_krajeven_COUNT] = 깊이;
        return lokalen_krajeven_COUNT++;
    }
    static boolean celo_število_Tip(int Tip_VALUE) { return Tip_VALUE == 1 || Tip_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokalen_krajeven_Tip[수] <= 2 || lokalen_krajeven_Tip[수] == 5 ? 21 : 25); 내보내기(수); }
    static void pisati_lokalen_krajeven(int 수) { 내보내기(lokalen_krajeven_Tip[수] <= 2 || lokalen_krajeven_Tip[수] == 5 ? 54 : 58); 내보내기(수); }
    static void 형확인(int dejanski_podatki, int 기대) { if (dejanski_podatki != 기대 && !(dejanski_podatki == 5 && 기대 == 1)) napaka_VALUE("type mismatch"); }
    static void 문자읽기(int žeton_VALUE) {
        문자수 = 0; int Zaženi = žeton_položaj[žeton_VALUE] + 1, 끝 = žeton_položaj[žeton_VALUE] + 토큰길이[žeton_VALUE] - 1;
        while (Zaženi < 끝 && !NAPAKA) {
            int VALUE = VIR[Zaženi++];
            if (VALUE == '\\') {
                if (Zaženi == 끝) { napaka_VALUE("invalid escape"); break; }
                VALUE = VIR[Zaženi++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') napaka_VALUE("unsupported escape");
            }
            dodati_SMS(VALUE);
        }
    }
    static int razčlenjevati_celo_število(int žeton_VALUE, boolean 음수) {
        if (토큰길이[žeton_VALUE] > 1 && VIR[žeton_položaj[žeton_VALUE]] == '0') napaka_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < 토큰길이[žeton_VALUE]; 수++) {
            int številka_element = VIR[žeton_položaj[žeton_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && številka_element > (음수 ? 8 : 7)) napaka_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - številka_element;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int Tip_VALUE = oblika_VALUE();
            if (Tip_VALUE != 6 && Tip_VALUE != 7) { napaka_VALUE("only file streams supported by new in source"); return 0; }
            String lastnik_VALUE = Tip_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Ukaz(187, Gradiva(7, Word_konstanta(lastnik_VALUE), 0)); 내보내기(89);
            zahteva_VALUE('('); 형확인(izraz_VALUE(), 3); boolean 이어 = false;
            if (sprejeti_sprejemati_prejeti_prejemati(',')) { if (Tip_VALUE != 7) napaka_VALUE("input stream constructor arguments"); 형확인(izraz_VALUE(), 2); 이어 = true; }
            zahteva_VALUE(')');
            Ukaz(183, zunanji_Gradiva(10, lastnik_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return Tip_VALUE;
        }
        if (sprejeti_sprejemati_prejeti_prejemati('(')) { int Tip_VALUE = izraz_VALUE(); zahteva_VALUE(')'); return Tip_VALUE; }
        if (종류() == 257) { 수상수(razčlenjevati_celo_število(Položaj++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Položaj++); Ukaz(19, Gradiva(8, znak_konstanta(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Položaj++); if (문자수 != 1) napaka_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("slovenščina")) {
            zahteva_VALUE('.'); 말요구("lastno"); zahteva_VALUE('.');
            String lastnik_VALUE = "", metoda_VALUE = "", 서술 = ""; int 가 = 0, SECOND_operand = 0, 다 = 0, 라 = 0, 마 = 0, REZULTAT = 0;
            if (TAKE_Word("Izpis")) {
                lastnik_VALUE = "slovenščina/lastno/Izpis"; zahteva_VALUE('.');
                if (TAKE_Word("pisati_linija")) { metoda_VALUE = "pisati_linija"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Pisanje")) { metoda_VALUE = "Pisanje"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { metoda_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else napaka_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                lastnik_VALUE = "slovenščina/lastno/문자"; zahteva_VALUE('.'); 가 = 3;
                if (TAKE_Word("길이")) { metoda_VALUE = "길이"; 서술 = "(Ljava/lang/String;)I"; REZULTAT = 1; }
                else if (TAKE_Word("koda_znaka_COUNT")) { metoda_VALUE = "koda_znaka_COUNT"; 서술 = "(Ljava/lang/String;)I"; REZULTAT = 1; }
                else if (TAKE_Word("razčlenjevati_celo_število")) { metoda_VALUE = "razčlenjevati_celo_število"; 서술 = "(Ljava/lang/String;)I"; REZULTAT = 1; }
                else if (TAKE_Word("pisati_celo_število_VALUE")) { metoda_VALUE = "pisati_celo_število_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; REZULTAT = 3; }
                else if (TAKE_Word("같음")) { metoda_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECOND_operand = 3; REZULTAT = 2; }
                else if (TAKE_Word("prilepiti_SMS")) { metoda_VALUE = "prilepiti_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECOND_operand = 3; REZULTAT = 3; }
                else if (TAKE_Word("rezati_VALUE")) { metoda_VALUE = "rezati_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECOND_operand = 1; 다 = 1; REZULTAT = 3; }
                else napaka_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Datoteka")) {
                lastnik_VALUE = "slovenščina/lastno/Datoteka"; zahteva_VALUE('.'); 가 = 3;
                if (TAKE_Word("Branje")) { metoda_VALUE = "Branje"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; REZULTAT = 3; }
                else if (TAKE_Word("Pisanje")) { metoda_VALUE = "Pisanje"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECOND_operand = 3; }
                else napaka_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                lastnik_VALUE = "slovenščina/lastno/화면"; zahteva_VALUE('.');
                if (TAKE_Word("너비")) { metoda_VALUE = "너비"; 서술 = "()I"; REZULTAT = 1; }
                else if (TAKE_Word("višina_VALUE")) { metoda_VALUE = "višina_VALUE"; 서술 = "()I"; REZULTAT = 1; }
                else if (TAKE_Word("pravokotnik")) { metoda_VALUE = "pravokotnik"; 서술 = "(IIIII)V"; 가 = 1; SECOND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("izbrisati_vnos")) { metoda_VALUE = "izbrisati_vnos"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metoda_VALUE = "기다리기"; 서술 = "()V"; }
                else napaka_VALUE("unknown Korean framebuffer method");
            } else napaka_VALUE("unsupported Korean library class");
            zahteva_VALUE('('); if (가 != 0) 형확인(izraz_VALUE(), 가);
            if (SECOND_operand != 0) { zahteva_VALUE(','); 형확인(izraz_VALUE(), SECOND_operand); }
            if (다 != 0) { zahteva_VALUE(','); 형확인(izraz_VALUE(), 다); }
            if (라 != 0) { zahteva_VALUE(','); 형확인(izraz_VALUE(), 라); }
            if (마 != 0) { zahteva_VALUE(','); 형확인(izraz_VALUE(), 마); }
            zahteva_VALUE(')'); Ukaz(184, zunanji_Gradiva(10, lastnik_VALUE, metoda_VALUE, 서술)); return REZULTAT;
        }
        if (TAKE_Word("Integer")) {
            zahteva_VALUE('.'); 말요구("parseInt"); zahteva_VALUE('('); 형확인(izraz_VALUE(), 3); zahteva_VALUE(')');
            Ukaz(184, zunanji_Gradiva(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Ime = identifikator_VALUE();
        if (sprejeti_sprejemati_prejeti_prejemati('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < metoda_COUNT; 수++) if (이름같음(Ime, metoda_vnos_ime[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { napaka_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!NAPAKA && 종류() != ')') {
                if (수 >= metoda_argument_COUNT[FUNCTION_VALUE]) { napaka_VALUE("too many arguments"); break; }
                형확인(izraz_VALUE(), metoda_argument_Tip[FUNCTION_VALUE * 16 + 수++]); if (!sprejeti_sprejemati_prejeti_prejemati(',')) break;
            }
            zahteva_VALUE(')'); if (수 != metoda_argument_COUNT[FUNCTION_VALUE]) napaka_VALUE("argument count mismatch");
            Ukaz(184, Gradiva(10, Razred_konstanta, Gradiva(12, metoda_ime_konstanta[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return metoda_vrni[FUNCTION_VALUE];
        }
        int lokalen_krajeven_obseg = FIND_lokalen_krajeven(Ime), Tip_VALUE = lokalen_krajeven_Tip[lokalen_krajeven_obseg]; 지역읽기(lokalen_krajeven_obseg);
        while (!NAPAKA) {
            if (sprejeti_sprejemati_prejeti_prejemati('[')) { 형확인(Tip_VALUE, 4); 형확인(izraz_VALUE(), 1); zahteva_VALUE(']'); 내보내기(50); Tip_VALUE = 3; }
            else if (sprejeti_sprejemati_prejeti_prejemati('.')) {
                if (Tip_VALUE == 6 || Tip_VALUE == 7) {
                    String lastnik_VALUE = Tip_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { zahteva_VALUE('('); zahteva_VALUE(')'); Ukaz(182, zunanji_Gradiva(10, lastnik_VALUE, "close", "()V")); Tip_VALUE = 0; }
                    else if (Tip_VALUE == 6 && TAKE_Word("read")) { zahteva_VALUE('('); zahteva_VALUE(')'); Ukaz(182, zunanji_Gradiva(10, lastnik_VALUE, "read", "()I")); Tip_VALUE = 1; }
                    else if (Tip_VALUE == 7 && TAKE_Word("write")) { zahteva_VALUE('('); 형확인(izraz_VALUE(), 1); zahteva_VALUE(')'); Ukaz(182, zunanji_Gradiva(10, lastnik_VALUE, "write", "(I)V")); Tip_VALUE = 0; }
                    else { napaka_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (Tip_VALUE == 4) { 내보내기(190); Tip_VALUE = 1; }
                else { 형확인(Tip_VALUE, 3); zahteva_VALUE('('); zahteva_VALUE(')'); Ukaz(182, zunanji_Gradiva(10, "java/lang/String", "length", "()I")); Tip_VALUE = 1; }
            } else break;
        }
        return Tip_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { napaka_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int Tip_VALUE;
        if (sprejeti_sprejemati_prejeti_prejemati('!')) { 형확인(단항(), 2); Primerjava_VALUE(153); Tip_VALUE = 2; }
        else if (sprejeti_sprejemati_prejeti_prejemati('-')) {
            if (종류() == 257) 수상수(razčlenjevati_celo_število(Položaj++, true));
            else { 형확인(단항(), 1); 내보내기(116); }
            Tip_VALUE = 1;
        } else if (sprejeti_sprejemati_prejeti_prejemati('+')) { 형확인(단항(), 1); Tip_VALUE = 1; }
        else Tip_VALUE = 기본식();
        식깊이--; return Tip_VALUE;
    }
    static int 곱식() {
        int Tip_VALUE = 단항();
        while (!NAPAKA && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodiranje_VALUE = 종류(); Položaj++; 형확인(Tip_VALUE, 1); 형확인(단항(), 1);
            내보내기(kodiranje_VALUE == '*' ? 104 : kodiranje_VALUE == '/' ? 108 : 112); Tip_VALUE = 1;
        }
        return Tip_VALUE;
    }
    static int 합식() {
        int Tip_VALUE = 곱식();
        while (!NAPAKA && (종류() == '+' || 종류() == '-')) {
            int kodiranje_VALUE = 종류(); Položaj++; int 경계 = CODE_spremeniti_velikost, ZAJ_VALUE_Tip = 곱식();
            if (kodiranje_VALUE == '+' && (Tip_VALUE == 3 || ZAJ_VALUE_Tip == 3)) { 결합(경계, Tip_VALUE, ZAJ_VALUE_Tip); Tip_VALUE = 3; }
            else { 형확인(Tip_VALUE, 1); 형확인(ZAJ_VALUE_Tip, 1); 내보내기(kodiranje_VALUE == '+' ? 96 : 100); Tip_VALUE = 1; }
        }
        return Tip_VALUE;
    }
    static int 붙임참조(int Tip_VALUE) {
        if (Tip_VALUE != 1 && Tip_VALUE != 2 && Tip_VALUE != 3 && Tip_VALUE != 5) napaka_VALUE("unsupported concatenation type");
        return zunanji_Gradiva(10, "java/lang/StringBuilder", "append", Tip_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : Tip_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : Tip_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int sprednja_VALUE_Tip, int ZAJ_VALUE_Tip) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 ustvariti 코드를 삽입한다.
        // RIGHT izraz_VALUE 내부의 enakovreden_VALUE veja 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_spremeniti_velikost;
        Ukaz(187, Gradiva(7, Word_konstanta("java/lang/StringBuilder"), 0)); 내보내기(89);
        Ukaz(183, zunanji_Gradiva(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Ukaz(182, 붙임참조(sprednja_VALUE_Tip));
        if (NAPAKA) return;
        int 길이 = CODE_spremeniti_velikost - 끝;
        for (int 수 = 0; 수 < 길이; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + 길이] = CODE_VALUE[수];
        for (int 수 = 0; 수 < 길이; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        Ukaz(182, 붙임참조(ZAJ_VALUE_Tip)); Ukaz(182, zunanji_Gradiva(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Primerjava_izraz() {
        int Tip_VALUE = 합식();
        while (!NAPAKA && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodiranje_VALUE = 종류(); Položaj++; 형확인(Tip_VALUE, 1); 형확인(합식(), 1);
            Primerjava_VALUE(kodiranje_VALUE == '<' ? 161 : kodiranje_VALUE == '>' ? 163 : kodiranje_VALUE == 302 ? 164 : 162); Tip_VALUE = 2;
        }
        return Tip_VALUE;
    }
    static int 동등식() {
        int Tip_VALUE = Primerjava_izraz();
        while (!NAPAKA && (종류() == 300 || 종류() == 301)) {
            int kodiranje_VALUE = 종류(); Položaj++; int ZAJ_VALUE_Tip = Primerjava_izraz();
            if (Tip_VALUE == 0 || ZAJ_VALUE_Tip == 0) napaka_VALUE("void expression");
            if (!(celo_število_Tip(Tip_VALUE) && celo_število_Tip(ZAJ_VALUE_Tip))) 형확인(ZAJ_VALUE_Tip, Tip_VALUE);
            Primerjava_VALUE((Tip_VALUE <= 2 || Tip_VALUE == 5 ? 159 : 165) + (kodiranje_VALUE == 301 ? 1 : 0)); Tip_VALUE = 2;
        }
        return Tip_VALUE;
    }
    static int logični_IN() {
        int Tip_VALUE = 동등식();
        while (!NAPAKA && sprejeti_sprejemati_prejeti_prejemati(304)) {
            형확인(Tip_VALUE, 2); int 가 = veja(153); 형확인(동등식(), 2); int SECOND_operand = veja(153);
            내보내기(4); int 끝 = veja(167); Povezava_VALUE(가, CODE_spremeniti_velikost); Povezava_VALUE(SECOND_operand, CODE_spremeniti_velikost); 내보내기(3); Povezava_VALUE(끝, CODE_spremeniti_velikost); Tip_VALUE = 2;
        }
        return Tip_VALUE;
    }
    static int izraz_VALUE() {
        int Tip_VALUE = logični_IN();
        while (!NAPAKA && sprejeti_sprejemati_prejeti_prejemati(305)) {
            형확인(Tip_VALUE, 2); int 가 = veja(154); 형확인(logični_IN(), 2); int SECOND_operand = veja(154);
            내보내기(3); int 끝 = veja(167); Povezava_VALUE(가, CODE_spremeniti_velikost); Povezava_VALUE(SECOND_operand, CODE_spremeniti_velikost); 내보내기(4); Povezava_VALUE(끝, CODE_spremeniti_velikost); Tip_VALUE = 2;
        }
        return Tip_VALUE;
    }
    static void dodelitev_VALUE(boolean Dovoli_deklaracija) {
        if (Word_VALUE(Položaj, "int") || Word_VALUE(Položaj, "boolean") || Word_VALUE(Položaj, "String") || Word_VALUE(Položaj, "char")
            || Word_VALUE(Položaj, "FileInputStream") || Word_VALUE(Položaj, "FileOutputStream")) {
            if (!Dovoli_deklaracija) napaka_VALUE("declaration not allowed here");
            int Tip_VALUE = oblika_VALUE(), Ime = identifikator_VALUE(); zahteva_VALUE('='); 형확인(izraz_VALUE(), Tip_VALUE);
            pisati_lokalen_krajeven(Dodaj_lokalen_krajeven(Ime, Tip_VALUE)); return;
        }
        int Ime = identifikator_VALUE(), lokalen_krajeven_obseg = FIND_lokalen_krajeven(Ime);
        if (sprejeti_sprejemati_prejeti_prejemati('=')) { 형확인(izraz_VALUE(), lokalen_krajeven_Tip[lokalen_krajeven_obseg]); pisati_lokalen_krajeven(lokalen_krajeven_obseg); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodiranje_VALUE = 종류(); Položaj++; 지역읽기(lokalen_krajeven_obseg); int 경계 = CODE_spremeniti_velikost, ZAJ_VALUE_Tip = izraz_VALUE();
            if (kodiranje_VALUE == 308 && lokalen_krajeven_Tip[lokalen_krajeven_obseg] == 3) 결합(경계, 3, ZAJ_VALUE_Tip);
            else {
                형확인(lokalen_krajeven_Tip[lokalen_krajeven_obseg], 1); 형확인(ZAJ_VALUE_Tip, 1);
                내보내기(kodiranje_VALUE == 308 ? 96 : kodiranje_VALUE == 309 ? 100 : kodiranje_VALUE == 310 ? 104 : kodiranje_VALUE == 311 ? 108 : 112);
                if (lokalen_krajeven_Tip[lokalen_krajeven_obseg] == 5) 내보내기(146);
            }
            pisati_lokalen_krajeven(lokalen_krajeven_obseg);
        }
        else if (종류() == 306 || 종류() == 307) {
            형확인(lokalen_krajeven_Tip[lokalen_krajeven_obseg], 1); 내보내기(132); 내보내기(lokalen_krajeven_obseg); 내보내기(종류() == 306 ? 1 : 255); Položaj++;
            if (lokalen_krajeven_Tip[lokalen_krajeven_obseg] == 5) { 지역읽기(lokalen_krajeven_obseg); 내보내기(146); pisati_lokalen_krajeven(lokalen_krajeven_obseg); }
        } else napaka_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); zahteva_VALUE('.'); 말요구("out"); zahteva_VALUE('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); zahteva_VALUE('(');
        Ukaz(178, zunanji_Gradiva(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean prazen_argument = 종류() == ')';
        int Tip_VALUE = prazen_argument ? 0 : izraz_VALUE(); zahteva_VALUE(')'); zahteva_VALUE(';');
        String 서술 = Tip_VALUE == 0 ? "()V" : Tip_VALUE == 1 ? "(I)V" : Tip_VALUE == 2 ? "(Z)V" : Tip_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (Tip_VALUE == 4 || Tip_VALUE >= 6 || Tip_VALUE == 0 && (!줄바꿈 || !prazen_argument)) napaka_VALUE("unsupported print argument");
        Ukaz(182, zunanji_Gradiva(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean izjava_VALUE() {
        if (NAPAKA) return false;
        if (깊이 > 32) { napaka_VALUE("statement nesting too deep"); return false; }
        if (sprejeti_sprejemati_prejeti_prejemati('{')) {
            깊이++; boolean vrni_KR = false;
            while (!NAPAKA && 종류() != '}') { if (vrni_KR) napaka_VALUE("unreachable statement"); vrni_KR = izjava_VALUE(); }
            zahteva_VALUE('}'); for (int 수 = 0; 수 < lokalen_krajeven_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return vrni_KR;
        }
        if (sprejeti_sprejemati_prejeti_prejemati(';')) return false;
        if (TAKE_Word("return")) {
            int Tip_VALUE = 종류() == ';' ? 0 : izraz_VALUE(); 형확인(Tip_VALUE, metoda_vrni[sprotno_metoda]); zahteva_VALUE(';');
            내보내기(Tip_VALUE == 0 ? 177 : Tip_VALUE <= 2 || Tip_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            zahteva_VALUE('('); 형확인(izraz_VALUE(), 2); zahteva_VALUE(')'); int FALSE_VALUE = veja(153);
            깊이++; boolean 가 = nadzor_izjava(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = veja(167); Povezava_VALUE(FALSE_VALUE, CODE_spremeniti_velikost); 깊이++; boolean SECOND_operand = nadzor_izjava(); 깊이--; Povezava_VALUE(끝, CODE_spremeniti_velikost); return 가 && SECOND_operand; }
            Povezava_VALUE(FALSE_VALUE, CODE_spremeniti_velikost); return false;
        }
        if (TAKE_Word("while")) {
            int Zaženi = CODE_spremeniti_velikost; zahteva_VALUE('('); 형확인(izraz_VALUE(), 2); zahteva_VALUE(')'); int 끝 = veja(153);
            깊이++; nadzor_izjava(); 깊이--; Povezava_VALUE(veja(167), Zaženi); Povezava_VALUE(끝, CODE_spremeniti_velikost); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; zahteva_VALUE('('); if (종류() != ';') dodelitev_VALUE(true); zahteva_VALUE(';');
            int pogoj = CODE_spremeniti_velikost; if (종류() == ';') 내보내기(4); else 형확인(izraz_VALUE(), 2); zahteva_VALUE(';');
            int 끝 = veja(153), telo_besedila = veja(167), osvežiti = CODE_spremeniti_velikost;
            if (종류() != ')') dodelitev_VALUE(false); zahteva_VALUE(')'); Povezava_VALUE(veja(167), pogoj); Povezava_VALUE(telo_besedila, CODE_spremeniti_velikost);
            nadzor_izjava(); Povezava_VALUE(veja(167), osvežiti); Povezava_VALUE(끝, CODE_spremeniti_velikost);
            for (int 수 = 0; 수 < lokalen_krajeven_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Položaj, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Položaj + 1 < žeton_COUNT && (토큰종류[Položaj + 1] == '(' || 토큰종류[Položaj + 1] == '.')) {
            int Tip_VALUE = izraz_VALUE(); if (Tip_VALUE != 0) 내보내기(87); zahteva_VALUE(';'); return false;
        }
        dodelitev_VALUE(true); zahteva_VALUE(';'); return false;
    }
    static boolean nadzor_izjava() {
        if (Word_VALUE(Položaj, "int") || Word_VALUE(Položaj, "boolean") || Word_VALUE(Položaj, "char") || Word_VALUE(Položaj, "String")
            || Word_VALUE(Položaj, "FileInputStream") || Word_VALUE(Položaj, "FileOutputStream")) napaka_VALUE("local declaration requires braces");
        return izjava_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == Izpis.length) napaka_VALUE("class file too large"); else Izpis[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void pisati_Razred() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstanta_COUNT);
        for (int 수 = 0; 수 < konstanta_spremeniti_velikost; 수++) 출바(konstanta_VALUE[수]);
        출짧(0x21); 출짧(Razred_konstanta); 출짧(nadrejen_konstanta); 출짧(0); 출짧(0); 출짧(metoda_COUNT);
        for (int 수 = 0; 수 < metoda_COUNT; 수++) {
            출짧(metoda_dostop[수]); 출짧(metoda_ime_konstanta[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_konstanta);
            출정(12 + 함수길이[수]); 출짧(128); 출짧(함수지역[수]); 출정(함수길이[수]);
            for (int 칸 = 0; 칸 < 함수길이[수]; 칸++) 출바(CODE_VALUE[metoda_CODE[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Zaženi() {
        if (uporabnik.인수개수() == 1 && 자바도구.같음(uporabnik.Argumenti(0), "-version")) {
            uporabnik.Pisanje("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (uporabnik.인수개수() != 1) { uporabnik.Pisanje("Usage: javac FILE.java\n"); return 2; }
        int ime_spremeniti_velikost = 자바도구.Ime(ime_datoteke_SMS, uporabnik.Argumenti(0));
        if (ime_spremeniti_velikost < 6 || ime_spremeniti_velikost > 62 || ime_datoteke_SMS[ime_spremeniti_velikost - 5] != '.' || ime_datoteke_SMS[ime_spremeniti_velikost - 4] != 'j'
            || ime_datoteke_SMS[ime_spremeniti_velikost - 3] != 'a' || ime_datoteke_SMS[ime_spremeniti_velikost - 2] != 'v' || ime_datoteke_SMS[ime_spremeniti_velikost - 1] != 'a') {
            uporabnik.Pisanje("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        vir_spremeniti_velikost = uporabnik.파일읽기(ime_datoteke_SMS, VIR);
        if (vir_spremeniti_velikost < 0) { uporabnik.Pisanje("javac: cannot read source: "); 자바도구.수쓰기(vir_spremeniti_velikost); uporabnik.pisati_znak_VALUE(10); return 1; }
        vir_spremeniti_velikost = 자바도구.원문해독(VIR, vir_spremeniti_velikost);
        if (vir_spremeniti_velikost < 0) { uporabnik.Pisanje("javac error: invalid UTF-8 source\n"); return 1; }
        rezati_VALUE(); if (!NAPAKA) 선언읽기();
        if (!NAPAKA) {
            if (토큰길이[Razred_žeton] != ime_spremeniti_velikost - 5) napaka_VALUE("class name must match file name");
            for (int 수 = 0; 수 < ime_spremeniti_velikost - 5; 수++) if (VIR[žeton_položaj[Razred_žeton] + 수] != ime_datoteke_SMS[수]) napaka_VALUE("class name must match file name");
        }
        for (sprotno_metoda = 0; sprotno_metoda < metoda_COUNT && !NAPAKA; sprotno_metoda++) {
            Položaj = metoda_telo[sprotno_metoda]; metoda_CODE[sprotno_metoda] = CODE_spremeniti_velikost; lokalen_krajeven_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metoda_argument_COUNT[sprotno_metoda]; 수++) Dodaj_lokalen_krajeven(metoda_argument_ime[sprotno_metoda * 16 + 수], metoda_argument_Tip[sprotno_metoda * 16 + 수]);
            boolean vrni_KR = izjava_VALUE();
            if (!vrni_KR && metoda_vrni[sprotno_metoda] != 0) napaka_VALUE("missing return");
            // veja 뒤의 합류 지점은 반드시 dejanski_podatki 명령이어야 한다 (버전 49 검증기).
            if (metoda_vrni[sprotno_metoda] == 0) 내보내기(177);
            else { boolean celo_število = metoda_vrni[sprotno_metoda] <= 2 || metoda_vrni[sprotno_metoda] == 5; 내보내기(celo_število ? 3 : 1); 내보내기(celo_število ? 172 : 176); }
            if (Položaj != metoda_končati_klic[sprotno_metoda]) napaka_VALUE("invalid method body");
            함수지역[sprotno_metoda] = lokalen_krajeven_COUNT; 함수길이[sprotno_metoda] = CODE_spremeniti_velikost - metoda_CODE[sprotno_metoda];
        }
        if (NAPAKA) return 1;
        pisati_Razred(); if (NAPAKA) return 1;
        ime_datoteke_SMS[ime_spremeniti_velikost - 4] = 'c'; ime_datoteke_SMS[ime_spremeniti_velikost - 3] = 'l'; ime_datoteke_SMS[ime_spremeniti_velikost - 2] = 'a';
        ime_datoteke_SMS[ime_spremeniti_velikost - 1] = 's'; ime_datoteke_SMS[ime_spremeniti_velikost] = 's'; ime_datoteke_SMS[ime_spremeniti_velikost + 1] = 0;
        int REZULTAT = uporabnik.pisati_Datoteka(ime_datoteke_SMS, Izpis, 출력크기);
        if (REZULTAT < 0) { uporabnik.Pisanje("javac: cannot save class: "); 자바도구.수쓰기(REZULTAT); uporabnik.pisati_znak_VALUE(10); return 1; }
        uporabnik.Pisanje("Compiled: "); for (int 수 = 0; ime_datoteke_SMS[수] != 0; 수++) uporabnik.pisati_znak_VALUE(ime_datoteke_SMS[수]);
        uporabnik.Pisanje(" (JVM class version 49)\n"); return 0;
    }
}
