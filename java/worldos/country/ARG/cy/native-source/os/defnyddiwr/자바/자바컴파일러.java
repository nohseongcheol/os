// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java ffynhonnell_coeden -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] FFYNHONNELL = new int[16384], Allbwn = new int[16384], cod_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], tocyn_safle = new int[2048], tocyn_hyd = new int[2048];
    static int[] cysonyn_VALUE = new int[4096], cysonyn_OFFSET = new int[512];
    static int[] 문자 = new int[512], ffeil_enw_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int ffynhonnell_newid_maint, tocyn_COUNT_3176ee99, safle, cod_newid_maint, cysonyn_newid_maint, cysonyn_COUNT = 1, 출력크기, nod_hyd;
    static boolean Gwall;
    static int Dosbarth_tocyn, Dosbarth_cysonyn, 부모상수, cod_cysonyn;
    static int[] dull_cofnod_enw = new int[32], dull_return = new int[32], dull_arg_COUNT = new int[32];
    static int[] dull_arg_enw = new int[512], dull_arg_TYPE = new int[512];
    static int[] dull_corff = new int[32], dull_gorffen = new int[32], dull_cod = new int[32];
    static int[] dull_hyd = new int[32], 함수지역 = new int[32], dull_enw_cysonyn = new int[32], 함수서술 = new int[32];
    static int[] dull_mynediad = new int[32];
    static int dull_COUNT, 현재함수, lleol_COUNT, 깊이, 식깊이;
    static int[] lleol_enw = new int[128], lleol_TYPE = new int[128], 지역깊이 = new int[128];

    static void methiant_VALUE(String 이유) {
        if (!Gwall) {
            defnyddiwr.Ysgrifennu("javac error: "); defnyddiwr.Ysgrifennu(이유);
            defnyddiwr.Ysgrifennu(" at line ");
            int llinell = 1, 끝 = safle < tocyn_COUNT_3176ee99 ? tocyn_safle[safle] : ffynhonnell_newid_maint;
            for (int 수 = 0; 수 < 끝; 수++) if (FFYNHONNELL[수] == 10) llinell++;
            자바도구.수쓰기(llinell); defnyddiwr.ysgrifennu_nod_VALUE(10);
        }
        Gwall = true;
    }
    static boolean nod_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean digid_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= tocyn_COUNT_3176ee99 || 나 >= tocyn_COUNT_3176ee99 || tocyn_hyd[가] != tocyn_hyd[나]) return false;
        for (int 수 = 0; 수 < tocyn_hyd[가]; 수++) if (FFYNHONNELL[tocyn_safle[가] + 수] != FFYNHONNELL[tocyn_safle[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int tocyn_VALUE_eb540501, String Word_SMS) {
        if (tocyn_VALUE_eb540501 < 0 || tocyn_VALUE_eb540501 >= tocyn_COUNT_3176ee99 || tocyn_hyd[tocyn_VALUE_eb540501] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (FFYNHONNELL[tocyn_safle[tocyn_VALUE_eb540501] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return safle < tocyn_COUNT_3176ee99 ? 토큰종류[safle] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; safle++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) methiant_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(safle, Word_SMS)) return false; safle++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) methiant_VALUE(Word_SMS); }
    static int dynodwr_VALUE() {
        int mesur = safle;
        if (종류() != 256) methiant_VALUE("identifier required"); else safle++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Gweithredu_2 = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Gweithredu_2 == tocyn_hyd[mesur];
                for (int slot_cofnod = Gweithredu_2; 같음 && slot_cofnod < 수; slot_cofnod++) if (예약어.charAt(slot_cofnod) != FFYNHONNELL[tocyn_safle[mesur] + slot_cofnod - Gweithredu_2]) 같음 = false;
                if (같음) methiant_VALUE("reserved word cannot be an identifier");
                Gweithredu_2 = 수 + 1;
            }
        }
        return mesur;
    }
    static void torri_VALUE() {
        int 수 = 0;
        while (수 < ffynhonnell_newid_maint && !Gwall) {
            int VALUE = FFYNHONNELL[수], Gweithredu_2 = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < ffynhonnell_newid_maint && FFYNHONNELL[수 + 1] == '/') {
                while (수 < ffynhonnell_newid_maint && FFYNHONNELL[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < ffynhonnell_newid_maint && FFYNHONNELL[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < ffynhonnell_newid_maint && !(FFYNHONNELL[수] == '*' && FFYNHONNELL[수 + 1] == '/')) 수++;
                if (수 + 1 >= ffynhonnell_newid_maint) { methiant_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (nod_VALUE(VALUE)) { 종류 = 256; while (수 < ffynhonnell_newid_maint && 문자이름규칙.이어진글자(FFYNHONNELL[수])) 수++; }
            else if (digid_VALUE(VALUE)) { 종류 = 257; while (수 < ffynhonnell_newid_maint && digid_VALUE(FFYNHONNELL[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < ffynhonnell_newid_maint && FFYNHONNELL[수] != VALUE && FFYNHONNELL[수] != 10 && FFYNHONNELL[수] != 13) {
                    if (FFYNHONNELL[수] == '\\') 수++;
                    수++;
                }
                if (수 >= ffynhonnell_newid_maint || FFYNHONNELL[수] != VALUE) { methiant_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < ffynhonnell_newid_maint) {
                    int Nesaf_eitem = FFYNHONNELL[수];
                    if (VALUE == '=' && Nesaf_eitem == '=') 종류 = 300;
                    if (VALUE == '!' && Nesaf_eitem == '=') 종류 = 301;
                    if (VALUE == '<' && Nesaf_eitem == '=') 종류 = 302;
                    if (VALUE == '>' && Nesaf_eitem == '=') 종류 = 303;
                    if (VALUE == '&' && Nesaf_eitem == '&') 종류 = 304;
                    if (VALUE == '|' && Nesaf_eitem == '|') 종류 = 305;
                    if (VALUE == '+' && Nesaf_eitem == '+') 종류 = 306;
                    if (VALUE == '-' && Nesaf_eitem == '-') 종류 = 307;
                    if (VALUE == '+' && Nesaf_eitem == '=') 종류 = 308;
                    if (VALUE == '-' && Nesaf_eitem == '=') 종류 = 309;
                    if (VALUE == '*' && Nesaf_eitem == '=') 종류 = 310;
                    if (VALUE == '/' && Nesaf_eitem == '=') 종류 = 311;
                    if (VALUE == '%' && Nesaf_eitem == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (tocyn_COUNT_3176ee99 == 토큰종류.length - 1) { methiant_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[tocyn_COUNT_3176ee99] = 종류; tocyn_safle[tocyn_COUNT_3176ee99] = Gweithredu_2; tocyn_hyd[tocyn_COUNT_3176ee99++] = 수 - Gweithredu_2;
        }
    }
    static void ysgrifennu_cysonyn_beit(int VALUE) {
        if (cysonyn_newid_maint == cysonyn_VALUE.length) { methiant_VALUE("constant pool too large"); return; }
        cysonyn_VALUE[cysonyn_newid_maint++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { ysgrifennu_cysonyn_beit(VALUE >> 8); ysgrifennu_cysonyn_beit(VALUE); }
    static int cofrestru_cysonyn(int Gweithredu_2) {
        for (int 수 = 1; 수 < cysonyn_COUNT; 수++) {
            int 앞 = cysonyn_OFFSET[수], hyd_VALUE = (수 + 1 < cysonyn_COUNT ? cysonyn_OFFSET[수 + 1] : Gweithredu_2) - 앞;
            if (hyd_VALUE != cysonyn_newid_maint - Gweithredu_2) continue;
            boolean 같음 = true;
            for (int slot_cofnod = 0; slot_cofnod < hyd_VALUE; slot_cofnod++) if (cysonyn_VALUE[앞 + slot_cofnod] != cysonyn_VALUE[Gweithredu_2 + slot_cofnod]) 같음 = false;
            if (같음) { cysonyn_newid_maint = Gweithredu_2; return 수; }
        }
        if (cysonyn_COUNT == cysonyn_OFFSET.length) { methiant_VALUE("too many constants"); return 0; }
        cysonyn_OFFSET[cysonyn_COUNT] = Gweithredu_2;
        return cysonyn_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (nod_hyd == 문자.length) { methiant_VALUE("text too long"); return; }
        문자[nod_hyd++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int nod_cysonyn() {
        int Gweithredu_2 = cysonyn_newid_maint; ysgrifennu_cysonyn_beit(1); 상짧(0);
        for (int 수 = 0; 수 < nod_hyd; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) ysgrifennu_cysonyn_beit(VALUE);
            else if (VALUE < 2048) { ysgrifennu_cysonyn_beit(192 | VALUE >> 6); ysgrifennu_cysonyn_beit(128 | VALUE & 63); }
            else { ysgrifennu_cysonyn_beit(224 | VALUE >> 12); ysgrifennu_cysonyn_beit(128 | VALUE >> 6 & 63); ysgrifennu_cysonyn_beit(128 | VALUE & 63); }
        }
        if (Gwall) return 0;
        int hyd_VALUE = cysonyn_newid_maint - Gweithredu_2 - 3;
        cysonyn_VALUE[Gweithredu_2 + 1] = hyd_VALUE >> 8; cysonyn_VALUE[Gweithredu_2 + 2] = hyd_VALUE & 255;
        return cofrestru_cysonyn(Gweithredu_2);
    }
    static int Word_cysonyn(String Word_SMS) { nod_hyd = 0; 말추가(Word_SMS); return nod_cysonyn(); }
    static int tocyn_cysonyn(int tocyn_VALUE_eb540501) {
        nod_hyd = 0;
        for (int 수 = 0; 수 < tocyn_hyd[tocyn_VALUE_eb540501]; 수++) 글추가(FFYNHONNELL[tocyn_safle[tocyn_VALUE_eb540501] + 수]);
        return nod_cysonyn();
    }
    static int cyfeiriad(int 종류, int 가, int 나) {
        int Gweithredu_2 = cysonyn_newid_maint; ysgrifennu_cysonyn_beit(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return cofrestru_cysonyn(Gweithredu_2);
    }
    static int cyfeirnod_allanol(int 종류, String perchennog_VALUE, String Enw, String 서술) {
        int perchennog_dynodwr = cyfeiriad(7, Word_cysonyn(perchennog_VALUE), 0);
        int enw_COUNT = Word_cysonyn(Enw), fformat_COUNT = Word_cysonyn(서술);
        return cyfeiriad(종류, perchennog_dynodwr, cyfeiriad(12, enw_COUNT, fformat_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (cod_newid_maint == cod_VALUE.length) { methiant_VALUE("bytecode too large"); return; }
        cod_VALUE[cod_newid_maint++] = VALUE & 255;
    }
    static void Gorchymyn(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Gweithredu_2 = cysonyn_newid_maint; ysgrifennu_cysonyn_beit(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Gorchymyn(19, cofrestru_cysonyn(Gweithredu_2));
    }
    static int cangen(int Gorchymyn) { int mesur = cod_newid_maint; Gorchymyn(Gorchymyn, 0); return mesur; }
    static void Dolen_VALUE(int cangen, int targed_gwrthrych) {
        if (Gwall) return;
        int 거리 = targed_gwrthrych - cangen;
        if (거리 < -32768 || 거리 > 32767 || cangen < 0 || cangen + 2 >= cod_newid_maint) { methiant_VALUE("invalid branch"); return; }
        cod_VALUE[cangen + 1] = 거리 >> 8 & 255; cod_VALUE[cangen + 2] = 거리 & 255;
    }
    static void 비교값(int Gorchymyn) {
        int TRUE_VALUE = cangen(Gorchymyn); 내보내기(3); int 끝 = cangen(167);
        Dolen_VALUE(TRUE_VALUE, cod_newid_maint); 내보내기(4); Dolen_VALUE(끝, cod_newid_maint);
    }
    static int fformat_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        methiant_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void ychwanegu_fformat(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. eithriad Proses_VALUE_cofnod 본문은 lletya javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Cymraeg");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("eithriad") || TAKE_Word("실행예외") || TAKE_Word("I_O_eithriad") || TAKE_Word("aros_TIMEOUT_eithriad") || TAKE_Word("ADDRESS_LOOKUP_eithriad") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("annilys_arg_eithriad") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NWL_cyfeiriad_eithriad") || TAKE_Word("산술예외") || TAKE_Word("cyflwr_eithriad") || TAKE_Word("TYPE_Castio_eithriad") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARAE_Store_methiant") || TAKE_Word("edefyn_cyflwr_eithriad") || TAKE_Word("대기중단예외")) return;
        methiant_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(safle, "Cymraeg")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) methiant_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); Dosbarth_tocyn = dynodwr_VALUE();
        Dosbarth_cysonyn = cyfeiriad(7, tocyn_cysonyn(Dosbarth_tocyn), 0);
        부모상수 = cyfeiriad(7, Word_cysonyn("java/lang/Object"), 0); cod_cysonyn = Word_cysonyn("Code"); 요구('{');
        while (!Gwall && 종류() != '}') {
            if (dull_COUNT == 32) { methiant_VALUE("too many methods"); break; }
            int mynediad_cofnod = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int SWYDDOGAETH_VALUE = dull_COUNT++;
            dull_mynediad[SWYDDOGAETH_VALUE] = mynediad_cofnod | 8;
            dull_return[SWYDDOGAETH_VALUE] = fformat_VALUE(); dull_cofnod_enw[SWYDDOGAETH_VALUE] = dynodwr_VALUE(); 요구('(');
            for (int 앞 = 0; 앞 < SWYDDOGAETH_VALUE; 앞++) if (이름같음(dull_cofnod_enw[앞], dull_cofnod_enw[SWYDDOGAETH_VALUE])) methiant_VALUE("duplicate method (overloading unsupported)");
            while (!Gwall && 종류() != ')') {
                int 수 = dull_arg_COUNT[SWYDDOGAETH_VALUE];
                if (수 == 16) { methiant_VALUE("too many parameters"); break; }
                int TYPE_VALUE = fformat_VALUE(); if (TYPE_VALUE == 0) methiant_VALUE("void parameter");
                dull_arg_TYPE[SWYDDOGAETH_VALUE * 16 + 수] = TYPE_VALUE; dull_arg_enw[SWYDDOGAETH_VALUE * 16 + 수] = dynodwr_VALUE();
                dull_arg_COUNT[SWYDDOGAETH_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!Gwall && 받기(','));
            }
            dull_corff[SWYDDOGAETH_VALUE] = safle; 요구('{');
            int 중첩 = 1;
            while (safle < tocyn_COUNT_3176ee99 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                safle++;
            }
            if (중첩 != 0) methiant_VALUE("unclosed method body");
            dull_gorffen[SWYDDOGAETH_VALUE] = safle;
            dull_enw_cysonyn[SWYDDOGAETH_VALUE] = tocyn_cysonyn(dull_cofnod_enw[SWYDDOGAETH_VALUE]);
            nod_hyd = 0; 글추가('(');
            for (int 수 = 0; 수 < dull_arg_COUNT[SWYDDOGAETH_VALUE]; 수++) ychwanegu_fformat(dull_arg_TYPE[SWYDDOGAETH_VALUE * 16 + 수]);
            글추가(')'); ychwanegu_fformat(dull_return[SWYDDOGAETH_VALUE]); 함수서술[SWYDDOGAETH_VALUE] = nod_cysonyn();
        }
        요구('}'); if (safle != tocyn_COUNT_3176ee99) methiant_VALUE("extra input after class");
    }
    static int FIND_lleol(int Enw) {
        for (int 수 = lleol_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lleol_enw[수], Enw)) return 수;
        methiant_VALUE("unknown variable"); return 0;
    }
    static int ychwanegu_lleol(int Enw, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lleol_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lleol_enw[수], Enw)) methiant_VALUE("duplicate local variable");
        if (lleol_COUNT == 128) { methiant_VALUE("too many locals"); return 0; }
        lleol_enw[lleol_COUNT] = Enw; lleol_TYPE[lleol_COUNT] = TYPE_VALUE; 지역깊이[lleol_COUNT] = 깊이;
        return lleol_COUNT++;
    }
    static boolean cyfanrif_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lleol_TYPE[수] <= 2 || lleol_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void ysgrifennu_lleol(int 수) { 내보내기(lleol_TYPE[수] <= 2 || lleol_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void dilysu_TYPE(int go_iawn_data, int 기대) { if (go_iawn_data != 기대 && !(go_iawn_data == 5 && 기대 == 1)) methiant_VALUE("type mismatch"); }
    static void 문자읽기(int tocyn_VALUE_eb540501) {
        nod_hyd = 0; int Gweithredu_2 = tocyn_safle[tocyn_VALUE_eb540501] + 1, 끝 = tocyn_safle[tocyn_VALUE_eb540501] + tocyn_hyd[tocyn_VALUE_eb540501] - 1;
        while (Gweithredu_2 < 끝 && !Gwall) {
            int VALUE = FFYNHONNELL[Gweithredu_2++];
            if (VALUE == '\\') {
                if (Gweithredu_2 == 끝) { methiant_VALUE("invalid escape"); break; }
                VALUE = FFYNHONNELL[Gweithredu_2++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') methiant_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int dosrannu_cyfanrif(int tocyn_VALUE_eb540501, boolean 음수) {
        if (tocyn_hyd[tocyn_VALUE_eb540501] > 1 && FFYNHONNELL[tocyn_safle[tocyn_VALUE_eb540501]] == '0') methiant_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < tocyn_hyd[tocyn_VALUE_eb540501]; 수++) {
            int digid_eitem = FFYNHONNELL[tocyn_safle[tocyn_VALUE_eb540501] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && digid_eitem > (음수 ? 8 : 7)) methiant_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - digid_eitem;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = fformat_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { methiant_VALUE("only file streams supported by new in source"); return 0; }
            String perchennog_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Gorchymyn(187, cyfeiriad(7, Word_cysonyn(perchennog_VALUE), 0)); 내보내기(89);
            요구('('); dilysu_TYPE(mynegiad_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) methiant_VALUE("input stream constructor arguments"); dilysu_TYPE(mynegiad_VALUE(), 2); 이어 = true; }
            요구(')');
            Gorchymyn(183, cyfeirnod_allanol(10, perchennog_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = mynegiad_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(dosrannu_cyfanrif(safle++, false)); return 1; }
        if (종류() == 258) { 문자읽기(safle++); Gorchymyn(19, cyfeiriad(8, nod_cysonyn(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(safle++); if (nod_hyd != 1) methiant_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Cymraeg")) {
            요구('.'); 말요구("자체"); 요구('.');
            String perchennog_VALUE = "", dull_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, mesur = 0;
            if (TAKE_Word("Allbwn")) {
                perchennog_VALUE = "Cymraeg/자체/Allbwn"; 요구('.');
                if (TAKE_Word("ysgrifennu_llinell")) { dull_VALUE = "ysgrifennu_llinell"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Ysgrifennu")) { dull_VALUE = "Ysgrifennu"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { dull_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else methiant_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                perchennog_VALUE = "Cymraeg/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("hyd_VALUE")) { dull_VALUE = "hyd_VALUE"; 서술 = "(Ljava/lang/String;)I"; mesur = 1; }
                else if (TAKE_Word("cod_nod_COUNT")) { dull_VALUE = "cod_nod_COUNT"; 서술 = "(Ljava/lang/String;)I"; mesur = 1; }
                else if (TAKE_Word("dosrannu_cyfanrif")) { dull_VALUE = "dosrannu_cyfanrif"; 서술 = "(Ljava/lang/String;)I"; mesur = 1; }
                else if (TAKE_Word("ysgrifennu_cyfanrif_VALUE")) { dull_VALUE = "ysgrifennu_cyfanrif_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; mesur = 3; }
                else if (TAKE_Word("같음")) { dull_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; mesur = 2; }
                else if (TAKE_Word("gludo_SMS")) { dull_VALUE = "gludo_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; mesur = 3; }
                else if (TAKE_Word("torri_VALUE")) { dull_VALUE = "torri_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; mesur = 3; }
                else methiant_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Ffeil")) {
                perchennog_VALUE = "Cymraeg/자체/Ffeil"; 요구('.'); 가 = 3;
                if (TAKE_Word("Darllen")) { dull_VALUE = "Darllen"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; mesur = 3; }
                else if (TAKE_Word("Ysgrifennu")) { dull_VALUE = "Ysgrifennu"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else methiant_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                perchennog_VALUE = "Cymraeg/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { dull_VALUE = "너비"; 서술 = "()I"; mesur = 1; }
                else if (TAKE_Word("높이")) { dull_VALUE = "높이"; 서술 = "()I"; mesur = 1; }
                else if (TAKE_Word("사각형")) { dull_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("지우기")) { dull_VALUE = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { dull_VALUE = "기다리기"; 서술 = "()V"; }
                else methiant_VALUE("unknown Korean framebuffer method");
            } else methiant_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) dilysu_TYPE(mynegiad_VALUE(), 가);
            if (나 != 0) { 요구(','); dilysu_TYPE(mynegiad_VALUE(), 나); }
            if (다 != 0) { 요구(','); dilysu_TYPE(mynegiad_VALUE(), 다); }
            if (라 != 0) { 요구(','); dilysu_TYPE(mynegiad_VALUE(), 라); }
            if (마 != 0) { 요구(','); dilysu_TYPE(mynegiad_VALUE(), 마); }
            요구(')'); Gorchymyn(184, cyfeirnod_allanol(10, perchennog_VALUE, dull_VALUE, 서술)); return mesur;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); dilysu_TYPE(mynegiad_VALUE(), 3); 요구(')');
            Gorchymyn(184, cyfeirnod_allanol(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Enw = dynodwr_VALUE();
        if (받기('(')) {
            int SWYDDOGAETH_VALUE = -1;
            for (int 수 = 0; 수 < dull_COUNT; 수++) if (이름같음(Enw, dull_cofnod_enw[수])) SWYDDOGAETH_VALUE = 수;
            if (SWYDDOGAETH_VALUE < 0) { methiant_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!Gwall && 종류() != ')') {
                if (수 >= dull_arg_COUNT[SWYDDOGAETH_VALUE]) { methiant_VALUE("too many arguments"); break; }
                dilysu_TYPE(mynegiad_VALUE(), dull_arg_TYPE[SWYDDOGAETH_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != dull_arg_COUNT[SWYDDOGAETH_VALUE]) methiant_VALUE("argument count mismatch");
            Gorchymyn(184, cyfeiriad(10, Dosbarth_cysonyn, cyfeiriad(12, dull_enw_cysonyn[SWYDDOGAETH_VALUE], 함수서술[SWYDDOGAETH_VALUE])));
            return dull_return[SWYDDOGAETH_VALUE];
        }
        int lleol_cwmpas = FIND_lleol(Enw), TYPE_VALUE = lleol_TYPE[lleol_cwmpas]; 지역읽기(lleol_cwmpas);
        while (!Gwall) {
            if (받기('[')) { dilysu_TYPE(TYPE_VALUE, 4); dilysu_TYPE(mynegiad_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String perchennog_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Gorchymyn(182, cyfeirnod_allanol(10, perchennog_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Gorchymyn(182, cyfeirnod_allanol(10, perchennog_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); dilysu_TYPE(mynegiad_VALUE(), 1); 요구(')'); Gorchymyn(182, cyfeirnod_allanol(10, perchennog_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { methiant_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { dilysu_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Gorchymyn(182, cyfeirnod_allanol(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { methiant_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { dilysu_TYPE(단항(), 2); 비교값(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(dosrannu_cyfanrif(safle++, true));
            else { dilysu_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { dilysu_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!Gwall && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int amgodio_VALUE = 종류(); safle++; dilysu_TYPE(TYPE_VALUE, 1); dilysu_TYPE(단항(), 1);
            내보내기(amgodio_VALUE == '*' ? 104 : amgodio_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!Gwall && (종류() == '+' || 종류() == '-')) {
            int amgodio_VALUE = 종류(); safle++; int 경계 = cod_newid_maint, BACK_VALUE_TYPE = 곱식();
            if (amgodio_VALUE == '+' && (TYPE_VALUE == 3 || BACK_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, BACK_VALUE_TYPE); TYPE_VALUE = 3; }
            else { dilysu_TYPE(TYPE_VALUE, 1); dilysu_TYPE(BACK_VALUE_TYPE, 1); 내보내기(amgodio_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) methiant_VALUE("unsupported concatenation type");
        return cyfeirnod_allanol(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int BACK_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT cod_VALUE 앞에 cynhyrchu 코드를 삽입한다.
        // RIGHT mynegiad_VALUE 내부의 cymar_VALUE cangen 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = cod_newid_maint;
        Gorchymyn(187, cyfeiriad(7, Word_cysonyn("java/lang/StringBuilder"), 0)); 내보내기(89);
        Gorchymyn(183, cyfeirnod_allanol(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Gorchymyn(182, 붙임참조(앞형));
        if (Gwall) return;
        int hyd_VALUE = cod_newid_maint - 끝;
        for (int 수 = 0; 수 < hyd_VALUE; 수++) 삽입코드[수] = cod_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) cod_VALUE[수 + hyd_VALUE] = cod_VALUE[수];
        for (int 수 = 0; 수 < hyd_VALUE; 수++) cod_VALUE[경계 + 수] = 삽입코드[수];
        Gorchymyn(182, 붙임참조(BACK_VALUE_TYPE)); Gorchymyn(182, cyfeirnod_allanol(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int TYPE_VALUE = 합식();
        while (!Gwall && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int amgodio_VALUE = 종류(); safle++; dilysu_TYPE(TYPE_VALUE, 1); dilysu_TYPE(합식(), 1);
            비교값(amgodio_VALUE == '<' ? 161 : amgodio_VALUE == '>' ? 163 : amgodio_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = 비교식();
        while (!Gwall && (종류() == 300 || 종류() == 301)) {
            int amgodio_VALUE = 종류(); safle++; int BACK_VALUE_TYPE = 비교식();
            if (TYPE_VALUE == 0 || BACK_VALUE_TYPE == 0) methiant_VALUE("void expression");
            if (!(cyfanrif_TYPE(TYPE_VALUE) && cyfanrif_TYPE(BACK_VALUE_TYPE))) dilysu_TYPE(BACK_VALUE_TYPE, TYPE_VALUE);
            비교값((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (amgodio_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!Gwall && 받기(304)) {
            dilysu_TYPE(TYPE_VALUE, 2); int 가 = cangen(153); dilysu_TYPE(동등식(), 2); int 나 = cangen(153);
            내보내기(4); int 끝 = cangen(167); Dolen_VALUE(가, cod_newid_maint); Dolen_VALUE(나, cod_newid_maint); 내보내기(3); Dolen_VALUE(끝, cod_newid_maint); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int mynegiad_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!Gwall && 받기(305)) {
            dilysu_TYPE(TYPE_VALUE, 2); int 가 = cangen(154); dilysu_TYPE(논리곱(), 2); int 나 = cangen(154);
            내보내기(3); int 끝 = cangen(167); Dolen_VALUE(가, cod_newid_maint); Dolen_VALUE(나, cod_newid_maint); 내보내기(4); Dolen_VALUE(끝, cod_newid_maint); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void aseiniad_VALUE(boolean 선언허용) {
        if (Word_VALUE(safle, "int") || Word_VALUE(safle, "boolean") || Word_VALUE(safle, "String") || Word_VALUE(safle, "char")
            || Word_VALUE(safle, "FileInputStream") || Word_VALUE(safle, "FileOutputStream")) {
            if (!선언허용) methiant_VALUE("declaration not allowed here");
            int TYPE_VALUE = fformat_VALUE(), Enw = dynodwr_VALUE(); 요구('='); dilysu_TYPE(mynegiad_VALUE(), TYPE_VALUE);
            ysgrifennu_lleol(ychwanegu_lleol(Enw, TYPE_VALUE)); return;
        }
        int Enw = dynodwr_VALUE(), lleol_cwmpas = FIND_lleol(Enw);
        if (받기('=')) { dilysu_TYPE(mynegiad_VALUE(), lleol_TYPE[lleol_cwmpas]); ysgrifennu_lleol(lleol_cwmpas); }
        else if (종류() >= 308 && 종류() <= 312) {
            int amgodio_VALUE = 종류(); safle++; 지역읽기(lleol_cwmpas); int 경계 = cod_newid_maint, BACK_VALUE_TYPE = mynegiad_VALUE();
            if (amgodio_VALUE == 308 && lleol_TYPE[lleol_cwmpas] == 3) 결합(경계, 3, BACK_VALUE_TYPE);
            else {
                dilysu_TYPE(lleol_TYPE[lleol_cwmpas], 1); dilysu_TYPE(BACK_VALUE_TYPE, 1);
                내보내기(amgodio_VALUE == 308 ? 96 : amgodio_VALUE == 309 ? 100 : amgodio_VALUE == 310 ? 104 : amgodio_VALUE == 311 ? 108 : 112);
                if (lleol_TYPE[lleol_cwmpas] == 5) 내보내기(146);
            }
            ysgrifennu_lleol(lleol_cwmpas);
        }
        else if (종류() == 306 || 종류() == 307) {
            dilysu_TYPE(lleol_TYPE[lleol_cwmpas], 1); 내보내기(132); 내보내기(lleol_cwmpas); 내보내기(종류() == 306 ? 1 : 255); safle++;
            if (lleol_TYPE[lleol_cwmpas] == 5) { 지역읽기(lleol_cwmpas); 내보내기(146); ysgrifennu_lleol(lleol_cwmpas); }
        } else methiant_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Gorchymyn(178, cyfeirnod_allanol(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean gwag_arg = 종류() == ')';
        int TYPE_VALUE = gwag_arg ? 0 : mynegiad_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !gwag_arg)) methiant_VALUE("unsupported print argument");
        Gorchymyn(182, cyfeirnod_allanol(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean gosodiad_VALUE() {
        if (Gwall) return false;
        if (깊이 > 32) { methiant_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean return_mesur = false;
            while (!Gwall && 종류() != '}') { if (return_mesur) methiant_VALUE("unreachable statement"); return_mesur = gosodiad_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < lleol_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return return_mesur;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : mynegiad_VALUE(); dilysu_TYPE(TYPE_VALUE, dull_return[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); dilysu_TYPE(mynegiad_VALUE(), 2); 요구(')'); int FALSE_VALUE = cangen(153);
            깊이++; boolean 가 = rheoli_gosodiad(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = cangen(167); Dolen_VALUE(FALSE_VALUE, cod_newid_maint); 깊이++; boolean 나 = rheoli_gosodiad(); 깊이--; Dolen_VALUE(끝, cod_newid_maint); return 가 && 나; }
            Dolen_VALUE(FALSE_VALUE, cod_newid_maint); return false;
        }
        if (TAKE_Word("while")) {
            int Gweithredu_2 = cod_newid_maint; 요구('('); dilysu_TYPE(mynegiad_VALUE(), 2); 요구(')'); int 끝 = cangen(153);
            깊이++; rheoli_gosodiad(); 깊이--; Dolen_VALUE(cangen(167), Gweithredu_2); Dolen_VALUE(끝, cod_newid_maint); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') aseiniad_VALUE(true); 요구(';');
            int cyflwr = cod_newid_maint; if (종류() == ';') 내보내기(4); else dilysu_TYPE(mynegiad_VALUE(), 2); 요구(';');
            int 끝 = cangen(153), corff_y_testun = cangen(167), adnewyddu = cod_newid_maint;
            if (종류() != ')') aseiniad_VALUE(false); 요구(')'); Dolen_VALUE(cangen(167), cyflwr); Dolen_VALUE(corff_y_testun, cod_newid_maint);
            rheoli_gosodiad(); Dolen_VALUE(cangen(167), adnewyddu); Dolen_VALUE(끝, cod_newid_maint);
            for (int 수 = 0; 수 < lleol_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(safle, "System")) { 화면출력(); return false; }
        if (종류() == 256 && safle + 1 < tocyn_COUNT_3176ee99 && (토큰종류[safle + 1] == '(' || 토큰종류[safle + 1] == '.')) {
            int TYPE_VALUE = mynegiad_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        aseiniad_VALUE(true); 요구(';'); return false;
    }
    static boolean rheoli_gosodiad() {
        if (Word_VALUE(safle, "int") || Word_VALUE(safle, "boolean") || Word_VALUE(safle, "char") || Word_VALUE(safle, "String")
            || Word_VALUE(safle, "FileInputStream") || Word_VALUE(safle, "FileOutputStream")) methiant_VALUE("local declaration requires braces");
        return gosodiad_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == Allbwn.length) methiant_VALUE("class file too large"); else Allbwn[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void ysgrifennu_Dosbarth() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(cysonyn_COUNT);
        for (int 수 = 0; 수 < cysonyn_newid_maint; 수++) 출바(cysonyn_VALUE[수]);
        출짧(0x21); 출짧(Dosbarth_cysonyn); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(dull_COUNT);
        for (int 수 = 0; 수 < dull_COUNT; 수++) {
            출짧(dull_mynediad[수]); 출짧(dull_enw_cysonyn[수]); 출짧(함수서술[수]); 출짧(1); 출짧(cod_cysonyn);
            출정(12 + dull_hyd[수]); 출짧(128); 출짧(함수지역[수]); 출정(dull_hyd[수]);
            for (int slot_cofnod = 0; slot_cofnod < dull_hyd[수]; slot_cofnod++) 출바(cod_VALUE[dull_cod[수] + slot_cofnod]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Gweithredu_2() {
        if (defnyddiwr.인수개수() == 1 && 자바도구.같음(defnyddiwr.인수(0), "-version")) {
            defnyddiwr.Ysgrifennu("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (defnyddiwr.인수개수() != 1) { defnyddiwr.Ysgrifennu("Usage: javac FILE.java\n"); return 2; }
        int enw_newid_maint = 자바도구.Enw(ffeil_enw_SMS, defnyddiwr.인수(0));
        if (enw_newid_maint < 6 || enw_newid_maint > 62 || ffeil_enw_SMS[enw_newid_maint - 5] != '.' || ffeil_enw_SMS[enw_newid_maint - 4] != 'j'
            || ffeil_enw_SMS[enw_newid_maint - 3] != 'a' || ffeil_enw_SMS[enw_newid_maint - 2] != 'v' || ffeil_enw_SMS[enw_newid_maint - 1] != 'a') {
            defnyddiwr.Ysgrifennu("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        ffynhonnell_newid_maint = defnyddiwr.파일읽기(ffeil_enw_SMS, FFYNHONNELL);
        if (ffynhonnell_newid_maint < 0) { defnyddiwr.Ysgrifennu("javac: cannot read source: "); 자바도구.수쓰기(ffynhonnell_newid_maint); defnyddiwr.ysgrifennu_nod_VALUE(10); return 1; }
        ffynhonnell_newid_maint = 자바도구.원문해독(FFYNHONNELL, ffynhonnell_newid_maint);
        if (ffynhonnell_newid_maint < 0) { defnyddiwr.Ysgrifennu("javac error: invalid UTF-8 source\n"); return 1; }
        torri_VALUE(); if (!Gwall) 선언읽기();
        if (!Gwall) {
            if (tocyn_hyd[Dosbarth_tocyn] != enw_newid_maint - 5) methiant_VALUE("class name must match file name");
            for (int 수 = 0; 수 < enw_newid_maint - 5; 수++) if (FFYNHONNELL[tocyn_safle[Dosbarth_tocyn] + 수] != ffeil_enw_SMS[수]) methiant_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < dull_COUNT && !Gwall; 현재함수++) {
            safle = dull_corff[현재함수]; dull_cod[현재함수] = cod_newid_maint; lleol_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < dull_arg_COUNT[현재함수]; 수++) ychwanegu_lleol(dull_arg_enw[현재함수 * 16 + 수], dull_arg_TYPE[현재함수 * 16 + 수]);
            boolean return_mesur = gosodiad_VALUE();
            if (!return_mesur && dull_return[현재함수] != 0) methiant_VALUE("missing return");
            // cangen 뒤의 합류 지점은 반드시 go_iawn_data 명령이어야 한다 (버전 49 검증기).
            if (dull_return[현재함수] == 0) 내보내기(177);
            else { boolean cyfanrif = dull_return[현재함수] <= 2 || dull_return[현재함수] == 5; 내보내기(cyfanrif ? 3 : 1); 내보내기(cyfanrif ? 172 : 176); }
            if (safle != dull_gorffen[현재함수]) methiant_VALUE("invalid method body");
            함수지역[현재함수] = lleol_COUNT; dull_hyd[현재함수] = cod_newid_maint - dull_cod[현재함수];
        }
        if (Gwall) return 1;
        ysgrifennu_Dosbarth(); if (Gwall) return 1;
        ffeil_enw_SMS[enw_newid_maint - 4] = 'c'; ffeil_enw_SMS[enw_newid_maint - 3] = 'l'; ffeil_enw_SMS[enw_newid_maint - 2] = 'a';
        ffeil_enw_SMS[enw_newid_maint - 1] = 's'; ffeil_enw_SMS[enw_newid_maint] = 's'; ffeil_enw_SMS[enw_newid_maint + 1] = 0;
        int mesur = defnyddiwr.ysgrifennu_ffeil(ffeil_enw_SMS, Allbwn, 출력크기);
        if (mesur < 0) { defnyddiwr.Ysgrifennu("javac: cannot save class: "); 자바도구.수쓰기(mesur); defnyddiwr.ysgrifennu_nod_VALUE(10); return 1; }
        defnyddiwr.Ysgrifennu("Compiled: "); for (int 수 = 0; ffeil_enw_SMS[수] != 0; 수++) defnyddiwr.ysgrifennu_nod_VALUE(ffeil_enw_SMS[수]);
        defnyddiwr.Ysgrifennu(" (JVM class version 49)\n"); return 0;
    }
}
