// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java foinse_crann -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] FOINSE = new int[16384], Aschur = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], licín_suíomh = new int[2048], licín_fad = new int[2048];
    static int[] tairiseach_VALUE = new int[4096], tairiseach_OFFSET = new int[512];
    static int[] 문자 = new int[512], comhad_ainm_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int foinse_socraigh_méid, licín_COUNT, suíomh, CODE_socraigh_méid, tairiseach_socraigh_méid, tairiseach_COUNT = 1, 출력크기, carachtar_fad;
    static boolean ERREÁID;
    static int aicme_licín, aicme_tairiseach, 부모상수, CODE_tairiseach;
    static int[] modh_iontráil_ainm = new int[32], modh_return = new int[32], modh_argóint_COUNT = new int[32];
    static int[] modh_argóint_ainm = new int[512], modh_argóint_TYPE = new int[512];
    static int[] modh_corp = new int[32], modh_cuir_deireadh_le = new int[32], modh_CODE = new int[32];
    static int[] modh_fad = new int[32], 함수지역 = new int[32], modh_ainm_tairiseach = new int[32], 함수서술 = new int[32];
    static int[] modh_rochtain = new int[32];
    static int modh_COUNT, 현재함수, logánta_COUNT, 깊이, 식깊이;
    static int[] logánta_ainm = new int[128], logánta_TYPE = new int[128], 지역깊이 = new int[128];

    static void teip_VALUE(String 이유) {
        if (!ERREÁID) {
            úsáideoir.Scríobh("javac error: "); úsáideoir.Scríobh(이유);
            úsáideoir.Scríobh(" at line ");
            int Líne = 1, 끝 = suíomh < licín_COUNT ? licín_suíomh[suíomh] : foinse_socraigh_méid;
            for (int 수 = 0; 수 < 끝; 수++) if (FOINSE[수] == 10) Líne++;
            자바도구.수쓰기(Líne); úsáideoir.scríobh_carachtar_VALUE(10);
        }
        ERREÁID = true;
    }
    static boolean carachtar_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean digit_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= licín_COUNT || 나 >= licín_COUNT || licín_fad[가] != licín_fad[나]) return false;
        for (int 수 = 0; 수 < licín_fad[가]; 수++) if (FOINSE[licín_suíomh[가] + 수] != FOINSE[licín_suíomh[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int licín_VALUE, String Word_SMS) {
        if (licín_VALUE < 0 || licín_VALUE >= licín_COUNT || licín_fad[licín_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (FOINSE[licín_suíomh[licín_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return suíomh < licín_COUNT ? 토큰종류[suíomh] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; suíomh++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) teip_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(suíomh, Word_SMS)) return false; suíomh++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) teip_VALUE(Word_SMS); }
    static int aitheantóir_VALUE() {
        int tomhas = suíomh;
        if (종류() != 256) teip_VALUE("identifier required"); else suíomh++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Rith_2 = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Rith_2 == licín_fad[tomhas];
                for (int spás_iontráil = Rith_2; 같음 && spás_iontráil < 수; spás_iontráil++) if (예약어.charAt(spás_iontráil) != FOINSE[licín_suíomh[tomhas] + spás_iontráil - Rith_2]) 같음 = false;
                if (같음) teip_VALUE("reserved word cannot be an identifier");
                Rith_2 = 수 + 1;
            }
        }
        return tomhas;
    }
    static void gearr_VALUE() {
        int 수 = 0;
        while (수 < foinse_socraigh_méid && !ERREÁID) {
            int VALUE = FOINSE[수], Rith_2 = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < foinse_socraigh_méid && FOINSE[수 + 1] == '/') {
                while (수 < foinse_socraigh_méid && FOINSE[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < foinse_socraigh_méid && FOINSE[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < foinse_socraigh_méid && !(FOINSE[수] == '*' && FOINSE[수 + 1] == '/')) 수++;
                if (수 + 1 >= foinse_socraigh_méid) { teip_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (carachtar_VALUE(VALUE)) { 종류 = 256; while (수 < foinse_socraigh_méid && 문자이름규칙.이어진글자(FOINSE[수])) 수++; }
            else if (digit_VALUE(VALUE)) { 종류 = 257; while (수 < foinse_socraigh_méid && digit_VALUE(FOINSE[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < foinse_socraigh_méid && FOINSE[수] != VALUE && FOINSE[수] != 10 && FOINSE[수] != 13) {
                    if (FOINSE[수] == '\\') 수++;
                    수++;
                }
                if (수 >= foinse_socraigh_méid || FOINSE[수] != VALUE) { teip_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < foinse_socraigh_méid) {
                    int Ar_aghaidh_mír = FOINSE[수];
                    if (VALUE == '=' && Ar_aghaidh_mír == '=') 종류 = 300;
                    if (VALUE == '!' && Ar_aghaidh_mír == '=') 종류 = 301;
                    if (VALUE == '<' && Ar_aghaidh_mír == '=') 종류 = 302;
                    if (VALUE == '>' && Ar_aghaidh_mír == '=') 종류 = 303;
                    if (VALUE == '&' && Ar_aghaidh_mír == '&') 종류 = 304;
                    if (VALUE == '|' && Ar_aghaidh_mír == '|') 종류 = 305;
                    if (VALUE == '+' && Ar_aghaidh_mír == '+') 종류 = 306;
                    if (VALUE == '-' && Ar_aghaidh_mír == '-') 종류 = 307;
                    if (VALUE == '+' && Ar_aghaidh_mír == '=') 종류 = 308;
                    if (VALUE == '-' && Ar_aghaidh_mír == '=') 종류 = 309;
                    if (VALUE == '*' && Ar_aghaidh_mír == '=') 종류 = 310;
                    if (VALUE == '/' && Ar_aghaidh_mír == '=') 종류 = 311;
                    if (VALUE == '%' && Ar_aghaidh_mír == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (licín_COUNT == 토큰종류.length - 1) { teip_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[licín_COUNT] = 종류; licín_suíomh[licín_COUNT] = Rith_2; licín_fad[licín_COUNT++] = 수 - Rith_2;
        }
    }
    static void scríobh_tairiseach_beart(int VALUE) {
        if (tairiseach_socraigh_méid == tairiseach_VALUE.length) { teip_VALUE("constant pool too large"); return; }
        tairiseach_VALUE[tairiseach_socraigh_méid++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { scríobh_tairiseach_beart(VALUE >> 8); scríobh_tairiseach_beart(VALUE); }
    static int cláraigh_tairiseach(int Rith_2) {
        for (int 수 = 1; 수 < tairiseach_COUNT; 수++) {
            int 앞 = tairiseach_OFFSET[수], fad_VALUE = (수 + 1 < tairiseach_COUNT ? tairiseach_OFFSET[수 + 1] : Rith_2) - 앞;
            if (fad_VALUE != tairiseach_socraigh_méid - Rith_2) continue;
            boolean 같음 = true;
            for (int spás_iontráil = 0; spás_iontráil < fad_VALUE; spás_iontráil++) if (tairiseach_VALUE[앞 + spás_iontráil] != tairiseach_VALUE[Rith_2 + spás_iontráil]) 같음 = false;
            if (같음) { tairiseach_socraigh_méid = Rith_2; return 수; }
        }
        if (tairiseach_COUNT == tairiseach_OFFSET.length) { teip_VALUE("too many constants"); return 0; }
        tairiseach_OFFSET[tairiseach_COUNT] = Rith_2;
        return tairiseach_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (carachtar_fad == 문자.length) { teip_VALUE("text too long"); return; }
        문자[carachtar_fad++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int carachtar_tairiseach() {
        int Rith_2 = tairiseach_socraigh_méid; scríobh_tairiseach_beart(1); 상짧(0);
        for (int 수 = 0; 수 < carachtar_fad; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) scríobh_tairiseach_beart(VALUE);
            else if (VALUE < 2048) { scríobh_tairiseach_beart(192 | VALUE >> 6); scríobh_tairiseach_beart(128 | VALUE & 63); }
            else { scríobh_tairiseach_beart(224 | VALUE >> 12); scríobh_tairiseach_beart(128 | VALUE >> 6 & 63); scríobh_tairiseach_beart(128 | VALUE & 63); }
        }
        if (ERREÁID) return 0;
        int fad_VALUE = tairiseach_socraigh_méid - Rith_2 - 3;
        tairiseach_VALUE[Rith_2 + 1] = fad_VALUE >> 8; tairiseach_VALUE[Rith_2 + 2] = fad_VALUE & 255;
        return cláraigh_tairiseach(Rith_2);
    }
    static int Word_tairiseach(String Word_SMS) { carachtar_fad = 0; 말추가(Word_SMS); return carachtar_tairiseach(); }
    static int licín_tairiseach(int licín_VALUE) {
        carachtar_fad = 0;
        for (int 수 = 0; 수 < licín_fad[licín_VALUE]; 수++) 글추가(FOINSE[licín_suíomh[licín_VALUE] + 수]);
        return carachtar_tairiseach();
    }
    static int Leabhair_thagartha(int 종류, int 가, int 나) {
        int Rith_2 = tairiseach_socraigh_méid; scríobh_tairiseach_beart(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return cláraigh_tairiseach(Rith_2);
    }
    static int tagairt_sheachtrach(int 종류, String úinéir_VALUE, String Ainm, String 서술) {
        int úinéir_aitheantóir = Leabhair_thagartha(7, Word_tairiseach(úinéir_VALUE), 0);
        int ainm_COUNT = Word_tairiseach(Ainm), formáid_COUNT = Word_tairiseach(서술);
        return Leabhair_thagartha(종류, úinéir_aitheantóir, Leabhair_thagartha(12, ainm_COUNT, formáid_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_socraigh_méid == CODE_VALUE.length) { teip_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_socraigh_méid++] = VALUE & 255;
    }
    static void Ordú(int VALUE, int Argóintí) { 내보내기(VALUE); 내보내기(Argóintí >> 8); 내보내기(Argóintí); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Rith_2 = tairiseach_socraigh_méid; scríobh_tairiseach_beart(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Ordú(19, cláraigh_tairiseach(Rith_2));
    }
    static int craobh(int Ordú) { int tomhas = CODE_socraigh_méid; Ordú(Ordú, 0); return tomhas; }
    static void Nasc_VALUE(int craobh, int sprioc_oibiacht) {
        if (ERREÁID) return;
        int 거리 = sprioc_oibiacht - craobh;
        if (거리 < -32768 || 거리 > 32767 || craobh < 0 || craobh + 2 >= CODE_socraigh_méid) { teip_VALUE("invalid branch"); return; }
        CODE_VALUE[craobh + 1] = 거리 >> 8 & 255; CODE_VALUE[craobh + 2] = 거리 & 255;
    }
    static void 비교값(int Ordú) {
        int TRUE_VALUE = craobh(Ordú); 내보내기(3); int 끝 = craobh(167);
        Nasc_VALUE(TRUE_VALUE, CODE_socraigh_méid); 내보내기(4); Nasc_VALUE(끝, CODE_socraigh_méid);
    }
    static int formáid_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        teip_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void cuir_le_formáid(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. eisceacht Próiseas_VALUE_iontráil 본문은 óstach javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Gaeilge");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("eisceacht") || TAKE_Word("실행예외") || TAKE_Word("I_O_eisceacht") || TAKE_Word("대기시간초과예외") || TAKE_Word("ADDRESS_LOOKUP_eisceacht") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("neamhbhailí_argóint_eisceacht") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_Leabhair_thagartha_eisceacht") || TAKE_Word("산술예외") || TAKE_Word("staid_eisceacht") || TAKE_Word("TYPE_craol_eisceacht") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_teip") || TAKE_Word("snáithe_staid_eisceacht") || TAKE_Word("대기중단예외")) return;
        teip_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(suíomh, "Gaeilge")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) teip_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); aicme_licín = aitheantóir_VALUE();
        aicme_tairiseach = Leabhair_thagartha(7, licín_tairiseach(aicme_licín), 0);
        부모상수 = Leabhair_thagartha(7, Word_tairiseach("java/lang/Object"), 0); CODE_tairiseach = Word_tairiseach("Code"); 요구('{');
        while (!ERREÁID && 종류() != '}') {
            if (modh_COUNT == 32) { teip_VALUE("too many methods"); break; }
            int rochtain_iontráil = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int feidhm_VALUE = modh_COUNT++;
            modh_rochtain[feidhm_VALUE] = rochtain_iontráil | 8;
            modh_return[feidhm_VALUE] = formáid_VALUE(); modh_iontráil_ainm[feidhm_VALUE] = aitheantóir_VALUE(); 요구('(');
            for (int 앞 = 0; 앞 < feidhm_VALUE; 앞++) if (이름같음(modh_iontráil_ainm[앞], modh_iontráil_ainm[feidhm_VALUE])) teip_VALUE("duplicate method (overloading unsupported)");
            while (!ERREÁID && 종류() != ')') {
                int 수 = modh_argóint_COUNT[feidhm_VALUE];
                if (수 == 16) { teip_VALUE("too many parameters"); break; }
                int TYPE_VALUE = formáid_VALUE(); if (TYPE_VALUE == 0) teip_VALUE("void parameter");
                modh_argóint_TYPE[feidhm_VALUE * 16 + 수] = TYPE_VALUE; modh_argóint_ainm[feidhm_VALUE * 16 + 수] = aitheantóir_VALUE();
                modh_argóint_COUNT[feidhm_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!ERREÁID && 받기(','));
            }
            modh_corp[feidhm_VALUE] = suíomh; 요구('{');
            int 중첩 = 1;
            while (suíomh < licín_COUNT && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                suíomh++;
            }
            if (중첩 != 0) teip_VALUE("unclosed method body");
            modh_cuir_deireadh_le[feidhm_VALUE] = suíomh;
            modh_ainm_tairiseach[feidhm_VALUE] = licín_tairiseach(modh_iontráil_ainm[feidhm_VALUE]);
            carachtar_fad = 0; 글추가('(');
            for (int 수 = 0; 수 < modh_argóint_COUNT[feidhm_VALUE]; 수++) cuir_le_formáid(modh_argóint_TYPE[feidhm_VALUE * 16 + 수]);
            글추가(')'); cuir_le_formáid(modh_return[feidhm_VALUE]); 함수서술[feidhm_VALUE] = carachtar_tairiseach();
        }
        요구('}'); if (suíomh != licín_COUNT) teip_VALUE("extra input after class");
    }
    static int FIND_logánta(int Ainm) {
        for (int 수 = logánta_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(logánta_ainm[수], Ainm)) return 수;
        teip_VALUE("unknown variable"); return 0;
    }
    static int cuir_le_logánta(int Ainm, int TYPE_VALUE) {
        for (int 수 = 0; 수 < logánta_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(logánta_ainm[수], Ainm)) teip_VALUE("duplicate local variable");
        if (logánta_COUNT == 128) { teip_VALUE("too many locals"); return 0; }
        logánta_ainm[logánta_COUNT] = Ainm; logánta_TYPE[logánta_COUNT] = TYPE_VALUE; 지역깊이[logánta_COUNT] = 깊이;
        return logánta_COUNT++;
    }
    static boolean slánuimhir_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(logánta_TYPE[수] <= 2 || logánta_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void scríobh_logánta(int 수) { 내보내기(logánta_TYPE[수] <= 2 || logánta_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void fíoraigh_TYPE(int iarbhír_sonraí, int 기대) { if (iarbhír_sonraí != 기대 && !(iarbhír_sonraí == 5 && 기대 == 1)) teip_VALUE("type mismatch"); }
    static void 문자읽기(int licín_VALUE) {
        carachtar_fad = 0; int Rith_2 = licín_suíomh[licín_VALUE] + 1, 끝 = licín_suíomh[licín_VALUE] + licín_fad[licín_VALUE] - 1;
        while (Rith_2 < 끝 && !ERREÁID) {
            int VALUE = FOINSE[Rith_2++];
            if (VALUE == '\\') {
                if (Rith_2 == 끝) { teip_VALUE("invalid escape"); break; }
                VALUE = FOINSE[Rith_2++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') teip_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int parsáil_slánuimhir(int licín_VALUE, boolean 음수) {
        if (licín_fad[licín_VALUE] > 1 && FOINSE[licín_suíomh[licín_VALUE]] == '0') teip_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < licín_fad[licín_VALUE]; 수++) {
            int digit_mír = FOINSE[licín_suíomh[licín_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && digit_mír > (음수 ? 8 : 7)) teip_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - digit_mír;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = formáid_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { teip_VALUE("only file streams supported by new in source"); return 0; }
            String úinéir_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Ordú(187, Leabhair_thagartha(7, Word_tairiseach(úinéir_VALUE), 0)); 내보내기(89);
            요구('('); fíoraigh_TYPE(slonn_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) teip_VALUE("input stream constructor arguments"); fíoraigh_TYPE(slonn_VALUE(), 2); 이어 = true; }
            요구(')');
            Ordú(183, tagairt_sheachtrach(10, úinéir_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = slonn_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(parsáil_slánuimhir(suíomh++, false)); return 1; }
        if (종류() == 258) { 문자읽기(suíomh++); Ordú(19, Leabhair_thagartha(8, carachtar_tairiseach(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(suíomh++); if (carachtar_fad != 1) teip_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Gaeilge")) {
            요구('.'); 말요구("자체"); 요구('.');
            String úinéir_VALUE = "", modh_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, tomhas = 0;
            if (TAKE_Word("Aschur")) {
                úinéir_VALUE = "Gaeilge/자체/Aschur"; 요구('.');
                if (TAKE_Word("scríobh_líne")) { modh_VALUE = "scríobh_líne"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Scríobh")) { modh_VALUE = "Scríobh"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { modh_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else teip_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                úinéir_VALUE = "Gaeilge/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("fad_VALUE")) { modh_VALUE = "fad_VALUE"; 서술 = "(Ljava/lang/String;)I"; tomhas = 1; }
                else if (TAKE_Word("pointe_cóid_COUNT")) { modh_VALUE = "pointe_cóid_COUNT"; 서술 = "(Ljava/lang/String;)I"; tomhas = 1; }
                else if (TAKE_Word("parsáil_slánuimhir")) { modh_VALUE = "parsáil_slánuimhir"; 서술 = "(Ljava/lang/String;)I"; tomhas = 1; }
                else if (TAKE_Word("scríobh_slánuimhir_VALUE")) { modh_VALUE = "scríobh_slánuimhir_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; tomhas = 3; }
                else if (TAKE_Word("같음")) { modh_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; tomhas = 2; }
                else if (TAKE_Word("greamaigh_SMS")) { modh_VALUE = "greamaigh_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; tomhas = 3; }
                else if (TAKE_Word("gearr_VALUE")) { modh_VALUE = "gearr_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; tomhas = 3; }
                else teip_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Comhad")) {
                úinéir_VALUE = "Gaeilge/자체/Comhad"; 요구('.'); 가 = 3;
                if (TAKE_Word("Léigh")) { modh_VALUE = "Léigh"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; tomhas = 3; }
                else if (TAKE_Word("Scríobh")) { modh_VALUE = "Scríobh"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else teip_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                úinéir_VALUE = "Gaeilge/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { modh_VALUE = "너비"; 서술 = "()I"; tomhas = 1; }
                else if (TAKE_Word("높이")) { modh_VALUE = "높이"; 서술 = "()I"; tomhas = 1; }
                else if (TAKE_Word("사각형")) { modh_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("지우기")) { modh_VALUE = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { modh_VALUE = "기다리기"; 서술 = "()V"; }
                else teip_VALUE("unknown Korean framebuffer method");
            } else teip_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) fíoraigh_TYPE(slonn_VALUE(), 가);
            if (나 != 0) { 요구(','); fíoraigh_TYPE(slonn_VALUE(), 나); }
            if (다 != 0) { 요구(','); fíoraigh_TYPE(slonn_VALUE(), 다); }
            if (라 != 0) { 요구(','); fíoraigh_TYPE(slonn_VALUE(), 라); }
            if (마 != 0) { 요구(','); fíoraigh_TYPE(slonn_VALUE(), 마); }
            요구(')'); Ordú(184, tagairt_sheachtrach(10, úinéir_VALUE, modh_VALUE, 서술)); return tomhas;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); fíoraigh_TYPE(slonn_VALUE(), 3); 요구(')');
            Ordú(184, tagairt_sheachtrach(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Ainm = aitheantóir_VALUE();
        if (받기('(')) {
            int feidhm_VALUE = -1;
            for (int 수 = 0; 수 < modh_COUNT; 수++) if (이름같음(Ainm, modh_iontráil_ainm[수])) feidhm_VALUE = 수;
            if (feidhm_VALUE < 0) { teip_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!ERREÁID && 종류() != ')') {
                if (수 >= modh_argóint_COUNT[feidhm_VALUE]) { teip_VALUE("too many arguments"); break; }
                fíoraigh_TYPE(slonn_VALUE(), modh_argóint_TYPE[feidhm_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != modh_argóint_COUNT[feidhm_VALUE]) teip_VALUE("argument count mismatch");
            Ordú(184, Leabhair_thagartha(10, aicme_tairiseach, Leabhair_thagartha(12, modh_ainm_tairiseach[feidhm_VALUE], 함수서술[feidhm_VALUE])));
            return modh_return[feidhm_VALUE];
        }
        int logánta_scóip = FIND_logánta(Ainm), TYPE_VALUE = logánta_TYPE[logánta_scóip]; 지역읽기(logánta_scóip);
        while (!ERREÁID) {
            if (받기('[')) { fíoraigh_TYPE(TYPE_VALUE, 4); fíoraigh_TYPE(slonn_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String úinéir_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Ordú(182, tagairt_sheachtrach(10, úinéir_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Ordú(182, tagairt_sheachtrach(10, úinéir_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); fíoraigh_TYPE(slonn_VALUE(), 1); 요구(')'); Ordú(182, tagairt_sheachtrach(10, úinéir_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { teip_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { fíoraigh_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Ordú(182, tagairt_sheachtrach(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { teip_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { fíoraigh_TYPE(단항(), 2); 비교값(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(parsáil_slánuimhir(suíomh++, true));
            else { fíoraigh_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { fíoraigh_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!ERREÁID && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int ionchódú_VALUE = 종류(); suíomh++; fíoraigh_TYPE(TYPE_VALUE, 1); fíoraigh_TYPE(단항(), 1);
            내보내기(ionchódú_VALUE == '*' ? 104 : ionchódú_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!ERREÁID && (종류() == '+' || 종류() == '-')) {
            int ionchódú_VALUE = 종류(); suíomh++; int 경계 = CODE_socraigh_méid, Siar_VALUE_TYPE = 곱식();
            if (ionchódú_VALUE == '+' && (TYPE_VALUE == 3 || Siar_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, Siar_VALUE_TYPE); TYPE_VALUE = 3; }
            else { fíoraigh_TYPE(TYPE_VALUE, 1); fíoraigh_TYPE(Siar_VALUE_TYPE, 1); 내보내기(ionchódú_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) teip_VALUE("unsupported concatenation type");
        return tagairt_sheachtrach(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Siar_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 giniúint 코드를 삽입한다.
        // RIGHT slonn_VALUE 내부의 piara_VALUE craobh 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_socraigh_méid;
        Ordú(187, Leabhair_thagartha(7, Word_tairiseach("java/lang/StringBuilder"), 0)); 내보내기(89);
        Ordú(183, tagairt_sheachtrach(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Ordú(182, 붙임참조(앞형));
        if (ERREÁID) return;
        int fad_VALUE = CODE_socraigh_méid - 끝;
        for (int 수 = 0; 수 < fad_VALUE; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + fad_VALUE] = CODE_VALUE[수];
        for (int 수 = 0; 수 < fad_VALUE; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        Ordú(182, 붙임참조(Siar_VALUE_TYPE)); Ordú(182, tagairt_sheachtrach(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int TYPE_VALUE = 합식();
        while (!ERREÁID && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int ionchódú_VALUE = 종류(); suíomh++; fíoraigh_TYPE(TYPE_VALUE, 1); fíoraigh_TYPE(합식(), 1);
            비교값(ionchódú_VALUE == '<' ? 161 : ionchódú_VALUE == '>' ? 163 : ionchódú_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = 비교식();
        while (!ERREÁID && (종류() == 300 || 종류() == 301)) {
            int ionchódú_VALUE = 종류(); suíomh++; int Siar_VALUE_TYPE = 비교식();
            if (TYPE_VALUE == 0 || Siar_VALUE_TYPE == 0) teip_VALUE("void expression");
            if (!(slánuimhir_TYPE(TYPE_VALUE) && slánuimhir_TYPE(Siar_VALUE_TYPE))) fíoraigh_TYPE(Siar_VALUE_TYPE, TYPE_VALUE);
            비교값((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (ionchódú_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!ERREÁID && 받기(304)) {
            fíoraigh_TYPE(TYPE_VALUE, 2); int 가 = craobh(153); fíoraigh_TYPE(동등식(), 2); int 나 = craobh(153);
            내보내기(4); int 끝 = craobh(167); Nasc_VALUE(가, CODE_socraigh_méid); Nasc_VALUE(나, CODE_socraigh_méid); 내보내기(3); Nasc_VALUE(끝, CODE_socraigh_méid); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int slonn_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!ERREÁID && 받기(305)) {
            fíoraigh_TYPE(TYPE_VALUE, 2); int 가 = craobh(154); fíoraigh_TYPE(논리곱(), 2); int 나 = craobh(154);
            내보내기(3); int 끝 = craobh(167); Nasc_VALUE(가, CODE_socraigh_méid); Nasc_VALUE(나, CODE_socraigh_méid); 내보내기(4); Nasc_VALUE(끝, CODE_socraigh_méid); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void tasc_VALUE(boolean 선언허용) {
        if (Word_VALUE(suíomh, "int") || Word_VALUE(suíomh, "boolean") || Word_VALUE(suíomh, "String") || Word_VALUE(suíomh, "char")
            || Word_VALUE(suíomh, "FileInputStream") || Word_VALUE(suíomh, "FileOutputStream")) {
            if (!선언허용) teip_VALUE("declaration not allowed here");
            int TYPE_VALUE = formáid_VALUE(), Ainm = aitheantóir_VALUE(); 요구('='); fíoraigh_TYPE(slonn_VALUE(), TYPE_VALUE);
            scríobh_logánta(cuir_le_logánta(Ainm, TYPE_VALUE)); return;
        }
        int Ainm = aitheantóir_VALUE(), logánta_scóip = FIND_logánta(Ainm);
        if (받기('=')) { fíoraigh_TYPE(slonn_VALUE(), logánta_TYPE[logánta_scóip]); scríobh_logánta(logánta_scóip); }
        else if (종류() >= 308 && 종류() <= 312) {
            int ionchódú_VALUE = 종류(); suíomh++; 지역읽기(logánta_scóip); int 경계 = CODE_socraigh_méid, Siar_VALUE_TYPE = slonn_VALUE();
            if (ionchódú_VALUE == 308 && logánta_TYPE[logánta_scóip] == 3) 결합(경계, 3, Siar_VALUE_TYPE);
            else {
                fíoraigh_TYPE(logánta_TYPE[logánta_scóip], 1); fíoraigh_TYPE(Siar_VALUE_TYPE, 1);
                내보내기(ionchódú_VALUE == 308 ? 96 : ionchódú_VALUE == 309 ? 100 : ionchódú_VALUE == 310 ? 104 : ionchódú_VALUE == 311 ? 108 : 112);
                if (logánta_TYPE[logánta_scóip] == 5) 내보내기(146);
            }
            scríobh_logánta(logánta_scóip);
        }
        else if (종류() == 306 || 종류() == 307) {
            fíoraigh_TYPE(logánta_TYPE[logánta_scóip], 1); 내보내기(132); 내보내기(logánta_scóip); 내보내기(종류() == 306 ? 1 : 255); suíomh++;
            if (logánta_TYPE[logánta_scóip] == 5) { 지역읽기(logánta_scóip); 내보내기(146); scríobh_logánta(logánta_scóip); }
        } else teip_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Ordú(178, tagairt_sheachtrach(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean folamh_argóint = 종류() == ')';
        int TYPE_VALUE = folamh_argóint ? 0 : slonn_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !folamh_argóint)) teip_VALUE("unsupported print argument");
        Ordú(182, tagairt_sheachtrach(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean ráiteas_VALUE() {
        if (ERREÁID) return false;
        if (깊이 > 32) { teip_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean return_tomhas = false;
            while (!ERREÁID && 종류() != '}') { if (return_tomhas) teip_VALUE("unreachable statement"); return_tomhas = ráiteas_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < logánta_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return return_tomhas;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : slonn_VALUE(); fíoraigh_TYPE(TYPE_VALUE, modh_return[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); fíoraigh_TYPE(slonn_VALUE(), 2); 요구(')'); int FALSE_VALUE = craobh(153);
            깊이++; boolean 가 = rialú_ráiteas(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = craobh(167); Nasc_VALUE(FALSE_VALUE, CODE_socraigh_méid); 깊이++; boolean 나 = rialú_ráiteas(); 깊이--; Nasc_VALUE(끝, CODE_socraigh_méid); return 가 && 나; }
            Nasc_VALUE(FALSE_VALUE, CODE_socraigh_méid); return false;
        }
        if (TAKE_Word("while")) {
            int Rith_2 = CODE_socraigh_méid; 요구('('); fíoraigh_TYPE(slonn_VALUE(), 2); 요구(')'); int 끝 = craobh(153);
            깊이++; rialú_ráiteas(); 깊이--; Nasc_VALUE(craobh(167), Rith_2); Nasc_VALUE(끝, CODE_socraigh_méid); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') tasc_VALUE(true); 요구(';');
            int coinníoll = CODE_socraigh_méid; if (종류() == ';') 내보내기(4); else fíoraigh_TYPE(slonn_VALUE(), 2); 요구(';');
            int 끝 = craobh(153), corpthéacs = craobh(167), athnuaigh = CODE_socraigh_méid;
            if (종류() != ')') tasc_VALUE(false); 요구(')'); Nasc_VALUE(craobh(167), coinníoll); Nasc_VALUE(corpthéacs, CODE_socraigh_méid);
            rialú_ráiteas(); Nasc_VALUE(craobh(167), athnuaigh); Nasc_VALUE(끝, CODE_socraigh_méid);
            for (int 수 = 0; 수 < logánta_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(suíomh, "System")) { 화면출력(); return false; }
        if (종류() == 256 && suíomh + 1 < licín_COUNT && (토큰종류[suíomh + 1] == '(' || 토큰종류[suíomh + 1] == '.')) {
            int TYPE_VALUE = slonn_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        tasc_VALUE(true); 요구(';'); return false;
    }
    static boolean rialú_ráiteas() {
        if (Word_VALUE(suíomh, "int") || Word_VALUE(suíomh, "boolean") || Word_VALUE(suíomh, "char") || Word_VALUE(suíomh, "String")
            || Word_VALUE(suíomh, "FileInputStream") || Word_VALUE(suíomh, "FileOutputStream")) teip_VALUE("local declaration requires braces");
        return ráiteas_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == Aschur.length) teip_VALUE("class file too large"); else Aschur[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void scríobh_aicme() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(tairiseach_COUNT);
        for (int 수 = 0; 수 < tairiseach_socraigh_méid; 수++) 출바(tairiseach_VALUE[수]);
        출짧(0x21); 출짧(aicme_tairiseach); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(modh_COUNT);
        for (int 수 = 0; 수 < modh_COUNT; 수++) {
            출짧(modh_rochtain[수]); 출짧(modh_ainm_tairiseach[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_tairiseach);
            출정(12 + modh_fad[수]); 출짧(128); 출짧(함수지역[수]); 출정(modh_fad[수]);
            for (int spás_iontráil = 0; spás_iontráil < modh_fad[수]; spás_iontráil++) 출바(CODE_VALUE[modh_CODE[수] + spás_iontráil]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Rith_2() {
        if (úsáideoir.인수개수() == 1 && 자바도구.같음(úsáideoir.Argóintí(0), "-version")) {
            úsáideoir.Scríobh("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (úsáideoir.인수개수() != 1) { úsáideoir.Scríobh("Usage: javac FILE.java\n"); return 2; }
        int ainm_socraigh_méid = 자바도구.Ainm(comhad_ainm_SMS, úsáideoir.Argóintí(0));
        if (ainm_socraigh_méid < 6 || ainm_socraigh_méid > 62 || comhad_ainm_SMS[ainm_socraigh_méid - 5] != '.' || comhad_ainm_SMS[ainm_socraigh_méid - 4] != 'j'
            || comhad_ainm_SMS[ainm_socraigh_méid - 3] != 'a' || comhad_ainm_SMS[ainm_socraigh_méid - 2] != 'v' || comhad_ainm_SMS[ainm_socraigh_méid - 1] != 'a') {
            úsáideoir.Scríobh("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        foinse_socraigh_méid = úsáideoir.파일읽기(comhad_ainm_SMS, FOINSE);
        if (foinse_socraigh_méid < 0) { úsáideoir.Scríobh("javac: cannot read source: "); 자바도구.수쓰기(foinse_socraigh_méid); úsáideoir.scríobh_carachtar_VALUE(10); return 1; }
        foinse_socraigh_méid = 자바도구.원문해독(FOINSE, foinse_socraigh_méid);
        if (foinse_socraigh_méid < 0) { úsáideoir.Scríobh("javac error: invalid UTF-8 source\n"); return 1; }
        gearr_VALUE(); if (!ERREÁID) 선언읽기();
        if (!ERREÁID) {
            if (licín_fad[aicme_licín] != ainm_socraigh_méid - 5) teip_VALUE("class name must match file name");
            for (int 수 = 0; 수 < ainm_socraigh_méid - 5; 수++) if (FOINSE[licín_suíomh[aicme_licín] + 수] != comhad_ainm_SMS[수]) teip_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < modh_COUNT && !ERREÁID; 현재함수++) {
            suíomh = modh_corp[현재함수]; modh_CODE[현재함수] = CODE_socraigh_méid; logánta_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < modh_argóint_COUNT[현재함수]; 수++) cuir_le_logánta(modh_argóint_ainm[현재함수 * 16 + 수], modh_argóint_TYPE[현재함수 * 16 + 수]);
            boolean return_tomhas = ráiteas_VALUE();
            if (!return_tomhas && modh_return[현재함수] != 0) teip_VALUE("missing return");
            // craobh 뒤의 합류 지점은 반드시 iarbhír_sonraí 명령이어야 한다 (버전 49 검증기).
            if (modh_return[현재함수] == 0) 내보내기(177);
            else { boolean slánuimhir = modh_return[현재함수] <= 2 || modh_return[현재함수] == 5; 내보내기(slánuimhir ? 3 : 1); 내보내기(slánuimhir ? 172 : 176); }
            if (suíomh != modh_cuir_deireadh_le[현재함수]) teip_VALUE("invalid method body");
            함수지역[현재함수] = logánta_COUNT; modh_fad[현재함수] = CODE_socraigh_méid - modh_CODE[현재함수];
        }
        if (ERREÁID) return 1;
        scríobh_aicme(); if (ERREÁID) return 1;
        comhad_ainm_SMS[ainm_socraigh_méid - 4] = 'c'; comhad_ainm_SMS[ainm_socraigh_méid - 3] = 'l'; comhad_ainm_SMS[ainm_socraigh_méid - 2] = 'a';
        comhad_ainm_SMS[ainm_socraigh_méid - 1] = 's'; comhad_ainm_SMS[ainm_socraigh_méid] = 's'; comhad_ainm_SMS[ainm_socraigh_méid + 1] = 0;
        int tomhas = úsáideoir.scríobh_comhad(comhad_ainm_SMS, Aschur, 출력크기);
        if (tomhas < 0) { úsáideoir.Scríobh("javac: cannot save class: "); 자바도구.수쓰기(tomhas); úsáideoir.scríobh_carachtar_VALUE(10); return 1; }
        úsáideoir.Scríobh("Compiled: "); for (int 수 = 0; comhad_ainm_SMS[수] != 0; 수++) úsáideoir.scríobh_carachtar_VALUE(comhad_ainm_SMS[수]);
        úsáideoir.Scríobh(" (JVM class version 49)\n"); return 0;
    }
}
