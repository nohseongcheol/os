// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java zdroj_strom -> 표준 버전 49 class kompilátor. */
public final class 자바컴파일러 {
    static int[] ZDROJ = new int[16384], Výstup = new int[16384], kód_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_pozícia = new int[2048], token_dĺžka = new int[2048];
    static int[] konštanta_VALUE = new int[4096], konštanta_Posun = new int[512];
    static int[] 문자 = new int[512], názov_súboru_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int zdroj_zmeniť_veľkosť, token_COUNT, Pozícia, kód_zmeniť_veľkosť, konštanta_zmeniť_veľkosť, konštanta_COUNT = 1, 출력크기, znak_dĺžka;
    static boolean chyba;
    static int lekcia_token, lekcia_konštanta, nadradený_konštanta, kód_konštanta;
    static int[] metóda_položka_názov = new int[32], metóda_vrátiť = new int[32], metóda_argument_COUNT = new int[32];
    static int[] metóda_argument_názov = new int[512], metóda_argument_Typ = new int[512];
    static int[] metóda_telo_správy = new int[32], metóda_ukončiť_hovor = new int[32], metóda_kód = new int[32];
    static int[] metóda_dĺžka = new int[32], 함수지역 = new int[32], metóda_názov_konštanta = new int[32], 함수서술 = new int[32];
    static int[] metóda_prístup = new int[32];
    static int metóda_COUNT, v_termíne_splatnosti_metóda, miestny_COUNT, 깊이, 식깊이;
    static int[] miestny_názov = new int[128], miestny_Typ = new int[128], 지역깊이 = new int[128];

