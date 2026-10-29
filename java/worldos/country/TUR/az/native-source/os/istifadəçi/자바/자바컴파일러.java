// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java mənbə_ağac -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] QAYNAQ = new int[16384], 출력 = new int[16384], kod_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], nişan_yerinə_qoymaq = new int[2048], nişan_uzunluq = new int[2048];
    static int[] sabit_VALUE = new int[4096], sabit_OFFSET = new int[512];
    static int[] 문자 = new int[512], fayl_ad_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int mənbə_ölçünü_dəyişmək, nişan_COUNT, yerinə_qoymaq, kod_ölçünü_dəyişmək, sabit_ölçünü_dəyişmək, sabit_COUNT = 1, 출력크기, simvol_uzunluq;
    static boolean XƏTA;
    static int Sinif_nişan, Sinif_sabit, 부모상수, kod_sabit;
    static int[] metod_daxiletmə_ad = new int[32], metod_geri_qaytarmaq = new int[32], metod_arqument_COUNT = new int[32];
    static int[] metod_arqument_ad = new int[512], metod_arqument_TYPE = new int[512];
    static int[] 함수본문 = new int[32], metod_bitirmək = new int[32], metod_kod = new int[32];
    static int[] metod_uzunluq = new int[32], 함수지역 = new int[32], metod_ad_sabit = new int[32], 함수서술 = new int[32];
    static int[] metod_müraciət = new int[32];
    static int metod_COUNT, 현재함수, lokal_COUNT, 깊이, 식깊이;
    static int[] lokal_ad = new int[128], lokal_TYPE = new int[128], 지역깊이 = new int[128];

    static void xəta_VALUE(String 이유) {
        if (!XƏTA) {
            istifadəçi.Yazma("javac error: "); istifadəçi.Yazma(이유);
            istifadəçi.Yazma(" at line ");
            int Giriş = 1, 끝 = yerinə_qoymaq < nişan_COUNT ? nişan_yerinə_qoymaq[yerinə_qoymaq] : mənbə_ölçünü_dəyişmək;
            for (int 수 = 0; 수 < 끝; 수++) if (QAYNAQ[수] == 10) Giriş++;
            자바도구.수쓰기(Giriş); istifadəçi.yazmaq_simvol_VALUE(10);
        }
        XƏTA = true;
    }
    static boolean simvol_VALUE_068c2631(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean rəqəm_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= nişan_COUNT || 나 >= nişan_COUNT || nişan_uzunluq[가] != nişan_uzunluq[나]) return false;
        for (int 수 = 0; 수 < nişan_uzunluq[가]; 수++) if (QAYNAQ[nişan_yerinə_qoymaq[가] + 수] != QAYNAQ[nişan_yerinə_qoymaq[나] + 수]) return false;
        return true;
    }
    static boolean Söz_VALUE(int nişan_VALUE, String Söz_SMS) {
        if (nişan_VALUE < 0 || nişan_VALUE >= nişan_COUNT || nişan_uzunluq[nişan_VALUE] != Söz_SMS.length()) return false;
        for (int 수 = 0; 수 < Söz_SMS.length(); 수++) if (QAYNAQ[nişan_yerinə_qoymaq[nişan_VALUE] + 수] != Söz_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return yerinə_qoymaq < nişan_COUNT ? 토큰종류[yerinə_qoymaq] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; yerinə_qoymaq++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) xəta_VALUE("unexpected token"); }
    static boolean TAKE_Söz(String Söz_SMS) { if (!Söz_VALUE(yerinə_qoymaq, Söz_SMS)) return false; yerinə_qoymaq++; return true; }
    static void 말요구(String Söz_SMS) { if (!TAKE_Söz(Söz_SMS)) xəta_VALUE(Söz_SMS); }
    static int identifikator_VALUE() {
        int ölçü = yerinə_qoymaq;
        if (종류() != 256) xəta_VALUE("identifier required"); else yerinə_qoymaq++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int İcra_Et = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - İcra_Et == nişan_uzunluq[ölçü];
                for (int slot_daxiletmə = İcra_Et; 같음 && slot_daxiletmə < 수; slot_daxiletmə++) if (예약어.charAt(slot_daxiletmə) != QAYNAQ[nişan_yerinə_qoymaq[ölçü] + slot_daxiletmə - İcra_Et]) 같음 = false;
                if (같음) xəta_VALUE("reserved word cannot be an identifier");
                İcra_Et = 수 + 1;
            }
        }
        return ölçü;
    }
    static void bölmək_VALUE() {
        int 수 = 0;
        while (수 < mənbə_ölçünü_dəyişmək && !XƏTA) {
            int VALUE = QAYNAQ[수], İcra_Et = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < mənbə_ölçünü_dəyişmək && QAYNAQ[수 + 1] == '/') {
                while (수 < mənbə_ölçünü_dəyişmək && QAYNAQ[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < mənbə_ölçünü_dəyişmək && QAYNAQ[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < mənbə_ölçünü_dəyişmək && !(QAYNAQ[수] == '*' && QAYNAQ[수 + 1] == '/')) 수++;
                if (수 + 1 >= mənbə_ölçünü_dəyişmək) { xəta_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (simvol_VALUE_068c2631(VALUE)) { 종류 = 256; while (수 < mənbə_ölçünü_dəyişmək && 문자이름규칙.이어진글자(QAYNAQ[수])) 수++; }
            else if (rəqəm_VALUE(VALUE)) { 종류 = 257; while (수 < mənbə_ölçünü_dəyişmək && rəqəm_VALUE(QAYNAQ[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < mənbə_ölçünü_dəyişmək && QAYNAQ[수] != VALUE && QAYNAQ[수] != 10 && QAYNAQ[수] != 13) {
                    if (QAYNAQ[수] == '\\') 수++;
                    수++;
                }
                if (수 >= mənbə_ölçünü_dəyişmək || QAYNAQ[수] != VALUE) { xəta_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < mənbə_ölçünü_dəyişmək) {
                    int Sonrakı_element = QAYNAQ[수];
                    if (VALUE == '=' && Sonrakı_element == '=') 종류 = 300;
                    if (VALUE == '!' && Sonrakı_element == '=') 종류 = 301;
                    if (VALUE == '<' && Sonrakı_element == '=') 종류 = 302;
                    if (VALUE == '>' && Sonrakı_element == '=') 종류 = 303;
                    if (VALUE == '&' && Sonrakı_element == '&') 종류 = 304;
                    if (VALUE == '|' && Sonrakı_element == '|') 종류 = 305;
                    if (VALUE == '+' && Sonrakı_element == '+') 종류 = 306;
                    if (VALUE == '-' && Sonrakı_element == '-') 종류 = 307;
                    if (VALUE == '+' && Sonrakı_element == '=') 종류 = 308;
                    if (VALUE == '-' && Sonrakı_element == '=') 종류 = 309;
                    if (VALUE == '*' && Sonrakı_element == '=') 종류 = 310;
                    if (VALUE == '/' && Sonrakı_element == '=') 종류 = 311;
                    if (VALUE == '%' && Sonrakı_element == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (nişan_COUNT == 토큰종류.length - 1) { xəta_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[nişan_COUNT] = 종류; nişan_yerinə_qoymaq[nişan_COUNT] = İcra_Et; nişan_uzunluq[nişan_COUNT++] = 수 - İcra_Et;
        }
    }
    static void yazmaq_sabit_bayt(int VALUE) {
        if (sabit_ölçünü_dəyişmək == sabit_VALUE.length) { xəta_VALUE("constant pool too large"); return; }
        sabit_VALUE[sabit_ölçünü_dəyişmək++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { yazmaq_sabit_bayt(VALUE >> 8); yazmaq_sabit_bayt(VALUE); }
    static int qeydiyyatdan_keçmək_sabit(int İcra_Et) {
        for (int 수 = 1; 수 < sabit_COUNT; 수++) {
            int ön_VALUE = sabit_OFFSET[수], uzunluq_VALUE = (수 + 1 < sabit_COUNT ? sabit_OFFSET[수 + 1] : İcra_Et) - ön_VALUE;
            if (uzunluq_VALUE != sabit_ölçünü_dəyişmək - İcra_Et) continue;
            boolean 같음 = true;
            for (int slot_daxiletmə = 0; slot_daxiletmə < uzunluq_VALUE; slot_daxiletmə++) if (sabit_VALUE[ön_VALUE + slot_daxiletmə] != sabit_VALUE[İcra_Et + slot_daxiletmə]) 같음 = false;
            if (같음) { sabit_ölçünü_dəyişmək = İcra_Et; return 수; }
        }
        if (sabit_COUNT == sabit_OFFSET.length) { xəta_VALUE("too many constants"); return 0; }
        sabit_OFFSET[sabit_COUNT] = İcra_Et;
        return sabit_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (simvol_uzunluq == 문자.length) { xəta_VALUE("text too long"); return; }
        문자[simvol_uzunluq++] = VALUE;
    }
    static void 말추가(String Söz_SMS) { for (int 수 = 0; 수 < Söz_SMS.length(); 수++) 글추가(Söz_SMS.charAt(수)); }
    static int simvol_sabit() {
        int İcra_Et = sabit_ölçünü_dəyişmək; yazmaq_sabit_bayt(1); 상짧(0);
        for (int 수 = 0; 수 < simvol_uzunluq; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) yazmaq_sabit_bayt(VALUE);
            else if (VALUE < 2048) { yazmaq_sabit_bayt(192 | VALUE >> 6); yazmaq_sabit_bayt(128 | VALUE & 63); }
            else { yazmaq_sabit_bayt(224 | VALUE >> 12); yazmaq_sabit_bayt(128 | VALUE >> 6 & 63); yazmaq_sabit_bayt(128 | VALUE & 63); }
        }
        if (XƏTA) return 0;
        int uzunluq_VALUE = sabit_ölçünü_dəyişmək - İcra_Et - 3;
        sabit_VALUE[İcra_Et + 1] = uzunluq_VALUE >> 8; sabit_VALUE[İcra_Et + 2] = uzunluq_VALUE & 255;
        return qeydiyyatdan_keçmək_sabit(İcra_Et);
    }
    static int Söz_sabit(String Söz_SMS) { simvol_uzunluq = 0; 말추가(Söz_SMS); return simvol_sabit(); }
    static int nişan_sabit(int nişan_VALUE) {
        simvol_uzunluq = 0;
        for (int 수 = 0; 수 < nişan_uzunluq[nişan_VALUE]; 수++) 글추가(QAYNAQ[nişan_yerinə_qoymaq[nişan_VALUE] + 수]);
        return simvol_sabit();
    }
    static int İstinad(int 종류, int 가, int 나) {
        int İcra_Et = sabit_ölçünü_dəyişmək; yazmaq_sabit_bayt(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return qeydiyyatdan_keçmək_sabit(İcra_Et);
    }
    static int xarici_istinad(int 종류, String sahib_VALUE, String Ad, String 서술) {
        int sahib_identifikator = İstinad(7, Söz_sabit(sahib_VALUE), 0);
        int ad_COUNT = Söz_sabit(Ad), format_COUNT = Söz_sabit(서술);
        return İstinad(종류, sahib_identifikator, İstinad(12, ad_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (kod_ölçünü_dəyişmək == kod_VALUE.length) { xəta_VALUE("bytecode too large"); return; }
        kod_VALUE[kod_ölçünü_dəyişmək++] = VALUE & 255;
    }
    static void Əmr(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int İcra_Et = sabit_ölçünü_dəyişmək; yazmaq_sabit_bayt(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Əmr(19, qeydiyyatdan_keçmək_sabit(İcra_Et));
    }
    static int qol(int Əmr) { int ölçü = kod_ölçünü_dəyişmək; Əmr(Əmr, 0); return ölçü; }
    static void keçid_VALUE(int qol, int hədəf_obyekt) {
        if (XƏTA) return;
        int 거리 = hədəf_obyekt - qol;
        if (거리 < -32768 || 거리 > 32767 || qol < 0 || qol + 2 >= kod_ölçünü_dəyişmək) { xəta_VALUE("invalid branch"); return; }
        kod_VALUE[qol + 1] = 거리 >> 8 & 255; kod_VALUE[qol + 2] = 거리 & 255;
    }
    static void Müqayisə_VALUE(int Əmr) {
        int TRUE_VALUE = qol(Əmr); 내보내기(3); int 끝 = qol(167);
        keçid_VALUE(TRUE_VALUE, kod_ölçünü_dəyişmək); 내보내기(4); keçid_VALUE(끝, kod_ölçünü_dəyişmək);
    }
    static int format_VALUE() {
        if (TAKE_Söz("void")) return 0;
        if (TAKE_Söz("int")) return 1;
        if (TAKE_Söz("boolean")) return 2;
        if (TAKE_Söz("char")) return 5;
        if (TAKE_Söz("FileInputStream")) return 6;
        if (TAKE_Söz("FileOutputStream")) return 7;
        if (TAKE_Söz("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        xəta_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void əlavə_etmək_format(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws bəyannamə. istisna Proses_VALUE_daxiletmə 본문은 host javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Söz("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Söz("Exception") || TAKE_Söz("IOException"))) return;
        if (TAKE_Söz("istisna") || TAKE_Söz("실행예외") || TAKE_Söz("giriş_çıxış_istisna") || TAKE_Söz("gözlə_FASİLƏ_istisna") || TAKE_Söz("ünvan_LOOKUP_istisna") || TAKE_Söz("파일없음예외") || TAKE_Söz("통신예외") || TAKE_Söz("yanlış_arqument_istisna") || TAKE_Söz("숫자형식예외") || TAKE_Söz("범위예외") || TAKE_Söz("배열범위예외") || TAKE_Söz("문자열범위예외") || TAKE_Söz("NULL_İstinad_istisna") || TAKE_Söz("산술예외") || TAKE_Söz("vəziyyət_istisna") || TAKE_Söz("TYPE_Yayım_istisna") || TAKE_Söz("음수배열크기예외") || TAKE_Söz("ARRAY_Store_xəta") || TAKE_Söz("axın_vəziyyət_istisna") || TAKE_Söz("대기중단예외")) return;
        xəta_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Söz("import")) {
            if (Söz_VALUE(yerinə_qoymaq, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Söz("FileInputStream") || TAKE_Söz("FileOutputStream") || TAKE_Söz("IOException"))) xəta_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Söz("public"); TAKE_Söz("final"); 말요구("class"); Sinif_nişan = identifikator_VALUE();
        Sinif_sabit = İstinad(7, nişan_sabit(Sinif_nişan), 0);
        부모상수 = İstinad(7, Söz_sabit("java/lang/Object"), 0); kod_sabit = Söz_sabit("Code"); 요구('{');
        while (!XƏTA && 종류() != '}') {
            if (metod_COUNT == 32) { xəta_VALUE("too many methods"); break; }
            int müraciət_daxiletmə = TAKE_Söz("public") ? 1 : TAKE_Söz("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = metod_COUNT++;
            metod_müraciət[FUNCTION_VALUE] = müraciət_daxiletmə | 8;
            metod_geri_qaytarmaq[FUNCTION_VALUE] = format_VALUE(); metod_daxiletmə_ad[FUNCTION_VALUE] = identifikator_VALUE(); 요구('(');
            for (int ön_VALUE = 0; ön_VALUE < FUNCTION_VALUE; ön_VALUE++) if (이름같음(metod_daxiletmə_ad[ön_VALUE], metod_daxiletmə_ad[FUNCTION_VALUE])) xəta_VALUE("duplicate method (overloading unsupported)");
            while (!XƏTA && 종류() != ')') {
                int 수 = metod_arqument_COUNT[FUNCTION_VALUE];
                if (수 == 16) { xəta_VALUE("too many parameters"); break; }
                int TYPE_VALUE = format_VALUE(); if (TYPE_VALUE == 0) xəta_VALUE("void parameter");
                metod_arqument_TYPE[FUNCTION_VALUE * 16 + 수] = TYPE_VALUE; metod_arqument_ad[FUNCTION_VALUE * 16 + 수] = identifikator_VALUE();
                metod_arqument_COUNT[FUNCTION_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Söz("throws")) {
                do { 예외이름읽기(); } while (!XƏTA && 받기(','));
            }
            함수본문[FUNCTION_VALUE] = yerinə_qoymaq; 요구('{');
            int iç_içə_yerləşdirmə_VALUE = 1;
            while (yerinə_qoymaq < nişan_COUNT && iç_içə_yerləşdirmə_VALUE > 0) {
                if (종류() == '{') iç_içə_yerləşdirmə_VALUE++;
                if (종류() == '}') iç_içə_yerləşdirmə_VALUE--;
                yerinə_qoymaq++;
            }
            if (iç_içə_yerləşdirmə_VALUE != 0) xəta_VALUE("unclosed method body");
            metod_bitirmək[FUNCTION_VALUE] = yerinə_qoymaq;
            metod_ad_sabit[FUNCTION_VALUE] = nişan_sabit(metod_daxiletmə_ad[FUNCTION_VALUE]);
            simvol_uzunluq = 0; 글추가('(');
            for (int 수 = 0; 수 < metod_arqument_COUNT[FUNCTION_VALUE]; 수++) əlavə_etmək_format(metod_arqument_TYPE[FUNCTION_VALUE * 16 + 수]);
            글추가(')'); əlavə_etmək_format(metod_geri_qaytarmaq[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = simvol_sabit();
        }
        요구('}'); if (yerinə_qoymaq != nişan_COUNT) xəta_VALUE("extra input after class");
    }
    static int FIND_lokal(int Ad) {
        for (int 수 = lokal_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokal_ad[수], Ad)) return 수;
        xəta_VALUE("unknown variable"); return 0;
    }
    static int əlavə_etmək_lokal(int Ad, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokal_ad[수], Ad)) xəta_VALUE("duplicate local variable");
        if (lokal_COUNT == 128) { xəta_VALUE("too many locals"); return 0; }
        lokal_ad[lokal_COUNT] = Ad; lokal_TYPE[lokal_COUNT] = TYPE_VALUE; 지역깊이[lokal_COUNT] = 깊이;
        return lokal_COUNT++;
    }
    static boolean tam_ədəd_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void yazmaq_lokal(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void yoxlamaq_TYPE(int faktiki_verilənlər, int 기대) { if (faktiki_verilənlər != 기대 && !(faktiki_verilənlər == 5 && 기대 == 1)) xəta_VALUE("type mismatch"); }
    static void 문자읽기(int nişan_VALUE) {
        simvol_uzunluq = 0; int İcra_Et = nişan_yerinə_qoymaq[nişan_VALUE] + 1, 끝 = nişan_yerinə_qoymaq[nişan_VALUE] + nişan_uzunluq[nişan_VALUE] - 1;
        while (İcra_Et < 끝 && !XƏTA) {
            int VALUE = QAYNAQ[İcra_Et++];
            if (VALUE == '\\') {
                if (İcra_Et == 끝) { xəta_VALUE("invalid escape"); break; }
                VALUE = QAYNAQ[İcra_Et++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') xəta_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int parselləmək_tam_ədəd(int nişan_VALUE, boolean 음수) {
        if (nişan_uzunluq[nişan_VALUE] > 1 && QAYNAQ[nişan_yerinə_qoymaq[nişan_VALUE]] == '0') xəta_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < nişan_uzunluq[nişan_VALUE]; 수++) {
            int rəqəm_element = QAYNAQ[nişan_yerinə_qoymaq[nişan_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && rəqəm_element > (음수 ? 8 : 7)) xəta_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - rəqəm_element;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Söz("new")) {
            int TYPE_VALUE = format_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { xəta_VALUE("only file streams supported by new in source"); return 0; }
            String sahib_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Əmr(187, İstinad(7, Söz_sabit(sahib_VALUE), 0)); 내보내기(89);
            요구('('); yoxlamaq_TYPE(ifadə_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) xəta_VALUE("input stream constructor arguments"); yoxlamaq_TYPE(ifadə_VALUE(), 2); 이어 = true; }
            요구(')');
            Əmr(183, xarici_istinad(10, sahib_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = ifadə_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(parselləmək_tam_ədəd(yerinə_qoymaq++, false)); return 1; }
        if (종류() == 258) { 문자읽기(yerinə_qoymaq++); Əmr(19, İstinad(8, simvol_sabit(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(yerinə_qoymaq++); if (simvol_uzunluq != 1) xəta_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Söz("true")) { 내보내기(4); return 2; }
        if (TAKE_Söz("false")) { 내보내기(3); return 2; }
        if (TAKE_Söz("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String sahib_VALUE = "", metod_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, ölçü = 0;
            if (TAKE_Söz("출력")) {
                sahib_VALUE = "한국어/자체/출력"; 요구('.');
                if (TAKE_Söz("yazmaq_xətt")) { metod_VALUE = "yazmaq_xətt"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Söz("Yazma")) { metod_VALUE = "Yazma"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Söz("수쓰기")) { metod_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else xəta_VALUE("unknown Korean output method");
            } else if (TAKE_Söz("문자")) {
                sahib_VALUE = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Söz("uzunluq_VALUE")) { metod_VALUE = "uzunluq_VALUE"; 서술 = "(Ljava/lang/String;)I"; ölçü = 1; }
                else if (TAKE_Söz("simvol_kodu_COUNT")) { metod_VALUE = "simvol_kodu_COUNT"; 서술 = "(Ljava/lang/String;)I"; ölçü = 1; }
                else if (TAKE_Söz("parselləmək_tam_ədəd")) { metod_VALUE = "parselləmək_tam_ədəd"; 서술 = "(Ljava/lang/String;)I"; ölçü = 1; }
                else if (TAKE_Söz("yazmaq_tam_ədəd_VALUE")) { metod_VALUE = "yazmaq_tam_ədəd_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; ölçü = 3; }
                else if (TAKE_Söz("같음")) { metod_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; ölçü = 2; }
                else if (TAKE_Söz("əlavə_etmək_SMS")) { metod_VALUE = "əlavə_etmək_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; ölçü = 3; }
                else if (TAKE_Söz("bölmək_VALUE")) { metod_VALUE = "bölmək_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; ölçü = 3; }
                else xəta_VALUE("unknown Korean text method");
            } else if (TAKE_Söz("FAYL")) {
                sahib_VALUE = "한국어/자체/FAYL"; 요구('.'); 가 = 3;
                if (TAKE_Söz("Oxuma")) { metod_VALUE = "Oxuma"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; ölçü = 3; }
                else if (TAKE_Söz("Yazma")) { metod_VALUE = "Yazma"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else xəta_VALUE("unknown Korean file method");
            } else if (TAKE_Söz("화면")) {
                sahib_VALUE = "한국어/자체/화면"; 요구('.');
                if (TAKE_Söz("너비")) { metod_VALUE = "너비"; 서술 = "()I"; ölçü = 1; }
                else if (TAKE_Söz("높이")) { metod_VALUE = "높이"; 서술 = "()I"; ölçü = 1; }
                else if (TAKE_Söz("사각형")) { metod_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Söz("silmək_daxiletmə_c8dbc399")) { metod_VALUE = "silmək_daxiletmə_c8dbc399"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Söz("기다리기")) { metod_VALUE = "기다리기"; 서술 = "()V"; }
                else xəta_VALUE("unknown Korean framebuffer method");
            } else xəta_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) yoxlamaq_TYPE(ifadə_VALUE(), 가);
            if (나 != 0) { 요구(','); yoxlamaq_TYPE(ifadə_VALUE(), 나); }
            if (다 != 0) { 요구(','); yoxlamaq_TYPE(ifadə_VALUE(), 다); }
            if (라 != 0) { 요구(','); yoxlamaq_TYPE(ifadə_VALUE(), 라); }
            if (마 != 0) { 요구(','); yoxlamaq_TYPE(ifadə_VALUE(), 마); }
            요구(')'); Əmr(184, xarici_istinad(10, sahib_VALUE, metod_VALUE, 서술)); return ölçü;
        }
        if (TAKE_Söz("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); yoxlamaq_TYPE(ifadə_VALUE(), 3); 요구(')');
            Əmr(184, xarici_istinad(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Ad = identifikator_VALUE();
        if (받기('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < metod_COUNT; 수++) if (이름같음(Ad, metod_daxiletmə_ad[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { xəta_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!XƏTA && 종류() != ')') {
                if (수 >= metod_arqument_COUNT[FUNCTION_VALUE]) { xəta_VALUE("too many arguments"); break; }
                yoxlamaq_TYPE(ifadə_VALUE(), metod_arqument_TYPE[FUNCTION_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != metod_arqument_COUNT[FUNCTION_VALUE]) xəta_VALUE("argument count mismatch");
            Əmr(184, İstinad(10, Sinif_sabit, İstinad(12, metod_ad_sabit[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return metod_geri_qaytarmaq[FUNCTION_VALUE];
        }
        int lokal_miqyas = FIND_lokal(Ad), TYPE_VALUE = lokal_TYPE[lokal_miqyas]; 지역읽기(lokal_miqyas);
        while (!XƏTA) {
            if (받기('[')) { yoxlamaq_TYPE(TYPE_VALUE, 4); yoxlamaq_TYPE(ifadə_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String sahib_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Söz("close")) { 요구('('); 요구(')'); Əmr(182, xarici_istinad(10, sahib_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Söz("read")) { 요구('('); 요구(')'); Əmr(182, xarici_istinad(10, sahib_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Söz("write")) { 요구('('); yoxlamaq_TYPE(ifadə_VALUE(), 1); 요구(')'); Əmr(182, xarici_istinad(10, sahib_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { xəta_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { yoxlamaq_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Əmr(182, xarici_istinad(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { xəta_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { yoxlamaq_TYPE(단항(), 2); Müqayisə_VALUE(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(parselləmək_tam_ədəd(yerinə_qoymaq++, true));
            else { yoxlamaq_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { yoxlamaq_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!XƏTA && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodlaşdırma_VALUE = 종류(); yerinə_qoymaq++; yoxlamaq_TYPE(TYPE_VALUE, 1); yoxlamaq_TYPE(단항(), 1);
            내보내기(kodlaşdırma_VALUE == '*' ? 104 : kodlaşdırma_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!XƏTA && (종류() == '+' || 종류() == '-')) {
            int kodlaşdırma_VALUE = 종류(); yerinə_qoymaq++; int 경계 = kod_ölçünü_dəyişmək, GERİ_VALUE_TYPE = 곱식();
            if (kodlaşdırma_VALUE == '+' && (TYPE_VALUE == 3 || GERİ_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, GERİ_VALUE_TYPE); TYPE_VALUE = 3; }
            else { yoxlamaq_TYPE(TYPE_VALUE, 1); yoxlamaq_TYPE(GERİ_VALUE_TYPE, 1); 내보내기(kodlaşdırma_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) xəta_VALUE("unsupported concatenation type");
        return xarici_istinad(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int ön_VALUE_TYPE, int GERİ_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT kod_VALUE 앞에 yarat 코드를 삽입한다.
        // RIGHT ifadə_VALUE 내부의 eynisəviyyəli_VALUE qol 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = kod_ölçünü_dəyişmək;
        Əmr(187, İstinad(7, Söz_sabit("java/lang/StringBuilder"), 0)); 내보내기(89);
        Əmr(183, xarici_istinad(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Əmr(182, 붙임참조(ön_VALUE_TYPE));
        if (XƏTA) return;
        int uzunluq_VALUE = kod_ölçünü_dəyişmək - 끝;
        for (int 수 = 0; 수 < uzunluq_VALUE; 수++) 삽입코드[수] = kod_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) kod_VALUE[수 + uzunluq_VALUE] = kod_VALUE[수];
        for (int 수 = 0; 수 < uzunluq_VALUE; 수++) kod_VALUE[경계 + 수] = 삽입코드[수];
        Əmr(182, 붙임참조(GERİ_VALUE_TYPE)); Əmr(182, xarici_istinad(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Müqayisə_ifadə() {
        int TYPE_VALUE = 합식();
        while (!XƏTA && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodlaşdırma_VALUE = 종류(); yerinə_qoymaq++; yoxlamaq_TYPE(TYPE_VALUE, 1); yoxlamaq_TYPE(합식(), 1);
            Müqayisə_VALUE(kodlaşdırma_VALUE == '<' ? 161 : kodlaşdırma_VALUE == '>' ? 163 : kodlaşdırma_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Müqayisə_ifadə();
        while (!XƏTA && (종류() == 300 || 종류() == 301)) {
            int kodlaşdırma_VALUE = 종류(); yerinə_qoymaq++; int GERİ_VALUE_TYPE = Müqayisə_ifadə();
            if (TYPE_VALUE == 0 || GERİ_VALUE_TYPE == 0) xəta_VALUE("void expression");
            if (!(tam_ədəd_TYPE(TYPE_VALUE) && tam_ədəd_TYPE(GERİ_VALUE_TYPE))) yoxlamaq_TYPE(GERİ_VALUE_TYPE, TYPE_VALUE);
            Müqayisə_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (kodlaşdırma_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!XƏTA && 받기(304)) {
            yoxlamaq_TYPE(TYPE_VALUE, 2); int 가 = qol(153); yoxlamaq_TYPE(동등식(), 2); int 나 = qol(153);
            내보내기(4); int 끝 = qol(167); keçid_VALUE(가, kod_ölçünü_dəyişmək); keçid_VALUE(나, kod_ölçünü_dəyişmək); 내보내기(3); keçid_VALUE(끝, kod_ölçünü_dəyişmək); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int ifadə_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!XƏTA && 받기(305)) {
            yoxlamaq_TYPE(TYPE_VALUE, 2); int 가 = qol(154); yoxlamaq_TYPE(논리곱(), 2); int 나 = qol(154);
            내보내기(3); int 끝 = qol(167); keçid_VALUE(가, kod_ölçünü_dəyişmək); keçid_VALUE(나, kod_ölçünü_dəyişmək); 내보내기(4); keçid_VALUE(끝, kod_ölçünü_dəyişmək); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void təyinat_VALUE(boolean İcazə_ver_bəyannamə) {
        if (Söz_VALUE(yerinə_qoymaq, "int") || Söz_VALUE(yerinə_qoymaq, "boolean") || Söz_VALUE(yerinə_qoymaq, "String") || Söz_VALUE(yerinə_qoymaq, "char")
            || Söz_VALUE(yerinə_qoymaq, "FileInputStream") || Söz_VALUE(yerinə_qoymaq, "FileOutputStream")) {
            if (!İcazə_ver_bəyannamə) xəta_VALUE("declaration not allowed here");
            int TYPE_VALUE = format_VALUE(), Ad = identifikator_VALUE(); 요구('='); yoxlamaq_TYPE(ifadə_VALUE(), TYPE_VALUE);
            yazmaq_lokal(əlavə_etmək_lokal(Ad, TYPE_VALUE)); return;
        }
        int Ad = identifikator_VALUE(), lokal_miqyas = FIND_lokal(Ad);
        if (받기('=')) { yoxlamaq_TYPE(ifadə_VALUE(), lokal_TYPE[lokal_miqyas]); yazmaq_lokal(lokal_miqyas); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodlaşdırma_VALUE = 종류(); yerinə_qoymaq++; 지역읽기(lokal_miqyas); int 경계 = kod_ölçünü_dəyişmək, GERİ_VALUE_TYPE = ifadə_VALUE();
            if (kodlaşdırma_VALUE == 308 && lokal_TYPE[lokal_miqyas] == 3) 결합(경계, 3, GERİ_VALUE_TYPE);
            else {
                yoxlamaq_TYPE(lokal_TYPE[lokal_miqyas], 1); yoxlamaq_TYPE(GERİ_VALUE_TYPE, 1);
                내보내기(kodlaşdırma_VALUE == 308 ? 96 : kodlaşdırma_VALUE == 309 ? 100 : kodlaşdırma_VALUE == 310 ? 104 : kodlaşdırma_VALUE == 311 ? 108 : 112);
                if (lokal_TYPE[lokal_miqyas] == 5) 내보내기(146);
            }
            yazmaq_lokal(lokal_miqyas);
        }
        else if (종류() == 306 || 종류() == 307) {
            yoxlamaq_TYPE(lokal_TYPE[lokal_miqyas], 1); 내보내기(132); 내보내기(lokal_miqyas); 내보내기(종류() == 306 ? 1 : 255); yerinə_qoymaq++;
            if (lokal_TYPE[lokal_miqyas] == 5) { 지역읽기(lokal_miqyas); 내보내기(146); yazmaq_lokal(lokal_miqyas); }
        } else xəta_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Söz("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Əmr(178, xarici_istinad(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean boş_arqument = 종류() == ')';
        int TYPE_VALUE = boş_arqument ? 0 : ifadə_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !boş_arqument)) xəta_VALUE("unsupported print argument");
        Əmr(182, xarici_istinad(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean bəyanat_VALUE() {
        if (XƏTA) return false;
        if (깊이 > 32) { xəta_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean geri_qaytarmaq_ölçü = false;
            while (!XƏTA && 종류() != '}') { if (geri_qaytarmaq_ölçü) xəta_VALUE("unreachable statement"); geri_qaytarmaq_ölçü = bəyanat_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return geri_qaytarmaq_ölçü;
        }
        if (받기(';')) return false;
        if (TAKE_Söz("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : ifadə_VALUE(); yoxlamaq_TYPE(TYPE_VALUE, metod_geri_qaytarmaq[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Söz("if")) {
            요구('('); yoxlamaq_TYPE(ifadə_VALUE(), 2); 요구(')'); int FALSE_VALUE = qol(153);
            깊이++; boolean 가 = nəzarət_bəyanat(); 깊이--;
            if (TAKE_Söz("else")) { int 끝 = qol(167); keçid_VALUE(FALSE_VALUE, kod_ölçünü_dəyişmək); 깊이++; boolean 나 = nəzarət_bəyanat(); 깊이--; keçid_VALUE(끝, kod_ölçünü_dəyişmək); return 가 && 나; }
            keçid_VALUE(FALSE_VALUE, kod_ölçünü_dəyişmək); return false;
        }
        if (TAKE_Söz("while")) {
            int İcra_Et = kod_ölçünü_dəyişmək; 요구('('); yoxlamaq_TYPE(ifadə_VALUE(), 2); 요구(')'); int 끝 = qol(153);
            깊이++; nəzarət_bəyanat(); 깊이--; keçid_VALUE(qol(167), İcra_Et); keçid_VALUE(끝, kod_ölçünü_dəyişmək); return false;
        }
        if (TAKE_Söz("for")) {
            깊이++; 요구('('); if (종류() != ';') təyinat_VALUE(true); 요구(';');
            int şərt = kod_ölçünü_dəyişmək; if (종류() == ';') 내보내기(4); else yoxlamaq_TYPE(ifadə_VALUE(), 2); 요구(';');
            int 끝 = qol(153), əsas_mətn = qol(167), təzələmək = kod_ölçünü_dəyişmək;
            if (종류() != ')') təyinat_VALUE(false); 요구(')'); keçid_VALUE(qol(167), şərt); keçid_VALUE(əsas_mətn, kod_ölçünü_dəyişmək);
            nəzarət_bəyanat(); keçid_VALUE(qol(167), təzələmək); keçid_VALUE(끝, kod_ölçünü_dəyişmək);
            for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Söz_VALUE(yerinə_qoymaq, "System")) { 화면출력(); return false; }
        if (종류() == 256 && yerinə_qoymaq + 1 < nişan_COUNT && (토큰종류[yerinə_qoymaq + 1] == '(' || 토큰종류[yerinə_qoymaq + 1] == '.')) {
            int TYPE_VALUE = ifadə_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        təyinat_VALUE(true); 요구(';'); return false;
    }
    static boolean nəzarət_bəyanat() {
        if (Söz_VALUE(yerinə_qoymaq, "int") || Söz_VALUE(yerinə_qoymaq, "boolean") || Söz_VALUE(yerinə_qoymaq, "char") || Söz_VALUE(yerinə_qoymaq, "String")
            || Söz_VALUE(yerinə_qoymaq, "FileInputStream") || Söz_VALUE(yerinə_qoymaq, "FileOutputStream")) xəta_VALUE("local declaration requires braces");
        return bəyanat_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) xəta_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void yazmaq_Sinif() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(sabit_COUNT);
        for (int 수 = 0; 수 < sabit_ölçünü_dəyişmək; 수++) 출바(sabit_VALUE[수]);
        출짧(0x21); 출짧(Sinif_sabit); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(metod_COUNT);
        for (int 수 = 0; 수 < metod_COUNT; 수++) {
            출짧(metod_müraciət[수]); 출짧(metod_ad_sabit[수]); 출짧(함수서술[수]); 출짧(1); 출짧(kod_sabit);
            출정(12 + metod_uzunluq[수]); 출짧(128); 출짧(함수지역[수]); 출정(metod_uzunluq[수]);
            for (int slot_daxiletmə = 0; slot_daxiletmə < metod_uzunluq[수]; slot_daxiletmə++) 출바(kod_VALUE[metod_kod[수] + slot_daxiletmə]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int İcra_Et() {
        if (istifadəçi.인수개수() == 1 && 자바도구.같음(istifadəçi.인수(0), "-version")) {
            istifadəçi.Yazma("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (istifadəçi.인수개수() != 1) { istifadəçi.Yazma("Usage: javac FILE.java\n"); return 2; }
        int ad_ölçünü_dəyişmək = 자바도구.Ad(fayl_ad_SMS, istifadəçi.인수(0));
        if (ad_ölçünü_dəyişmək < 6 || ad_ölçünü_dəyişmək > 62 || fayl_ad_SMS[ad_ölçünü_dəyişmək - 5] != '.' || fayl_ad_SMS[ad_ölçünü_dəyişmək - 4] != 'j'
            || fayl_ad_SMS[ad_ölçünü_dəyişmək - 3] != 'a' || fayl_ad_SMS[ad_ölçünü_dəyişmək - 2] != 'v' || fayl_ad_SMS[ad_ölçünü_dəyişmək - 1] != 'a') {
            istifadəçi.Yazma("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        mənbə_ölçünü_dəyişmək = istifadəçi.파일읽기(fayl_ad_SMS, QAYNAQ);
        if (mənbə_ölçünü_dəyişmək < 0) { istifadəçi.Yazma("javac: cannot read source: "); 자바도구.수쓰기(mənbə_ölçünü_dəyişmək); istifadəçi.yazmaq_simvol_VALUE(10); return 1; }
        mənbə_ölçünü_dəyişmək = 자바도구.원문해독(QAYNAQ, mənbə_ölçünü_dəyişmək);
        if (mənbə_ölçünü_dəyişmək < 0) { istifadəçi.Yazma("javac error: invalid UTF-8 source\n"); return 1; }
        bölmək_VALUE(); if (!XƏTA) 선언읽기();
        if (!XƏTA) {
            if (nişan_uzunluq[Sinif_nişan] != ad_ölçünü_dəyişmək - 5) xəta_VALUE("class name must match file name");
            for (int 수 = 0; 수 < ad_ölçünü_dəyişmək - 5; 수++) if (QAYNAQ[nişan_yerinə_qoymaq[Sinif_nişan] + 수] != fayl_ad_SMS[수]) xəta_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < metod_COUNT && !XƏTA; 현재함수++) {
            yerinə_qoymaq = 함수본문[현재함수]; metod_kod[현재함수] = kod_ölçünü_dəyişmək; lokal_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metod_arqument_COUNT[현재함수]; 수++) əlavə_etmək_lokal(metod_arqument_ad[현재함수 * 16 + 수], metod_arqument_TYPE[현재함수 * 16 + 수]);
            boolean geri_qaytarmaq_ölçü = bəyanat_VALUE();
            if (!geri_qaytarmaq_ölçü && metod_geri_qaytarmaq[현재함수] != 0) xəta_VALUE("missing return");
            // qol 뒤의 합류 지점은 반드시 faktiki_verilənlər 명령이어야 한다 (버전 49 검증기).
            if (metod_geri_qaytarmaq[현재함수] == 0) 내보내기(177);
            else { boolean tam_ədəd = metod_geri_qaytarmaq[현재함수] <= 2 || metod_geri_qaytarmaq[현재함수] == 5; 내보내기(tam_ədəd ? 3 : 1); 내보내기(tam_ədəd ? 172 : 176); }
            if (yerinə_qoymaq != metod_bitirmək[현재함수]) xəta_VALUE("invalid method body");
            함수지역[현재함수] = lokal_COUNT; metod_uzunluq[현재함수] = kod_ölçünü_dəyişmək - metod_kod[현재함수];
        }
        if (XƏTA) return 1;
        yazmaq_Sinif(); if (XƏTA) return 1;
        fayl_ad_SMS[ad_ölçünü_dəyişmək - 4] = 'c'; fayl_ad_SMS[ad_ölçünü_dəyişmək - 3] = 'l'; fayl_ad_SMS[ad_ölçünü_dəyişmək - 2] = 'a';
        fayl_ad_SMS[ad_ölçünü_dəyişmək - 1] = 's'; fayl_ad_SMS[ad_ölçünü_dəyişmək] = 's'; fayl_ad_SMS[ad_ölçünü_dəyişmək + 1] = 0;
        int ölçü = istifadəçi.yazmaq_fayl(fayl_ad_SMS, 출력, 출력크기);
        if (ölçü < 0) { istifadəçi.Yazma("javac: cannot save class: "); 자바도구.수쓰기(ölçü); istifadəçi.yazmaq_simvol_VALUE(10); return 1; }
        istifadəçi.Yazma("Compiled: "); for (int 수 = 0; fayl_ad_SMS[수] != 0; 수++) istifadəçi.yazmaq_simvol_VALUE(fayl_ad_SMS[수]);
        istifadəçi.Yazma(" (JVM class version 49)\n"); return 0;
    }
}
