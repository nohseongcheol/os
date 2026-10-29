// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java 소스 -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] FONTO = new int[16384], Eligo = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], 토큰길이 = new int[2048];
    static int[] 상수 = new int[4096], 상수위치 = new int[512];
    static int[] 문자 = new int[512], 파일명 = new int[64];
    static int[] 삽입코드 = new int[16];
    static int 원문크기, 토큰수, 위치, 코드크기, 상수크기, 상수수 = 1, 출력크기, 문자수;
    static boolean eraro;
    static int 클래스토큰, 클래스상수, 부모상수, 코드상수;
    static int[] 함수이름 = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] 함수인수이름 = new int[512], 함수인수형 = new int[512];
    static int[] 함수본문 = new int[32], 함수끝 = new int[32], 함수코드 = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], 함수명상수 = new int[32], 함수서술 = new int[32];
    static int[] 함수권한 = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] 지역이름 = new int[128], 지역형 = new int[128], 지역깊이 = new int[128];

    static void 실패(String 이유) {
        if (!eraro) {
            사용자.Skribo("javac error: "); 사용자.Skribo(이유);
            사용자.Skribo(" at line ");
            int Linio = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : 원문크기;
            for (int 수 = 0; 수 < 끝; 수++) if (FONTO[수] == 10) Linio++;
            자바도구.수쓰기(Linio); 사용자.문자쓰기(10);
        }
        eraro = true;
    }
    static boolean 글자(int 값) { return 문자이름규칙.첫글자(값); }
    static boolean 숫자(int 값) { return 값 >= '0' && 값 <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || 토큰길이[가] != 토큰길이[나]) return false;
        for (int 수 = 0; 수 < 토큰길이[가]; 수++) if (FONTO[토큰위치[가] + 수] != FONTO[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean 단어(int 토큰, String 말) {
        if (토큰 < 0 || 토큰 >= 토큰수 || 토큰길이[토큰] != 말.length()) return false;
        for (int 수 = 0; 수 < 말.length(); 수++) if (FONTO[토큰위치[토큰] + 수] != 말.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int 값) { if (종류() != 값) return false; 위치++; return true; }
    static void 요구(int 값) { if (!받기(값)) 실패("unexpected token"); }
    static boolean 말받기(String 말) { if (!단어(위치, 말)) return false; 위치++; return true; }
    static void 말요구(String 말) { if (!말받기(말)) 실패(말); }
    static int 식별자() {
        int 결과 = 위치;
        if (종류() != 256) 실패("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Ruli = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Ruli == 토큰길이[결과];
                for (int 칸 = Ruli; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != FONTO[토큰위치[결과] + 칸 - Ruli]) 같음 = false;
                if (같음) 실패("reserved word cannot be an identifier");
                Ruli = 수 + 1;
            }
        }
        return 결과;
    }
    static void 자르기() {
        int 수 = 0;
        while (수 < 원문크기 && !eraro) {
            int 값 = FONTO[수], Ruli = 수, 종류 = 값;
            if (값 == 32 || 값 == 9 || 값 == 10 || 값 == 13) { 수++; continue; }
            if (값 == '/' && 수 + 1 < 원문크기 && FONTO[수 + 1] == '/') {
                while (수 < 원문크기 && FONTO[수] != 10) 수++;
                continue;
            }
            if (값 == '/' && 수 + 1 < 원문크기 && FONTO[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < 원문크기 && !(FONTO[수] == '*' && FONTO[수 + 1] == '/')) 수++;
                if (수 + 1 >= 원문크기) { 실패("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (글자(값)) { 종류 = 256; while (수 < 원문크기 && 문자이름규칙.이어진글자(FONTO[수])) 수++; }
            else if (숫자(값)) { 종류 = 257; while (수 < 원문크기 && 숫자(FONTO[수])) 수++; }
            else if (값 == '"' || 값 == '\'') {
                종류 = 값 == '"' ? 258 : 259; 수++;
                while (수 < 원문크기 && FONTO[수] != 값 && FONTO[수] != 10 && FONTO[수] != 13) {
                    if (FONTO[수] == '\\') 수++;
                    수++;
                }
                if (수 >= 원문크기 || FONTO[수] != 값) { 실패("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < 원문크기) {
                    int 다음 = FONTO[수];
                    if (값 == '=' && 다음 == '=') 종류 = 300;
                    if (값 == '!' && 다음 == '=') 종류 = 301;
                    if (값 == '<' && 다음 == '=') 종류 = 302;
                    if (값 == '>' && 다음 == '=') 종류 = 303;
                    if (값 == '&' && 다음 == '&') 종류 = 304;
                    if (값 == '|' && 다음 == '|') 종류 = 305;
                    if (값 == '+' && 다음 == '+') 종류 = 306;
                    if (값 == '-' && 다음 == '-') 종류 = 307;
                    if (값 == '+' && 다음 == '=') 종류 = 308;
                    if (값 == '-' && 다음 == '=') 종류 = 309;
                    if (값 == '*' && 다음 == '=') 종류 = 310;
                    if (값 == '/' && 다음 == '=') 종류 = 311;
                    if (값 == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { 실패("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = Ruli; 토큰길이[토큰수++] = 수 - Ruli;
        }
    }
    static void 상바(int 값) {
        if (상수크기 == 상수.length) { 실패("constant pool too large"); return; }
        상수[상수크기++] = 값 & 255;
    }
    static void 상짧(int 값) { 상바(값 >> 8); 상바(값); }
    static int 상등록(int Ruli) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = 상수위치[수], 길이 = (수 + 1 < 상수수 ? 상수위치[수 + 1] : Ruli) - 앞;
            if (길이 != 상수크기 - Ruli) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (상수[앞 + 칸] != 상수[Ruli + 칸]) 같음 = false;
            if (같음) { 상수크기 = Ruli; return 수; }
        }
        if (상수수 == 상수위치.length) { 실패("too many constants"); return 0; }
        상수위치[상수수] = Ruli;
        return 상수수++;
    }
    static void 글추가(int 값) {
        if (문자수 == 문자.length) { 실패("text too long"); return; }
        문자[문자수++] = 값;
    }
    static void 말추가(String 말) { for (int 수 = 0; 수 < 말.length(); 수++) 글추가(말.charAt(수)); }
    static int 문자상수() {
        int Ruli = 상수크기; 상바(1); 상짧(0);
        for (int 수 = 0; 수 < 문자수; 수++) {
            int 값 = 문자[수];
            if (값 > 0 && 값 < 128) 상바(값);
            else if (값 < 2048) { 상바(192 | 값 >> 6); 상바(128 | 값 & 63); }
            else { 상바(224 | 값 >> 12); 상바(128 | 값 >> 6 & 63); 상바(128 | 값 & 63); }
        }
        if (eraro) return 0;
        int 길이 = 상수크기 - Ruli - 3;
        상수[Ruli + 1] = 길이 >> 8; 상수[Ruli + 2] = 길이 & 255;
        return 상등록(Ruli);
    }
    static int 말상수(String 말) { 문자수 = 0; 말추가(말); return 문자상수(); }
    static int 토큰상수(int 토큰) {
        문자수 = 0;
        for (int 수 = 0; 수 < 토큰길이[토큰]; 수++) 글추가(FONTO[토큰위치[토큰] + 수]);
        return 문자상수();
    }
    static int 참조(int 종류, int 가, int 나) {
        int Ruli = 상수크기; 상바(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return 상등록(Ruli);
    }
    static int 외부참조(int 종류, String 소유, String Nomo, String 서술) {
        int 주인 = 참조(7, 말상수(소유), 0);
        int 이름수 = 말상수(Nomo), 형식수 = 말상수(서술);
        return 참조(종류, 주인, 참조(12, 이름수, 형식수));
    }
    static void 내보내기(int 값) {
        if (코드크기 == 코드.length) { 실패("bytecode too large"); return; }
        코드[코드크기++] = 값 & 255;
    }
    static void Komando(int 값, int Argumentoj) { 내보내기(값); 내보내기(Argumentoj >> 8); 내보내기(Argumentoj); }
    static void 수상수(int 값) {
        if (값 >= -1 && 값 <= 5) { 내보내기(값 + 3); return; }
        int Ruli = 상수크기; 상바(3); 상짧(값 >>> 16); 상짧(값);
        Komando(19, 상등록(Ruli));
    }
    static int 분기(int Komando) { int 결과 = 코드크기; Komando(Komando, 0); return 결과; }
    static void 잇기(int 분기, int 목표) {
        if (eraro) return;
        int 거리 = 목표 - 분기;
        if (거리 < -32768 || 거리 > 32767 || 분기 < 0 || 분기 + 2 >= 코드크기) { 실패("invalid branch"); return; }
        코드[분기 + 1] = 거리 >> 8 & 255; 코드[분기 + 2] = 거리 & 255;
    }
    static void 비교값(int Komando) {
        int 참 = 분기(Komando); 내보내기(3); int 끝 = 분기(167);
        잇기(참, 코드크기); 내보내기(4); 잇기(끝, 코드크기);
    }
    static int 형식() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        실패("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void 형식추가(int 형) {
        if (형 == 0) 글추가('V');
        if (형 == 1) 글추가('I');
        if (형 == 2) 글추가('Z');
        if (형 == 3) 말추가("Ljava/lang/String;");
        if (형 == 4) 말추가("[Ljava/lang/String;");
        if (형 == 5) 글추가('C');
        if (형 == 6) 말추가("Ljava/io/FileInputStream;");
        if (형 == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 처리 본문은 호스트 javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("배열저장예외") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        실패("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (단어(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) 실패("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); 클래스토큰 = 식별자();
        클래스상수 = 참조(7, 토큰상수(클래스토큰), 0);
        부모상수 = 참조(7, 말상수("java/lang/Object"), 0); 코드상수 = 말상수("Code"); 요구('{');
        while (!eraro && 종류() != '}') {
            if (함수수 == 32) { 실패("too many methods"); break; }
            int 접근 = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int 함수 = 함수수++;
            함수권한[함수] = 접근 | 8;
            함수반환[함수] = 형식(); 함수이름[함수] = 식별자(); 요구('(');
            for (int 앞 = 0; 앞 < 함수; 앞++) if (이름같음(함수이름[앞], 함수이름[함수])) 실패("duplicate method (overloading unsupported)");
            while (!eraro && 종류() != ')') {
                int 수 = 함수인수수[함수];
                if (수 == 16) { 실패("too many parameters"); break; }
                int 형 = 형식(); if (형 == 0) 실패("void parameter");
                함수인수형[함수 * 16 + 수] = 형; 함수인수이름[함수 * 16 + 수] = 식별자();
                함수인수수[함수]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!eraro && 받기(','));
            }
            함수본문[함수] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) 실패("unclosed method body");
            함수끝[함수] = 위치;
            함수명상수[함수] = 토큰상수(함수이름[함수]);
            문자수 = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[함수]; 수++) 형식추가(함수인수형[함수 * 16 + 수]);
            글추가(')'); 형식추가(함수반환[함수]); 함수서술[함수] = 문자상수();
        }
        요구('}'); if (위치 != 토큰수) 실패("extra input after class");
    }
    static int 지역찾기(int Nomo) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(지역이름[수], Nomo)) return 수;
        실패("unknown variable"); return 0;
    }
    static int 지역추가(int Nomo, int 형) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(지역이름[수], Nomo)) 실패("duplicate local variable");
        if (지역수 == 128) { 실패("too many locals"); return 0; }
        지역이름[지역수] = Nomo; 지역형[지역수] = 형; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean 정수형(int 형) { return 형 == 1 || 형 == 5; }
    static void 지역읽기(int 수) { 내보내기(지역형[수] <= 2 || 지역형[수] == 5 ? 21 : 25); 내보내기(수); }
    static void 지역쓰기(int 수) { 내보내기(지역형[수] <= 2 || 지역형[수] == 5 ? 54 : 58); 내보내기(수); }
    static void 형확인(int 실제, int 기대) { if (실제 != 기대 && !(실제 == 5 && 기대 == 1)) 실패("type mismatch"); }
    static void 문자읽기(int 토큰) {
        문자수 = 0; int Ruli = 토큰위치[토큰] + 1, 끝 = 토큰위치[토큰] + 토큰길이[토큰] - 1;
        while (Ruli < 끝 && !eraro) {
            int 값 = FONTO[Ruli++];
            if (값 == '\\') {
                if (Ruli == 끝) { 실패("invalid escape"); break; }
                값 = FONTO[Ruli++];
                if (값 == 'n') 값 = 10;
                else if (값 == 'r') 값 = 13;
                else if (값 == 't') 값 = 9;
                else if (값 == 'b') 값 = 8;
                else if (값 == 'f') 값 = 12;
                else if (값 != '\\' && 값 != '"' && 값 != '\'') 실패("unsupported escape");
            }
            글추가(값);
        }
    }
    static int 정수읽기(int 토큰, boolean 음수) {
        if (토큰길이[토큰] > 1 && FONTO[토큰위치[토큰]] == '0') 실패("octal literals unsupported");
        int 값 = 0;
        for (int 수 = 0; 수 < 토큰길이[토큰]; 수++) {
            int 숫 = FONTO[토큰위치[토큰] + 수] - '0';
            if (값 < -214748364 || 값 == -214748364 && 숫 > (음수 ? 8 : 7)) 실패("integer literal out of range");
            값 = 값 * 10 - 숫;
        }
        return 음수 ? 값 : -값;
    }
    static int 기본식() {
        if (말받기("new")) {
            int 형 = 형식();
            if (형 != 6 && 형 != 7) { 실패("only file streams supported by new in source"); return 0; }
            String 소유 = 형 == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Komando(187, 참조(7, 말상수(소유), 0)); 내보내기(89);
            요구('('); 형확인(식(), 3); boolean 이어 = false;
            if (받기(',')) { if (형 != 7) 실패("input stream constructor arguments"); 형확인(식(), 2); 이어 = true; }
            요구(')');
            Komando(183, 외부참조(10, 소유, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return 형;
        }
        if (받기('(')) { int 형 = 식(); 요구(')'); return 형; }
        if (종류() == 257) { 수상수(정수읽기(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); Komando(19, 참조(8, 문자상수(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (문자수 != 1) 실패("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String 소유 = "", 메서드 = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("Eligo")) {
                소유 = "한국어/자체/Eligo"; 요구('.');
                if (말받기("줄쓰기")) { 메서드 = "줄쓰기"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("Skribo")) { 메서드 = "Skribo"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { 메서드 = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else 실패("unknown Korean output method");
            } else if (말받기("문자")) {
                소유 = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("길이")) { 메서드 = "길이"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { 메서드 = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("정수읽기")) { 메서드 = "정수읽기"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("정수쓰기")) { 메서드 = "정수쓰기"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { 메서드 = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("붙이기")) { 메서드 = "붙이기"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("자르기")) { 메서드 = "자르기"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else 실패("unknown Korean text method");
            } else if (말받기("Dosiero")) {
                소유 = "한국어/자체/Dosiero"; 요구('.'); 가 = 3;
                if (말받기("Lego")) { 메서드 = "Lego"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("Skribo")) { 메서드 = "Skribo"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else 실패("unknown Korean file method");
            } else if (말받기("화면")) {
                소유 = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { 메서드 = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { 메서드 = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { 메서드 = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { 메서드 = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { 메서드 = "기다리기"; 서술 = "()V"; }
                else 실패("unknown Korean framebuffer method");
            } else 실패("unsupported Korean library class");
            요구('('); if (가 != 0) 형확인(식(), 가);
            if (나 != 0) { 요구(','); 형확인(식(), 나); }
            if (다 != 0) { 요구(','); 형확인(식(), 다); }
            if (라 != 0) { 요구(','); 형확인(식(), 라); }
            if (마 != 0) { 요구(','); 형확인(식(), 마); }
            요구(')'); Komando(184, 외부참조(10, 소유, 메서드, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); 형확인(식(), 3); 요구(')');
            Komando(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nomo = 식별자();
        if (받기('(')) {
            int 함수 = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Nomo, 함수이름[수])) 함수 = 수;
            if (함수 < 0) { 실패("unknown static method"); return 0; }
            int 수 = 0;
            while (!eraro && 종류() != ')') {
                if (수 >= 함수인수수[함수]) { 실패("too many arguments"); break; }
                형확인(식(), 함수인수형[함수 * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[함수]) 실패("argument count mismatch");
            Komando(184, 참조(10, 클래스상수, 참조(12, 함수명상수[함수], 함수서술[함수])));
            return 함수반환[함수];
        }
        int 지역 = 지역찾기(Nomo), 형 = 지역형[지역]; 지역읽기(지역);
        while (!eraro) {
            if (받기('[')) { 형확인(형, 4); 형확인(식(), 1); 요구(']'); 내보내기(50); 형 = 3; }
            else if (받기('.')) {
                if (형 == 6 || 형 == 7) {
                    String 소유 = 형 == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); Komando(182, 외부참조(10, 소유, "close", "()V")); 형 = 0; }
                    else if (형 == 6 && 말받기("read")) { 요구('('); 요구(')'); Komando(182, 외부참조(10, 소유, "read", "()I")); 형 = 1; }
                    else if (형 == 7 && 말받기("write")) { 요구('('); 형확인(식(), 1); 요구(')'); Komando(182, 외부참조(10, 소유, "write", "(I)V")); 형 = 0; }
                    else { 실패("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (형 == 4) { 내보내기(190); 형 = 1; }
                else { 형확인(형, 3); 요구('('); 요구(')'); Komando(182, 외부참조(10, "java/lang/String", "length", "()I")); 형 = 1; }
            } else break;
        }
        return 형;
    }
    static int 단항() {
        if (++식깊이 > 64) { 실패("expression nesting too deep"); 식깊이--; return 0; }
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
        while (!eraro && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int 부호 = 종류(); 위치++; 형확인(형, 1); 형확인(단항(), 1);
            내보내기(부호 == '*' ? 104 : 부호 == '/' ? 108 : 112); 형 = 1;
        }
        return 형;
    }
    static int 합식() {
        int 형 = 곱식();
        while (!eraro && (종류() == '+' || 종류() == '-')) {
            int 부호 = 종류(); 위치++; int 경계 = 코드크기, 뒤형 = 곱식();
            if (부호 == '+' && (형 == 3 || 뒤형 == 3)) { 결합(경계, 형, 뒤형); 형 = 3; }
            else { 형확인(형, 1); 형확인(뒤형, 1); 내보내기(부호 == '+' ? 96 : 100); 형 = 1; }
        }
        return 형;
    }
    static int 붙임참조(int 형) {
        if (형 != 1 && 형 != 2 && 형 != 3 && 형 != 5) 실패("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", 형 == 1 ? "(I)Ljava/lang/StringBuilder;"
            : 형 == 2 ? "(Z)Ljava/lang/StringBuilder;" : 형 == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int 뒤형) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 식 내부의 상대 분기 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        Komando(187, 참조(7, 말상수("java/lang/StringBuilder"), 0)); 내보내기(89);
        Komando(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Komando(182, 붙임참조(앞형));
        if (eraro) return;
        int 길이 = 코드크기 - 끝;
        for (int 수 = 0; 수 < 길이; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + 길이] = 코드[수];
        for (int 수 = 0; 수 < 길이; 수++) 코드[경계 + 수] = 삽입코드[수];
        Komando(182, 붙임참조(뒤형)); Komando(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int 형 = 합식();
        while (!eraro && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int 부호 = 종류(); 위치++; 형확인(형, 1); 형확인(합식(), 1);
            비교값(부호 == '<' ? 161 : 부호 == '>' ? 163 : 부호 == 302 ? 164 : 162); 형 = 2;
        }
        return 형;
    }
    static int 동등식() {
        int 형 = 비교식();
        while (!eraro && (종류() == 300 || 종류() == 301)) {
            int 부호 = 종류(); 위치++; int 뒤형 = 비교식();
            if (형 == 0 || 뒤형 == 0) 실패("void expression");
            if (!(정수형(형) && 정수형(뒤형))) 형확인(뒤형, 형);
            비교값((형 <= 2 || 형 == 5 ? 159 : 165) + (부호 == 301 ? 1 : 0)); 형 = 2;
        }
        return 형;
    }
    static int 논리곱() {
        int 형 = 동등식();
        while (!eraro && 받기(304)) {
            형확인(형, 2); int 가 = 분기(153); 형확인(동등식(), 2); int 나 = 분기(153);
            내보내기(4); int 끝 = 분기(167); 잇기(가, 코드크기); 잇기(나, 코드크기); 내보내기(3); 잇기(끝, 코드크기); 형 = 2;
        }
        return 형;
    }
    static int 식() {
        int 형 = 논리곱();
        while (!eraro && 받기(305)) {
            형확인(형, 2); int 가 = 분기(154); 형확인(논리곱(), 2); int 나 = 분기(154);
            내보내기(3); int 끝 = 분기(167); 잇기(가, 코드크기); 잇기(나, 코드크기); 내보내기(4); 잇기(끝, 코드크기); 형 = 2;
        }
        return 형;
    }
    static void 대입(boolean 선언허용) {
        if (단어(위치, "int") || 단어(위치, "boolean") || 단어(위치, "String") || 단어(위치, "char")
            || 단어(위치, "FileInputStream") || 단어(위치, "FileOutputStream")) {
            if (!선언허용) 실패("declaration not allowed here");
            int 형 = 형식(), Nomo = 식별자(); 요구('='); 형확인(식(), 형);
            지역쓰기(지역추가(Nomo, 형)); return;
        }
        int Nomo = 식별자(), 지역 = 지역찾기(Nomo);
        if (받기('=')) { 형확인(식(), 지역형[지역]); 지역쓰기(지역); }
        else if (종류() >= 308 && 종류() <= 312) {
            int 부호 = 종류(); 위치++; 지역읽기(지역); int 경계 = 코드크기, 뒤형 = 식();
            if (부호 == 308 && 지역형[지역] == 3) 결합(경계, 3, 뒤형);
            else {
                형확인(지역형[지역], 1); 형확인(뒤형, 1);
                내보내기(부호 == 308 ? 96 : 부호 == 309 ? 100 : 부호 == 310 ? 104 : 부호 == 311 ? 108 : 112);
                if (지역형[지역] == 5) 내보내기(146);
            }
            지역쓰기(지역);
        }
        else if (종류() == 306 || 종류() == 307) {
            형확인(지역형[지역], 1); 내보내기(132); 내보내기(지역); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (지역형[지역] == 5) { 지역읽기(지역); 내보내기(146); 지역쓰기(지역); }
        } else 실패("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Komando(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int 형 = 빈인수 ? 0 : 식(); 요구(')'); 요구(';');
        String 서술 = 형 == 0 ? "()V" : 형 == 1 ? "(I)V" : 형 == 2 ? "(Z)V" : 형 == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (형 == 4 || 형 >= 6 || 형 == 0 && (!줄바꿈 || !빈인수)) 실패("unsupported print argument");
        Komando(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean 문장() {
        if (eraro) return false;
        if (깊이 > 32) { 실패("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!eraro && 종류() != '}') { if (반환) 실패("unreachable statement"); 반환 = 문장(); }
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
            깊이++; boolean 가 = 제어문(); 깊이--;
            if (말받기("else")) { int 끝 = 분기(167); 잇기(거짓, 코드크기); 깊이++; boolean 나 = 제어문(); 깊이--; 잇기(끝, 코드크기); return 가 && 나; }
            잇기(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int Ruli = 코드크기; 요구('('); 형확인(식(), 2); 요구(')'); int 끝 = 분기(153);
            깊이++; 제어문(); 깊이--; 잇기(분기(167), Ruli); 잇기(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') 대입(true); 요구(';');
            int 조건 = 코드크기; if (종류() == ';') 내보내기(4); else 형확인(식(), 2); 요구(';');
            int 끝 = 분기(153), 본문 = 분기(167), 갱신 = 코드크기;
            if (종류() != ')') 대입(false); 요구(')'); 잇기(분기(167), 조건); 잇기(본문, 코드크기);
            제어문(); 잇기(분기(167), 갱신); 잇기(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (단어(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int 형 = 식(); if (형 != 0) 내보내기(87); 요구(';'); return false;
        }
        대입(true); 요구(';'); return false;
    }
    static boolean 제어문() {
        if (단어(위치, "int") || 단어(위치, "boolean") || 단어(위치, "char") || 단어(위치, "String")
            || 단어(위치, "FileInputStream") || 단어(위치, "FileOutputStream")) 실패("local declaration requires braces");
        return 문장();
    }
    static void 출바(int 값) { if (출력크기 == Eligo.length) 실패("class file too large"); else Eligo[출력크기++] = 값 & 255; }
    static void 출짧(int 값) { 출바(값 >> 8); 출바(값); }
    static void 출정(int 값) { 출짧(값 >>> 16); 출짧(값); }
    static void 클래스쓰기() {
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
    public static int Ruli() {
        if (사용자.인수개수() == 1 && 자바도구.같음(사용자.Argumentoj(0), "-version")) {
            사용자.Skribo("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (사용자.인수개수() != 1) { 사용자.Skribo("Usage: javac FILE.java\n"); return 2; }
        int 이름크기 = 자바도구.Nomo(파일명, 사용자.Argumentoj(0));
        if (이름크기 < 6 || 이름크기 > 62 || 파일명[이름크기 - 5] != '.' || 파일명[이름크기 - 4] != 'j'
            || 파일명[이름크기 - 3] != 'a' || 파일명[이름크기 - 2] != 'v' || 파일명[이름크기 - 1] != 'a') {
            사용자.Skribo("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        원문크기 = 사용자.파일읽기(파일명, FONTO);
        if (원문크기 < 0) { 사용자.Skribo("javac: cannot read source: "); 자바도구.수쓰기(원문크기); 사용자.문자쓰기(10); return 1; }
        원문크기 = 자바도구.원문해독(FONTO, 원문크기);
        if (원문크기 < 0) { 사용자.Skribo("javac error: invalid UTF-8 source\n"); return 1; }
        자르기(); if (!eraro) 선언읽기();
        if (!eraro) {
            if (토큰길이[클래스토큰] != 이름크기 - 5) 실패("class name must match file name");
            for (int 수 = 0; 수 < 이름크기 - 5; 수++) if (FONTO[토큰위치[클래스토큰] + 수] != 파일명[수]) 실패("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !eraro; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) 지역추가(함수인수이름[현재함수 * 16 + 수], 함수인수형[현재함수 * 16 + 수]);
            boolean 반환 = 문장();
            if (!반환 && 함수반환[현재함수] != 0) 실패("missing return");
            // 분기 뒤의 합류 지점은 반드시 실제 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean 정수 = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(정수 ? 3 : 1); 내보내기(정수 ? 172 : 176); }
            if (위치 != 함수끝[현재함수]) 실패("invalid method body");
            함수지역[현재함수] = 지역수; 함수길이[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (eraro) return 1;
        클래스쓰기(); if (eraro) return 1;
        파일명[이름크기 - 4] = 'c'; 파일명[이름크기 - 3] = 'l'; 파일명[이름크기 - 2] = 'a';
        파일명[이름크기 - 1] = 's'; 파일명[이름크기] = 's'; 파일명[이름크기 + 1] = 0;
        int 결과 = 사용자.파일쓰기(파일명, Eligo, 출력크기);
        if (결과 < 0) { 사용자.Skribo("javac: cannot save class: "); 자바도구.수쓰기(결과); 사용자.문자쓰기(10); return 1; }
        사용자.Skribo("Compiled: "); for (int 수 = 0; 파일명[수] != 0; 수++) 사용자.문자쓰기(파일명[수]);
        사용자.Skribo(" (JVM class version 49)\n"); return 0;
    }
}
