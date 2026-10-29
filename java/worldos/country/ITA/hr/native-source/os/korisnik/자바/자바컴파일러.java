// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java izvor_stablo -> 표준 버전 49 class kompilator. */
public final class 자바컴파일러 {
    static int[] IZVOR = new int[16384], Izlaz = new int[16384], kod_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_položaj = new int[2048], 토큰길이 = new int[2048];
    static int[] konstanta_VALUE = new int[4096], konstanta_pomak = new int[512];
    static int[] 문자 = new int[512], naziv_datoteke_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int izvor_promijeniti_veličinu, token_COUNT, Položaj, kod_promijeniti_veličinu, konstanta_promijeniti_veličinu, konstanta_COUNT = 1, 출력크기, 문자수;
    static boolean GREŠKA;
    static int poduka_token, poduka_konstanta, roditeljski_konstanta, kod_konstanta;
    static int[] postupak_unos_naziv = new int[32], postupak_vratiti = new int[32], postupak_argument_COUNT = new int[32];
    static int[] postupak_argument_naziv = new int[512], postupak_argument_TYPE = new int[512];
    static int[] postupak_tijelo = new int[32], postupak_završiti_razgovor = new int[32], postupak_kod = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], postupak_naziv_konstanta = new int[32], 함수서술 = new int[32];
    static int[] postupak_pristup = new int[32];
    static int postupak_COUNT, redovno_postupak, lokalno_COUNT, 깊이, 식깊이;
    static int[] lokalno_naziv = new int[128], lokalno_TYPE = new int[128], 지역깊이 = new int[128];

    static void kvar_VALUE(String 이유) {
        if (!GREŠKA) {
            korisnik.Zapisuj("javac error: "); korisnik.Zapisuj(이유);
            korisnik.Zapisuj(" at line ");
            int red = 1, 끝 = Položaj < token_COUNT ? token_položaj[Položaj] : izvor_promijeniti_veličinu;
            for (int 수 = 0; 수 < 끝; 수++) if (IZVOR[수] == 10) red++;
            자바도구.수쓰기(red); korisnik.zapisivanje_znak_VALUE(10);
        }
        GREŠKA = true;
    }
    static boolean znak_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean znamenka_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int SECOND_operand) {
        if (가 < 0 || SECOND_operand < 0 || 가 >= token_COUNT || SECOND_operand >= token_COUNT || 토큰길이[가] != 토큰길이[SECOND_operand]) return false;
        for (int 수 = 0; 수 < 토큰길이[가]; 수++) if (IZVOR[token_položaj[가] + 수] != IZVOR[token_položaj[SECOND_operand] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int token_VALUE, String Word_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || 토큰길이[token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (IZVOR[token_položaj[token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Položaj < token_COUNT ? 토큰종류[Položaj] : 0; }
    static boolean primiti(int VALUE) { if (종류() != VALUE) return false; Položaj++; return true; }
    static void preduvjet_VALUE(int VALUE) { if (!primiti(VALUE)) kvar_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Položaj, Word_SMS)) return false; Položaj++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) kvar_VALUE(Word_SMS); }
    static int identifikator_VALUE() {
        int REZULTAT = Položaj;
        if (종류() != 256) kvar_VALUE("identifier required"); else Položaj++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Pokreni = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Pokreni == 토큰길이[REZULTAT];
                for (int 칸 = Pokreni; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != IZVOR[token_položaj[REZULTAT] + 칸 - Pokreni]) 같음 = false;
                if (같음) kvar_VALUE("reserved word cannot be an identifier");
                Pokreni = 수 + 1;
            }
        }
        return REZULTAT;
    }
    static void izrezati_VALUE() {
        int 수 = 0;
        while (수 < izvor_promijeniti_veličinu && !GREŠKA) {
            int VALUE = IZVOR[수], Pokreni = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < izvor_promijeniti_veličinu && IZVOR[수 + 1] == '/') {
                while (수 < izvor_promijeniti_veličinu && IZVOR[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < izvor_promijeniti_veličinu && IZVOR[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < izvor_promijeniti_veličinu && !(IZVOR[수] == '*' && IZVOR[수 + 1] == '/')) 수++;
                if (수 + 1 >= izvor_promijeniti_veličinu) { kvar_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (znak_VALUE(VALUE)) { 종류 = 256; while (수 < izvor_promijeniti_veličinu && 문자이름규칙.이어진글자(IZVOR[수])) 수++; }
            else if (znamenka_VALUE(VALUE)) { 종류 = 257; while (수 < izvor_promijeniti_veličinu && znamenka_VALUE(IZVOR[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < izvor_promijeniti_veličinu && IZVOR[수] != VALUE && IZVOR[수] != 10 && IZVOR[수] != 13) {
                    if (IZVOR[수] == '\\') 수++;
                    수++;
                }
                if (수 >= izvor_promijeniti_veličinu || IZVOR[수] != VALUE) { kvar_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < izvor_promijeniti_veličinu) {
                    int Dalje_artikl = IZVOR[수];
                    if (VALUE == '=' && Dalje_artikl == '=') 종류 = 300;
                    if (VALUE == '!' && Dalje_artikl == '=') 종류 = 301;
                    if (VALUE == '<' && Dalje_artikl == '=') 종류 = 302;
                    if (VALUE == '>' && Dalje_artikl == '=') 종류 = 303;
                    if (VALUE == '&' && Dalje_artikl == '&') 종류 = 304;
                    if (VALUE == '|' && Dalje_artikl == '|') 종류 = 305;
                    if (VALUE == '+' && Dalje_artikl == '+') 종류 = 306;
                    if (VALUE == '-' && Dalje_artikl == '-') 종류 = 307;
                    if (VALUE == '+' && Dalje_artikl == '=') 종류 = 308;
                    if (VALUE == '-' && Dalje_artikl == '=') 종류 = 309;
                    if (VALUE == '*' && Dalje_artikl == '=') 종류 = 310;
                    if (VALUE == '/' && Dalje_artikl == '=') 종류 = 311;
                    if (VALUE == '%' && Dalje_artikl == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_COUNT == 토큰종류.length - 1) { kvar_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_položaj[token_COUNT] = Pokreni; 토큰길이[token_COUNT++] = 수 - Pokreni;
        }
    }
    static void zapisivanje_konstanta_bajt(int VALUE) {
        if (konstanta_promijeniti_veličinu == konstanta_VALUE.length) { kvar_VALUE("constant pool too large"); return; }
        konstanta_VALUE[konstanta_promijeniti_veličinu++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { zapisivanje_konstanta_bajt(VALUE >> 8); zapisivanje_konstanta_bajt(VALUE); }
    static int registar_konstanta(int Pokreni) {
        for (int 수 = 1; 수 < konstanta_COUNT; 수++) {
            int prednja_VALUE = konstanta_pomak[수], 길이 = (수 + 1 < konstanta_COUNT ? konstanta_pomak[수 + 1] : Pokreni) - prednja_VALUE;
            if (길이 != konstanta_promijeniti_veličinu - Pokreni) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (konstanta_VALUE[prednja_VALUE + 칸] != konstanta_VALUE[Pokreni + 칸]) 같음 = false;
            if (같음) { konstanta_promijeniti_veličinu = Pokreni; return 수; }
        }
        if (konstanta_COUNT == konstanta_pomak.length) { kvar_VALUE("too many constants"); return 0; }
        konstanta_pomak[konstanta_COUNT] = Pokreni;
        return konstanta_COUNT++;
    }
    static void dodati_SMS(int VALUE) {
        if (문자수 == 문자.length) { kvar_VALUE("text too long"); return; }
        문자[문자수++] = VALUE;
    }
    static void dodati_Word(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) dodati_SMS(Word_SMS.charAt(수)); }
    static int znak_konstanta() {
        int Pokreni = konstanta_promijeniti_veličinu; zapisivanje_konstanta_bajt(1); 상짧(0);
        for (int 수 = 0; 수 < 문자수; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) zapisivanje_konstanta_bajt(VALUE);
            else if (VALUE < 2048) { zapisivanje_konstanta_bajt(192 | VALUE >> 6); zapisivanje_konstanta_bajt(128 | VALUE & 63); }
            else { zapisivanje_konstanta_bajt(224 | VALUE >> 12); zapisivanje_konstanta_bajt(128 | VALUE >> 6 & 63); zapisivanje_konstanta_bajt(128 | VALUE & 63); }
        }
        if (GREŠKA) return 0;
        int 길이 = konstanta_promijeniti_veličinu - Pokreni - 3;
        konstanta_VALUE[Pokreni + 1] = 길이 >> 8; konstanta_VALUE[Pokreni + 2] = 길이 & 255;
        return registar_konstanta(Pokreni);
    }
    static int Word_konstanta(String Word_SMS) { 문자수 = 0; dodati_Word(Word_SMS); return znak_konstanta(); }
    static int token_konstanta(int token_VALUE) {
        문자수 = 0;
        for (int 수 = 0; 수 < 토큰길이[token_VALUE]; 수++) dodati_SMS(IZVOR[token_položaj[token_VALUE] + 수]);
        return znak_konstanta();
    }
    static int Reference(int 종류, int 가, int SECOND_operand) {
        int Pokreni = konstanta_promijeniti_veličinu; zapisivanje_konstanta_bajt(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SECOND_operand);
        return registar_konstanta(Pokreni);
    }
    static int vanjski_Reference(int 종류, String vlasnik_VALUE, String Ime, String 서술) {
        int vlasnik_identifikator = Reference(7, Word_konstanta(vlasnik_VALUE), 0);
        int naziv_COUNT = Word_konstanta(Ime), oblik_COUNT = Word_konstanta(서술);
        return Reference(종류, vlasnik_identifikator, Reference(12, naziv_COUNT, oblik_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (kod_promijeniti_veličinu == kod_VALUE.length) { kvar_VALUE("bytecode too large"); return; }
        kod_VALUE[kod_promijeniti_veličinu++] = VALUE & 255;
    }
    static void Naredba(int VALUE, int Argumenti) { 내보내기(VALUE); 내보내기(Argumenti >> 8); 내보내기(Argumenti); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Pokreni = konstanta_promijeniti_veličinu; zapisivanje_konstanta_bajt(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Naredba(19, registar_konstanta(Pokreni));
    }
    static int grana(int Naredba) { int REZULTAT = kod_promijeniti_veličinu; Naredba(Naredba, 0); return REZULTAT; }
    static void veza_VALUE(int grana, int cilj_objekt) {
        if (GREŠKA) return;
        int 거리 = cilj_objekt - grana;
        if (거리 < -32768 || 거리 > 32767 || grana < 0 || grana + 2 >= kod_promijeniti_veličinu) { kvar_VALUE("invalid branch"); return; }
        kod_VALUE[grana + 1] = 거리 >> 8 & 255; kod_VALUE[grana + 2] = 거리 & 255;
    }
    static void Usporedba_VALUE(int Naredba) {
        int TRUE_VALUE = grana(Naredba); 내보내기(3); int 끝 = grana(167);
        veza_VALUE(TRUE_VALUE, kod_promijeniti_veličinu); 내보내기(4); veza_VALUE(끝, kod_promijeniti_veličinu);
    }
    static int oblik_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (primiti('[')) { preduvjet_VALUE(']'); return 4; } return 3; }
        kvar_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Dodaj_oblik(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) dodati_SMS('V');
        if (TYPE_VALUE == 1) dodati_SMS('I');
        if (TYPE_VALUE == 2) dodati_SMS('Z');
        if (TYPE_VALUE == 3) dodati_Word("Ljava/lang/String;");
        if (TYPE_VALUE == 4) dodati_Word("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) dodati_SMS('C');
        if (TYPE_VALUE == 6) dodati_Word("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) dodati_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklaracija. iznimka Proces_VALUE_unos 본문은 domaćin javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("hrvatski");
        if (한국어묶음) { preduvjet_VALUE('.'); 말요구("vlastiti"); preduvjet_VALUE('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("iznimka") || TAKE_Word("실행예외") || TAKE_Word("U_I_iznimka") || TAKE_Word("čekaj_TIMEOUT_iznimka") || TAKE_Word("adresa_LOOKUP_iznimka") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("nevaljan_argument_iznimka") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_Reference_iznimka") || TAKE_Word("산술예외") || TAKE_Word("Stanje_iznimka") || TAKE_Word("TYPE_emitirati_iznimka") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_kvar") || TAKE_Word("nit_Stanje_iznimka") || TAKE_Word("대기중단예외")) return;
        kvar_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Položaj, "hrvatski")) 예외이름읽기();
            else {
                말요구("java"); preduvjet_VALUE('.'); 말요구("io"); preduvjet_VALUE('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) kvar_VALUE("unsupported import");
            }
            preduvjet_VALUE(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); poduka_token = identifikator_VALUE();
        poduka_konstanta = Reference(7, token_konstanta(poduka_token), 0);
        roditeljski_konstanta = Reference(7, Word_konstanta("java/lang/Object"), 0); kod_konstanta = Word_konstanta("Code"); preduvjet_VALUE('{');
        while (!GREŠKA && 종류() != '}') {
            if (postupak_COUNT == 32) { kvar_VALUE("too many methods"); break; }
            int pristup_unos = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = postupak_COUNT++;
            postupak_pristup[FUNCTION_VALUE] = pristup_unos | 8;
            postupak_vratiti[FUNCTION_VALUE] = oblik_VALUE(); postupak_unos_naziv[FUNCTION_VALUE] = identifikator_VALUE(); preduvjet_VALUE('(');
            for (int prednja_VALUE = 0; prednja_VALUE < FUNCTION_VALUE; prednja_VALUE++) if (이름같음(postupak_unos_naziv[prednja_VALUE], postupak_unos_naziv[FUNCTION_VALUE])) kvar_VALUE("duplicate method (overloading unsupported)");
            while (!GREŠKA && 종류() != ')') {
                int 수 = postupak_argument_COUNT[FUNCTION_VALUE];
                if (수 == 16) { kvar_VALUE("too many parameters"); break; }
                int TYPE_VALUE = oblik_VALUE(); if (TYPE_VALUE == 0) kvar_VALUE("void parameter");
                postupak_argument_TYPE[FUNCTION_VALUE * 16 + 수] = TYPE_VALUE; postupak_argument_naziv[FUNCTION_VALUE * 16 + 수] = identifikator_VALUE();
                postupak_argument_COUNT[FUNCTION_VALUE]++;
                if (!primiti(',')) break;
            }
            preduvjet_VALUE(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!GREŠKA && primiti(','));
            }
            postupak_tijelo[FUNCTION_VALUE] = Položaj; preduvjet_VALUE('{');
            int ugnježđivanje_VALUE = 1;
            while (Položaj < token_COUNT && ugnježđivanje_VALUE > 0) {
                if (종류() == '{') ugnježđivanje_VALUE++;
                if (종류() == '}') ugnježđivanje_VALUE--;
                Položaj++;
            }
            if (ugnježđivanje_VALUE != 0) kvar_VALUE("unclosed method body");
            postupak_završiti_razgovor[FUNCTION_VALUE] = Položaj;
            postupak_naziv_konstanta[FUNCTION_VALUE] = token_konstanta(postupak_unos_naziv[FUNCTION_VALUE]);
            문자수 = 0; dodati_SMS('(');
            for (int 수 = 0; 수 < postupak_argument_COUNT[FUNCTION_VALUE]; 수++) Dodaj_oblik(postupak_argument_TYPE[FUNCTION_VALUE * 16 + 수]);
            dodati_SMS(')'); Dodaj_oblik(postupak_vratiti[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = znak_konstanta();
        }
        preduvjet_VALUE('}'); if (Položaj != token_COUNT) kvar_VALUE("extra input after class");
    }
    static int FIND_lokalno(int Ime) {
        for (int 수 = lokalno_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokalno_naziv[수], Ime)) return 수;
        kvar_VALUE("unknown variable"); return 0;
    }
    static int Dodaj_lokalno(int Ime, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lokalno_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokalno_naziv[수], Ime)) kvar_VALUE("duplicate local variable");
        if (lokalno_COUNT == 128) { kvar_VALUE("too many locals"); return 0; }
        lokalno_naziv[lokalno_COUNT] = Ime; lokalno_TYPE[lokalno_COUNT] = TYPE_VALUE; 지역깊이[lokalno_COUNT] = 깊이;
        return lokalno_COUNT++;
    }
    static boolean cijeli_broj_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokalno_TYPE[수] <= 2 || lokalno_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void zapisivanje_lokalno(int 수) { 내보내기(lokalno_TYPE[수] <= 2 || lokalno_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void provjeriti_TYPE(int stvaran_podaci, int 기대) { if (stvaran_podaci != 기대 && !(stvaran_podaci == 5 && 기대 == 1)) kvar_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        문자수 = 0; int Pokreni = token_položaj[token_VALUE] + 1, 끝 = token_položaj[token_VALUE] + 토큰길이[token_VALUE] - 1;
        while (Pokreni < 끝 && !GREŠKA) {
            int VALUE = IZVOR[Pokreni++];
            if (VALUE == '\\') {
                if (Pokreni == 끝) { kvar_VALUE("invalid escape"); break; }
                VALUE = IZVOR[Pokreni++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') kvar_VALUE("unsupported escape");
            }
            dodati_SMS(VALUE);
        }
    }
    static int rastavljati_cijeli_broj(int token_VALUE, boolean 음수) {
        if (토큰길이[token_VALUE] > 1 && IZVOR[token_položaj[token_VALUE]] == '0') kvar_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < 토큰길이[token_VALUE]; 수++) {
            int znamenka_artikl = IZVOR[token_položaj[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && znamenka_artikl > (음수 ? 8 : 7)) kvar_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - znamenka_artikl;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = oblik_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { kvar_VALUE("only file streams supported by new in source"); return 0; }
            String vlasnik_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Naredba(187, Reference(7, Word_konstanta(vlasnik_VALUE), 0)); 내보내기(89);
            preduvjet_VALUE('('); provjeriti_TYPE(izraz_VALUE(), 3); boolean 이어 = false;
            if (primiti(',')) { if (TYPE_VALUE != 7) kvar_VALUE("input stream constructor arguments"); provjeriti_TYPE(izraz_VALUE(), 2); 이어 = true; }
            preduvjet_VALUE(')');
            Naredba(183, vanjski_Reference(10, vlasnik_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (primiti('(')) { int TYPE_VALUE = izraz_VALUE(); preduvjet_VALUE(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(rastavljati_cijeli_broj(Položaj++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Položaj++); Naredba(19, Reference(8, znak_konstanta(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Položaj++); if (문자수 != 1) kvar_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("hrvatski")) {
            preduvjet_VALUE('.'); 말요구("vlastiti"); preduvjet_VALUE('.');
            String vlasnik_VALUE = "", postupak_VALUE = "", 서술 = ""; int 가 = 0, SECOND_operand = 0, 다 = 0, 라 = 0, 마 = 0, REZULTAT = 0;
            if (TAKE_Word("Izlaz")) {
                vlasnik_VALUE = "hrvatski/vlastiti/Izlaz"; preduvjet_VALUE('.');
                if (TAKE_Word("zapisivanje_red")) { postupak_VALUE = "zapisivanje_red"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Zapisuj")) { postupak_VALUE = "Zapisuj"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { postupak_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else kvar_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                vlasnik_VALUE = "hrvatski/vlastiti/문자"; preduvjet_VALUE('.'); 가 = 3;
                if (TAKE_Word("길이")) { postupak_VALUE = "길이"; 서술 = "(Ljava/lang/String;)I"; REZULTAT = 1; }
                else if (TAKE_Word("točka_koda_COUNT")) { postupak_VALUE = "točka_koda_COUNT"; 서술 = "(Ljava/lang/String;)I"; REZULTAT = 1; }
                else if (TAKE_Word("rastavljati_cijeli_broj")) { postupak_VALUE = "rastavljati_cijeli_broj"; 서술 = "(Ljava/lang/String;)I"; REZULTAT = 1; }
                else if (TAKE_Word("zapisivanje_cijeli_broj_VALUE")) { postupak_VALUE = "zapisivanje_cijeli_broj_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; REZULTAT = 3; }
                else if (TAKE_Word("같음")) { postupak_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECOND_operand = 3; REZULTAT = 2; }
                else if (TAKE_Word("zalijepiti_SMS")) { postupak_VALUE = "zalijepiti_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECOND_operand = 3; REZULTAT = 3; }
                else if (TAKE_Word("izrezati_VALUE")) { postupak_VALUE = "izrezati_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECOND_operand = 1; 다 = 1; REZULTAT = 3; }
                else kvar_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Datoteka")) {
                vlasnik_VALUE = "hrvatski/vlastiti/Datoteka"; preduvjet_VALUE('.'); 가 = 3;
                if (TAKE_Word("Čitaj")) { postupak_VALUE = "Čitaj"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; REZULTAT = 3; }
                else if (TAKE_Word("Zapisuj")) { postupak_VALUE = "Zapisuj"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECOND_operand = 3; }
                else kvar_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                vlasnik_VALUE = "hrvatski/vlastiti/화면"; preduvjet_VALUE('.');
                if (TAKE_Word("너비")) { postupak_VALUE = "너비"; 서술 = "()I"; REZULTAT = 1; }
                else if (TAKE_Word("높이")) { postupak_VALUE = "높이"; 서술 = "()I"; REZULTAT = 1; }
                else if (TAKE_Word("pravokutnik")) { postupak_VALUE = "pravokutnik"; 서술 = "(IIIII)V"; 가 = 1; SECOND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("izbrisati_unos")) { postupak_VALUE = "izbrisati_unos"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { postupak_VALUE = "기다리기"; 서술 = "()V"; }
                else kvar_VALUE("unknown Korean framebuffer method");
            } else kvar_VALUE("unsupported Korean library class");
            preduvjet_VALUE('('); if (가 != 0) provjeriti_TYPE(izraz_VALUE(), 가);
            if (SECOND_operand != 0) { preduvjet_VALUE(','); provjeriti_TYPE(izraz_VALUE(), SECOND_operand); }
            if (다 != 0) { preduvjet_VALUE(','); provjeriti_TYPE(izraz_VALUE(), 다); }
            if (라 != 0) { preduvjet_VALUE(','); provjeriti_TYPE(izraz_VALUE(), 라); }
            if (마 != 0) { preduvjet_VALUE(','); provjeriti_TYPE(izraz_VALUE(), 마); }
            preduvjet_VALUE(')'); Naredba(184, vanjski_Reference(10, vlasnik_VALUE, postupak_VALUE, 서술)); return REZULTAT;
        }
        if (TAKE_Word("Integer")) {
            preduvjet_VALUE('.'); 말요구("parseInt"); preduvjet_VALUE('('); provjeriti_TYPE(izraz_VALUE(), 3); preduvjet_VALUE(')');
            Naredba(184, vanjski_Reference(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Ime = identifikator_VALUE();
        if (primiti('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < postupak_COUNT; 수++) if (이름같음(Ime, postupak_unos_naziv[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { kvar_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!GREŠKA && 종류() != ')') {
                if (수 >= postupak_argument_COUNT[FUNCTION_VALUE]) { kvar_VALUE("too many arguments"); break; }
                provjeriti_TYPE(izraz_VALUE(), postupak_argument_TYPE[FUNCTION_VALUE * 16 + 수++]); if (!primiti(',')) break;
            }
            preduvjet_VALUE(')'); if (수 != postupak_argument_COUNT[FUNCTION_VALUE]) kvar_VALUE("argument count mismatch");
            Naredba(184, Reference(10, poduka_konstanta, Reference(12, postupak_naziv_konstanta[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return postupak_vratiti[FUNCTION_VALUE];
        }
        int lokalno_doseg = FIND_lokalno(Ime), TYPE_VALUE = lokalno_TYPE[lokalno_doseg]; 지역읽기(lokalno_doseg);
        while (!GREŠKA) {
            if (primiti('[')) { provjeriti_TYPE(TYPE_VALUE, 4); provjeriti_TYPE(izraz_VALUE(), 1); preduvjet_VALUE(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (primiti('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String vlasnik_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { preduvjet_VALUE('('); preduvjet_VALUE(')'); Naredba(182, vanjski_Reference(10, vlasnik_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { preduvjet_VALUE('('); preduvjet_VALUE(')'); Naredba(182, vanjski_Reference(10, vlasnik_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { preduvjet_VALUE('('); provjeriti_TYPE(izraz_VALUE(), 1); preduvjet_VALUE(')'); Naredba(182, vanjski_Reference(10, vlasnik_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { kvar_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { provjeriti_TYPE(TYPE_VALUE, 3); preduvjet_VALUE('('); preduvjet_VALUE(')'); Naredba(182, vanjski_Reference(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { kvar_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (primiti('!')) { provjeriti_TYPE(단항(), 2); Usporedba_VALUE(153); TYPE_VALUE = 2; }
        else if (primiti('-')) {
            if (종류() == 257) 수상수(rastavljati_cijeli_broj(Položaj++, true));
            else { provjeriti_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (primiti('+')) { provjeriti_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!GREŠKA && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int šifriranje_VALUE = 종류(); Položaj++; provjeriti_TYPE(TYPE_VALUE, 1); provjeriti_TYPE(단항(), 1);
            내보내기(šifriranje_VALUE == '*' ? 104 : šifriranje_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!GREŠKA && (종류() == '+' || 종류() == '-')) {
            int šifriranje_VALUE = 종류(); Položaj++; int 경계 = kod_promijeniti_veličinu, TRAG_VALUE_TYPE = 곱식();
            if (šifriranje_VALUE == '+' && (TYPE_VALUE == 3 || TRAG_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, TRAG_VALUE_TYPE); TYPE_VALUE = 3; }
            else { provjeriti_TYPE(TYPE_VALUE, 1); provjeriti_TYPE(TRAG_VALUE_TYPE, 1); 내보내기(šifriranje_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) kvar_VALUE("unsupported concatenation type");
        return vanjski_Reference(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int prednja_VALUE_TYPE, int TRAG_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT kod_VALUE 앞에 generirati 코드를 삽입한다.
        // RIGHT izraz_VALUE 내부의 ravnopravan_član_VALUE grana 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = kod_promijeniti_veličinu;
        Naredba(187, Reference(7, Word_konstanta("java/lang/StringBuilder"), 0)); 내보내기(89);
        Naredba(183, vanjski_Reference(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Naredba(182, 붙임참조(prednja_VALUE_TYPE));
        if (GREŠKA) return;
        int 길이 = kod_promijeniti_veličinu - 끝;
        for (int 수 = 0; 수 < 길이; 수++) 삽입코드[수] = kod_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) kod_VALUE[수 + 길이] = kod_VALUE[수];
        for (int 수 = 0; 수 < 길이; 수++) kod_VALUE[경계 + 수] = 삽입코드[수];
        Naredba(182, 붙임참조(TRAG_VALUE_TYPE)); Naredba(182, vanjski_Reference(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Usporedba_izraz() {
        int TYPE_VALUE = 합식();
        while (!GREŠKA && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int šifriranje_VALUE = 종류(); Položaj++; provjeriti_TYPE(TYPE_VALUE, 1); provjeriti_TYPE(합식(), 1);
            Usporedba_VALUE(šifriranje_VALUE == '<' ? 161 : šifriranje_VALUE == '>' ? 163 : šifriranje_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Usporedba_izraz();
        while (!GREŠKA && (종류() == 300 || 종류() == 301)) {
            int šifriranje_VALUE = 종류(); Položaj++; int TRAG_VALUE_TYPE = Usporedba_izraz();
            if (TYPE_VALUE == 0 || TRAG_VALUE_TYPE == 0) kvar_VALUE("void expression");
            if (!(cijeli_broj_TYPE(TYPE_VALUE) && cijeli_broj_TYPE(TRAG_VALUE_TYPE))) provjeriti_TYPE(TRAG_VALUE_TYPE, TYPE_VALUE);
            Usporedba_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (šifriranje_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int AND() {
        int TYPE_VALUE = 동등식();
        while (!GREŠKA && primiti(304)) {
            provjeriti_TYPE(TYPE_VALUE, 2); int 가 = grana(153); provjeriti_TYPE(동등식(), 2); int SECOND_operand = grana(153);
            내보내기(4); int 끝 = grana(167); veza_VALUE(가, kod_promijeniti_veličinu); veza_VALUE(SECOND_operand, kod_promijeniti_veličinu); 내보내기(3); veza_VALUE(끝, kod_promijeniti_veličinu); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int izraz_VALUE() {
        int TYPE_VALUE = AND();
        while (!GREŠKA && primiti(305)) {
            provjeriti_TYPE(TYPE_VALUE, 2); int 가 = grana(154); provjeriti_TYPE(AND(), 2); int SECOND_operand = grana(154);
            내보내기(3); int 끝 = grana(167); veza_VALUE(가, kod_promijeniti_veličinu); veza_VALUE(SECOND_operand, kod_promijeniti_veličinu); 내보내기(4); veza_VALUE(끝, kod_promijeniti_veličinu); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void dodjela_VALUE(boolean Dopusti_deklaracija) {
        if (Word_VALUE(Položaj, "int") || Word_VALUE(Položaj, "boolean") || Word_VALUE(Položaj, "String") || Word_VALUE(Položaj, "char")
            || Word_VALUE(Položaj, "FileInputStream") || Word_VALUE(Položaj, "FileOutputStream")) {
            if (!Dopusti_deklaracija) kvar_VALUE("declaration not allowed here");
            int TYPE_VALUE = oblik_VALUE(), Ime = identifikator_VALUE(); preduvjet_VALUE('='); provjeriti_TYPE(izraz_VALUE(), TYPE_VALUE);
            zapisivanje_lokalno(Dodaj_lokalno(Ime, TYPE_VALUE)); return;
        }
        int Ime = identifikator_VALUE(), lokalno_doseg = FIND_lokalno(Ime);
        if (primiti('=')) { provjeriti_TYPE(izraz_VALUE(), lokalno_TYPE[lokalno_doseg]); zapisivanje_lokalno(lokalno_doseg); }
        else if (종류() >= 308 && 종류() <= 312) {
            int šifriranje_VALUE = 종류(); Položaj++; 지역읽기(lokalno_doseg); int 경계 = kod_promijeniti_veličinu, TRAG_VALUE_TYPE = izraz_VALUE();
            if (šifriranje_VALUE == 308 && lokalno_TYPE[lokalno_doseg] == 3) 결합(경계, 3, TRAG_VALUE_TYPE);
            else {
                provjeriti_TYPE(lokalno_TYPE[lokalno_doseg], 1); provjeriti_TYPE(TRAG_VALUE_TYPE, 1);
                내보내기(šifriranje_VALUE == 308 ? 96 : šifriranje_VALUE == 309 ? 100 : šifriranje_VALUE == 310 ? 104 : šifriranje_VALUE == 311 ? 108 : 112);
                if (lokalno_TYPE[lokalno_doseg] == 5) 내보내기(146);
            }
            zapisivanje_lokalno(lokalno_doseg);
        }
        else if (종류() == 306 || 종류() == 307) {
            provjeriti_TYPE(lokalno_TYPE[lokalno_doseg], 1); 내보내기(132); 내보내기(lokalno_doseg); 내보내기(종류() == 306 ? 1 : 255); Položaj++;
            if (lokalno_TYPE[lokalno_doseg] == 5) { 지역읽기(lokalno_doseg); 내보내기(146); zapisivanje_lokalno(lokalno_doseg); }
        } else kvar_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); preduvjet_VALUE('.'); 말요구("out"); preduvjet_VALUE('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); preduvjet_VALUE('(');
        Naredba(178, vanjski_Reference(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int TYPE_VALUE = 빈인수 ? 0 : izraz_VALUE(); preduvjet_VALUE(')'); preduvjet_VALUE(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !빈인수)) kvar_VALUE("unsupported print argument");
        Naredba(182, vanjski_Reference(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean izjava_VALUE() {
        if (GREŠKA) return false;
        if (깊이 > 32) { kvar_VALUE("statement nesting too deep"); return false; }
        if (primiti('{')) {
            깊이++; boolean vratiti_KR = false;
            while (!GREŠKA && 종류() != '}') { if (vratiti_KR) kvar_VALUE("unreachable statement"); vratiti_KR = izjava_VALUE(); }
            preduvjet_VALUE('}'); for (int 수 = 0; 수 < lokalno_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return vratiti_KR;
        }
        if (primiti(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : izraz_VALUE(); provjeriti_TYPE(TYPE_VALUE, postupak_vratiti[redovno_postupak]); preduvjet_VALUE(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            preduvjet_VALUE('('); provjeriti_TYPE(izraz_VALUE(), 2); preduvjet_VALUE(')'); int FALSE_VALUE = grana(153);
            깊이++; boolean 가 = kontrola_izjava(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = grana(167); veza_VALUE(FALSE_VALUE, kod_promijeniti_veličinu); 깊이++; boolean SECOND_operand = kontrola_izjava(); 깊이--; veza_VALUE(끝, kod_promijeniti_veličinu); return 가 && SECOND_operand; }
            veza_VALUE(FALSE_VALUE, kod_promijeniti_veličinu); return false;
        }
        if (TAKE_Word("while")) {
            int Pokreni = kod_promijeniti_veličinu; preduvjet_VALUE('('); provjeriti_TYPE(izraz_VALUE(), 2); preduvjet_VALUE(')'); int 끝 = grana(153);
            깊이++; kontrola_izjava(); 깊이--; veza_VALUE(grana(167), Pokreni); veza_VALUE(끝, kod_promijeniti_veličinu); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; preduvjet_VALUE('('); if (종류() != ';') dodjela_VALUE(true); preduvjet_VALUE(';');
            int uvjet = kod_promijeniti_veličinu; if (종류() == ';') 내보내기(4); else provjeriti_TYPE(izraz_VALUE(), 2); preduvjet_VALUE(';');
            int 끝 = grana(153), tijelo_teksta = grana(167), osvježiti = kod_promijeniti_veličinu;
            if (종류() != ')') dodjela_VALUE(false); preduvjet_VALUE(')'); veza_VALUE(grana(167), uvjet); veza_VALUE(tijelo_teksta, kod_promijeniti_veličinu);
            kontrola_izjava(); veza_VALUE(grana(167), osvježiti); veza_VALUE(끝, kod_promijeniti_veličinu);
            for (int 수 = 0; 수 < lokalno_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Položaj, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Položaj + 1 < token_COUNT && (토큰종류[Položaj + 1] == '(' || 토큰종류[Položaj + 1] == '.')) {
            int TYPE_VALUE = izraz_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); preduvjet_VALUE(';'); return false;
        }
        dodjela_VALUE(true); preduvjet_VALUE(';'); return false;
    }
    static boolean kontrola_izjava() {
        if (Word_VALUE(Položaj, "int") || Word_VALUE(Položaj, "boolean") || Word_VALUE(Položaj, "char") || Word_VALUE(Položaj, "String")
            || Word_VALUE(Položaj, "FileInputStream") || Word_VALUE(Položaj, "FileOutputStream")) kvar_VALUE("local declaration requires braces");
        return izjava_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == Izlaz.length) kvar_VALUE("class file too large"); else Izlaz[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void zapisivanje_poduka() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstanta_COUNT);
        for (int 수 = 0; 수 < konstanta_promijeniti_veličinu; 수++) 출바(konstanta_VALUE[수]);
        출짧(0x21); 출짧(poduka_konstanta); 출짧(roditeljski_konstanta); 출짧(0); 출짧(0); 출짧(postupak_COUNT);
        for (int 수 = 0; 수 < postupak_COUNT; 수++) {
            출짧(postupak_pristup[수]); 출짧(postupak_naziv_konstanta[수]); 출짧(함수서술[수]); 출짧(1); 출짧(kod_konstanta);
            출정(12 + 함수길이[수]); 출짧(128); 출짧(함수지역[수]); 출정(함수길이[수]);
            for (int 칸 = 0; 칸 < 함수길이[수]; 칸++) 출바(kod_VALUE[postupak_kod[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Pokreni() {
        if (korisnik.인수개수() == 1 && 자바도구.같음(korisnik.Argumenti(0), "-version")) {
            korisnik.Zapisuj("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (korisnik.인수개수() != 1) { korisnik.Zapisuj("Usage: javac FILE.java\n"); return 2; }
        int naziv_promijeniti_veličinu = 자바도구.Ime(naziv_datoteke_SMS, korisnik.Argumenti(0));
        if (naziv_promijeniti_veličinu < 6 || naziv_promijeniti_veličinu > 62 || naziv_datoteke_SMS[naziv_promijeniti_veličinu - 5] != '.' || naziv_datoteke_SMS[naziv_promijeniti_veličinu - 4] != 'j'
            || naziv_datoteke_SMS[naziv_promijeniti_veličinu - 3] != 'a' || naziv_datoteke_SMS[naziv_promijeniti_veličinu - 2] != 'v' || naziv_datoteke_SMS[naziv_promijeniti_veličinu - 1] != 'a') {
            korisnik.Zapisuj("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        izvor_promijeniti_veličinu = korisnik.파일읽기(naziv_datoteke_SMS, IZVOR);
        if (izvor_promijeniti_veličinu < 0) { korisnik.Zapisuj("javac: cannot read source: "); 자바도구.수쓰기(izvor_promijeniti_veličinu); korisnik.zapisivanje_znak_VALUE(10); return 1; }
        izvor_promijeniti_veličinu = 자바도구.원문해독(IZVOR, izvor_promijeniti_veličinu);
        if (izvor_promijeniti_veličinu < 0) { korisnik.Zapisuj("javac error: invalid UTF-8 source\n"); return 1; }
        izrezati_VALUE(); if (!GREŠKA) 선언읽기();
        if (!GREŠKA) {
            if (토큰길이[poduka_token] != naziv_promijeniti_veličinu - 5) kvar_VALUE("class name must match file name");
            for (int 수 = 0; 수 < naziv_promijeniti_veličinu - 5; 수++) if (IZVOR[token_položaj[poduka_token] + 수] != naziv_datoteke_SMS[수]) kvar_VALUE("class name must match file name");
        }
        for (redovno_postupak = 0; redovno_postupak < postupak_COUNT && !GREŠKA; redovno_postupak++) {
            Položaj = postupak_tijelo[redovno_postupak]; postupak_kod[redovno_postupak] = kod_promijeniti_veličinu; lokalno_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < postupak_argument_COUNT[redovno_postupak]; 수++) Dodaj_lokalno(postupak_argument_naziv[redovno_postupak * 16 + 수], postupak_argument_TYPE[redovno_postupak * 16 + 수]);
            boolean vratiti_KR = izjava_VALUE();
            if (!vratiti_KR && postupak_vratiti[redovno_postupak] != 0) kvar_VALUE("missing return");
            // grana 뒤의 합류 지점은 반드시 stvaran_podaci 명령이어야 한다 (버전 49 검증기).
            if (postupak_vratiti[redovno_postupak] == 0) 내보내기(177);
            else { boolean cijeli_broj = postupak_vratiti[redovno_postupak] <= 2 || postupak_vratiti[redovno_postupak] == 5; 내보내기(cijeli_broj ? 3 : 1); 내보내기(cijeli_broj ? 172 : 176); }
            if (Položaj != postupak_završiti_razgovor[redovno_postupak]) kvar_VALUE("invalid method body");
            함수지역[redovno_postupak] = lokalno_COUNT; 함수길이[redovno_postupak] = kod_promijeniti_veličinu - postupak_kod[redovno_postupak];
        }
        if (GREŠKA) return 1;
        zapisivanje_poduka(); if (GREŠKA) return 1;
        naziv_datoteke_SMS[naziv_promijeniti_veličinu - 4] = 'c'; naziv_datoteke_SMS[naziv_promijeniti_veličinu - 3] = 'l'; naziv_datoteke_SMS[naziv_promijeniti_veličinu - 2] = 'a';
        naziv_datoteke_SMS[naziv_promijeniti_veličinu - 1] = 's'; naziv_datoteke_SMS[naziv_promijeniti_veličinu] = 's'; naziv_datoteke_SMS[naziv_promijeniti_veličinu + 1] = 0;
        int REZULTAT = korisnik.zapisivanje_Datoteka(naziv_datoteke_SMS, Izlaz, 출력크기);
        if (REZULTAT < 0) { korisnik.Zapisuj("javac: cannot save class: "); 자바도구.수쓰기(REZULTAT); korisnik.zapisivanje_znak_VALUE(10); return 1; }
        korisnik.Zapisuj("Compiled: "); for (int 수 = 0; naziv_datoteke_SMS[수] != 0; 수++) korisnik.zapisivanje_znak_VALUE(naziv_datoteke_SMS[수]);
        korisnik.Zapisuj(" (JVM class version 49)\n"); return 0;
    }
}
