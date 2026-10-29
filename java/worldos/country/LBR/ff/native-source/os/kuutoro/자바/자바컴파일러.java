// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java sewnde_lekki -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] sewnde = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], 토큰길이 = new int[2048];
    static int[] 상수 = new int[4096], 상수위치 = new int[512];
    static int[] 문자 = new int[512], fiilde_innde_binndi = new int[64];
    static int[] 삽입코드 = new int[16];
    static int sewnde_waylude_etannde, 토큰수, 위치, 코드크기, 상수크기, 상수수 = 1, 출력크기, alkulal_njuuteendi;
    static boolean juumre;
    static int 클래스토큰, 클래스상수, 부모상수, 코드상수;
    static int[] 함수이름 = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] 함수인수이름 = new int[512], 함수인수형 = new int[512];
    static int[] 함수본문 = new int[32], 함수끝 = new int[32], 함수코드 = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], 함수명상수 = new int[32], 함수서술 = new int[32];
    static int[] 함수권한 = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] nokkuwal_innde = new int[128], 지역형 = new int[128], 지역깊이 = new int[128];

    static void ella_njaru(String 이유) {
        if (!juumre) {
            kuutoro.winndude("javac error: "); kuutoro.winndude(이유);
            kuutoro.winndude(" at line ");
            int diidol = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : sewnde_waylude_etannde;
            for (int 수 = 0; 수 < 끝; 수++) if (sewnde[수] == 10) diidol++;
            자바도구.수쓰기(diidol); kuutoro.winndude_alkulal_njaru(10);
        }
        juumre = true;
    }
    static boolean alkulal_njaru(int njaru) { return 문자이름규칙.첫글자(njaru); }
    static boolean 숫자(int njaru) { return njaru >= '0' && njaru <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || 토큰길이[가] != 토큰길이[나]) return false;
        for (int 수 = 0; 수 < 토큰길이[가]; 수++) if (sewnde[토큰위치[가] + 수] != sewnde[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean 단어(int 토큰, String 말) {
        if (토큰 < 0 || 토큰 >= 토큰수 || 토큰길이[토큰] != 말.length()) return false;
        for (int 수 = 0; 수 < 말.length(); 수++) if (sewnde[토큰위치[토큰] + 수] != 말.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int njaru) { if (종류() != njaru) return false; 위치++; return true; }
    static void 요구(int njaru) { if (!받기(njaru)) ella_njaru("unexpected token"); }
    static boolean 말받기(String 말) { if (!단어(위치, 말)) return false; 위치++; return true; }
    static void 말요구(String 말) { if (!말받기(말)) ella_njaru(말); }
    static int 식별자() {
        int 결과 = 위치;
        if (종류() != 256) ella_njaru("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int huutoraade = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - huutoraade == 토큰길이[결과];
                for (int 칸 = huutoraade; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != sewnde[토큰위치[결과] + 칸 - huutoraade]) 같음 = false;
                if (같음) ella_njaru("reserved word cannot be an identifier");
                huutoraade = 수 + 1;
            }
        }
        return 결과;
    }
    static void taƴde_njaru() {
        int 수 = 0;
        while (수 < sewnde_waylude_etannde && !juumre) {
            int njaru = sewnde[수], huutoraade = 수, 종류 = njaru;
            if (njaru == 32 || njaru == 9 || njaru == 10 || njaru == 13) { 수++; continue; }
            if (njaru == '/' && 수 + 1 < sewnde_waylude_etannde && sewnde[수 + 1] == '/') {
                while (수 < sewnde_waylude_etannde && sewnde[수] != 10) 수++;
                continue;
            }
            if (njaru == '/' && 수 + 1 < sewnde_waylude_etannde && sewnde[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < sewnde_waylude_etannde && !(sewnde[수] == '*' && sewnde[수 + 1] == '/')) 수++;
                if (수 + 1 >= sewnde_waylude_etannde) { ella_njaru("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (alkulal_njaru(njaru)) { 종류 = 256; while (수 < sewnde_waylude_etannde && 문자이름규칙.이어진글자(sewnde[수])) 수++; }
            else if (숫자(njaru)) { 종류 = 257; while (수 < sewnde_waylude_etannde && 숫자(sewnde[수])) 수++; }
            else if (njaru == '"' || njaru == '\'') {
                종류 = njaru == '"' ? 258 : 259; 수++;
                while (수 < sewnde_waylude_etannde && sewnde[수] != njaru && sewnde[수] != 10 && sewnde[수] != 13) {
                    if (sewnde[수] == '\\') 수++;
                    수++;
                }
                if (수 >= sewnde_waylude_etannde || sewnde[수] != njaru) { ella_njaru("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < sewnde_waylude_etannde) {
                    int 다음 = sewnde[수];
                    if (njaru == '=' && 다음 == '=') 종류 = 300;
                    if (njaru == '!' && 다음 == '=') 종류 = 301;
                    if (njaru == '<' && 다음 == '=') 종류 = 302;
                    if (njaru == '>' && 다음 == '=') 종류 = 303;
                    if (njaru == '&' && 다음 == '&') 종류 = 304;
                    if (njaru == '|' && 다음 == '|') 종류 = 305;
                    if (njaru == '+' && 다음 == '+') 종류 = 306;
                    if (njaru == '-' && 다음 == '-') 종류 = 307;
                    if (njaru == '+' && 다음 == '=') 종류 = 308;
                    if (njaru == '-' && 다음 == '=') 종류 = 309;
                    if (njaru == '*' && 다음 == '=') 종류 = 310;
                    if (njaru == '/' && 다음 == '=') 종류 = 311;
                    if (njaru == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { ella_njaru("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = huutoraade; 토큰길이[토큰수++] = 수 - huutoraade;
        }
    }
    static void 상바(int njaru) {
        if (상수크기 == 상수.length) { ella_njaru("constant pool too large"); return; }
        상수[상수크기++] = njaru & 255;
    }
    static void 상짧(int njaru) { 상바(njaru >> 8); 상바(njaru); }
    static int 상등록(int huutoraade) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = 상수위치[수], njuuteendi_njaru = (수 + 1 < 상수수 ? 상수위치[수 + 1] : huutoraade) - 앞;
            if (njuuteendi_njaru != 상수크기 - huutoraade) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < njuuteendi_njaru; 칸++) if (상수[앞 + 칸] != 상수[huutoraade + 칸]) 같음 = false;
            if (같음) { 상수크기 = huutoraade; return 수; }
        }
        if (상수수 == 상수위치.length) { ella_njaru("too many constants"); return 0; }
        상수위치[상수수] = huutoraade;
        return 상수수++;
    }
    static void 글추가(int njaru) {
        if (alkulal_njuuteendi == 문자.length) { ella_njaru("text too long"); return; }
        문자[alkulal_njuuteendi++] = njaru;
    }
    static void 말추가(String 말) { for (int 수 = 0; 수 < 말.length(); 수++) 글추가(말.charAt(수)); }
    static int 문자상수() {
        int huutoraade = 상수크기; 상바(1); 상짧(0);
        for (int 수 = 0; 수 < alkulal_njuuteendi; 수++) {
            int njaru = 문자[수];
            if (njaru > 0 && njaru < 128) 상바(njaru);
            else if (njaru < 2048) { 상바(192 | njaru >> 6); 상바(128 | njaru & 63); }
            else { 상바(224 | njaru >> 12); 상바(128 | njaru >> 6 & 63); 상바(128 | njaru & 63); }
        }
        if (juumre) return 0;
        int njuuteendi_njaru = 상수크기 - huutoraade - 3;
        상수[huutoraade + 1] = njuuteendi_njaru >> 8; 상수[huutoraade + 2] = njuuteendi_njaru & 255;
        return 상등록(huutoraade);
    }
    static int 말상수(String 말) { alkulal_njuuteendi = 0; 말추가(말); return 문자상수(); }
    static int 토큰상수(int 토큰) {
        alkulal_njuuteendi = 0;
        for (int 수 = 0; 수 < 토큰길이[토큰]; 수++) 글추가(sewnde[토큰위치[토큰] + 수]);
        return 문자상수();
    }
    static int 참조(int 종류, int 가, int 나) {
        int huutoraade = 상수크기; 상바(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return 상등록(huutoraade);
    }
    static int 외부참조(int 종류, String 소유, String innde, String 서술) {
        int 주인 = 참조(7, 말상수(소유), 0);
        int 이름수 = 말상수(innde), 형식수 = 말상수(서술);
        return 참조(종류, 주인, 참조(12, 이름수, 형식수));
    }
    static void 내보내기(int njaru) {
        if (코드크기 == 코드.length) { ella_njaru("bytecode too large"); return; }
        코드[코드크기++] = njaru & 255;
    }
    static void ginol(int njaru, int 인수) { 내보내기(njaru); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int njaru) {
        if (njaru >= -1 && njaru <= 5) { 내보내기(njaru + 3); return; }
        int huutoraade = 상수크기; 상바(3); 상짧(njaru >>> 16); 상짧(njaru);
        ginol(19, 상등록(huutoraade));
    }
    static int 분기(int ginol) { int 결과 = 코드크기; ginol(ginol, 0); return 결과; }
    static void jokkere_njaru(int 분기, int faandaare_huunde) {
        if (juumre) return;
        int 거리 = faandaare_huunde - 분기;
        if (거리 < -32768 || 거리 > 32767 || 분기 < 0 || 분기 + 2 >= 코드크기) { ella_njaru("invalid branch"); return; }
        코드[분기 + 1] = 거리 >> 8 & 255; 코드[분기 + 2] = 거리 & 255;
    }
    static void 비교값(int ginol) {
        int 참 = 분기(ginol); 내보내기(3); int 끝 = 분기(167);
        jokkere_njaru(참, 코드크기); 내보내기(4); jokkere_njaru(끝, 코드크기);
    }
    static int formaa_njaru() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        ella_njaru("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void ɓeydude_formaa(int 형) {
        if (형 == 0) 글추가('V');
        if (형 == 1) 글추가('I');
        if (형 == 2) 글추가('Z');
        if (형 == 3) 말추가("Ljava/lang/String;");
        if (형 == 4) 말추가("[Ljava/lang/String;");
        if (형 == 5) 글추가('C');
        if (형 == 6) 말추가("Ljava/io/FileInputStream;");
        if (형 == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Yuɓɓo_golle_njaru_naatnugol 본문은 njaatigi javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("배열저장예외") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        ella_njaru("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (단어(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) ella_njaru("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); 클래스토큰 = 식별자();
        클래스상수 = 참조(7, 토큰상수(클래스토큰), 0);
        부모상수 = 참조(7, 말상수("java/lang/Object"), 0); 코드상수 = 말상수("Code"); 요구('{');
        while (!juumre && 종류() != '}') {
            if (함수수 == 32) { ella_njaru("too many methods"); break; }
            int naatde_naatnugol = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int juɓɓol_njaru = 함수수++;
            함수권한[juɓɓol_njaru] = naatde_naatnugol | 8;
            함수반환[juɓɓol_njaru] = formaa_njaru(); 함수이름[juɓɓol_njaru] = 식별자(); 요구('(');
            for (int 앞 = 0; 앞 < juɓɓol_njaru; 앞++) if (이름같음(함수이름[앞], 함수이름[juɓɓol_njaru])) ella_njaru("duplicate method (overloading unsupported)");
            while (!juumre && 종류() != ')') {
                int 수 = 함수인수수[juɓɓol_njaru];
                if (수 == 16) { ella_njaru("too many parameters"); break; }
                int 형 = formaa_njaru(); if (형 == 0) ella_njaru("void parameter");
                함수인수형[juɓɓol_njaru * 16 + 수] = 형; 함수인수이름[juɓɓol_njaru * 16 + 수] = 식별자();
                함수인수수[juɓɓol_njaru]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!juumre && 받기(','));
            }
            함수본문[juɓɓol_njaru] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) ella_njaru("unclosed method body");
            함수끝[juɓɓol_njaru] = 위치;
            함수명상수[juɓɓol_njaru] = 토큰상수(함수이름[juɓɓol_njaru]);
            alkulal_njuuteendi = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[juɓɓol_njaru]; 수++) ɓeydude_formaa(함수인수형[juɓɓol_njaru * 16 + 수]);
            글추가(')'); ɓeydude_formaa(함수반환[juɓɓol_njaru]); 함수서술[juɓɓol_njaru] = 문자상수();
        }
        요구('}'); if (위치 != 토큰수) ella_njaru("extra input after class");
    }
    static int yiylaade_nokkuwal(int innde) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(nokkuwal_innde[수], innde)) return 수;
        ella_njaru("unknown variable"); return 0;
    }
    static int ɓeydude_nokkuwal(int innde, int 형) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(nokkuwal_innde[수], innde)) ella_njaru("duplicate local variable");
        if (지역수 == 128) { ella_njaru("too many locals"); return 0; }
        nokkuwal_innde[지역수] = innde; 지역형[지역수] = 형; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean 정수형(int 형) { return 형 == 1 || 형 == 5; }
    static void 지역읽기(int 수) { 내보내기(지역형[수] <= 2 || 지역형[수] == 5 ? 21 : 25); 내보내기(수); }
    static void winndude_nokkuwal(int 수) { 내보내기(지역형[수] <= 2 || 지역형[수] == 5 ? 54 : 58); 내보내기(수); }
    static void 형확인(int laatii_keɓe, int 기대) { if (laatii_keɓe != 기대 && !(laatii_keɓe == 5 && 기대 == 1)) ella_njaru("type mismatch"); }
    static void 문자읽기(int 토큰) {
        alkulal_njuuteendi = 0; int huutoraade = 토큰위치[토큰] + 1, 끝 = 토큰위치[토큰] + 토큰길이[토큰] - 1;
        while (huutoraade < 끝 && !juumre) {
            int njaru = sewnde[huutoraade++];
            if (njaru == '\\') {
                if (huutoraade == 끝) { ella_njaru("invalid escape"); break; }
                njaru = sewnde[huutoraade++];
                if (njaru == 'n') njaru = 10;
                else if (njaru == 'r') njaru = 13;
                else if (njaru == 't') njaru = 9;
                else if (njaru == 'b') njaru = 8;
                else if (njaru == 'f') njaru = 12;
                else if (njaru != '\\' && njaru != '"' && njaru != '\'') ella_njaru("unsupported escape");
            }
            글추가(njaru);
        }
    }
    static int 정수읽기(int 토큰, boolean 음수) {
        if (토큰길이[토큰] > 1 && sewnde[토큰위치[토큰]] == '0') ella_njaru("octal literals unsupported");
        int njaru = 0;
        for (int 수 = 0; 수 < 토큰길이[토큰]; 수++) {
            int 숫 = sewnde[토큰위치[토큰] + 수] - '0';
            if (njaru < -214748364 || njaru == -214748364 && 숫 > (음수 ? 8 : 7)) ella_njaru("integer literal out of range");
            njaru = njaru * 10 - 숫;
        }
        return 음수 ? njaru : -njaru;
    }
    static int 기본식() {
        if (말받기("new")) {
            int 형 = formaa_njaru();
            if (형 != 6 && 형 != 7) { ella_njaru("only file streams supported by new in source"); return 0; }
            String 소유 = 형 == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            ginol(187, 참조(7, 말상수(소유), 0)); 내보내기(89);
            요구('('); 형확인(식(), 3); boolean 이어 = false;
            if (받기(',')) { if (형 != 7) ella_njaru("input stream constructor arguments"); 형확인(식(), 2); 이어 = true; }
            요구(')');
            ginol(183, 외부참조(10, 소유, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return 형;
        }
        if (받기('(')) { int 형 = 식(); 요구(')'); return 형; }
        if (종류() == 257) { 수상수(정수읽기(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); ginol(19, 참조(8, 문자상수(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (alkulal_njuuteendi != 1) ella_njaru("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String 소유 = "", 메서드 = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                소유 = "한국어/자체/출력"; 요구('.');
                if (말받기("winndude_diidol")) { 메서드 = "winndude_diidol"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("winndude")) { 메서드 = "winndude"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { 메서드 = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else ella_njaru("unknown Korean output method");
            } else if (말받기("문자")) {
                소유 = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("njuuteendi_njaru")) { 메서드 = "njuuteendi_njaru"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { 메서드 = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("정수읽기")) { 메서드 = "정수읽기"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("정수쓰기")) { 메서드 = "정수쓰기"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { 메서드 = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("ɗakkude_binndi")) { 메서드 = "ɗakkude_binndi"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("taƴde_njaru")) { 메서드 = "taƴde_njaru"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else ella_njaru("unknown Korean text method");
            } else if (말받기("fiilde")) {
                소유 = "한국어/자체/fiilde"; 요구('.'); 가 = 3;
                if (말받기("읽기")) { 메서드 = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("winndude")) { 메서드 = "winndude"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else ella_njaru("unknown Korean file method");
            } else if (말받기("화면")) {
                소유 = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { 메서드 = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { 메서드 = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { 메서드 = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { 메서드 = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { 메서드 = "기다리기"; 서술 = "()V"; }
                else ella_njaru("unknown Korean framebuffer method");
            } else ella_njaru("unsupported Korean library class");
            요구('('); if (가 != 0) 형확인(식(), 가);
            if (나 != 0) { 요구(','); 형확인(식(), 나); }
            if (다 != 0) { 요구(','); 형확인(식(), 다); }
            if (라 != 0) { 요구(','); 형확인(식(), 라); }
            if (마 != 0) { 요구(','); 형확인(식(), 마); }
            요구(')'); ginol(184, 외부참조(10, 소유, 메서드, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); 형확인(식(), 3); 요구(')');
            ginol(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int innde = 식별자();
        if (받기('(')) {
            int juɓɓol_njaru = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(innde, 함수이름[수])) juɓɓol_njaru = 수;
            if (juɓɓol_njaru < 0) { ella_njaru("unknown static method"); return 0; }
            int 수 = 0;
            while (!juumre && 종류() != ')') {
                if (수 >= 함수인수수[juɓɓol_njaru]) { ella_njaru("too many arguments"); break; }
                형확인(식(), 함수인수형[juɓɓol_njaru * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[juɓɓol_njaru]) ella_njaru("argument count mismatch");
            ginol(184, 참조(10, 클래스상수, 참조(12, 함수명상수[juɓɓol_njaru], 함수서술[juɓɓol_njaru])));
            return 함수반환[juɓɓol_njaru];
        }
        int nokkuwal_njaajeendi = yiylaade_nokkuwal(innde), 형 = 지역형[nokkuwal_njaajeendi]; 지역읽기(nokkuwal_njaajeendi);
        while (!juumre) {
            if (받기('[')) { 형확인(형, 4); 형확인(식(), 1); 요구(']'); 내보내기(50); 형 = 3; }
            else if (받기('.')) {
                if (형 == 6 || 형 == 7) {
                    String 소유 = 형 == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); ginol(182, 외부참조(10, 소유, "close", "()V")); 형 = 0; }
                    else if (형 == 6 && 말받기("read")) { 요구('('); 요구(')'); ginol(182, 외부참조(10, 소유, "read", "()I")); 형 = 1; }
                    else if (형 == 7 && 말받기("write")) { 요구('('); 형확인(식(), 1); 요구(')'); ginol(182, 외부참조(10, 소유, "write", "(I)V")); 형 = 0; }
                    else { ella_njaru("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (형 == 4) { 내보내기(190); 형 = 1; }
                else { 형확인(형, 3); 요구('('); 요구(')'); ginol(182, 외부참조(10, "java/lang/String", "length", "()I")); 형 = 1; }
            } else break;
        }
        return 형;
    }
    static int 단항() {
        if (++식깊이 > 64) { ella_njaru("expression nesting too deep"); 식깊이--; return 0; }
        int 형;
        if (받기('!')) { 형확인(단항(), 2); 비교값(153); 형 = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(정수읽기(위치++, true));
            else { 형확인(단항(), 1); 내보내기(116); }
            형 = 1;
        } else if (받기('+')) { 형확인(단항(), 1); 형 = 1; }
        else 형 = 기본식();
        식깊이--; return 형;
    }
    static int 곱식() {
        int 형 = 단항();
        while (!juumre && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int dokkagol_njaru = 종류(); 위치++; 형확인(형, 1); 형확인(단항(), 1);
            내보내기(dokkagol_njaru == '*' ? 104 : dokkagol_njaru == '/' ? 108 : 112); 형 = 1;
        }
        return 형;
    }
    static int 합식() {
        int 형 = 곱식();
        while (!juumre && (종류() == '+' || 종류() == '-')) {
            int dokkagol_njaru = 종류(); 위치++; int 경계 = 코드크기, 뒤형 = 곱식();
            if (dokkagol_njaru == '+' && (형 == 3 || 뒤형 == 3)) { 결합(경계, 형, 뒤형); 형 = 3; }
            else { 형확인(형, 1); 형확인(뒤형, 1); 내보내기(dokkagol_njaru == '+' ? 96 : 100); 형 = 1; }
        }
        return 형;
    }
    static int 붙임참조(int 형) {
        if (형 != 1 && 형 != 2 && 형 != 3 && 형 != 5) ella_njaru("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", 형 == 1 ? "(I)Ljava/lang/StringBuilder;"
            : 형 == 2 ? "(Z)Ljava/lang/StringBuilder;" : 형 == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int 뒤형) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 식 내부의 giƴiraaɗo_njaru 분기 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        ginol(187, 참조(7, 말상수("java/lang/StringBuilder"), 0)); 내보내기(89);
        ginol(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); ginol(182, 붙임참조(앞형));
        if (juumre) return;
        int njuuteendi_njaru = 코드크기 - 끝;
        for (int 수 = 0; 수 < njuuteendi_njaru; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + njuuteendi_njaru] = 코드[수];
        for (int 수 = 0; 수 < njuuteendi_njaru; 수++) 코드[경계 + 수] = 삽입코드[수];
        ginol(182, 붙임참조(뒤형)); ginol(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int 형 = 합식();
        while (!juumre && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int dokkagol_njaru = 종류(); 위치++; 형확인(형, 1); 형확인(합식(), 1);
            비교값(dokkagol_njaru == '<' ? 161 : dokkagol_njaru == '>' ? 163 : dokkagol_njaru == 302 ? 164 : 162); 형 = 2;
        }
        return 형;
    }
    static int 동등식() {
        int 형 = 비교식();
        while (!juumre && (종류() == 300 || 종류() == 301)) {
            int dokkagol_njaru = 종류(); 위치++; int 뒤형 = 비교식();
            if (형 == 0 || 뒤형 == 0) ella_njaru("void expression");
            if (!(정수형(형) && 정수형(뒤형))) 형확인(뒤형, 형);
            비교값((형 <= 2 || 형 == 5 ? 159 : 165) + (dokkagol_njaru == 301 ? 1 : 0)); 형 = 2;
        }
        return 형;
    }
    static int 논리곱() {
        int 형 = 동등식();
        while (!juumre && 받기(304)) {
            형확인(형, 2); int 가 = 분기(153); 형확인(동등식(), 2); int 나 = 분기(153);
            내보내기(4); int 끝 = 분기(167); jokkere_njaru(가, 코드크기); jokkere_njaru(나, 코드크기); 내보내기(3); jokkere_njaru(끝, 코드크기); 형 = 2;
        }
        return 형;
    }
    static int 식() {
        int 형 = 논리곱();
        while (!juumre && 받기(305)) {
            형확인(형, 2); int 가 = 분기(154); 형확인(논리곱(), 2); int 나 = 분기(154);
            내보내기(3); int 끝 = 분기(167); jokkere_njaru(가, 코드크기); jokkere_njaru(나, 코드크기); 내보내기(4); jokkere_njaru(끝, 코드크기); 형 = 2;
        }
        return 형;
    }
    static void 대입(boolean 선언허용) {
        if (단어(위치, "int") || 단어(위치, "boolean") || 단어(위치, "String") || 단어(위치, "char")
            || 단어(위치, "FileInputStream") || 단어(위치, "FileOutputStream")) {
            if (!선언허용) ella_njaru("declaration not allowed here");
            int 형 = formaa_njaru(), innde = 식별자(); 요구('='); 형확인(식(), 형);
            winndude_nokkuwal(ɓeydude_nokkuwal(innde, 형)); return;
        }
        int innde = 식별자(), nokkuwal_njaajeendi = yiylaade_nokkuwal(innde);
        if (받기('=')) { 형확인(식(), 지역형[nokkuwal_njaajeendi]); winndude_nokkuwal(nokkuwal_njaajeendi); }
        else if (종류() >= 308 && 종류() <= 312) {
            int dokkagol_njaru = 종류(); 위치++; 지역읽기(nokkuwal_njaajeendi); int 경계 = 코드크기, 뒤형 = 식();
            if (dokkagol_njaru == 308 && 지역형[nokkuwal_njaajeendi] == 3) 결합(경계, 3, 뒤형);
            else {
                형확인(지역형[nokkuwal_njaajeendi], 1); 형확인(뒤형, 1);
                내보내기(dokkagol_njaru == 308 ? 96 : dokkagol_njaru == 309 ? 100 : dokkagol_njaru == 310 ? 104 : dokkagol_njaru == 311 ? 108 : 112);
                if (지역형[nokkuwal_njaajeendi] == 5) 내보내기(146);
            }
            winndude_nokkuwal(nokkuwal_njaajeendi);
        }
        else if (종류() == 306 || 종류() == 307) {
            형확인(지역형[nokkuwal_njaajeendi], 1); 내보내기(132); 내보내기(nokkuwal_njaajeendi); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (지역형[nokkuwal_njaajeendi] == 5) { 지역읽기(nokkuwal_njaajeendi); 내보내기(146); winndude_nokkuwal(nokkuwal_njaajeendi); }
        } else ella_njaru("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        ginol(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int 형 = 빈인수 ? 0 : 식(); 요구(')'); 요구(';');
        String 서술 = 형 == 0 ? "()V" : 형 == 1 ? "(I)V" : 형 == 2 ? "(Z)V" : 형 == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (형 == 4 || 형 >= 6 || 형 == 0 && (!줄바꿈 || !빈인수)) ella_njaru("unsupported print argument");
        ginol(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean konngol_njaru() {
        if (juumre) return false;
        if (깊이 > 32) { ella_njaru("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!juumre && 종류() != '}') { if (반환) ella_njaru("unreachable statement"); 반환 = konngol_njaru(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int 형 = 종류() == ';' ? 0 : 식(); 형확인(형, 함수반환[현재함수]); 요구(';');
            내보내기(형 == 0 ? 177 : 형 <= 2 || 형 == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); 형확인(식(), 2); 요구(')'); int 거짓 = 분기(153);
            깊이++; boolean 가 = yuurnitorde_konngol(); 깊이--;
            if (말받기("else")) { int 끝 = 분기(167); jokkere_njaru(거짓, 코드크기); 깊이++; boolean 나 = yuurnitorde_konngol(); 깊이--; jokkere_njaru(끝, 코드크기); return 가 && 나; }
            jokkere_njaru(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int huutoraade = 코드크기; 요구('('); 형확인(식(), 2); 요구(')'); int 끝 = 분기(153);
            깊이++; yuurnitorde_konngol(); 깊이--; jokkere_njaru(분기(167), huutoraade); jokkere_njaru(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') 대입(true); 요구(';');
            int ngonka = 코드크기; if (종류() == ';') 내보내기(4); else 형확인(식(), 2); 요구(';');
            int 끝 = 분기(153), 본문 = 분기(167), ɓamtude = 코드크기;
            if (종류() != ')') 대입(false); 요구(')'); jokkere_njaru(분기(167), ngonka); jokkere_njaru(본문, 코드크기);
            yuurnitorde_konngol(); jokkere_njaru(분기(167), ɓamtude); jokkere_njaru(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (단어(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int 형 = 식(); if (형 != 0) 내보내기(87); 요구(';'); return false;
        }
        대입(true); 요구(';'); return false;
    }
    static boolean yuurnitorde_konngol() {
        if (단어(위치, "int") || 단어(위치, "boolean") || 단어(위치, "char") || 단어(위치, "String")
            || 단어(위치, "FileInputStream") || 단어(위치, "FileOutputStream")) ella_njaru("local declaration requires braces");
        return konngol_njaru();
    }
    static void 출바(int njaru) { if (출력크기 == 출력.length) ella_njaru("class file too large"); else 출력[출력크기++] = njaru & 255; }
    static void 출짧(int njaru) { 출바(njaru >> 8); 출바(njaru); }
    static void 출정(int njaru) { 출짧(njaru >>> 16); 출짧(njaru); }
    static void winndude_fedde() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < 상수크기; 수++) 출바(상수[수]);
        출짧(0x21); 출짧(클래스상수); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(함수권한[수]); 출짧(함수명상수[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + 함수길이[수]); 출짧(128); 출짧(함수지역[수]); 출정(함수길이[수]);
            for (int 칸 = 0; 칸 < 함수길이[수]; 칸++) 출바(코드[함수코드[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int huutoraade() {
        if (kuutoro.인수개수() == 1 && 자바도구.같음(kuutoro.인수(0), "-version")) {
            kuutoro.winndude("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (kuutoro.인수개수() != 1) { kuutoro.winndude("Usage: javac FILE.java\n"); return 2; }
        int innde_waylude_etannde = 자바도구.innde(fiilde_innde_binndi, kuutoro.인수(0));
        if (innde_waylude_etannde < 6 || innde_waylude_etannde > 62 || fiilde_innde_binndi[innde_waylude_etannde - 5] != '.' || fiilde_innde_binndi[innde_waylude_etannde - 4] != 'j'
            || fiilde_innde_binndi[innde_waylude_etannde - 3] != 'a' || fiilde_innde_binndi[innde_waylude_etannde - 2] != 'v' || fiilde_innde_binndi[innde_waylude_etannde - 1] != 'a') {
            kuutoro.winndude("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        sewnde_waylude_etannde = kuutoro.파일읽기(fiilde_innde_binndi, sewnde);
        if (sewnde_waylude_etannde < 0) { kuutoro.winndude("javac: cannot read source: "); 자바도구.수쓰기(sewnde_waylude_etannde); kuutoro.winndude_alkulal_njaru(10); return 1; }
        sewnde_waylude_etannde = 자바도구.원문해독(sewnde, sewnde_waylude_etannde);
        if (sewnde_waylude_etannde < 0) { kuutoro.winndude("javac error: invalid UTF-8 source\n"); return 1; }
        taƴde_njaru(); if (!juumre) 선언읽기();
        if (!juumre) {
            if (토큰길이[클래스토큰] != innde_waylude_etannde - 5) ella_njaru("class name must match file name");
            for (int 수 = 0; 수 < innde_waylude_etannde - 5; 수++) if (sewnde[토큰위치[클래스토큰] + 수] != fiilde_innde_binndi[수]) ella_njaru("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !juumre; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) ɓeydude_nokkuwal(함수인수이름[현재함수 * 16 + 수], 함수인수형[현재함수 * 16 + 수]);
            boolean 반환 = konngol_njaru();
            if (!반환 && 함수반환[현재함수] != 0) ella_njaru("missing return");
            // 분기 뒤의 합류 지점은 반드시 laatii_keɓe 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean 정수 = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(정수 ? 3 : 1); 내보내기(정수 ? 172 : 176); }
            if (위치 != 함수끝[현재함수]) ella_njaru("invalid method body");
            함수지역[현재함수] = 지역수; 함수길이[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (juumre) return 1;
        winndude_fedde(); if (juumre) return 1;
        fiilde_innde_binndi[innde_waylude_etannde - 4] = 'c'; fiilde_innde_binndi[innde_waylude_etannde - 3] = 'l'; fiilde_innde_binndi[innde_waylude_etannde - 2] = 'a';
        fiilde_innde_binndi[innde_waylude_etannde - 1] = 's'; fiilde_innde_binndi[innde_waylude_etannde] = 's'; fiilde_innde_binndi[innde_waylude_etannde + 1] = 0;
        int 결과 = kuutoro.winndude_fiilde(fiilde_innde_binndi, 출력, 출력크기);
        if (결과 < 0) { kuutoro.winndude("javac: cannot save class: "); 자바도구.수쓰기(결과); kuutoro.winndude_alkulal_njaru(10); return 1; }
        kuutoro.winndude("Compiled: "); for (int 수 = 0; fiilde_innde_binndi[수] != 0; 수++) kuutoro.winndude_alkulal_njaru(fiilde_innde_binndi[수]);
        kuutoro.winndude(" (JVM class version 49)\n"); return 0;
    }
}
