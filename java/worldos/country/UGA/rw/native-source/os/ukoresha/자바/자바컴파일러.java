// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java inkomoko_igiti -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] Inkomoko = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], tike_uburebure = new int[2048];
    static int[] kidahinduka_agaciro = new int[4096], kidahinduka_Ofuseti = new int[512];
    static int[] 문자 = new int[512], dosiye_izina_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int inkomoko_ingano, 토큰수, 위치, 코드크기, kidahinduka_ingano, 상수수 = 1, 출력크기, inyuguti_uburebure;
    static boolean IKOSA;
    static int icyiciro_tike, icyiciro_kidahinduka, 부모상수, 코드상수;
    static int[] uburyo_icyinjizwa_izina = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] uburyo_ingingo_izina = new int[512], 함수인수형 = new int[512];
    static int[] 함수본문 = new int[32], uburyo_kurangiza = new int[32], 함수코드 = new int[32];
    static int[] uburyo_uburebure = new int[32], 함수지역 = new int[32], uburyo_izina_kidahinduka = new int[32], 함수서술 = new int[32];
    static int[] uburyo_kwinjira = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] mu_gace_izina = new int[128], 지역형 = new int[128], 지역깊이 = new int[128];

    static void kudakora_agaciro(String 이유) {
        if (!IKOSA) {
            ukoresha.kwandika("javac error: "); ukoresha.kwandika(이유);
            ukoresha.kwandika(" at line ");
            int umurongo = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : inkomoko_ingano;
            for (int 수 = 0; 수 < 끝; 수++) if (Inkomoko[수] == 10) umurongo++;
            자바도구.수쓰기(umurongo); ukoresha.kwandika_inyuguti_agaciro(10);
        }
        IKOSA = true;
    }
    static boolean inyuguti_agaciro(int agaciro) { return 문자이름규칙.첫글자(agaciro); }
    static boolean umubare_agaciro(int agaciro) { return agaciro >= '0' && agaciro <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || tike_uburebure[가] != tike_uburebure[나]) return false;
        for (int 수 = 0; 수 < tike_uburebure[가]; 수++) if (Inkomoko[토큰위치[가] + 수] != Inkomoko[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Ijambo_agaciro(int tike_agaciro, String Ijambo_SMS) {
        if (tike_agaciro < 0 || tike_agaciro >= 토큰수 || tike_uburebure[tike_agaciro] != Ijambo_SMS.length()) return false;
        for (int 수 = 0; 수 < Ijambo_SMS.length(); 수++) if (Inkomoko[토큰위치[tike_agaciro] + 수] != Ijambo_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int agaciro) { if (종류() != agaciro) return false; 위치++; return true; }
    static void 요구(int agaciro) { if (!받기(agaciro)) kudakora_agaciro("unexpected token"); }
    static boolean 말받기(String Ijambo_SMS) { if (!Ijambo_agaciro(위치, Ijambo_SMS)) return false; 위치++; return true; }
    static void 말요구(String Ijambo_SMS) { if (!말받기(Ijambo_SMS)) kudakora_agaciro(Ijambo_SMS); }
    static int indanga_agaciro() {
        int 결과 = 위치;
        if (종류() != 256) kudakora_agaciro("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int ihuriro = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - ihuriro == tike_uburebure[결과];
                for (int umwanya_icyinjizwa = ihuriro; 같음 && umwanya_icyinjizwa < 수; umwanya_icyinjizwa++) if (예약어.charAt(umwanya_icyinjizwa) != Inkomoko[토큰위치[결과] + umwanya_icyinjizwa - ihuriro]) 같음 = false;
                if (같음) kudakora_agaciro("reserved word cannot be an identifier");
                ihuriro = 수 + 1;
            }
        }
        return 결과;
    }
    static void gukata_agaciro() {
        int 수 = 0;
        while (수 < inkomoko_ingano && !IKOSA) {
            int agaciro = Inkomoko[수], ihuriro = 수, 종류 = agaciro;
            if (agaciro == 32 || agaciro == 9 || agaciro == 10 || agaciro == 13) { 수++; continue; }
            if (agaciro == '/' && 수 + 1 < inkomoko_ingano && Inkomoko[수 + 1] == '/') {
                while (수 < inkomoko_ingano && Inkomoko[수] != 10) 수++;
                continue;
            }
            if (agaciro == '/' && 수 + 1 < inkomoko_ingano && Inkomoko[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < inkomoko_ingano && !(Inkomoko[수] == '*' && Inkomoko[수 + 1] == '/')) 수++;
                if (수 + 1 >= inkomoko_ingano) { kudakora_agaciro("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (inyuguti_agaciro(agaciro)) { 종류 = 256; while (수 < inkomoko_ingano && 문자이름규칙.이어진글자(Inkomoko[수])) 수++; }
            else if (umubare_agaciro(agaciro)) { 종류 = 257; while (수 < inkomoko_ingano && umubare_agaciro(Inkomoko[수])) 수++; }
            else if (agaciro == '"' || agaciro == '\'') {
                종류 = agaciro == '"' ? 258 : 259; 수++;
                while (수 < inkomoko_ingano && Inkomoko[수] != agaciro && Inkomoko[수] != 10 && Inkomoko[수] != 13) {
                    if (Inkomoko[수] == '\\') 수++;
                    수++;
                }
                if (수 >= inkomoko_ingano || Inkomoko[수] != agaciro) { kudakora_agaciro("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < inkomoko_ingano) {
                    int 다음 = Inkomoko[수];
                    if (agaciro == '=' && 다음 == '=') 종류 = 300;
                    if (agaciro == '!' && 다음 == '=') 종류 = 301;
                    if (agaciro == '<' && 다음 == '=') 종류 = 302;
                    if (agaciro == '>' && 다음 == '=') 종류 = 303;
                    if (agaciro == '&' && 다음 == '&') 종류 = 304;
                    if (agaciro == '|' && 다음 == '|') 종류 = 305;
                    if (agaciro == '+' && 다음 == '+') 종류 = 306;
                    if (agaciro == '-' && 다음 == '-') 종류 = 307;
                    if (agaciro == '+' && 다음 == '=') 종류 = 308;
                    if (agaciro == '-' && 다음 == '=') 종류 = 309;
                    if (agaciro == '*' && 다음 == '=') 종류 = 310;
                    if (agaciro == '/' && 다음 == '=') 종류 = 311;
                    if (agaciro == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { kudakora_agaciro("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = ihuriro; tike_uburebure[토큰수++] = 수 - ihuriro;
        }
    }
    static void kwandika_kidahinduka_bayiti(int agaciro) {
        if (kidahinduka_ingano == kidahinduka_agaciro.length) { kudakora_agaciro("constant pool too large"); return; }
        kidahinduka_agaciro[kidahinduka_ingano++] = agaciro & 255;
    }
    static void 상짧(int agaciro) { kwandika_kidahinduka_bayiti(agaciro >> 8); kwandika_kidahinduka_bayiti(agaciro); }
    static int 상등록(int ihuriro) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = kidahinduka_Ofuseti[수], uburebure_agaciro = (수 + 1 < 상수수 ? kidahinduka_Ofuseti[수 + 1] : ihuriro) - 앞;
            if (uburebure_agaciro != kidahinduka_ingano - ihuriro) continue;
            boolean 같음 = true;
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < uburebure_agaciro; umwanya_icyinjizwa++) if (kidahinduka_agaciro[앞 + umwanya_icyinjizwa] != kidahinduka_agaciro[ihuriro + umwanya_icyinjizwa]) 같음 = false;
            if (같음) { kidahinduka_ingano = ihuriro; return 수; }
        }
        if (상수수 == kidahinduka_Ofuseti.length) { kudakora_agaciro("too many constants"); return 0; }
        kidahinduka_Ofuseti[상수수] = ihuriro;
        return 상수수++;
    }
    static void 글추가(int agaciro) {
        if (inyuguti_uburebure == 문자.length) { kudakora_agaciro("text too long"); return; }
        문자[inyuguti_uburebure++] = agaciro;
    }
    static void 말추가(String Ijambo_SMS) { for (int 수 = 0; 수 < Ijambo_SMS.length(); 수++) 글추가(Ijambo_SMS.charAt(수)); }
    static int inyuguti_kidahinduka() {
        int ihuriro = kidahinduka_ingano; kwandika_kidahinduka_bayiti(1); 상짧(0);
        for (int 수 = 0; 수 < inyuguti_uburebure; 수++) {
            int agaciro = 문자[수];
            if (agaciro > 0 && agaciro < 128) kwandika_kidahinduka_bayiti(agaciro);
            else if (agaciro < 2048) { kwandika_kidahinduka_bayiti(192 | agaciro >> 6); kwandika_kidahinduka_bayiti(128 | agaciro & 63); }
            else { kwandika_kidahinduka_bayiti(224 | agaciro >> 12); kwandika_kidahinduka_bayiti(128 | agaciro >> 6 & 63); kwandika_kidahinduka_bayiti(128 | agaciro & 63); }
        }
        if (IKOSA) return 0;
        int uburebure_agaciro = kidahinduka_ingano - ihuriro - 3;
        kidahinduka_agaciro[ihuriro + 1] = uburebure_agaciro >> 8; kidahinduka_agaciro[ihuriro + 2] = uburebure_agaciro & 255;
        return 상등록(ihuriro);
    }
    static int Ijambo_kidahinduka(String Ijambo_SMS) { inyuguti_uburebure = 0; 말추가(Ijambo_SMS); return inyuguti_kidahinduka(); }
    static int tike_kidahinduka(int tike_agaciro) {
        inyuguti_uburebure = 0;
        for (int 수 = 0; 수 < tike_uburebure[tike_agaciro]; 수++) 글추가(Inkomoko[토큰위치[tike_agaciro] + 수]);
        return inyuguti_kidahinduka();
    }
    static int Indanga(int 종류, int 가, int 나) {
        int ihuriro = kidahinduka_ingano; kwandika_kidahinduka_bayiti(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return 상등록(ihuriro);
    }
    static int 외부참조(int 종류, String nyirayo_agaciro, String Izina, String 서술) {
        int nyirayo_indanga = Indanga(7, Ijambo_kidahinduka(nyirayo_agaciro), 0);
        int 이름수 = Ijambo_kidahinduka(Izina), 형식수 = Ijambo_kidahinduka(서술);
        return Indanga(종류, nyirayo_indanga, Indanga(12, 이름수, 형식수));
    }
    static void 내보내기(int agaciro) {
        if (코드크기 == 코드.length) { kudakora_agaciro("bytecode too large"); return; }
        코드[코드크기++] = agaciro & 255;
    }
    static void Icyo_wifuza(int agaciro, int 인수) { 내보내기(agaciro); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int agaciro) {
        if (agaciro >= -1 && agaciro <= 5) { 내보내기(agaciro + 3); return; }
        int ihuriro = kidahinduka_ingano; kwandika_kidahinduka_bayiti(3); 상짧(agaciro >>> 16); 상짧(agaciro);
        Icyo_wifuza(19, 상등록(ihuriro));
    }
    static int ishami(int Icyo_wifuza) { int 결과 = 코드크기; Icyo_wifuza(Icyo_wifuza, 0); return 결과; }
    static void Ihuza_agaciro(int ishami, int gusimbuza_igishya_ikintu) {
        if (IKOSA) return;
        int 거리 = gusimbuza_igishya_ikintu - ishami;
        if (거리 < -32768 || 거리 > 32767 || ishami < 0 || ishami + 2 >= 코드크기) { kudakora_agaciro("invalid branch"); return; }
        코드[ishami + 1] = 거리 >> 8 & 255; 코드[ishami + 2] = 거리 & 255;
    }
    static void 비교값(int Icyo_wifuza) {
        int 참 = ishami(Icyo_wifuza); 내보내기(3); int 끝 = ishami(167);
        Ihuza_agaciro(참, 코드크기); 내보내기(4); Ihuza_agaciro(끝, 코드크기);
    }
    static int imiterere_agaciro() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        kudakora_agaciro("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void kongeraho_imiterere(int 형) {
        if (형 == 0) 글추가('V');
        if (형 == 1) 글추가('I');
        if (형 == 2) 글추가('Z');
        if (형 == 3) 말추가("Ljava/lang/String;");
        if (형 == 4) 말추가("[Ljava/lang/String;");
        if (형 == 5) 글추가('C');
        if (형 == 6) 말추가("Ljava/io/FileInputStream;");
        if (형 == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Inzira_agaciro_icyinjizwa 본문은 gucumbikira javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("Ikinyarwanda");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("ARRAY_Store_kudakora") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        kudakora_agaciro("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Ijambo_agaciro(위치, "Ikinyarwanda")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) kudakora_agaciro("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); icyiciro_tike = indanga_agaciro();
        icyiciro_kidahinduka = Indanga(7, tike_kidahinduka(icyiciro_tike), 0);
        부모상수 = Indanga(7, Ijambo_kidahinduka("java/lang/Object"), 0); 코드상수 = Ijambo_kidahinduka("Code"); 요구('{');
        while (!IKOSA && 종류() != '}') {
            if (함수수 == 32) { kudakora_agaciro("too many methods"); break; }
            int kwinjira_icyinjizwa = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int FUNCTION_agaciro = 함수수++;
            uburyo_kwinjira[FUNCTION_agaciro] = kwinjira_icyinjizwa | 8;
            함수반환[FUNCTION_agaciro] = imiterere_agaciro(); uburyo_icyinjizwa_izina[FUNCTION_agaciro] = indanga_agaciro(); 요구('(');
            for (int 앞 = 0; 앞 < FUNCTION_agaciro; 앞++) if (이름같음(uburyo_icyinjizwa_izina[앞], uburyo_icyinjizwa_izina[FUNCTION_agaciro])) kudakora_agaciro("duplicate method (overloading unsupported)");
            while (!IKOSA && 종류() != ')') {
                int 수 = 함수인수수[FUNCTION_agaciro];
                if (수 == 16) { kudakora_agaciro("too many parameters"); break; }
                int 형 = imiterere_agaciro(); if (형 == 0) kudakora_agaciro("void parameter");
                함수인수형[FUNCTION_agaciro * 16 + 수] = 형; uburyo_ingingo_izina[FUNCTION_agaciro * 16 + 수] = indanga_agaciro();
                함수인수수[FUNCTION_agaciro]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!IKOSA && 받기(','));
            }
            함수본문[FUNCTION_agaciro] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) kudakora_agaciro("unclosed method body");
            uburyo_kurangiza[FUNCTION_agaciro] = 위치;
            uburyo_izina_kidahinduka[FUNCTION_agaciro] = tike_kidahinduka(uburyo_icyinjizwa_izina[FUNCTION_agaciro]);
            inyuguti_uburebure = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[FUNCTION_agaciro]; 수++) kongeraho_imiterere(함수인수형[FUNCTION_agaciro * 16 + 수]);
            글추가(')'); kongeraho_imiterere(함수반환[FUNCTION_agaciro]); 함수서술[FUNCTION_agaciro] = inyuguti_kidahinduka();
        }
        요구('}'); if (위치 != 토큰수) kudakora_agaciro("extra input after class");
    }
    static int gushaka_mu_gace(int Izina) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(mu_gace_izina[수], Izina)) return 수;
        kudakora_agaciro("unknown variable"); return 0;
    }
    static int kongeraho_mu_gace(int Izina, int 형) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(mu_gace_izina[수], Izina)) kudakora_agaciro("duplicate local variable");
        if (지역수 == 128) { kudakora_agaciro("too many locals"); return 0; }
        mu_gace_izina[지역수] = Izina; 지역형[지역수] = 형; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean 정수형(int 형) { return 형 == 1 || 형 == 5; }
    static void 지역읽기(int 수) { 내보내기(지역형[수] <= 2 || 지역형[수] == 5 ? 21 : 25); 내보내기(수); }
    static void kwandika_mu_gace(int 수) { 내보내기(지역형[수] <= 2 || 지역형[수] == 5 ? 54 : 58); 내보내기(수); }
    static void 형확인(int nyakuri_amakurushingiro, int 기대) { if (nyakuri_amakurushingiro != 기대 && !(nyakuri_amakurushingiro == 5 && 기대 == 1)) kudakora_agaciro("type mismatch"); }
    static void 문자읽기(int tike_agaciro) {
        inyuguti_uburebure = 0; int ihuriro = 토큰위치[tike_agaciro] + 1, 끝 = 토큰위치[tike_agaciro] + tike_uburebure[tike_agaciro] - 1;
        while (ihuriro < 끝 && !IKOSA) {
            int agaciro = Inkomoko[ihuriro++];
            if (agaciro == '\\') {
                if (ihuriro == 끝) { kudakora_agaciro("invalid escape"); break; }
                agaciro = Inkomoko[ihuriro++];
                if (agaciro == 'n') agaciro = 10;
                else if (agaciro == 'r') agaciro = 13;
                else if (agaciro == 't') agaciro = 9;
                else if (agaciro == 'b') agaciro = 8;
                else if (agaciro == 'f') agaciro = 12;
                else if (agaciro != '\\' && agaciro != '"' && agaciro != '\'') kudakora_agaciro("unsupported escape");
            }
            글추가(agaciro);
        }
    }
    static int gusesengura_umubare_wuzuye(int tike_agaciro, boolean 음수) {
        if (tike_uburebure[tike_agaciro] > 1 && Inkomoko[토큰위치[tike_agaciro]] == '0') kudakora_agaciro("octal literals unsupported");
        int agaciro = 0;
        for (int 수 = 0; 수 < tike_uburebure[tike_agaciro]; 수++) {
            int umubare_igice = Inkomoko[토큰위치[tike_agaciro] + 수] - '0';
            if (agaciro < -214748364 || agaciro == -214748364 && umubare_igice > (음수 ? 8 : 7)) kudakora_agaciro("integer literal out of range");
            agaciro = agaciro * 10 - umubare_igice;
        }
        return 음수 ? agaciro : -agaciro;
    }
    static int 기본식() {
        if (말받기("new")) {
            int 형 = imiterere_agaciro();
            if (형 != 6 && 형 != 7) { kudakora_agaciro("only file streams supported by new in source"); return 0; }
            String nyirayo_agaciro = 형 == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Icyo_wifuza(187, Indanga(7, Ijambo_kidahinduka(nyirayo_agaciro), 0)); 내보내기(89);
            요구('('); 형확인(imvugo_agaciro(), 3); boolean 이어 = false;
            if (받기(',')) { if (형 != 7) kudakora_agaciro("input stream constructor arguments"); 형확인(imvugo_agaciro(), 2); 이어 = true; }
            요구(')');
            Icyo_wifuza(183, 외부참조(10, nyirayo_agaciro, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return 형;
        }
        if (받기('(')) { int 형 = imvugo_agaciro(); 요구(')'); return 형; }
        if (종류() == 257) { 수상수(gusesengura_umubare_wuzuye(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); Icyo_wifuza(19, Indanga(8, inyuguti_kidahinduka(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (inyuguti_uburebure != 1) kudakora_agaciro("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("Ikinyarwanda")) {
            요구('.'); 말요구("자체"); 요구('.');
            String nyirayo_agaciro = "", uburyo_agaciro = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                nyirayo_agaciro = "Ikinyarwanda/자체/출력"; 요구('.');
                if (말받기("kwandika_umurongo")) { uburyo_agaciro = "kwandika_umurongo"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("kwandika")) { uburyo_agaciro = "kwandika"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { uburyo_agaciro = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else kudakora_agaciro("unknown Korean output method");
            } else if (말받기("문자")) {
                nyirayo_agaciro = "Ikinyarwanda/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("uburebure_agaciro")) { uburyo_agaciro = "uburebure_agaciro"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { uburyo_agaciro = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("gusesengura_umubare_wuzuye")) { uburyo_agaciro = "gusesengura_umubare_wuzuye"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("kwandika_umubare_wuzuye_agaciro")) { uburyo_agaciro = "kwandika_umubare_wuzuye_agaciro"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { uburyo_agaciro = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("komeka_SMS")) { uburyo_agaciro = "komeka_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("gukata_agaciro")) { uburyo_agaciro = "gukata_agaciro"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else kudakora_agaciro("unknown Korean text method");
            } else if (말받기("Idosiye")) {
                nyirayo_agaciro = "Ikinyarwanda/자체/Idosiye"; 요구('.'); 가 = 3;
                if (말받기("읽기")) { uburyo_agaciro = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("kwandika")) { uburyo_agaciro = "kwandika"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else kudakora_agaciro("unknown Korean file method");
            } else if (말받기("화면")) {
                nyirayo_agaciro = "Ikinyarwanda/자체/화면"; 요구('.');
                if (말받기("너비")) { uburyo_agaciro = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { uburyo_agaciro = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { uburyo_agaciro = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { uburyo_agaciro = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { uburyo_agaciro = "기다리기"; 서술 = "()V"; }
                else kudakora_agaciro("unknown Korean framebuffer method");
            } else kudakora_agaciro("unsupported Korean library class");
            요구('('); if (가 != 0) 형확인(imvugo_agaciro(), 가);
            if (나 != 0) { 요구(','); 형확인(imvugo_agaciro(), 나); }
            if (다 != 0) { 요구(','); 형확인(imvugo_agaciro(), 다); }
            if (라 != 0) { 요구(','); 형확인(imvugo_agaciro(), 라); }
            if (마 != 0) { 요구(','); 형확인(imvugo_agaciro(), 마); }
            요구(')'); Icyo_wifuza(184, 외부참조(10, nyirayo_agaciro, uburyo_agaciro, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); 형확인(imvugo_agaciro(), 3); 요구(')');
            Icyo_wifuza(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Izina = indanga_agaciro();
        if (받기('(')) {
            int FUNCTION_agaciro = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Izina, uburyo_icyinjizwa_izina[수])) FUNCTION_agaciro = 수;
            if (FUNCTION_agaciro < 0) { kudakora_agaciro("unknown static method"); return 0; }
            int 수 = 0;
            while (!IKOSA && 종류() != ')') {
                if (수 >= 함수인수수[FUNCTION_agaciro]) { kudakora_agaciro("too many arguments"); break; }
                형확인(imvugo_agaciro(), 함수인수형[FUNCTION_agaciro * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[FUNCTION_agaciro]) kudakora_agaciro("argument count mismatch");
            Icyo_wifuza(184, Indanga(10, icyiciro_kidahinduka, Indanga(12, uburyo_izina_kidahinduka[FUNCTION_agaciro], 함수서술[FUNCTION_agaciro])));
            return 함수반환[FUNCTION_agaciro];
        }
        int mu_gace_urwego = gushaka_mu_gace(Izina), 형 = 지역형[mu_gace_urwego]; 지역읽기(mu_gace_urwego);
        while (!IKOSA) {
            if (받기('[')) { 형확인(형, 4); 형확인(imvugo_agaciro(), 1); 요구(']'); 내보내기(50); 형 = 3; }
            else if (받기('.')) {
                if (형 == 6 || 형 == 7) {
                    String nyirayo_agaciro = 형 == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); Icyo_wifuza(182, 외부참조(10, nyirayo_agaciro, "close", "()V")); 형 = 0; }
                    else if (형 == 6 && 말받기("read")) { 요구('('); 요구(')'); Icyo_wifuza(182, 외부참조(10, nyirayo_agaciro, "read", "()I")); 형 = 1; }
                    else if (형 == 7 && 말받기("write")) { 요구('('); 형확인(imvugo_agaciro(), 1); 요구(')'); Icyo_wifuza(182, 외부참조(10, nyirayo_agaciro, "write", "(I)V")); 형 = 0; }
                    else { kudakora_agaciro("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (형 == 4) { 내보내기(190); 형 = 1; }
                else { 형확인(형, 3); 요구('('); 요구(')'); Icyo_wifuza(182, 외부참조(10, "java/lang/String", "length", "()I")); 형 = 1; }
            } else break;
        }
        return 형;
    }
    static int 단항() {
        if (++식깊이 > 64) { kudakora_agaciro("expression nesting too deep"); 식깊이--; return 0; }
        int 형;
        if (받기('!')) { 형확인(단항(), 2); 비교값(153); 형 = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(gusesengura_umubare_wuzuye(위치++, true));
            else { 형확인(단항(), 1); 내보내기(116); }
            형 = 1;
        } else if (받기('+')) { 형확인(단항(), 1); 형 = 1; }
        else 형 = 기본식();
        식깊이--; return 형;
    }
    static int 곱식() {
        int 형 = 단항();
        while (!IKOSA && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int gusobeka_agaciro = 종류(); 위치++; 형확인(형, 1); 형확인(단항(), 1);
            내보내기(gusobeka_agaciro == '*' ? 104 : gusobeka_agaciro == '/' ? 108 : 112); 형 = 1;
        }
        return 형;
    }
    static int 합식() {
        int 형 = 곱식();
        while (!IKOSA && (종류() == '+' || 종류() == '-')) {
            int gusobeka_agaciro = 종류(); 위치++; int 경계 = 코드크기, 뒤형 = 곱식();
            if (gusobeka_agaciro == '+' && (형 == 3 || 뒤형 == 3)) { 결합(경계, 형, 뒤형); 형 = 3; }
            else { 형확인(형, 1); 형확인(뒤형, 1); 내보내기(gusobeka_agaciro == '+' ? 96 : 100); 형 = 1; }
        }
        return 형;
    }
    static int 붙임참조(int 형) {
        if (형 != 1 && 형 != 2 && 형 != 3 && 형 != 5) kudakora_agaciro("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", 형 == 1 ? "(I)Ljava/lang/StringBuilder;"
            : 형 == 2 ? "(Z)Ljava/lang/StringBuilder;" : 형 == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int 뒤형) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 imvugo_agaciro 내부의 Mugenzi_agaciro ishami 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        Icyo_wifuza(187, Indanga(7, Ijambo_kidahinduka("java/lang/StringBuilder"), 0)); 내보내기(89);
        Icyo_wifuza(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Icyo_wifuza(182, 붙임참조(앞형));
        if (IKOSA) return;
        int uburebure_agaciro = 코드크기 - 끝;
        for (int 수 = 0; 수 < uburebure_agaciro; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + uburebure_agaciro] = 코드[수];
        for (int 수 = 0; 수 < uburebure_agaciro; 수++) 코드[경계 + 수] = 삽입코드[수];
        Icyo_wifuza(182, 붙임참조(뒤형)); Icyo_wifuza(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int 형 = 합식();
        while (!IKOSA && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int gusobeka_agaciro = 종류(); 위치++; 형확인(형, 1); 형확인(합식(), 1);
            비교값(gusobeka_agaciro == '<' ? 161 : gusobeka_agaciro == '>' ? 163 : gusobeka_agaciro == 302 ? 164 : 162); 형 = 2;
        }
        return 형;
    }
    static int 동등식() {
        int 형 = 비교식();
        while (!IKOSA && (종류() == 300 || 종류() == 301)) {
            int gusobeka_agaciro = 종류(); 위치++; int 뒤형 = 비교식();
            if (형 == 0 || 뒤형 == 0) kudakora_agaciro("void expression");
            if (!(정수형(형) && 정수형(뒤형))) 형확인(뒤형, 형);
            비교값((형 <= 2 || 형 == 5 ? 159 : 165) + (gusobeka_agaciro == 301 ? 1 : 0)); 형 = 2;
        }
        return 형;
    }
    static int 논리곱() {
        int 형 = 동등식();
        while (!IKOSA && 받기(304)) {
            형확인(형, 2); int 가 = ishami(153); 형확인(동등식(), 2); int 나 = ishami(153);
            내보내기(4); int 끝 = ishami(167); Ihuza_agaciro(가, 코드크기); Ihuza_agaciro(나, 코드크기); 내보내기(3); Ihuza_agaciro(끝, 코드크기); 형 = 2;
        }
        return 형;
    }
    static int imvugo_agaciro() {
        int 형 = 논리곱();
        while (!IKOSA && 받기(305)) {
            형확인(형, 2); int 가 = ishami(154); 형확인(논리곱(), 2); int 나 = ishami(154);
            내보내기(3); int 끝 = ishami(167); Ihuza_agaciro(가, 코드크기); Ihuza_agaciro(나, 코드크기); 내보내기(4); Ihuza_agaciro(끝, 코드크기); 형 = 2;
        }
        return 형;
    }
    static void umukoro_agaciro(boolean 선언허용) {
        if (Ijambo_agaciro(위치, "int") || Ijambo_agaciro(위치, "boolean") || Ijambo_agaciro(위치, "String") || Ijambo_agaciro(위치, "char")
            || Ijambo_agaciro(위치, "FileInputStream") || Ijambo_agaciro(위치, "FileOutputStream")) {
            if (!선언허용) kudakora_agaciro("declaration not allowed here");
            int 형 = imiterere_agaciro(), Izina = indanga_agaciro(); 요구('='); 형확인(imvugo_agaciro(), 형);
            kwandika_mu_gace(kongeraho_mu_gace(Izina, 형)); return;
        }
        int Izina = indanga_agaciro(), mu_gace_urwego = gushaka_mu_gace(Izina);
        if (받기('=')) { 형확인(imvugo_agaciro(), 지역형[mu_gace_urwego]); kwandika_mu_gace(mu_gace_urwego); }
        else if (종류() >= 308 && 종류() <= 312) {
            int gusobeka_agaciro = 종류(); 위치++; 지역읽기(mu_gace_urwego); int 경계 = 코드크기, 뒤형 = imvugo_agaciro();
            if (gusobeka_agaciro == 308 && 지역형[mu_gace_urwego] == 3) 결합(경계, 3, 뒤형);
            else {
                형확인(지역형[mu_gace_urwego], 1); 형확인(뒤형, 1);
                내보내기(gusobeka_agaciro == 308 ? 96 : gusobeka_agaciro == 309 ? 100 : gusobeka_agaciro == 310 ? 104 : gusobeka_agaciro == 311 ? 108 : 112);
                if (지역형[mu_gace_urwego] == 5) 내보내기(146);
            }
            kwandika_mu_gace(mu_gace_urwego);
        }
        else if (종류() == 306 || 종류() == 307) {
            형확인(지역형[mu_gace_urwego], 1); 내보내기(132); 내보내기(mu_gace_urwego); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (지역형[mu_gace_urwego] == 5) { 지역읽기(mu_gace_urwego); 내보내기(146); kwandika_mu_gace(mu_gace_urwego); }
        } else kudakora_agaciro("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Icyo_wifuza(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean irimo_ubusa_ingingo = 종류() == ')';
        int 형 = irimo_ubusa_ingingo ? 0 : imvugo_agaciro(); 요구(')'); 요구(';');
        String 서술 = 형 == 0 ? "()V" : 형 == 1 ? "(I)V" : 형 == 2 ? "(Z)V" : 형 == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (형 == 4 || 형 >= 6 || 형 == 0 && (!줄바꿈 || !irimo_ubusa_ingingo)) kudakora_agaciro("unsupported print argument");
        Icyo_wifuza(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean ibwiriza_agaciro() {
        if (IKOSA) return false;
        if (깊이 > 32) { kudakora_agaciro("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!IKOSA && 종류() != '}') { if (반환) kudakora_agaciro("unreachable statement"); 반환 = ibwiriza_agaciro(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int 형 = 종류() == ';' ? 0 : imvugo_agaciro(); 형확인(형, 함수반환[현재함수]); 요구(';');
            내보내기(형 == 0 ? 177 : 형 <= 2 || 형 == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); 형확인(imvugo_agaciro(), 2); 요구(')'); int 거짓 = ishami(153);
            깊이++; boolean 가 = icunga_ibwiriza(); 깊이--;
            if (말받기("else")) { int 끝 = ishami(167); Ihuza_agaciro(거짓, 코드크기); 깊이++; boolean 나 = icunga_ibwiriza(); 깊이--; Ihuza_agaciro(끝, 코드크기); return 가 && 나; }
            Ihuza_agaciro(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int ihuriro = 코드크기; 요구('('); 형확인(imvugo_agaciro(), 2); 요구(')'); int 끝 = ishami(153);
            깊이++; icunga_ibwiriza(); 깊이--; Ihuza_agaciro(ishami(167), ihuriro); Ihuza_agaciro(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') umukoro_agaciro(true); 요구(';');
            int icyangombwa = 코드크기; if (종류() == ';') 내보내기(4); else 형확인(imvugo_agaciro(), 2); 요구(';');
            int 끝 = ishami(153), igihimba_cy_umwandiko = ishami(167), kugaruraho = 코드크기;
            if (종류() != ')') umukoro_agaciro(false); 요구(')'); Ihuza_agaciro(ishami(167), icyangombwa); Ihuza_agaciro(igihimba_cy_umwandiko, 코드크기);
            icunga_ibwiriza(); Ihuza_agaciro(ishami(167), kugaruraho); Ihuza_agaciro(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Ijambo_agaciro(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int 형 = imvugo_agaciro(); if (형 != 0) 내보내기(87); 요구(';'); return false;
        }
        umukoro_agaciro(true); 요구(';'); return false;
    }
    static boolean icunga_ibwiriza() {
        if (Ijambo_agaciro(위치, "int") || Ijambo_agaciro(위치, "boolean") || Ijambo_agaciro(위치, "char") || Ijambo_agaciro(위치, "String")
            || Ijambo_agaciro(위치, "FileInputStream") || Ijambo_agaciro(위치, "FileOutputStream")) kudakora_agaciro("local declaration requires braces");
        return ibwiriza_agaciro();
    }
    static void 출바(int agaciro) { if (출력크기 == 출력.length) kudakora_agaciro("class file too large"); else 출력[출력크기++] = agaciro & 255; }
    static void 출짧(int agaciro) { 출바(agaciro >> 8); 출바(agaciro); }
    static void 출정(int agaciro) { 출짧(agaciro >>> 16); 출짧(agaciro); }
    static void kwandika_icyiciro() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < kidahinduka_ingano; 수++) 출바(kidahinduka_agaciro[수]);
        출짧(0x21); 출짧(icyiciro_kidahinduka); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(uburyo_kwinjira[수]); 출짧(uburyo_izina_kidahinduka[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + uburyo_uburebure[수]); 출짧(128); 출짧(함수지역[수]); 출정(uburyo_uburebure[수]);
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < uburyo_uburebure[수]; umwanya_icyinjizwa++) 출바(코드[함수코드[수] + umwanya_icyinjizwa]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int ihuriro() {
        if (ukoresha.인수개수() == 1 && 자바도구.같음(ukoresha.인수(0), "-version")) {
            ukoresha.kwandika("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (ukoresha.인수개수() != 1) { ukoresha.kwandika("Usage: javac FILE.java\n"); return 2; }
        int izina_ingano = 자바도구.Izina(dosiye_izina_SMS, ukoresha.인수(0));
        if (izina_ingano < 6 || izina_ingano > 62 || dosiye_izina_SMS[izina_ingano - 5] != '.' || dosiye_izina_SMS[izina_ingano - 4] != 'j'
            || dosiye_izina_SMS[izina_ingano - 3] != 'a' || dosiye_izina_SMS[izina_ingano - 2] != 'v' || dosiye_izina_SMS[izina_ingano - 1] != 'a') {
            ukoresha.kwandika("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        inkomoko_ingano = ukoresha.파일읽기(dosiye_izina_SMS, Inkomoko);
        if (inkomoko_ingano < 0) { ukoresha.kwandika("javac: cannot read source: "); 자바도구.수쓰기(inkomoko_ingano); ukoresha.kwandika_inyuguti_agaciro(10); return 1; }
        inkomoko_ingano = 자바도구.원문해독(Inkomoko, inkomoko_ingano);
        if (inkomoko_ingano < 0) { ukoresha.kwandika("javac error: invalid UTF-8 source\n"); return 1; }
        gukata_agaciro(); if (!IKOSA) 선언읽기();
        if (!IKOSA) {
            if (tike_uburebure[icyiciro_tike] != izina_ingano - 5) kudakora_agaciro("class name must match file name");
            for (int 수 = 0; 수 < izina_ingano - 5; 수++) if (Inkomoko[토큰위치[icyiciro_tike] + 수] != dosiye_izina_SMS[수]) kudakora_agaciro("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !IKOSA; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) kongeraho_mu_gace(uburyo_ingingo_izina[현재함수 * 16 + 수], 함수인수형[현재함수 * 16 + 수]);
            boolean 반환 = ibwiriza_agaciro();
            if (!반환 && 함수반환[현재함수] != 0) kudakora_agaciro("missing return");
            // ishami 뒤의 합류 지점은 반드시 nyakuri_amakurushingiro 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean umubare_wuzuye = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(umubare_wuzuye ? 3 : 1); 내보내기(umubare_wuzuye ? 172 : 176); }
            if (위치 != uburyo_kurangiza[현재함수]) kudakora_agaciro("invalid method body");
            함수지역[현재함수] = 지역수; uburyo_uburebure[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (IKOSA) return 1;
        kwandika_icyiciro(); if (IKOSA) return 1;
        dosiye_izina_SMS[izina_ingano - 4] = 'c'; dosiye_izina_SMS[izina_ingano - 3] = 'l'; dosiye_izina_SMS[izina_ingano - 2] = 'a';
        dosiye_izina_SMS[izina_ingano - 1] = 's'; dosiye_izina_SMS[izina_ingano] = 's'; dosiye_izina_SMS[izina_ingano + 1] = 0;
        int 결과 = ukoresha.kwandika_dosiye(dosiye_izina_SMS, 출력, 출력크기);
        if (결과 < 0) { ukoresha.kwandika("javac: cannot save class: "); 자바도구.수쓰기(결과); ukoresha.kwandika_inyuguti_agaciro(10); return 1; }
        ukoresha.kwandika("Compiled: "); for (int 수 = 0; dosiye_izina_SMS[수] != 0; 수++) ukoresha.kwandika_inyuguti_agaciro(dosiye_izina_SMS[수]);
        ukoresha.kwandika(" (JVM class version 49)\n"); return 0;
    }
}
