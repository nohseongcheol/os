// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java zdroj_strom -> 표준 버전 49 class kompilátor. */
public final class 자바컴파일러 {
    static int[] zdrojový_soubor = new int[16384], výstupní_pozice = new int[16384], KÓD_HODNOTA = new int[4096];
    static int[] token_Druh = new int[2048], token_pozice = new int[2048], token_délka = new int[2048];
    static int[] konstanta_HODNOTA = new int[4096], konstanta_POSUN = new int[512];
    static int[] 문자 = new int[512], název_souboru_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int zdroj_změnit_velikost, token_POČET, pozice, KÓD_změnit_velikost, konstanta_změnit_velikost, konstanta_POČET = 1, výstup_změnit_velikost, znak_délka;
    static boolean chyba;
    static int Třída_token, Třída_konstanta, nadřazený_konstanta, KÓD_konstanta;
    static int[] metoda_položka_název = new int[32], metoda_Vratka = new int[32], metoda_argument_POČET = new int[32];
    static int[] metoda_argument_název = new int[512], metoda_argument_TYP = new int[512];
    static int[] tělo_metody = new int[32], metoda_konec = new int[32], metoda_KÓD = new int[32];
    static int[] metoda_délka = new int[32], 함수지역 = new int[32], metoda_název_konstanta = new int[32], metoda_popisovač_konstanta = new int[32];
    static int[] metoda_přístup = new int[32];
    static int metoda_POČET, dobrá_metoda, místní_POČET, 깊이, 식깊이;
    static int[] místní_název = new int[128], místní_TYP = new int[128], 지역깊이 = new int[128];

