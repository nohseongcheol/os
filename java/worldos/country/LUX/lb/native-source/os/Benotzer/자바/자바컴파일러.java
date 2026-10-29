// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java Quell_Bamstruktur -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] Quell = new int[16384], 출력 = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], Token_positionéieren = new int[2048], Token_Längt = new int[2048];
    static int[] Konstant_VALUE = new int[4096], Konstant_OFFSET = new int[512];
    static int[] 문자 = new int[512], Fichier_Numm_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int Quell_d_Gréisst_veränneren, Token_COUNT, positionéieren, CODE_d_Gréisst_veränneren, Konstant_d_Gréisst_veränneren, Konstant_COUNT = 1, 출력크기, Zeechen_Längt;
    static boolean Feeler;
    static int Klass_Token, Klass_Konstant, 부모상수, CODE_Konstant;
    static int[] Method_Agab_Numm = new int[32], 함수반환 = new int[32], Method_Argument_COUNT = new int[32];
    static int[] Method_Argument_Numm = new int[512], Method_Argument_TYPE = new int[512];
    static int[] 함수본문 = new int[32], Method_bëennegen = new int[32], Method_CODE = new int[32];
    static int[] Method_Längt = new int[32], 함수지역 = new int[32], Method_Numm_Konstant = new int[32], 함수서술 = new int[32];
    static int[] Method_Zougrëff = new int[32];
    static int Method_COUNT, 현재함수, lokal_COUNT, 깊이, 식깊이;
    static int[] lokal_Numm = new int[128], lokal_TYPE = new int[128], 지역깊이 = new int[128];

    static void Feeler_VALUE(String 이유) {
        if (!Feeler) {
            Benotzer.schreiwen("javac error: "); Benotzer.schreiwen(이유);
            Benotzer.schreiwen(" at line ");
            int Zeil = 1, 끝 = positionéieren < Token_COUNT ? Token_positionéieren[positionéieren] : Quell_d_Gréisst_veränneren;
            for (int 수 = 0; 수 < 끝; 수++) if (Quell[수] == 10) Zeil++;
            자바도구.수쓰기(Zeil); Benotzer.schreiwen_Zeechen_VALUE(10);
        }
        Feeler = true;
    }
    static boolean Zeechen_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean Ziffer_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= Token_COUNT || 나 >= Token_COUNT || Token_Längt[가] != Token_Längt[나]) return false;
        for (int 수 = 0; 수 < Token_Längt[가]; 수++) if (Quell[Token_positionéieren[가] + 수] != Quell[Token_positionéieren[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int Token_VALUE, String Word_SMS) {
        if (Token_VALUE < 0 || Token_VALUE >= Token_COUNT || Token_Längt[Token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (Quell[Token_positionéieren[Token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return positionéieren < Token_COUNT ? 토큰종류[positionéieren] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; positionéieren++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) Feeler_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(positionéieren, Word_SMS)) return false; positionéieren++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) Feeler_VALUE(Word_SMS); }
    static int Identifikateur_VALUE() {
        int Mooss = positionéieren;
        if (종류() != 256) Feeler_VALUE("identifier required"); else positionéieren++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Laf = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Laf == Token_Längt[Mooss];
                for (int Slot_Agab = Laf; 같음 && Slot_Agab < 수; Slot_Agab++) if (예약어.charAt(Slot_Agab) != Quell[Token_positionéieren[Mooss] + Slot_Agab - Laf]) 같음 = false;
                if (같음) Feeler_VALUE("reserved word cannot be an identifier");
                Laf = 수 + 1;
            }
        }
        return Mooss;
    }
    static void schneiden_VALUE() {
        int 수 = 0;
        while (수 < Quell_d_Gréisst_veränneren && !Feeler) {
            int VALUE = Quell[수], Laf = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < Quell_d_Gréisst_veränneren && Quell[수 + 1] == '/') {
                while (수 < Quell_d_Gréisst_veränneren && Quell[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < Quell_d_Gréisst_veränneren && Quell[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < Quell_d_Gréisst_veränneren && !(Quell[수] == '*' && Quell[수 + 1] == '/')) 수++;
                if (수 + 1 >= Quell_d_Gréisst_veränneren) { Feeler_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (Zeechen_VALUE(VALUE)) { 종류 = 256; while (수 < Quell_d_Gréisst_veränneren && 문자이름규칙.이어진글자(Quell[수])) 수++; }
            else if (Ziffer_VALUE(VALUE)) { 종류 = 257; while (수 < Quell_d_Gréisst_veränneren && Ziffer_VALUE(Quell[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < Quell_d_Gréisst_veränneren && Quell[수] != VALUE && Quell[수] != 10 && Quell[수] != 13) {
                    if (Quell[수] == '\\') 수++;
                    수++;
                }
                if (수 >= Quell_d_Gréisst_veränneren || Quell[수] != VALUE) { Feeler_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < Quell_d_Gréisst_veränneren) {
                    int Weider_Element = Quell[수];
                    if (VALUE == '=' && Weider_Element == '=') 종류 = 300;
                    if (VALUE == '!' && Weider_Element == '=') 종류 = 301;
                    if (VALUE == '<' && Weider_Element == '=') 종류 = 302;
                    if (VALUE == '>' && Weider_Element == '=') 종류 = 303;
                    if (VALUE == '&' && Weider_Element == '&') 종류 = 304;
                    if (VALUE == '|' && Weider_Element == '|') 종류 = 305;
                    if (VALUE == '+' && Weider_Element == '+') 종류 = 306;
                    if (VALUE == '-' && Weider_Element == '-') 종류 = 307;
                    if (VALUE == '+' && Weider_Element == '=') 종류 = 308;
                    if (VALUE == '-' && Weider_Element == '=') 종류 = 309;
                    if (VALUE == '*' && Weider_Element == '=') 종류 = 310;
                    if (VALUE == '/' && Weider_Element == '=') 종류 = 311;
                    if (VALUE == '%' && Weider_Element == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (Token_COUNT == 토큰종류.length - 1) { Feeler_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[Token_COUNT] = 종류; Token_positionéieren[Token_COUNT] = Laf; Token_Längt[Token_COUNT++] = 수 - Laf;
        }
    }
    static void schreiwen_Konstant_Byte(int VALUE) {
        if (Konstant_d_Gréisst_veränneren == Konstant_VALUE.length) { Feeler_VALUE("constant pool too large"); return; }
        Konstant_VALUE[Konstant_d_Gréisst_veränneren++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { schreiwen_Konstant_Byte(VALUE >> 8); schreiwen_Konstant_Byte(VALUE); }
    static int registréieren_Konstant(int Laf) {
        for (int 수 = 1; 수 < Konstant_COUNT; 수++) {
            int 앞 = Konstant_OFFSET[수], Längt_VALUE = (수 + 1 < Konstant_COUNT ? Konstant_OFFSET[수 + 1] : Laf) - 앞;
            if (Längt_VALUE != Konstant_d_Gréisst_veränneren - Laf) continue;
            boolean 같음 = true;
            for (int Slot_Agab = 0; Slot_Agab < Längt_VALUE; Slot_Agab++) if (Konstant_VALUE[앞 + Slot_Agab] != Konstant_VALUE[Laf + Slot_Agab]) 같음 = false;
            if (같음) { Konstant_d_Gréisst_veränneren = Laf; return 수; }
        }
        if (Konstant_COUNT == Konstant_OFFSET.length) { Feeler_VALUE("too many constants"); return 0; }
        Konstant_OFFSET[Konstant_COUNT] = Laf;
        return Konstant_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (Zeechen_Längt == 문자.length) { Feeler_VALUE("text too long"); return; }
        문자[Zeechen_Längt++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int Zeechen_Konstant() {
        int Laf = Konstant_d_Gréisst_veränneren; schreiwen_Konstant_Byte(1); 상짧(0);
        for (int 수 = 0; 수 < Zeechen_Längt; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) schreiwen_Konstant_Byte(VALUE);
            else if (VALUE < 2048) { schreiwen_Konstant_Byte(192 | VALUE >> 6); schreiwen_Konstant_Byte(128 | VALUE & 63); }
            else { schreiwen_Konstant_Byte(224 | VALUE >> 12); schreiwen_Konstant_Byte(128 | VALUE >> 6 & 63); schreiwen_Konstant_Byte(128 | VALUE & 63); }
        }
        if (Feeler) return 0;
        int Längt_VALUE = Konstant_d_Gréisst_veränneren - Laf - 3;
        Konstant_VALUE[Laf + 1] = Längt_VALUE >> 8; Konstant_VALUE[Laf + 2] = Längt_VALUE & 255;
        return registréieren_Konstant(Laf);
    }
    static int Word_Konstant(String Word_SMS) { Zeechen_Längt = 0; 말추가(Word_SMS); return Zeechen_Konstant(); }
    static int Token_Konstant(int Token_VALUE) {
        Zeechen_Längt = 0;
        for (int 수 = 0; 수 < Token_Längt[Token_VALUE]; 수++) 글추가(Quell[Token_positionéieren[Token_VALUE] + 수]);
        return Zeechen_Konstant();
    }
    static int Referenzen(int 종류, int 가, int 나) {
        int Laf = Konstant_d_Gréisst_veränneren; schreiwen_Konstant_Byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return registréieren_Konstant(Laf);
    }
    static int 외부참조(int 종류, String Besëtzer_VALUE, String Numm, String 서술) {
        int Besëtzer_Identifikateur = Referenzen(7, Word_Konstant(Besëtzer_VALUE), 0);
        int Numm_COUNT = Word_Konstant(Numm), Format_COUNT = Word_Konstant(서술);
        return Referenzen(종류, Besëtzer_Identifikateur, Referenzen(12, Numm_COUNT, Format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_d_Gréisst_veränneren == CODE_VALUE.length) { Feeler_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_d_Gréisst_veränneren++] = VALUE & 255;
    }
    static void Befeel(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Laf = Konstant_d_Gréisst_veränneren; schreiwen_Konstant_Byte(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Befeel(19, registréieren_Konstant(Laf));
    }
    static int Branche(int Befeel) { int Mooss = CODE_d_Gréisst_veränneren; Befeel(Befeel, 0); return Mooss; }
    static void Link_VALUE(int Branche, int Zil_Objet) {
        if (Feeler) return;
        int 거리 = Zil_Objet - Branche;
        if (거리 < -32768 || 거리 > 32767 || Branche < 0 || Branche + 2 >= CODE_d_Gréisst_veränneren) { Feeler_VALUE("invalid branch"); return; }
        CODE_VALUE[Branche + 1] = 거리 >> 8 & 255; CODE_VALUE[Branche + 2] = 거리 & 255;
    }
    static void 비교값(int Befeel) {
        int TRUE_VALUE = Branche(Befeel); 내보내기(3); int 끝 = Branche(167);
        Link_VALUE(TRUE_VALUE, CODE_d_Gréisst_veränneren); 내보내기(4); Link_VALUE(끝, CODE_d_Gréisst_veränneren);
    }
    static int Format_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        Feeler_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void derbäisetzen_Format(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Prozess_VALUE_Agab 본문은 Host javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("예외") || TAKE_Word("실행예외") || TAKE_Word("입출력예외") || TAKE_Word("대기시간초과예외") || TAKE_Word("주소확인예외") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("잘못된인수예외") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("빈참조예외") || TAKE_Word("산술예외") || TAKE_Word("상태예외") || TAKE_Word("형변환예외") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_Feeler") || TAKE_Word("가닥상태예외") || TAKE_Word("대기중단예외")) return;
        Feeler_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(positionéieren, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) Feeler_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); Klass_Token = Identifikateur_VALUE();
        Klass_Konstant = Referenzen(7, Token_Konstant(Klass_Token), 0);
        부모상수 = Referenzen(7, Word_Konstant("java/lang/Object"), 0); CODE_Konstant = Word_Konstant("Code"); 요구('{');
        while (!Feeler && 종류() != '}') {
            if (Method_COUNT == 32) { Feeler_VALUE("too many methods"); break; }
            int Zougrëff_Agab = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = Method_COUNT++;
            Method_Zougrëff[FUNCTION_VALUE] = Zougrëff_Agab | 8;
            함수반환[FUNCTION_VALUE] = Format_VALUE(); Method_Agab_Numm[FUNCTION_VALUE] = Identifikateur_VALUE(); 요구('(');
            for (int 앞 = 0; 앞 < FUNCTION_VALUE; 앞++) if (이름같음(Method_Agab_Numm[앞], Method_Agab_Numm[FUNCTION_VALUE])) Feeler_VALUE("duplicate method (overloading unsupported)");
            while (!Feeler && 종류() != ')') {
                int 수 = Method_Argument_COUNT[FUNCTION_VALUE];
                if (수 == 16) { Feeler_VALUE("too many parameters"); break; }
                int TYPE_VALUE = Format_VALUE(); if (TYPE_VALUE == 0) Feeler_VALUE("void parameter");
                Method_Argument_TYPE[FUNCTION_VALUE * 16 + 수] = TYPE_VALUE; Method_Argument_Numm[FUNCTION_VALUE * 16 + 수] = Identifikateur_VALUE();
                Method_Argument_COUNT[FUNCTION_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!Feeler && 받기(','));
            }
            함수본문[FUNCTION_VALUE] = positionéieren; 요구('{');
            int 중첩 = 1;
            while (positionéieren < Token_COUNT && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                positionéieren++;
            }
            if (중첩 != 0) Feeler_VALUE("unclosed method body");
            Method_bëennegen[FUNCTION_VALUE] = positionéieren;
            Method_Numm_Konstant[FUNCTION_VALUE] = Token_Konstant(Method_Agab_Numm[FUNCTION_VALUE]);
            Zeechen_Längt = 0; 글추가('(');
            for (int 수 = 0; 수 < Method_Argument_COUNT[FUNCTION_VALUE]; 수++) derbäisetzen_Format(Method_Argument_TYPE[FUNCTION_VALUE * 16 + 수]);
            글추가(')'); derbäisetzen_Format(함수반환[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = Zeechen_Konstant();
        }
        요구('}'); if (positionéieren != Token_COUNT) Feeler_VALUE("extra input after class");
    }
    static int FIND_lokal(int Numm) {
        for (int 수 = lokal_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokal_Numm[수], Numm)) return 수;
        Feeler_VALUE("unknown variable"); return 0;
    }
    static int derbäisetzen_lokal(int Numm, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokal_Numm[수], Numm)) Feeler_VALUE("duplicate local variable");
        if (lokal_COUNT == 128) { Feeler_VALUE("too many locals"); return 0; }
        lokal_Numm[lokal_COUNT] = Numm; lokal_TYPE[lokal_COUNT] = TYPE_VALUE; 지역깊이[lokal_COUNT] = 깊이;
        return lokal_COUNT++;
    }
    static boolean Ganzzuel_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void schreiwen_lokal(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void verifizéieren_TYPE(int aktuell_Daten, int 기대) { if (aktuell_Daten != 기대 && !(aktuell_Daten == 5 && 기대 == 1)) Feeler_VALUE("type mismatch"); }
    static void 문자읽기(int Token_VALUE) {
        Zeechen_Längt = 0; int Laf = Token_positionéieren[Token_VALUE] + 1, 끝 = Token_positionéieren[Token_VALUE] + Token_Längt[Token_VALUE] - 1;
        while (Laf < 끝 && !Feeler) {
            int VALUE = Quell[Laf++];
            if (VALUE == '\\') {
                if (Laf == 끝) { Feeler_VALUE("invalid escape"); break; }
                VALUE = Quell[Laf++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') Feeler_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int analyséieren_Ganzzuel(int Token_VALUE, boolean 음수) {
        if (Token_Längt[Token_VALUE] > 1 && Quell[Token_positionéieren[Token_VALUE]] == '0') Feeler_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < Token_Längt[Token_VALUE]; 수++) {
            int Ziffer_Element = Quell[Token_positionéieren[Token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && Ziffer_Element > (음수 ? 8 : 7)) Feeler_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - Ziffer_Element;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = Format_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { Feeler_VALUE("only file streams supported by new in source"); return 0; }
            String Besëtzer_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Befeel(187, Referenzen(7, Word_Konstant(Besëtzer_VALUE), 0)); 내보내기(89);
            요구('('); verifizéieren_TYPE(Ausdrock_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) Feeler_VALUE("input stream constructor arguments"); verifizéieren_TYPE(Ausdrock_VALUE(), 2); 이어 = true; }
            요구(')');
            Befeel(183, 외부참조(10, Besëtzer_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = Ausdrock_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(analyséieren_Ganzzuel(positionéieren++, false)); return 1; }
        if (종류() == 258) { 문자읽기(positionéieren++); Befeel(19, Referenzen(8, Zeechen_Konstant(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(positionéieren++); if (Zeechen_Längt != 1) Feeler_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String Besëtzer_VALUE = "", Method_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, Mooss = 0;
            if (TAKE_Word("출력")) {
                Besëtzer_VALUE = "한국어/자체/출력"; 요구('.');
                if (TAKE_Word("schreiwen_Zeil")) { Method_VALUE = "schreiwen_Zeil"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("schreiwen")) { Method_VALUE = "schreiwen"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { Method_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else Feeler_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                Besëtzer_VALUE = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("Längt_VALUE")) { Method_VALUE = "Längt_VALUE"; 서술 = "(Ljava/lang/String;)I"; Mooss = 1; }
                else if (TAKE_Word("Zeechecode_COUNT")) { Method_VALUE = "Zeechecode_COUNT"; 서술 = "(Ljava/lang/String;)I"; Mooss = 1; }
                else if (TAKE_Word("analyséieren_Ganzzuel")) { Method_VALUE = "analyséieren_Ganzzuel"; 서술 = "(Ljava/lang/String;)I"; Mooss = 1; }
                else if (TAKE_Word("schreiwen_Ganzzuel_VALUE")) { Method_VALUE = "schreiwen_Ganzzuel_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; Mooss = 3; }
                else if (TAKE_Word("같음")) { Method_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; Mooss = 2; }
                else if (TAKE_Word("apechen_SMS")) { Method_VALUE = "apechen_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; Mooss = 3; }
                else if (TAKE_Word("schneiden_VALUE")) { Method_VALUE = "schneiden_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; Mooss = 3; }
                else Feeler_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Fichier")) {
                Besëtzer_VALUE = "한국어/자체/Fichier"; 요구('.'); 가 = 3;
                if (TAKE_Word("읽기")) { Method_VALUE = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; Mooss = 3; }
                else if (TAKE_Word("schreiwen")) { Method_VALUE = "schreiwen"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else Feeler_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                Besëtzer_VALUE = "한국어/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { Method_VALUE = "너비"; 서술 = "()I"; Mooss = 1; }
                else if (TAKE_Word("높이")) { Method_VALUE = "높이"; 서술 = "()I"; Mooss = 1; }
                else if (TAKE_Word("사각형")) { Method_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("지우기")) { Method_VALUE = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { Method_VALUE = "기다리기"; 서술 = "()V"; }
                else Feeler_VALUE("unknown Korean framebuffer method");
            } else Feeler_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) verifizéieren_TYPE(Ausdrock_VALUE(), 가);
            if (나 != 0) { 요구(','); verifizéieren_TYPE(Ausdrock_VALUE(), 나); }
            if (다 != 0) { 요구(','); verifizéieren_TYPE(Ausdrock_VALUE(), 다); }
            if (라 != 0) { 요구(','); verifizéieren_TYPE(Ausdrock_VALUE(), 라); }
            if (마 != 0) { 요구(','); verifizéieren_TYPE(Ausdrock_VALUE(), 마); }
            요구(')'); Befeel(184, 외부참조(10, Besëtzer_VALUE, Method_VALUE, 서술)); return Mooss;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); verifizéieren_TYPE(Ausdrock_VALUE(), 3); 요구(')');
            Befeel(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Numm = Identifikateur_VALUE();
        if (받기('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < Method_COUNT; 수++) if (이름같음(Numm, Method_Agab_Numm[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { Feeler_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!Feeler && 종류() != ')') {
                if (수 >= Method_Argument_COUNT[FUNCTION_VALUE]) { Feeler_VALUE("too many arguments"); break; }
                verifizéieren_TYPE(Ausdrock_VALUE(), Method_Argument_TYPE[FUNCTION_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != Method_Argument_COUNT[FUNCTION_VALUE]) Feeler_VALUE("argument count mismatch");
            Befeel(184, Referenzen(10, Klass_Konstant, Referenzen(12, Method_Numm_Konstant[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return 함수반환[FUNCTION_VALUE];
        }
        int lokal_Beräich = FIND_lokal(Numm), TYPE_VALUE = lokal_TYPE[lokal_Beräich]; 지역읽기(lokal_Beräich);
        while (!Feeler) {
            if (받기('[')) { verifizéieren_TYPE(TYPE_VALUE, 4); verifizéieren_TYPE(Ausdrock_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String Besëtzer_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Befeel(182, 외부참조(10, Besëtzer_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Befeel(182, 외부참조(10, Besëtzer_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); verifizéieren_TYPE(Ausdrock_VALUE(), 1); 요구(')'); Befeel(182, 외부참조(10, Besëtzer_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { Feeler_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { verifizéieren_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Befeel(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { Feeler_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { verifizéieren_TYPE(단항(), 2); 비교값(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(analyséieren_Ganzzuel(positionéieren++, true));
            else { verifizéieren_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { verifizéieren_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!Feeler && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int Codéierung_VALUE = 종류(); positionéieren++; verifizéieren_TYPE(TYPE_VALUE, 1); verifizéieren_TYPE(단항(), 1);
            내보내기(Codéierung_VALUE == '*' ? 104 : Codéierung_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!Feeler && (종류() == '+' || 종류() == '-')) {
            int Codéierung_VALUE = 종류(); positionéieren++; int 경계 = CODE_d_Gréisst_veränneren, Zeréck_VALUE_TYPE = 곱식();
            if (Codéierung_VALUE == '+' && (TYPE_VALUE == 3 || Zeréck_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, Zeréck_VALUE_TYPE); TYPE_VALUE = 3; }
            else { verifizéieren_TYPE(TYPE_VALUE, 1); verifizéieren_TYPE(Zeréck_VALUE_TYPE, 1); 내보내기(Codéierung_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) Feeler_VALUE("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Zeréck_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 generéieren 코드를 삽입한다.
        // RIGHT Ausdrock_VALUE 내부의 Peer_VALUE Branche 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_d_Gréisst_veränneren;
        Befeel(187, Referenzen(7, Word_Konstant("java/lang/StringBuilder"), 0)); 내보내기(89);
        Befeel(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Befeel(182, 붙임참조(앞형));
        if (Feeler) return;
        int Längt_VALUE = CODE_d_Gréisst_veränneren - 끝;
        for (int 수 = 0; 수 < Längt_VALUE; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + Längt_VALUE] = CODE_VALUE[수];
        for (int 수 = 0; 수 < Längt_VALUE; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        Befeel(182, 붙임참조(Zeréck_VALUE_TYPE)); Befeel(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int TYPE_VALUE = 합식();
        while (!Feeler && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int Codéierung_VALUE = 종류(); positionéieren++; verifizéieren_TYPE(TYPE_VALUE, 1); verifizéieren_TYPE(합식(), 1);
            비교값(Codéierung_VALUE == '<' ? 161 : Codéierung_VALUE == '>' ? 163 : Codéierung_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = 비교식();
        while (!Feeler && (종류() == 300 || 종류() == 301)) {
            int Codéierung_VALUE = 종류(); positionéieren++; int Zeréck_VALUE_TYPE = 비교식();
            if (TYPE_VALUE == 0 || Zeréck_VALUE_TYPE == 0) Feeler_VALUE("void expression");
            if (!(Ganzzuel_TYPE(TYPE_VALUE) && Ganzzuel_TYPE(Zeréck_VALUE_TYPE))) verifizéieren_TYPE(Zeréck_VALUE_TYPE, TYPE_VALUE);
            비교값((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (Codéierung_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!Feeler && 받기(304)) {
            verifizéieren_TYPE(TYPE_VALUE, 2); int 가 = Branche(153); verifizéieren_TYPE(동등식(), 2); int 나 = Branche(153);
            내보내기(4); int 끝 = Branche(167); Link_VALUE(가, CODE_d_Gréisst_veränneren); Link_VALUE(나, CODE_d_Gréisst_veränneren); 내보내기(3); Link_VALUE(끝, CODE_d_Gréisst_veränneren); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int Ausdrock_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!Feeler && 받기(305)) {
            verifizéieren_TYPE(TYPE_VALUE, 2); int 가 = Branche(154); verifizéieren_TYPE(논리곱(), 2); int 나 = Branche(154);
            내보내기(3); int 끝 = Branche(167); Link_VALUE(가, CODE_d_Gréisst_veränneren); Link_VALUE(나, CODE_d_Gréisst_veränneren); 내보내기(4); Link_VALUE(끝, CODE_d_Gréisst_veränneren); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void Aufgab_VALUE(boolean 선언허용) {
        if (Word_VALUE(positionéieren, "int") || Word_VALUE(positionéieren, "boolean") || Word_VALUE(positionéieren, "String") || Word_VALUE(positionéieren, "char")
            || Word_VALUE(positionéieren, "FileInputStream") || Word_VALUE(positionéieren, "FileOutputStream")) {
            if (!선언허용) Feeler_VALUE("declaration not allowed here");
            int TYPE_VALUE = Format_VALUE(), Numm = Identifikateur_VALUE(); 요구('='); verifizéieren_TYPE(Ausdrock_VALUE(), TYPE_VALUE);
            schreiwen_lokal(derbäisetzen_lokal(Numm, TYPE_VALUE)); return;
        }
        int Numm = Identifikateur_VALUE(), lokal_Beräich = FIND_lokal(Numm);
        if (받기('=')) { verifizéieren_TYPE(Ausdrock_VALUE(), lokal_TYPE[lokal_Beräich]); schreiwen_lokal(lokal_Beräich); }
        else if (종류() >= 308 && 종류() <= 312) {
            int Codéierung_VALUE = 종류(); positionéieren++; 지역읽기(lokal_Beräich); int 경계 = CODE_d_Gréisst_veränneren, Zeréck_VALUE_TYPE = Ausdrock_VALUE();
            if (Codéierung_VALUE == 308 && lokal_TYPE[lokal_Beräich] == 3) 결합(경계, 3, Zeréck_VALUE_TYPE);
            else {
                verifizéieren_TYPE(lokal_TYPE[lokal_Beräich], 1); verifizéieren_TYPE(Zeréck_VALUE_TYPE, 1);
                내보내기(Codéierung_VALUE == 308 ? 96 : Codéierung_VALUE == 309 ? 100 : Codéierung_VALUE == 310 ? 104 : Codéierung_VALUE == 311 ? 108 : 112);
                if (lokal_TYPE[lokal_Beräich] == 5) 내보내기(146);
            }
            schreiwen_lokal(lokal_Beräich);
        }
        else if (종류() == 306 || 종류() == 307) {
            verifizéieren_TYPE(lokal_TYPE[lokal_Beräich], 1); 내보내기(132); 내보내기(lokal_Beräich); 내보내기(종류() == 306 ? 1 : 255); positionéieren++;
            if (lokal_TYPE[lokal_Beräich] == 5) { 지역읽기(lokal_Beräich); 내보내기(146); schreiwen_lokal(lokal_Beräich); }
        } else Feeler_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Befeel(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean eidel_Argument = 종류() == ')';
        int TYPE_VALUE = eidel_Argument ? 0 : Ausdrock_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !eidel_Argument)) Feeler_VALUE("unsupported print argument");
        Befeel(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean Ausso_VALUE() {
        if (Feeler) return false;
        if (깊이 > 32) { Feeler_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!Feeler && 종류() != '}') { if (반환) Feeler_VALUE("unreachable statement"); 반환 = Ausso_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : Ausdrock_VALUE(); verifizéieren_TYPE(TYPE_VALUE, 함수반환[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); verifizéieren_TYPE(Ausdrock_VALUE(), 2); 요구(')'); int FALSE_VALUE = Branche(153);
            깊이++; boolean 가 = Kontroll_Ausso(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = Branche(167); Link_VALUE(FALSE_VALUE, CODE_d_Gréisst_veränneren); 깊이++; boolean 나 = Kontroll_Ausso(); 깊이--; Link_VALUE(끝, CODE_d_Gréisst_veränneren); return 가 && 나; }
            Link_VALUE(FALSE_VALUE, CODE_d_Gréisst_veränneren); return false;
        }
        if (TAKE_Word("while")) {
            int Laf = CODE_d_Gréisst_veränneren; 요구('('); verifizéieren_TYPE(Ausdrock_VALUE(), 2); 요구(')'); int 끝 = Branche(153);
            깊이++; Kontroll_Ausso(); 깊이--; Link_VALUE(Branche(167), Laf); Link_VALUE(끝, CODE_d_Gréisst_veränneren); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') Aufgab_VALUE(true); 요구(';');
            int Bedéngung = CODE_d_Gréisst_veränneren; if (종류() == ';') 내보내기(4); else verifizéieren_TYPE(Ausdrock_VALUE(), 2); 요구(';');
            int 끝 = Branche(153), Textkierper = Branche(167), aktualiséieren = CODE_d_Gréisst_veränneren;
            if (종류() != ')') Aufgab_VALUE(false); 요구(')'); Link_VALUE(Branche(167), Bedéngung); Link_VALUE(Textkierper, CODE_d_Gréisst_veränneren);
            Kontroll_Ausso(); Link_VALUE(Branche(167), aktualiséieren); Link_VALUE(끝, CODE_d_Gréisst_veränneren);
            for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(positionéieren, "System")) { 화면출력(); return false; }
        if (종류() == 256 && positionéieren + 1 < Token_COUNT && (토큰종류[positionéieren + 1] == '(' || 토큰종류[positionéieren + 1] == '.')) {
            int TYPE_VALUE = Ausdrock_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        Aufgab_VALUE(true); 요구(';'); return false;
    }
    static boolean Kontroll_Ausso() {
        if (Word_VALUE(positionéieren, "int") || Word_VALUE(positionéieren, "boolean") || Word_VALUE(positionéieren, "char") || Word_VALUE(positionéieren, "String")
            || Word_VALUE(positionéieren, "FileInputStream") || Word_VALUE(positionéieren, "FileOutputStream")) Feeler_VALUE("local declaration requires braces");
        return Ausso_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) Feeler_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void schreiwen_Klass() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(Konstant_COUNT);
        for (int 수 = 0; 수 < Konstant_d_Gréisst_veränneren; 수++) 출바(Konstant_VALUE[수]);
        출짧(0x21); 출짧(Klass_Konstant); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(Method_COUNT);
        for (int 수 = 0; 수 < Method_COUNT; 수++) {
            출짧(Method_Zougrëff[수]); 출짧(Method_Numm_Konstant[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_Konstant);
            출정(12 + Method_Längt[수]); 출짧(128); 출짧(함수지역[수]); 출정(Method_Längt[수]);
            for (int Slot_Agab = 0; Slot_Agab < Method_Längt[수]; Slot_Agab++) 출바(CODE_VALUE[Method_CODE[수] + Slot_Agab]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Laf() {
        if (Benotzer.인수개수() == 1 && 자바도구.같음(Benotzer.인수(0), "-version")) {
            Benotzer.schreiwen("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (Benotzer.인수개수() != 1) { Benotzer.schreiwen("Usage: javac FILE.java\n"); return 2; }
        int Numm_d_Gréisst_veränneren = 자바도구.Numm(Fichier_Numm_SMS, Benotzer.인수(0));
        if (Numm_d_Gréisst_veränneren < 6 || Numm_d_Gréisst_veränneren > 62 || Fichier_Numm_SMS[Numm_d_Gréisst_veränneren - 5] != '.' || Fichier_Numm_SMS[Numm_d_Gréisst_veränneren - 4] != 'j'
            || Fichier_Numm_SMS[Numm_d_Gréisst_veränneren - 3] != 'a' || Fichier_Numm_SMS[Numm_d_Gréisst_veränneren - 2] != 'v' || Fichier_Numm_SMS[Numm_d_Gréisst_veränneren - 1] != 'a') {
            Benotzer.schreiwen("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        Quell_d_Gréisst_veränneren = Benotzer.파일읽기(Fichier_Numm_SMS, Quell);
        if (Quell_d_Gréisst_veränneren < 0) { Benotzer.schreiwen("javac: cannot read source: "); 자바도구.수쓰기(Quell_d_Gréisst_veränneren); Benotzer.schreiwen_Zeechen_VALUE(10); return 1; }
        Quell_d_Gréisst_veränneren = 자바도구.원문해독(Quell, Quell_d_Gréisst_veränneren);
        if (Quell_d_Gréisst_veränneren < 0) { Benotzer.schreiwen("javac error: invalid UTF-8 source\n"); return 1; }
        schneiden_VALUE(); if (!Feeler) 선언읽기();
        if (!Feeler) {
            if (Token_Längt[Klass_Token] != Numm_d_Gréisst_veränneren - 5) Feeler_VALUE("class name must match file name");
            for (int 수 = 0; 수 < Numm_d_Gréisst_veränneren - 5; 수++) if (Quell[Token_positionéieren[Klass_Token] + 수] != Fichier_Numm_SMS[수]) Feeler_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < Method_COUNT && !Feeler; 현재함수++) {
            positionéieren = 함수본문[현재함수]; Method_CODE[현재함수] = CODE_d_Gréisst_veränneren; lokal_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < Method_Argument_COUNT[현재함수]; 수++) derbäisetzen_lokal(Method_Argument_Numm[현재함수 * 16 + 수], Method_Argument_TYPE[현재함수 * 16 + 수]);
            boolean 반환 = Ausso_VALUE();
            if (!반환 && 함수반환[현재함수] != 0) Feeler_VALUE("missing return");
            // Branche 뒤의 합류 지점은 반드시 aktuell_Daten 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean Ganzzuel = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(Ganzzuel ? 3 : 1); 내보내기(Ganzzuel ? 172 : 176); }
            if (positionéieren != Method_bëennegen[현재함수]) Feeler_VALUE("invalid method body");
            함수지역[현재함수] = lokal_COUNT; Method_Längt[현재함수] = CODE_d_Gréisst_veränneren - Method_CODE[현재함수];
        }
        if (Feeler) return 1;
        schreiwen_Klass(); if (Feeler) return 1;
        Fichier_Numm_SMS[Numm_d_Gréisst_veränneren - 4] = 'c'; Fichier_Numm_SMS[Numm_d_Gréisst_veränneren - 3] = 'l'; Fichier_Numm_SMS[Numm_d_Gréisst_veränneren - 2] = 'a';
        Fichier_Numm_SMS[Numm_d_Gréisst_veränneren - 1] = 's'; Fichier_Numm_SMS[Numm_d_Gréisst_veränneren] = 's'; Fichier_Numm_SMS[Numm_d_Gréisst_veränneren + 1] = 0;
        int Mooss = Benotzer.schreiwen_Fichier(Fichier_Numm_SMS, 출력, 출력크기);
        if (Mooss < 0) { Benotzer.schreiwen("javac: cannot save class: "); 자바도구.수쓰기(Mooss); Benotzer.schreiwen_Zeechen_VALUE(10); return 1; }
        Benotzer.schreiwen("Compiled: "); for (int 수 = 0; Fichier_Numm_SMS[수] != 0; 수++) Benotzer.schreiwen_Zeechen_VALUE(Fichier_Numm_SMS[수]);
        Benotzer.schreiwen(" (JVM class version 49)\n"); return 0;
    }
}