    static void zlyhanie_VALUE(String 이유) {
        if (!chyba) {
            používateľ.Zápis("javac error: "); používateľ.Zápis(이유);
            používateľ.Zápis(" at line ");
            int riadok = 1, 끝 = Pozícia < token_COUNT ? token_pozícia[Pozícia] : zdroj_zmeniť_veľkosť;
            for (int 수 = 0; 수 < 끝; 수++) if (ZDROJ[수] == 10) riadok++;
            자바도구.수쓰기(riadok); používateľ.zapísať_znak_VALUE(10);
        }
        chyba = true;
    }
    static boolean znak_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean číslica_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int SECOND_operand) {
        if (가 < 0 || SECOND_operand < 0 || 가 >= token_COUNT || SECOND_operand >= token_COUNT || token_dĺžka[가] != token_dĺžka[SECOND_operand]) return false;
        for (int 수 = 0; 수 < token_dĺžka[가]; 수++) if (ZDROJ[token_pozícia[가] + 수] != ZDROJ[token_pozícia[SECOND_operand] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int token_VALUE, String Word_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || token_dĺžka[token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (ZDROJ[token_pozícia[token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Pozícia < token_COUNT ? 토큰종류[Pozícia] : 0; }
    static boolean dostať(int VALUE) { if (종류() != VALUE) return false; Pozícia++; return true; }
    static void požiadavka_VALUE(int VALUE) { if (!dostať(VALUE)) zlyhanie_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Pozícia, Word_SMS)) return false; Pozícia++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) zlyhanie_VALUE(Word_SMS); }
    static int identifikátor_VALUE() {
        int KR = Pozícia;
        if (종류() != 256) zlyhanie_VALUE("identifier required"); else Pozícia++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Spustiť_2 = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Spustiť_2 == token_dĺžka[KR];
                for (int 칸 = Spustiť_2; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != ZDROJ[token_pozícia[KR] + 칸 - Spustiť_2]) 같음 = false;
                if (같음) zlyhanie_VALUE("reserved word cannot be an identifier");
                Spustiť_2 = 수 + 1;
            }
        }
        return KR;
    }
    static void strihať_VALUE() {
        int 수 = 0;
        while (수 < zdroj_zmeniť_veľkosť && !chyba) {
            int VALUE = ZDROJ[수], Spustiť_2 = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < zdroj_zmeniť_veľkosť && ZDROJ[수 + 1] == '/') {
                while (수 < zdroj_zmeniť_veľkosť && ZDROJ[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < zdroj_zmeniť_veľkosť && ZDROJ[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < zdroj_zmeniť_veľkosť && !(ZDROJ[수] == '*' && ZDROJ[수 + 1] == '/')) 수++;
                if (수 + 1 >= zdroj_zmeniť_veľkosť) { zlyhanie_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (znak_VALUE(VALUE)) { 종류 = 256; while (수 < zdroj_zmeniť_veľkosť && 문자이름규칙.이어진글자(ZDROJ[수])) 수++; }
            else if (číslica_VALUE(VALUE)) { 종류 = 257; while (수 < zdroj_zmeniť_veľkosť && číslica_VALUE(ZDROJ[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < zdroj_zmeniť_veľkosť && ZDROJ[수] != VALUE && ZDROJ[수] != 10 && ZDROJ[수] != 13) {
                    if (ZDROJ[수] == '\\') 수++;
                    수++;
                }
                if (수 >= zdroj_zmeniť_veľkosť || ZDROJ[수] != VALUE) { zlyhanie_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < zdroj_zmeniť_veľkosť) {
                    int Ďalej_položka = ZDROJ[수];
                    if (VALUE == '=' && Ďalej_položka == '=') 종류 = 300;
                    if (VALUE == '!' && Ďalej_položka == '=') 종류 = 301;
                    if (VALUE == '<' && Ďalej_položka == '=') 종류 = 302;
                    if (VALUE == '>' && Ďalej_položka == '=') 종류 = 303;
                    if (VALUE == '&' && Ďalej_položka == '&') 종류 = 304;
                    if (VALUE == '|' && Ďalej_položka == '|') 종류 = 305;
                    if (VALUE == '+' && Ďalej_položka == '+') 종류 = 306;
                    if (VALUE == '-' && Ďalej_položka == '-') 종류 = 307;
                    if (VALUE == '+' && Ďalej_položka == '=') 종류 = 308;
                    if (VALUE == '-' && Ďalej_položka == '=') 종류 = 309;
                    if (VALUE == '*' && Ďalej_položka == '=') 종류 = 310;
                    if (VALUE == '/' && Ďalej_položka == '=') 종류 = 311;
                    if (VALUE == '%' && Ďalej_položka == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_COUNT == 토큰종류.length - 1) { zlyhanie_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_pozícia[token_COUNT] = Spustiť_2; token_dĺžka[token_COUNT++] = 수 - Spustiť_2;
        }
    }
    static void zapísať_konštanta_Byte(int VALUE) {
        if (konštanta_zmeniť_veľkosť == konštanta_VALUE.length) { zlyhanie_VALUE("constant pool too large"); return; }
        konštanta_VALUE[konštanta_zmeniť_veľkosť++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { zapísať_konštanta_Byte(VALUE >> 8); zapísať_konštanta_Byte(VALUE); }
    static int register_konštanta(int Spustiť_2) {
        for (int 수 = 1; 수 < konštanta_COUNT; 수++) {
            int predný_VALUE = konštanta_Posun[수], dĺžka_VALUE = (수 + 1 < konštanta_COUNT ? konštanta_Posun[수 + 1] : Spustiť_2) - predný_VALUE;
            if (dĺžka_VALUE != konštanta_zmeniť_veľkosť - Spustiť_2) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < dĺžka_VALUE; 칸++) if (konštanta_VALUE[predný_VALUE + 칸] != konštanta_VALUE[Spustiť_2 + 칸]) 같음 = false;
            if (같음) { konštanta_zmeniť_veľkosť = Spustiť_2; return 수; }
        }
        if (konštanta_COUNT == konštanta_Posun.length) { zlyhanie_VALUE("too many constants"); return 0; }
        konštanta_Posun[konštanta_COUNT] = Spustiť_2;
        return konštanta_COUNT++;
    }
    static void Pripojiť_SMS(int VALUE) {
        if (znak_dĺžka == 문자.length) { zlyhanie_VALUE("text too long"); return; }
        문자[znak_dĺžka++] = VALUE;
    }
    static void Pripojiť_Word(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) Pripojiť_SMS(Word_SMS.charAt(수)); }
    static int znak_konštanta() {
        int Spustiť_2 = konštanta_zmeniť_veľkosť; zapísať_konštanta_Byte(1); 상짧(0);
        for (int 수 = 0; 수 < znak_dĺžka; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) zapísať_konštanta_Byte(VALUE);
            else if (VALUE < 2048) { zapísať_konštanta_Byte(192 | VALUE >> 6); zapísať_konštanta_Byte(128 | VALUE & 63); }
            else { zapísať_konštanta_Byte(224 | VALUE >> 12); zapísať_konštanta_Byte(128 | VALUE >> 6 & 63); zapísať_konštanta_Byte(128 | VALUE & 63); }
        }
        if (chyba) return 0;
        int dĺžka_VALUE = konštanta_zmeniť_veľkosť - Spustiť_2 - 3;
        konštanta_VALUE[Spustiť_2 + 1] = dĺžka_VALUE >> 8; konštanta_VALUE[Spustiť_2 + 2] = dĺžka_VALUE & 255;
        return register_konštanta(Spustiť_2);
    }
    static int Word_konštanta(String Word_SMS) { znak_dĺžka = 0; Pripojiť_Word(Word_SMS); return znak_konštanta(); }
    static int token_konštanta(int token_VALUE) {
        znak_dĺžka = 0;
        for (int 수 = 0; 수 < token_dĺžka[token_VALUE]; 수++) Pripojiť_SMS(ZDROJ[token_pozícia[token_VALUE] + 수]);
        return znak_konštanta();
    }
    static int zdroj(int 종류, int 가, int SECOND_operand) {
        int Spustiť_2 = konštanta_zmeniť_veľkosť; zapísať_konštanta_Byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SECOND_operand);
        return register_konštanta(Spustiť_2);
    }
    static int externý_zdroj(int 종류, String vlastník_VALUE, String Názov, String 서술) {
        int vlastník_identifikátor = zdroj(7, Word_konštanta(vlastník_VALUE), 0);
        int názov_COUNT = Word_konštanta(Názov), formát_COUNT = Word_konštanta(서술);
        return zdroj(종류, vlastník_identifikátor, zdroj(12, názov_COUNT, formát_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (kód_zmeniť_veľkosť == kód_VALUE.length) { zlyhanie_VALUE("bytecode too large"); return; }
        kód_VALUE[kód_zmeniť_veľkosť++] = VALUE & 255;
    }
    static void Príkaz(int VALUE, int Argumenty) { 내보내기(VALUE); 내보내기(Argumenty >> 8); 내보내기(Argumenty); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Spustiť_2 = konštanta_zmeniť_veľkosť; zapísať_konštanta_Byte(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Príkaz(19, register_konštanta(Spustiť_2));
    }
    static int vetva(int Príkaz) { int KR = kód_zmeniť_veľkosť; Príkaz(Príkaz, 0); return KR; }
    static void odkaz_VALUE(int vetva, int cieľ_objekt) {
        if (chyba) return;
        int 거리 = cieľ_objekt - vetva;
        if (거리 < -32768 || 거리 > 32767 || vetva < 0 || vetva + 2 >= kód_zmeniť_veľkosť) { zlyhanie_VALUE("invalid branch"); return; }
        kód_VALUE[vetva + 1] = 거리 >> 8 & 255; kód_VALUE[vetva + 2] = 거리 & 255;
    }
    static void Porovnanie_VALUE(int Príkaz) {
        int TRUE_VALUE = vetva(Príkaz); 내보내기(3); int 끝 = vetva(167);
        odkaz_VALUE(TRUE_VALUE, kód_zmeniť_veľkosť); 내보내기(4); odkaz_VALUE(끝, kód_zmeniť_veľkosť);
    }
    static int formát_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (dostať('[')) { požiadavka_VALUE(']'); return 4; } return 3; }
        zlyhanie_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Pridať_formát(int Typ_VALUE) {
        if (Typ_VALUE == 0) Pripojiť_SMS('V');
        if (Typ_VALUE == 1) Pripojiť_SMS('I');
        if (Typ_VALUE == 2) Pripojiť_SMS('Z');
        if (Typ_VALUE == 3) Pripojiť_Word("Ljava/lang/String;");
        if (Typ_VALUE == 4) Pripojiť_Word("[Ljava/lang/String;");
        if (Typ_VALUE == 5) Pripojiť_SMS('C');
        if (Typ_VALUE == 6) Pripojiť_Word("Ljava/io/FileInputStream;");
        if (Typ_VALUE == 7) Pripojiť_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklarácia. výnimka Proces_VALUE_položka 본문은 hostiteľ javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Slovenský");
        if (한국어묶음) { požiadavka_VALUE('.'); 말요구("vlastné"); požiadavka_VALUE('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("výnimka") || TAKE_Word("실행예외") || TAKE_Word("vstup_a_výstup_výnimka") || TAKE_Word("počkaj_TIMEOUT_výnimka") || TAKE_Word("adresa_LOOKUP_výnimka") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("neplatné_argument_výnimka") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NEPLATNÝ_zdroj_výnimka") || TAKE_Word("산술예외") || TAKE_Word("Stav_výnimka") || TAKE_Word("Typ_vysielať_výnimka") || TAKE_Word("음수배열크기예외") || TAKE_Word("pole_Store_zlyhanie") || TAKE_Word("vlákno_Stav_výnimka") || TAKE_Word("대기중단예외")) return;
        zlyhanie_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Pozícia, "Slovenský")) 예외이름읽기();
            else {
                말요구("java"); požiadavka_VALUE('.'); 말요구("io"); požiadavka_VALUE('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) zlyhanie_VALUE("unsupported import");
            }
            požiadavka_VALUE(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); lekcia_token = identifikátor_VALUE();
        lekcia_konštanta = zdroj(7, token_konštanta(lekcia_token), 0);
        nadradený_konštanta = zdroj(7, Word_konštanta("java/lang/Object"), 0); kód_konštanta = Word_konštanta("Code"); požiadavka_VALUE('{');
        while (!chyba && 종류() != '}') {
            if (metóda_COUNT == 32) { zlyhanie_VALUE("too many methods"); break; }
            int prístup_položka = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int funkcia_VALUE = metóda_COUNT++;
            metóda_prístup[funkcia_VALUE] = prístup_položka | 8;
            metóda_vrátiť[funkcia_VALUE] = formát_VALUE(); metóda_položka_názov[funkcia_VALUE] = identifikátor_VALUE(); požiadavka_VALUE('(');
            for (int predný_VALUE = 0; predný_VALUE < funkcia_VALUE; predný_VALUE++) if (이름같음(metóda_položka_názov[predný_VALUE], metóda_položka_názov[funkcia_VALUE])) zlyhanie_VALUE("duplicate method (overloading unsupported)");
            while (!chyba && 종류() != ')') {
                int 수 = metóda_argument_COUNT[funkcia_VALUE];
                if (수 == 16) { zlyhanie_VALUE("too many parameters"); break; }
                int Typ_VALUE = formát_VALUE(); if (Typ_VALUE == 0) zlyhanie_VALUE("void parameter");
                metóda_argument_Typ[funkcia_VALUE * 16 + 수] = Typ_VALUE; metóda_argument_názov[funkcia_VALUE * 16 + 수] = identifikátor_VALUE();
                metóda_argument_COUNT[funkcia_VALUE]++;
                if (!dostať(',')) break;
            }
            požiadavka_VALUE(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!chyba && dostať(','));
            }
            metóda_telo_správy[funkcia_VALUE] = Pozícia; požiadavka_VALUE('{');
            int vnorenie_VALUE = 1;
            while (Pozícia < token_COUNT && vnorenie_VALUE > 0) {
                if (종류() == '{') vnorenie_VALUE++;
                if (종류() == '}') vnorenie_VALUE--;
                Pozícia++;
            }
            if (vnorenie_VALUE != 0) zlyhanie_VALUE("unclosed method body");
            metóda_ukončiť_hovor[funkcia_VALUE] = Pozícia;
            metóda_názov_konštanta[funkcia_VALUE] = token_konštanta(metóda_položka_názov[funkcia_VALUE]);
            znak_dĺžka = 0; Pripojiť_SMS('(');
            for (int 수 = 0; 수 < metóda_argument_COUNT[funkcia_VALUE]; 수++) Pridať_formát(metóda_argument_Typ[funkcia_VALUE * 16 + 수]);
            Pripojiť_SMS(')'); Pridať_formát(metóda_vrátiť[funkcia_VALUE]); 함수서술[funkcia_VALUE] = znak_konštanta();
        }
        požiadavka_VALUE('}'); if (Pozícia != token_COUNT) zlyhanie_VALUE("extra input after class");
    }
    static int FIND_miestny(int Názov) {
        for (int 수 = miestny_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(miestny_názov[수], Názov)) return 수;
        zlyhanie_VALUE("unknown variable"); return 0;
    }
    static int Pridať_miestny(int Názov, int Typ_VALUE) {
        for (int 수 = 0; 수 < miestny_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(miestny_názov[수], Názov)) zlyhanie_VALUE("duplicate local variable");
        if (miestny_COUNT == 128) { zlyhanie_VALUE("too many locals"); return 0; }
        miestny_názov[miestny_COUNT] = Názov; miestny_Typ[miestny_COUNT] = Typ_VALUE; 지역깊이[miestny_COUNT] = 깊이;
        return miestny_COUNT++;
    }
    static boolean celé_číslo_Typ(int Typ_VALUE) { return Typ_VALUE == 1 || Typ_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(miestny_Typ[수] <= 2 || miestny_Typ[수] == 5 ? 21 : 25); 내보내기(수); }
    static void zapísať_miestny(int 수) { 내보내기(miestny_Typ[수] <= 2 || miestny_Typ[수] == 5 ? 54 : 58); 내보내기(수); }
    static void overiť_Typ(int skutočný_údaje, int 기대) { if (skutočný_údaje != 기대 && !(skutočný_údaje == 5 && 기대 == 1)) zlyhanie_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        znak_dĺžka = 0; int Spustiť_2 = token_pozícia[token_VALUE] + 1, 끝 = token_pozícia[token_VALUE] + token_dĺžka[token_VALUE] - 1;
        while (Spustiť_2 < 끝 && !chyba) {
            int VALUE = ZDROJ[Spustiť_2++];
            if (VALUE == '\\') {
                if (Spustiť_2 == 끝) { zlyhanie_VALUE("invalid escape"); break; }
                VALUE = ZDROJ[Spustiť_2++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') zlyhanie_VALUE("unsupported escape");
            }
            Pripojiť_SMS(VALUE);
        }
    }
    static int analyzovať_celé_číslo(int token_VALUE, boolean 음수) {
        if (token_dĺžka[token_VALUE] > 1 && ZDROJ[token_pozícia[token_VALUE]] == '0') zlyhanie_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < token_dĺžka[token_VALUE]; 수++) {
            int číslica_položka = ZDROJ[token_pozícia[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && číslica_položka > (음수 ? 8 : 7)) zlyhanie_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - číslica_položka;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int Typ_VALUE = formát_VALUE();
            if (Typ_VALUE != 6 && Typ_VALUE != 7) { zlyhanie_VALUE("only file streams supported by new in source"); return 0; }
            String vlastník_VALUE = Typ_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Príkaz(187, zdroj(7, Word_konštanta(vlastník_VALUE), 0)); 내보내기(89);
            požiadavka_VALUE('('); overiť_Typ(výraz_VALUE(), 3); boolean 이어 = false;
            if (dostať(',')) { if (Typ_VALUE != 7) zlyhanie_VALUE("input stream constructor arguments"); overiť_Typ(výraz_VALUE(), 2); 이어 = true; }
            požiadavka_VALUE(')');
            Príkaz(183, externý_zdroj(10, vlastník_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return Typ_VALUE;
        }
        if (dostať('(')) { int Typ_VALUE = výraz_VALUE(); požiadavka_VALUE(')'); return Typ_VALUE; }
        if (종류() == 257) { 수상수(analyzovať_celé_číslo(Pozícia++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Pozícia++); Príkaz(19, zdroj(8, znak_konštanta(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Pozícia++); if (znak_dĺžka != 1) zlyhanie_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Slovenský")) {
            požiadavka_VALUE('.'); 말요구("vlastné"); požiadavka_VALUE('.');
            String vlastník_VALUE = "", metóda_VALUE = "", 서술 = ""; int 가 = 0, SECOND_operand = 0, 다 = 0, 라 = 0, 마 = 0, KR = 0;
            if (TAKE_Word("Výstup")) {
                vlastník_VALUE = "Slovenský/vlastné/Výstup"; požiadavka_VALUE('.');
                if (TAKE_Word("zapísať_linka")) { metóda_VALUE = "zapísať_linka"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Zápis")) { metóda_VALUE = "Zápis"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { metóda_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else zlyhanie_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                vlastník_VALUE = "Slovenský/vlastné/문자"; požiadavka_VALUE('.'); 가 = 3;
                if (TAKE_Word("dĺžka_VALUE")) { metóda_VALUE = "dĺžka_VALUE"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAKE_Word("bod_kódu_COUNT")) { metóda_VALUE = "bod_kódu_COUNT"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAKE_Word("analyzovať_celé_číslo")) { metóda_VALUE = "analyzovať_celé_číslo"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAKE_Word("zapísať_celé_číslo_VALUE")) { metóda_VALUE = "zapísať_celé_číslo_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; KR = 3; }
                else if (TAKE_Word("같음")) { metóda_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECOND_operand = 3; KR = 2; }
                else if (TAKE_Word("prilepiť_SMS")) { metóda_VALUE = "prilepiť_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECOND_operand = 3; KR = 3; }
                else if (TAKE_Word("strihať_VALUE")) { metóda_VALUE = "strihať_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECOND_operand = 1; 다 = 1; KR = 3; }
                else zlyhanie_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Súbor")) {
                vlastník_VALUE = "Slovenský/vlastné/Súbor"; požiadavka_VALUE('.'); 가 = 3;
                if (TAKE_Word("Čítanie")) { metóda_VALUE = "Čítanie"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; KR = 3; }
                else if (TAKE_Word("Zápis")) { metóda_VALUE = "Zápis"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECOND_operand = 3; }
                else zlyhanie_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                vlastník_VALUE = "Slovenský/vlastné/화면"; požiadavka_VALUE('.');
                if (TAKE_Word("너비")) { metóda_VALUE = "너비"; 서술 = "()I"; KR = 1; }
                else if (TAKE_Word("výška_VALUE")) { metóda_VALUE = "výška_VALUE"; 서술 = "()I"; KR = 1; }
                else if (TAKE_Word("obdĺžnik")) { metóda_VALUE = "obdĺžnik"; 서술 = "(IIIII)V"; 가 = 1; SECOND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("vymazať_položka")) { metóda_VALUE = "vymazať_položka"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metóda_VALUE = "기다리기"; 서술 = "()V"; }
                else zlyhanie_VALUE("unknown Korean framebuffer method");
            } else zlyhanie_VALUE("unsupported Korean library class");
            požiadavka_VALUE('('); if (가 != 0) overiť_Typ(výraz_VALUE(), 가);
            if (SECOND_operand != 0) { požiadavka_VALUE(','); overiť_Typ(výraz_VALUE(), SECOND_operand); }
            if (다 != 0) { požiadavka_VALUE(','); overiť_Typ(výraz_VALUE(), 다); }
            if (라 != 0) { požiadavka_VALUE(','); overiť_Typ(výraz_VALUE(), 라); }
            if (마 != 0) { požiadavka_VALUE(','); overiť_Typ(výraz_VALUE(), 마); }
            požiadavka_VALUE(')'); Príkaz(184, externý_zdroj(10, vlastník_VALUE, metóda_VALUE, 서술)); return KR;
        }
        if (TAKE_Word("Integer")) {
            požiadavka_VALUE('.'); 말요구("parseInt"); požiadavka_VALUE('('); overiť_Typ(výraz_VALUE(), 3); požiadavka_VALUE(')');
            Príkaz(184, externý_zdroj(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Názov = identifikátor_VALUE();
        if (dostať('(')) {
            int funkcia_VALUE = -1;
            for (int 수 = 0; 수 < metóda_COUNT; 수++) if (이름같음(Názov, metóda_položka_názov[수])) funkcia_VALUE = 수;
            if (funkcia_VALUE < 0) { zlyhanie_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!chyba && 종류() != ')') {
                if (수 >= metóda_argument_COUNT[funkcia_VALUE]) { zlyhanie_VALUE("too many arguments"); break; }
                overiť_Typ(výraz_VALUE(), metóda_argument_Typ[funkcia_VALUE * 16 + 수++]); if (!dostať(',')) break;
            }
            požiadavka_VALUE(')'); if (수 != metóda_argument_COUNT[funkcia_VALUE]) zlyhanie_VALUE("argument count mismatch");
            Príkaz(184, zdroj(10, lekcia_konštanta, zdroj(12, metóda_názov_konštanta[funkcia_VALUE], 함수서술[funkcia_VALUE])));
            return metóda_vrátiť[funkcia_VALUE];
        }
        int miestny_Rozsah = FIND_miestny(Názov), Typ_VALUE = miestny_Typ[miestny_Rozsah]; 지역읽기(miestny_Rozsah);
        while (!chyba) {
            if (dostať('[')) { overiť_Typ(Typ_VALUE, 4); overiť_Typ(výraz_VALUE(), 1); požiadavka_VALUE(']'); 내보내기(50); Typ_VALUE = 3; }
            else if (dostať('.')) {
                if (Typ_VALUE == 6 || Typ_VALUE == 7) {
                    String vlastník_VALUE = Typ_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { požiadavka_VALUE('('); požiadavka_VALUE(')'); Príkaz(182, externý_zdroj(10, vlastník_VALUE, "close", "()V")); Typ_VALUE = 0; }
                    else if (Typ_VALUE == 6 && TAKE_Word("read")) { požiadavka_VALUE('('); požiadavka_VALUE(')'); Príkaz(182, externý_zdroj(10, vlastník_VALUE, "read", "()I")); Typ_VALUE = 1; }
                    else if (Typ_VALUE == 7 && TAKE_Word("write")) { požiadavka_VALUE('('); overiť_Typ(výraz_VALUE(), 1); požiadavka_VALUE(')'); Príkaz(182, externý_zdroj(10, vlastník_VALUE, "write", "(I)V")); Typ_VALUE = 0; }
                    else { zlyhanie_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (Typ_VALUE == 4) { 내보내기(190); Typ_VALUE = 1; }
                else { overiť_Typ(Typ_VALUE, 3); požiadavka_VALUE('('); požiadavka_VALUE(')'); Príkaz(182, externý_zdroj(10, "java/lang/String", "length", "()I")); Typ_VALUE = 1; }
            } else break;
        }
        return Typ_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { zlyhanie_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int Typ_VALUE;
        if (dostať('!')) { overiť_Typ(단항(), 2); Porovnanie_VALUE(153); Typ_VALUE = 2; }
        else if (dostať('-')) {
            if (종류() == 257) 수상수(analyzovať_celé_číslo(Pozícia++, true));
            else { overiť_Typ(단항(), 1); 내보내기(116); }
            Typ_VALUE = 1;
        } else if (dostať('+')) { overiť_Typ(단항(), 1); Typ_VALUE = 1; }
        else Typ_VALUE = 기본식();
        식깊이--; return Typ_VALUE;
    }
    static int 곱식() {
        int Typ_VALUE = 단항();
        while (!chyba && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kódovanie_VALUE = 종류(); Pozícia++; overiť_Typ(Typ_VALUE, 1); overiť_Typ(단항(), 1);
            내보내기(kódovanie_VALUE == '*' ? 104 : kódovanie_VALUE == '/' ? 108 : 112); Typ_VALUE = 1;
        }
        return Typ_VALUE;
    }
    static int 합식() {
        int Typ_VALUE = 곱식();
        while (!chyba && (종류() == '+' || 종류() == '-')) {
            int kódovanie_VALUE = 종류(); Pozícia++; int 경계 = kód_zmeniť_veľkosť, BACK_typ_hodnoty = 곱식();
            if (kódovanie_VALUE == '+' && (Typ_VALUE == 3 || BACK_typ_hodnoty == 3)) { 결합(경계, Typ_VALUE, BACK_typ_hodnoty); Typ_VALUE = 3; }
            else { overiť_Typ(Typ_VALUE, 1); overiť_Typ(BACK_typ_hodnoty, 1); 내보내기(kódovanie_VALUE == '+' ? 96 : 100); Typ_VALUE = 1; }
        }
        return Typ_VALUE;
    }
    static int 붙임참조(int Typ_VALUE) {
        if (Typ_VALUE != 1 && Typ_VALUE != 2 && Typ_VALUE != 3 && Typ_VALUE != 5) zlyhanie_VALUE("unsupported concatenation type");
        return externý_zdroj(10, "java/lang/StringBuilder", "append", Typ_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : Typ_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : Typ_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int predný_typ_hodnoty, int BACK_typ_hodnoty) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT kód_VALUE 앞에 generovať 코드를 삽입한다.
        // RIGHT výraz_VALUE 내부의 partnerský_uzol_VALUE vetva 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = kód_zmeniť_veľkosť;
        Príkaz(187, zdroj(7, Word_konštanta("java/lang/StringBuilder"), 0)); 내보내기(89);
        Príkaz(183, externý_zdroj(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Príkaz(182, 붙임참조(predný_typ_hodnoty));
        if (chyba) return;
        int dĺžka_VALUE = kód_zmeniť_veľkosť - 끝;
        for (int 수 = 0; 수 < dĺžka_VALUE; 수++) 삽입코드[수] = kód_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) kód_VALUE[수 + dĺžka_VALUE] = kód_VALUE[수];
        for (int 수 = 0; 수 < dĺžka_VALUE; 수++) kód_VALUE[경계 + 수] = 삽입코드[수];
        Príkaz(182, 붙임참조(BACK_typ_hodnoty)); Príkaz(182, externý_zdroj(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Porovnanie_výraz() {
        int Typ_VALUE = 합식();
        while (!chyba && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kódovanie_VALUE = 종류(); Pozícia++; overiť_Typ(Typ_VALUE, 1); overiť_Typ(합식(), 1);
            Porovnanie_VALUE(kódovanie_VALUE == '<' ? 161 : kódovanie_VALUE == '>' ? 163 : kódovanie_VALUE == 302 ? 164 : 162); Typ_VALUE = 2;
        }
        return Typ_VALUE;
    }
    static int 동등식() {
        int Typ_VALUE = Porovnanie_výraz();
        while (!chyba && (종류() == 300 || 종류() == 301)) {
            int kódovanie_VALUE = 종류(); Pozícia++; int BACK_typ_hodnoty = Porovnanie_výraz();
            if (Typ_VALUE == 0 || BACK_typ_hodnoty == 0) zlyhanie_VALUE("void expression");
            if (!(celé_číslo_Typ(Typ_VALUE) && celé_číslo_Typ(BACK_typ_hodnoty))) overiť_Typ(BACK_typ_hodnoty, Typ_VALUE);
            Porovnanie_VALUE((Typ_VALUE <= 2 || Typ_VALUE == 5 ? 159 : 165) + (kódovanie_VALUE == 301 ? 1 : 0)); Typ_VALUE = 2;
        }
        return Typ_VALUE;
    }
    static int logická_spojka_a() {
        int Typ_VALUE = 동등식();
        while (!chyba && dostať(304)) {
            overiť_Typ(Typ_VALUE, 2); int 가 = vetva(153); overiť_Typ(동등식(), 2); int SECOND_operand = vetva(153);
            내보내기(4); int 끝 = vetva(167); odkaz_VALUE(가, kód_zmeniť_veľkosť); odkaz_VALUE(SECOND_operand, kód_zmeniť_veľkosť); 내보내기(3); odkaz_VALUE(끝, kód_zmeniť_veľkosť); Typ_VALUE = 2;
        }
        return Typ_VALUE;
    }
    static int výraz_VALUE() {
        int Typ_VALUE = logická_spojka_a();
        while (!chyba && dostať(305)) {
            overiť_Typ(Typ_VALUE, 2); int 가 = vetva(154); overiť_Typ(logická_spojka_a(), 2); int SECOND_operand = vetva(154);
            내보내기(3); int 끝 = vetva(167); odkaz_VALUE(가, kód_zmeniť_veľkosť); odkaz_VALUE(SECOND_operand, kód_zmeniť_veľkosť); 내보내기(4); odkaz_VALUE(끝, kód_zmeniť_veľkosť); Typ_VALUE = 2;
        }
        return Typ_VALUE;
    }
    static void úloha_VALUE(boolean Povoliť_deklarácia) {
        if (Word_VALUE(Pozícia, "int") || Word_VALUE(Pozícia, "boolean") || Word_VALUE(Pozícia, "String") || Word_VALUE(Pozícia, "char")
            || Word_VALUE(Pozícia, "FileInputStream") || Word_VALUE(Pozícia, "FileOutputStream")) {
            if (!Povoliť_deklarácia) zlyhanie_VALUE("declaration not allowed here");
            int Typ_VALUE = formát_VALUE(), Názov = identifikátor_VALUE(); požiadavka_VALUE('='); overiť_Typ(výraz_VALUE(), Typ_VALUE);
            zapísať_miestny(Pridať_miestny(Názov, Typ_VALUE)); return;
        }
        int Názov = identifikátor_VALUE(), miestny_Rozsah = FIND_miestny(Názov);
        if (dostať('=')) { overiť_Typ(výraz_VALUE(), miestny_Typ[miestny_Rozsah]); zapísať_miestny(miestny_Rozsah); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kódovanie_VALUE = 종류(); Pozícia++; 지역읽기(miestny_Rozsah); int 경계 = kód_zmeniť_veľkosť, BACK_typ_hodnoty = výraz_VALUE();
            if (kódovanie_VALUE == 308 && miestny_Typ[miestny_Rozsah] == 3) 결합(경계, 3, BACK_typ_hodnoty);
            else {
                overiť_Typ(miestny_Typ[miestny_Rozsah], 1); overiť_Typ(BACK_typ_hodnoty, 1);
                내보내기(kódovanie_VALUE == 308 ? 96 : kódovanie_VALUE == 309 ? 100 : kódovanie_VALUE == 310 ? 104 : kódovanie_VALUE == 311 ? 108 : 112);
                if (miestny_Typ[miestny_Rozsah] == 5) 내보내기(146);
            }
            zapísať_miestny(miestny_Rozsah);
        }
        else if (종류() == 306 || 종류() == 307) {
            overiť_Typ(miestny_Typ[miestny_Rozsah], 1); 내보내기(132); 내보내기(miestny_Rozsah); 내보내기(종류() == 306 ? 1 : 255); Pozícia++;
            if (miestny_Typ[miestny_Rozsah] == 5) { 지역읽기(miestny_Rozsah); 내보내기(146); zapísať_miestny(miestny_Rozsah); }
        } else zlyhanie_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); požiadavka_VALUE('.'); 말요구("out"); požiadavka_VALUE('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); požiadavka_VALUE('(');
        Príkaz(178, externý_zdroj(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean prázdny_argument = 종류() == ')';
        int Typ_VALUE = prázdny_argument ? 0 : výraz_VALUE(); požiadavka_VALUE(')'); požiadavka_VALUE(';');
        String 서술 = Typ_VALUE == 0 ? "()V" : Typ_VALUE == 1 ? "(I)V" : Typ_VALUE == 2 ? "(Z)V" : Typ_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (Typ_VALUE == 4 || Typ_VALUE >= 6 || Typ_VALUE == 0 && (!줄바꿈 || !prázdny_argument)) zlyhanie_VALUE("unsupported print argument");
        Príkaz(182, externý_zdroj(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean príkaz_VALUE() {
        if (chyba) return false;
        if (깊이 > 32) { zlyhanie_VALUE("statement nesting too deep"); return false; }
        if (dostať('{')) {
            깊이++; boolean vrátiť_KR = false;
            while (!chyba && 종류() != '}') { if (vrátiť_KR) zlyhanie_VALUE("unreachable statement"); vrátiť_KR = príkaz_VALUE(); }
            požiadavka_VALUE('}'); for (int 수 = 0; 수 < miestny_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return vrátiť_KR;
        }
        if (dostať(';')) return false;
        if (TAKE_Word("return")) {
            int Typ_VALUE = 종류() == ';' ? 0 : výraz_VALUE(); overiť_Typ(Typ_VALUE, metóda_vrátiť[v_termíne_splatnosti_metóda]); požiadavka_VALUE(';');
            내보내기(Typ_VALUE == 0 ? 177 : Typ_VALUE <= 2 || Typ_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            požiadavka_VALUE('('); overiť_Typ(výraz_VALUE(), 2); požiadavka_VALUE(')'); int FALSE_VALUE = vetva(153);
            깊이++; boolean 가 = riadenie_príkaz(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = vetva(167); odkaz_VALUE(FALSE_VALUE, kód_zmeniť_veľkosť); 깊이++; boolean SECOND_operand = riadenie_príkaz(); 깊이--; odkaz_VALUE(끝, kód_zmeniť_veľkosť); return 가 && SECOND_operand; }
            odkaz_VALUE(FALSE_VALUE, kód_zmeniť_veľkosť); return false;
        }
        if (TAKE_Word("while")) {
            int Spustiť_2 = kód_zmeniť_veľkosť; požiadavka_VALUE('('); overiť_Typ(výraz_VALUE(), 2); požiadavka_VALUE(')'); int 끝 = vetva(153);
            깊이++; riadenie_príkaz(); 깊이--; odkaz_VALUE(vetva(167), Spustiť_2); odkaz_VALUE(끝, kód_zmeniť_veľkosť); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; požiadavka_VALUE('('); if (종류() != ';') úloha_VALUE(true); požiadavka_VALUE(';');
            int podmienka = kód_zmeniť_veľkosť; if (종류() == ';') 내보내기(4); else overiť_Typ(výraz_VALUE(), 2); požiadavka_VALUE(';');
            int 끝 = vetva(153), základný_text = vetva(167), obnoviť = kód_zmeniť_veľkosť;
            if (종류() != ')') úloha_VALUE(false); požiadavka_VALUE(')'); odkaz_VALUE(vetva(167), podmienka); odkaz_VALUE(základný_text, kód_zmeniť_veľkosť);
            riadenie_príkaz(); odkaz_VALUE(vetva(167), obnoviť); odkaz_VALUE(끝, kód_zmeniť_veľkosť);
            for (int 수 = 0; 수 < miestny_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Pozícia, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Pozícia + 1 < token_COUNT && (토큰종류[Pozícia + 1] == '(' || 토큰종류[Pozícia + 1] == '.')) {
            int Typ_VALUE = výraz_VALUE(); if (Typ_VALUE != 0) 내보내기(87); požiadavka_VALUE(';'); return false;
        }
        úloha_VALUE(true); požiadavka_VALUE(';'); return false;
    }
    static boolean riadenie_príkaz() {
        if (Word_VALUE(Pozícia, "int") || Word_VALUE(Pozícia, "boolean") || Word_VALUE(Pozícia, "char") || Word_VALUE(Pozícia, "String")
            || Word_VALUE(Pozícia, "FileInputStream") || Word_VALUE(Pozícia, "FileOutputStream")) zlyhanie_VALUE("local declaration requires braces");
        return príkaz_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == Výstup.length) zlyhanie_VALUE("class file too large"); else Výstup[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void zapísať_lekcia() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konštanta_COUNT);
        for (int 수 = 0; 수 < konštanta_zmeniť_veľkosť; 수++) 출바(konštanta_VALUE[수]);
        출짧(0x21); 출짧(lekcia_konštanta); 출짧(nadradený_konštanta); 출짧(0); 출짧(0); 출짧(metóda_COUNT);
        for (int 수 = 0; 수 < metóda_COUNT; 수++) {
            출짧(metóda_prístup[수]); 출짧(metóda_názov_konštanta[수]); 출짧(함수서술[수]); 출짧(1); 출짧(kód_konštanta);
            출정(12 + metóda_dĺžka[수]); 출짧(128); 출짧(함수지역[수]); 출정(metóda_dĺžka[수]);
            for (int 칸 = 0; 칸 < metóda_dĺžka[수]; 칸++) 출바(kód_VALUE[metóda_kód[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Spustiť_2() {
        if (používateľ.인수개수() == 1 && 자바도구.같음(používateľ.Argumenty(0), "-version")) {
            používateľ.Zápis("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (používateľ.인수개수() != 1) { používateľ.Zápis("Usage: javac FILE.java\n"); return 2; }
        int názov_zmeniť_veľkosť = 자바도구.Názov(názov_súboru_SMS, používateľ.Argumenty(0));
        if (názov_zmeniť_veľkosť < 6 || názov_zmeniť_veľkosť > 62 || názov_súboru_SMS[názov_zmeniť_veľkosť - 5] != '.' || názov_súboru_SMS[názov_zmeniť_veľkosť - 4] != 'j'
            || názov_súboru_SMS[názov_zmeniť_veľkosť - 3] != 'a' || názov_súboru_SMS[názov_zmeniť_veľkosť - 2] != 'v' || názov_súboru_SMS[názov_zmeniť_veľkosť - 1] != 'a') {
            používateľ.Zápis("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        zdroj_zmeniť_veľkosť = používateľ.파일읽기(názov_súboru_SMS, ZDROJ);
        if (zdroj_zmeniť_veľkosť < 0) { používateľ.Zápis("javac: cannot read source: "); 자바도구.수쓰기(zdroj_zmeniť_veľkosť); používateľ.zapísať_znak_VALUE(10); return 1; }
        zdroj_zmeniť_veľkosť = 자바도구.원문해독(ZDROJ, zdroj_zmeniť_veľkosť);
        if (zdroj_zmeniť_veľkosť < 0) { používateľ.Zápis("javac error: invalid UTF-8 source\n"); return 1; }
        strihať_VALUE(); if (!chyba) 선언읽기();
        if (!chyba) {
            if (token_dĺžka[lekcia_token] != názov_zmeniť_veľkosť - 5) zlyhanie_VALUE("class name must match file name");
            for (int 수 = 0; 수 < názov_zmeniť_veľkosť - 5; 수++) if (ZDROJ[token_pozícia[lekcia_token] + 수] != názov_súboru_SMS[수]) zlyhanie_VALUE("class name must match file name");
        }
        for (v_termíne_splatnosti_metóda = 0; v_termíne_splatnosti_metóda < metóda_COUNT && !chyba; v_termíne_splatnosti_metóda++) {
            Pozícia = metóda_telo_správy[v_termíne_splatnosti_metóda]; metóda_kód[v_termíne_splatnosti_metóda] = kód_zmeniť_veľkosť; miestny_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metóda_argument_COUNT[v_termíne_splatnosti_metóda]; 수++) Pridať_miestny(metóda_argument_názov[v_termíne_splatnosti_metóda * 16 + 수], metóda_argument_Typ[v_termíne_splatnosti_metóda * 16 + 수]);
            boolean vrátiť_KR = príkaz_VALUE();
            if (!vrátiť_KR && metóda_vrátiť[v_termíne_splatnosti_metóda] != 0) zlyhanie_VALUE("missing return");
            // vetva 뒤의 합류 지점은 반드시 skutočný_údaje 명령이어야 한다 (버전 49 검증기).
            if (metóda_vrátiť[v_termíne_splatnosti_metóda] == 0) 내보내기(177);
            else { boolean celé_číslo = metóda_vrátiť[v_termíne_splatnosti_metóda] <= 2 || metóda_vrátiť[v_termíne_splatnosti_metóda] == 5; 내보내기(celé_číslo ? 3 : 1); 내보내기(celé_číslo ? 172 : 176); }
            if (Pozícia != metóda_ukončiť_hovor[v_termíne_splatnosti_metóda]) zlyhanie_VALUE("invalid method body");
            함수지역[v_termíne_splatnosti_metóda] = miestny_COUNT; metóda_dĺžka[v_termíne_splatnosti_metóda] = kód_zmeniť_veľkosť - metóda_kód[v_termíne_splatnosti_metóda];
        }
        if (chyba) return 1;
        zapísať_lekcia(); if (chyba) return 1;
        názov_súboru_SMS[názov_zmeniť_veľkosť - 4] = 'c'; názov_súboru_SMS[názov_zmeniť_veľkosť - 3] = 'l'; názov_súboru_SMS[názov_zmeniť_veľkosť - 2] = 'a';
        názov_súboru_SMS[názov_zmeniť_veľkosť - 1] = 's'; názov_súboru_SMS[názov_zmeniť_veľkosť] = 's'; názov_súboru_SMS[názov_zmeniť_veľkosť + 1] = 0;
        int KR = používateľ.zapísať_Súbor(názov_súboru_SMS, Výstup, 출력크기);
        if (KR < 0) { používateľ.Zápis("javac: cannot save class: "); 자바도구.수쓰기(KR); používateľ.zapísať_znak_VALUE(10); return 1; }
        používateľ.Zápis("Compiled: "); for (int 수 = 0; názov_súboru_SMS[수] != 0; 수++) používateľ.zapísať_znak_VALUE(názov_súboru_SMS[수]);
        používateľ.Zápis(" (JVM class version 49)\n"); return 0;
    }
}