    static void selhání_HODNOTA(String 이유) {
        if (!chyba) {
            uživatelský_prostor.Zápis("javac error: "); uživatelský_prostor.Zápis(이유);
            uživatelský_prostor.Zápis(" at line ");
            int vstupní_řádek = 1, 끝 = pozice < token_POČET ? token_pozice[pozice] : zdroj_změnit_velikost;
            for (int číslo = 0; číslo < 끝; číslo++) if (zdrojový_soubor[číslo] == 10) vstupní_řádek++;
            자바도구.zápis_číslo(vstupní_řádek); uživatelský_prostor.zápis_znak_HODNOTA(10);
        }
        chyba = true;
    }
    static boolean znak_HODNOTA(int HODNOTA) { return 문자이름규칙.첫글자(HODNOTA); }
    static boolean číslice_HODNOTA(int HODNOTA) { return HODNOTA >= '0' && HODNOTA <= '9'; }
    static boolean 이름같음(int 가, int SEKUNDA_operand) {
        if (가 < 0 || SEKUNDA_operand < 0 || 가 >= token_POČET || SEKUNDA_operand >= token_POČET || token_délka[가] != token_délka[SEKUNDA_operand]) return false;
        for (int číslo = 0; číslo < token_délka[가]; číslo++) if (zdrojový_soubor[token_pozice[가] + číslo] != zdrojový_soubor[token_pozice[SEKUNDA_operand] + číslo]) return false;
        return true;
    }
    static boolean Word_HODNOTA(int token_HODNOTA, String Word_SMS) {
        if (token_HODNOTA < 0 || token_HODNOTA >= token_POČET || token_délka[token_HODNOTA] != Word_SMS.length()) return false;
        for (int číslo = 0; číslo < Word_SMS.length(); číslo++) if (zdrojový_soubor[token_pozice[token_HODNOTA] + číslo] != Word_SMS.charAt(číslo)) return false;
        return true;
    }
    static int Druh_HODNOTA() { return pozice < token_POČET ? token_Druh[pozice] : 0; }
    static boolean dostat(int HODNOTA) { if (Druh_HODNOTA() != HODNOTA) return false; pozice++; return true; }
    static void požadavek_HODNOTA(int HODNOTA) { if (!dostat(HODNOTA)) selhání_HODNOTA("unexpected token"); }
    static boolean VZÍT_Word(String Word_SMS) { if (!Word_HODNOTA(pozice, Word_SMS)) return false; pozice++; return true; }
    static void 말요구(String Word_SMS) { if (!VZÍT_Word(Word_SMS)) selhání_HODNOTA(Word_SMS); }
    static int identifikátor_HODNOTA() {
        int VÝSLEDEK = pozice;
        if (Druh_HODNOTA() != 256) selhání_HODNOTA("identifier required"); else pozice++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Spustit_2 = 0;
        for (int číslo = 0; číslo <= 예약어.length(); číslo++) {
            if (číslo == 예약어.length() || 예약어.charAt(číslo) == ' ') {
                boolean 같음 = číslo - Spustit_2 == token_délka[VÝSLEDEK];
                for (int přihrádka_položka = Spustit_2; 같음 && přihrádka_položka < číslo; přihrádka_položka++) if (예약어.charAt(přihrádka_položka) != zdrojový_soubor[token_pozice[VÝSLEDEK] + přihrádka_položka - Spustit_2]) 같음 = false;
                if (같음) selhání_HODNOTA("reserved word cannot be an identifier");
                Spustit_2 = číslo + 1;
            }
        }
        return VÝSLEDEK;
    }
    static void stříhat_HODNOTA() {
        int číslo = 0;
        while (číslo < zdroj_změnit_velikost && !chyba) {
            int HODNOTA = zdrojový_soubor[číslo], Spustit_2 = číslo, Druh_HODNOTA = HODNOTA;
            if (HODNOTA == 32 || HODNOTA == 9 || HODNOTA == 10 || HODNOTA == 13) { číslo++; continue; }
            if (HODNOTA == '/' && číslo + 1 < zdroj_změnit_velikost && zdrojový_soubor[číslo + 1] == '/') {
                while (číslo < zdroj_změnit_velikost && zdrojový_soubor[číslo] != 10) číslo++;
                continue;
            }
            if (HODNOTA == '/' && číslo + 1 < zdroj_změnit_velikost && zdrojový_soubor[číslo + 1] == '*') {
                číslo += 2;
                while (číslo + 1 < zdroj_změnit_velikost && !(zdrojový_soubor[číslo] == '*' && zdrojový_soubor[číslo + 1] == '/')) číslo++;
                if (číslo + 1 >= zdroj_změnit_velikost) { selhání_HODNOTA("unterminated comment"); break; }
                číslo += 2; continue;
            }
            if (znak_HODNOTA(HODNOTA)) { Druh_HODNOTA = 256; while (číslo < zdroj_změnit_velikost && 문자이름규칙.이어진글자(zdrojový_soubor[číslo])) číslo++; }
            else if (číslice_HODNOTA(HODNOTA)) { Druh_HODNOTA = 257; while (číslo < zdroj_změnit_velikost && číslice_HODNOTA(zdrojový_soubor[číslo])) číslo++; }
            else if (HODNOTA == '"' || HODNOTA == '\'') {
                Druh_HODNOTA = HODNOTA == '"' ? 258 : 259; číslo++;
                while (číslo < zdroj_změnit_velikost && zdrojový_soubor[číslo] != HODNOTA && zdrojový_soubor[číslo] != 10 && zdrojový_soubor[číslo] != 13) {
                    if (zdrojový_soubor[číslo] == '\\') číslo++;
                    číslo++;
                }
                if (číslo >= zdroj_změnit_velikost || zdrojový_soubor[číslo] != HODNOTA) { selhání_HODNOTA("unterminated literal"); break; }
                číslo++;
            } else {
                číslo++;
                if (číslo < zdroj_změnit_velikost) {
                    int Další_zboží = zdrojový_soubor[číslo];
                    if (HODNOTA == '=' && Další_zboží == '=') Druh_HODNOTA = 300;
                    if (HODNOTA == '!' && Další_zboží == '=') Druh_HODNOTA = 301;
                    if (HODNOTA == '<' && Další_zboží == '=') Druh_HODNOTA = 302;
                    if (HODNOTA == '>' && Další_zboží == '=') Druh_HODNOTA = 303;
                    if (HODNOTA == '&' && Další_zboží == '&') Druh_HODNOTA = 304;
                    if (HODNOTA == '|' && Další_zboží == '|') Druh_HODNOTA = 305;
                    if (HODNOTA == '+' && Další_zboží == '+') Druh_HODNOTA = 306;
                    if (HODNOTA == '-' && Další_zboží == '-') Druh_HODNOTA = 307;
                    if (HODNOTA == '+' && Další_zboží == '=') Druh_HODNOTA = 308;
                    if (HODNOTA == '-' && Další_zboží == '=') Druh_HODNOTA = 309;
                    if (HODNOTA == '*' && Další_zboží == '=') Druh_HODNOTA = 310;
                    if (HODNOTA == '/' && Další_zboží == '=') Druh_HODNOTA = 311;
                    if (HODNOTA == '%' && Další_zboží == '=') Druh_HODNOTA = 312;
                    if (Druh_HODNOTA >= 300) číslo++;
                }
            }
            if (token_POČET == token_Druh.length - 1) { selhání_HODNOTA("too many tokens (2047 maximum)"); break; }
            token_Druh[token_POČET] = Druh_HODNOTA; token_pozice[token_POČET] = Spustit_2; token_délka[token_POČET++] = číslo - Spustit_2;
        }
    }
    static void zápis_konstanta_bajt(int HODNOTA) {
        if (konstanta_změnit_velikost == konstanta_HODNOTA.length) { selhání_HODNOTA("constant pool too large"); return; }
        konstanta_HODNOTA[konstanta_změnit_velikost++] = HODNOTA & 255;
    }
    static void 상짧(int HODNOTA) { zápis_konstanta_bajt(HODNOTA >> 8); zápis_konstanta_bajt(HODNOTA); }
    static int registr_konstanta(int Spustit_2) {
        for (int číslo = 1; číslo < konstanta_POČET; číslo++) {
            int přední_fotoaparát_HODNOTA = konstanta_POSUN[číslo], délka_HODNOTA = (číslo + 1 < konstanta_POČET ? konstanta_POSUN[číslo + 1] : Spustit_2) - přední_fotoaparát_HODNOTA;
            if (délka_HODNOTA != konstanta_změnit_velikost - Spustit_2) continue;
            boolean 같음 = true;
            for (int přihrádka_položka = 0; přihrádka_položka < délka_HODNOTA; přihrádka_položka++) if (konstanta_HODNOTA[přední_fotoaparát_HODNOTA + přihrádka_položka] != konstanta_HODNOTA[Spustit_2 + přihrádka_položka]) 같음 = false;
            if (같음) { konstanta_změnit_velikost = Spustit_2; return číslo; }
        }
        if (konstanta_POČET == konstanta_POSUN.length) { selhání_HODNOTA("too many constants"); return 0; }
        konstanta_POSUN[konstanta_POČET] = Spustit_2;
        return konstanta_POČET++;
    }
    static void Připojit_SMS(int HODNOTA) {
        if (znak_délka == 문자.length) { selhání_HODNOTA("text too long"); return; }
        문자[znak_délka++] = HODNOTA;
    }
    static void Připojit_Word(String Word_SMS) { for (int číslo = 0; číslo < Word_SMS.length(); číslo++) Připojit_SMS(Word_SMS.charAt(číslo)); }
    static int znak_konstanta() {
        int Spustit_2 = konstanta_změnit_velikost; zápis_konstanta_bajt(1); 상짧(0);
        for (int číslo = 0; číslo < znak_délka; číslo++) {
            int HODNOTA = 문자[číslo];
            if (HODNOTA > 0 && HODNOTA < 128) zápis_konstanta_bajt(HODNOTA);
            else if (HODNOTA < 2048) { zápis_konstanta_bajt(192 | HODNOTA >> 6); zápis_konstanta_bajt(128 | HODNOTA & 63); }
            else { zápis_konstanta_bajt(224 | HODNOTA >> 12); zápis_konstanta_bajt(128 | HODNOTA >> 6 & 63); zápis_konstanta_bajt(128 | HODNOTA & 63); }
        }
        if (chyba) return 0;
        int délka_HODNOTA = konstanta_změnit_velikost - Spustit_2 - 3;
        konstanta_HODNOTA[Spustit_2 + 1] = délka_HODNOTA >> 8; konstanta_HODNOTA[Spustit_2 + 2] = délka_HODNOTA & 255;
        return registr_konstanta(Spustit_2);
    }
    static int Word_konstanta(String Word_SMS) { znak_délka = 0; Připojit_Word(Word_SMS); return znak_konstanta(); }
    static int token_konstanta(int token_HODNOTA) {
        znak_délka = 0;
        for (int číslo = 0; číslo < token_délka[token_HODNOTA]; číslo++) Připojit_SMS(zdrojový_soubor[token_pozice[token_HODNOTA] + číslo]);
        return znak_konstanta();
    }
    static int odkaz(int Druh_HODNOTA, int 가, int SEKUNDA_operand) {
        int Spustit_2 = konstanta_změnit_velikost; zápis_konstanta_bajt(Druh_HODNOTA); 상짧(가);
        if (Druh_HODNOTA == 9 || Druh_HODNOTA == 10 || Druh_HODNOTA == 12) 상짧(SEKUNDA_operand);
        return registr_konstanta(Spustit_2);
    }
    static int externí_odkaz(int Druh_HODNOTA, String vlastník_HODNOTA, String Název, String 서술) {
        int vlastník_identifikátor = odkaz(7, Word_konstanta(vlastník_HODNOTA), 0);
        int název_POČET = Word_konstanta(Název), formát_POČET = Word_konstanta(서술);
        return odkaz(Druh_HODNOTA, vlastník_identifikátor, odkaz(12, název_POČET, formát_POČET));
    }
    static void 내보내기(int HODNOTA) {
        if (KÓD_změnit_velikost == KÓD_HODNOTA.length) { selhání_HODNOTA("bytecode too large"); return; }
        KÓD_HODNOTA[KÓD_změnit_velikost++] = HODNOTA & 255;
    }
    static void příkaz(int HODNOTA, int argumenty) { 내보내기(HODNOTA); 내보내기(argumenty >> 8); 내보내기(argumenty); }
    static void 수상수(int HODNOTA) {
        if (HODNOTA >= -1 && HODNOTA <= 5) { 내보내기(HODNOTA + 3); return; }
        int Spustit_2 = konstanta_změnit_velikost; zápis_konstanta_bajt(3); 상짧(HODNOTA >>> 16); 상짧(HODNOTA);
        příkaz(19, registr_konstanta(Spustit_2));
    }
    static int větev(int příkaz) { int VÝSLEDEK = KÓD_změnit_velikost; příkaz(příkaz, 0); return VÝSLEDEK; }
    static void Odkaz_HODNOTA(int větev, int cíl_objekt) {
        if (chyba) return;
        int 거리 = cíl_objekt - větev;
        if (거리 < -32768 || 거리 > 32767 || větev < 0 || větev + 2 >= KÓD_změnit_velikost) { selhání_HODNOTA("invalid branch"); return; }
        KÓD_HODNOTA[větev + 1] = 거리 >> 8 & 255; KÓD_HODNOTA[větev + 2] = 거리 & 255;
    }
    static void Porovnání_HODNOTA(int příkaz) {
        int PRAVDA_HODNOTA = větev(příkaz); 내보내기(3); int 끝 = větev(167);
        Odkaz_HODNOTA(PRAVDA_HODNOTA, KÓD_změnit_velikost); 내보내기(4); Odkaz_HODNOTA(끝, KÓD_změnit_velikost);
    }
    static int formát_HODNOTA() {
        if (VZÍT_Word("void")) return 0;
        if (VZÍT_Word("int")) return 1;
        if (VZÍT_Word("boolean")) return 2;
        if (VZÍT_Word("char")) return 5;
        if (VZÍT_Word("FileInputStream")) return 6;
        if (VZÍT_Word("FileOutputStream")) return 7;
        if (VZÍT_Word("String")) { if (dostat('[')) { požadavek_HODNOTA(']'); return 4; } return 3; }
        selhání_HODNOTA("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Přidat_formát(int TYP_HODNOTA) {
        if (TYP_HODNOTA == 0) Připojit_SMS('V');
        if (TYP_HODNOTA == 1) Připojit_SMS('I');
        if (TYP_HODNOTA == 2) Připojit_SMS('Z');
        if (TYP_HODNOTA == 3) Připojit_Word("Ljava/lang/String;");
        if (TYP_HODNOTA == 4) Připojit_Word("[Ljava/lang/String;");
        if (TYP_HODNOTA == 5) Připojit_SMS('C');
        if (TYP_HODNOTA == 6) Připojit_Word("Ljava/io/FileInputStream;");
        if (TYP_HODNOTA == 7) Připojit_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklarace_4f4f026b. výjimka Proces_HODNOTA_položka 본문은 hostit javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = VZÍT_Word("čeština");
        if (한국어묶음) { požadavek_HODNOTA('.'); 말요구("vlastní"); požadavek_HODNOTA('.'); }
        if (!한국어묶음 && (VZÍT_Word("Exception") || VZÍT_Word("IOException"))) return;
        if (VZÍT_Word("výjimka") || VZÍT_Word("spuštění_výjimka") || VZÍT_Word("vstup_a_výstup_výjimka") || VZÍT_Word("počkej_TIMEOUT_výjimka") || VZÍT_Word("ODKAZ_VYHLEDAT_výjimka") || VZÍT_Word("파일없음예외") || VZÍT_Word("komunikace_výjimka") || VZÍT_Word("neplatný_argument_výjimka") || VZÍT_Word("číslo_formát_selhání") || VZÍT_Word("범위예외") || VZÍT_Word("배열범위예외") || VZÍT_Word("문자열범위예외") || VZÍT_Word("nulový_odkaz_výjimka") || VZÍT_Word("산술예외") || VZÍT_Word("Stav_výjimka") || VZÍT_Word("TYP_převod_výjimka") || VZÍT_Word("음수배열크기예외") || VZÍT_Word("pole_Store_selhání") || VZÍT_Word("vlákno_Stav_výjimka") || VZÍT_Word("대기중단예외")) return;
        selhání_HODNOTA("unsupported throws type");
    }
    static void 선언읽기() {
        while (VZÍT_Word("import")) {
            if (Word_HODNOTA(pozice, "čeština")) 예외이름읽기();
            else {
                말요구("java"); požadavek_HODNOTA('.'); 말요구("io"); požadavek_HODNOTA('.');
                if (!(VZÍT_Word("FileInputStream") || VZÍT_Word("FileOutputStream") || VZÍT_Word("IOException"))) selhání_HODNOTA("unsupported import");
            }
            požadavek_HODNOTA(';');
        }
        VZÍT_Word("public"); VZÍT_Word("final"); 말요구("class"); Třída_token = identifikátor_HODNOTA();
        Třída_konstanta = odkaz(7, token_konstanta(Třída_token), 0);
        nadřazený_konstanta = odkaz(7, Word_konstanta("java/lang/Object"), 0); KÓD_konstanta = Word_konstanta("Code"); požadavek_HODNOTA('{');
        while (!chyba && Druh_HODNOTA() != '}') {
            if (metoda_POČET == 32) { selhání_HODNOTA("too many methods"); break; }
            int přístup_položka = VZÍT_Word("public") ? 1 : VZÍT_Word("private") ? 2 : 0; 말요구("static");
            int funkce_HODNOTA = metoda_POČET++;
            metoda_přístup[funkce_HODNOTA] = přístup_položka | 8;
            metoda_Vratka[funkce_HODNOTA] = formát_HODNOTA(); metoda_položka_název[funkce_HODNOTA] = identifikátor_HODNOTA(); požadavek_HODNOTA('(');
            for (int přední_fotoaparát_HODNOTA = 0; přední_fotoaparát_HODNOTA < funkce_HODNOTA; přední_fotoaparát_HODNOTA++) if (이름같음(metoda_položka_název[přední_fotoaparát_HODNOTA], metoda_položka_název[funkce_HODNOTA])) selhání_HODNOTA("duplicate method (overloading unsupported)");
            while (!chyba && Druh_HODNOTA() != ')') {
                int číslo = metoda_argument_POČET[funkce_HODNOTA];
                if (číslo == 16) { selhání_HODNOTA("too many parameters"); break; }
                int TYP_HODNOTA = formát_HODNOTA(); if (TYP_HODNOTA == 0) selhání_HODNOTA("void parameter");
                metoda_argument_TYP[funkce_HODNOTA * 16 + číslo] = TYP_HODNOTA; metoda_argument_název[funkce_HODNOTA * 16 + číslo] = identifikátor_HODNOTA();
                metoda_argument_POČET[funkce_HODNOTA]++;
                if (!dostat(',')) break;
            }
            požadavek_HODNOTA(')');
            if (VZÍT_Word("throws")) {
                do { 예외이름읽기(); } while (!chyba && dostat(','));
            }
            tělo_metody[funkce_HODNOTA] = pozice; požadavek_HODNOTA('{');
            int vnoření_HODNOTA = 1;
            while (pozice < token_POČET && vnoření_HODNOTA > 0) {
                if (Druh_HODNOTA() == '{') vnoření_HODNOTA++;
                if (Druh_HODNOTA() == '}') vnoření_HODNOTA--;
                pozice++;
            }
            if (vnoření_HODNOTA != 0) selhání_HODNOTA("unclosed method body");
            metoda_konec[funkce_HODNOTA] = pozice;
            metoda_název_konstanta[funkce_HODNOTA] = token_konstanta(metoda_položka_název[funkce_HODNOTA]);
            znak_délka = 0; Připojit_SMS('(');
            for (int číslo = 0; číslo < metoda_argument_POČET[funkce_HODNOTA]; číslo++) Přidat_formát(metoda_argument_TYP[funkce_HODNOTA * 16 + číslo]);
            Připojit_SMS(')'); Přidat_formát(metoda_Vratka[funkce_HODNOTA]); metoda_popisovač_konstanta[funkce_HODNOTA] = znak_konstanta();
        }
        požadavek_HODNOTA('}'); if (pozice != token_POČET) selhání_HODNOTA("extra input after class");
    }
    static int NAJÍT_místní(int Název) {
        for (int číslo = místní_POČET - 1; číslo >= 0; číslo--) if (지역깊이[číslo] >= 0 && 이름같음(místní_název[číslo], Název)) return číslo;
        selhání_HODNOTA("unknown variable"); return 0;
    }
    static int Přidat_místní(int Název, int TYP_HODNOTA) {
        for (int číslo = 0; číslo < místní_POČET; číslo++) if (지역깊이[číslo] >= 0 && 이름같음(místní_název[číslo], Název)) selhání_HODNOTA("duplicate local variable");
        if (místní_POČET == 128) { selhání_HODNOTA("too many locals"); return 0; }
        místní_název[místní_POČET] = Název; místní_TYP[místní_POČET] = TYP_HODNOTA; 지역깊이[místní_POČET] = 깊이;
        return místní_POČET++;
    }
    static boolean integer_TYP(int TYP_HODNOTA) { return TYP_HODNOTA == 1 || TYP_HODNOTA == 5; }
    static void 지역읽기(int číslo) { 내보내기(místní_TYP[číslo] <= 2 || místní_TYP[číslo] == 5 ? 21 : 25); 내보내기(číslo); }
    static void zápis_místní(int číslo) { 내보내기(místní_TYP[číslo] <= 2 || místní_TYP[číslo] == 5 ? 54 : 58); 내보내기(číslo); }
    static void ověřit_TYP(int skutečný_data, int 기대) { if (skutečný_data != 기대 && !(skutečný_data == 5 && 기대 == 1)) selhání_HODNOTA("type mismatch"); }
    static void 문자읽기(int token_HODNOTA) {
        znak_délka = 0; int Spustit_2 = token_pozice[token_HODNOTA] + 1, 끝 = token_pozice[token_HODNOTA] + token_délka[token_HODNOTA] - 1;
        while (Spustit_2 < 끝 && !chyba) {
            int HODNOTA = zdrojový_soubor[Spustit_2++];
            if (HODNOTA == '\\') {
                if (Spustit_2 == 끝) { selhání_HODNOTA("invalid escape"); break; }
                HODNOTA = zdrojový_soubor[Spustit_2++];
                if (HODNOTA == 'n') HODNOTA = 10;
                else if (HODNOTA == 'r') HODNOTA = 13;
                else if (HODNOTA == 't') HODNOTA = 9;
                else if (HODNOTA == 'b') HODNOTA = 8;
                else if (HODNOTA == 'f') HODNOTA = 12;
                else if (HODNOTA != '\\' && HODNOTA != '"' && HODNOTA != '\'') selhání_HODNOTA("unsupported escape");
            }
            Připojit_SMS(HODNOTA);
        }
    }
    static int parsovat_integer(int token_HODNOTA, boolean 음수) {
        if (token_délka[token_HODNOTA] > 1 && zdrojový_soubor[token_pozice[token_HODNOTA]] == '0') selhání_HODNOTA("octal literals unsupported");
        int HODNOTA = 0;
        for (int číslo = 0; číslo < token_délka[token_HODNOTA]; číslo++) {
            int číslice_zboží = zdrojový_soubor[token_pozice[token_HODNOTA] + číslo] - '0';
            if (HODNOTA < -214748364 || HODNOTA == -214748364 && číslice_zboží > (음수 ? 8 : 7)) selhání_HODNOTA("integer literal out of range");
            HODNOTA = HODNOTA * 10 - číslice_zboží;
        }
        return 음수 ? HODNOTA : -HODNOTA;
    }
    static int 기본식() {
        if (VZÍT_Word("new")) {
            int TYP_HODNOTA = formát_HODNOTA();
            if (TYP_HODNOTA != 6 && TYP_HODNOTA != 7) { selhání_HODNOTA("only file streams supported by new in source"); return 0; }
            String vlastník_HODNOTA = TYP_HODNOTA == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            příkaz(187, odkaz(7, Word_konstanta(vlastník_HODNOTA), 0)); 내보내기(89);
            požadavek_HODNOTA('('); ověřit_TYP(výraz_HODNOTA(), 3); boolean 이어 = false;
            if (dostat(',')) { if (TYP_HODNOTA != 7) selhání_HODNOTA("input stream constructor arguments"); ověřit_TYP(výraz_HODNOTA(), 2); 이어 = true; }
            požadavek_HODNOTA(')');
            příkaz(183, externí_odkaz(10, vlastník_HODNOTA, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYP_HODNOTA;
        }
        if (dostat('(')) { int TYP_HODNOTA = výraz_HODNOTA(); požadavek_HODNOTA(')'); return TYP_HODNOTA; }
        if (Druh_HODNOTA() == 257) { 수상수(parsovat_integer(pozice++, false)); return 1; }
        if (Druh_HODNOTA() == 258) { 문자읽기(pozice++); příkaz(19, odkaz(8, znak_konstanta(), 0)); return 3; }
        if (Druh_HODNOTA() == 259) { 문자읽기(pozice++); if (znak_délka != 1) selhání_HODNOTA("character literal length"); 수상수(문자[0]); return 5; }
        if (VZÍT_Word("true")) { 내보내기(4); return 2; }
        if (VZÍT_Word("false")) { 내보내기(3); return 2; }
        if (VZÍT_Word("čeština")) {
            požadavek_HODNOTA('.'); 말요구("vlastní"); požadavek_HODNOTA('.');
            String vlastník_HODNOTA = "", metoda_HODNOTA = "", 서술 = ""; int 가 = 0, SEKUNDA_operand = 0, 다 = 0, 라 = 0, 마 = 0, VÝSLEDEK = 0;
            if (VZÍT_Word("výstupní_pozice")) {
                vlastník_HODNOTA = "čeština/vlastní/výstupní_pozice"; požadavek_HODNOTA('.');
                if (VZÍT_Word("zápis_čára")) { metoda_HODNOTA = "zápis_čára"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (VZÍT_Word("Zápis")) { metoda_HODNOTA = "Zápis"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (VZÍT_Word("zápis_číslo")) { metoda_HODNOTA = "zápis_číslo"; 서술 = "(I)V"; 가 = 1; }
                else selhání_HODNOTA("unknown Korean output method");
            } else if (VZÍT_Word("문자")) {
                vlastník_HODNOTA = "čeština/vlastní/문자"; požadavek_HODNOTA('.'); 가 = 3;
                if (VZÍT_Word("délka_HODNOTA")) { metoda_HODNOTA = "délka_HODNOTA"; 서술 = "(Ljava/lang/String;)I"; VÝSLEDEK = 1; }
                else if (VZÍT_Word("bod_kódu_POČET")) { metoda_HODNOTA = "bod_kódu_POČET"; 서술 = "(Ljava/lang/String;)I"; VÝSLEDEK = 1; }
                else if (VZÍT_Word("parsovat_integer")) { metoda_HODNOTA = "parsovat_integer"; 서술 = "(Ljava/lang/String;)I"; VÝSLEDEK = 1; }
                else if (VZÍT_Word("zápis_integer_HODNOTA")) { metoda_HODNOTA = "zápis_integer_HODNOTA"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; VÝSLEDEK = 3; }
                else if (VZÍT_Word("같음")) { metoda_HODNOTA = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SEKUNDA_operand = 3; VÝSLEDEK = 2; }
                else if (VZÍT_Word("vložit_SMS")) { metoda_HODNOTA = "vložit_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SEKUNDA_operand = 3; VÝSLEDEK = 3; }
                else if (VZÍT_Word("stříhat_HODNOTA")) { metoda_HODNOTA = "stříhat_HODNOTA"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SEKUNDA_operand = 1; 다 = 1; VÝSLEDEK = 3; }
                else selhání_HODNOTA("unknown Korean text method");
            } else if (VZÍT_Word("název_souboru")) {
                vlastník_HODNOTA = "čeština/vlastní/název_souboru"; požadavek_HODNOTA('.'); 가 = 3;
                if (VZÍT_Word("Čtení")) { metoda_HODNOTA = "Čtení"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; VÝSLEDEK = 3; }
                else if (VZÍT_Word("Zápis")) { metoda_HODNOTA = "Zápis"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SEKUNDA_operand = 3; }
                else selhání_HODNOTA("unknown Korean file method");
            } else if (VZÍT_Word("화면")) {
                vlastník_HODNOTA = "čeština/vlastní/화면"; požadavek_HODNOTA('.');
                if (VZÍT_Word("너비")) { metoda_HODNOTA = "너비"; 서술 = "()I"; VÝSLEDEK = 1; }
                else if (VZÍT_Word("výška_HODNOTA")) { metoda_HODNOTA = "výška_HODNOTA"; 서술 = "()I"; VÝSLEDEK = 1; }
                else if (VZÍT_Word("obdélník")) { metoda_HODNOTA = "obdélník"; 서술 = "(IIIII)V"; 가 = 1; SEKUNDA_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (VZÍT_Word("vymazat_položka")) { metoda_HODNOTA = "vymazat_položka"; 서술 = "(I)V"; 가 = 1; }
                else if (VZÍT_Word("기다리기")) { metoda_HODNOTA = "기다리기"; 서술 = "()V"; }
                else selhání_HODNOTA("unknown Korean framebuffer method");
            } else selhání_HODNOTA("unsupported Korean library class");
            požadavek_HODNOTA('('); if (가 != 0) ověřit_TYP(výraz_HODNOTA(), 가);
            if (SEKUNDA_operand != 0) { požadavek_HODNOTA(','); ověřit_TYP(výraz_HODNOTA(), SEKUNDA_operand); }
            if (다 != 0) { požadavek_HODNOTA(','); ověřit_TYP(výraz_HODNOTA(), 다); }
            if (라 != 0) { požadavek_HODNOTA(','); ověřit_TYP(výraz_HODNOTA(), 라); }
            if (마 != 0) { požadavek_HODNOTA(','); ověřit_TYP(výraz_HODNOTA(), 마); }
            požadavek_HODNOTA(')'); příkaz(184, externí_odkaz(10, vlastník_HODNOTA, metoda_HODNOTA, 서술)); return VÝSLEDEK;
        }
        if (VZÍT_Word("Integer")) {
            požadavek_HODNOTA('.'); 말요구("parseInt"); požadavek_HODNOTA('('); ověřit_TYP(výraz_HODNOTA(), 3); požadavek_HODNOTA(')');
            příkaz(184, externí_odkaz(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Název = identifikátor_HODNOTA();
        if (dostat('(')) {
            int funkce_HODNOTA = -1;
            for (int číslo = 0; číslo < metoda_POČET; číslo++) if (이름같음(Název, metoda_položka_název[číslo])) funkce_HODNOTA = číslo;
            if (funkce_HODNOTA < 0) { selhání_HODNOTA("unknown static method"); return 0; }
            int číslo = 0;
            while (!chyba && Druh_HODNOTA() != ')') {
                if (číslo >= metoda_argument_POČET[funkce_HODNOTA]) { selhání_HODNOTA("too many arguments"); break; }
                ověřit_TYP(výraz_HODNOTA(), metoda_argument_TYP[funkce_HODNOTA * 16 + číslo++]); if (!dostat(',')) break;
            }
            požadavek_HODNOTA(')'); if (číslo != metoda_argument_POČET[funkce_HODNOTA]) selhání_HODNOTA("argument count mismatch");
            příkaz(184, odkaz(10, Třída_konstanta, odkaz(12, metoda_název_konstanta[funkce_HODNOTA], metoda_popisovač_konstanta[funkce_HODNOTA])));
            return metoda_Vratka[funkce_HODNOTA];
        }
        int místní_obor = NAJÍT_místní(Název), TYP_HODNOTA = místní_TYP[místní_obor]; 지역읽기(místní_obor);
        while (!chyba) {
            if (dostat('[')) { ověřit_TYP(TYP_HODNOTA, 4); ověřit_TYP(výraz_HODNOTA(), 1); požadavek_HODNOTA(']'); 내보내기(50); TYP_HODNOTA = 3; }
            else if (dostat('.')) {
                if (TYP_HODNOTA == 6 || TYP_HODNOTA == 7) {
                    String vlastník_HODNOTA = TYP_HODNOTA == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (VZÍT_Word("close")) { požadavek_HODNOTA('('); požadavek_HODNOTA(')'); příkaz(182, externí_odkaz(10, vlastník_HODNOTA, "close", "()V")); TYP_HODNOTA = 0; }
                    else if (TYP_HODNOTA == 6 && VZÍT_Word("read")) { požadavek_HODNOTA('('); požadavek_HODNOTA(')'); příkaz(182, externí_odkaz(10, vlastník_HODNOTA, "read", "()I")); TYP_HODNOTA = 1; }
                    else if (TYP_HODNOTA == 7 && VZÍT_Word("write")) { požadavek_HODNOTA('('); ověřit_TYP(výraz_HODNOTA(), 1); požadavek_HODNOTA(')'); příkaz(182, externí_odkaz(10, vlastník_HODNOTA, "write", "(I)V")); TYP_HODNOTA = 0; }
                    else { selhání_HODNOTA("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYP_HODNOTA == 4) { 내보내기(190); TYP_HODNOTA = 1; }
                else { ověřit_TYP(TYP_HODNOTA, 3); požadavek_HODNOTA('('); požadavek_HODNOTA(')'); příkaz(182, externí_odkaz(10, "java/lang/String", "length", "()I")); TYP_HODNOTA = 1; }
            } else break;
        }
        return TYP_HODNOTA;
    }
    static int 단항() {
        if (++식깊이 > 64) { selhání_HODNOTA("expression nesting too deep"); 식깊이--; return 0; }
        int TYP_HODNOTA;
        if (dostat('!')) { ověřit_TYP(단항(), 2); Porovnání_HODNOTA(153); TYP_HODNOTA = 2; }
        else if (dostat('-')) {
            if (Druh_HODNOTA() == 257) 수상수(parsovat_integer(pozice++, true));
            else { ověřit_TYP(단항(), 1); 내보내기(116); }
            TYP_HODNOTA = 1;
        } else if (dostat('+')) { ověřit_TYP(단항(), 1); TYP_HODNOTA = 1; }
        else TYP_HODNOTA = 기본식();
        식깊이--; return TYP_HODNOTA;
    }
    static int 곱식() {
        int TYP_HODNOTA = 단항();
        while (!chyba && (Druh_HODNOTA() == '*' || Druh_HODNOTA() == '/' || Druh_HODNOTA() == '%')) {
            int Encoding_HODNOTA = Druh_HODNOTA(); pozice++; ověřit_TYP(TYP_HODNOTA, 1); ověřit_TYP(단항(), 1);
            내보내기(Encoding_HODNOTA == '*' ? 104 : Encoding_HODNOTA == '/' ? 108 : 112); TYP_HODNOTA = 1;
        }
        return TYP_HODNOTA;
    }
    static int 합식() {
        int TYP_HODNOTA = 곱식();
        while (!chyba && (Druh_HODNOTA() == '+' || Druh_HODNOTA() == '-')) {
            int Encoding_HODNOTA = Druh_HODNOTA(); pozice++; int mez_HODNOTA = KÓD_změnit_velikost, BACK_hodnota = 곱식();
            if (Encoding_HODNOTA == '+' && (TYP_HODNOTA == 3 || BACK_hodnota == 3)) { 결합(mez_HODNOTA, TYP_HODNOTA, BACK_hodnota); TYP_HODNOTA = 3; }
            else { ověřit_TYP(TYP_HODNOTA, 1); ověřit_TYP(BACK_hodnota, 1); 내보내기(Encoding_HODNOTA == '+' ? 96 : 100); TYP_HODNOTA = 1; }
        }
        return TYP_HODNOTA;
    }
    static int připojený_odkaz(int TYP_HODNOTA) {
        if (TYP_HODNOTA != 1 && TYP_HODNOTA != 2 && TYP_HODNOTA != 3 && TYP_HODNOTA != 5) selhání_HODNOTA("unsupported concatenation type");
        return externí_odkaz(10, "java/lang/StringBuilder", "append", TYP_HODNOTA == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYP_HODNOTA == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYP_HODNOTA == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int mez_HODNOTA, int přední_fotoaparát_hodnota, int BACK_hodnota) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 právo KÓD_HODNOTA 앞에 generovat 코드를 삽입한다.
        // právo výraz_HODNOTA 내부의 partner_HODNOTA větev 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = KÓD_změnit_velikost;
        příkaz(187, odkaz(7, Word_konstanta("java/lang/StringBuilder"), 0)); 내보내기(89);
        příkaz(183, externí_odkaz(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); příkaz(182, připojený_odkaz(přední_fotoaparát_hodnota));
        if (chyba) return;
        int délka_HODNOTA = KÓD_změnit_velikost - 끝;
        for (int číslo = 0; číslo < délka_HODNOTA; číslo++) 삽입코드[číslo] = KÓD_HODNOTA[끝 + číslo];
        for (int číslo = 끝 - 1; číslo >= mez_HODNOTA; číslo--) KÓD_HODNOTA[číslo + délka_HODNOTA] = KÓD_HODNOTA[číslo];
        for (int číslo = 0; číslo < délka_HODNOTA; číslo++) KÓD_HODNOTA[mez_HODNOTA + číslo] = 삽입코드[číslo];
        příkaz(182, připojený_odkaz(BACK_hodnota)); příkaz(182, externí_odkaz(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Porovnání_výraz() {
        int TYP_HODNOTA = 합식();
        while (!chyba && (Druh_HODNOTA() == '<' || Druh_HODNOTA() == '>' || Druh_HODNOTA() == 302 || Druh_HODNOTA() == 303)) {
            int Encoding_HODNOTA = Druh_HODNOTA(); pozice++; ověřit_TYP(TYP_HODNOTA, 1); ověřit_TYP(합식(), 1);
            Porovnání_HODNOTA(Encoding_HODNOTA == '<' ? 161 : Encoding_HODNOTA == '>' ? 163 : Encoding_HODNOTA == 302 ? 164 : 162); TYP_HODNOTA = 2;
        }
        return TYP_HODNOTA;
    }
    static int 동등식() {
        int TYP_HODNOTA = Porovnání_výraz();
        while (!chyba && (Druh_HODNOTA() == 300 || Druh_HODNOTA() == 301)) {
            int Encoding_HODNOTA = Druh_HODNOTA(); pozice++; int BACK_hodnota = Porovnání_výraz();
            if (TYP_HODNOTA == 0 || BACK_hodnota == 0) selhání_HODNOTA("void expression");
            if (!(integer_TYP(TYP_HODNOTA) && integer_TYP(BACK_hodnota))) ověřit_TYP(BACK_hodnota, TYP_HODNOTA);
            Porovnání_HODNOTA((TYP_HODNOTA <= 2 || TYP_HODNOTA == 5 ? 159 : 165) + (Encoding_HODNOTA == 301 ? 1 : 0)); TYP_HODNOTA = 2;
        }
        return TYP_HODNOTA;
    }
    static int A() {
        int TYP_HODNOTA = 동등식();
        while (!chyba && dostat(304)) {
            ověřit_TYP(TYP_HODNOTA, 2); int 가 = větev(153); ověřit_TYP(동등식(), 2); int SEKUNDA_operand = větev(153);
            내보내기(4); int 끝 = větev(167); Odkaz_HODNOTA(가, KÓD_změnit_velikost); Odkaz_HODNOTA(SEKUNDA_operand, KÓD_změnit_velikost); 내보내기(3); Odkaz_HODNOTA(끝, KÓD_změnit_velikost); TYP_HODNOTA = 2;
        }
        return TYP_HODNOTA;
    }
    static int výraz_HODNOTA() {
        int TYP_HODNOTA = A();
        while (!chyba && dostat(305)) {
            ověřit_TYP(TYP_HODNOTA, 2); int 가 = větev(154); ověřit_TYP(A(), 2); int SEKUNDA_operand = větev(154);
            내보내기(3); int 끝 = větev(167); Odkaz_HODNOTA(가, KÓD_změnit_velikost); Odkaz_HODNOTA(SEKUNDA_operand, KÓD_změnit_velikost); 내보내기(4); Odkaz_HODNOTA(끝, KÓD_změnit_velikost); TYP_HODNOTA = 2;
        }
        return TYP_HODNOTA;
    }
    static void zadání_HODNOTA(boolean Povolit_deklarace) {
        if (Word_HODNOTA(pozice, "int") || Word_HODNOTA(pozice, "boolean") || Word_HODNOTA(pozice, "String") || Word_HODNOTA(pozice, "char")
            || Word_HODNOTA(pozice, "FileInputStream") || Word_HODNOTA(pozice, "FileOutputStream")) {
            if (!Povolit_deklarace) selhání_HODNOTA("declaration not allowed here");
            int TYP_HODNOTA = formát_HODNOTA(), Název = identifikátor_HODNOTA(); požadavek_HODNOTA('='); ověřit_TYP(výraz_HODNOTA(), TYP_HODNOTA);
            zápis_místní(Přidat_místní(Název, TYP_HODNOTA)); return;
        }
        int Název = identifikátor_HODNOTA(), místní_obor = NAJÍT_místní(Název);
        if (dostat('=')) { ověřit_TYP(výraz_HODNOTA(), místní_TYP[místní_obor]); zápis_místní(místní_obor); }
        else if (Druh_HODNOTA() >= 308 && Druh_HODNOTA() <= 312) {
            int Encoding_HODNOTA = Druh_HODNOTA(); pozice++; 지역읽기(místní_obor); int mez_HODNOTA = KÓD_změnit_velikost, BACK_hodnota = výraz_HODNOTA();
            if (Encoding_HODNOTA == 308 && místní_TYP[místní_obor] == 3) 결합(mez_HODNOTA, 3, BACK_hodnota);
            else {
                ověřit_TYP(místní_TYP[místní_obor], 1); ověřit_TYP(BACK_hodnota, 1);
                내보내기(Encoding_HODNOTA == 308 ? 96 : Encoding_HODNOTA == 309 ? 100 : Encoding_HODNOTA == 310 ? 104 : Encoding_HODNOTA == 311 ? 108 : 112);
                if (místní_TYP[místní_obor] == 5) 내보내기(146);
            }
            zápis_místní(místní_obor);
        }
        else if (Druh_HODNOTA() == 306 || Druh_HODNOTA() == 307) {
            ověřit_TYP(místní_TYP[místní_obor], 1); 내보내기(132); 내보내기(místní_obor); 내보내기(Druh_HODNOTA() == 306 ? 1 : 255); pozice++;
            if (místní_TYP[místní_obor] == 5) { 지역읽기(místní_obor); 내보내기(146); zápis_místní(místní_obor); }
        } else selhání_HODNOTA("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); požadavek_HODNOTA('.'); 말요구("out"); požadavek_HODNOTA('.');
        boolean 줄바꿈 = VZÍT_Word("println"); if (!줄바꿈) 말요구("print"); požadavek_HODNOTA('(');
        příkaz(178, externí_odkaz(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = Druh_HODNOTA() == ')';
        int TYP_HODNOTA = 빈인수 ? 0 : výraz_HODNOTA(); požadavek_HODNOTA(')'); požadavek_HODNOTA(';');
        String 서술 = TYP_HODNOTA == 0 ? "()V" : TYP_HODNOTA == 1 ? "(I)V" : TYP_HODNOTA == 2 ? "(Z)V" : TYP_HODNOTA == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYP_HODNOTA == 4 || TYP_HODNOTA >= 6 || TYP_HODNOTA == 0 && (!줄바꿈 || !빈인수)) selhání_HODNOTA("unsupported print argument");
        příkaz(182, externí_odkaz(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean výpis_HODNOTA() {
        if (chyba) return false;
        if (깊이 > 32) { selhání_HODNOTA("statement nesting too deep"); return false; }
        if (dostat('{')) {
            깊이++; boolean Vratka_KV = false;
            while (!chyba && Druh_HODNOTA() != '}') { if (Vratka_KV) selhání_HODNOTA("unreachable statement"); Vratka_KV = výpis_HODNOTA(); }
            požadavek_HODNOTA('}'); for (int číslo = 0; číslo < místní_POČET; číslo++) if (지역깊이[číslo] == 깊이) 지역깊이[číslo] = -1;
            깊이--; return Vratka_KV;
        }
        if (dostat(';')) return false;
        if (VZÍT_Word("return")) {
            int TYP_HODNOTA = Druh_HODNOTA() == ';' ? 0 : výraz_HODNOTA(); ověřit_TYP(TYP_HODNOTA, metoda_Vratka[dobrá_metoda]); požadavek_HODNOTA(';');
            내보내기(TYP_HODNOTA == 0 ? 177 : TYP_HODNOTA <= 2 || TYP_HODNOTA == 5 ? 172 : 176); return true;
        }
        if (VZÍT_Word("if")) {
            požadavek_HODNOTA('('); ověřit_TYP(výraz_HODNOTA(), 2); požadavek_HODNOTA(')'); int NEPRAVDA_HODNOTA = větev(153);
            깊이++; boolean 가 = řízení_výpis(); 깊이--;
            if (VZÍT_Word("else")) { int 끝 = větev(167); Odkaz_HODNOTA(NEPRAVDA_HODNOTA, KÓD_změnit_velikost); 깊이++; boolean SEKUNDA_operand = řízení_výpis(); 깊이--; Odkaz_HODNOTA(끝, KÓD_změnit_velikost); return 가 && SEKUNDA_operand; }
            Odkaz_HODNOTA(NEPRAVDA_HODNOTA, KÓD_změnit_velikost); return false;
        }
        if (VZÍT_Word("while")) {
            int Spustit_2 = KÓD_změnit_velikost; požadavek_HODNOTA('('); ověřit_TYP(výraz_HODNOTA(), 2); požadavek_HODNOTA(')'); int 끝 = větev(153);
            깊이++; řízení_výpis(); 깊이--; Odkaz_HODNOTA(větev(167), Spustit_2); Odkaz_HODNOTA(끝, KÓD_změnit_velikost); return false;
        }
        if (VZÍT_Word("for")) {
            깊이++; požadavek_HODNOTA('('); if (Druh_HODNOTA() != ';') zadání_HODNOTA(true); požadavek_HODNOTA(';');
            int podmínka = KÓD_změnit_velikost; if (Druh_HODNOTA() == ';') 내보내기(4); else ověřit_TYP(výraz_HODNOTA(), 2); požadavek_HODNOTA(';');
            int 끝 = větev(153), základní_text = větev(167), aktualizovat = KÓD_změnit_velikost;
            if (Druh_HODNOTA() != ')') zadání_HODNOTA(false); požadavek_HODNOTA(')'); Odkaz_HODNOTA(větev(167), podmínka); Odkaz_HODNOTA(základní_text, KÓD_změnit_velikost);
            řízení_výpis(); Odkaz_HODNOTA(větev(167), aktualizovat); Odkaz_HODNOTA(끝, KÓD_změnit_velikost);
            for (int číslo = 0; číslo < místní_POČET; číslo++) if (지역깊이[číslo] == 깊이) 지역깊이[číslo] = -1;
            깊이--; return false;
        }
        if (Word_HODNOTA(pozice, "System")) { 화면출력(); return false; }
        if (Druh_HODNOTA() == 256 && pozice + 1 < token_POČET && (token_Druh[pozice + 1] == '(' || token_Druh[pozice + 1] == '.')) {
            int TYP_HODNOTA = výraz_HODNOTA(); if (TYP_HODNOTA != 0) 내보내기(87); požadavek_HODNOTA(';'); return false;
        }
        zadání_HODNOTA(true); požadavek_HODNOTA(';'); return false;
    }
    static boolean řízení_výpis() {
        if (Word_HODNOTA(pozice, "int") || Word_HODNOTA(pozice, "boolean") || Word_HODNOTA(pozice, "char") || Word_HODNOTA(pozice, "String")
            || Word_HODNOTA(pozice, "FileInputStream") || Word_HODNOTA(pozice, "FileOutputStream")) selhání_HODNOTA("local declaration requires braces");
        return výpis_HODNOTA();
    }
    static void 출바(int HODNOTA) { if (výstup_změnit_velikost == výstupní_pozice.length) selhání_HODNOTA("class file too large"); else výstupní_pozice[výstup_změnit_velikost++] = HODNOTA & 255; }
    static void 출짧(int HODNOTA) { 출바(HODNOTA >> 8); 출바(HODNOTA); }
    static void 출정(int HODNOTA) { 출짧(HODNOTA >>> 16); 출짧(HODNOTA); }
    static void zápis_Třída() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstanta_POČET);
        for (int číslo = 0; číslo < konstanta_změnit_velikost; číslo++) 출바(konstanta_HODNOTA[číslo]);
        출짧(0x21); 출짧(Třída_konstanta); 출짧(nadřazený_konstanta); 출짧(0); 출짧(0); 출짧(metoda_POČET);
        for (int číslo = 0; číslo < metoda_POČET; číslo++) {
            출짧(metoda_přístup[číslo]); 출짧(metoda_název_konstanta[číslo]); 출짧(metoda_popisovač_konstanta[číslo]); 출짧(1); 출짧(KÓD_konstanta);
            출정(12 + metoda_délka[číslo]); 출짧(128); 출짧(함수지역[číslo]); 출정(metoda_délka[číslo]);
            for (int přihrádka_položka = 0; přihrádka_položka < metoda_délka[číslo]; přihrádka_položka++) 출바(KÓD_HODNOTA[metoda_KÓD[číslo] + přihrádka_položka]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Spustit_2() {
        if (uživatelský_prostor.인수개수() == 1 && 자바도구.같음(uživatelský_prostor.argumenty(0), "-version")) {
            uživatelský_prostor.Zápis("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (uživatelský_prostor.인수개수() != 1) { uživatelský_prostor.Zápis("Usage: javac FILE.java\n"); return 2; }
        int název_změnit_velikost = 자바도구.Název(název_souboru_SMS, uživatelský_prostor.argumenty(0));
        if (název_změnit_velikost < 6 || název_změnit_velikost > 62 || název_souboru_SMS[název_změnit_velikost - 5] != '.' || název_souboru_SMS[název_změnit_velikost - 4] != 'j'
            || název_souboru_SMS[název_změnit_velikost - 3] != 'a' || název_souboru_SMS[název_změnit_velikost - 2] != 'v' || název_souboru_SMS[název_změnit_velikost - 1] != 'a') {
            uživatelský_prostor.Zápis("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        zdroj_změnit_velikost = uživatelský_prostor.파일읽기(název_souboru_SMS, zdrojový_soubor);
        if (zdroj_změnit_velikost < 0) { uživatelský_prostor.Zápis("javac: cannot read source: "); 자바도구.zápis_číslo(zdroj_změnit_velikost); uživatelský_prostor.zápis_znak_HODNOTA(10); return 1; }
        zdroj_změnit_velikost = 자바도구.원문해독(zdrojový_soubor, zdroj_změnit_velikost);
        if (zdroj_změnit_velikost < 0) { uživatelský_prostor.Zápis("javac error: invalid UTF-8 source\n"); return 1; }
        stříhat_HODNOTA(); if (!chyba) 선언읽기();
        if (!chyba) {
            if (token_délka[Třída_token] != název_změnit_velikost - 5) selhání_HODNOTA("class name must match file name");
            for (int číslo = 0; číslo < název_změnit_velikost - 5; číslo++) if (zdrojový_soubor[token_pozice[Třída_token] + číslo] != název_souboru_SMS[číslo]) selhání_HODNOTA("class name must match file name");
        }
        for (dobrá_metoda = 0; dobrá_metoda < metoda_POČET && !chyba; dobrá_metoda++) {
            pozice = tělo_metody[dobrá_metoda]; metoda_KÓD[dobrá_metoda] = KÓD_změnit_velikost; místní_POČET = 0; 깊이 = 0;
            for (int číslo = 0; číslo < metoda_argument_POČET[dobrá_metoda]; číslo++) Přidat_místní(metoda_argument_název[dobrá_metoda * 16 + číslo], metoda_argument_TYP[dobrá_metoda * 16 + číslo]);
            boolean Vratka_KV = výpis_HODNOTA();
            if (!Vratka_KV && metoda_Vratka[dobrá_metoda] != 0) selhání_HODNOTA("missing return");
            // větev 뒤의 합류 지점은 반드시 skutečný_data 명령이어야 한다 (버전 49 검증기).
            if (metoda_Vratka[dobrá_metoda] == 0) 내보내기(177);
            else { boolean integer = metoda_Vratka[dobrá_metoda] <= 2 || metoda_Vratka[dobrá_metoda] == 5; 내보내기(integer ? 3 : 1); 내보내기(integer ? 172 : 176); }
            if (pozice != metoda_konec[dobrá_metoda]) selhání_HODNOTA("invalid method body");
            함수지역[dobrá_metoda] = místní_POČET; metoda_délka[dobrá_metoda] = KÓD_změnit_velikost - metoda_KÓD[dobrá_metoda];
        }
        if (chyba) return 1;
        zápis_Třída(); if (chyba) return 1;
        název_souboru_SMS[název_změnit_velikost - 4] = 'c'; název_souboru_SMS[název_změnit_velikost - 3] = 'l'; název_souboru_SMS[název_změnit_velikost - 2] = 'a';
        název_souboru_SMS[název_změnit_velikost - 1] = 's'; název_souboru_SMS[název_změnit_velikost] = 's'; název_souboru_SMS[název_změnit_velikost + 1] = 0;
        int VÝSLEDEK = uživatelský_prostor.zápis_Soubor(název_souboru_SMS, výstupní_pozice, výstup_změnit_velikost);
        if (VÝSLEDEK < 0) { uživatelský_prostor.Zápis("javac: cannot save class: "); 자바도구.zápis_číslo(VÝSLEDEK); uživatelský_prostor.zápis_znak_HODNOTA(10); return 1; }
        uživatelský_prostor.Zápis("Compiled: "); for (int číslo = 0; název_souboru_SMS[číslo] != 0; číslo++) uživatelský_prostor.zápis_znak_HODNOTA(název_souboru_SMS[číslo]);
        uživatelský_prostor.Zápis(" (JVM class version 49)\n"); return 0;
    }
}
