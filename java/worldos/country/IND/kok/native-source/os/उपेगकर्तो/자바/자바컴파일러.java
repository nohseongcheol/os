// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java स्त्रोत_ट्री -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] स्त्रोत = new int[16384], 출력 = new int[16384], CODE_मोल = new int[4096];
    static int[] 토큰종류 = new int[2048], टोकन_स्थिती = new int[2048], टोकन_लांबाय = new int[2048];
    static int[] अचल_मोल = new int[4096], अचल_ऑफसॅट = new int[512];
    static int[] 문자 = new int[512], फायल_नांव_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int स्त्रोत_आवाठ, टोकन_COUNT, स्थिती, CODE_आवाठ, अचल_आवाठ, अचल_COUNT = 1, 출력크기, वर्ण_लांबाय;
    static boolean चूक;
    static int वर्ग_टोकन, वर्ग_अचल, 부모상수, CODE_अचल;
    static int[] पद्दत_प्रवेश_नांव = new int[32], पद्दत_return = new int[32], पद्दत_युक्तीवाद_COUNT = new int[32];
    static int[] पद्दत_युक्तीवाद_नांव = new int[512], पद्दत_युक्तीवाद_TYPE = new int[512];
    static int[] 함수본문 = new int[32], पद्दत_सोपोवचें = new int[32], पद्दत_CODE = new int[32];
    static int[] पद्दत_लांबाय = new int[32], 함수지역 = new int[32], पद्दत_नांव_अचल = new int[32], 함수서술 = new int[32];
    static int[] पद्दत_ऍक्सॅस = new int[32];
    static int पद्दत_COUNT, 현재함수, थळावो_COUNT, 깊이, 식깊이;
    static int[] थळावो_नांव = new int[128], थळावो_TYPE = new int[128], 지역깊이 = new int[128];

    static void अपेस_मोल(String 이유) {
        if (!चूक) {
            उपेगकर्तो.बरोवचें("javac error: "); उपेगकर्तो.बरोवचें(이유);
            उपेगकर्तो.बरोवचें(" at line ");
            int रेग = 1, 끝 = स्थिती < टोकन_COUNT ? टोकन_स्थिती[स्थिती] : स्त्रोत_आवाठ;
            for (int 수 = 0; 수 < 끝; 수++) if (स्त्रोत[수] == 10) रेग++;
            자바도구.수쓰기(रेग); उपेगकर्तो.बरोवचें_वर्ण_मोल(10);
        }
        चूक = true;
    }
    static boolean वर्ण_मोल(int मोल) { return 문자이름규칙.첫글자(मोल); }
    static boolean अंक_मोल(int मोल) { return मोल >= '0' && मोल <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= टोकन_COUNT || 나 >= टोकन_COUNT || टोकन_लांबाय[가] != टोकन_लांबाय[나]) return false;
        for (int 수 = 0; 수 < टोकन_लांबाय[가]; 수++) if (स्त्रोत[टोकन_स्थिती[가] + 수] != स्त्रोत[टोकन_स्थिती[나] + 수]) return false;
        return true;
    }
    static boolean Word_मोल(int टोकन_मोल, String Word_SMS) {
        if (टोकन_मोल < 0 || टोकन_मोल >= टोकन_COUNT || टोकन_लांबाय[टोकन_मोल] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (स्त्रोत[टोकन_स्थिती[टोकन_मोल] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return स्थिती < टोकन_COUNT ? 토큰종류[स्थिती] : 0; }
    static boolean 받기(int मोल) { if (종류() != मोल) return false; स्थिती++; return true; }
    static void 요구(int मोल) { if (!받기(मोल)) अपेस_मोल("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_मोल(स्थिती, Word_SMS)) return false; स्थिती++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) अपेस_मोल(Word_SMS); }
    static int वळखुपी_मोल() {
        int मेजप = स्थिती;
        if (종류() != 256) अपेस_मोल("identifier required"); else स्थिती++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int चलोवप = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - चलोवप == टोकन_लांबाय[मेजप];
                for (int स्लॉट_प्रवेश = चलोवप; 같음 && स्लॉट_प्रवेश < 수; स्लॉट_प्रवेश++) if (예약어.charAt(स्लॉट_प्रवेश) != स्त्रोत[टोकन_स्थिती[मेजप] + स्लॉट_प्रवेश - चलोवप]) 같음 = false;
                if (같음) अपेस_मोल("reserved word cannot be an identifier");
                चलोवप = 수 + 1;
            }
        }
        return मेजप;
    }
    static void कातरप_मोल() {
        int 수 = 0;
        while (수 < स्त्रोत_आवाठ && !चूक) {
            int मोल = स्त्रोत[수], चलोवप = 수, 종류 = मोल;
            if (मोल == 32 || मोल == 9 || मोल == 10 || मोल == 13) { 수++; continue; }
            if (मोल == '/' && 수 + 1 < स्त्रोत_आवाठ && स्त्रोत[수 + 1] == '/') {
                while (수 < स्त्रोत_आवाठ && स्त्रोत[수] != 10) 수++;
                continue;
            }
            if (मोल == '/' && 수 + 1 < स्त्रोत_आवाठ && स्त्रोत[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < स्त्रोत_आवाठ && !(स्त्रोत[수] == '*' && स्त्रोत[수 + 1] == '/')) 수++;
                if (수 + 1 >= स्त्रोत_आवाठ) { अपेस_मोल("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (वर्ण_मोल(मोल)) { 종류 = 256; while (수 < स्त्रोत_आवाठ && 문자이름규칙.이어진글자(स्त्रोत[수])) 수++; }
            else if (अंक_मोल(मोल)) { 종류 = 257; while (수 < स्त्रोत_आवाठ && अंक_मोल(स्त्रोत[수])) 수++; }
            else if (मोल == '"' || मोल == '\'') {
                종류 = मोल == '"' ? 258 : 259; 수++;
                while (수 < स्त्रोत_आवाठ && स्त्रोत[수] != मोल && स्त्रोत[수] != 10 && स्त्रोत[수] != 13) {
                    if (स्त्रोत[수] == '\\') 수++;
                    수++;
                }
                if (수 >= स्त्रोत_आवाठ || स्त्रोत[수] != मोल) { अपेस_मोल("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < स्त्रोत_आवाठ) {
                    int फुडलें_आयटम = स्त्रोत[수];
                    if (मोल == '=' && फुडलें_आयटम == '=') 종류 = 300;
                    if (मोल == '!' && फुडलें_आयटम == '=') 종류 = 301;
                    if (मोल == '<' && फुडलें_आयटम == '=') 종류 = 302;
                    if (मोल == '>' && फुडलें_आयटम == '=') 종류 = 303;
                    if (मोल == '&' && फुडलें_आयटम == '&') 종류 = 304;
                    if (मोल == '|' && फुडलें_आयटम == '|') 종류 = 305;
                    if (मोल == '+' && फुडलें_आयटम == '+') 종류 = 306;
                    if (मोल == '-' && फुडलें_आयटम == '-') 종류 = 307;
                    if (मोल == '+' && फुडलें_आयटम == '=') 종류 = 308;
                    if (मोल == '-' && फुडलें_आयटम == '=') 종류 = 309;
                    if (मोल == '*' && फुडलें_आयटम == '=') 종류 = 310;
                    if (मोल == '/' && फुडलें_आयटम == '=') 종류 = 311;
                    if (मोल == '%' && फुडलें_आयटम == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (टोकन_COUNT == 토큰종류.length - 1) { अपेस_मोल("too many tokens (2047 maximum)"); break; }
            토큰종류[टोकन_COUNT] = 종류; टोकन_स्थिती[टोकन_COUNT] = चलोवप; टोकन_लांबाय[टोकन_COUNT++] = 수 - चलोवप;
        }
    }
    static void बरोवचें_अचल_बायट(int मोल) {
        if (अचल_आवाठ == अचल_मोल.length) { अपेस_मोल("constant pool too large"); return; }
        अचल_मोल[अचल_आवाठ++] = मोल & 255;
    }
    static void 상짧(int मोल) { बरोवचें_अचल_बायट(मोल >> 8); बरोवचें_अचल_बायट(मोल); }
    static int नोंदणी_अचल(int चलोवप) {
        for (int 수 = 1; 수 < अचल_COUNT; 수++) {
            int 앞 = अचल_ऑफसॅट[수], लांबाय_मोल = (수 + 1 < अचल_COUNT ? अचल_ऑफसॅट[수 + 1] : चलोवप) - 앞;
            if (लांबाय_मोल != अचल_आवाठ - चलोवप) continue;
            boolean 같음 = true;
            for (int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < लांबाय_मोल; स्लॉट_प्रवेश++) if (अचल_मोल[앞 + स्लॉट_प्रवेश] != अचल_मोल[चलोवप + स्लॉट_प्रवेश]) 같음 = false;
            if (같음) { अचल_आवाठ = चलोवप; return 수; }
        }
        if (अचल_COUNT == अचल_ऑफसॅट.length) { अपेस_मोल("too many constants"); return 0; }
        अचल_ऑफसॅट[अचल_COUNT] = चलोवप;
        return अचल_COUNT++;
    }
    static void 글추가(int मोल) {
        if (वर्ण_लांबाय == 문자.length) { अपेस_मोल("text too long"); return; }
        문자[वर्ण_लांबाय++] = मोल;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int वर्ण_अचल() {
        int चलोवप = अचल_आवाठ; बरोवचें_अचल_बायट(1); 상짧(0);
        for (int 수 = 0; 수 < वर्ण_लांबाय; 수++) {
            int मोल = 문자[수];
            if (मोल > 0 && मोल < 128) बरोवचें_अचल_बायट(मोल);
            else if (मोल < 2048) { बरोवचें_अचल_बायट(192 | मोल >> 6); बरोवचें_अचल_बायट(128 | मोल & 63); }
            else { बरोवचें_अचल_बायट(224 | मोल >> 12); बरोवचें_अचल_बायट(128 | मोल >> 6 & 63); बरोवचें_अचल_बायट(128 | मोल & 63); }
        }
        if (चूक) return 0;
        int लांबाय_मोल = अचल_आवाठ - चलोवप - 3;
        अचल_मोल[चलोवप + 1] = लांबाय_मोल >> 8; अचल_मोल[चलोवप + 2] = लांबाय_मोल & 255;
        return नोंदणी_अचल(चलोवप);
    }
    static int Word_अचल(String Word_SMS) { वर्ण_लांबाय = 0; 말추가(Word_SMS); return वर्ण_अचल(); }
    static int टोकन_अचल(int टोकन_मोल) {
        वर्ण_लांबाय = 0;
        for (int 수 = 0; 수 < टोकन_लांबाय[टोकन_मोल]; 수++) 글추가(स्त्रोत[टोकन_स्थिती[टोकन_मोल] + 수]);
        return वर्ण_अचल();
    }
    static int संदर्भ(int 종류, int 가, int 나) {
        int चलोवप = अचल_आवाठ; बरोवचें_अचल_बायट(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return नोंदणी_अचल(चलोवप);
    }
    static int 외부참조(int 종류, String धनी_मोल, String नांव, String 서술) {
        int धनी_वळखुपी = संदर्भ(7, Word_अचल(धनी_मोल), 0);
        int नांव_COUNT = Word_अचल(नांव), स्वरूप_COUNT = Word_अचल(서술);
        return संदर्भ(종류, धनी_वळखुपी, संदर्भ(12, नांव_COUNT, स्वरूप_COUNT));
    }
    static void 내보내기(int मोल) {
        if (CODE_आवाठ == CODE_मोल.length) { अपेस_मोल("bytecode too large"); return; }
        CODE_मोल[CODE_आवाठ++] = मोल & 255;
    }
    static void आदेश(int मोल, int 인수) { 내보내기(मोल); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int मोल) {
        if (मोल >= -1 && मोल <= 5) { 내보내기(मोल + 3); return; }
        int चलोवप = अचल_आवाठ; बरोवचें_अचल_बायट(3); 상짧(मोल >>> 16); 상짧(मोल);
        आदेश(19, नोंदणी_अचल(चलोवप));
    }
    static int शाखा(int आदेश) { int मेजप = CODE_आवाठ; आदेश(आदेश, 0); return मेजप; }
    static void लिंक_मोल(int शाखा, int लक्ष्य_ऑब्जॅक्ट) {
        if (चूक) return;
        int 거리 = लक्ष्य_ऑब्जॅक्ट - शाखा;
        if (거리 < -32768 || 거리 > 32767 || शाखा < 0 || शाखा + 2 >= CODE_आवाठ) { अपेस_मोल("invalid branch"); return; }
        CODE_मोल[शाखा + 1] = 거리 >> 8 & 255; CODE_मोल[शाखा + 2] = 거리 & 255;
    }
    static void 비교값(int आदेश) {
        int TRUE_मोल = शाखा(आदेश); 내보내기(3); int 끝 = शाखा(167);
        लिंक_मोल(TRUE_मोल, CODE_आवाठ); 내보내기(4); लिंक_मोल(끝, CODE_आवाठ);
    }
    static int स्वरूप_मोल() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        अपेस_मोल("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void संयोजन_करचें_स्वरूप(int TYPE_मोल) {
        if (TYPE_मोल == 0) 글추가('V');
        if (TYPE_मोल == 1) 글추가('I');
        if (TYPE_मोल == 2) 글추가('Z');
        if (TYPE_मोल == 3) 말추가("Ljava/lang/String;");
        if (TYPE_मोल == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_मोल == 5) 글추가('C');
        if (TYPE_मोल == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_मोल == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 प्रक्रिया_मोल_प्रवेश 본문은 येजमान javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("예외") || TAKE_Word("실행예외") || TAKE_Word("입출력예외") || TAKE_Word("대기시간초과예외") || TAKE_Word("주소확인예외") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("잘못된인수예외") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("빈참조예외") || TAKE_Word("산술예외") || TAKE_Word("상태예외") || TAKE_Word("형변환예외") || TAKE_Word("음수배열크기예외") || TAKE_Word("क्रम_Store_अपेस") || TAKE_Word("가닥상태예외") || TAKE_Word("대기중단예외")) return;
        अपेस_मोल("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_मोल(स्थिती, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) अपेस_मोल("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); वर्ग_टोकन = वळखुपी_मोल();
        वर्ग_अचल = संदर्भ(7, टोकन_अचल(वर्ग_टोकन), 0);
        부모상수 = संदर्भ(7, Word_अचल("java/lang/Object"), 0); CODE_अचल = Word_अचल("Code"); 요구('{');
        while (!चूक && 종류() != '}') {
            if (पद्दत_COUNT == 32) { अपेस_मोल("too many methods"); break; }
            int ऍक्सॅस_प्रवेश = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int फंक्शन_मोल = पद्दत_COUNT++;
            पद्दत_ऍक्सॅस[फंक्शन_मोल] = ऍक्सॅस_प्रवेश | 8;
            पद्दत_return[फंक्शन_मोल] = स्वरूप_मोल(); पद्दत_प्रवेश_नांव[फंक्शन_मोल] = वळखुपी_मोल(); 요구('(');
            for (int 앞 = 0; 앞 < फंक्शन_मोल; 앞++) if (이름같음(पद्दत_प्रवेश_नांव[앞], पद्दत_प्रवेश_नांव[फंक्शन_मोल])) अपेस_मोल("duplicate method (overloading unsupported)");
            while (!चूक && 종류() != ')') {
                int 수 = पद्दत_युक्तीवाद_COUNT[फंक्शन_मोल];
                if (수 == 16) { अपेस_मोल("too many parameters"); break; }
                int TYPE_मोल = स्वरूप_मोल(); if (TYPE_मोल == 0) अपेस_मोल("void parameter");
                पद्दत_युक्तीवाद_TYPE[फंक्शन_मोल * 16 + 수] = TYPE_मोल; पद्दत_युक्तीवाद_नांव[फंक्शन_मोल * 16 + 수] = वळखुपी_मोल();
                पद्दत_युक्तीवाद_COUNT[फंक्शन_मोल]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!चूक && 받기(','));
            }
            함수본문[फंक्शन_मोल] = स्थिती; 요구('{');
            int 중첩 = 1;
            while (स्थिती < टोकन_COUNT && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                स्थिती++;
            }
            if (중첩 != 0) अपेस_मोल("unclosed method body");
            पद्दत_सोपोवचें[फंक्शन_मोल] = स्थिती;
            पद्दत_नांव_अचल[फंक्शन_मोल] = टोकन_अचल(पद्दत_प्रवेश_नांव[फंक्शन_मोल]);
            वर्ण_लांबाय = 0; 글추가('(');
            for (int 수 = 0; 수 < पद्दत_युक्तीवाद_COUNT[फंक्शन_मोल]; 수++) संयोजन_करचें_स्वरूप(पद्दत_युक्तीवाद_TYPE[फंक्शन_मोल * 16 + 수]);
            글추가(')'); संयोजन_करचें_स्वरूप(पद्दत_return[फंक्शन_मोल]); 함수서술[फंक्शन_मोल] = वर्ण_अचल();
        }
        요구('}'); if (स्थिती != टोकन_COUNT) अपेस_मोल("extra input after class");
    }
    static int FIND_थळावो(int नांव) {
        for (int 수 = थळावो_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(थळावो_नांव[수], नांव)) return 수;
        अपेस_मोल("unknown variable"); return 0;
    }
    static int संयोजन_करचें_थळावो(int नांव, int TYPE_मोल) {
        for (int 수 = 0; 수 < थळावो_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(थळावो_नांव[수], नांव)) अपेस_मोल("duplicate local variable");
        if (थळावो_COUNT == 128) { अपेस_मोल("too many locals"); return 0; }
        थळावो_नांव[थळावो_COUNT] = नांव; थळावो_TYPE[थळावो_COUNT] = TYPE_मोल; 지역깊이[थळावो_COUNT] = 깊이;
        return थळावो_COUNT++;
    }
    static boolean पुर्णांक_TYPE(int TYPE_मोल) { return TYPE_मोल == 1 || TYPE_मोल == 5; }
    static void 지역읽기(int 수) { 내보내기(थळावो_TYPE[수] <= 2 || थळावो_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void बरोवचें_थळावो(int 수) { 내보내기(थळावो_TYPE[수] <= 2 || थळावो_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void पुनर्तपासणी_करची_TYPE(int प्रत्यक्ष_डेटा, int 기대) { if (प्रत्यक्ष_डेटा != 기대 && !(प्रत्यक्ष_डेटा == 5 && 기대 == 1)) अपेस_मोल("type mismatch"); }
    static void 문자읽기(int टोकन_मोल) {
        वर्ण_लांबाय = 0; int चलोवप = टोकन_स्थिती[टोकन_मोल] + 1, 끝 = टोकन_स्थिती[टोकन_मोल] + टोकन_लांबाय[टोकन_मोल] - 1;
        while (चलोवप < 끝 && !चूक) {
            int मोल = स्त्रोत[चलोवप++];
            if (मोल == '\\') {
                if (चलोवप == 끝) { अपेस_मोल("invalid escape"); break; }
                मोल = स्त्रोत[चलोवप++];
                if (मोल == 'n') मोल = 10;
                else if (मोल == 'r') मोल = 13;
                else if (मोल == 't') मोल = 9;
                else if (मोल == 'b') मोल = 8;
                else if (मोल == 'f') मोल = 12;
                else if (मोल != '\\' && मोल != '"' && मोल != '\'') अपेस_मोल("unsupported escape");
            }
            글추가(मोल);
        }
    }
    static int व्याकरणी_फोडणिशी_पुर्णांक(int टोकन_मोल, boolean 음수) {
        if (टोकन_लांबाय[टोकन_मोल] > 1 && स्त्रोत[टोकन_स्थिती[टोकन_मोल]] == '0') अपेस_मोल("octal literals unsupported");
        int मोल = 0;
        for (int 수 = 0; 수 < टोकन_लांबाय[टोकन_मोल]; 수++) {
            int अंक_आयटम = स्त्रोत[टोकन_स्थिती[टोकन_मोल] + 수] - '0';
            if (मोल < -214748364 || मोल == -214748364 && अंक_आयटम > (음수 ? 8 : 7)) अपेस_मोल("integer literal out of range");
            मोल = मोल * 10 - अंक_आयटम;
        }
        return 음수 ? मोल : -मोल;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_मोल = स्वरूप_मोल();
            if (TYPE_मोल != 6 && TYPE_मोल != 7) { अपेस_मोल("only file streams supported by new in source"); return 0; }
            String धनी_मोल = TYPE_मोल == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            आदेश(187, संदर्भ(7, Word_अचल(धनी_मोल), 0)); 내보내기(89);
            요구('('); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_मोल != 7) अपेस_मोल("input stream constructor arguments"); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 2); 이어 = true; }
            요구(')');
            आदेश(183, 외부참조(10, धनी_मोल, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_मोल;
        }
        if (받기('(')) { int TYPE_मोल = ऍक्सप्रॅशन_मोल(); 요구(')'); return TYPE_मोल; }
        if (종류() == 257) { 수상수(व्याकरणी_फोडणिशी_पुर्णांक(स्थिती++, false)); return 1; }
        if (종류() == 258) { 문자읽기(स्थिती++); आदेश(19, संदर्भ(8, वर्ण_अचल(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(स्थिती++); if (वर्ण_लांबाय != 1) अपेस_मोल("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String धनी_मोल = "", पद्दत_मोल = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, मेजप = 0;
            if (TAKE_Word("출력")) {
                धनी_मोल = "한국어/자체/출력"; 요구('.');
                if (TAKE_Word("बरोवचें_रेग")) { पद्दत_मोल = "बरोवचें_रेग"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("बरोवचें")) { पद्दत_मोल = "बरोवचें"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { पद्दत_मोल = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else अपेस_मोल("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                धनी_मोल = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("लांबाय_मोल")) { पद्दत_मोल = "लांबाय_मोल"; 서술 = "(Ljava/lang/String;)I"; मेजप = 1; }
                else if (TAKE_Word("वर्ण_कोड_COUNT")) { पद्दत_मोल = "वर्ण_कोड_COUNT"; 서술 = "(Ljava/lang/String;)I"; मेजप = 1; }
                else if (TAKE_Word("व्याकरणी_फोडणिशी_पुर्णांक")) { पद्दत_मोल = "व्याकरणी_फोडणिशी_पुर्णांक"; 서술 = "(Ljava/lang/String;)I"; मेजप = 1; }
                else if (TAKE_Word("बरोवचें_पुर्णांक_मोल")) { पद्दत_मोल = "बरोवचें_पुर्णांक_मोल"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; मेजप = 3; }
                else if (TAKE_Word("같음")) { पद्दत_मोल = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; मेजप = 2; }
                else if (TAKE_Word("दसोवचें_SMS")) { पद्दत_मोल = "दसोवचें_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; मेजप = 3; }
                else if (TAKE_Word("कातरप_मोल")) { पद्दत_मोल = "कातरप_मोल"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; मेजप = 3; }
                else अपेस_मोल("unknown Korean text method");
            } else if (TAKE_Word("फायल")) {
                धनी_मोल = "한국어/자체/फायल"; 요구('.'); 가 = 3;
                if (TAKE_Word("읽기")) { पद्दत_मोल = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; मेजप = 3; }
                else if (TAKE_Word("बरोवचें")) { पद्दत_मोल = "बरोवचें"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else अपेस_मोल("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                धनी_मोल = "한국어/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { पद्दत_मोल = "너비"; 서술 = "()I"; मेजप = 1; }
                else if (TAKE_Word("높이")) { पद्दत_मोल = "높이"; 서술 = "()I"; मेजप = 1; }
                else if (TAKE_Word("사각형")) { पद्दत_मोल = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("지우기")) { पद्दत_मोल = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { पद्दत_मोल = "기다리기"; 서술 = "()V"; }
                else अपेस_मोल("unknown Korean framebuffer method");
            } else अपेस_मोल("unsupported Korean library class");
            요구('('); if (가 != 0) पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 가);
            if (나 != 0) { 요구(','); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 나); }
            if (다 != 0) { 요구(','); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 다); }
            if (라 != 0) { 요구(','); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 라); }
            if (마 != 0) { 요구(','); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 마); }
            요구(')'); आदेश(184, 외부참조(10, धनी_मोल, पद्दत_मोल, 서술)); return मेजप;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 3); 요구(')');
            आदेश(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int नांव = वळखुपी_मोल();
        if (받기('(')) {
            int फंक्शन_मोल = -1;
            for (int 수 = 0; 수 < पद्दत_COUNT; 수++) if (이름같음(नांव, पद्दत_प्रवेश_नांव[수])) फंक्शन_मोल = 수;
            if (फंक्शन_मोल < 0) { अपेस_मोल("unknown static method"); return 0; }
            int 수 = 0;
            while (!चूक && 종류() != ')') {
                if (수 >= पद्दत_युक्तीवाद_COUNT[फंक्शन_मोल]) { अपेस_मोल("too many arguments"); break; }
                पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), पद्दत_युक्तीवाद_TYPE[फंक्शन_मोल * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != पद्दत_युक्तीवाद_COUNT[फंक्शन_मोल]) अपेस_मोल("argument count mismatch");
            आदेश(184, संदर्भ(10, वर्ग_अचल, संदर्भ(12, पद्दत_नांव_अचल[फंक्शन_मोल], 함수서술[फंक्शन_मोल])));
            return पद्दत_return[फंक्शन_मोल];
        }
        int थळावो_मळ = FIND_थळावो(नांव), TYPE_मोल = थळावो_TYPE[थळावो_मळ]; 지역읽기(थळावो_मळ);
        while (!चूक) {
            if (받기('[')) { पुनर्तपासणी_करची_TYPE(TYPE_मोल, 4); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 1); 요구(']'); 내보내기(50); TYPE_मोल = 3; }
            else if (받기('.')) {
                if (TYPE_मोल == 6 || TYPE_मोल == 7) {
                    String धनी_मोल = TYPE_मोल == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); आदेश(182, 외부참조(10, धनी_मोल, "close", "()V")); TYPE_मोल = 0; }
                    else if (TYPE_मोल == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); आदेश(182, 외부참조(10, धनी_मोल, "read", "()I")); TYPE_मोल = 1; }
                    else if (TYPE_मोल == 7 && TAKE_Word("write")) { 요구('('); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 1); 요구(')'); आदेश(182, 외부참조(10, धनी_मोल, "write", "(I)V")); TYPE_मोल = 0; }
                    else { अपेस_मोल("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_मोल == 4) { 내보내기(190); TYPE_मोल = 1; }
                else { पुनर्तपासणी_करची_TYPE(TYPE_मोल, 3); 요구('('); 요구(')'); आदेश(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_मोल = 1; }
            } else break;
        }
        return TYPE_मोल;
    }
    static int 단항() {
        if (++식깊이 > 64) { अपेस_मोल("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_मोल;
        if (받기('!')) { पुनर्तपासणी_करची_TYPE(단항(), 2); 비교값(153); TYPE_मोल = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(व्याकरणी_फोडणिशी_पुर्णांक(स्थिती++, true));
            else { पुनर्तपासणी_करची_TYPE(단항(), 1); 내보내기(116); }
            TYPE_मोल = 1;
        } else if (받기('+')) { पुनर्तपासणी_करची_TYPE(단항(), 1); TYPE_मोल = 1; }
        else TYPE_मोल = 기본식();
        식깊이--; return TYPE_मोल;
    }
    static int 곱식() {
        int TYPE_मोल = 단항();
        while (!चूक && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int एनकोडिंग_मोल = 종류(); स्थिती++; पुनर्तपासणी_करची_TYPE(TYPE_मोल, 1); पुनर्तपासणी_करची_TYPE(단항(), 1);
            내보내기(एनकोडिंग_मोल == '*' ? 104 : एनकोडिंग_मोल == '/' ? 108 : 112); TYPE_मोल = 1;
        }
        return TYPE_मोल;
    }
    static int 합식() {
        int TYPE_मोल = 곱식();
        while (!चूक && (종류() == '+' || 종류() == '-')) {
            int एनकोडिंग_मोल = 종류(); स्थिती++; int 경계 = CODE_आवाठ, फाटीं_मोल_TYPE = 곱식();
            if (एनकोडिंग_मोल == '+' && (TYPE_मोल == 3 || फाटीं_मोल_TYPE == 3)) { 결합(경계, TYPE_मोल, फाटीं_मोल_TYPE); TYPE_मोल = 3; }
            else { पुनर्तपासणी_करची_TYPE(TYPE_मोल, 1); पुनर्तपासणी_करची_TYPE(फाटीं_मोल_TYPE, 1); 내보내기(एनकोडिंग_मोल == '+' ? 96 : 100); TYPE_मोल = 1; }
        }
        return TYPE_मोल;
    }
    static int 붙임참조(int TYPE_मोल) {
        if (TYPE_मोल != 1 && TYPE_मोल != 2 && TYPE_मोल != 3 && TYPE_मोल != 5) अपेस_मोल("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_मोल == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_मोल == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_मोल == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int फाटीं_मोल_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_मोल 앞에 तयार_करचें 코드를 삽입한다.
        // RIGHT ऍक्सप्रॅशन_मोल 내부의 पीयर_मोल शाखा 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_आवाठ;
        आदेश(187, संदर्भ(7, Word_अचल("java/lang/StringBuilder"), 0)); 내보내기(89);
        आदेश(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); आदेश(182, 붙임참조(앞형));
        if (चूक) return;
        int लांबाय_मोल = CODE_आवाठ - 끝;
        for (int 수 = 0; 수 < लांबाय_मोल; 수++) 삽입코드[수] = CODE_मोल[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_मोल[수 + लांबाय_मोल] = CODE_मोल[수];
        for (int 수 = 0; 수 < लांबाय_मोल; 수++) CODE_मोल[경계 + 수] = 삽입코드[수];
        आदेश(182, 붙임참조(फाटीं_मोल_TYPE)); आदेश(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int TYPE_मोल = 합식();
        while (!चूक && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int एनकोडिंग_मोल = 종류(); स्थिती++; पुनर्तपासणी_करची_TYPE(TYPE_मोल, 1); पुनर्तपासणी_करची_TYPE(합식(), 1);
            비교값(एनकोडिंग_मोल == '<' ? 161 : एनकोडिंग_मोल == '>' ? 163 : एनकोडिंग_मोल == 302 ? 164 : 162); TYPE_मोल = 2;
        }
        return TYPE_मोल;
    }
    static int 동등식() {
        int TYPE_मोल = 비교식();
        while (!चूक && (종류() == 300 || 종류() == 301)) {
            int एनकोडिंग_मोल = 종류(); स्थिती++; int फाटीं_मोल_TYPE = 비교식();
            if (TYPE_मोल == 0 || फाटीं_मोल_TYPE == 0) अपेस_मोल("void expression");
            if (!(पुर्णांक_TYPE(TYPE_मोल) && पुर्णांक_TYPE(फाटीं_मोल_TYPE))) पुनर्तपासणी_करची_TYPE(फाटीं_मोल_TYPE, TYPE_मोल);
            비교값((TYPE_मोल <= 2 || TYPE_मोल == 5 ? 159 : 165) + (एनकोडिंग_मोल == 301 ? 1 : 0)); TYPE_मोल = 2;
        }
        return TYPE_मोल;
    }
    static int 논리곱() {
        int TYPE_मोल = 동등식();
        while (!चूक && 받기(304)) {
            पुनर्तपासणी_करची_TYPE(TYPE_मोल, 2); int 가 = शाखा(153); पुनर्तपासणी_करची_TYPE(동등식(), 2); int 나 = शाखा(153);
            내보내기(4); int 끝 = शाखा(167); लिंक_मोल(가, CODE_आवाठ); लिंक_मोल(나, CODE_आवाठ); 내보내기(3); लिंक_मोल(끝, CODE_आवाठ); TYPE_मोल = 2;
        }
        return TYPE_मोल;
    }
    static int ऍक्सप्रॅशन_मोल() {
        int TYPE_मोल = 논리곱();
        while (!चूक && 받기(305)) {
            पुनर्तपासणी_करची_TYPE(TYPE_मोल, 2); int 가 = शाखा(154); पुनर्तपासणी_करची_TYPE(논리곱(), 2); int 나 = शाखा(154);
            내보내기(3); int 끝 = शाखा(167); लिंक_मोल(가, CODE_आवाठ); लिंक_मोल(나, CODE_आवाठ); 내보내기(4); लिंक_मोल(끝, CODE_आवाठ); TYPE_मोल = 2;
        }
        return TYPE_मोल;
    }
    static void प्रकल्प_मोल(boolean 선언허용) {
        if (Word_मोल(स्थिती, "int") || Word_मोल(स्थिती, "boolean") || Word_मोल(स्थिती, "String") || Word_मोल(स्थिती, "char")
            || Word_मोल(स्थिती, "FileInputStream") || Word_मोल(स्थिती, "FileOutputStream")) {
            if (!선언허용) अपेस_मोल("declaration not allowed here");
            int TYPE_मोल = स्वरूप_मोल(), नांव = वळखुपी_मोल(); 요구('='); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), TYPE_मोल);
            बरोवचें_थळावो(संयोजन_करचें_थळावो(नांव, TYPE_मोल)); return;
        }
        int नांव = वळखुपी_मोल(), थळावो_मळ = FIND_थळावो(नांव);
        if (받기('=')) { पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), थळावो_TYPE[थळावो_मळ]); बरोवचें_थळावो(थळावो_मळ); }
        else if (종류() >= 308 && 종류() <= 312) {
            int एनकोडिंग_मोल = 종류(); स्थिती++; 지역읽기(थळावो_मळ); int 경계 = CODE_आवाठ, फाटीं_मोल_TYPE = ऍक्सप्रॅशन_मोल();
            if (एनकोडिंग_मोल == 308 && थळावो_TYPE[थळावो_मळ] == 3) 결합(경계, 3, फाटीं_मोल_TYPE);
            else {
                पुनर्तपासणी_करची_TYPE(थळावो_TYPE[थळावो_मळ], 1); पुनर्तपासणी_करची_TYPE(फाटीं_मोल_TYPE, 1);
                내보내기(एनकोडिंग_मोल == 308 ? 96 : एनकोडिंग_मोल == 309 ? 100 : एनकोडिंग_मोल == 310 ? 104 : एनकोडिंग_मोल == 311 ? 108 : 112);
                if (थळावो_TYPE[थळावो_मळ] == 5) 내보내기(146);
            }
            बरोवचें_थळावो(थळावो_मळ);
        }
        else if (종류() == 306 || 종류() == 307) {
            पुनर्तपासणी_करची_TYPE(थळावो_TYPE[थळावो_मळ], 1); 내보내기(132); 내보내기(थळावो_मळ); 내보내기(종류() == 306 ? 1 : 255); स्थिती++;
            if (थळावो_TYPE[थळावो_मळ] == 5) { 지역읽기(थळावो_मळ); 내보내기(146); बरोवचें_थळावो(थळावो_मळ); }
        } else अपेस_मोल("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        आदेश(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean रिकामें_युक्तीवाद = 종류() == ')';
        int TYPE_मोल = रिकामें_युक्तीवाद ? 0 : ऍक्सप्रॅशन_मोल(); 요구(')'); 요구(';');
        String 서술 = TYPE_मोल == 0 ? "()V" : TYPE_मोल == 1 ? "(I)V" : TYPE_मोल == 2 ? "(Z)V" : TYPE_मोल == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_मोल == 4 || TYPE_मोल >= 6 || TYPE_मोल == 0 && (!줄바꿈 || !रिकामें_युक्तीवाद)) अपेस_मोल("unsupported print argument");
        आदेश(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean निवेदन_मोल() {
        if (चूक) return false;
        if (깊이 > 32) { अपेस_मोल("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean return_मेजप = false;
            while (!चूक && 종류() != '}') { if (return_मेजप) अपेस_मोल("unreachable statement"); return_मेजप = निवेदन_मोल(); }
            요구('}'); for (int 수 = 0; 수 < थळावो_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return return_मेजप;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_मोल = 종류() == ';' ? 0 : ऍक्सप्रॅशन_मोल(); पुनर्तपासणी_करची_TYPE(TYPE_मोल, पद्दत_return[현재함수]); 요구(';');
            내보내기(TYPE_मोल == 0 ? 177 : TYPE_मोल <= 2 || TYPE_मोल == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 2); 요구(')'); int FALSE_मोल = शाखा(153);
            깊이++; boolean 가 = नियंत्रण_निवेदन(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = शाखा(167); लिंक_मोल(FALSE_मोल, CODE_आवाठ); 깊이++; boolean 나 = नियंत्रण_निवेदन(); 깊이--; लिंक_मोल(끝, CODE_आवाठ); return 가 && 나; }
            लिंक_मोल(FALSE_मोल, CODE_आवाठ); return false;
        }
        if (TAKE_Word("while")) {
            int चलोवप = CODE_आवाठ; 요구('('); पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 2); 요구(')'); int 끝 = शाखा(153);
            깊이++; नियंत्रण_निवेदन(); 깊이--; लिंक_मोल(शाखा(167), चलोवप); लिंक_मोल(끝, CODE_आवाठ); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') प्रकल्प_मोल(true); 요구(';');
            int स्थिती_291ac971 = CODE_आवाठ; if (종류() == ';') 내보내기(4); else पुनर्तपासणी_करची_TYPE(ऍक्सप्रॅशन_मोल(), 2); 요구(';');
            int 끝 = शाखा(153), देखीचो_उतारो = शाखा(167), परतून_ताजें_करचें = CODE_आवाठ;
            if (종류() != ')') प्रकल्प_मोल(false); 요구(')'); लिंक_मोल(शाखा(167), स्थिती_291ac971); लिंक_मोल(देखीचो_उतारो, CODE_आवाठ);
            नियंत्रण_निवेदन(); लिंक_मोल(शाखा(167), परतून_ताजें_करचें); लिंक_मोल(끝, CODE_आवाठ);
            for (int 수 = 0; 수 < थळावो_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_मोल(स्थिती, "System")) { 화면출력(); return false; }
        if (종류() == 256 && स्थिती + 1 < टोकन_COUNT && (토큰종류[स्थिती + 1] == '(' || 토큰종류[स्थिती + 1] == '.')) {
            int TYPE_मोल = ऍक्सप्रॅशन_मोल(); if (TYPE_मोल != 0) 내보내기(87); 요구(';'); return false;
        }
        प्रकल्प_मोल(true); 요구(';'); return false;
    }
    static boolean नियंत्रण_निवेदन() {
        if (Word_मोल(स्थिती, "int") || Word_मोल(स्थिती, "boolean") || Word_मोल(स्थिती, "char") || Word_मोल(स्थिती, "String")
            || Word_मोल(स्थिती, "FileInputStream") || Word_मोल(स्थिती, "FileOutputStream")) अपेस_मोल("local declaration requires braces");
        return निवेदन_मोल();
    }
    static void 출바(int मोल) { if (출력크기 == 출력.length) अपेस_मोल("class file too large"); else 출력[출력크기++] = मोल & 255; }
    static void 출짧(int मोल) { 출바(मोल >> 8); 출바(मोल); }
    static void 출정(int मोल) { 출짧(मोल >>> 16); 출짧(मोल); }
    static void बरोवचें_वर्ग() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(अचल_COUNT);
        for (int 수 = 0; 수 < अचल_आवाठ; 수++) 출바(अचल_मोल[수]);
        출짧(0x21); 출짧(वर्ग_अचल); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(पद्दत_COUNT);
        for (int 수 = 0; 수 < पद्दत_COUNT; 수++) {
            출짧(पद्दत_ऍक्सॅस[수]); 출짧(पद्दत_नांव_अचल[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_अचल);
            출정(12 + पद्दत_लांबाय[수]); 출짧(128); 출짧(함수지역[수]); 출정(पद्दत_लांबाय[수]);
            for (int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < पद्दत_लांबाय[수]; स्लॉट_प्रवेश++) 출바(CODE_मोल[पद्दत_CODE[수] + स्लॉट_प्रवेश]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int चलोवप() {
        if (उपेगकर्तो.인수개수() == 1 && 자바도구.같음(उपेगकर्तो.인수(0), "-version")) {
            उपेगकर्तो.बरोवचें("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (उपेगकर्तो.인수개수() != 1) { उपेगकर्तो.बरोवचें("Usage: javac FILE.java\n"); return 2; }
        int नांव_आवाठ = 자바도구.नांव(फायल_नांव_SMS, उपेगकर्तो.인수(0));
        if (नांव_आवाठ < 6 || नांव_आवाठ > 62 || फायल_नांव_SMS[नांव_आवाठ - 5] != '.' || फायल_नांव_SMS[नांव_आवाठ - 4] != 'j'
            || फायल_नांव_SMS[नांव_आवाठ - 3] != 'a' || फायल_नांव_SMS[नांव_आवाठ - 2] != 'v' || फायल_नांव_SMS[नांव_आवाठ - 1] != 'a') {
            उपेगकर्तो.बरोवचें("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        स्त्रोत_आवाठ = उपेगकर्तो.파일읽기(फायल_नांव_SMS, स्त्रोत);
        if (स्त्रोत_आवाठ < 0) { उपेगकर्तो.बरोवचें("javac: cannot read source: "); 자바도구.수쓰기(स्त्रोत_आवाठ); उपेगकर्तो.बरोवचें_वर्ण_मोल(10); return 1; }
        स्त्रोत_आवाठ = 자바도구.원문해독(स्त्रोत, स्त्रोत_आवाठ);
        if (स्त्रोत_आवाठ < 0) { उपेगकर्तो.बरोवचें("javac error: invalid UTF-8 source\n"); return 1; }
        कातरप_मोल(); if (!चूक) 선언읽기();
        if (!चूक) {
            if (टोकन_लांबाय[वर्ग_टोकन] != नांव_आवाठ - 5) अपेस_मोल("class name must match file name");
            for (int 수 = 0; 수 < नांव_आवाठ - 5; 수++) if (स्त्रोत[टोकन_स्थिती[वर्ग_टोकन] + 수] != फायल_नांव_SMS[수]) अपेस_मोल("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < पद्दत_COUNT && !चूक; 현재함수++) {
            स्थिती = 함수본문[현재함수]; पद्दत_CODE[현재함수] = CODE_आवाठ; थळावो_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < पद्दत_युक्तीवाद_COUNT[현재함수]; 수++) संयोजन_करचें_थळावो(पद्दत_युक्तीवाद_नांव[현재함수 * 16 + 수], पद्दत_युक्तीवाद_TYPE[현재함수 * 16 + 수]);
            boolean return_मेजप = निवेदन_मोल();
            if (!return_मेजप && पद्दत_return[현재함수] != 0) अपेस_मोल("missing return");
            // शाखा 뒤의 합류 지점은 반드시 प्रत्यक्ष_डेटा 명령이어야 한다 (버전 49 검증기).
            if (पद्दत_return[현재함수] == 0) 내보내기(177);
            else { boolean पुर्णांक = पद्दत_return[현재함수] <= 2 || पद्दत_return[현재함수] == 5; 내보내기(पुर्णांक ? 3 : 1); 내보내기(पुर्णांक ? 172 : 176); }
            if (स्थिती != पद्दत_सोपोवचें[현재함수]) अपेस_मोल("invalid method body");
            함수지역[현재함수] = थळावो_COUNT; पद्दत_लांबाय[현재함수] = CODE_आवाठ - पद्दत_CODE[현재함수];
        }
        if (चूक) return 1;
        बरोवचें_वर्ग(); if (चूक) return 1;
        फायल_नांव_SMS[नांव_आवाठ - 4] = 'c'; फायल_नांव_SMS[नांव_आवाठ - 3] = 'l'; फायल_नांव_SMS[नांव_आवाठ - 2] = 'a';
        फायल_नांव_SMS[नांव_आवाठ - 1] = 's'; फायल_नांव_SMS[नांव_आवाठ] = 's'; फायल_नांव_SMS[नांव_आवाठ + 1] = 0;
        int मेजप = उपेगकर्तो.बरोवचें_फायल(फायल_नांव_SMS, 출력, 출력크기);
        if (मेजप < 0) { उपेगकर्तो.बरोवचें("javac: cannot save class: "); 자바도구.수쓰기(मेजप); उपेगकर्तो.बरोवचें_वर्ण_मोल(10); return 1; }
        उपेगकर्तो.बरोवचें("Compiled: "); for (int 수 = 0; फायल_नांव_SMS[수] != 0; 수++) उपेगकर्तो.बरोवचें_वर्ण_मोल(फायल_नांव_SMS[수]);
        उपेगकर्तो.बरोवचें(" (JVM class version 49)\n"); return 0;
    }
}
