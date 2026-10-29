// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java tùs_craobh -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] tùs = new int[16384], 출력 = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], tòcan_suidhich = new int[2048], tòcan_faid = new int[2048];
    static int[] cunbhalachan_VALUE = new int[4096], cunbhalachan_OFFSET = new int[512];
    static int[] 문자 = new int[512], faidhle_ainm_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int tùs_atharraich_am_meud, tòcan_COUNT, suidhich, CODE_atharraich_am_meud, cunbhalachan_atharraich_am_meud, cunbhalachan_COUNT = 1, 출력크기, caractar_faid;
    static boolean Mearachd;
    static int clas_tòcan, clas_cunbhalachan, 부모상수, CODE_cunbhalachan;
    static int[] dòigh_cur_a_steach_ainm = new int[32], dòigh_return = new int[32], dòigh_argamaid_COUNT = new int[32];
    static int[] dòigh_argamaid_ainm = new int[512], dòigh_argamaid_TYPE = new int[512];
    static int[] 함수본문 = new int[32], dòigh_crìochnaich = new int[32], dòigh_CODE = new int[32];
    static int[] dòigh_faid = new int[32], 함수지역 = new int[32], dòigh_ainm_cunbhalachan = new int[32], 함수서술 = new int[32];
    static int[] dòigh_inntrigeadh = new int[32];
    static int dòigh_COUNT, 현재함수, ionadail_COUNT, 깊이, 식깊이;
    static int[] ionadail_ainm = new int[128], ionadail_TYPE = new int[128], 지역깊이 = new int[128];

    static void fàilligeadh_VALUE(String 이유) {
        if (!Mearachd) {
            cleachdaiche.sgrìobh("javac error: "); cleachdaiche.sgrìobh(이유);
            cleachdaiche.sgrìobh(" at line ");
            int loidhne = 1, 끝 = suidhich < tòcan_COUNT ? tòcan_suidhich[suidhich] : tùs_atharraich_am_meud;
            for (int 수 = 0; 수 < 끝; 수++) if (tùs[수] == 10) loidhne++;
            자바도구.수쓰기(loidhne); cleachdaiche.sgrìobh_caractar_VALUE(10);
        }
        Mearachd = true;
    }
    static boolean caractar_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean figear_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= tòcan_COUNT || 나 >= tòcan_COUNT || tòcan_faid[가] != tòcan_faid[나]) return false;
        for (int 수 = 0; 수 < tòcan_faid[가]; 수++) if (tùs[tòcan_suidhich[가] + 수] != tùs[tòcan_suidhich[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int tòcan_VALUE, String Word_SMS) {
        if (tòcan_VALUE < 0 || tòcan_VALUE >= tòcan_COUNT || tòcan_faid[tòcan_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (tùs[tòcan_suidhich[tòcan_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return suidhich < tòcan_COUNT ? 토큰종류[suidhich] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; suidhich++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) fàilligeadh_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(suidhich, Word_SMS)) return false; suidhich++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) fàilligeadh_VALUE(Word_SMS); }
    static int aithnichear_VALUE() {
        int tomhas = suidhich;
        if (종류() != 256) fàilligeadh_VALUE("identifier required"); else suidhich++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int ruith = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - ruith == tòcan_faid[tomhas];
                for (int slot_cur_a_steach = ruith; 같음 && slot_cur_a_steach < 수; slot_cur_a_steach++) if (예약어.charAt(slot_cur_a_steach) != tùs[tòcan_suidhich[tomhas] + slot_cur_a_steach - ruith]) 같음 = false;
                if (같음) fàilligeadh_VALUE("reserved word cannot be an identifier");
                ruith = 수 + 1;
            }
        }
        return tomhas;
    }
    static void gearr_VALUE() {
        int 수 = 0;
        while (수 < tùs_atharraich_am_meud && !Mearachd) {
            int VALUE = tùs[수], ruith = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < tùs_atharraich_am_meud && tùs[수 + 1] == '/') {
                while (수 < tùs_atharraich_am_meud && tùs[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < tùs_atharraich_am_meud && tùs[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < tùs_atharraich_am_meud && !(tùs[수] == '*' && tùs[수 + 1] == '/')) 수++;
                if (수 + 1 >= tùs_atharraich_am_meud) { fàilligeadh_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (caractar_VALUE(VALUE)) { 종류 = 256; while (수 < tùs_atharraich_am_meud && 문자이름규칙.이어진글자(tùs[수])) 수++; }
            else if (figear_VALUE(VALUE)) { 종류 = 257; while (수 < tùs_atharraich_am_meud && figear_VALUE(tùs[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < tùs_atharraich_am_meud && tùs[수] != VALUE && tùs[수] != 10 && tùs[수] != 13) {
                    if (tùs[수] == '\\') 수++;
                    수++;
                }
                if (수 >= tùs_atharraich_am_meud || tùs[수] != VALUE) { fàilligeadh_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < tùs_atharraich_am_meud) {
                    int air_adhart_nì = tùs[수];
                    if (VALUE == '=' && air_adhart_nì == '=') 종류 = 300;
                    if (VALUE == '!' && air_adhart_nì == '=') 종류 = 301;
                    if (VALUE == '<' && air_adhart_nì == '=') 종류 = 302;
                    if (VALUE == '>' && air_adhart_nì == '=') 종류 = 303;
                    if (VALUE == '&' && air_adhart_nì == '&') 종류 = 304;
                    if (VALUE == '|' && air_adhart_nì == '|') 종류 = 305;
                    if (VALUE == '+' && air_adhart_nì == '+') 종류 = 306;
                    if (VALUE == '-' && air_adhart_nì == '-') 종류 = 307;
                    if (VALUE == '+' && air_adhart_nì == '=') 종류 = 308;
                    if (VALUE == '-' && air_adhart_nì == '=') 종류 = 309;
                    if (VALUE == '*' && air_adhart_nì == '=') 종류 = 310;
                    if (VALUE == '/' && air_adhart_nì == '=') 종류 = 311;
                    if (VALUE == '%' && air_adhart_nì == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (tòcan_COUNT == 토큰종류.length - 1) { fàilligeadh_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[tòcan_COUNT] = 종류; tòcan_suidhich[tòcan_COUNT] = ruith; tòcan_faid[tòcan_COUNT++] = 수 - ruith;
        }
    }
    static void sgrìobh_cunbhalachan_baidht(int VALUE) {
        if (cunbhalachan_atharraich_am_meud == cunbhalachan_VALUE.length) { fàilligeadh_VALUE("constant pool too large"); return; }
        cunbhalachan_VALUE[cunbhalachan_atharraich_am_meud++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { sgrìobh_cunbhalachan_baidht(VALUE >> 8); sgrìobh_cunbhalachan_baidht(VALUE); }
    static int clàraich_cunbhalachan(int ruith) {
        for (int 수 = 1; 수 < cunbhalachan_COUNT; 수++) {
            int 앞 = cunbhalachan_OFFSET[수], faid_VALUE = (수 + 1 < cunbhalachan_COUNT ? cunbhalachan_OFFSET[수 + 1] : ruith) - 앞;
            if (faid_VALUE != cunbhalachan_atharraich_am_meud - ruith) continue;
            boolean 같음 = true;
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < faid_VALUE; slot_cur_a_steach++) if (cunbhalachan_VALUE[앞 + slot_cur_a_steach] != cunbhalachan_VALUE[ruith + slot_cur_a_steach]) 같음 = false;
            if (같음) { cunbhalachan_atharraich_am_meud = ruith; return 수; }
        }
        if (cunbhalachan_COUNT == cunbhalachan_OFFSET.length) { fàilligeadh_VALUE("too many constants"); return 0; }
        cunbhalachan_OFFSET[cunbhalachan_COUNT] = ruith;
        return cunbhalachan_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (caractar_faid == 문자.length) { fàilligeadh_VALUE("text too long"); return; }
        문자[caractar_faid++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int caractar_cunbhalachan() {
        int ruith = cunbhalachan_atharraich_am_meud; sgrìobh_cunbhalachan_baidht(1); 상짧(0);
        for (int 수 = 0; 수 < caractar_faid; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) sgrìobh_cunbhalachan_baidht(VALUE);
            else if (VALUE < 2048) { sgrìobh_cunbhalachan_baidht(192 | VALUE >> 6); sgrìobh_cunbhalachan_baidht(128 | VALUE & 63); }
            else { sgrìobh_cunbhalachan_baidht(224 | VALUE >> 12); sgrìobh_cunbhalachan_baidht(128 | VALUE >> 6 & 63); sgrìobh_cunbhalachan_baidht(128 | VALUE & 63); }
        }
        if (Mearachd) return 0;
        int faid_VALUE = cunbhalachan_atharraich_am_meud - ruith - 3;
        cunbhalachan_VALUE[ruith + 1] = faid_VALUE >> 8; cunbhalachan_VALUE[ruith + 2] = faid_VALUE & 255;
        return clàraich_cunbhalachan(ruith);
    }
    static int Word_cunbhalachan(String Word_SMS) { caractar_faid = 0; 말추가(Word_SMS); return caractar_cunbhalachan(); }
    static int tòcan_cunbhalachan(int tòcan_VALUE) {
        caractar_faid = 0;
        for (int 수 = 0; 수 < tòcan_faid[tòcan_VALUE]; 수++) 글추가(tùs[tòcan_suidhich[tòcan_VALUE] + 수]);
        return caractar_cunbhalachan();
    }
    static int fiosrachadh(int 종류, int 가, int 나) {
        int ruith = cunbhalachan_atharraich_am_meud; sgrìobh_cunbhalachan_baidht(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return clàraich_cunbhalachan(ruith);
    }
    static int 외부참조(int 종류, String sealbhadair_VALUE, String Ainm, String 서술) {
        int sealbhadair_aithnichear = fiosrachadh(7, Word_cunbhalachan(sealbhadair_VALUE), 0);
        int ainm_COUNT = Word_cunbhalachan(Ainm), fòrmat_COUNT = Word_cunbhalachan(서술);
        return fiosrachadh(종류, sealbhadair_aithnichear, fiosrachadh(12, ainm_COUNT, fòrmat_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_atharraich_am_meud == CODE_VALUE.length) { fàilligeadh_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_atharraich_am_meud++] = VALUE & 255;
    }
    static void àithne(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int ruith = cunbhalachan_atharraich_am_meud; sgrìobh_cunbhalachan_baidht(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        àithne(19, clàraich_cunbhalachan(ruith));
    }
    static int meur(int àithne) { int tomhas = CODE_atharraich_am_meud; àithne(àithne, 0); return tomhas; }
    static void ceangal_VALUE(int meur, int targaid_nì) {
        if (Mearachd) return;
        int 거리 = targaid_nì - meur;
        if (거리 < -32768 || 거리 > 32767 || meur < 0 || meur + 2 >= CODE_atharraich_am_meud) { fàilligeadh_VALUE("invalid branch"); return; }
        CODE_VALUE[meur + 1] = 거리 >> 8 & 255; CODE_VALUE[meur + 2] = 거리 & 255;
    }
    static void 비교값(int àithne) {
        int TRUE_VALUE = meur(àithne); 내보내기(3); int 끝 = meur(167);
        ceangal_VALUE(TRUE_VALUE, CODE_atharraich_am_meud); 내보내기(4); ceangal_VALUE(끝, CODE_atharraich_am_meud);
    }
    static int fòrmat_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        fàilligeadh_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void cuir_ris_fòrmat(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Pròiseas_VALUE_cur_a_steach 본문은 òstair javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("예외") || TAKE_Word("실행예외") || TAKE_Word("입출력예외") || TAKE_Word("대기시간초과예외") || TAKE_Word("주소확인예외") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("잘못된인수예외") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("빈참조예외") || TAKE_Word("산술예외") || TAKE_Word("상태예외") || TAKE_Word("형변환예외") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_fàilligeadh") || TAKE_Word("가닥상태예외") || TAKE_Word("대기중단예외")) return;
        fàilligeadh_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(suidhich, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) fàilligeadh_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); clas_tòcan = aithnichear_VALUE();
        clas_cunbhalachan = fiosrachadh(7, tòcan_cunbhalachan(clas_tòcan), 0);
        부모상수 = fiosrachadh(7, Word_cunbhalachan("java/lang/Object"), 0); CODE_cunbhalachan = Word_cunbhalachan("Code"); 요구('{');
        while (!Mearachd && 종류() != '}') {
            if (dòigh_COUNT == 32) { fàilligeadh_VALUE("too many methods"); break; }
            int inntrigeadh_cur_a_steach = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = dòigh_COUNT++;
            dòigh_inntrigeadh[FUNCTION_VALUE] = inntrigeadh_cur_a_steach | 8;
            dòigh_return[FUNCTION_VALUE] = fòrmat_VALUE(); dòigh_cur_a_steach_ainm[FUNCTION_VALUE] = aithnichear_VALUE(); 요구('(');
            for (int 앞 = 0; 앞 < FUNCTION_VALUE; 앞++) if (이름같음(dòigh_cur_a_steach_ainm[앞], dòigh_cur_a_steach_ainm[FUNCTION_VALUE])) fàilligeadh_VALUE("duplicate method (overloading unsupported)");
            while (!Mearachd && 종류() != ')') {
                int 수 = dòigh_argamaid_COUNT[FUNCTION_VALUE];
                if (수 == 16) { fàilligeadh_VALUE("too many parameters"); break; }
                int TYPE_VALUE = fòrmat_VALUE(); if (TYPE_VALUE == 0) fàilligeadh_VALUE("void parameter");
                dòigh_argamaid_TYPE[FUNCTION_VALUE * 16 + 수] = TYPE_VALUE; dòigh_argamaid_ainm[FUNCTION_VALUE * 16 + 수] = aithnichear_VALUE();
                dòigh_argamaid_COUNT[FUNCTION_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!Mearachd && 받기(','));
            }
            함수본문[FUNCTION_VALUE] = suidhich; 요구('{');
            int 중첩 = 1;
            while (suidhich < tòcan_COUNT && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                suidhich++;
            }
            if (중첩 != 0) fàilligeadh_VALUE("unclosed method body");
            dòigh_crìochnaich[FUNCTION_VALUE] = suidhich;
            dòigh_ainm_cunbhalachan[FUNCTION_VALUE] = tòcan_cunbhalachan(dòigh_cur_a_steach_ainm[FUNCTION_VALUE]);
            caractar_faid = 0; 글추가('(');
            for (int 수 = 0; 수 < dòigh_argamaid_COUNT[FUNCTION_VALUE]; 수++) cuir_ris_fòrmat(dòigh_argamaid_TYPE[FUNCTION_VALUE * 16 + 수]);
            글추가(')'); cuir_ris_fòrmat(dòigh_return[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = caractar_cunbhalachan();
        }
        요구('}'); if (suidhich != tòcan_COUNT) fàilligeadh_VALUE("extra input after class");
    }
    static int FIND_ionadail(int Ainm) {
        for (int 수 = ionadail_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(ionadail_ainm[수], Ainm)) return 수;
        fàilligeadh_VALUE("unknown variable"); return 0;
    }
    static int cuir_ris_ionadail(int Ainm, int TYPE_VALUE) {
        for (int 수 = 0; 수 < ionadail_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(ionadail_ainm[수], Ainm)) fàilligeadh_VALUE("duplicate local variable");
        if (ionadail_COUNT == 128) { fàilligeadh_VALUE("too many locals"); return 0; }
        ionadail_ainm[ionadail_COUNT] = Ainm; ionadail_TYPE[ionadail_COUNT] = TYPE_VALUE; 지역깊이[ionadail_COUNT] = 깊이;
        return ionadail_COUNT++;
    }
    static boolean àireamh_shlàn_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(ionadail_TYPE[수] <= 2 || ionadail_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void sgrìobh_ionadail(int 수) { 내보내기(ionadail_TYPE[수] <= 2 || ionadail_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void dearbh_TYPE(int dearbh_dàta, int 기대) { if (dearbh_dàta != 기대 && !(dearbh_dàta == 5 && 기대 == 1)) fàilligeadh_VALUE("type mismatch"); }
    static void 문자읽기(int tòcan_VALUE) {
        caractar_faid = 0; int ruith = tòcan_suidhich[tòcan_VALUE] + 1, 끝 = tòcan_suidhich[tòcan_VALUE] + tòcan_faid[tòcan_VALUE] - 1;
        while (ruith < 끝 && !Mearachd) {
            int VALUE = tùs[ruith++];
            if (VALUE == '\\') {
                if (ruith == 끝) { fàilligeadh_VALUE("invalid escape"); break; }
                VALUE = tùs[ruith++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') fàilligeadh_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int 정수읽기(int tòcan_VALUE, boolean 음수) {
        if (tòcan_faid[tòcan_VALUE] > 1 && tùs[tòcan_suidhich[tòcan_VALUE]] == '0') fàilligeadh_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < tòcan_faid[tòcan_VALUE]; 수++) {
            int figear_nì = tùs[tòcan_suidhich[tòcan_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && figear_nì > (음수 ? 8 : 7)) fàilligeadh_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - figear_nì;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = fòrmat_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { fàilligeadh_VALUE("only file streams supported by new in source"); return 0; }
            String sealbhadair_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            àithne(187, fiosrachadh(7, Word_cunbhalachan(sealbhadair_VALUE), 0)); 내보내기(89);
            요구('('); dearbh_TYPE(eas_preisean_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) fàilligeadh_VALUE("input stream constructor arguments"); dearbh_TYPE(eas_preisean_VALUE(), 2); 이어 = true; }
            요구(')');
            àithne(183, 외부참조(10, sealbhadair_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = eas_preisean_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(정수읽기(suidhich++, false)); return 1; }
        if (종류() == 258) { 문자읽기(suidhich++); àithne(19, fiosrachadh(8, caractar_cunbhalachan(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(suidhich++); if (caractar_faid != 1) fàilligeadh_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String sealbhadair_VALUE = "", dòigh_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, tomhas = 0;
            if (TAKE_Word("출력")) {
                sealbhadair_VALUE = "한국어/자체/출력"; 요구('.');
                if (TAKE_Word("sgrìobh_loidhne")) { dòigh_VALUE = "sgrìobh_loidhne"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("sgrìobh")) { dòigh_VALUE = "sgrìobh"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { dòigh_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else fàilligeadh_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                sealbhadair_VALUE = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("faid_VALUE")) { dòigh_VALUE = "faid_VALUE"; 서술 = "(Ljava/lang/String;)I"; tomhas = 1; }
                else if (TAKE_Word("còd_a_charactair_COUNT")) { dòigh_VALUE = "còd_a_charactair_COUNT"; 서술 = "(Ljava/lang/String;)I"; tomhas = 1; }
                else if (TAKE_Word("정수읽기")) { dòigh_VALUE = "정수읽기"; 서술 = "(Ljava/lang/String;)I"; tomhas = 1; }
                else if (TAKE_Word("sgrìobh_àireamh_shlàn_VALUE")) { dòigh_VALUE = "sgrìobh_àireamh_shlàn_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; tomhas = 3; }
                else if (TAKE_Word("같음")) { dòigh_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; tomhas = 2; }
                else if (TAKE_Word("cuir_ann_SMS")) { dòigh_VALUE = "cuir_ann_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; tomhas = 3; }
                else if (TAKE_Word("gearr_VALUE")) { dòigh_VALUE = "gearr_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; tomhas = 3; }
                else fàilligeadh_VALUE("unknown Korean text method");
            } else if (TAKE_Word("faidhle")) {
                sealbhadair_VALUE = "한국어/자체/faidhle"; 요구('.'); 가 = 3;
                if (TAKE_Word("읽기")) { dòigh_VALUE = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; tomhas = 3; }
                else if (TAKE_Word("sgrìobh")) { dòigh_VALUE = "sgrìobh"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else fàilligeadh_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                sealbhadair_VALUE = "한국어/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { dòigh_VALUE = "너비"; 서술 = "()I"; tomhas = 1; }
                else if (TAKE_Word("높이")) { dòigh_VALUE = "높이"; 서술 = "()I"; tomhas = 1; }
                else if (TAKE_Word("사각형")) { dòigh_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("지우기")) { dòigh_VALUE = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { dòigh_VALUE = "기다리기"; 서술 = "()V"; }
                else fàilligeadh_VALUE("unknown Korean framebuffer method");
            } else fàilligeadh_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) dearbh_TYPE(eas_preisean_VALUE(), 가);
            if (나 != 0) { 요구(','); dearbh_TYPE(eas_preisean_VALUE(), 나); }
            if (다 != 0) { 요구(','); dearbh_TYPE(eas_preisean_VALUE(), 다); }
            if (라 != 0) { 요구(','); dearbh_TYPE(eas_preisean_VALUE(), 라); }
            if (마 != 0) { 요구(','); dearbh_TYPE(eas_preisean_VALUE(), 마); }
            요구(')'); àithne(184, 외부참조(10, sealbhadair_VALUE, dòigh_VALUE, 서술)); return tomhas;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); dearbh_TYPE(eas_preisean_VALUE(), 3); 요구(')');
            àithne(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Ainm = aithnichear_VALUE();
        if (받기('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < dòigh_COUNT; 수++) if (이름같음(Ainm, dòigh_cur_a_steach_ainm[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { fàilligeadh_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!Mearachd && 종류() != ')') {
                if (수 >= dòigh_argamaid_COUNT[FUNCTION_VALUE]) { fàilligeadh_VALUE("too many arguments"); break; }
                dearbh_TYPE(eas_preisean_VALUE(), dòigh_argamaid_TYPE[FUNCTION_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != dòigh_argamaid_COUNT[FUNCTION_VALUE]) fàilligeadh_VALUE("argument count mismatch");
            àithne(184, fiosrachadh(10, clas_cunbhalachan, fiosrachadh(12, dòigh_ainm_cunbhalachan[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return dòigh_return[FUNCTION_VALUE];
        }
        int ionadail_sgòp = FIND_ionadail(Ainm), TYPE_VALUE = ionadail_TYPE[ionadail_sgòp]; 지역읽기(ionadail_sgòp);
        while (!Mearachd) {
            if (받기('[')) { dearbh_TYPE(TYPE_VALUE, 4); dearbh_TYPE(eas_preisean_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String sealbhadair_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); àithne(182, 외부참조(10, sealbhadair_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); àithne(182, 외부참조(10, sealbhadair_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); dearbh_TYPE(eas_preisean_VALUE(), 1); 요구(')'); àithne(182, 외부참조(10, sealbhadair_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { fàilligeadh_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { dearbh_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); àithne(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { fàilligeadh_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { dearbh_TYPE(단항(), 2); 비교값(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(정수읽기(suidhich++, true));
            else { dearbh_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { dearbh_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!Mearachd && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int còdachadh_VALUE = 종류(); suidhich++; dearbh_TYPE(TYPE_VALUE, 1); dearbh_TYPE(단항(), 1);
            내보내기(còdachadh_VALUE == '*' ? 104 : còdachadh_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!Mearachd && (종류() == '+' || 종류() == '-')) {
            int còdachadh_VALUE = 종류(); suidhich++; int 경계 = CODE_atharraich_am_meud, Air_ais_VALUE_TYPE = 곱식();
            if (còdachadh_VALUE == '+' && (TYPE_VALUE == 3 || Air_ais_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, Air_ais_VALUE_TYPE); TYPE_VALUE = 3; }
            else { dearbh_TYPE(TYPE_VALUE, 1); dearbh_TYPE(Air_ais_VALUE_TYPE, 1); 내보내기(còdachadh_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) fàilligeadh_VALUE("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Air_ais_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 gin 코드를 삽입한다.
        // RIGHT eas_preisean_VALUE 내부의 seise_VALUE meur 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_atharraich_am_meud;
        àithne(187, fiosrachadh(7, Word_cunbhalachan("java/lang/StringBuilder"), 0)); 내보내기(89);
        àithne(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); àithne(182, 붙임참조(앞형));
        if (Mearachd) return;
        int faid_VALUE = CODE_atharraich_am_meud - 끝;
        for (int 수 = 0; 수 < faid_VALUE; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + faid_VALUE] = CODE_VALUE[수];
        for (int 수 = 0; 수 < faid_VALUE; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        àithne(182, 붙임참조(Air_ais_VALUE_TYPE)); àithne(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int TYPE_VALUE = 합식();
        while (!Mearachd && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int còdachadh_VALUE = 종류(); suidhich++; dearbh_TYPE(TYPE_VALUE, 1); dearbh_TYPE(합식(), 1);
            비교값(còdachadh_VALUE == '<' ? 161 : còdachadh_VALUE == '>' ? 163 : còdachadh_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = 비교식();
        while (!Mearachd && (종류() == 300 || 종류() == 301)) {
            int còdachadh_VALUE = 종류(); suidhich++; int Air_ais_VALUE_TYPE = 비교식();
            if (TYPE_VALUE == 0 || Air_ais_VALUE_TYPE == 0) fàilligeadh_VALUE("void expression");
            if (!(àireamh_shlàn_TYPE(TYPE_VALUE) && àireamh_shlàn_TYPE(Air_ais_VALUE_TYPE))) dearbh_TYPE(Air_ais_VALUE_TYPE, TYPE_VALUE);
            비교값((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (còdachadh_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!Mearachd && 받기(304)) {
            dearbh_TYPE(TYPE_VALUE, 2); int 가 = meur(153); dearbh_TYPE(동등식(), 2); int 나 = meur(153);
            내보내기(4); int 끝 = meur(167); ceangal_VALUE(가, CODE_atharraich_am_meud); ceangal_VALUE(나, CODE_atharraich_am_meud); 내보내기(3); ceangal_VALUE(끝, CODE_atharraich_am_meud); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int eas_preisean_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!Mearachd && 받기(305)) {
            dearbh_TYPE(TYPE_VALUE, 2); int 가 = meur(154); dearbh_TYPE(논리곱(), 2); int 나 = meur(154);
            내보내기(3); int 끝 = meur(167); ceangal_VALUE(가, CODE_atharraich_am_meud); ceangal_VALUE(나, CODE_atharraich_am_meud); 내보내기(4); ceangal_VALUE(끝, CODE_atharraich_am_meud); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void obair_sgoile_VALUE(boolean 선언허용) {
        if (Word_VALUE(suidhich, "int") || Word_VALUE(suidhich, "boolean") || Word_VALUE(suidhich, "String") || Word_VALUE(suidhich, "char")
            || Word_VALUE(suidhich, "FileInputStream") || Word_VALUE(suidhich, "FileOutputStream")) {
            if (!선언허용) fàilligeadh_VALUE("declaration not allowed here");
            int TYPE_VALUE = fòrmat_VALUE(), Ainm = aithnichear_VALUE(); 요구('='); dearbh_TYPE(eas_preisean_VALUE(), TYPE_VALUE);
            sgrìobh_ionadail(cuir_ris_ionadail(Ainm, TYPE_VALUE)); return;
        }
        int Ainm = aithnichear_VALUE(), ionadail_sgòp = FIND_ionadail(Ainm);
        if (받기('=')) { dearbh_TYPE(eas_preisean_VALUE(), ionadail_TYPE[ionadail_sgòp]); sgrìobh_ionadail(ionadail_sgòp); }
        else if (종류() >= 308 && 종류() <= 312) {
            int còdachadh_VALUE = 종류(); suidhich++; 지역읽기(ionadail_sgòp); int 경계 = CODE_atharraich_am_meud, Air_ais_VALUE_TYPE = eas_preisean_VALUE();
            if (còdachadh_VALUE == 308 && ionadail_TYPE[ionadail_sgòp] == 3) 결합(경계, 3, Air_ais_VALUE_TYPE);
            else {
                dearbh_TYPE(ionadail_TYPE[ionadail_sgòp], 1); dearbh_TYPE(Air_ais_VALUE_TYPE, 1);
                내보내기(còdachadh_VALUE == 308 ? 96 : còdachadh_VALUE == 309 ? 100 : còdachadh_VALUE == 310 ? 104 : còdachadh_VALUE == 311 ? 108 : 112);
                if (ionadail_TYPE[ionadail_sgòp] == 5) 내보내기(146);
            }
            sgrìobh_ionadail(ionadail_sgòp);
        }
        else if (종류() == 306 || 종류() == 307) {
            dearbh_TYPE(ionadail_TYPE[ionadail_sgòp], 1); 내보내기(132); 내보내기(ionadail_sgòp); 내보내기(종류() == 306 ? 1 : 255); suidhich++;
            if (ionadail_TYPE[ionadail_sgòp] == 5) { 지역읽기(ionadail_sgòp); 내보내기(146); sgrìobh_ionadail(ionadail_sgòp); }
        } else fàilligeadh_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        àithne(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean falamh_argamaid = 종류() == ')';
        int TYPE_VALUE = falamh_argamaid ? 0 : eas_preisean_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !falamh_argamaid)) fàilligeadh_VALUE("unsupported print argument");
        àithne(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean aithris_VALUE() {
        if (Mearachd) return false;
        if (깊이 > 32) { fàilligeadh_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean return_tomhas = false;
            while (!Mearachd && 종류() != '}') { if (return_tomhas) fàilligeadh_VALUE("unreachable statement"); return_tomhas = aithris_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < ionadail_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return return_tomhas;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : eas_preisean_VALUE(); dearbh_TYPE(TYPE_VALUE, dòigh_return[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); dearbh_TYPE(eas_preisean_VALUE(), 2); 요구(')'); int FALSE_VALUE = meur(153);
            깊이++; boolean 가 = smachd_aithris(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = meur(167); ceangal_VALUE(FALSE_VALUE, CODE_atharraich_am_meud); 깊이++; boolean 나 = smachd_aithris(); 깊이--; ceangal_VALUE(끝, CODE_atharraich_am_meud); return 가 && 나; }
            ceangal_VALUE(FALSE_VALUE, CODE_atharraich_am_meud); return false;
        }
        if (TAKE_Word("while")) {
            int ruith = CODE_atharraich_am_meud; 요구('('); dearbh_TYPE(eas_preisean_VALUE(), 2); 요구(')'); int 끝 = meur(153);
            깊이++; smachd_aithris(); 깊이--; ceangal_VALUE(meur(167), ruith); ceangal_VALUE(끝, CODE_atharraich_am_meud); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') obair_sgoile_VALUE(true); 요구(';');
            int cumha = CODE_atharraich_am_meud; if (종류() == ';') 내보내기(4); else dearbh_TYPE(eas_preisean_VALUE(), 2); 요구(';');
            int 끝 = meur(153), bodhaig_an_teacsa = meur(167), ath_nuadhaich = CODE_atharraich_am_meud;
            if (종류() != ')') obair_sgoile_VALUE(false); 요구(')'); ceangal_VALUE(meur(167), cumha); ceangal_VALUE(bodhaig_an_teacsa, CODE_atharraich_am_meud);
            smachd_aithris(); ceangal_VALUE(meur(167), ath_nuadhaich); ceangal_VALUE(끝, CODE_atharraich_am_meud);
            for (int 수 = 0; 수 < ionadail_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(suidhich, "System")) { 화면출력(); return false; }
        if (종류() == 256 && suidhich + 1 < tòcan_COUNT && (토큰종류[suidhich + 1] == '(' || 토큰종류[suidhich + 1] == '.')) {
            int TYPE_VALUE = eas_preisean_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        obair_sgoile_VALUE(true); 요구(';'); return false;
    }
    static boolean smachd_aithris() {
        if (Word_VALUE(suidhich, "int") || Word_VALUE(suidhich, "boolean") || Word_VALUE(suidhich, "char") || Word_VALUE(suidhich, "String")
            || Word_VALUE(suidhich, "FileInputStream") || Word_VALUE(suidhich, "FileOutputStream")) fàilligeadh_VALUE("local declaration requires braces");
        return aithris_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) fàilligeadh_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void sgrìobh_clas() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(cunbhalachan_COUNT);
        for (int 수 = 0; 수 < cunbhalachan_atharraich_am_meud; 수++) 출바(cunbhalachan_VALUE[수]);
        출짧(0x21); 출짧(clas_cunbhalachan); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(dòigh_COUNT);
        for (int 수 = 0; 수 < dòigh_COUNT; 수++) {
            출짧(dòigh_inntrigeadh[수]); 출짧(dòigh_ainm_cunbhalachan[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_cunbhalachan);
            출정(12 + dòigh_faid[수]); 출짧(128); 출짧(함수지역[수]); 출정(dòigh_faid[수]);
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < dòigh_faid[수]; slot_cur_a_steach++) 출바(CODE_VALUE[dòigh_CODE[수] + slot_cur_a_steach]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int ruith() {
        if (cleachdaiche.인수개수() == 1 && 자바도구.같음(cleachdaiche.인수(0), "-version")) {
            cleachdaiche.sgrìobh("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (cleachdaiche.인수개수() != 1) { cleachdaiche.sgrìobh("Usage: javac FILE.java\n"); return 2; }
        int ainm_atharraich_am_meud = 자바도구.Ainm(faidhle_ainm_SMS, cleachdaiche.인수(0));
        if (ainm_atharraich_am_meud < 6 || ainm_atharraich_am_meud > 62 || faidhle_ainm_SMS[ainm_atharraich_am_meud - 5] != '.' || faidhle_ainm_SMS[ainm_atharraich_am_meud - 4] != 'j'
            || faidhle_ainm_SMS[ainm_atharraich_am_meud - 3] != 'a' || faidhle_ainm_SMS[ainm_atharraich_am_meud - 2] != 'v' || faidhle_ainm_SMS[ainm_atharraich_am_meud - 1] != 'a') {
            cleachdaiche.sgrìobh("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        tùs_atharraich_am_meud = cleachdaiche.파일읽기(faidhle_ainm_SMS, tùs);
        if (tùs_atharraich_am_meud < 0) { cleachdaiche.sgrìobh("javac: cannot read source: "); 자바도구.수쓰기(tùs_atharraich_am_meud); cleachdaiche.sgrìobh_caractar_VALUE(10); return 1; }
        tùs_atharraich_am_meud = 자바도구.원문해독(tùs, tùs_atharraich_am_meud);
        if (tùs_atharraich_am_meud < 0) { cleachdaiche.sgrìobh("javac error: invalid UTF-8 source\n"); return 1; }
        gearr_VALUE(); if (!Mearachd) 선언읽기();
        if (!Mearachd) {
            if (tòcan_faid[clas_tòcan] != ainm_atharraich_am_meud - 5) fàilligeadh_VALUE("class name must match file name");
            for (int 수 = 0; 수 < ainm_atharraich_am_meud - 5; 수++) if (tùs[tòcan_suidhich[clas_tòcan] + 수] != faidhle_ainm_SMS[수]) fàilligeadh_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < dòigh_COUNT && !Mearachd; 현재함수++) {
            suidhich = 함수본문[현재함수]; dòigh_CODE[현재함수] = CODE_atharraich_am_meud; ionadail_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < dòigh_argamaid_COUNT[현재함수]; 수++) cuir_ris_ionadail(dòigh_argamaid_ainm[현재함수 * 16 + 수], dòigh_argamaid_TYPE[현재함수 * 16 + 수]);
            boolean return_tomhas = aithris_VALUE();
            if (!return_tomhas && dòigh_return[현재함수] != 0) fàilligeadh_VALUE("missing return");
            // meur 뒤의 합류 지점은 반드시 dearbh_dàta 명령이어야 한다 (버전 49 검증기).
            if (dòigh_return[현재함수] == 0) 내보내기(177);
            else { boolean àireamh_shlàn = dòigh_return[현재함수] <= 2 || dòigh_return[현재함수] == 5; 내보내기(àireamh_shlàn ? 3 : 1); 내보내기(àireamh_shlàn ? 172 : 176); }
            if (suidhich != dòigh_crìochnaich[현재함수]) fàilligeadh_VALUE("invalid method body");
            함수지역[현재함수] = ionadail_COUNT; dòigh_faid[현재함수] = CODE_atharraich_am_meud - dòigh_CODE[현재함수];
        }
        if (Mearachd) return 1;
        sgrìobh_clas(); if (Mearachd) return 1;
        faidhle_ainm_SMS[ainm_atharraich_am_meud - 4] = 'c'; faidhle_ainm_SMS[ainm_atharraich_am_meud - 3] = 'l'; faidhle_ainm_SMS[ainm_atharraich_am_meud - 2] = 'a';
        faidhle_ainm_SMS[ainm_atharraich_am_meud - 1] = 's'; faidhle_ainm_SMS[ainm_atharraich_am_meud] = 's'; faidhle_ainm_SMS[ainm_atharraich_am_meud + 1] = 0;
        int tomhas = cleachdaiche.sgrìobh_faidhle(faidhle_ainm_SMS, 출력, 출력크기);
        if (tomhas < 0) { cleachdaiche.sgrìobh("javac: cannot save class: "); 자바도구.수쓰기(tomhas); cleachdaiche.sgrìobh_caractar_VALUE(10); return 1; }
        cleachdaiche.sgrìobh("Compiled: "); for (int 수 = 0; faidhle_ainm_SMS[수] != 0; 수++) cleachdaiche.sgrìobh_caractar_VALUE(faidhle_ainm_SMS[수]);
        cleachdaiche.sgrìobh(" (JVM class version 49)\n"); return 0;
    }
}
