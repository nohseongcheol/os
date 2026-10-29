// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java izvor_stablo -> 표준 버전 49 class kompajler. */
public final class 자바컴파일러 {
    static int[] izvor = new int[16384], 출력 = new int[16384], kôd_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_pozicija = new int[2048], 토큰길이 = new int[2048];
    static int[] konstanta_VALUE = new int[4096], konstanta_Pomak = new int[512];
    static int[] 문자 = new int[512], ime_datoteke_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int izvor_promeniti_veličinu, token_COUNT, pozicija, kôd_promeniti_veličinu, konstanta_promeniti_veličinu, konstanta_COUNT = 1, 출력크기, 문자수;
    static boolean greška;
    static int Razred_token, Razred_konstanta, nadređen_konstanta, kôd_konstanta;
    static int[] metod_stavka_ime = new int[32], metod_vratiti = new int[32], metod_argument_COUNT = new int[32];
    static int[] metod_argument_ime = new int[512], metod_argument_tip = new int[512];
    static int[] metod_telo = new int[32], metod_završiti_razgovor = new int[32], metod_kôd = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], metod_ime_konstanta = new int[32], 함수서술 = new int[32];
    static int[] metod_pristup = new int[32];
    static int metod_COUNT, aktuelno_metod, lokalni_COUNT, 깊이, 식깊이;
    static int[] lokalni_ime = new int[128], lokalni_tip = new int[128], 지역깊이 = new int[128];

    static void otkazivanje_VALUE(String 이유) {
        if (!greška) {
            korisnik.쓰기("javac error: "); korisnik.쓰기(이유);
            korisnik.쓰기(" at line ");
            int red = 1, 끝 = pozicija < token_COUNT ? token_pozicija[pozicija] : izvor_promeniti_veličinu;
            for (int 수 = 0; 수 < 끝; 수++) if (izvor[수] == 10) red++;
            자바도구.수쓰기(red); korisnik.문자쓰기(10);
        }
        greška = true;
    }
    static boolean znak_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean cifra_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int SECOND_operand) {
        if (가 < 0 || SECOND_operand < 0 || 가 >= token_COUNT || SECOND_operand >= token_COUNT || 토큰길이[가] != 토큰길이[SECOND_operand]) return false;
        for (int 수 = 0; 수 < 토큰길이[가]; 수++) if (izvor[token_pozicija[가] + 수] != izvor[token_pozicija[SECOND_operand] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int token_VALUE, String Word_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || 토큰길이[token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (izvor[token_pozicija[token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return pozicija < token_COUNT ? 토큰종류[pozicija] : 0; }
    static boolean primiti(int VALUE) { if (종류() != VALUE) return false; pozicija++; return true; }
    static void zahtev_VALUE(int VALUE) { if (!primiti(VALUE)) otkazivanje_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(pozicija, Word_SMS)) return false; pozicija++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) otkazivanje_VALUE(Word_SMS); }
    static int identifikator_VALUE() {
        int KR = pozicija;
        if (종류() != 256) otkazivanje_VALUE("identifier required"); else pozicija++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int koristiti = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - koristiti == 토큰길이[KR];
                for (int 칸 = koristiti; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != izvor[token_pozicija[KR] + 칸 - koristiti]) 같음 = false;
                if (같음) otkazivanje_VALUE("reserved word cannot be an identifier");
                koristiti = 수 + 1;
            }
        }
        return KR;
    }
    static void iseći_VALUE() {
        int 수 = 0;
        while (수 < izvor_promeniti_veličinu && !greška) {
            int VALUE = izvor[수], koristiti = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < izvor_promeniti_veličinu && izvor[수 + 1] == '/') {
                while (수 < izvor_promeniti_veličinu && izvor[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < izvor_promeniti_veličinu && izvor[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < izvor_promeniti_veličinu && !(izvor[수] == '*' && izvor[수 + 1] == '/')) 수++;
                if (수 + 1 >= izvor_promeniti_veličinu) { otkazivanje_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (znak_VALUE(VALUE)) { 종류 = 256; while (수 < izvor_promeniti_veličinu && 문자이름규칙.이어진글자(izvor[수])) 수++; }
            else if (cifra_VALUE(VALUE)) { 종류 = 257; while (수 < izvor_promeniti_veličinu && cifra_VALUE(izvor[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < izvor_promeniti_veličinu && izvor[수] != VALUE && izvor[수] != 10 && izvor[수] != 13) {
                    if (izvor[수] == '\\') 수++;
                    수++;
                }
                if (수 >= izvor_promeniti_veličinu || izvor[수] != VALUE) { otkazivanje_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < izvor_promeniti_veličinu) {
                    int Dalje_stavka = izvor[수];
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
            if (token_COUNT == 토큰종류.length - 1) { otkazivanje_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_pozicija[token_COUNT] = koristiti; 토큰길이[token_COUNT++] = 수 - koristiti;
        }
    }
    static void 상바(int VALUE) {
        if (konstanta_promeniti_veličinu == konstanta_VALUE.length) { otkazivanje_VALUE("constant pool too large"); return; }
        konstanta_VALUE[konstanta_promeniti_veličinu++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { 상바(VALUE >> 8); 상바(VALUE); }
    static int registar_konstanta(int koristiti) {
        for (int 수 = 1; 수 < konstanta_COUNT; 수++) {
            int čeona_kamera_VALUE = konstanta_Pomak[수], 길이 = (수 + 1 < konstanta_COUNT ? konstanta_Pomak[수 + 1] : koristiti) - čeona_kamera_VALUE;
            if (길이 != konstanta_promeniti_veličinu - koristiti) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (konstanta_VALUE[čeona_kamera_VALUE + 칸] != konstanta_VALUE[koristiti + 칸]) 같음 = false;
            if (같음) { konstanta_promeniti_veličinu = koristiti; return 수; }
        }
        if (konstanta_COUNT == konstanta_Pomak.length) { otkazivanje_VALUE("too many constants"); return 0; }
        konstanta_Pomak[konstanta_COUNT] = koristiti;
        return konstanta_COUNT++;
    }
    static void dodati_SMS(int VALUE) {
        if (문자수 == 문자.length) { otkazivanje_VALUE("text too long"); return; }
        문자[문자수++] = VALUE;
    }
    static void dodati_Word(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) dodati_SMS(Word_SMS.charAt(수)); }
    static int znak_konstanta() {
        int koristiti = konstanta_promeniti_veličinu; 상바(1); 상짧(0);
        for (int 수 = 0; 수 < 문자수; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) 상바(VALUE);
            else if (VALUE < 2048) { 상바(192 | VALUE >> 6); 상바(128 | VALUE & 63); }
            else { 상바(224 | VALUE >> 12); 상바(128 | VALUE >> 6 & 63); 상바(128 | VALUE & 63); }
        }
        if (greška) return 0;
        int 길이 = konstanta_promeniti_veličinu - koristiti - 3;
        konstanta_VALUE[koristiti + 1] = 길이 >> 8; konstanta_VALUE[koristiti + 2] = 길이 & 255;
        return registar_konstanta(koristiti);
    }
    static int Word_konstanta(String Word_SMS) { 문자수 = 0; dodati_Word(Word_SMS); return znak_konstanta(); }
    static int token_konstanta(int token_VALUE) {
        문자수 = 0;
        for (int 수 = 0; 수 < 토큰길이[token_VALUE]; 수++) dodati_SMS(izvor[token_pozicija[token_VALUE] + 수]);
        return znak_konstanta();
    }
    static int referenca(int 종류, int 가, int SECOND_operand) {
        int koristiti = konstanta_promeniti_veličinu; 상바(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SECOND_operand);
        return registar_konstanta(koristiti);
    }
    static int spoljni_referenca(int 종류, String vlasnik_VALUE, String ime, String 서술) {
        int vlasnik_identifikator = referenca(7, Word_konstanta(vlasnik_VALUE), 0);
        int ime_COUNT = Word_konstanta(ime), format_COUNT = Word_konstanta(서술);
        return referenca(종류, vlasnik_identifikator, referenca(12, ime_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (kôd_promeniti_veličinu == kôd_VALUE.length) { otkazivanje_VALUE("bytecode too large"); return; }
        kôd_VALUE[kôd_promeniti_veličinu++] = VALUE & 255;
    }
    static void komanda(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int koristiti = konstanta_promeniti_veličinu; 상바(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        komanda(19, registar_konstanta(koristiti));
    }
    static int grana(int komanda) { int KR = kôd_promeniti_veličinu; komanda(komanda, 0); return KR; }
    static void Veza_VALUE(int grana, int cilj_objekat) {
        if (greška) return;
        int 거리 = cilj_objekat - grana;
        if (거리 < -32768 || 거리 > 32767 || grana < 0 || grana + 2 >= kôd_promeniti_veličinu) { otkazivanje_VALUE("invalid branch"); return; }
        kôd_VALUE[grana + 1] = 거리 >> 8 & 255; kôd_VALUE[grana + 2] = 거리 & 255;
    }
    static void Poređenje_VALUE(int komanda) {
        int TRUE_VALUE = grana(komanda); 내보내기(3); int 끝 = grana(167);
        Veza_VALUE(TRUE_VALUE, kôd_promeniti_veličinu); 내보내기(4); Veza_VALUE(끝, kôd_promeniti_veličinu);
    }
    static int format_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (primiti('[')) { zahtev_VALUE(']'); return 4; } return 3; }
        otkazivanje_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Dodaj_format(int tip_VALUE) {
        if (tip_VALUE == 0) dodati_SMS('V');
        if (tip_VALUE == 1) dodati_SMS('I');
        if (tip_VALUE == 2) dodati_SMS('Z');
        if (tip_VALUE == 3) dodati_Word("Ljava/lang/String;");
        if (tip_VALUE == 4) dodati_Word("[Ljava/lang/String;");
        if (tip_VALUE == 5) dodati_SMS('C');
        if (tip_VALUE == 6) dodati_Word("Ljava/io/FileInputStream;");
        if (tip_VALUE == 7) dodati_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklaracija. izuzetak Proces_VALUE_stavka 본문은 host javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("한국어");
        if (한국어묶음) { zahtev_VALUE('.'); 말요구("자체"); zahtev_VALUE('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("izuzetak") || TAKE_Word("실행예외") || TAKE_Word("U_I_izuzetak") || TAKE_Word("čekaj_TIMEOUT_izuzetak") || TAKE_Word("adresa_LOOKUP_izuzetak") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("nevažeći_argument_izuzetak") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_referenca_izuzetak") || TAKE_Word("산술예외") || TAKE_Word("Status_izuzetak") || TAKE_Word("tip_Emitovanje_izuzetak") || TAKE_Word("음수배열크기예외") || TAKE_Word("niz_Store_otkazivanje") || TAKE_Word("nit_Status_izuzetak") || TAKE_Word("대기중단예외")) return;
        otkazivanje_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(pozicija, "한국어")) 예외이름읽기();
            else {
                말요구("java"); zahtev_VALUE('.'); 말요구("io"); zahtev_VALUE('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) otkazivanje_VALUE("unsupported import");
            }
            zahtev_VALUE(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); Razred_token = identifikator_VALUE();
        Razred_konstanta = referenca(7, token_konstanta(Razred_token), 0);
        nadređen_konstanta = referenca(7, Word_konstanta("java/lang/Object"), 0); kôd_konstanta = Word_konstanta("Code"); zahtev_VALUE('{');
        while (!greška && 종류() != '}') {
            if (metod_COUNT == 32) { otkazivanje_VALUE("too many methods"); break; }
            int pristup_stavka = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = metod_COUNT++;
            metod_pristup[FUNCTION_VALUE] = pristup_stavka | 8;
            metod_vratiti[FUNCTION_VALUE] = format_VALUE(); metod_stavka_ime[FUNCTION_VALUE] = identifikator_VALUE(); zahtev_VALUE('(');
            for (int čeona_kamera_VALUE = 0; čeona_kamera_VALUE < FUNCTION_VALUE; čeona_kamera_VALUE++) if (이름같음(metod_stavka_ime[čeona_kamera_VALUE], metod_stavka_ime[FUNCTION_VALUE])) otkazivanje_VALUE("duplicate method (overloading unsupported)");
            while (!greška && 종류() != ')') {
                int 수 = metod_argument_COUNT[FUNCTION_VALUE];
                if (수 == 16) { otkazivanje_VALUE("too many parameters"); break; }
                int tip_VALUE = format_VALUE(); if (tip_VALUE == 0) otkazivanje_VALUE("void parameter");
                metod_argument_tip[FUNCTION_VALUE * 16 + 수] = tip_VALUE; metod_argument_ime[FUNCTION_VALUE * 16 + 수] = identifikator_VALUE();
                metod_argument_COUNT[FUNCTION_VALUE]++;
                if (!primiti(',')) break;
            }
            zahtev_VALUE(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!greška && primiti(','));
            }
            metod_telo[FUNCTION_VALUE] = pozicija; zahtev_VALUE('{');
            int ugnežđivanje_VALUE = 1;
            while (pozicija < token_COUNT && ugnežđivanje_VALUE > 0) {
                if (종류() == '{') ugnežđivanje_VALUE++;
                if (종류() == '}') ugnežđivanje_VALUE--;
                pozicija++;
            }
            if (ugnežđivanje_VALUE != 0) otkazivanje_VALUE("unclosed method body");
            metod_završiti_razgovor[FUNCTION_VALUE] = pozicija;
            metod_ime_konstanta[FUNCTION_VALUE] = token_konstanta(metod_stavka_ime[FUNCTION_VALUE]);
            문자수 = 0; dodati_SMS('(');
            for (int 수 = 0; 수 < metod_argument_COUNT[FUNCTION_VALUE]; 수++) Dodaj_format(metod_argument_tip[FUNCTION_VALUE * 16 + 수]);
            dodati_SMS(')'); Dodaj_format(metod_vratiti[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = znak_konstanta();
        }
        zahtev_VALUE('}'); if (pozicija != token_COUNT) otkazivanje_VALUE("extra input after class");
    }
    static int FIND_lokalni(int ime) {
        for (int 수 = lokalni_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokalni_ime[수], ime)) return 수;
        otkazivanje_VALUE("unknown variable"); return 0;
    }
    static int Dodaj_lokalni(int ime, int tip_VALUE) {
        for (int 수 = 0; 수 < lokalni_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokalni_ime[수], ime)) otkazivanje_VALUE("duplicate local variable");
        if (lokalni_COUNT == 128) { otkazivanje_VALUE("too many locals"); return 0; }
        lokalni_ime[lokalni_COUNT] = ime; lokalni_tip[lokalni_COUNT] = tip_VALUE; 지역깊이[lokalni_COUNT] = 깊이;
        return lokalni_COUNT++;
    }
    static boolean ceo_broj_tip(int tip_VALUE) { return tip_VALUE == 1 || tip_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokalni_tip[수] <= 2 || lokalni_tip[수] == 5 ? 21 : 25); 내보내기(수); }
    static void 지역쓰기(int 수) { 내보내기(lokalni_tip[수] <= 2 || lokalni_tip[수] == 5 ? 54 : 58); 내보내기(수); }
    static void verifikovati_tip(int stvarni_podaci, int 기대) { if (stvarni_podaci != 기대 && !(stvarni_podaci == 5 && 기대 == 1)) otkazivanje_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        문자수 = 0; int koristiti = token_pozicija[token_VALUE] + 1, 끝 = token_pozicija[token_VALUE] + 토큰길이[token_VALUE] - 1;
        while (koristiti < 끝 && !greška) {
            int VALUE = izvor[koristiti++];
            if (VALUE == '\\') {
                if (koristiti == 끝) { otkazivanje_VALUE("invalid escape"); break; }
                VALUE = izvor[koristiti++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') otkazivanje_VALUE("unsupported escape");
            }
            dodati_SMS(VALUE);
        }
    }
    static int raščlaniti_ceo_broj(int token_VALUE, boolean 음수) {
        if (토큰길이[token_VALUE] > 1 && izvor[token_pozicija[token_VALUE]] == '0') otkazivanje_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < 토큰길이[token_VALUE]; 수++) {
            int cifra_stavka = izvor[token_pozicija[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && cifra_stavka > (음수 ? 8 : 7)) otkazivanje_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - cifra_stavka;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int tip_VALUE = format_VALUE();
            if (tip_VALUE != 6 && tip_VALUE != 7) { otkazivanje_VALUE("only file streams supported by new in source"); return 0; }
            String vlasnik_VALUE = tip_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            komanda(187, referenca(7, Word_konstanta(vlasnik_VALUE), 0)); 내보내기(89);
            zahtev_VALUE('('); verifikovati_tip(izraz_VALUE(), 3); boolean 이어 = false;
            if (primiti(',')) { if (tip_VALUE != 7) otkazivanje_VALUE("input stream constructor arguments"); verifikovati_tip(izraz_VALUE(), 2); 이어 = true; }
            zahtev_VALUE(')');
            komanda(183, spoljni_referenca(10, vlasnik_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return tip_VALUE;
        }
        if (primiti('(')) { int tip_VALUE = izraz_VALUE(); zahtev_VALUE(')'); return tip_VALUE; }
        if (종류() == 257) { 수상수(raščlaniti_ceo_broj(pozicija++, false)); return 1; }
        if (종류() == 258) { 문자읽기(pozicija++); komanda(19, referenca(8, znak_konstanta(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(pozicija++); if (문자수 != 1) otkazivanje_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("한국어")) {
            zahtev_VALUE('.'); 말요구("자체"); zahtev_VALUE('.');
            String vlasnik_VALUE = "", metod_VALUE = "", 서술 = ""; int 가 = 0, SECOND_operand = 0, 다 = 0, 라 = 0, 마 = 0, KR = 0;
            if (TAKE_Word("출력")) {
                vlasnik_VALUE = "한국어/자체/출력"; zahtev_VALUE('.');
                if (TAKE_Word("줄쓰기")) { metod_VALUE = "줄쓰기"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("쓰기")) { metod_VALUE = "쓰기"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { metod_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else otkazivanje_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                vlasnik_VALUE = "한국어/자체/문자"; zahtev_VALUE('.'); 가 = 3;
                if (TAKE_Word("길이")) { metod_VALUE = "길이"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAKE_Word("kôd_znaka_COUNT")) { metod_VALUE = "kôd_znaka_COUNT"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAKE_Word("raščlaniti_ceo_broj")) { metod_VALUE = "raščlaniti_ceo_broj"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAKE_Word("정수쓰기")) { metod_VALUE = "정수쓰기"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; KR = 3; }
                else if (TAKE_Word("같음")) { metod_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECOND_operand = 3; KR = 2; }
                else if (TAKE_Word("nalepiti_SMS")) { metod_VALUE = "nalepiti_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECOND_operand = 3; KR = 3; }
                else if (TAKE_Word("iseći_VALUE")) { metod_VALUE = "iseći_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECOND_operand = 1; 다 = 1; KR = 3; }
                else otkazivanje_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Datoteka")) {
                vlasnik_VALUE = "한국어/자체/Datoteka"; zahtev_VALUE('.'); 가 = 3;
                if (TAKE_Word("읽기")) { metod_VALUE = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; KR = 3; }
                else if (TAKE_Word("쓰기")) { metod_VALUE = "쓰기"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECOND_operand = 3; }
                else otkazivanje_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                vlasnik_VALUE = "한국어/자체/화면"; zahtev_VALUE('.');
                if (TAKE_Word("너비")) { metod_VALUE = "너비"; 서술 = "()I"; KR = 1; }
                else if (TAKE_Word("높이")) { metod_VALUE = "높이"; 서술 = "()I"; KR = 1; }
                else if (TAKE_Word("사각형")) { metod_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; SECOND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("obrisati_stavka")) { metod_VALUE = "obrisati_stavka"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metod_VALUE = "기다리기"; 서술 = "()V"; }
                else otkazivanje_VALUE("unknown Korean framebuffer method");
            } else otkazivanje_VALUE("unsupported Korean library class");
            zahtev_VALUE('('); if (가 != 0) verifikovati_tip(izraz_VALUE(), 가);
            if (SECOND_operand != 0) { zahtev_VALUE(','); verifikovati_tip(izraz_VALUE(), SECOND_operand); }
            if (다 != 0) { zahtev_VALUE(','); verifikovati_tip(izraz_VALUE(), 다); }
            if (라 != 0) { zahtev_VALUE(','); verifikovati_tip(izraz_VALUE(), 라); }
            if (마 != 0) { zahtev_VALUE(','); verifikovati_tip(izraz_VALUE(), 마); }
            zahtev_VALUE(')'); komanda(184, spoljni_referenca(10, vlasnik_VALUE, metod_VALUE, 서술)); return KR;
        }
        if (TAKE_Word("Integer")) {
            zahtev_VALUE('.'); 말요구("parseInt"); zahtev_VALUE('('); verifikovati_tip(izraz_VALUE(), 3); zahtev_VALUE(')');
            komanda(184, spoljni_referenca(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int ime = identifikator_VALUE();
        if (primiti('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < metod_COUNT; 수++) if (이름같음(ime, metod_stavka_ime[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { otkazivanje_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!greška && 종류() != ')') {
                if (수 >= metod_argument_COUNT[FUNCTION_VALUE]) { otkazivanje_VALUE("too many arguments"); break; }
                verifikovati_tip(izraz_VALUE(), metod_argument_tip[FUNCTION_VALUE * 16 + 수++]); if (!primiti(',')) break;
            }
            zahtev_VALUE(')'); if (수 != metod_argument_COUNT[FUNCTION_VALUE]) otkazivanje_VALUE("argument count mismatch");
            komanda(184, referenca(10, Razred_konstanta, referenca(12, metod_ime_konstanta[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return metod_vratiti[FUNCTION_VALUE];
        }
        int lokalni_skup = FIND_lokalni(ime), tip_VALUE = lokalni_tip[lokalni_skup]; 지역읽기(lokalni_skup);
        while (!greška) {
            if (primiti('[')) { verifikovati_tip(tip_VALUE, 4); verifikovati_tip(izraz_VALUE(), 1); zahtev_VALUE(']'); 내보내기(50); tip_VALUE = 3; }
            else if (primiti('.')) {
                if (tip_VALUE == 6 || tip_VALUE == 7) {
                    String vlasnik_VALUE = tip_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { zahtev_VALUE('('); zahtev_VALUE(')'); komanda(182, spoljni_referenca(10, vlasnik_VALUE, "close", "()V")); tip_VALUE = 0; }
                    else if (tip_VALUE == 6 && TAKE_Word("read")) { zahtev_VALUE('('); zahtev_VALUE(')'); komanda(182, spoljni_referenca(10, vlasnik_VALUE, "read", "()I")); tip_VALUE = 1; }
                    else if (tip_VALUE == 7 && TAKE_Word("write")) { zahtev_VALUE('('); verifikovati_tip(izraz_VALUE(), 1); zahtev_VALUE(')'); komanda(182, spoljni_referenca(10, vlasnik_VALUE, "write", "(I)V")); tip_VALUE = 0; }
                    else { otkazivanje_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (tip_VALUE == 4) { 내보내기(190); tip_VALUE = 1; }
                else { verifikovati_tip(tip_VALUE, 3); zahtev_VALUE('('); zahtev_VALUE(')'); komanda(182, spoljni_referenca(10, "java/lang/String", "length", "()I")); tip_VALUE = 1; }
            } else break;
        }
        return tip_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { otkazivanje_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int tip_VALUE;
        if (primiti('!')) { verifikovati_tip(단항(), 2); Poređenje_VALUE(153); tip_VALUE = 2; }
        else if (primiti('-')) {
            if (종류() == 257) 수상수(raščlaniti_ceo_broj(pozicija++, true));
            else { verifikovati_tip(단항(), 1); 내보내기(116); }
            tip_VALUE = 1;
        } else if (primiti('+')) { verifikovati_tip(단항(), 1); tip_VALUE = 1; }
        else tip_VALUE = 기본식();
        식깊이--; return tip_VALUE;
    }
    static int 곱식() {
        int tip_VALUE = 단항();
        while (!greška && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodiranje_VALUE = 종류(); pozicija++; verifikovati_tip(tip_VALUE, 1); verifikovati_tip(단항(), 1);
            내보내기(kodiranje_VALUE == '*' ? 104 : kodiranje_VALUE == '/' ? 108 : 112); tip_VALUE = 1;
        }
        return tip_VALUE;
    }
    static int 합식() {
        int tip_VALUE = 곱식();
        while (!greška && (종류() == '+' || 종류() == '-')) {
            int kodiranje_VALUE = 종류(); pozicija++; int 경계 = kôd_promeniti_veličinu, NAZAD_VALUE_tip = 곱식();
            if (kodiranje_VALUE == '+' && (tip_VALUE == 3 || NAZAD_VALUE_tip == 3)) { 결합(경계, tip_VALUE, NAZAD_VALUE_tip); tip_VALUE = 3; }
            else { verifikovati_tip(tip_VALUE, 1); verifikovati_tip(NAZAD_VALUE_tip, 1); 내보내기(kodiranje_VALUE == '+' ? 96 : 100); tip_VALUE = 1; }
        }
        return tip_VALUE;
    }
    static int 붙임참조(int tip_VALUE) {
        if (tip_VALUE != 1 && tip_VALUE != 2 && tip_VALUE != 3 && tip_VALUE != 5) otkazivanje_VALUE("unsupported concatenation type");
        return spoljni_referenca(10, "java/lang/StringBuilder", "append", tip_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : tip_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : tip_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int čeona_kamera_VALUE_tip, int NAZAD_VALUE_tip) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT kôd_VALUE 앞에 generisati 코드를 삽입한다.
        // RIGHT izraz_VALUE 내부의 ravnopravni_uređaj_VALUE grana 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = kôd_promeniti_veličinu;
        komanda(187, referenca(7, Word_konstanta("java/lang/StringBuilder"), 0)); 내보내기(89);
        komanda(183, spoljni_referenca(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); komanda(182, 붙임참조(čeona_kamera_VALUE_tip));
        if (greška) return;
        int 길이 = kôd_promeniti_veličinu - 끝;
        for (int 수 = 0; 수 < 길이; 수++) 삽입코드[수] = kôd_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) kôd_VALUE[수 + 길이] = kôd_VALUE[수];
        for (int 수 = 0; 수 < 길이; 수++) kôd_VALUE[경계 + 수] = 삽입코드[수];
        komanda(182, 붙임참조(NAZAD_VALUE_tip)); komanda(182, spoljni_referenca(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Poređenje_izraz() {
        int tip_VALUE = 합식();
        while (!greška && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodiranje_VALUE = 종류(); pozicija++; verifikovati_tip(tip_VALUE, 1); verifikovati_tip(합식(), 1);
            Poređenje_VALUE(kodiranje_VALUE == '<' ? 161 : kodiranje_VALUE == '>' ? 163 : kodiranje_VALUE == 302 ? 164 : 162); tip_VALUE = 2;
        }
        return tip_VALUE;
    }
    static int 동등식() {
        int tip_VALUE = Poređenje_izraz();
        while (!greška && (종류() == 300 || 종류() == 301)) {
            int kodiranje_VALUE = 종류(); pozicija++; int NAZAD_VALUE_tip = Poređenje_izraz();
            if (tip_VALUE == 0 || NAZAD_VALUE_tip == 0) otkazivanje_VALUE("void expression");
            if (!(ceo_broj_tip(tip_VALUE) && ceo_broj_tip(NAZAD_VALUE_tip))) verifikovati_tip(NAZAD_VALUE_tip, tip_VALUE);
            Poređenje_VALUE((tip_VALUE <= 2 || tip_VALUE == 5 ? 159 : 165) + (kodiranje_VALUE == 301 ? 1 : 0)); tip_VALUE = 2;
        }
        return tip_VALUE;
    }
    static int I() {
        int tip_VALUE = 동등식();
        while (!greška && primiti(304)) {
            verifikovati_tip(tip_VALUE, 2); int 가 = grana(153); verifikovati_tip(동등식(), 2); int SECOND_operand = grana(153);
            내보내기(4); int 끝 = grana(167); Veza_VALUE(가, kôd_promeniti_veličinu); Veza_VALUE(SECOND_operand, kôd_promeniti_veličinu); 내보내기(3); Veza_VALUE(끝, kôd_promeniti_veličinu); tip_VALUE = 2;
        }
        return tip_VALUE;
    }
    static int izraz_VALUE() {
        int tip_VALUE = I();
        while (!greška && primiti(305)) {
            verifikovati_tip(tip_VALUE, 2); int 가 = grana(154); verifikovati_tip(I(), 2); int SECOND_operand = grana(154);
            내보내기(3); int 끝 = grana(167); Veza_VALUE(가, kôd_promeniti_veličinu); Veza_VALUE(SECOND_operand, kôd_promeniti_veličinu); 내보내기(4); Veza_VALUE(끝, kôd_promeniti_veličinu); tip_VALUE = 2;
        }
        return tip_VALUE;
    }
    static void dodela_VALUE(boolean Dozvoli_deklaracija) {
        if (Word_VALUE(pozicija, "int") || Word_VALUE(pozicija, "boolean") || Word_VALUE(pozicija, "String") || Word_VALUE(pozicija, "char")
            || Word_VALUE(pozicija, "FileInputStream") || Word_VALUE(pozicija, "FileOutputStream")) {
            if (!Dozvoli_deklaracija) otkazivanje_VALUE("declaration not allowed here");
            int tip_VALUE = format_VALUE(), ime = identifikator_VALUE(); zahtev_VALUE('='); verifikovati_tip(izraz_VALUE(), tip_VALUE);
            지역쓰기(Dodaj_lokalni(ime, tip_VALUE)); return;
        }
        int ime = identifikator_VALUE(), lokalni_skup = FIND_lokalni(ime);
        if (primiti('=')) { verifikovati_tip(izraz_VALUE(), lokalni_tip[lokalni_skup]); 지역쓰기(lokalni_skup); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodiranje_VALUE = 종류(); pozicija++; 지역읽기(lokalni_skup); int 경계 = kôd_promeniti_veličinu, NAZAD_VALUE_tip = izraz_VALUE();
            if (kodiranje_VALUE == 308 && lokalni_tip[lokalni_skup] == 3) 결합(경계, 3, NAZAD_VALUE_tip);
            else {
                verifikovati_tip(lokalni_tip[lokalni_skup], 1); verifikovati_tip(NAZAD_VALUE_tip, 1);
                내보내기(kodiranje_VALUE == 308 ? 96 : kodiranje_VALUE == 309 ? 100 : kodiranje_VALUE == 310 ? 104 : kodiranje_VALUE == 311 ? 108 : 112);
                if (lokalni_tip[lokalni_skup] == 5) 내보내기(146);
            }
            지역쓰기(lokalni_skup);
        }
        else if (종류() == 306 || 종류() == 307) {
            verifikovati_tip(lokalni_tip[lokalni_skup], 1); 내보내기(132); 내보내기(lokalni_skup); 내보내기(종류() == 306 ? 1 : 255); pozicija++;
            if (lokalni_tip[lokalni_skup] == 5) { 지역읽기(lokalni_skup); 내보내기(146); 지역쓰기(lokalni_skup); }
        } else otkazivanje_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); zahtev_VALUE('.'); 말요구("out"); zahtev_VALUE('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); zahtev_VALUE('(');
        komanda(178, spoljni_referenca(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int tip_VALUE = 빈인수 ? 0 : izraz_VALUE(); zahtev_VALUE(')'); zahtev_VALUE(';');
        String 서술 = tip_VALUE == 0 ? "()V" : tip_VALUE == 1 ? "(I)V" : tip_VALUE == 2 ? "(Z)V" : tip_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (tip_VALUE == 4 || tip_VALUE >= 6 || tip_VALUE == 0 && (!줄바꿈 || !빈인수)) otkazivanje_VALUE("unsupported print argument");
        komanda(182, spoljni_referenca(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean instrukcija_VALUE() {
        if (greška) return false;
        if (깊이 > 32) { otkazivanje_VALUE("statement nesting too deep"); return false; }
        if (primiti('{')) {
            깊이++; boolean vratiti_KR = false;
            while (!greška && 종류() != '}') { if (vratiti_KR) otkazivanje_VALUE("unreachable statement"); vratiti_KR = instrukcija_VALUE(); }
            zahtev_VALUE('}'); for (int 수 = 0; 수 < lokalni_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return vratiti_KR;
        }
        if (primiti(';')) return false;
        if (TAKE_Word("return")) {
            int tip_VALUE = 종류() == ';' ? 0 : izraz_VALUE(); verifikovati_tip(tip_VALUE, metod_vratiti[aktuelno_metod]); zahtev_VALUE(';');
            내보내기(tip_VALUE == 0 ? 177 : tip_VALUE <= 2 || tip_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            zahtev_VALUE('('); verifikovati_tip(izraz_VALUE(), 2); zahtev_VALUE(')'); int FALSE_VALUE = grana(153);
            깊이++; boolean 가 = kontrola_instrukcija(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = grana(167); Veza_VALUE(FALSE_VALUE, kôd_promeniti_veličinu); 깊이++; boolean SECOND_operand = kontrola_instrukcija(); 깊이--; Veza_VALUE(끝, kôd_promeniti_veličinu); return 가 && SECOND_operand; }
            Veza_VALUE(FALSE_VALUE, kôd_promeniti_veličinu); return false;
        }
        if (TAKE_Word("while")) {
            int koristiti = kôd_promeniti_veličinu; zahtev_VALUE('('); verifikovati_tip(izraz_VALUE(), 2); zahtev_VALUE(')'); int 끝 = grana(153);
            깊이++; kontrola_instrukcija(); 깊이--; Veza_VALUE(grana(167), koristiti); Veza_VALUE(끝, kôd_promeniti_veličinu); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; zahtev_VALUE('('); if (종류() != ';') dodela_VALUE(true); zahtev_VALUE(';');
            int stanje = kôd_promeniti_veličinu; if (종류() == ';') 내보내기(4); else verifikovati_tip(izraz_VALUE(), 2); zahtev_VALUE(';');
            int 끝 = grana(153), telo_teksta = grana(167), osvežiti = kôd_promeniti_veličinu;
            if (종류() != ')') dodela_VALUE(false); zahtev_VALUE(')'); Veza_VALUE(grana(167), stanje); Veza_VALUE(telo_teksta, kôd_promeniti_veličinu);
            kontrola_instrukcija(); Veza_VALUE(grana(167), osvežiti); Veza_VALUE(끝, kôd_promeniti_veličinu);
            for (int 수 = 0; 수 < lokalni_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(pozicija, "System")) { 화면출력(); return false; }
        if (종류() == 256 && pozicija + 1 < token_COUNT && (토큰종류[pozicija + 1] == '(' || 토큰종류[pozicija + 1] == '.')) {
            int tip_VALUE = izraz_VALUE(); if (tip_VALUE != 0) 내보내기(87); zahtev_VALUE(';'); return false;
        }
        dodela_VALUE(true); zahtev_VALUE(';'); return false;
    }
    static boolean kontrola_instrukcija() {
        if (Word_VALUE(pozicija, "int") || Word_VALUE(pozicija, "boolean") || Word_VALUE(pozicija, "char") || Word_VALUE(pozicija, "String")
            || Word_VALUE(pozicija, "FileInputStream") || Word_VALUE(pozicija, "FileOutputStream")) otkazivanje_VALUE("local declaration requires braces");
        return instrukcija_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) otkazivanje_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void 클래스쓰기() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstanta_COUNT);
        for (int 수 = 0; 수 < konstanta_promeniti_veličinu; 수++) 출바(konstanta_VALUE[수]);
        출짧(0x21); 출짧(Razred_konstanta); 출짧(nadređen_konstanta); 출짧(0); 출짧(0); 출짧(metod_COUNT);
        for (int 수 = 0; 수 < metod_COUNT; 수++) {
            출짧(metod_pristup[수]); 출짧(metod_ime_konstanta[수]); 출짧(함수서술[수]); 출짧(1); 출짧(kôd_konstanta);
            출정(12 + 함수길이[수]); 출짧(128); 출짧(함수지역[수]); 출정(함수길이[수]);
            for (int 칸 = 0; 칸 < 함수길이[수]; 칸++) 출바(kôd_VALUE[metod_kôd[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int koristiti() {
        if (korisnik.인수개수() == 1 && 자바도구.같음(korisnik.인수(0), "-version")) {
            korisnik.쓰기("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (korisnik.인수개수() != 1) { korisnik.쓰기("Usage: javac FILE.java\n"); return 2; }
        int ime_promeniti_veličinu = 자바도구.ime(ime_datoteke_SMS, korisnik.인수(0));
        if (ime_promeniti_veličinu < 6 || ime_promeniti_veličinu > 62 || ime_datoteke_SMS[ime_promeniti_veličinu - 5] != '.' || ime_datoteke_SMS[ime_promeniti_veličinu - 4] != 'j'
            || ime_datoteke_SMS[ime_promeniti_veličinu - 3] != 'a' || ime_datoteke_SMS[ime_promeniti_veličinu - 2] != 'v' || ime_datoteke_SMS[ime_promeniti_veličinu - 1] != 'a') {
            korisnik.쓰기("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        izvor_promeniti_veličinu = korisnik.파일읽기(ime_datoteke_SMS, izvor);
        if (izvor_promeniti_veličinu < 0) { korisnik.쓰기("javac: cannot read source: "); 자바도구.수쓰기(izvor_promeniti_veličinu); korisnik.문자쓰기(10); return 1; }
        izvor_promeniti_veličinu = 자바도구.원문해독(izvor, izvor_promeniti_veličinu);
        if (izvor_promeniti_veličinu < 0) { korisnik.쓰기("javac error: invalid UTF-8 source\n"); return 1; }
        iseći_VALUE(); if (!greška) 선언읽기();
        if (!greška) {
            if (토큰길이[Razred_token] != ime_promeniti_veličinu - 5) otkazivanje_VALUE("class name must match file name");
            for (int 수 = 0; 수 < ime_promeniti_veličinu - 5; 수++) if (izvor[token_pozicija[Razred_token] + 수] != ime_datoteke_SMS[수]) otkazivanje_VALUE("class name must match file name");
        }
        for (aktuelno_metod = 0; aktuelno_metod < metod_COUNT && !greška; aktuelno_metod++) {
            pozicija = metod_telo[aktuelno_metod]; metod_kôd[aktuelno_metod] = kôd_promeniti_veličinu; lokalni_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metod_argument_COUNT[aktuelno_metod]; 수++) Dodaj_lokalni(metod_argument_ime[aktuelno_metod * 16 + 수], metod_argument_tip[aktuelno_metod * 16 + 수]);
            boolean vratiti_KR = instrukcija_VALUE();
            if (!vratiti_KR && metod_vratiti[aktuelno_metod] != 0) otkazivanje_VALUE("missing return");
            // grana 뒤의 합류 지점은 반드시 stvarni_podaci 명령이어야 한다 (버전 49 검증기).
            if (metod_vratiti[aktuelno_metod] == 0) 내보내기(177);
            else { boolean ceo_broj = metod_vratiti[aktuelno_metod] <= 2 || metod_vratiti[aktuelno_metod] == 5; 내보내기(ceo_broj ? 3 : 1); 내보내기(ceo_broj ? 172 : 176); }
            if (pozicija != metod_završiti_razgovor[aktuelno_metod]) otkazivanje_VALUE("invalid method body");
            함수지역[aktuelno_metod] = lokalni_COUNT; 함수길이[aktuelno_metod] = kôd_promeniti_veličinu - metod_kôd[aktuelno_metod];
        }
        if (greška) return 1;
        클래스쓰기(); if (greška) return 1;
        ime_datoteke_SMS[ime_promeniti_veličinu - 4] = 'c'; ime_datoteke_SMS[ime_promeniti_veličinu - 3] = 'l'; ime_datoteke_SMS[ime_promeniti_veličinu - 2] = 'a';
        ime_datoteke_SMS[ime_promeniti_veličinu - 1] = 's'; ime_datoteke_SMS[ime_promeniti_veličinu] = 's'; ime_datoteke_SMS[ime_promeniti_veličinu + 1] = 0;
        int KR = korisnik.파일쓰기(ime_datoteke_SMS, 출력, 출력크기);
        if (KR < 0) { korisnik.쓰기("javac: cannot save class: "); 자바도구.수쓰기(KR); korisnik.문자쓰기(10); return 1; }
        korisnik.쓰기("Compiled: "); for (int 수 = 0; ime_datoteke_SMS[수] != 0; 수++) korisnik.문자쓰기(ime_datoteke_SMS[수]);
        korisnik.쓰기(" (JVM class version 49)\n"); return 0;
    }
}
