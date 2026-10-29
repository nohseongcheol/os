// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java pivviujuq_attavigiit -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] pivviujuq = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], 토큰길이 = new int[2048];
    static int[] surragunnangittuq_atuutilik = new int[4096], 상수위치 = new int[512];
    static int[] 문자 = new int[512], ini_atiq_titiqqaq = new int[64];
    static int[] 삽입코드 = new int[16];
    static int pivviujuq_anininga, 토큰수, 위치, 코드크기, surragunnangittuq_anininga, 상수수 = 1, 출력크기, immikkuuqtuq_takininga;
    static boolean tammarniq;
    static int 클래스토큰, naliannuungavik_surragunnangittuq, 부모상수, 코드상수;
    static int[] 함수이름 = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] 함수인수이름 = new int[512], 함수인수형 = new int[512];
    static int[] 함수본문 = new int[32], 함수끝 = new int[32], 함수코드 = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], 함수명상수 = new int[32], 함수서술 = new int[32];
    static int[] 함수권한 = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] tamaani_atiq = new int[128], tamaani_qanuittuuninga = new int[128], 지역깊이 = new int[128];

    static void itigaqtuq_atuutilik(String 이유) {
        if (!tammarniq) {
            atuqtuq.titiraq("javac error: "); atuqtuq.titiraq(이유);
            atuqtuq.titiraq(" at line ");
            int titikutaak = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : pivviujuq_anininga;
            for (int 수 = 0; 수 < 끝; 수++) if (pivviujuq[수] == 10) titikutaak++;
            자바도구.수쓰기(titikutaak); atuqtuq.titiraq_immikkuuqtuq_atuutilik(10);
        }
        tammarniq = true;
    }
    static boolean immikkuuqtuq_atuutilik(int atuutilik) { return 문자이름규칙.첫글자(atuutilik); }
    static boolean 숫자(int atuutilik) { return atuutilik >= '0' && atuutilik <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || 토큰길이[가] != 토큰길이[나]) return false;
        for (int 수 = 0; 수 < 토큰길이[가]; 수++) if (pivviujuq[토큰위치[가] + 수] != pivviujuq[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean 단어(int 토큰, String 말) {
        if (토큰 < 0 || 토큰 >= 토큰수 || 토큰길이[토큰] != 말.length()) return false;
        for (int 수 = 0; 수 < 말.length(); 수++) if (pivviujuq[토큰위치[토큰] + 수] != 말.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int atuutilik) { if (종류() != atuutilik) return false; 위치++; return true; }
    static void 요구(int atuutilik) { if (!받기(atuutilik)) itigaqtuq_atuutilik("unexpected token"); }
    static boolean 말받기(String 말) { if (!단어(위치, 말)) return false; 위치++; return true; }
    static void 말요구(String 말) { if (!말받기(말)) itigaqtuq_atuutilik(말); }
    static int 식별자() {
        int 결과 = 위치;
        if (종류() != 256) itigaqtuq_atuutilik("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int 시작 = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - 시작 == 토큰길이[결과];
                for (int 칸 = 시작; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != pivviujuq[토큰위치[결과] + 칸 - 시작]) 같음 = false;
                if (같음) itigaqtuq_atuutilik("reserved word cannot be an identifier");
                시작 = 수 + 1;
            }
        }
        return 결과;
    }
    static void nakalli_atuutilik() {
        int 수 = 0;
        while (수 < pivviujuq_anininga && !tammarniq) {
            int atuutilik = pivviujuq[수], 시작 = 수, 종류 = atuutilik;
            if (atuutilik == 32 || atuutilik == 9 || atuutilik == 10 || atuutilik == 13) { 수++; continue; }
            if (atuutilik == '/' && 수 + 1 < pivviujuq_anininga && pivviujuq[수 + 1] == '/') {
                while (수 < pivviujuq_anininga && pivviujuq[수] != 10) 수++;
                continue;
            }
            if (atuutilik == '/' && 수 + 1 < pivviujuq_anininga && pivviujuq[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < pivviujuq_anininga && !(pivviujuq[수] == '*' && pivviujuq[수 + 1] == '/')) 수++;
                if (수 + 1 >= pivviujuq_anininga) { itigaqtuq_atuutilik("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (immikkuuqtuq_atuutilik(atuutilik)) { 종류 = 256; while (수 < pivviujuq_anininga && 문자이름규칙.이어진글자(pivviujuq[수])) 수++; }
            else if (숫자(atuutilik)) { 종류 = 257; while (수 < pivviujuq_anininga && 숫자(pivviujuq[수])) 수++; }
            else if (atuutilik == '"' || atuutilik == '\'') {
                종류 = atuutilik == '"' ? 258 : 259; 수++;
                while (수 < pivviujuq_anininga && pivviujuq[수] != atuutilik && pivviujuq[수] != 10 && pivviujuq[수] != 13) {
                    if (pivviujuq[수] == '\\') 수++;
                    수++;
                }
                if (수 >= pivviujuq_anininga || pivviujuq[수] != atuutilik) { itigaqtuq_atuutilik("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < pivviujuq_anininga) {
                    int 다음 = pivviujuq[수];
                    if (atuutilik == '=' && 다음 == '=') 종류 = 300;
                    if (atuutilik == '!' && 다음 == '=') 종류 = 301;
                    if (atuutilik == '<' && 다음 == '=') 종류 = 302;
                    if (atuutilik == '>' && 다음 == '=') 종류 = 303;
                    if (atuutilik == '&' && 다음 == '&') 종류 = 304;
                    if (atuutilik == '|' && 다음 == '|') 종류 = 305;
                    if (atuutilik == '+' && 다음 == '+') 종류 = 306;
                    if (atuutilik == '-' && 다음 == '-') 종류 = 307;
                    if (atuutilik == '+' && 다음 == '=') 종류 = 308;
                    if (atuutilik == '-' && 다음 == '=') 종류 = 309;
                    if (atuutilik == '*' && 다음 == '=') 종류 = 310;
                    if (atuutilik == '/' && 다음 == '=') 종류 = 311;
                    if (atuutilik == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { itigaqtuq_atuutilik("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = 시작; 토큰길이[토큰수++] = 수 - 시작;
        }
    }
    static void titiraq_surragunnangittuq_byte(int atuutilik) {
        if (surragunnangittuq_anininga == surragunnangittuq_atuutilik.length) { itigaqtuq_atuutilik("constant pool too large"); return; }
        surragunnangittuq_atuutilik[surragunnangittuq_anininga++] = atuutilik & 255;
    }
    static void 상짧(int atuutilik) { titiraq_surragunnangittuq_byte(atuutilik >> 8); titiraq_surragunnangittuq_byte(atuutilik); }
    static int 상등록(int 시작) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = 상수위치[수], takininga_atuutilik = (수 + 1 < 상수수 ? 상수위치[수 + 1] : 시작) - 앞;
            if (takininga_atuutilik != surragunnangittuq_anininga - 시작) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < takininga_atuutilik; 칸++) if (surragunnangittuq_atuutilik[앞 + 칸] != surragunnangittuq_atuutilik[시작 + 칸]) 같음 = false;
            if (같음) { surragunnangittuq_anininga = 시작; return 수; }
        }
        if (상수수 == 상수위치.length) { itigaqtuq_atuutilik("too many constants"); return 0; }
        상수위치[상수수] = 시작;
        return 상수수++;
    }
    static void 글추가(int atuutilik) {
        if (immikkuuqtuq_takininga == 문자.length) { itigaqtuq_atuutilik("text too long"); return; }
        문자[immikkuuqtuq_takininga++] = atuutilik;
    }
    static void 말추가(String 말) { for (int 수 = 0; 수 < 말.length(); 수++) 글추가(말.charAt(수)); }
    static int immikkuuqtuq_surragunnangittuq() {
        int 시작 = surragunnangittuq_anininga; titiraq_surragunnangittuq_byte(1); 상짧(0);
        for (int 수 = 0; 수 < immikkuuqtuq_takininga; 수++) {
            int atuutilik = 문자[수];
            if (atuutilik > 0 && atuutilik < 128) titiraq_surragunnangittuq_byte(atuutilik);
            else if (atuutilik < 2048) { titiraq_surragunnangittuq_byte(192 | atuutilik >> 6); titiraq_surragunnangittuq_byte(128 | atuutilik & 63); }
            else { titiraq_surragunnangittuq_byte(224 | atuutilik >> 12); titiraq_surragunnangittuq_byte(128 | atuutilik >> 6 & 63); titiraq_surragunnangittuq_byte(128 | atuutilik & 63); }
        }
        if (tammarniq) return 0;
        int takininga_atuutilik = surragunnangittuq_anininga - 시작 - 3;
        surragunnangittuq_atuutilik[시작 + 1] = takininga_atuutilik >> 8; surragunnangittuq_atuutilik[시작 + 2] = takininga_atuutilik & 255;
        return 상등록(시작);
    }
    static int 말상수(String 말) { immikkuuqtuq_takininga = 0; 말추가(말); return immikkuuqtuq_surragunnangittuq(); }
    static int 토큰상수(int 토큰) {
        immikkuuqtuq_takininga = 0;
        for (int 수 = 0; 수 < 토큰길이[토큰]; 수++) 글추가(pivviujuq[토큰위치[토큰] + 수]);
        return immikkuuqtuq_surragunnangittuq();
    }
    static int 참조(int 종류, int 가, int 나) {
        int 시작 = surragunnangittuq_anininga; titiraq_surragunnangittuq_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return 상등록(시작);
    }
    static int 외부참조(int 종류, String 소유, String atiq, String 서술) {
        int 주인 = 참조(7, 말상수(소유), 0);
        int 이름수 = 말상수(atiq), 형식수 = 말상수(서술);
        return 참조(종류, 주인, 참조(12, 이름수, 형식수));
    }
    static void 내보내기(int atuutilik) {
        if (코드크기 == 코드.length) { itigaqtuq_atuutilik("bytecode too large"); return; }
        코드[코드크기++] = atuutilik & 255;
    }
    static void piqujijjut(int atuutilik, int 인수) { 내보내기(atuutilik); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int atuutilik) {
        if (atuutilik >= -1 && atuutilik <= 5) { 내보내기(atuutilik + 3); return; }
        int 시작 = surragunnangittuq_anininga; titiraq_surragunnangittuq_byte(3); 상짧(atuutilik >>> 16); 상짧(atuutilik);
        piqujijjut(19, 상등록(시작));
    }
    static int avalangajuq(int piqujijjut) { int 결과 = 코드크기; piqujijjut(piqujijjut, 0); return 결과; }
    static void kasurvik_atuutilik(int avalangajuq, int turaagaq_kisu) {
        if (tammarniq) return;
        int 거리 = turaagaq_kisu - avalangajuq;
        if (거리 < -32768 || 거리 > 32767 || avalangajuq < 0 || avalangajuq + 2 >= 코드크기) { itigaqtuq_atuutilik("invalid branch"); return; }
        코드[avalangajuq + 1] = 거리 >> 8 & 255; 코드[avalangajuq + 2] = 거리 & 255;
    }
    static void 비교값(int piqujijjut) {
        int 참 = avalangajuq(piqujijjut); 내보내기(3); int 끝 = avalangajuq(167);
        kasurvik_atuutilik(참, 코드크기); 내보내기(4); kasurvik_atuutilik(끝, 코드크기);
    }
    static int aaqqisurli_atuutilik() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        itigaqtuq_atuutilik("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void ilali_aaqqisurli(int qanuittuuninga_atuutilik) {
        if (qanuittuuninga_atuutilik == 0) 글추가('V');
        if (qanuittuuninga_atuutilik == 1) 글추가('I');
        if (qanuittuuninga_atuutilik == 2) 글추가('Z');
        if (qanuittuuninga_atuutilik == 3) 말추가("Ljava/lang/String;");
        if (qanuittuuninga_atuutilik == 4) 말추가("[Ljava/lang/String;");
        if (qanuittuuninga_atuutilik == 5) 글추가('C');
        if (qanuittuuninga_atuutilik == 6) 말추가("Ljava/io/FileInputStream;");
        if (qanuittuuninga_atuutilik == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Pivallianiq_atuutilik_Iliniku 본문은 tuttarvik javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("array_tuqqurli_itigaqtuq") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        itigaqtuq_atuutilik("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (단어(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) itigaqtuq_atuutilik("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); 클래스토큰 = 식별자();
        naliannuungavik_surragunnangittuq = 참조(7, 토큰상수(클래스토큰), 0);
        부모상수 = 참조(7, 말상수("java/lang/Object"), 0); 코드상수 = 말상수("Code"); 요구('{');
        while (!tammarniq && 종류() != '}') {
            if (함수수 == 32) { itigaqtuq_atuutilik("too many methods"); break; }
            int pili_Iliniku = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int sugiakkannirut_atuutilik = 함수수++;
            함수권한[sugiakkannirut_atuutilik] = pili_Iliniku | 8;
            함수반환[sugiakkannirut_atuutilik] = aaqqisurli_atuutilik(); 함수이름[sugiakkannirut_atuutilik] = 식별자(); 요구('(');
            for (int 앞 = 0; 앞 < sugiakkannirut_atuutilik; 앞++) if (이름같음(함수이름[앞], 함수이름[sugiakkannirut_atuutilik])) itigaqtuq_atuutilik("duplicate method (overloading unsupported)");
            while (!tammarniq && 종류() != ')') {
                int 수 = 함수인수수[sugiakkannirut_atuutilik];
                if (수 == 16) { itigaqtuq_atuutilik("too many parameters"); break; }
                int qanuittuuninga_atuutilik = aaqqisurli_atuutilik(); if (qanuittuuninga_atuutilik == 0) itigaqtuq_atuutilik("void parameter");
                함수인수형[sugiakkannirut_atuutilik * 16 + 수] = qanuittuuninga_atuutilik; 함수인수이름[sugiakkannirut_atuutilik * 16 + 수] = 식별자();
                함수인수수[sugiakkannirut_atuutilik]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!tammarniq && 받기(','));
            }
            함수본문[sugiakkannirut_atuutilik] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) itigaqtuq_atuutilik("unclosed method body");
            함수끝[sugiakkannirut_atuutilik] = 위치;
            함수명상수[sugiakkannirut_atuutilik] = 토큰상수(함수이름[sugiakkannirut_atuutilik]);
            immikkuuqtuq_takininga = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[sugiakkannirut_atuutilik]; 수++) ilali_aaqqisurli(함수인수형[sugiakkannirut_atuutilik * 16 + 수]);
            글추가(')'); ilali_aaqqisurli(함수반환[sugiakkannirut_atuutilik]); 함수서술[sugiakkannirut_atuutilik] = immikkuuqtuq_surragunnangittuq();
        }
        요구('}'); if (위치 != 토큰수) itigaqtuq_atuutilik("extra input after class");
    }
    static int nanili_tamaani(int atiq) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(tamaani_atiq[수], atiq)) return 수;
        itigaqtuq_atuutilik("unknown variable"); return 0;
    }
    static int ilali_tamaani(int atiq, int qanuittuuninga_atuutilik) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(tamaani_atiq[수], atiq)) itigaqtuq_atuutilik("duplicate local variable");
        if (지역수 == 128) { itigaqtuq_atuutilik("too many locals"); return 0; }
        tamaani_atiq[지역수] = atiq; tamaani_qanuittuuninga[지역수] = qanuittuuninga_atuutilik; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean naasaut_qanuittuuninga(int qanuittuuninga_atuutilik) { return qanuittuuninga_atuutilik == 1 || qanuittuuninga_atuutilik == 5; }
    static void 지역읽기(int 수) { 내보내기(tamaani_qanuittuuninga[수] <= 2 || tamaani_qanuittuuninga[수] == 5 ? 21 : 25); 내보내기(수); }
    static void titiraq_tamaani(int 수) { 내보내기(tamaani_qanuittuuninga[수] <= 2 || tamaani_qanuittuuninga[수] == 5 ? 54 : 58); 내보내기(수); }
    static void nalunairli_qanuittuuninga(int taannallarik_titiqqat, int 기대) { if (taannallarik_titiqqat != 기대 && !(taannallarik_titiqqat == 5 && 기대 == 1)) itigaqtuq_atuutilik("type mismatch"); }
    static void 문자읽기(int 토큰) {
        immikkuuqtuq_takininga = 0; int 시작 = 토큰위치[토큰] + 1, 끝 = 토큰위치[토큰] + 토큰길이[토큰] - 1;
        while (시작 < 끝 && !tammarniq) {
            int atuutilik = pivviujuq[시작++];
            if (atuutilik == '\\') {
                if (시작 == 끝) { itigaqtuq_atuutilik("invalid escape"); break; }
                atuutilik = pivviujuq[시작++];
                if (atuutilik == 'n') atuutilik = 10;
                else if (atuutilik == 'r') atuutilik = 13;
                else if (atuutilik == 't') atuutilik = 9;
                else if (atuutilik == 'b') atuutilik = 8;
                else if (atuutilik == 'f') atuutilik = 12;
                else if (atuutilik != '\\' && atuutilik != '"' && atuutilik != '\'') itigaqtuq_atuutilik("unsupported escape");
            }
            글추가(atuutilik);
        }
    }
    static int agguqtuut_naasaut(int 토큰, boolean 음수) {
        if (토큰길이[토큰] > 1 && pivviujuq[토큰위치[토큰]] == '0') itigaqtuq_atuutilik("octal literals unsupported");
        int atuutilik = 0;
        for (int 수 = 0; 수 < 토큰길이[토큰]; 수++) {
            int 숫 = pivviujuq[토큰위치[토큰] + 수] - '0';
            if (atuutilik < -214748364 || atuutilik == -214748364 && 숫 > (음수 ? 8 : 7)) itigaqtuq_atuutilik("integer literal out of range");
            atuutilik = atuutilik * 10 - 숫;
        }
        return 음수 ? atuutilik : -atuutilik;
    }
    static int 기본식() {
        if (말받기("new")) {
            int qanuittuuninga_atuutilik = aaqqisurli_atuutilik();
            if (qanuittuuninga_atuutilik != 6 && qanuittuuninga_atuutilik != 7) { itigaqtuq_atuutilik("only file streams supported by new in source"); return 0; }
            String 소유 = qanuittuuninga_atuutilik == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            piqujijjut(187, 참조(7, 말상수(소유), 0)); 내보내기(89);
            요구('('); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 3); boolean 이어 = false;
            if (받기(',')) { if (qanuittuuninga_atuutilik != 7) itigaqtuq_atuutilik("input stream constructor arguments"); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 2); 이어 = true; }
            요구(')');
            piqujijjut(183, 외부참조(10, 소유, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return qanuittuuninga_atuutilik;
        }
        if (받기('(')) { int qanuittuuninga_atuutilik = uqarusiq_atuutilik(); 요구(')'); return qanuittuuninga_atuutilik; }
        if (종류() == 257) { 수상수(agguqtuut_naasaut(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); piqujijjut(19, 참조(8, immikkuuqtuq_surragunnangittuq(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (immikkuuqtuq_takininga != 1) itigaqtuq_atuutilik("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String 소유 = "", 메서드 = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                소유 = "한국어/자체/출력"; 요구('.');
                if (말받기("titiraq_titikutaak")) { 메서드 = "titiraq_titikutaak"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("titiraq")) { 메서드 = "titiraq"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { 메서드 = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else itigaqtuq_atuutilik("unknown Korean output method");
            } else if (말받기("문자")) {
                소유 = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("takininga_atuutilik")) { 메서드 = "takininga_atuutilik"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { 메서드 = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("agguqtuut_naasaut")) { 메서드 = "agguqtuut_naasaut"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("titiraq_naasaut_atuutilik")) { 메서드 = "titiraq_naasaut_atuutilik"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { 메서드 = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("nipitilli_titiqqaq")) { 메서드 = "nipitilli_titiqqaq"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("nakalli_atuutilik")) { 메서드 = "nakalli_atuutilik"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else itigaqtuq_atuutilik("unknown Korean text method");
            } else if (말받기("ini")) {
                소유 = "한국어/자체/ini"; 요구('.'); 가 = 3;
                if (말받기("읽기")) { 메서드 = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("titiraq")) { 메서드 = "titiraq"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else itigaqtuq_atuutilik("unknown Korean file method");
            } else if (말받기("화면")) {
                소유 = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { 메서드 = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { 메서드 = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { 메서드 = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { 메서드 = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { 메서드 = "기다리기"; 서술 = "()V"; }
                else itigaqtuq_atuutilik("unknown Korean framebuffer method");
            } else itigaqtuq_atuutilik("unsupported Korean library class");
            요구('('); if (가 != 0) nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 가);
            if (나 != 0) { 요구(','); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 나); }
            if (다 != 0) { 요구(','); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 다); }
            if (라 != 0) { 요구(','); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 라); }
            if (마 != 0) { 요구(','); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 마); }
            요구(')'); piqujijjut(184, 외부참조(10, 소유, 메서드, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 3); 요구(')');
            piqujijjut(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int atiq = 식별자();
        if (받기('(')) {
            int sugiakkannirut_atuutilik = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(atiq, 함수이름[수])) sugiakkannirut_atuutilik = 수;
            if (sugiakkannirut_atuutilik < 0) { itigaqtuq_atuutilik("unknown static method"); return 0; }
            int 수 = 0;
            while (!tammarniq && 종류() != ')') {
                if (수 >= 함수인수수[sugiakkannirut_atuutilik]) { itigaqtuq_atuutilik("too many arguments"); break; }
                nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 함수인수형[sugiakkannirut_atuutilik * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[sugiakkannirut_atuutilik]) itigaqtuq_atuutilik("argument count mismatch");
            piqujijjut(184, 참조(10, naliannuungavik_surragunnangittuq, 참조(12, 함수명상수[sugiakkannirut_atuutilik], 함수서술[sugiakkannirut_atuutilik])));
            return 함수반환[sugiakkannirut_atuutilik];
        }
        int tamaani_qinirvik = nanili_tamaani(atiq), qanuittuuninga_atuutilik = tamaani_qanuittuuninga[tamaani_qinirvik]; 지역읽기(tamaani_qinirvik);
        while (!tammarniq) {
            if (받기('[')) { nalunairli_qanuittuuninga(qanuittuuninga_atuutilik, 4); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 1); 요구(']'); 내보내기(50); qanuittuuninga_atuutilik = 3; }
            else if (받기('.')) {
                if (qanuittuuninga_atuutilik == 6 || qanuittuuninga_atuutilik == 7) {
                    String 소유 = qanuittuuninga_atuutilik == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); piqujijjut(182, 외부참조(10, 소유, "close", "()V")); qanuittuuninga_atuutilik = 0; }
                    else if (qanuittuuninga_atuutilik == 6 && 말받기("read")) { 요구('('); 요구(')'); piqujijjut(182, 외부참조(10, 소유, "read", "()I")); qanuittuuninga_atuutilik = 1; }
                    else if (qanuittuuninga_atuutilik == 7 && 말받기("write")) { 요구('('); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 1); 요구(')'); piqujijjut(182, 외부참조(10, 소유, "write", "(I)V")); qanuittuuninga_atuutilik = 0; }
                    else { itigaqtuq_atuutilik("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (qanuittuuninga_atuutilik == 4) { 내보내기(190); qanuittuuninga_atuutilik = 1; }
                else { nalunairli_qanuittuuninga(qanuittuuninga_atuutilik, 3); 요구('('); 요구(')'); piqujijjut(182, 외부참조(10, "java/lang/String", "length", "()I")); qanuittuuninga_atuutilik = 1; }
            } else break;
        }
        return qanuittuuninga_atuutilik;
    }
    static int 단항() {
        if (++식깊이 > 64) { itigaqtuq_atuutilik("expression nesting too deep"); 식깊이--; return 0; }
        int qanuittuuninga_atuutilik;
        if (받기('!')) { nalunairli_qanuittuuninga(단항(), 2); 비교값(153); qanuittuuninga_atuutilik = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(agguqtuut_naasaut(위치++, true));
            else { nalunairli_qanuittuuninga(단항(), 1); 내보내기(116); }
            qanuittuuninga_atuutilik = 1;
        } else if (받기('+')) { nalunairli_qanuittuuninga(단항(), 1); qanuittuuninga_atuutilik = 1; }
        else qanuittuuninga_atuutilik = 기본식();
        식깊이--; return qanuittuuninga_atuutilik;
    }
    static int 곱식() {
        int qanuittuuninga_atuutilik = 단항();
        while (!tammarniq && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int tukiniktiri_atuutilik = 종류(); 위치++; nalunairli_qanuittuuninga(qanuittuuninga_atuutilik, 1); nalunairli_qanuittuuninga(단항(), 1);
            내보내기(tukiniktiri_atuutilik == '*' ? 104 : tukiniktiri_atuutilik == '/' ? 108 : 112); qanuittuuninga_atuutilik = 1;
        }
        return qanuittuuninga_atuutilik;
    }
    static int 합식() {
        int qanuittuuninga_atuutilik = 곱식();
        while (!tammarniq && (종류() == '+' || 종류() == '-')) {
            int tukiniktiri_atuutilik = 종류(); 위치++; int 경계 = 코드크기, Utimut_atuutilik_qanuittuuninga = 곱식();
            if (tukiniktiri_atuutilik == '+' && (qanuittuuninga_atuutilik == 3 || Utimut_atuutilik_qanuittuuninga == 3)) { 결합(경계, qanuittuuninga_atuutilik, Utimut_atuutilik_qanuittuuninga); qanuittuuninga_atuutilik = 3; }
            else { nalunairli_qanuittuuninga(qanuittuuninga_atuutilik, 1); nalunairli_qanuittuuninga(Utimut_atuutilik_qanuittuuninga, 1); 내보내기(tukiniktiri_atuutilik == '+' ? 96 : 100); qanuittuuninga_atuutilik = 1; }
        }
        return qanuittuuninga_atuutilik;
    }
    static int 붙임참조(int qanuittuuninga_atuutilik) {
        if (qanuittuuninga_atuutilik != 1 && qanuittuuninga_atuutilik != 2 && qanuittuuninga_atuutilik != 3 && qanuittuuninga_atuutilik != 5) itigaqtuq_atuutilik("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", qanuittuuninga_atuutilik == 1 ? "(I)Ljava/lang/StringBuilder;"
            : qanuittuuninga_atuutilik == 2 ? "(Z)Ljava/lang/StringBuilder;" : qanuittuuninga_atuutilik == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Utimut_atuutilik_qanuittuuninga) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 uqarusiq_atuutilik 내부의 ilagijaujuq_atuutilik avalangajuq 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        piqujijjut(187, 참조(7, 말상수("java/lang/StringBuilder"), 0)); 내보내기(89);
        piqujijjut(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); piqujijjut(182, 붙임참조(앞형));
        if (tammarniq) return;
        int takininga_atuutilik = 코드크기 - 끝;
        for (int 수 = 0; 수 < takininga_atuutilik; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + takininga_atuutilik] = 코드[수];
        for (int 수 = 0; 수 < takininga_atuutilik; 수++) 코드[경계 + 수] = 삽입코드[수];
        piqujijjut(182, 붙임참조(Utimut_atuutilik_qanuittuuninga)); piqujijjut(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int qanuittuuninga_atuutilik = 합식();
        while (!tammarniq && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int tukiniktiri_atuutilik = 종류(); 위치++; nalunairli_qanuittuuninga(qanuittuuninga_atuutilik, 1); nalunairli_qanuittuuninga(합식(), 1);
            비교값(tukiniktiri_atuutilik == '<' ? 161 : tukiniktiri_atuutilik == '>' ? 163 : tukiniktiri_atuutilik == 302 ? 164 : 162); qanuittuuninga_atuutilik = 2;
        }
        return qanuittuuninga_atuutilik;
    }
    static int 동등식() {
        int qanuittuuninga_atuutilik = 비교식();
        while (!tammarniq && (종류() == 300 || 종류() == 301)) {
            int tukiniktiri_atuutilik = 종류(); 위치++; int Utimut_atuutilik_qanuittuuninga = 비교식();
            if (qanuittuuninga_atuutilik == 0 || Utimut_atuutilik_qanuittuuninga == 0) itigaqtuq_atuutilik("void expression");
            if (!(naasaut_qanuittuuninga(qanuittuuninga_atuutilik) && naasaut_qanuittuuninga(Utimut_atuutilik_qanuittuuninga))) nalunairli_qanuittuuninga(Utimut_atuutilik_qanuittuuninga, qanuittuuninga_atuutilik);
            비교값((qanuittuuninga_atuutilik <= 2 || qanuittuuninga_atuutilik == 5 ? 159 : 165) + (tukiniktiri_atuutilik == 301 ? 1 : 0)); qanuittuuninga_atuutilik = 2;
        }
        return qanuittuuninga_atuutilik;
    }
    static int 논리곱() {
        int qanuittuuninga_atuutilik = 동등식();
        while (!tammarniq && 받기(304)) {
            nalunairli_qanuittuuninga(qanuittuuninga_atuutilik, 2); int 가 = avalangajuq(153); nalunairli_qanuittuuninga(동등식(), 2); int 나 = avalangajuq(153);
            내보내기(4); int 끝 = avalangajuq(167); kasurvik_atuutilik(가, 코드크기); kasurvik_atuutilik(나, 코드크기); 내보내기(3); kasurvik_atuutilik(끝, 코드크기); qanuittuuninga_atuutilik = 2;
        }
        return qanuittuuninga_atuutilik;
    }
    static int uqarusiq_atuutilik() {
        int qanuittuuninga_atuutilik = 논리곱();
        while (!tammarniq && 받기(305)) {
            nalunairli_qanuittuuninga(qanuittuuninga_atuutilik, 2); int 가 = avalangajuq(154); nalunairli_qanuittuuninga(논리곱(), 2); int 나 = avalangajuq(154);
            내보내기(3); int 끝 = avalangajuq(167); kasurvik_atuutilik(가, 코드크기); kasurvik_atuutilik(나, 코드크기); 내보내기(4); kasurvik_atuutilik(끝, 코드크기); qanuittuuninga_atuutilik = 2;
        }
        return qanuittuuninga_atuutilik;
    }
    static void 대입(boolean 선언허용) {
        if (단어(위치, "int") || 단어(위치, "boolean") || 단어(위치, "String") || 단어(위치, "char")
            || 단어(위치, "FileInputStream") || 단어(위치, "FileOutputStream")) {
            if (!선언허용) itigaqtuq_atuutilik("declaration not allowed here");
            int qanuittuuninga_atuutilik = aaqqisurli_atuutilik(), atiq = 식별자(); 요구('='); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), qanuittuuninga_atuutilik);
            titiraq_tamaani(ilali_tamaani(atiq, qanuittuuninga_atuutilik)); return;
        }
        int atiq = 식별자(), tamaani_qinirvik = nanili_tamaani(atiq);
        if (받기('=')) { nalunairli_qanuittuuninga(uqarusiq_atuutilik(), tamaani_qanuittuuninga[tamaani_qinirvik]); titiraq_tamaani(tamaani_qinirvik); }
        else if (종류() >= 308 && 종류() <= 312) {
            int tukiniktiri_atuutilik = 종류(); 위치++; 지역읽기(tamaani_qinirvik); int 경계 = 코드크기, Utimut_atuutilik_qanuittuuninga = uqarusiq_atuutilik();
            if (tukiniktiri_atuutilik == 308 && tamaani_qanuittuuninga[tamaani_qinirvik] == 3) 결합(경계, 3, Utimut_atuutilik_qanuittuuninga);
            else {
                nalunairli_qanuittuuninga(tamaani_qanuittuuninga[tamaani_qinirvik], 1); nalunairli_qanuittuuninga(Utimut_atuutilik_qanuittuuninga, 1);
                내보내기(tukiniktiri_atuutilik == 308 ? 96 : tukiniktiri_atuutilik == 309 ? 100 : tukiniktiri_atuutilik == 310 ? 104 : tukiniktiri_atuutilik == 311 ? 108 : 112);
                if (tamaani_qanuittuuninga[tamaani_qinirvik] == 5) 내보내기(146);
            }
            titiraq_tamaani(tamaani_qinirvik);
        }
        else if (종류() == 306 || 종류() == 307) {
            nalunairli_qanuittuuninga(tamaani_qanuittuuninga[tamaani_qinirvik], 1); 내보내기(132); 내보내기(tamaani_qinirvik); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (tamaani_qanuittuuninga[tamaani_qinirvik] == 5) { 지역읽기(tamaani_qinirvik); 내보내기(146); titiraq_tamaani(tamaani_qinirvik); }
        } else itigaqtuq_atuutilik("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        piqujijjut(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int qanuittuuninga_atuutilik = 빈인수 ? 0 : uqarusiq_atuutilik(); 요구(')'); 요구(';');
        String 서술 = qanuittuuninga_atuutilik == 0 ? "()V" : qanuittuuninga_atuutilik == 1 ? "(I)V" : qanuittuuninga_atuutilik == 2 ? "(Z)V" : qanuittuuninga_atuutilik == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (qanuittuuninga_atuutilik == 4 || qanuittuuninga_atuutilik >= 6 || qanuittuuninga_atuutilik == 0 && (!줄바꿈 || !빈인수)) itigaqtuq_atuutilik("unsupported print argument");
        piqujijjut(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean uqaqtaujuq_atuutilik() {
        if (tammarniq) return false;
        if (깊이 > 32) { itigaqtuq_atuutilik("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!tammarniq && 종류() != '}') { if (반환) itigaqtuq_atuutilik("unreachable statement"); 반환 = uqaqtaujuq_atuutilik(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int qanuittuuninga_atuutilik = 종류() == ';' ? 0 : uqarusiq_atuutilik(); nalunairli_qanuittuuninga(qanuittuuninga_atuutilik, 함수반환[현재함수]); 요구(';');
            내보내기(qanuittuuninga_atuutilik == 0 ? 177 : qanuittuuninga_atuutilik <= 2 || qanuittuuninga_atuutilik == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 2); 요구(')'); int 거짓 = avalangajuq(153);
            깊이++; boolean 가 = aulattivik_uqaqtaujuq(); 깊이--;
            if (말받기("else")) { int 끝 = avalangajuq(167); kasurvik_atuutilik(거짓, 코드크기); 깊이++; boolean 나 = aulattivik_uqaqtaujuq(); 깊이--; kasurvik_atuutilik(끝, 코드크기); return 가 && 나; }
            kasurvik_atuutilik(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int 시작 = 코드크기; 요구('('); nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 2); 요구(')'); int 끝 = avalangajuq(153);
            깊이++; aulattivik_uqaqtaujuq(); 깊이--; kasurvik_atuutilik(avalangajuq(167), 시작); kasurvik_atuutilik(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') 대입(true); 요구(';');
            int qanuinniq = 코드크기; if (종류() == ';') 내보내기(4); else nalunairli_qanuittuuninga(uqarusiq_atuutilik(), 2); 요구(';');
            int 끝 = avalangajuq(153), Titiqqaup_ilulilluataa = avalangajuq(167), qittaijarli = 코드크기;
            if (종류() != ')') 대입(false); 요구(')'); kasurvik_atuutilik(avalangajuq(167), qanuinniq); kasurvik_atuutilik(Titiqqaup_ilulilluataa, 코드크기);
            aulattivik_uqaqtaujuq(); kasurvik_atuutilik(avalangajuq(167), qittaijarli); kasurvik_atuutilik(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (단어(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int qanuittuuninga_atuutilik = uqarusiq_atuutilik(); if (qanuittuuninga_atuutilik != 0) 내보내기(87); 요구(';'); return false;
        }
        대입(true); 요구(';'); return false;
    }
    static boolean aulattivik_uqaqtaujuq() {
        if (단어(위치, "int") || 단어(위치, "boolean") || 단어(위치, "char") || 단어(위치, "String")
            || 단어(위치, "FileInputStream") || 단어(위치, "FileOutputStream")) itigaqtuq_atuutilik("local declaration requires braces");
        return uqaqtaujuq_atuutilik();
    }
    static void 출바(int atuutilik) { if (출력크기 == 출력.length) itigaqtuq_atuutilik("class file too large"); else 출력[출력크기++] = atuutilik & 255; }
    static void 출짧(int atuutilik) { 출바(atuutilik >> 8); 출바(atuutilik); }
    static void 출정(int atuutilik) { 출짧(atuutilik >>> 16); 출짧(atuutilik); }
    static void titiraq_naliannuungavik() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < surragunnangittuq_anininga; 수++) 출바(surragunnangittuq_atuutilik[수]);
        출짧(0x21); 출짧(naliannuungavik_surragunnangittuq); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(함수권한[수]); 출짧(함수명상수[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + 함수길이[수]); 출짧(128); 출짧(함수지역[수]); 출정(함수길이[수]);
            for (int 칸 = 0; 칸 < 함수길이[수]; 칸++) 출바(코드[함수코드[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int 시작() {
        if (atuqtuq.인수개수() == 1 && 자바도구.같음(atuqtuq.인수(0), "-version")) {
            atuqtuq.titiraq("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (atuqtuq.인수개수() != 1) { atuqtuq.titiraq("Usage: javac FILE.java\n"); return 2; }
        int atiq_anininga = 자바도구.atiq(ini_atiq_titiqqaq, atuqtuq.인수(0));
        if (atiq_anininga < 6 || atiq_anininga > 62 || ini_atiq_titiqqaq[atiq_anininga - 5] != '.' || ini_atiq_titiqqaq[atiq_anininga - 4] != 'j'
            || ini_atiq_titiqqaq[atiq_anininga - 3] != 'a' || ini_atiq_titiqqaq[atiq_anininga - 2] != 'v' || ini_atiq_titiqqaq[atiq_anininga - 1] != 'a') {
            atuqtuq.titiraq("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        pivviujuq_anininga = atuqtuq.파일읽기(ini_atiq_titiqqaq, pivviujuq);
        if (pivviujuq_anininga < 0) { atuqtuq.titiraq("javac: cannot read source: "); 자바도구.수쓰기(pivviujuq_anininga); atuqtuq.titiraq_immikkuuqtuq_atuutilik(10); return 1; }
        pivviujuq_anininga = 자바도구.원문해독(pivviujuq, pivviujuq_anininga);
        if (pivviujuq_anininga < 0) { atuqtuq.titiraq("javac error: invalid UTF-8 source\n"); return 1; }
        nakalli_atuutilik(); if (!tammarniq) 선언읽기();
        if (!tammarniq) {
            if (토큰길이[클래스토큰] != atiq_anininga - 5) itigaqtuq_atuutilik("class name must match file name");
            for (int 수 = 0; 수 < atiq_anininga - 5; 수++) if (pivviujuq[토큰위치[클래스토큰] + 수] != ini_atiq_titiqqaq[수]) itigaqtuq_atuutilik("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !tammarniq; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) ilali_tamaani(함수인수이름[현재함수 * 16 + 수], 함수인수형[현재함수 * 16 + 수]);
            boolean 반환 = uqaqtaujuq_atuutilik();
            if (!반환 && 함수반환[현재함수] != 0) itigaqtuq_atuutilik("missing return");
            // avalangajuq 뒤의 합류 지점은 반드시 taannallarik_titiqqat 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean naasaut = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(naasaut ? 3 : 1); 내보내기(naasaut ? 172 : 176); }
            if (위치 != 함수끝[현재함수]) itigaqtuq_atuutilik("invalid method body");
            함수지역[현재함수] = 지역수; 함수길이[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (tammarniq) return 1;
        titiraq_naliannuungavik(); if (tammarniq) return 1;
        ini_atiq_titiqqaq[atiq_anininga - 4] = 'c'; ini_atiq_titiqqaq[atiq_anininga - 3] = 'l'; ini_atiq_titiqqaq[atiq_anininga - 2] = 'a';
        ini_atiq_titiqqaq[atiq_anininga - 1] = 's'; ini_atiq_titiqqaq[atiq_anininga] = 's'; ini_atiq_titiqqaq[atiq_anininga + 1] = 0;
        int 결과 = atuqtuq.titiraq_ini(ini_atiq_titiqqaq, 출력, 출력크기);
        if (결과 < 0) { atuqtuq.titiraq("javac: cannot save class: "); 자바도구.수쓰기(결과); atuqtuq.titiraq_immikkuuqtuq_atuutilik(10); return 1; }
        atuqtuq.titiraq("Compiled: "); for (int 수 = 0; ini_atiq_titiqqaq[수] != 0; 수++) atuqtuq.titiraq_immikkuuqtuq_atuutilik(ini_atiq_titiqqaq[수]);
        atuqtuq.titiraq(" (JVM class version 49)\n"); return 0;
    }
}
