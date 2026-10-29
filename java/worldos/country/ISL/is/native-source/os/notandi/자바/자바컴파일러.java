// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java uppruni_tré -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] Uppruni = new int[16384], úttak = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], tákn_staða = new int[2048], tákn_lengd = new int[2048];
    static int[] fasti_VALUE = new int[4096], fasti_OFFSET = new int[512];
    static int[] 문자 = new int[512], skrá_heiti_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int uppruni_breyta_stærð, tákn_COUNT, Staðsetning, CODE_breyta_stærð, fasti_breyta_stærð, fasti_COUNT = 1, úttak_breyta_stærð, stafur_lengd;
    static boolean Villa;
    static int klasi_tákn, klasi_fasti, yfireining_fasti, CODE_fasti;
    static int[] aðferð_færsla_heiti = new int[32], aðferð_skila = new int[32], aðferð_frumbreyta_COUNT = new int[32];
    static int[] aðferð_frumbreyta_heiti = new int[512], aðferð_frumbreyta_TYPE = new int[512];
    static int[] aðferð_meginmál = new int[32], aðferð_ljúka = new int[32], aðferð_CODE = new int[32];
    static int[] aðferð_lengd = new int[32], 함수지역 = new int[32], aðferð_heiti_fasti = new int[32], 함수서술 = new int[32];
    static int[] aðferð_aðgangur = new int[32];
    static int aðferð_COUNT, 현재함수, staðbundið_COUNT, 깊이, 식깊이;
    static int[] staðbundið_heiti = new int[128], staðbundið_TYPE = new int[128], 지역깊이 = new int[128];

    static void bilun_VALUE(String 이유) {
        if (!Villa) {
            notandi.Skrift("javac error: "); notandi.Skrift(이유);
            notandi.Skrift(" at line ");
            int Lína = 1, 끝 = Staðsetning < tákn_COUNT ? tákn_staða[Staðsetning] : uppruni_breyta_stærð;
            for (int númer = 0; númer < 끝; númer++) if (Uppruni[númer] == 10) Lína++;
            자바도구.skrifa_númer(Lína); notandi.skrifa_stafur_VALUE(10);
        }
        Villa = true;
    }
    static boolean stafur_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean tölustafur_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= tákn_COUNT || 나 >= tákn_COUNT || tákn_lengd[가] != tákn_lengd[나]) return false;
        for (int númer = 0; númer < tákn_lengd[가]; númer++) if (Uppruni[tákn_staða[가] + númer] != Uppruni[tákn_staða[나] + númer]) return false;
        return true;
    }
    static boolean Word_VALUE(int tákn_VALUE_eb540501, String Word_SMS) {
        if (tákn_VALUE_eb540501 < 0 || tákn_VALUE_eb540501 >= tákn_COUNT || tákn_lengd[tákn_VALUE_eb540501] != Word_SMS.length()) return false;
        for (int númer = 0; númer < Word_SMS.length(); númer++) if (Uppruni[tákn_staða[tákn_VALUE_eb540501] + númer] != Word_SMS.charAt(númer)) return false;
        return true;
    }
    static int 종류() { return Staðsetning < tákn_COUNT ? 토큰종류[Staðsetning] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; Staðsetning++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) bilun_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Staðsetning, Word_SMS)) return false; Staðsetning++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) bilun_VALUE(Word_SMS); }
    static int auðkenni_VALUE() {
        int NIÐURSTAÐA = Staðsetning;
        if (종류() != 256) bilun_VALUE("identifier required"); else Staðsetning++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Keyra_2 = 0;
        for (int númer = 0; númer <= 예약어.length(); númer++) {
            if (númer == 예약어.length() || 예약어.charAt(númer) == ' ') {
                boolean 같음 = númer - Keyra_2 == tákn_lengd[NIÐURSTAÐA];
                for (int rauf_færsla = Keyra_2; 같음 && rauf_færsla < númer; rauf_færsla++) if (예약어.charAt(rauf_færsla) != Uppruni[tákn_staða[NIÐURSTAÐA] + rauf_færsla - Keyra_2]) 같음 = false;
                if (같음) bilun_VALUE("reserved word cannot be an identifier");
                Keyra_2 = númer + 1;
            }
        }
        return NIÐURSTAÐA;
    }
    static void klippa_VALUE() {
        int númer = 0;
        while (númer < uppruni_breyta_stærð && !Villa) {
            int VALUE = Uppruni[númer], Keyra_2 = númer, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { númer++; continue; }
            if (VALUE == '/' && númer + 1 < uppruni_breyta_stærð && Uppruni[númer + 1] == '/') {
                while (númer < uppruni_breyta_stærð && Uppruni[númer] != 10) númer++;
                continue;
            }
            if (VALUE == '/' && númer + 1 < uppruni_breyta_stærð && Uppruni[númer + 1] == '*') {
                númer += 2;
                while (númer + 1 < uppruni_breyta_stærð && !(Uppruni[númer] == '*' && Uppruni[númer + 1] == '/')) númer++;
                if (númer + 1 >= uppruni_breyta_stærð) { bilun_VALUE("unterminated comment"); break; }
                númer += 2; continue;
            }
            if (stafur_VALUE(VALUE)) { 종류 = 256; while (númer < uppruni_breyta_stærð && 문자이름규칙.이어진글자(Uppruni[númer])) númer++; }
            else if (tölustafur_VALUE(VALUE)) { 종류 = 257; while (númer < uppruni_breyta_stærð && tölustafur_VALUE(Uppruni[númer])) númer++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; númer++;
                while (númer < uppruni_breyta_stærð && Uppruni[númer] != VALUE && Uppruni[númer] != 10 && Uppruni[númer] != 13) {
                    if (Uppruni[númer] == '\\') númer++;
                    númer++;
                }
                if (númer >= uppruni_breyta_stærð || Uppruni[númer] != VALUE) { bilun_VALUE("unterminated literal"); break; }
                númer++;
            } else {
                númer++;
                if (númer < uppruni_breyta_stærð) {
                    int Áfram_vara = Uppruni[númer];
                    if (VALUE == '=' && Áfram_vara == '=') 종류 = 300;
                    if (VALUE == '!' && Áfram_vara == '=') 종류 = 301;
                    if (VALUE == '<' && Áfram_vara == '=') 종류 = 302;
                    if (VALUE == '>' && Áfram_vara == '=') 종류 = 303;
                    if (VALUE == '&' && Áfram_vara == '&') 종류 = 304;
                    if (VALUE == '|' && Áfram_vara == '|') 종류 = 305;
                    if (VALUE == '+' && Áfram_vara == '+') 종류 = 306;
                    if (VALUE == '-' && Áfram_vara == '-') 종류 = 307;
                    if (VALUE == '+' && Áfram_vara == '=') 종류 = 308;
                    if (VALUE == '-' && Áfram_vara == '=') 종류 = 309;
                    if (VALUE == '*' && Áfram_vara == '=') 종류 = 310;
                    if (VALUE == '/' && Áfram_vara == '=') 종류 = 311;
                    if (VALUE == '%' && Áfram_vara == '=') 종류 = 312;
                    if (종류 >= 300) númer++;
                }
            }
            if (tákn_COUNT == 토큰종류.length - 1) { bilun_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[tákn_COUNT] = 종류; tákn_staða[tákn_COUNT] = Keyra_2; tákn_lengd[tákn_COUNT++] = númer - Keyra_2;
        }
    }
    static void skrifa_fasti_bæti(int VALUE) {
        if (fasti_breyta_stærð == fasti_VALUE.length) { bilun_VALUE("constant pool too large"); return; }
        fasti_VALUE[fasti_breyta_stærð++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { skrifa_fasti_bæti(VALUE >> 8); skrifa_fasti_bæti(VALUE); }
    static int skrá_fasti(int Keyra_2) {
        for (int númer = 1; númer < fasti_COUNT; númer++) {
            int myndavél_að_framan_VALUE = fasti_OFFSET[númer], lengd_VALUE = (númer + 1 < fasti_COUNT ? fasti_OFFSET[númer + 1] : Keyra_2) - myndavél_að_framan_VALUE;
            if (lengd_VALUE != fasti_breyta_stærð - Keyra_2) continue;
            boolean 같음 = true;
            for (int rauf_færsla = 0; rauf_færsla < lengd_VALUE; rauf_færsla++) if (fasti_VALUE[myndavél_að_framan_VALUE + rauf_færsla] != fasti_VALUE[Keyra_2 + rauf_færsla]) 같음 = false;
            if (같음) { fasti_breyta_stærð = Keyra_2; return númer; }
        }
        if (fasti_COUNT == fasti_OFFSET.length) { bilun_VALUE("too many constants"); return 0; }
        fasti_OFFSET[fasti_COUNT] = Keyra_2;
        return fasti_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (stafur_lengd == 문자.length) { bilun_VALUE("text too long"); return; }
        문자[stafur_lengd++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int númer = 0; númer < Word_SMS.length(); númer++) 글추가(Word_SMS.charAt(númer)); }
    static int stafur_fasti() {
        int Keyra_2 = fasti_breyta_stærð; skrifa_fasti_bæti(1); 상짧(0);
        for (int númer = 0; númer < stafur_lengd; númer++) {
            int VALUE = 문자[númer];
            if (VALUE > 0 && VALUE < 128) skrifa_fasti_bæti(VALUE);
            else if (VALUE < 2048) { skrifa_fasti_bæti(192 | VALUE >> 6); skrifa_fasti_bæti(128 | VALUE & 63); }
            else { skrifa_fasti_bæti(224 | VALUE >> 12); skrifa_fasti_bæti(128 | VALUE >> 6 & 63); skrifa_fasti_bæti(128 | VALUE & 63); }
        }
        if (Villa) return 0;
        int lengd_VALUE = fasti_breyta_stærð - Keyra_2 - 3;
        fasti_VALUE[Keyra_2 + 1] = lengd_VALUE >> 8; fasti_VALUE[Keyra_2 + 2] = lengd_VALUE & 255;
        return skrá_fasti(Keyra_2);
    }
    static int Word_fasti(String Word_SMS) { stafur_lengd = 0; 말추가(Word_SMS); return stafur_fasti(); }
    static int tákn_fasti(int tákn_VALUE_eb540501) {
        stafur_lengd = 0;
        for (int númer = 0; númer < tákn_lengd[tákn_VALUE_eb540501]; númer++) 글추가(Uppruni[tákn_staða[tákn_VALUE_eb540501] + númer]);
        return stafur_fasti();
    }
    static int tilvísun(int 종류, int 가, int 나) {
        int Keyra_2 = fasti_breyta_stærð; skrifa_fasti_bæti(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return skrá_fasti(Keyra_2);
    }
    static int 외부참조(int 종류, String eigandi_VALUE, String Heiti, String 서술) {
        int eigandi_auðkenni = tilvísun(7, Word_fasti(eigandi_VALUE), 0);
        int heiti_COUNT = Word_fasti(Heiti), snið_COUNT = Word_fasti(서술);
        return tilvísun(종류, eigandi_auðkenni, tilvísun(12, heiti_COUNT, snið_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_breyta_stærð == CODE_VALUE.length) { bilun_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_breyta_stærð++] = VALUE & 255;
    }
    static void Skipun(int VALUE, int Viðföng) { 내보내기(VALUE); 내보내기(Viðföng >> 8); 내보내기(Viðföng); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Keyra_2 = fasti_breyta_stærð; skrifa_fasti_bæti(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Skipun(19, skrá_fasti(Keyra_2));
    }
    static int grein(int Skipun) { int NIÐURSTAÐA = CODE_breyta_stærð; Skipun(Skipun, 0); return NIÐURSTAÐA; }
    static void tengja_VALUE(int grein, int markmið_hlutur) {
        if (Villa) return;
        int 거리 = markmið_hlutur - grein;
        if (거리 < -32768 || 거리 > 32767 || grein < 0 || grein + 2 >= CODE_breyta_stærð) { bilun_VALUE("invalid branch"); return; }
        CODE_VALUE[grein + 1] = 거리 >> 8 & 255; CODE_VALUE[grein + 2] = 거리 & 255;
    }
    static void Samanburður_VALUE(int Skipun) {
        int TRUE_VALUE = grein(Skipun); 내보내기(3); int 끝 = grein(167);
        tengja_VALUE(TRUE_VALUE, CODE_breyta_stærð); 내보내기(4); tengja_VALUE(끝, CODE_breyta_stærð);
    }
    static int snið_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        bilun_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void bæta_við_snið(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws skýrsla. undantekning Ferli_VALUE_færsla 본문은 hýsa javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Íslenska");
        if (한국어묶음) { 요구('.'); 말요구("eigin"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("undantekning") || TAKE_Word("실행예외") || TAKE_Word("I_Ú_undantekning") || TAKE_Word("Bíddu_TIMEOUT_undantekning") || TAKE_Word("slóð_LOOKUP_undantekning") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("ógilt_frumbreyta_undantekning") || TAKE_Word("númer_snið_bilun") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_tilvísun_undantekning") || TAKE_Word("산술예외") || TAKE_Word("staða_undantekning") || TAKE_Word("TYPE_senda_út_undantekning") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_bilun") || TAKE_Word("þráður_staða_undantekning") || TAKE_Word("대기중단예외")) return;
        bilun_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Staðsetning, "Íslenska")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) bilun_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); klasi_tákn = auðkenni_VALUE();
        klasi_fasti = tilvísun(7, tákn_fasti(klasi_tákn), 0);
        yfireining_fasti = tilvísun(7, Word_fasti("java/lang/Object"), 0); CODE_fasti = Word_fasti("Code"); 요구('{');
        while (!Villa && 종류() != '}') {
            if (aðferð_COUNT == 32) { bilun_VALUE("too many methods"); break; }
            int aðgangur_færsla = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int fall_VALUE = aðferð_COUNT++;
            aðferð_aðgangur[fall_VALUE] = aðgangur_færsla | 8;
            aðferð_skila[fall_VALUE] = snið_VALUE(); aðferð_færsla_heiti[fall_VALUE] = auðkenni_VALUE(); 요구('(');
            for (int myndavél_að_framan_VALUE = 0; myndavél_að_framan_VALUE < fall_VALUE; myndavél_að_framan_VALUE++) if (이름같음(aðferð_færsla_heiti[myndavél_að_framan_VALUE], aðferð_færsla_heiti[fall_VALUE])) bilun_VALUE("duplicate method (overloading unsupported)");
            while (!Villa && 종류() != ')') {
                int númer = aðferð_frumbreyta_COUNT[fall_VALUE];
                if (númer == 16) { bilun_VALUE("too many parameters"); break; }
                int TYPE_VALUE = snið_VALUE(); if (TYPE_VALUE == 0) bilun_VALUE("void parameter");
                aðferð_frumbreyta_TYPE[fall_VALUE * 16 + númer] = TYPE_VALUE; aðferð_frumbreyta_heiti[fall_VALUE * 16 + númer] = auðkenni_VALUE();
                aðferð_frumbreyta_COUNT[fall_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!Villa && 받기(','));
            }
            aðferð_meginmál[fall_VALUE] = Staðsetning; 요구('{');
            int földun_VALUE = 1;
            while (Staðsetning < tákn_COUNT && földun_VALUE > 0) {
                if (종류() == '{') földun_VALUE++;
                if (종류() == '}') földun_VALUE--;
                Staðsetning++;
            }
            if (földun_VALUE != 0) bilun_VALUE("unclosed method body");
            aðferð_ljúka[fall_VALUE] = Staðsetning;
            aðferð_heiti_fasti[fall_VALUE] = tákn_fasti(aðferð_færsla_heiti[fall_VALUE]);
            stafur_lengd = 0; 글추가('(');
            for (int númer = 0; númer < aðferð_frumbreyta_COUNT[fall_VALUE]; númer++) bæta_við_snið(aðferð_frumbreyta_TYPE[fall_VALUE * 16 + númer]);
            글추가(')'); bæta_við_snið(aðferð_skila[fall_VALUE]); 함수서술[fall_VALUE] = stafur_fasti();
        }
        요구('}'); if (Staðsetning != tákn_COUNT) bilun_VALUE("extra input after class");
    }
    static int FIND_staðbundið(int Heiti) {
        for (int númer = staðbundið_COUNT - 1; númer >= 0; númer--) if (지역깊이[númer] >= 0 && 이름같음(staðbundið_heiti[númer], Heiti)) return númer;
        bilun_VALUE("unknown variable"); return 0;
    }
    static int bæta_við_staðbundið(int Heiti, int TYPE_VALUE) {
        for (int númer = 0; númer < staðbundið_COUNT; númer++) if (지역깊이[númer] >= 0 && 이름같음(staðbundið_heiti[númer], Heiti)) bilun_VALUE("duplicate local variable");
        if (staðbundið_COUNT == 128) { bilun_VALUE("too many locals"); return 0; }
        staðbundið_heiti[staðbundið_COUNT] = Heiti; staðbundið_TYPE[staðbundið_COUNT] = TYPE_VALUE; 지역깊이[staðbundið_COUNT] = 깊이;
        return staðbundið_COUNT++;
    }
    static boolean heiltala_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int númer) { 내보내기(staðbundið_TYPE[númer] <= 2 || staðbundið_TYPE[númer] == 5 ? 21 : 25); 내보내기(númer); }
    static void skrifa_staðbundið(int númer) { 내보내기(staðbundið_TYPE[númer] <= 2 || staðbundið_TYPE[númer] == 5 ? 54 : 58); 내보내기(númer); }
    static void sannprófa_TYPE(int raun_gögn, int 기대) { if (raun_gögn != 기대 && !(raun_gögn == 5 && 기대 == 1)) bilun_VALUE("type mismatch"); }
    static void 문자읽기(int tákn_VALUE_eb540501) {
        stafur_lengd = 0; int Keyra_2 = tákn_staða[tákn_VALUE_eb540501] + 1, 끝 = tákn_staða[tákn_VALUE_eb540501] + tákn_lengd[tákn_VALUE_eb540501] - 1;
        while (Keyra_2 < 끝 && !Villa) {
            int VALUE = Uppruni[Keyra_2++];
            if (VALUE == '\\') {
                if (Keyra_2 == 끝) { bilun_VALUE("invalid escape"); break; }
                VALUE = Uppruni[Keyra_2++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') bilun_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int þátta_heiltala(int tákn_VALUE_eb540501, boolean 음수) {
        if (tákn_lengd[tákn_VALUE_eb540501] > 1 && Uppruni[tákn_staða[tákn_VALUE_eb540501]] == '0') bilun_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int númer = 0; númer < tákn_lengd[tákn_VALUE_eb540501]; númer++) {
            int tölustafur_vara = Uppruni[tákn_staða[tákn_VALUE_eb540501] + númer] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && tölustafur_vara > (음수 ? 8 : 7)) bilun_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - tölustafur_vara;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = snið_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { bilun_VALUE("only file streams supported by new in source"); return 0; }
            String eigandi_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Skipun(187, tilvísun(7, Word_fasti(eigandi_VALUE), 0)); 내보내기(89);
            요구('('); sannprófa_TYPE(segð_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) bilun_VALUE("input stream constructor arguments"); sannprófa_TYPE(segð_VALUE(), 2); 이어 = true; }
            요구(')');
            Skipun(183, 외부참조(10, eigandi_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = segð_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(þátta_heiltala(Staðsetning++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Staðsetning++); Skipun(19, tilvísun(8, stafur_fasti(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Staðsetning++); if (stafur_lengd != 1) bilun_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Íslenska")) {
            요구('.'); 말요구("eigin"); 요구('.');
            String eigandi_VALUE = "", aðferð_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, NIÐURSTAÐA = 0;
            if (TAKE_Word("úttak")) {
                eigandi_VALUE = "Íslenska/eigin/úttak"; 요구('.');
                if (TAKE_Word("skrifa_lína")) { aðferð_VALUE = "skrifa_lína"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Skrift")) { aðferð_VALUE = "Skrift"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("skrifa_númer")) { aðferð_VALUE = "skrifa_númer"; 서술 = "(I)V"; 가 = 1; }
                else bilun_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                eigandi_VALUE = "Íslenska/eigin/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("lengd_VALUE")) { aðferð_VALUE = "lengd_VALUE"; 서술 = "(Ljava/lang/String;)I"; NIÐURSTAÐA = 1; }
                else if (TAKE_Word("stafkóði_COUNT")) { aðferð_VALUE = "stafkóði_COUNT"; 서술 = "(Ljava/lang/String;)I"; NIÐURSTAÐA = 1; }
                else if (TAKE_Word("þátta_heiltala")) { aðferð_VALUE = "þátta_heiltala"; 서술 = "(Ljava/lang/String;)I"; NIÐURSTAÐA = 1; }
                else if (TAKE_Word("skrifa_heiltala_VALUE")) { aðferð_VALUE = "skrifa_heiltala_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; NIÐURSTAÐA = 3; }
                else if (TAKE_Word("같음")) { aðferð_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; NIÐURSTAÐA = 2; }
                else if (TAKE_Word("líma_SMS")) { aðferð_VALUE = "líma_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; NIÐURSTAÐA = 3; }
                else if (TAKE_Word("klippa_VALUE")) { aðferð_VALUE = "klippa_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; NIÐURSTAÐA = 3; }
                else bilun_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Skrá")) {
                eigandi_VALUE = "Íslenska/eigin/Skrá"; 요구('.'); 가 = 3;
                if (TAKE_Word("Lestur")) { aðferð_VALUE = "Lestur"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; NIÐURSTAÐA = 3; }
                else if (TAKE_Word("Skrift")) { aðferð_VALUE = "Skrift"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else bilun_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                eigandi_VALUE = "Íslenska/eigin/화면"; 요구('.');
                if (TAKE_Word("너비")) { aðferð_VALUE = "너비"; 서술 = "()I"; NIÐURSTAÐA = 1; }
                else if (TAKE_Word("높이")) { aðferð_VALUE = "높이"; 서술 = "()I"; NIÐURSTAÐA = 1; }
                else if (TAKE_Word("사각형")) { aðferð_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("eyða_færsla")) { aðferð_VALUE = "eyða_færsla"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { aðferð_VALUE = "기다리기"; 서술 = "()V"; }
                else bilun_VALUE("unknown Korean framebuffer method");
            } else bilun_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) sannprófa_TYPE(segð_VALUE(), 가);
            if (나 != 0) { 요구(','); sannprófa_TYPE(segð_VALUE(), 나); }
            if (다 != 0) { 요구(','); sannprófa_TYPE(segð_VALUE(), 다); }
            if (라 != 0) { 요구(','); sannprófa_TYPE(segð_VALUE(), 라); }
            if (마 != 0) { 요구(','); sannprófa_TYPE(segð_VALUE(), 마); }
            요구(')'); Skipun(184, 외부참조(10, eigandi_VALUE, aðferð_VALUE, 서술)); return NIÐURSTAÐA;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); sannprófa_TYPE(segð_VALUE(), 3); 요구(')');
            Skipun(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Heiti = auðkenni_VALUE();
        if (받기('(')) {
            int fall_VALUE = -1;
            for (int númer = 0; númer < aðferð_COUNT; númer++) if (이름같음(Heiti, aðferð_færsla_heiti[númer])) fall_VALUE = númer;
            if (fall_VALUE < 0) { bilun_VALUE("unknown static method"); return 0; }
            int númer = 0;
            while (!Villa && 종류() != ')') {
                if (númer >= aðferð_frumbreyta_COUNT[fall_VALUE]) { bilun_VALUE("too many arguments"); break; }
                sannprófa_TYPE(segð_VALUE(), aðferð_frumbreyta_TYPE[fall_VALUE * 16 + númer++]); if (!받기(',')) break;
            }
            요구(')'); if (númer != aðferð_frumbreyta_COUNT[fall_VALUE]) bilun_VALUE("argument count mismatch");
            Skipun(184, tilvísun(10, klasi_fasti, tilvísun(12, aðferð_heiti_fasti[fall_VALUE], 함수서술[fall_VALUE])));
            return aðferð_skila[fall_VALUE];
        }
        int staðbundið_umfang = FIND_staðbundið(Heiti), TYPE_VALUE = staðbundið_TYPE[staðbundið_umfang]; 지역읽기(staðbundið_umfang);
        while (!Villa) {
            if (받기('[')) { sannprófa_TYPE(TYPE_VALUE, 4); sannprófa_TYPE(segð_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String eigandi_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Skipun(182, 외부참조(10, eigandi_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Skipun(182, 외부참조(10, eigandi_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); sannprófa_TYPE(segð_VALUE(), 1); 요구(')'); Skipun(182, 외부참조(10, eigandi_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { bilun_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { sannprófa_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Skipun(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { bilun_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { sannprófa_TYPE(단항(), 2); Samanburður_VALUE(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(þátta_heiltala(Staðsetning++, true));
            else { sannprófa_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { sannprófa_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!Villa && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kóðun_VALUE = 종류(); Staðsetning++; sannprófa_TYPE(TYPE_VALUE, 1); sannprófa_TYPE(단항(), 1);
            내보내기(kóðun_VALUE == '*' ? 104 : kóðun_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!Villa && (종류() == '+' || 종류() == '-')) {
            int kóðun_VALUE = 종류(); Staðsetning++; int 경계 = CODE_breyta_stærð, TIL_BAKA_VALUE_TYPE = 곱식();
            if (kóðun_VALUE == '+' && (TYPE_VALUE == 3 || TIL_BAKA_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, TIL_BAKA_VALUE_TYPE); TYPE_VALUE = 3; }
            else { sannprófa_TYPE(TYPE_VALUE, 1); sannprófa_TYPE(TIL_BAKA_VALUE_TYPE, 1); 내보내기(kóðun_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) bilun_VALUE("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int myndavél_að_framan_VALUE_TYPE, int TIL_BAKA_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 skapa 코드를 삽입한다.
        // RIGHT segð_VALUE 내부의 jafningi_VALUE grein 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_breyta_stærð;
        Skipun(187, tilvísun(7, Word_fasti("java/lang/StringBuilder"), 0)); 내보내기(89);
        Skipun(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Skipun(182, 붙임참조(myndavél_að_framan_VALUE_TYPE));
        if (Villa) return;
        int lengd_VALUE = CODE_breyta_stærð - 끝;
        for (int númer = 0; númer < lengd_VALUE; númer++) 삽입코드[númer] = CODE_VALUE[끝 + númer];
        for (int númer = 끝 - 1; númer >= 경계; númer--) CODE_VALUE[númer + lengd_VALUE] = CODE_VALUE[númer];
        for (int númer = 0; númer < lengd_VALUE; númer++) CODE_VALUE[경계 + númer] = 삽입코드[númer];
        Skipun(182, 붙임참조(TIL_BAKA_VALUE_TYPE)); Skipun(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Samanburður_segð() {
        int TYPE_VALUE = 합식();
        while (!Villa && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kóðun_VALUE = 종류(); Staðsetning++; sannprófa_TYPE(TYPE_VALUE, 1); sannprófa_TYPE(합식(), 1);
            Samanburður_VALUE(kóðun_VALUE == '<' ? 161 : kóðun_VALUE == '>' ? 163 : kóðun_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Samanburður_segð();
        while (!Villa && (종류() == 300 || 종류() == 301)) {
            int kóðun_VALUE = 종류(); Staðsetning++; int TIL_BAKA_VALUE_TYPE = Samanburður_segð();
            if (TYPE_VALUE == 0 || TIL_BAKA_VALUE_TYPE == 0) bilun_VALUE("void expression");
            if (!(heiltala_TYPE(TYPE_VALUE) && heiltala_TYPE(TIL_BAKA_VALUE_TYPE))) sannprófa_TYPE(TIL_BAKA_VALUE_TYPE, TYPE_VALUE);
            Samanburður_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (kóðun_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!Villa && 받기(304)) {
            sannprófa_TYPE(TYPE_VALUE, 2); int 가 = grein(153); sannprófa_TYPE(동등식(), 2); int 나 = grein(153);
            내보내기(4); int 끝 = grein(167); tengja_VALUE(가, CODE_breyta_stærð); tengja_VALUE(나, CODE_breyta_stærð); 내보내기(3); tengja_VALUE(끝, CODE_breyta_stærð); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int segð_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!Villa && 받기(305)) {
            sannprófa_TYPE(TYPE_VALUE, 2); int 가 = grein(154); sannprófa_TYPE(논리곱(), 2); int 나 = grein(154);
            내보내기(3); int 끝 = grein(167); tengja_VALUE(가, CODE_breyta_stærð); tengja_VALUE(나, CODE_breyta_stærð); 내보내기(4); tengja_VALUE(끝, CODE_breyta_stærð); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void verkefni_VALUE(boolean leyfa_skýrsla) {
        if (Word_VALUE(Staðsetning, "int") || Word_VALUE(Staðsetning, "boolean") || Word_VALUE(Staðsetning, "String") || Word_VALUE(Staðsetning, "char")
            || Word_VALUE(Staðsetning, "FileInputStream") || Word_VALUE(Staðsetning, "FileOutputStream")) {
            if (!leyfa_skýrsla) bilun_VALUE("declaration not allowed here");
            int TYPE_VALUE = snið_VALUE(), Heiti = auðkenni_VALUE(); 요구('='); sannprófa_TYPE(segð_VALUE(), TYPE_VALUE);
            skrifa_staðbundið(bæta_við_staðbundið(Heiti, TYPE_VALUE)); return;
        }
        int Heiti = auðkenni_VALUE(), staðbundið_umfang = FIND_staðbundið(Heiti);
        if (받기('=')) { sannprófa_TYPE(segð_VALUE(), staðbundið_TYPE[staðbundið_umfang]); skrifa_staðbundið(staðbundið_umfang); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kóðun_VALUE = 종류(); Staðsetning++; 지역읽기(staðbundið_umfang); int 경계 = CODE_breyta_stærð, TIL_BAKA_VALUE_TYPE = segð_VALUE();
            if (kóðun_VALUE == 308 && staðbundið_TYPE[staðbundið_umfang] == 3) 결합(경계, 3, TIL_BAKA_VALUE_TYPE);
            else {
                sannprófa_TYPE(staðbundið_TYPE[staðbundið_umfang], 1); sannprófa_TYPE(TIL_BAKA_VALUE_TYPE, 1);
                내보내기(kóðun_VALUE == 308 ? 96 : kóðun_VALUE == 309 ? 100 : kóðun_VALUE == 310 ? 104 : kóðun_VALUE == 311 ? 108 : 112);
                if (staðbundið_TYPE[staðbundið_umfang] == 5) 내보내기(146);
            }
            skrifa_staðbundið(staðbundið_umfang);
        }
        else if (종류() == 306 || 종류() == 307) {
            sannprófa_TYPE(staðbundið_TYPE[staðbundið_umfang], 1); 내보내기(132); 내보내기(staðbundið_umfang); 내보내기(종류() == 306 ? 1 : 255); Staðsetning++;
            if (staðbundið_TYPE[staðbundið_umfang] == 5) { 지역읽기(staðbundið_umfang); 내보내기(146); skrifa_staðbundið(staðbundið_umfang); }
        } else bilun_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Skipun(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean autt_frumbreyta = 종류() == ')';
        int TYPE_VALUE = autt_frumbreyta ? 0 : segð_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !autt_frumbreyta)) bilun_VALUE("unsupported print argument");
        Skipun(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean setning_VALUE() {
        if (Villa) return false;
        if (깊이 > 32) { bilun_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean skila_mæld_stærð = false;
            while (!Villa && 종류() != '}') { if (skila_mæld_stærð) bilun_VALUE("unreachable statement"); skila_mæld_stærð = setning_VALUE(); }
            요구('}'); for (int númer = 0; númer < staðbundið_COUNT; númer++) if (지역깊이[númer] == 깊이) 지역깊이[númer] = -1;
            깊이--; return skila_mæld_stærð;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : segð_VALUE(); sannprófa_TYPE(TYPE_VALUE, aðferð_skila[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); sannprófa_TYPE(segð_VALUE(), 2); 요구(')'); int FALSE_VALUE = grein(153);
            깊이++; boolean 가 = stýring_setning(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = grein(167); tengja_VALUE(FALSE_VALUE, CODE_breyta_stærð); 깊이++; boolean 나 = stýring_setning(); 깊이--; tengja_VALUE(끝, CODE_breyta_stærð); return 가 && 나; }
            tengja_VALUE(FALSE_VALUE, CODE_breyta_stærð); return false;
        }
        if (TAKE_Word("while")) {
            int Keyra_2 = CODE_breyta_stærð; 요구('('); sannprófa_TYPE(segð_VALUE(), 2); 요구(')'); int 끝 = grein(153);
            깊이++; stýring_setning(); 깊이--; tengja_VALUE(grein(167), Keyra_2); tengja_VALUE(끝, CODE_breyta_stærð); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') verkefni_VALUE(true); 요구(';');
            int skilyrði = CODE_breyta_stærð; if (종류() == ';') 내보내기(4); else sannprófa_TYPE(segð_VALUE(), 2); 요구(';');
            int 끝 = grein(153), meginmál = grein(167), uppfæra = CODE_breyta_stærð;
            if (종류() != ')') verkefni_VALUE(false); 요구(')'); tengja_VALUE(grein(167), skilyrði); tengja_VALUE(meginmál, CODE_breyta_stærð);
            stýring_setning(); tengja_VALUE(grein(167), uppfæra); tengja_VALUE(끝, CODE_breyta_stærð);
            for (int númer = 0; númer < staðbundið_COUNT; númer++) if (지역깊이[númer] == 깊이) 지역깊이[númer] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Staðsetning, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Staðsetning + 1 < tákn_COUNT && (토큰종류[Staðsetning + 1] == '(' || 토큰종류[Staðsetning + 1] == '.')) {
            int TYPE_VALUE = segð_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        verkefni_VALUE(true); 요구(';'); return false;
    }
    static boolean stýring_setning() {
        if (Word_VALUE(Staðsetning, "int") || Word_VALUE(Staðsetning, "boolean") || Word_VALUE(Staðsetning, "char") || Word_VALUE(Staðsetning, "String")
            || Word_VALUE(Staðsetning, "FileInputStream") || Word_VALUE(Staðsetning, "FileOutputStream")) bilun_VALUE("local declaration requires braces");
        return setning_VALUE();
    }
    static void 출바(int VALUE) { if (úttak_breyta_stærð == úttak.length) bilun_VALUE("class file too large"); else úttak[úttak_breyta_stærð++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void skrifa_klasi() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(fasti_COUNT);
        for (int númer = 0; númer < fasti_breyta_stærð; númer++) 출바(fasti_VALUE[númer]);
        출짧(0x21); 출짧(klasi_fasti); 출짧(yfireining_fasti); 출짧(0); 출짧(0); 출짧(aðferð_COUNT);
        for (int númer = 0; númer < aðferð_COUNT; númer++) {
            출짧(aðferð_aðgangur[númer]); 출짧(aðferð_heiti_fasti[númer]); 출짧(함수서술[númer]); 출짧(1); 출짧(CODE_fasti);
            출정(12 + aðferð_lengd[númer]); 출짧(128); 출짧(함수지역[númer]); 출정(aðferð_lengd[númer]);
            for (int rauf_færsla = 0; rauf_færsla < aðferð_lengd[númer]; rauf_færsla++) 출바(CODE_VALUE[aðferð_CODE[númer] + rauf_færsla]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Keyra_2() {
        if (notandi.인수개수() == 1 && 자바도구.같음(notandi.Viðföng(0), "-version")) {
            notandi.Skrift("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (notandi.인수개수() != 1) { notandi.Skrift("Usage: javac FILE.java\n"); return 2; }
        int heiti_breyta_stærð = 자바도구.Heiti(skrá_heiti_SMS, notandi.Viðföng(0));
        if (heiti_breyta_stærð < 6 || heiti_breyta_stærð > 62 || skrá_heiti_SMS[heiti_breyta_stærð - 5] != '.' || skrá_heiti_SMS[heiti_breyta_stærð - 4] != 'j'
            || skrá_heiti_SMS[heiti_breyta_stærð - 3] != 'a' || skrá_heiti_SMS[heiti_breyta_stærð - 2] != 'v' || skrá_heiti_SMS[heiti_breyta_stærð - 1] != 'a') {
            notandi.Skrift("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        uppruni_breyta_stærð = notandi.파일읽기(skrá_heiti_SMS, Uppruni);
        if (uppruni_breyta_stærð < 0) { notandi.Skrift("javac: cannot read source: "); 자바도구.skrifa_númer(uppruni_breyta_stærð); notandi.skrifa_stafur_VALUE(10); return 1; }
        uppruni_breyta_stærð = 자바도구.원문해독(Uppruni, uppruni_breyta_stærð);
        if (uppruni_breyta_stærð < 0) { notandi.Skrift("javac error: invalid UTF-8 source\n"); return 1; }
        klippa_VALUE(); if (!Villa) 선언읽기();
        if (!Villa) {
            if (tákn_lengd[klasi_tákn] != heiti_breyta_stærð - 5) bilun_VALUE("class name must match file name");
            for (int númer = 0; númer < heiti_breyta_stærð - 5; númer++) if (Uppruni[tákn_staða[klasi_tákn] + númer] != skrá_heiti_SMS[númer]) bilun_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < aðferð_COUNT && !Villa; 현재함수++) {
            Staðsetning = aðferð_meginmál[현재함수]; aðferð_CODE[현재함수] = CODE_breyta_stærð; staðbundið_COUNT = 0; 깊이 = 0;
            for (int númer = 0; númer < aðferð_frumbreyta_COUNT[현재함수]; númer++) bæta_við_staðbundið(aðferð_frumbreyta_heiti[현재함수 * 16 + númer], aðferð_frumbreyta_TYPE[현재함수 * 16 + númer]);
            boolean skila_mæld_stærð = setning_VALUE();
            if (!skila_mæld_stærð && aðferð_skila[현재함수] != 0) bilun_VALUE("missing return");
            // grein 뒤의 합류 지점은 반드시 raun_gögn 명령이어야 한다 (버전 49 검증기).
            if (aðferð_skila[현재함수] == 0) 내보내기(177);
            else { boolean heiltala = aðferð_skila[현재함수] <= 2 || aðferð_skila[현재함수] == 5; 내보내기(heiltala ? 3 : 1); 내보내기(heiltala ? 172 : 176); }
            if (Staðsetning != aðferð_ljúka[현재함수]) bilun_VALUE("invalid method body");
            함수지역[현재함수] = staðbundið_COUNT; aðferð_lengd[현재함수] = CODE_breyta_stærð - aðferð_CODE[현재함수];
        }
        if (Villa) return 1;
        skrifa_klasi(); if (Villa) return 1;
        skrá_heiti_SMS[heiti_breyta_stærð - 4] = 'c'; skrá_heiti_SMS[heiti_breyta_stærð - 3] = 'l'; skrá_heiti_SMS[heiti_breyta_stærð - 2] = 'a';
        skrá_heiti_SMS[heiti_breyta_stærð - 1] = 's'; skrá_heiti_SMS[heiti_breyta_stærð] = 's'; skrá_heiti_SMS[heiti_breyta_stærð + 1] = 0;
        int NIÐURSTAÐA = notandi.skrifa_skrá(skrá_heiti_SMS, úttak, úttak_breyta_stærð);
        if (NIÐURSTAÐA < 0) { notandi.Skrift("javac: cannot save class: "); 자바도구.skrifa_númer(NIÐURSTAÐA); notandi.skrifa_stafur_VALUE(10); return 1; }
        notandi.Skrift("Compiled: "); for (int númer = 0; skrá_heiti_SMS[númer] != 0; númer++) notandi.skrifa_stafur_VALUE(skrá_heiti_SMS[númer]);
        notandi.Skrift(" (JVM class version 49)\n"); return 0;
    }
}
