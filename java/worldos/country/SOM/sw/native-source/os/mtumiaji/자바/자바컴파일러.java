// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java chanzo_mti -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] chanzo = new int[16384], 출력 = new int[16384], msimbo_thamani = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], tuzo_urefu = new int[2048];
    static int[] kisobadilika_thamani = new int[4096], kisobadilika_Chipua = new int[512];
    static int[] 문자 = new int[512], faili_jina_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int chanzo_panga_ukubwa, 토큰수, 위치, msimbo_panga_ukubwa, kisobadilika_panga_ukubwa, 상수수 = 1, 출력크기, kibambo_urefu;
    static boolean kosa;
    static int tabaka_tuzo, tabaka_kisobadilika, 부모상수, msimbo_kisobadilika;
    static int[] mbinu_ingizo_jina = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] mbinu_hoja_jina = new int[512], mbinu_hoja_aina = new int[512];
    static int[] mbinu_kiini = new int[32], mbinu_tamatia = new int[32], mbinu_msimbo = new int[32];
    static int[] mbinu_urefu = new int[32], 함수지역 = new int[32], mbinu_jina_kisobadilika = new int[32], 함수서술 = new int[32];
    static int[] mbinu_fikia = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] jirani_jina = new int[128], jirani_aina = new int[128], 지역깊이 = new int[128];

    static void kushindwa_thamani(String 이유) {
        if (!kosa) {
            mtumiaji.andika("javac error: "); mtumiaji.andika(이유);
            mtumiaji.andika(" at line ");
            int laini = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : chanzo_panga_ukubwa;
            for (int 수 = 0; 수 < 끝; 수++) if (chanzo[수] == 10) laini++;
            자바도구.수쓰기(laini); mtumiaji.andika_kibambo_thamani(10);
        }
        kosa = true;
    }
    static boolean kibambo_thamani(int thamani) { return 문자이름규칙.첫글자(thamani); }
    static boolean dijiti_thamani(int thamani) { return thamani >= '0' && thamani <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || tuzo_urefu[가] != tuzo_urefu[나]) return false;
        for (int 수 = 0; 수 < tuzo_urefu[가]; 수++) if (chanzo[토큰위치[가] + 수] != chanzo[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Neno_thamani(int tuzo_thamani, String Neno_SMS) {
        if (tuzo_thamani < 0 || tuzo_thamani >= 토큰수 || tuzo_urefu[tuzo_thamani] != Neno_SMS.length()) return false;
        for (int 수 = 0; 수 < Neno_SMS.length(); 수++) if (chanzo[토큰위치[tuzo_thamani] + 수] != Neno_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int thamani) { if (종류() != thamani) return false; 위치++; return true; }
    static void 요구(int thamani) { if (!받기(thamani)) kushindwa_thamani("unexpected token"); }
    static boolean 말받기(String Neno_SMS) { if (!Neno_thamani(위치, Neno_SMS)) return false; 위치++; return true; }
    static void 말요구(String Neno_SMS) { if (!말받기(Neno_SMS)) kushindwa_thamani(Neno_SMS); }
    static int kitambulishi_thamani() {
        int 결과 = 위치;
        if (종류() != 256) kushindwa_thamani("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int endesha = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - endesha == tuzo_urefu[결과];
                for (int Sloti_ingizo = endesha; 같음 && Sloti_ingizo < 수; Sloti_ingizo++) if (예약어.charAt(Sloti_ingizo) != chanzo[토큰위치[결과] + Sloti_ingizo - endesha]) 같음 = false;
                if (같음) kushindwa_thamani("reserved word cannot be an identifier");
                endesha = 수 + 1;
            }
        }
        return 결과;
    }
    static void kata_thamani() {
        int 수 = 0;
        while (수 < chanzo_panga_ukubwa && !kosa) {
            int thamani = chanzo[수], endesha = 수, 종류 = thamani;
            if (thamani == 32 || thamani == 9 || thamani == 10 || thamani == 13) { 수++; continue; }
            if (thamani == '/' && 수 + 1 < chanzo_panga_ukubwa && chanzo[수 + 1] == '/') {
                while (수 < chanzo_panga_ukubwa && chanzo[수] != 10) 수++;
                continue;
            }
            if (thamani == '/' && 수 + 1 < chanzo_panga_ukubwa && chanzo[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < chanzo_panga_ukubwa && !(chanzo[수] == '*' && chanzo[수 + 1] == '/')) 수++;
                if (수 + 1 >= chanzo_panga_ukubwa) { kushindwa_thamani("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (kibambo_thamani(thamani)) { 종류 = 256; while (수 < chanzo_panga_ukubwa && 문자이름규칙.이어진글자(chanzo[수])) 수++; }
            else if (dijiti_thamani(thamani)) { 종류 = 257; while (수 < chanzo_panga_ukubwa && dijiti_thamani(chanzo[수])) 수++; }
            else if (thamani == '"' || thamani == '\'') {
                종류 = thamani == '"' ? 258 : 259; 수++;
                while (수 < chanzo_panga_ukubwa && chanzo[수] != thamani && chanzo[수] != 10 && chanzo[수] != 13) {
                    if (chanzo[수] == '\\') 수++;
                    수++;
                }
                if (수 >= chanzo_panga_ukubwa || chanzo[수] != thamani) { kushindwa_thamani("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < chanzo_panga_ukubwa) {
                    int 다음 = chanzo[수];
                    if (thamani == '=' && 다음 == '=') 종류 = 300;
                    if (thamani == '!' && 다음 == '=') 종류 = 301;
                    if (thamani == '<' && 다음 == '=') 종류 = 302;
                    if (thamani == '>' && 다음 == '=') 종류 = 303;
                    if (thamani == '&' && 다음 == '&') 종류 = 304;
                    if (thamani == '|' && 다음 == '|') 종류 = 305;
                    if (thamani == '+' && 다음 == '+') 종류 = 306;
                    if (thamani == '-' && 다음 == '-') 종류 = 307;
                    if (thamani == '+' && 다음 == '=') 종류 = 308;
                    if (thamani == '-' && 다음 == '=') 종류 = 309;
                    if (thamani == '*' && 다음 == '=') 종류 = 310;
                    if (thamani == '/' && 다음 == '=') 종류 = 311;
                    if (thamani == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { kushindwa_thamani("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = endesha; tuzo_urefu[토큰수++] = 수 - endesha;
        }
    }
    static void andika_kisobadilika_baiti(int thamani) {
        if (kisobadilika_panga_ukubwa == kisobadilika_thamani.length) { kushindwa_thamani("constant pool too large"); return; }
        kisobadilika_thamani[kisobadilika_panga_ukubwa++] = thamani & 255;
    }
    static void 상짧(int thamani) { andika_kisobadilika_baiti(thamani >> 8); andika_kisobadilika_baiti(thamani); }
    static int sajili_kisobadilika(int endesha) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int mbele_thamani = kisobadilika_Chipua[수], urefu_thamani = (수 + 1 < 상수수 ? kisobadilika_Chipua[수 + 1] : endesha) - mbele_thamani;
            if (urefu_thamani != kisobadilika_panga_ukubwa - endesha) continue;
            boolean 같음 = true;
            for (int Sloti_ingizo = 0; Sloti_ingizo < urefu_thamani; Sloti_ingizo++) if (kisobadilika_thamani[mbele_thamani + Sloti_ingizo] != kisobadilika_thamani[endesha + Sloti_ingizo]) 같음 = false;
            if (같음) { kisobadilika_panga_ukubwa = endesha; return 수; }
        }
        if (상수수 == kisobadilika_Chipua.length) { kushindwa_thamani("too many constants"); return 0; }
        kisobadilika_Chipua[상수수] = endesha;
        return 상수수++;
    }
    static void 글추가(int thamani) {
        if (kibambo_urefu == 문자.length) { kushindwa_thamani("text too long"); return; }
        문자[kibambo_urefu++] = thamani;
    }
    static void 말추가(String Neno_SMS) { for (int 수 = 0; 수 < Neno_SMS.length(); 수++) 글추가(Neno_SMS.charAt(수)); }
    static int kibambo_kisobadilika() {
        int endesha = kisobadilika_panga_ukubwa; andika_kisobadilika_baiti(1); 상짧(0);
        for (int 수 = 0; 수 < kibambo_urefu; 수++) {
            int thamani = 문자[수];
            if (thamani > 0 && thamani < 128) andika_kisobadilika_baiti(thamani);
            else if (thamani < 2048) { andika_kisobadilika_baiti(192 | thamani >> 6); andika_kisobadilika_baiti(128 | thamani & 63); }
            else { andika_kisobadilika_baiti(224 | thamani >> 12); andika_kisobadilika_baiti(128 | thamani >> 6 & 63); andika_kisobadilika_baiti(128 | thamani & 63); }
        }
        if (kosa) return 0;
        int urefu_thamani = kisobadilika_panga_ukubwa - endesha - 3;
        kisobadilika_thamani[endesha + 1] = urefu_thamani >> 8; kisobadilika_thamani[endesha + 2] = urefu_thamani & 255;
        return sajili_kisobadilika(endesha);
    }
    static int Neno_kisobadilika(String Neno_SMS) { kibambo_urefu = 0; 말추가(Neno_SMS); return kibambo_kisobadilika(); }
    static int tuzo_kisobadilika(int tuzo_thamani) {
        kibambo_urefu = 0;
        for (int 수 = 0; 수 < tuzo_urefu[tuzo_thamani]; 수++) 글추가(chanzo[토큰위치[tuzo_thamani] + 수]);
        return kibambo_kisobadilika();
    }
    static int Marejeleo(int 종류, int 가, int 나) {
        int endesha = kisobadilika_panga_ukubwa; andika_kisobadilika_baiti(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return sajili_kisobadilika(endesha);
    }
    static int 외부참조(int 종류, String mmiliki_thamani, String Jina, String 서술) {
        int mmiliki_kitambulishi = Marejeleo(7, Neno_kisobadilika(mmiliki_thamani), 0);
        int 이름수 = Neno_kisobadilika(Jina), 형식수 = Neno_kisobadilika(서술);
        return Marejeleo(종류, mmiliki_kitambulishi, Marejeleo(12, 이름수, 형식수));
    }
    static void 내보내기(int thamani) {
        if (msimbo_panga_ukubwa == msimbo_thamani.length) { kushindwa_thamani("bytecode too large"); return; }
        msimbo_thamani[msimbo_panga_ukubwa++] = thamani & 255;
    }
    static void amri(int thamani, int 인수) { 내보내기(thamani); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int thamani) {
        if (thamani >= -1 && thamani <= 5) { 내보내기(thamani + 3); return; }
        int endesha = kisobadilika_panga_ukubwa; andika_kisobadilika_baiti(3); 상짧(thamani >>> 16); 상짧(thamani);
        amri(19, sajili_kisobadilika(endesha));
    }
    static int tawi(int amri) { int 결과 = msimbo_panga_ukubwa; amri(amri, 0); return 결과; }
    static void Kiungo_thamani(int tawi, int lengo_kipengee) {
        if (kosa) return;
        int 거리 = lengo_kipengee - tawi;
        if (거리 < -32768 || 거리 > 32767 || tawi < 0 || tawi + 2 >= msimbo_panga_ukubwa) { kushindwa_thamani("invalid branch"); return; }
        msimbo_thamani[tawi + 1] = 거리 >> 8 & 255; msimbo_thamani[tawi + 2] = 거리 & 255;
    }
    static void Kulinganisha_thamani(int amri) {
        int 참 = tawi(amri); 내보내기(3); int 끝 = tawi(167);
        Kiungo_thamani(참, msimbo_panga_ukubwa); 내보내기(4); Kiungo_thamani(끝, msimbo_panga_ukubwa);
    }
    static int umbiza_thamani() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        kushindwa_thamani("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void jumlisha_umbiza(int aina_thamani) {
        if (aina_thamani == 0) 글추가('V');
        if (aina_thamani == 1) 글추가('I');
        if (aina_thamani == 2) 글추가('Z');
        if (aina_thamani == 3) 말추가("Ljava/lang/String;");
        if (aina_thamani == 4) 말추가("[Ljava/lang/String;");
        if (aina_thamani == 5) 글추가('C');
        if (aina_thamani == 6) 말추가("Ljava/io/FileInputStream;");
        if (aina_thamani == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws tamko. vighairi Mchakato_thamani_ingizo 본문은 mwenyeji javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("vighairi") || 말받기("실행예외") || 말받기("I_T_vighairi") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("batili_hoja_vighairi") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("batili_Marejeleo_vighairi") || 말받기("산술예외") || 말받기("hali_vighairi") || 말받기("aina_cheza_vighairi") || 말받기("음수배열크기예외") || 말받기("ARRAY_Store_kushindwa") || 말받기("mtungo_hali_vighairi") || 말받기("대기중단예외")) return;
        kushindwa_thamani("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Neno_thamani(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) kushindwa_thamani("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); tabaka_tuzo = kitambulishi_thamani();
        tabaka_kisobadilika = Marejeleo(7, tuzo_kisobadilika(tabaka_tuzo), 0);
        부모상수 = Marejeleo(7, Neno_kisobadilika("java/lang/Object"), 0); msimbo_kisobadilika = Neno_kisobadilika("Code"); 요구('{');
        while (!kosa && 종류() != '}') {
            if (함수수 == 32) { kushindwa_thamani("too many methods"); break; }
            int fikia_ingizo = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int KITENDAKAZI_thamani = 함수수++;
            mbinu_fikia[KITENDAKAZI_thamani] = fikia_ingizo | 8;
            함수반환[KITENDAKAZI_thamani] = umbiza_thamani(); mbinu_ingizo_jina[KITENDAKAZI_thamani] = kitambulishi_thamani(); 요구('(');
            for (int mbele_thamani = 0; mbele_thamani < KITENDAKAZI_thamani; mbele_thamani++) if (이름같음(mbinu_ingizo_jina[mbele_thamani], mbinu_ingizo_jina[KITENDAKAZI_thamani])) kushindwa_thamani("duplicate method (overloading unsupported)");
            while (!kosa && 종류() != ')') {
                int 수 = 함수인수수[KITENDAKAZI_thamani];
                if (수 == 16) { kushindwa_thamani("too many parameters"); break; }
                int aina_thamani = umbiza_thamani(); if (aina_thamani == 0) kushindwa_thamani("void parameter");
                mbinu_hoja_aina[KITENDAKAZI_thamani * 16 + 수] = aina_thamani; mbinu_hoja_jina[KITENDAKAZI_thamani * 16 + 수] = kitambulishi_thamani();
                함수인수수[KITENDAKAZI_thamani]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!kosa && 받기(','));
            }
            mbinu_kiini[KITENDAKAZI_thamani] = 위치; 요구('{');
            int uingiliani_thamani = 1;
            while (위치 < 토큰수 && uingiliani_thamani > 0) {
                if (종류() == '{') uingiliani_thamani++;
                if (종류() == '}') uingiliani_thamani--;
                위치++;
            }
            if (uingiliani_thamani != 0) kushindwa_thamani("unclosed method body");
            mbinu_tamatia[KITENDAKAZI_thamani] = 위치;
            mbinu_jina_kisobadilika[KITENDAKAZI_thamani] = tuzo_kisobadilika(mbinu_ingizo_jina[KITENDAKAZI_thamani]);
            kibambo_urefu = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[KITENDAKAZI_thamani]; 수++) jumlisha_umbiza(mbinu_hoja_aina[KITENDAKAZI_thamani * 16 + 수]);
            글추가(')'); jumlisha_umbiza(함수반환[KITENDAKAZI_thamani]); 함수서술[KITENDAKAZI_thamani] = kibambo_kisobadilika();
        }
        요구('}'); if (위치 != 토큰수) kushindwa_thamani("extra input after class");
    }
    static int gundua_jirani(int Jina) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(jirani_jina[수], Jina)) return 수;
        kushindwa_thamani("unknown variable"); return 0;
    }
    static int jumlisha_jirani(int Jina, int aina_thamani) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(jirani_jina[수], Jina)) kushindwa_thamani("duplicate local variable");
        if (지역수 == 128) { kushindwa_thamani("too many locals"); return 0; }
        jirani_jina[지역수] = Jina; jirani_aina[지역수] = aina_thamani; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean namba_kamili_aina(int aina_thamani) { return aina_thamani == 1 || aina_thamani == 5; }
    static void 지역읽기(int 수) { 내보내기(jirani_aina[수] <= 2 || jirani_aina[수] == 5 ? 21 : 25); 내보내기(수); }
    static void andika_jirani(int 수) { 내보내기(jirani_aina[수] <= 2 || jirani_aina[수] == 5 ? 54 : 58); 내보내기(수); }
    static void thibitisha_aina(int halisi_data, int 기대) { if (halisi_data != 기대 && !(halisi_data == 5 && 기대 == 1)) kushindwa_thamani("type mismatch"); }
    static void 문자읽기(int tuzo_thamani) {
        kibambo_urefu = 0; int endesha = 토큰위치[tuzo_thamani] + 1, 끝 = 토큰위치[tuzo_thamani] + tuzo_urefu[tuzo_thamani] - 1;
        while (endesha < 끝 && !kosa) {
            int thamani = chanzo[endesha++];
            if (thamani == '\\') {
                if (endesha == 끝) { kushindwa_thamani("invalid escape"); break; }
                thamani = chanzo[endesha++];
                if (thamani == 'n') thamani = 10;
                else if (thamani == 'r') thamani = 13;
                else if (thamani == 't') thamani = 9;
                else if (thamani == 'b') thamani = 8;
                else if (thamani == 'f') thamani = 12;
                else if (thamani != '\\' && thamani != '"' && thamani != '\'') kushindwa_thamani("unsupported escape");
            }
            글추가(thamani);
        }
    }
    static int changanua_namba_kamili(int tuzo_thamani, boolean 음수) {
        if (tuzo_urefu[tuzo_thamani] > 1 && chanzo[토큰위치[tuzo_thamani]] == '0') kushindwa_thamani("octal literals unsupported");
        int thamani = 0;
        for (int 수 = 0; 수 < tuzo_urefu[tuzo_thamani]; 수++) {
            int dijiti_kipengee = chanzo[토큰위치[tuzo_thamani] + 수] - '0';
            if (thamani < -214748364 || thamani == -214748364 && dijiti_kipengee > (음수 ? 8 : 7)) kushindwa_thamani("integer literal out of range");
            thamani = thamani * 10 - dijiti_kipengee;
        }
        return 음수 ? thamani : -thamani;
    }
    static int 기본식() {
        if (말받기("new")) {
            int aina_thamani = umbiza_thamani();
            if (aina_thamani != 6 && aina_thamani != 7) { kushindwa_thamani("only file streams supported by new in source"); return 0; }
            String mmiliki_thamani = aina_thamani == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            amri(187, Marejeleo(7, Neno_kisobadilika(mmiliki_thamani), 0)); 내보내기(89);
            요구('('); thibitisha_aina(usemi_thamani(), 3); boolean 이어 = false;
            if (받기(',')) { if (aina_thamani != 7) kushindwa_thamani("input stream constructor arguments"); thibitisha_aina(usemi_thamani(), 2); 이어 = true; }
            요구(')');
            amri(183, 외부참조(10, mmiliki_thamani, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return aina_thamani;
        }
        if (받기('(')) { int aina_thamani = usemi_thamani(); 요구(')'); return aina_thamani; }
        if (종류() == 257) { 수상수(changanua_namba_kamili(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); amri(19, Marejeleo(8, kibambo_kisobadilika(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (kibambo_urefu != 1) kushindwa_thamani("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String mmiliki_thamani = "", mbinu_thamani = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                mmiliki_thamani = "한국어/자체/출력"; 요구('.');
                if (말받기("andika_laini")) { mbinu_thamani = "andika_laini"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("andika")) { mbinu_thamani = "andika"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { mbinu_thamani = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else kushindwa_thamani("unknown Korean output method");
            } else if (말받기("문자")) {
                mmiliki_thamani = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("urefu_thamani")) { mbinu_thamani = "urefu_thamani"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { mbinu_thamani = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("changanua_namba_kamili")) { mbinu_thamani = "changanua_namba_kamili"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("andika_namba_kamili_thamani")) { mbinu_thamani = "andika_namba_kamili_thamani"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { mbinu_thamani = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("bandika_SMS")) { mbinu_thamani = "bandika_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("kata_thamani")) { mbinu_thamani = "kata_thamani"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else kushindwa_thamani("unknown Korean text method");
            } else if (말받기("faili")) {
                mmiliki_thamani = "한국어/자체/faili"; 요구('.'); 가 = 3;
                if (말받기("읽기")) { mbinu_thamani = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("andika")) { mbinu_thamani = "andika"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else kushindwa_thamani("unknown Korean file method");
            } else if (말받기("화면")) {
                mmiliki_thamani = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { mbinu_thamani = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { mbinu_thamani = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { mbinu_thamani = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("futa_ingizo")) { mbinu_thamani = "futa_ingizo"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { mbinu_thamani = "기다리기"; 서술 = "()V"; }
                else kushindwa_thamani("unknown Korean framebuffer method");
            } else kushindwa_thamani("unsupported Korean library class");
            요구('('); if (가 != 0) thibitisha_aina(usemi_thamani(), 가);
            if (나 != 0) { 요구(','); thibitisha_aina(usemi_thamani(), 나); }
            if (다 != 0) { 요구(','); thibitisha_aina(usemi_thamani(), 다); }
            if (라 != 0) { 요구(','); thibitisha_aina(usemi_thamani(), 라); }
            if (마 != 0) { 요구(','); thibitisha_aina(usemi_thamani(), 마); }
            요구(')'); amri(184, 외부참조(10, mmiliki_thamani, mbinu_thamani, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); thibitisha_aina(usemi_thamani(), 3); 요구(')');
            amri(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Jina = kitambulishi_thamani();
        if (받기('(')) {
            int KITENDAKAZI_thamani = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Jina, mbinu_ingizo_jina[수])) KITENDAKAZI_thamani = 수;
            if (KITENDAKAZI_thamani < 0) { kushindwa_thamani("unknown static method"); return 0; }
            int 수 = 0;
            while (!kosa && 종류() != ')') {
                if (수 >= 함수인수수[KITENDAKAZI_thamani]) { kushindwa_thamani("too many arguments"); break; }
                thibitisha_aina(usemi_thamani(), mbinu_hoja_aina[KITENDAKAZI_thamani * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[KITENDAKAZI_thamani]) kushindwa_thamani("argument count mismatch");
            amri(184, Marejeleo(10, tabaka_kisobadilika, Marejeleo(12, mbinu_jina_kisobadilika[KITENDAKAZI_thamani], 함수서술[KITENDAKAZI_thamani])));
            return 함수반환[KITENDAKAZI_thamani];
        }
        int jirani_upeo = gundua_jirani(Jina), aina_thamani = jirani_aina[jirani_upeo]; 지역읽기(jirani_upeo);
        while (!kosa) {
            if (받기('[')) { thibitisha_aina(aina_thamani, 4); thibitisha_aina(usemi_thamani(), 1); 요구(']'); 내보내기(50); aina_thamani = 3; }
            else if (받기('.')) {
                if (aina_thamani == 6 || aina_thamani == 7) {
                    String mmiliki_thamani = aina_thamani == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); amri(182, 외부참조(10, mmiliki_thamani, "close", "()V")); aina_thamani = 0; }
                    else if (aina_thamani == 6 && 말받기("read")) { 요구('('); 요구(')'); amri(182, 외부참조(10, mmiliki_thamani, "read", "()I")); aina_thamani = 1; }
                    else if (aina_thamani == 7 && 말받기("write")) { 요구('('); thibitisha_aina(usemi_thamani(), 1); 요구(')'); amri(182, 외부참조(10, mmiliki_thamani, "write", "(I)V")); aina_thamani = 0; }
                    else { kushindwa_thamani("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (aina_thamani == 4) { 내보내기(190); aina_thamani = 1; }
                else { thibitisha_aina(aina_thamani, 3); 요구('('); 요구(')'); amri(182, 외부참조(10, "java/lang/String", "length", "()I")); aina_thamani = 1; }
            } else break;
        }
        return aina_thamani;
    }
    static int 단항() {
        if (++식깊이 > 64) { kushindwa_thamani("expression nesting too deep"); 식깊이--; return 0; }
        int aina_thamani;
        if (받기('!')) { thibitisha_aina(단항(), 2); Kulinganisha_thamani(153); aina_thamani = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(changanua_namba_kamili(위치++, true));
            else { thibitisha_aina(단항(), 1); 내보내기(116); }
            aina_thamani = 1;
        } else if (받기('+')) { thibitisha_aina(단항(), 1); aina_thamani = 1; }
        else aina_thamani = 기본식();
        식깊이--; return aina_thamani;
    }
    static int 곱식() {
        int aina_thamani = 단항();
        while (!kosa && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int usimbaji_thamani = 종류(); 위치++; thibitisha_aina(aina_thamani, 1); thibitisha_aina(단항(), 1);
            내보내기(usimbaji_thamani == '*' ? 104 : usimbaji_thamani == '/' ? 108 : 112); aina_thamani = 1;
        }
        return aina_thamani;
    }
    static int 합식() {
        int aina_thamani = 곱식();
        while (!kosa && (종류() == '+' || 종류() == '-')) {
            int usimbaji_thamani = 종류(); 위치++; int 경계 = msimbo_panga_ukubwa, Nyuma_thamani_aina = 곱식();
            if (usimbaji_thamani == '+' && (aina_thamani == 3 || Nyuma_thamani_aina == 3)) { 결합(경계, aina_thamani, Nyuma_thamani_aina); aina_thamani = 3; }
            else { thibitisha_aina(aina_thamani, 1); thibitisha_aina(Nyuma_thamani_aina, 1); 내보내기(usimbaji_thamani == '+' ? 96 : 100); aina_thamani = 1; }
        }
        return aina_thamani;
    }
    static int 붙임참조(int aina_thamani) {
        if (aina_thamani != 1 && aina_thamani != 2 && aina_thamani != 3 && aina_thamani != 5) kushindwa_thamani("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", aina_thamani == 1 ? "(I)Ljava/lang/StringBuilder;"
            : aina_thamani == 2 ? "(Z)Ljava/lang/StringBuilder;" : aina_thamani == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int mbele_thamani_aina, int Nyuma_thamani_aina) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 msimbo_thamani 앞에 생성 코드를 삽입한다.
        // 오른쪽 usemi_thamani 내부의 kompyuta_rika_thamani tawi 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = msimbo_panga_ukubwa;
        amri(187, Marejeleo(7, Neno_kisobadilika("java/lang/StringBuilder"), 0)); 내보내기(89);
        amri(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); amri(182, 붙임참조(mbele_thamani_aina));
        if (kosa) return;
        int urefu_thamani = msimbo_panga_ukubwa - 끝;
        for (int 수 = 0; 수 < urefu_thamani; 수++) 삽입코드[수] = msimbo_thamani[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) msimbo_thamani[수 + urefu_thamani] = msimbo_thamani[수];
        for (int 수 = 0; 수 < urefu_thamani; 수++) msimbo_thamani[경계 + 수] = 삽입코드[수];
        amri(182, 붙임참조(Nyuma_thamani_aina)); amri(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Kulinganisha_usemi() {
        int aina_thamani = 합식();
        while (!kosa && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int usimbaji_thamani = 종류(); 위치++; thibitisha_aina(aina_thamani, 1); thibitisha_aina(합식(), 1);
            Kulinganisha_thamani(usimbaji_thamani == '<' ? 161 : usimbaji_thamani == '>' ? 163 : usimbaji_thamani == 302 ? 164 : 162); aina_thamani = 2;
        }
        return aina_thamani;
    }
    static int 동등식() {
        int aina_thamani = Kulinganisha_usemi();
        while (!kosa && (종류() == 300 || 종류() == 301)) {
            int usimbaji_thamani = 종류(); 위치++; int Nyuma_thamani_aina = Kulinganisha_usemi();
            if (aina_thamani == 0 || Nyuma_thamani_aina == 0) kushindwa_thamani("void expression");
            if (!(namba_kamili_aina(aina_thamani) && namba_kamili_aina(Nyuma_thamani_aina))) thibitisha_aina(Nyuma_thamani_aina, aina_thamani);
            Kulinganisha_thamani((aina_thamani <= 2 || aina_thamani == 5 ? 159 : 165) + (usimbaji_thamani == 301 ? 1 : 0)); aina_thamani = 2;
        }
        return aina_thamani;
    }
    static int 논리곱() {
        int aina_thamani = 동등식();
        while (!kosa && 받기(304)) {
            thibitisha_aina(aina_thamani, 2); int 가 = tawi(153); thibitisha_aina(동등식(), 2); int 나 = tawi(153);
            내보내기(4); int 끝 = tawi(167); Kiungo_thamani(가, msimbo_panga_ukubwa); Kiungo_thamani(나, msimbo_panga_ukubwa); 내보내기(3); Kiungo_thamani(끝, msimbo_panga_ukubwa); aina_thamani = 2;
        }
        return aina_thamani;
    }
    static int usemi_thamani() {
        int aina_thamani = 논리곱();
        while (!kosa && 받기(305)) {
            thibitisha_aina(aina_thamani, 2); int 가 = tawi(154); thibitisha_aina(논리곱(), 2); int 나 = tawi(154);
            내보내기(3); int 끝 = tawi(167); Kiungo_thamani(가, msimbo_panga_ukubwa); Kiungo_thamani(나, msimbo_panga_ukubwa); 내보내기(4); Kiungo_thamani(끝, msimbo_panga_ukubwa); aina_thamani = 2;
        }
        return aina_thamani;
    }
    static void kazi_thamani(boolean Ruhusu_tamko) {
        if (Neno_thamani(위치, "int") || Neno_thamani(위치, "boolean") || Neno_thamani(위치, "String") || Neno_thamani(위치, "char")
            || Neno_thamani(위치, "FileInputStream") || Neno_thamani(위치, "FileOutputStream")) {
            if (!Ruhusu_tamko) kushindwa_thamani("declaration not allowed here");
            int aina_thamani = umbiza_thamani(), Jina = kitambulishi_thamani(); 요구('='); thibitisha_aina(usemi_thamani(), aina_thamani);
            andika_jirani(jumlisha_jirani(Jina, aina_thamani)); return;
        }
        int Jina = kitambulishi_thamani(), jirani_upeo = gundua_jirani(Jina);
        if (받기('=')) { thibitisha_aina(usemi_thamani(), jirani_aina[jirani_upeo]); andika_jirani(jirani_upeo); }
        else if (종류() >= 308 && 종류() <= 312) {
            int usimbaji_thamani = 종류(); 위치++; 지역읽기(jirani_upeo); int 경계 = msimbo_panga_ukubwa, Nyuma_thamani_aina = usemi_thamani();
            if (usimbaji_thamani == 308 && jirani_aina[jirani_upeo] == 3) 결합(경계, 3, Nyuma_thamani_aina);
            else {
                thibitisha_aina(jirani_aina[jirani_upeo], 1); thibitisha_aina(Nyuma_thamani_aina, 1);
                내보내기(usimbaji_thamani == 308 ? 96 : usimbaji_thamani == 309 ? 100 : usimbaji_thamani == 310 ? 104 : usimbaji_thamani == 311 ? 108 : 112);
                if (jirani_aina[jirani_upeo] == 5) 내보내기(146);
            }
            andika_jirani(jirani_upeo);
        }
        else if (종류() == 306 || 종류() == 307) {
            thibitisha_aina(jirani_aina[jirani_upeo], 1); 내보내기(132); 내보내기(jirani_upeo); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (jirani_aina[jirani_upeo] == 5) { 지역읽기(jirani_upeo); 내보내기(146); andika_jirani(jirani_upeo); }
        } else kushindwa_thamani("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        amri(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean tupu_hoja = 종류() == ')';
        int aina_thamani = tupu_hoja ? 0 : usemi_thamani(); 요구(')'); 요구(';');
        String 서술 = aina_thamani == 0 ? "()V" : aina_thamani == 1 ? "(I)V" : aina_thamani == 2 ? "(Z)V" : aina_thamani == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (aina_thamani == 4 || aina_thamani >= 6 || aina_thamani == 0 && (!줄바꿈 || !tupu_hoja)) kushindwa_thamani("unsupported print argument");
        amri(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean kauli_thamani() {
        if (kosa) return false;
        if (깊이 > 32) { kushindwa_thamani("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!kosa && 종류() != '}') { if (반환) kushindwa_thamani("unreachable statement"); 반환 = kauli_thamani(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int aina_thamani = 종류() == ';' ? 0 : usemi_thamani(); thibitisha_aina(aina_thamani, 함수반환[현재함수]); 요구(';');
            내보내기(aina_thamani == 0 ? 177 : aina_thamani <= 2 || aina_thamani == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); thibitisha_aina(usemi_thamani(), 2); 요구(')'); int 거짓 = tawi(153);
            깊이++; boolean 가 = udhibiti_kauli(); 깊이--;
            if (말받기("else")) { int 끝 = tawi(167); Kiungo_thamani(거짓, msimbo_panga_ukubwa); 깊이++; boolean 나 = udhibiti_kauli(); 깊이--; Kiungo_thamani(끝, msimbo_panga_ukubwa); return 가 && 나; }
            Kiungo_thamani(거짓, msimbo_panga_ukubwa); return false;
        }
        if (말받기("while")) {
            int endesha = msimbo_panga_ukubwa; 요구('('); thibitisha_aina(usemi_thamani(), 2); 요구(')'); int 끝 = tawi(153);
            깊이++; udhibiti_kauli(); 깊이--; Kiungo_thamani(tawi(167), endesha); Kiungo_thamani(끝, msimbo_panga_ukubwa); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') kazi_thamani(true); 요구(';');
            int sharti = msimbo_panga_ukubwa; if (종류() == ';') 내보내기(4); else thibitisha_aina(usemi_thamani(), 2); 요구(';');
            int 끝 = tawi(153), Matini_kiini = tawi(167), onyesha_upya = msimbo_panga_ukubwa;
            if (종류() != ')') kazi_thamani(false); 요구(')'); Kiungo_thamani(tawi(167), sharti); Kiungo_thamani(Matini_kiini, msimbo_panga_ukubwa);
            udhibiti_kauli(); Kiungo_thamani(tawi(167), onyesha_upya); Kiungo_thamani(끝, msimbo_panga_ukubwa);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Neno_thamani(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int aina_thamani = usemi_thamani(); if (aina_thamani != 0) 내보내기(87); 요구(';'); return false;
        }
        kazi_thamani(true); 요구(';'); return false;
    }
    static boolean udhibiti_kauli() {
        if (Neno_thamani(위치, "int") || Neno_thamani(위치, "boolean") || Neno_thamani(위치, "char") || Neno_thamani(위치, "String")
            || Neno_thamani(위치, "FileInputStream") || Neno_thamani(위치, "FileOutputStream")) kushindwa_thamani("local declaration requires braces");
        return kauli_thamani();
    }
    static void 출바(int thamani) { if (출력크기 == 출력.length) kushindwa_thamani("class file too large"); else 출력[출력크기++] = thamani & 255; }
    static void 출짧(int thamani) { 출바(thamani >> 8); 출바(thamani); }
    static void 출정(int thamani) { 출짧(thamani >>> 16); 출짧(thamani); }
    static void andika_tabaka() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < kisobadilika_panga_ukubwa; 수++) 출바(kisobadilika_thamani[수]);
        출짧(0x21); 출짧(tabaka_kisobadilika); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(mbinu_fikia[수]); 출짧(mbinu_jina_kisobadilika[수]); 출짧(함수서술[수]); 출짧(1); 출짧(msimbo_kisobadilika);
            출정(12 + mbinu_urefu[수]); 출짧(128); 출짧(함수지역[수]); 출정(mbinu_urefu[수]);
            for (int Sloti_ingizo = 0; Sloti_ingizo < mbinu_urefu[수]; Sloti_ingizo++) 출바(msimbo_thamani[mbinu_msimbo[수] + Sloti_ingizo]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int endesha() {
        if (mtumiaji.인수개수() == 1 && 자바도구.같음(mtumiaji.인수(0), "-version")) {
            mtumiaji.andika("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (mtumiaji.인수개수() != 1) { mtumiaji.andika("Usage: javac FILE.java\n"); return 2; }
        int jina_panga_ukubwa = 자바도구.Jina(faili_jina_SMS, mtumiaji.인수(0));
        if (jina_panga_ukubwa < 6 || jina_panga_ukubwa > 62 || faili_jina_SMS[jina_panga_ukubwa - 5] != '.' || faili_jina_SMS[jina_panga_ukubwa - 4] != 'j'
            || faili_jina_SMS[jina_panga_ukubwa - 3] != 'a' || faili_jina_SMS[jina_panga_ukubwa - 2] != 'v' || faili_jina_SMS[jina_panga_ukubwa - 1] != 'a') {
            mtumiaji.andika("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        chanzo_panga_ukubwa = mtumiaji.파일읽기(faili_jina_SMS, chanzo);
        if (chanzo_panga_ukubwa < 0) { mtumiaji.andika("javac: cannot read source: "); 자바도구.수쓰기(chanzo_panga_ukubwa); mtumiaji.andika_kibambo_thamani(10); return 1; }
        chanzo_panga_ukubwa = 자바도구.원문해독(chanzo, chanzo_panga_ukubwa);
        if (chanzo_panga_ukubwa < 0) { mtumiaji.andika("javac error: invalid UTF-8 source\n"); return 1; }
        kata_thamani(); if (!kosa) 선언읽기();
        if (!kosa) {
            if (tuzo_urefu[tabaka_tuzo] != jina_panga_ukubwa - 5) kushindwa_thamani("class name must match file name");
            for (int 수 = 0; 수 < jina_panga_ukubwa - 5; 수++) if (chanzo[토큰위치[tabaka_tuzo] + 수] != faili_jina_SMS[수]) kushindwa_thamani("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !kosa; 현재함수++) {
            위치 = mbinu_kiini[현재함수]; mbinu_msimbo[현재함수] = msimbo_panga_ukubwa; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) jumlisha_jirani(mbinu_hoja_jina[현재함수 * 16 + 수], mbinu_hoja_aina[현재함수 * 16 + 수]);
            boolean 반환 = kauli_thamani();
            if (!반환 && 함수반환[현재함수] != 0) kushindwa_thamani("missing return");
            // tawi 뒤의 합류 지점은 반드시 halisi_data 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean namba_kamili = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(namba_kamili ? 3 : 1); 내보내기(namba_kamili ? 172 : 176); }
            if (위치 != mbinu_tamatia[현재함수]) kushindwa_thamani("invalid method body");
            함수지역[현재함수] = 지역수; mbinu_urefu[현재함수] = msimbo_panga_ukubwa - mbinu_msimbo[현재함수];
        }
        if (kosa) return 1;
        andika_tabaka(); if (kosa) return 1;
        faili_jina_SMS[jina_panga_ukubwa - 4] = 'c'; faili_jina_SMS[jina_panga_ukubwa - 3] = 'l'; faili_jina_SMS[jina_panga_ukubwa - 2] = 'a';
        faili_jina_SMS[jina_panga_ukubwa - 1] = 's'; faili_jina_SMS[jina_panga_ukubwa] = 's'; faili_jina_SMS[jina_panga_ukubwa + 1] = 0;
        int 결과 = mtumiaji.andika_faili(faili_jina_SMS, 출력, 출력크기);
        if (결과 < 0) { mtumiaji.andika("javac: cannot save class: "); 자바도구.수쓰기(결과); mtumiaji.andika_kibambo_thamani(10); return 1; }
        mtumiaji.andika("Compiled: "); for (int 수 = 0; faili_jina_SMS[수] != 0; 수++) mtumiaji.andika_kibambo_thamani(faili_jina_SMS[수]);
        mtumiaji.andika(" (JVM class version 49)\n"); return 0;
    }
}
