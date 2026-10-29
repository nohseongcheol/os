// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java izvor_stablo -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] IZVOR = new int[16384], Ispis = new int[16384], kod_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_položaj = new int[2048], token_dužina = new int[2048];
    static int[] konstanta_VALUE = new int[4096], konstanta_Pomak = new int[512];
    static int[] 문자 = new int[512], fajl_naziv_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int izvor_podesiti_veličinu, token_COUNT, Pozicija, kod_podesiti_veličinu, konstanta_podesiti_veličinu, konstanta_COUNT = 1, 출력크기, znak_dužina;
    static boolean GRESKA;
    static int klasa_token, klasa_konstanta, roditelj_konstanta, kod_konstanta;
    static int[] metoda_unos_naziv = new int[32], metoda_vratiti = new int[32], metoda_argument_COUNT = new int[32];
    static int[] metoda_argument_naziv = new int[512], metoda_argument_TYPE = new int[512];
    static int[] metoda_tijelo = new int[32], metoda_završiti = new int[32], metoda_kod = new int[32];
    static int[] metoda_dužina = new int[32], 함수지역 = new int[32], metoda_naziv_konstanta = new int[32], 함수서술 = new int[32];
    static int[] metoda_pristup = new int[32];
    static int metoda_COUNT, trenutno_metoda, lokalni_COUNT, 깊이, 식깊이;
    static int[] lokalni_naziv = new int[128], lokalni_TYPE = new int[128], 지역깊이 = new int[128];

    static void neuspjeh_VALUE(String 이유) {
        if (!GRESKA) {
            korisnik.Piši("javac error: "); korisnik.Piši(이유);
            korisnik.Piši(" at line ");
            int Linija = 1, 끝 = Pozicija < token_COUNT ? token_položaj[Pozicija] : izvor_podesiti_veličinu;
            for (int 수 = 0; 수 < 끝; 수++) if (IZVOR[수] == 10) Linija++;
            자바도구.수쓰기(Linija); korisnik.pisati_znak_VALUE(10);
        }
        GRESKA = true;
    }
    static boolean znak_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean cifra_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int SECOND_operand) {
        if (가 < 0 || SECOND_operand < 0 || 가 >= token_COUNT || SECOND_operand >= token_COUNT || token_dužina[가] != token_dužina[SECOND_operand]) return false;
        for (int 수 = 0; 수 < token_dužina[가]; 수++) if (IZVOR[token_položaj[가] + 수] != IZVOR[token_položaj[SECOND_operand] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int token_VALUE, String Word_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || token_dužina[token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (IZVOR[token_položaj[token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Pozicija < token_COUNT ? 토큰종류[Pozicija] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; Pozicija++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) neuspjeh_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Pozicija, Word_SMS)) return false; Pozicija++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) neuspjeh_VALUE(Word_SMS); }
    static int identifikator_VALUE() {
        int mjera = Pozicija;
        if (종류() != 256) neuspjeh_VALUE("identifier required"); else Pozicija++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Pokreni = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Pokreni == token_dužina[mjera];
                for (int prostor_za_unos_unos = Pokreni; 같음 && prostor_za_unos_unos < 수; prostor_za_unos_unos++) if (예약어.charAt(prostor_za_unos_unos) != IZVOR[token_položaj[mjera] + prostor_za_unos_unos - Pokreni]) 같음 = false;
                if (같음) neuspjeh_VALUE("reserved word cannot be an identifier");
                Pokreni = 수 + 1;
            }
        }
        return mjera;
    }
    static void izrezati_VALUE() {
        int 수 = 0;
        while (수 < izvor_podesiti_veličinu && !GRESKA) {
            int VALUE = IZVOR[수], Pokreni = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < izvor_podesiti_veličinu && IZVOR[수 + 1] == '/') {
                while (수 < izvor_podesiti_veličinu && IZVOR[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < izvor_podesiti_veličinu && IZVOR[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < izvor_podesiti_veličinu && !(IZVOR[수] == '*' && IZVOR[수 + 1] == '/')) 수++;
                if (수 + 1 >= izvor_podesiti_veličinu) { neuspjeh_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (znak_VALUE(VALUE)) { 종류 = 256; while (수 < izvor_podesiti_veličinu && 문자이름규칙.이어진글자(IZVOR[수])) 수++; }
            else if (cifra_VALUE(VALUE)) { 종류 = 257; while (수 < izvor_podesiti_veličinu && cifra_VALUE(IZVOR[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < izvor_podesiti_veličinu && IZVOR[수] != VALUE && IZVOR[수] != 10 && IZVOR[수] != 13) {
                    if (IZVOR[수] == '\\') 수++;
                    수++;
                }
                if (수 >= izvor_podesiti_veličinu || IZVOR[수] != VALUE) { neuspjeh_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < izvor_podesiti_veličinu) {
                    int Dalje_stavka = IZVOR[수];
                    if (VALUE == '=' && Dalje_stavka == '=') 종류 = 300;
                    if (VALUE == '!' && Dalje_stavka == '=') 종류 = 301;
                    if (VALUE == '<' && Dalje_stavka == '=') 종류 = 302;
                    if (VALUE == '>' && Dalje_stavka == '=') 종류 = 303;
                    if (VALUE == '&' && Dalje_stavka == '&') 종류 = 304;
                    if (VALUE == '|' && Dalje_stavka == '|') 종류 = 305;
                    if (VALUE == '+' && Dalje_stavka == '+') 종류 = 306;
                    if (VALUE == '-' && Dalje_stavka == '-') 종류 = 307;
                    if (VALUE == '+' && Dalje_stavka == '=') 종류 = 308;
                    if (VALUE == '-' && Dalje_stavka == '=') 종류 = 309;
                    if (VALUE == '*' && Dalje_stavka == '=') 종류 = 310;
                    if (VALUE == '/' && Dalje_stavka == '=') 종류 = 311;
                    if (VALUE == '%' && Dalje_stavka == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_COUNT == 토큰종류.length - 1) { neuspjeh_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_položaj[token_COUNT] = Pokreni; token_dužina[token_COUNT++] = 수 - Pokreni;
        }
    }
    static void pisati_konstanta_bajt(int VALUE) {
        if (konstanta_podesiti_veličinu == konstanta_VALUE.length) { neuspjeh_VALUE("constant pool too large"); return; }
        konstanta_VALUE[konstanta_podesiti_veličinu++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { pisati_konstanta_bajt(VALUE >> 8); pisati_konstanta_bajt(VALUE); }
    static int registrirati_konstanta(int Pokreni) {
        for (int 수 = 1; 수 < konstanta_COUNT; 수++) {
            int 앞 = konstanta_Pomak[수], dužina_VALUE = (수 + 1 < konstanta_COUNT ? konstanta_Pomak[수 + 1] : Pokreni) - 앞;
            if (dužina_VALUE != konstanta_podesiti_veličinu - Pokreni) continue;
            boolean 같음 = true;
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < dužina_VALUE; prostor_za_unos_unos++) if (konstanta_VALUE[앞 + prostor_za_unos_unos] != konstanta_VALUE[Pokreni + prostor_za_unos_unos]) 같음 = false;
            if (같음) { konstanta_podesiti_veličinu = Pokreni; return 수; }
        }
        if (konstanta_COUNT == konstanta_Pomak.length) { neuspjeh_VALUE("too many constants"); return 0; }
        konstanta_Pomak[konstanta_COUNT] = Pokreni;
        return konstanta_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (znak_dužina == 문자.length) { neuspjeh_VALUE("text too long"); return; }
        문자[znak_dužina++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int znak_konstanta() {
        int Pokreni = konstanta_podesiti_veličinu; pisati_konstanta_bajt(1); 상짧(0);
        for (int 수 = 0; 수 < znak_dužina; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) pisati_konstanta_bajt(VALUE);
            else if (VALUE < 2048) { pisati_konstanta_bajt(192 | VALUE >> 6); pisati_konstanta_bajt(128 | VALUE & 63); }
            else { pisati_konstanta_bajt(224 | VALUE >> 12); pisati_konstanta_bajt(128 | VALUE >> 6 & 63); pisati_konstanta_bajt(128 | VALUE & 63); }
        }
        if (GRESKA) return 0;
        int dužina_VALUE = konstanta_podesiti_veličinu - Pokreni - 3;
        konstanta_VALUE[Pokreni + 1] = dužina_VALUE >> 8; konstanta_VALUE[Pokreni + 2] = dužina_VALUE & 255;
        return registrirati_konstanta(Pokreni);
    }
    static int Word_konstanta(String Word_SMS) { znak_dužina = 0; 말추가(Word_SMS); return znak_konstanta(); }
    static int token_konstanta(int token_VALUE) {
        znak_dužina = 0;
        for (int 수 = 0; 수 < token_dužina[token_VALUE]; 수++) 글추가(IZVOR[token_položaj[token_VALUE] + 수]);
        return znak_konstanta();
    }
    static int Reference(int 종류, int 가, int SECOND_operand) {
        int Pokreni = konstanta_podesiti_veličinu; pisati_konstanta_bajt(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SECOND_operand);
        return registrirati_konstanta(Pokreni);
    }
    static int vanjska_referenca(int 종류, String vlasnik_VALUE, String Naziv, String 서술) {
        int vlasnik_identifikator = Reference(7, Word_konstanta(vlasnik_VALUE), 0);
        int naziv_COUNT = Word_konstanta(Naziv), format_COUNT = Word_konstanta(서술);
        return Reference(종류, vlasnik_identifikator, Reference(12, naziv_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (kod_podesiti_veličinu == kod_VALUE.length) { neuspjeh_VALUE("bytecode too large"); return; }
        kod_VALUE[kod_podesiti_veličinu++] = VALUE & 255;
    }
    static void Naredba(int VALUE, int Argumenti) { 내보내기(VALUE); 내보내기(Argumenti >> 8); 내보내기(Argumenti); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Pokreni = konstanta_podesiti_veličinu; pisati_konstanta_bajt(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Naredba(19, registrirati_konstanta(Pokreni));
    }
    static int ogranak(int Naredba) { int mjera = kod_podesiti_veličinu; Naredba(Naredba, 0); return mjera; }
    static void Veza_VALUE(int ogranak, int cilj_objekt) {
        if (GRESKA) return;
        int 거리 = cilj_objekt - ogranak;
        if (거리 < -32768 || 거리 > 32767 || ogranak < 0 || ogranak + 2 >= kod_podesiti_veličinu) { neuspjeh_VALUE("invalid branch"); return; }
        kod_VALUE[ogranak + 1] = 거리 >> 8 & 255; kod_VALUE[ogranak + 2] = 거리 & 255;
    }
    static void Poređenje_VALUE(int Naredba) {
        int TRUE_VALUE = ogranak(Naredba); 내보내기(3); int 끝 = ogranak(167);
        Veza_VALUE(TRUE_VALUE, kod_podesiti_veličinu); 내보내기(4); Veza_VALUE(끝, kod_podesiti_veličinu);
    }
    static int format_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        neuspjeh_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void dodati_format(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. izuzetak proces_VALUE_unos 본문은 organizator javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("izuzetak") || TAKE_Word("실행예외") || TAKE_Word("U_I_izuzetak") || TAKE_Word("čekaj_TIMEOUT_izuzetak") || TAKE_Word("adresa_LOOKUP_izuzetak") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("nevažeće_argument_izuzetak") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_Reference_izuzetak") || TAKE_Word("산술예외") || TAKE_Word("stanje_izuzetak") || TAKE_Word("TYPE_Emitiranje_izuzetak") || TAKE_Word("음수배열크기예외") || TAKE_Word("niz_Store_neuspjeh") || TAKE_Word("nit_stanje_izuzetak") || TAKE_Word("대기중단예외")) return;
        neuspjeh_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Pozicija, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) neuspjeh_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); klasa_token = identifikator_VALUE();
        klasa_konstanta = Reference(7, token_konstanta(klasa_token), 0);
        roditelj_konstanta = Reference(7, Word_konstanta("java/lang/Object"), 0); kod_konstanta = Word_konstanta("Code"); 요구('{');
        while (!GRESKA && 종류() != '}') {
            if (metoda_COUNT == 32) { neuspjeh_VALUE("too many methods"); break; }
            int pristup_unos = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = metoda_COUNT++;
            metoda_pristup[FUNCTION_VALUE] = pristup_unos | 8;
            metoda_vratiti[FUNCTION_VALUE] = format_VALUE(); metoda_unos_naziv[FUNCTION_VALUE] = identifikator_VALUE(); 요구('(');
            for (int 앞 = 0; 앞 < FUNCTION_VALUE; 앞++) if (이름같음(metoda_unos_naziv[앞], metoda_unos_naziv[FUNCTION_VALUE])) neuspjeh_VALUE("duplicate method (overloading unsupported)");
            while (!GRESKA && 종류() != ')') {
                int 수 = metoda_argument_COUNT[FUNCTION_VALUE];
                if (수 == 16) { neuspjeh_VALUE("too many parameters"); break; }
                int TYPE_VALUE = format_VALUE(); if (TYPE_VALUE == 0) neuspjeh_VALUE("void parameter");
                metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수] = TYPE_VALUE; metoda_argument_naziv[FUNCTION_VALUE * 16 + 수] = identifikator_VALUE();
                metoda_argument_COUNT[FUNCTION_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!GRESKA && 받기(','));
            }
            metoda_tijelo[FUNCTION_VALUE] = Pozicija; 요구('{');
            int 중첩 = 1;
            while (Pozicija < token_COUNT && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                Pozicija++;
            }
            if (중첩 != 0) neuspjeh_VALUE("unclosed method body");
            metoda_završiti[FUNCTION_VALUE] = Pozicija;
            metoda_naziv_konstanta[FUNCTION_VALUE] = token_konstanta(metoda_unos_naziv[FUNCTION_VALUE]);
            znak_dužina = 0; 글추가('(');
            for (int 수 = 0; 수 < metoda_argument_COUNT[FUNCTION_VALUE]; 수++) dodati_format(metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수]);
            글추가(')'); dodati_format(metoda_vratiti[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = znak_konstanta();
        }
        요구('}'); if (Pozicija != token_COUNT) neuspjeh_VALUE("extra input after class");
    }
    static int FIND_lokalni(int Naziv) {
        for (int 수 = lokalni_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokalni_naziv[수], Naziv)) return 수;
        neuspjeh_VALUE("unknown variable"); return 0;
    }
    static int dodati_lokalni(int Naziv, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lokalni_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokalni_naziv[수], Naziv)) neuspjeh_VALUE("duplicate local variable");
        if (lokalni_COUNT == 128) { neuspjeh_VALUE("too many locals"); return 0; }
        lokalni_naziv[lokalni_COUNT] = Naziv; lokalni_TYPE[lokalni_COUNT] = TYPE_VALUE; 지역깊이[lokalni_COUNT] = 깊이;
        return lokalni_COUNT++;
    }
    static boolean cijeli_broj_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokalni_TYPE[수] <= 2 || lokalni_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void pisati_lokalni(int 수) { 내보내기(lokalni_TYPE[수] <= 2 || lokalni_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void potvrditi_TYPE(int stvaran_podaci, int 기대) { if (stvaran_podaci != 기대 && !(stvaran_podaci == 5 && 기대 == 1)) neuspjeh_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        znak_dužina = 0; int Pokreni = token_položaj[token_VALUE] + 1, 끝 = token_položaj[token_VALUE] + token_dužina[token_VALUE] - 1;
        while (Pokreni < 끝 && !GRESKA) {
            int VALUE = IZVOR[Pokreni++];
            if (VALUE == '\\') {
                if (Pokreni == 끝) { neuspjeh_VALUE("invalid escape"); break; }
                VALUE = IZVOR[Pokreni++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') neuspjeh_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int raščlanjivati_cijeli_broj(int token_VALUE, boolean 음수) {
        if (token_dužina[token_VALUE] > 1 && IZVOR[token_položaj[token_VALUE]] == '0') neuspjeh_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < token_dužina[token_VALUE]; 수++) {
            int cifra_stavka = IZVOR[token_položaj[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && cifra_stavka > (음수 ? 8 : 7)) neuspjeh_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - cifra_stavka;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = format_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { neuspjeh_VALUE("only file streams supported by new in source"); return 0; }
            String vlasnik_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Naredba(187, Reference(7, Word_konstanta(vlasnik_VALUE), 0)); 내보내기(89);
            요구('('); potvrditi_TYPE(izraz_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) neuspjeh_VALUE("input stream constructor arguments"); potvrditi_TYPE(izraz_VALUE(), 2); 이어 = true; }
            요구(')');
            Naredba(183, vanjska_referenca(10, vlasnik_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = izraz_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(raščlanjivati_cijeli_broj(Pozicija++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Pozicija++); Naredba(19, Reference(8, znak_konstanta(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Pozicija++); if (znak_dužina != 1) neuspjeh_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String vlasnik_VALUE = "", metoda_VALUE = "", 서술 = ""; int 가 = 0, SECOND_operand = 0, 다 = 0, 라 = 0, 마 = 0, mjera = 0;
            if (TAKE_Word("Ispis")) {
                vlasnik_VALUE = "한국어/자체/Ispis"; 요구('.');
                if (TAKE_Word("pisati_redak")) { metoda_VALUE = "pisati_redak"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Piši")) { metoda_VALUE = "Piši"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { metoda_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else neuspjeh_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                vlasnik_VALUE = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("dužina_VALUE")) { metoda_VALUE = "dužina_VALUE"; 서술 = "(Ljava/lang/String;)I"; mjera = 1; }
                else if (TAKE_Word("kôd_znaka_COUNT")) { metoda_VALUE = "kôd_znaka_COUNT"; 서술 = "(Ljava/lang/String;)I"; mjera = 1; }
                else if (TAKE_Word("raščlanjivati_cijeli_broj")) { metoda_VALUE = "raščlanjivati_cijeli_broj"; 서술 = "(Ljava/lang/String;)I"; mjera = 1; }
                else if (TAKE_Word("pisati_cijeli_broj_VALUE")) { metoda_VALUE = "pisati_cijeli_broj_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; mjera = 3; }
                else if (TAKE_Word("같음")) { metoda_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECOND_operand = 3; mjera = 2; }
                else if (TAKE_Word("zalijepiti_SMS")) { metoda_VALUE = "zalijepiti_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECOND_operand = 3; mjera = 3; }
                else if (TAKE_Word("izrezati_VALUE")) { metoda_VALUE = "izrezati_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECOND_operand = 1; 다 = 1; mjera = 3; }
                else neuspjeh_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Fajl")) {
                vlasnik_VALUE = "한국어/자체/Fajl"; 요구('.'); 가 = 3;
                if (TAKE_Word("Čitaj")) { metoda_VALUE = "Čitaj"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; mjera = 3; }
                else if (TAKE_Word("Piši")) { metoda_VALUE = "Piši"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECOND_operand = 3; }
                else neuspjeh_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                vlasnik_VALUE = "한국어/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { metoda_VALUE = "너비"; 서술 = "()I"; mjera = 1; }
                else if (TAKE_Word("높이")) { metoda_VALUE = "높이"; 서술 = "()I"; mjera = 1; }
                else if (TAKE_Word("사각형")) { metoda_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; SECOND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("지우기")) { metoda_VALUE = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metoda_VALUE = "기다리기"; 서술 = "()V"; }
                else neuspjeh_VALUE("unknown Korean framebuffer method");
            } else neuspjeh_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) potvrditi_TYPE(izraz_VALUE(), 가);
            if (SECOND_operand != 0) { 요구(','); potvrditi_TYPE(izraz_VALUE(), SECOND_operand); }
            if (다 != 0) { 요구(','); potvrditi_TYPE(izraz_VALUE(), 다); }
            if (라 != 0) { 요구(','); potvrditi_TYPE(izraz_VALUE(), 라); }
            if (마 != 0) { 요구(','); potvrditi_TYPE(izraz_VALUE(), 마); }
            요구(')'); Naredba(184, vanjska_referenca(10, vlasnik_VALUE, metoda_VALUE, 서술)); return mjera;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); potvrditi_TYPE(izraz_VALUE(), 3); 요구(')');
            Naredba(184, vanjska_referenca(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Naziv = identifikator_VALUE();
        if (받기('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < metoda_COUNT; 수++) if (이름같음(Naziv, metoda_unos_naziv[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { neuspjeh_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!GRESKA && 종류() != ')') {
                if (수 >= metoda_argument_COUNT[FUNCTION_VALUE]) { neuspjeh_VALUE("too many arguments"); break; }
                potvrditi_TYPE(izraz_VALUE(), metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != metoda_argument_COUNT[FUNCTION_VALUE]) neuspjeh_VALUE("argument count mismatch");
            Naredba(184, Reference(10, klasa_konstanta, Reference(12, metoda_naziv_konstanta[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return metoda_vratiti[FUNCTION_VALUE];
        }
        int lokalni_opseg = FIND_lokalni(Naziv), TYPE_VALUE = lokalni_TYPE[lokalni_opseg]; 지역읽기(lokalni_opseg);
        while (!GRESKA) {
            if (받기('[')) { potvrditi_TYPE(TYPE_VALUE, 4); potvrditi_TYPE(izraz_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String vlasnik_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Naredba(182, vanjska_referenca(10, vlasnik_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Naredba(182, vanjska_referenca(10, vlasnik_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); potvrditi_TYPE(izraz_VALUE(), 1); 요구(')'); Naredba(182, vanjska_referenca(10, vlasnik_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { neuspjeh_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { potvrditi_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Naredba(182, vanjska_referenca(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { neuspjeh_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { potvrditi_TYPE(단항(), 2); Poređenje_VALUE(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(raščlanjivati_cijeli_broj(Pozicija++, true));
            else { potvrditi_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { potvrditi_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!GRESKA && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodiranje_VALUE = 종류(); Pozicija++; potvrditi_TYPE(TYPE_VALUE, 1); potvrditi_TYPE(단항(), 1);
            내보내기(kodiranje_VALUE == '*' ? 104 : kodiranje_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!GRESKA && (종류() == '+' || 종류() == '-')) {
            int kodiranje_VALUE = 종류(); Pozicija++; int 경계 = kod_podesiti_veličinu, ZAD_VALUE_TYPE = 곱식();
            if (kodiranje_VALUE == '+' && (TYPE_VALUE == 3 || ZAD_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, ZAD_VALUE_TYPE); TYPE_VALUE = 3; }
            else { potvrditi_TYPE(TYPE_VALUE, 1); potvrditi_TYPE(ZAD_VALUE_TYPE, 1); 내보내기(kodiranje_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) neuspjeh_VALUE("unsupported concatenation type");
        return vanjska_referenca(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int ZAD_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT kod_VALUE 앞에 generirati 코드를 삽입한다.
        // RIGHT izraz_VALUE 내부의 peer_VALUE ogranak 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = kod_podesiti_veličinu;
        Naredba(187, Reference(7, Word_konstanta("java/lang/StringBuilder"), 0)); 내보내기(89);
        Naredba(183, vanjska_referenca(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Naredba(182, 붙임참조(앞형));
        if (GRESKA) return;
        int dužina_VALUE = kod_podesiti_veličinu - 끝;
        for (int 수 = 0; 수 < dužina_VALUE; 수++) 삽입코드[수] = kod_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) kod_VALUE[수 + dužina_VALUE] = kod_VALUE[수];
        for (int 수 = 0; 수 < dužina_VALUE; 수++) kod_VALUE[경계 + 수] = 삽입코드[수];
        Naredba(182, 붙임참조(ZAD_VALUE_TYPE)); Naredba(182, vanjska_referenca(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Poređenje_izraz() {
        int TYPE_VALUE = 합식();
        while (!GRESKA && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodiranje_VALUE = 종류(); Pozicija++; potvrditi_TYPE(TYPE_VALUE, 1); potvrditi_TYPE(합식(), 1);
            Poređenje_VALUE(kodiranje_VALUE == '<' ? 161 : kodiranje_VALUE == '>' ? 163 : kodiranje_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Poređenje_izraz();
        while (!GRESKA && (종류() == 300 || 종류() == 301)) {
            int kodiranje_VALUE = 종류(); Pozicija++; int ZAD_VALUE_TYPE = Poređenje_izraz();
            if (TYPE_VALUE == 0 || ZAD_VALUE_TYPE == 0) neuspjeh_VALUE("void expression");
            if (!(cijeli_broj_TYPE(TYPE_VALUE) && cijeli_broj_TYPE(ZAD_VALUE_TYPE))) potvrditi_TYPE(ZAD_VALUE_TYPE, TYPE_VALUE);
            Poređenje_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (kodiranje_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!GRESKA && 받기(304)) {
            potvrditi_TYPE(TYPE_VALUE, 2); int 가 = ogranak(153); potvrditi_TYPE(동등식(), 2); int SECOND_operand = ogranak(153);
            내보내기(4); int 끝 = ogranak(167); Veza_VALUE(가, kod_podesiti_veličinu); Veza_VALUE(SECOND_operand, kod_podesiti_veličinu); 내보내기(3); Veza_VALUE(끝, kod_podesiti_veličinu); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int izraz_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!GRESKA && 받기(305)) {
            potvrditi_TYPE(TYPE_VALUE, 2); int 가 = ogranak(154); potvrditi_TYPE(논리곱(), 2); int SECOND_operand = ogranak(154);
            내보내기(3); int 끝 = ogranak(167); Veza_VALUE(가, kod_podesiti_veličinu); Veza_VALUE(SECOND_operand, kod_podesiti_veličinu); 내보내기(4); Veza_VALUE(끝, kod_podesiti_veličinu); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void zadatak_VALUE(boolean 선언허용) {
        if (Word_VALUE(Pozicija, "int") || Word_VALUE(Pozicija, "boolean") || Word_VALUE(Pozicija, "String") || Word_VALUE(Pozicija, "char")
            || Word_VALUE(Pozicija, "FileInputStream") || Word_VALUE(Pozicija, "FileOutputStream")) {
            if (!선언허용) neuspjeh_VALUE("declaration not allowed here");
            int TYPE_VALUE = format_VALUE(), Naziv = identifikator_VALUE(); 요구('='); potvrditi_TYPE(izraz_VALUE(), TYPE_VALUE);
            pisati_lokalni(dodati_lokalni(Naziv, TYPE_VALUE)); return;
        }
        int Naziv = identifikator_VALUE(), lokalni_opseg = FIND_lokalni(Naziv);
        if (받기('=')) { potvrditi_TYPE(izraz_VALUE(), lokalni_TYPE[lokalni_opseg]); pisati_lokalni(lokalni_opseg); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodiranje_VALUE = 종류(); Pozicija++; 지역읽기(lokalni_opseg); int 경계 = kod_podesiti_veličinu, ZAD_VALUE_TYPE = izraz_VALUE();
            if (kodiranje_VALUE == 308 && lokalni_TYPE[lokalni_opseg] == 3) 결합(경계, 3, ZAD_VALUE_TYPE);
            else {
                potvrditi_TYPE(lokalni_TYPE[lokalni_opseg], 1); potvrditi_TYPE(ZAD_VALUE_TYPE, 1);
                내보내기(kodiranje_VALUE == 308 ? 96 : kodiranje_VALUE == 309 ? 100 : kodiranje_VALUE == 310 ? 104 : kodiranje_VALUE == 311 ? 108 : 112);
                if (lokalni_TYPE[lokalni_opseg] == 5) 내보내기(146);
            }
            pisati_lokalni(lokalni_opseg);
        }
        else if (종류() == 306 || 종류() == 307) {
            potvrditi_TYPE(lokalni_TYPE[lokalni_opseg], 1); 내보내기(132); 내보내기(lokalni_opseg); 내보내기(종류() == 306 ? 1 : 255); Pozicija++;
            if (lokalni_TYPE[lokalni_opseg] == 5) { 지역읽기(lokalni_opseg); 내보내기(146); pisati_lokalni(lokalni_opseg); }
        } else neuspjeh_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Naredba(178, vanjska_referenca(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean prazno_argument = 종류() == ')';
        int TYPE_VALUE = prazno_argument ? 0 : izraz_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !prazno_argument)) neuspjeh_VALUE("unsupported print argument");
        Naredba(182, vanjska_referenca(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean izjava_VALUE() {
        if (GRESKA) return false;
        if (깊이 > 32) { neuspjeh_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean vratiti_mjera = false;
            while (!GRESKA && 종류() != '}') { if (vratiti_mjera) neuspjeh_VALUE("unreachable statement"); vratiti_mjera = izjava_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < lokalni_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return vratiti_mjera;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : izraz_VALUE(); potvrditi_TYPE(TYPE_VALUE, metoda_vratiti[trenutno_metoda]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); potvrditi_TYPE(izraz_VALUE(), 2); 요구(')'); int FALSE_VALUE = ogranak(153);
            깊이++; boolean 가 = kontrola_izjava(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = ogranak(167); Veza_VALUE(FALSE_VALUE, kod_podesiti_veličinu); 깊이++; boolean SECOND_operand = kontrola_izjava(); 깊이--; Veza_VALUE(끝, kod_podesiti_veličinu); return 가 && SECOND_operand; }
            Veza_VALUE(FALSE_VALUE, kod_podesiti_veličinu); return false;
        }
        if (TAKE_Word("while")) {
            int Pokreni = kod_podesiti_veličinu; 요구('('); potvrditi_TYPE(izraz_VALUE(), 2); 요구(')'); int 끝 = ogranak(153);
            깊이++; kontrola_izjava(); 깊이--; Veza_VALUE(ogranak(167), Pokreni); Veza_VALUE(끝, kod_podesiti_veličinu); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') zadatak_VALUE(true); 요구(';');
            int uvjet = kod_podesiti_veličinu; if (종류() == ';') 내보내기(4); else potvrditi_TYPE(izraz_VALUE(), 2); 요구(';');
            int 끝 = ogranak(153), tijelo_teksta = ogranak(167), osvježiti = kod_podesiti_veličinu;
            if (종류() != ')') zadatak_VALUE(false); 요구(')'); Veza_VALUE(ogranak(167), uvjet); Veza_VALUE(tijelo_teksta, kod_podesiti_veličinu);
            kontrola_izjava(); Veza_VALUE(ogranak(167), osvježiti); Veza_VALUE(끝, kod_podesiti_veličinu);
            for (int 수 = 0; 수 < lokalni_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Pozicija, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Pozicija + 1 < token_COUNT && (토큰종류[Pozicija + 1] == '(' || 토큰종류[Pozicija + 1] == '.')) {
            int TYPE_VALUE = izraz_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        zadatak_VALUE(true); 요구(';'); return false;
    }
    static boolean kontrola_izjava() {
        if (Word_VALUE(Pozicija, "int") || Word_VALUE(Pozicija, "boolean") || Word_VALUE(Pozicija, "char") || Word_VALUE(Pozicija, "String")
            || Word_VALUE(Pozicija, "FileInputStream") || Word_VALUE(Pozicija, "FileOutputStream")) neuspjeh_VALUE("local declaration requires braces");
        return izjava_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == Ispis.length) neuspjeh_VALUE("class file too large"); else Ispis[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void pisati_klasa() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstanta_COUNT);
        for (int 수 = 0; 수 < konstanta_podesiti_veličinu; 수++) 출바(konstanta_VALUE[수]);
        출짧(0x21); 출짧(klasa_konstanta); 출짧(roditelj_konstanta); 출짧(0); 출짧(0); 출짧(metoda_COUNT);
        for (int 수 = 0; 수 < metoda_COUNT; 수++) {
            출짧(metoda_pristup[수]); 출짧(metoda_naziv_konstanta[수]); 출짧(함수서술[수]); 출짧(1); 출짧(kod_konstanta);
            출정(12 + metoda_dužina[수]); 출짧(128); 출짧(함수지역[수]); 출정(metoda_dužina[수]);
            for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < metoda_dužina[수]; prostor_za_unos_unos++) 출바(kod_VALUE[metoda_kod[수] + prostor_za_unos_unos]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Pokreni() {
        if (korisnik.인수개수() == 1 && 자바도구.같음(korisnik.Argumenti(0), "-version")) {
            korisnik.Piši("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (korisnik.인수개수() != 1) { korisnik.Piši("Usage: javac FILE.java\n"); return 2; }
        int naziv_podesiti_veličinu = 자바도구.Naziv(fajl_naziv_SMS, korisnik.Argumenti(0));
        if (naziv_podesiti_veličinu < 6 || naziv_podesiti_veličinu > 62 || fajl_naziv_SMS[naziv_podesiti_veličinu - 5] != '.' || fajl_naziv_SMS[naziv_podesiti_veličinu - 4] != 'j'
            || fajl_naziv_SMS[naziv_podesiti_veličinu - 3] != 'a' || fajl_naziv_SMS[naziv_podesiti_veličinu - 2] != 'v' || fajl_naziv_SMS[naziv_podesiti_veličinu - 1] != 'a') {
            korisnik.Piši("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        izvor_podesiti_veličinu = korisnik.파일읽기(fajl_naziv_SMS, IZVOR);
        if (izvor_podesiti_veličinu < 0) { korisnik.Piši("javac: cannot read source: "); 자바도구.수쓰기(izvor_podesiti_veličinu); korisnik.pisati_znak_VALUE(10); return 1; }
        izvor_podesiti_veličinu = 자바도구.원문해독(IZVOR, izvor_podesiti_veličinu);
        if (izvor_podesiti_veličinu < 0) { korisnik.Piši("javac error: invalid UTF-8 source\n"); return 1; }
        izrezati_VALUE(); if (!GRESKA) 선언읽기();
        if (!GRESKA) {
            if (token_dužina[klasa_token] != naziv_podesiti_veličinu - 5) neuspjeh_VALUE("class name must match file name");
            for (int 수 = 0; 수 < naziv_podesiti_veličinu - 5; 수++) if (IZVOR[token_položaj[klasa_token] + 수] != fajl_naziv_SMS[수]) neuspjeh_VALUE("class name must match file name");
        }
        for (trenutno_metoda = 0; trenutno_metoda < metoda_COUNT && !GRESKA; trenutno_metoda++) {
            Pozicija = metoda_tijelo[trenutno_metoda]; metoda_kod[trenutno_metoda] = kod_podesiti_veličinu; lokalni_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metoda_argument_COUNT[trenutno_metoda]; 수++) dodati_lokalni(metoda_argument_naziv[trenutno_metoda * 16 + 수], metoda_argument_TYPE[trenutno_metoda * 16 + 수]);
            boolean vratiti_mjera = izjava_VALUE();
            if (!vratiti_mjera && metoda_vratiti[trenutno_metoda] != 0) neuspjeh_VALUE("missing return");
            // ogranak 뒤의 합류 지점은 반드시 stvaran_podaci 명령이어야 한다 (버전 49 검증기).
            if (metoda_vratiti[trenutno_metoda] == 0) 내보내기(177);
            else { boolean cijeli_broj = metoda_vratiti[trenutno_metoda] <= 2 || metoda_vratiti[trenutno_metoda] == 5; 내보내기(cijeli_broj ? 3 : 1); 내보내기(cijeli_broj ? 172 : 176); }
            if (Pozicija != metoda_završiti[trenutno_metoda]) neuspjeh_VALUE("invalid method body");
            함수지역[trenutno_metoda] = lokalni_COUNT; metoda_dužina[trenutno_metoda] = kod_podesiti_veličinu - metoda_kod[trenutno_metoda];
        }
        if (GRESKA) return 1;
        pisati_klasa(); if (GRESKA) return 1;
        fajl_naziv_SMS[naziv_podesiti_veličinu - 4] = 'c'; fajl_naziv_SMS[naziv_podesiti_veličinu - 3] = 'l'; fajl_naziv_SMS[naziv_podesiti_veličinu - 2] = 'a';
        fajl_naziv_SMS[naziv_podesiti_veličinu - 1] = 's'; fajl_naziv_SMS[naziv_podesiti_veličinu] = 's'; fajl_naziv_SMS[naziv_podesiti_veličinu + 1] = 0;
        int mjera = korisnik.pisati_fajl(fajl_naziv_SMS, Ispis, 출력크기);
        if (mjera < 0) { korisnik.Piši("javac: cannot save class: "); 자바도구.수쓰기(mjera); korisnik.pisati_znak_VALUE(10); return 1; }
        korisnik.Piši("Compiled: "); for (int 수 = 0; fajl_naziv_SMS[수] != 0; 수++) korisnik.pisati_znak_VALUE(fajl_naziv_SMS[수]);
        korisnik.Piši(" (JVM class version 49)\n"); return 0;
    }
}
