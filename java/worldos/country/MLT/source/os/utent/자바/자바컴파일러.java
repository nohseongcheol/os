// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java sors_siġra -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] sors = new int[16384], 출력 = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_pożizzjoni = new int[2048], token_tul = new int[2048];
    static int[] valur_fiss_VALUE = new int[4096], valur_fiss_OFFSET = new int[512];
    static int[] 문자 = new int[512], fajl_isem_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int sors_daqqas, token_COUNT, pożizzjoni, CODE_daqqas, valur_fiss_daqqas, valur_fiss_COUNT = 1, 출력크기, karattru_tul;
    static boolean żball;
    static int klassi_token, klassi_valur_fiss, 부모상수, CODE_valur_fiss;
    static int[] metodu_entrata_isem = new int[32], 함수반환 = new int[32], metodu_argument_COUNT = new int[32];
    static int[] metodu_argument_isem = new int[512], metodu_argument_TYPE = new int[512];
    static int[] 함수본문 = new int[32], metodu_ttermina = new int[32], metodu_CODE = new int[32];
    static int[] metodu_tul = new int[32], 함수지역 = new int[32], metodu_isem_valur_fiss = new int[32], 함수서술 = new int[32];
    static int[] metodu_aċċess = new int[32];
    static int metodu_COUNT, 현재함수, lokali_COUNT, 깊이, 식깊이;
    static int[] lokali_isem = new int[128], lokali_TYPE = new int[128], 지역깊이 = new int[128];

    static void żball_VALUE(String 이유) {
        if (!żball) {
            utent.kiteb("javac error: "); utent.kiteb(이유);
            utent.kiteb(" at line ");
            int linja = 1, 끝 = pożizzjoni < token_COUNT ? token_pożizzjoni[pożizzjoni] : sors_daqqas;
            for (int 수 = 0; 수 < 끝; 수++) if (sors[수] == 10) linja++;
            자바도구.수쓰기(linja); utent.kiteb_karattru_VALUE(10);
        }
        żball = true;
    }
    static boolean karattru_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean ċifra_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= token_COUNT || 나 >= token_COUNT || token_tul[가] != token_tul[나]) return false;
        for (int 수 = 0; 수 < token_tul[가]; 수++) if (sors[token_pożizzjoni[가] + 수] != sors[token_pożizzjoni[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int token_VALUE, String Word_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || token_tul[token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (sors[token_pożizzjoni[token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return pożizzjoni < token_COUNT ? 토큰종류[pożizzjoni] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; pożizzjoni++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) żball_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(pożizzjoni, Word_SMS)) return false; pożizzjoni++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) żball_VALUE(Word_SMS); }
    static int identifikatur_VALUE() {
        int miżura = pożizzjoni;
        if (종류() != 256) żball_VALUE("identifier required"); else pożizzjoni++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int serje = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - serje == token_tul[miżura];
                for (int slott_entrata = serje; 같음 && slott_entrata < 수; slott_entrata++) if (예약어.charAt(slott_entrata) != sors[token_pożizzjoni[miżura] + slott_entrata - serje]) 같음 = false;
                if (같음) żball_VALUE("reserved word cannot be an identifier");
                serje = 수 + 1;
            }
        }
        return miżura;
    }
    static void aqta_VALUE() {
        int 수 = 0;
        while (수 < sors_daqqas && !żball) {
            int VALUE = sors[수], serje = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < sors_daqqas && sors[수 + 1] == '/') {
                while (수 < sors_daqqas && sors[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < sors_daqqas && sors[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < sors_daqqas && !(sors[수] == '*' && sors[수 + 1] == '/')) 수++;
                if (수 + 1 >= sors_daqqas) { żball_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (karattru_VALUE(VALUE)) { 종류 = 256; while (수 < sors_daqqas && 문자이름규칙.이어진글자(sors[수])) 수++; }
            else if (ċifra_VALUE(VALUE)) { 종류 = 257; while (수 < sors_daqqas && ċifra_VALUE(sors[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < sors_daqqas && sors[수] != VALUE && sors[수] != 10 && sors[수] != 13) {
                    if (sors[수] == '\\') 수++;
                    수++;
                }
                if (수 >= sors_daqqas || sors[수] != VALUE) { żball_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < sors_daqqas) {
                    int Li_Jmiss_element = sors[수];
                    if (VALUE == '=' && Li_Jmiss_element == '=') 종류 = 300;
                    if (VALUE == '!' && Li_Jmiss_element == '=') 종류 = 301;
                    if (VALUE == '<' && Li_Jmiss_element == '=') 종류 = 302;
                    if (VALUE == '>' && Li_Jmiss_element == '=') 종류 = 303;
                    if (VALUE == '&' && Li_Jmiss_element == '&') 종류 = 304;
                    if (VALUE == '|' && Li_Jmiss_element == '|') 종류 = 305;
                    if (VALUE == '+' && Li_Jmiss_element == '+') 종류 = 306;
                    if (VALUE == '-' && Li_Jmiss_element == '-') 종류 = 307;
                    if (VALUE == '+' && Li_Jmiss_element == '=') 종류 = 308;
                    if (VALUE == '-' && Li_Jmiss_element == '=') 종류 = 309;
                    if (VALUE == '*' && Li_Jmiss_element == '=') 종류 = 310;
                    if (VALUE == '/' && Li_Jmiss_element == '=') 종류 = 311;
                    if (VALUE == '%' && Li_Jmiss_element == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_COUNT == 토큰종류.length - 1) { żball_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_pożizzjoni[token_COUNT] = serje; token_tul[token_COUNT++] = 수 - serje;
        }
    }
    static void kiteb_valur_fiss_byte(int VALUE) {
        if (valur_fiss_daqqas == valur_fiss_VALUE.length) { żball_VALUE("constant pool too large"); return; }
        valur_fiss_VALUE[valur_fiss_daqqas++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { kiteb_valur_fiss_byte(VALUE >> 8); kiteb_valur_fiss_byte(VALUE); }
    static int i_rreġistra_valur_fiss(int serje) {
        for (int 수 = 1; 수 < valur_fiss_COUNT; 수++) {
            int 앞 = valur_fiss_OFFSET[수], tul_VALUE = (수 + 1 < valur_fiss_COUNT ? valur_fiss_OFFSET[수 + 1] : serje) - 앞;
            if (tul_VALUE != valur_fiss_daqqas - serje) continue;
            boolean 같음 = true;
            for (int slott_entrata = 0; slott_entrata < tul_VALUE; slott_entrata++) if (valur_fiss_VALUE[앞 + slott_entrata] != valur_fiss_VALUE[serje + slott_entrata]) 같음 = false;
            if (같음) { valur_fiss_daqqas = serje; return 수; }
        }
        if (valur_fiss_COUNT == valur_fiss_OFFSET.length) { żball_VALUE("too many constants"); return 0; }
        valur_fiss_OFFSET[valur_fiss_COUNT] = serje;
        return valur_fiss_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (karattru_tul == 문자.length) { żball_VALUE("text too long"); return; }
        문자[karattru_tul++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int karattru_valur_fiss() {
        int serje = valur_fiss_daqqas; kiteb_valur_fiss_byte(1); 상짧(0);
        for (int 수 = 0; 수 < karattru_tul; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) kiteb_valur_fiss_byte(VALUE);
            else if (VALUE < 2048) { kiteb_valur_fiss_byte(192 | VALUE >> 6); kiteb_valur_fiss_byte(128 | VALUE & 63); }
            else { kiteb_valur_fiss_byte(224 | VALUE >> 12); kiteb_valur_fiss_byte(128 | VALUE >> 6 & 63); kiteb_valur_fiss_byte(128 | VALUE & 63); }
        }
        if (żball) return 0;
        int tul_VALUE = valur_fiss_daqqas - serje - 3;
        valur_fiss_VALUE[serje + 1] = tul_VALUE >> 8; valur_fiss_VALUE[serje + 2] = tul_VALUE & 255;
        return i_rreġistra_valur_fiss(serje);
    }
    static int Word_valur_fiss(String Word_SMS) { karattru_tul = 0; 말추가(Word_SMS); return karattru_valur_fiss(); }
    static int token_valur_fiss(int token_VALUE) {
        karattru_tul = 0;
        for (int 수 = 0; 수 < token_tul[token_VALUE]; 수++) 글추가(sors[token_pożizzjoni[token_VALUE] + 수]);
        return karattru_valur_fiss();
    }
    static int Referenza(int 종류, int 가, int 나) {
        int serje = valur_fiss_daqqas; kiteb_valur_fiss_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return i_rreġistra_valur_fiss(serje);
    }
    static int 외부참조(int 종류, String propjetarju_VALUE, String isem, String 서술) {
        int propjetarju_identifikatur = Referenza(7, Word_valur_fiss(propjetarju_VALUE), 0);
        int isem_COUNT = Word_valur_fiss(isem), format_COUNT = Word_valur_fiss(서술);
        return Referenza(종류, propjetarju_identifikatur, Referenza(12, isem_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_daqqas == CODE_VALUE.length) { żball_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_daqqas++] = VALUE & 255;
    }
    static void kmand(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int serje = valur_fiss_daqqas; kiteb_valur_fiss_byte(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        kmand(19, i_rreġistra_valur_fiss(serje));
    }
    static int fergħa(int kmand) { int miżura = CODE_daqqas; kmand(kmand, 0); return miżura; }
    static void Link_VALUE(int fergħa, int mira_oġġett) {
        if (żball) return;
        int 거리 = mira_oġġett - fergħa;
        if (거리 < -32768 || 거리 > 32767 || fergħa < 0 || fergħa + 2 >= CODE_daqqas) { żball_VALUE("invalid branch"); return; }
        CODE_VALUE[fergħa + 1] = 거리 >> 8 & 255; CODE_VALUE[fergħa + 2] = 거리 & 255;
    }
    static void 비교값(int kmand) {
        int TRUE_VALUE = fergħa(kmand); 내보내기(3); int 끝 = fergħa(167);
        Link_VALUE(TRUE_VALUE, CODE_daqqas); 내보내기(4); Link_VALUE(끝, CODE_daqqas);
    }
    static int format_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        żball_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void żied_format(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Proċess_VALUE_entrata 본문은 host javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Malti");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("예외") || TAKE_Word("실행예외") || TAKE_Word("입출력예외") || TAKE_Word("대기시간초과예외") || TAKE_Word("주소확인예외") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("잘못된인수예외") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("빈참조예외") || TAKE_Word("산술예외") || TAKE_Word("상태예외") || TAKE_Word("형변환예외") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_żball") || TAKE_Word("가닥상태예외") || TAKE_Word("대기중단예외")) return;
        żball_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(pożizzjoni, "Malti")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) żball_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); klassi_token = identifikatur_VALUE();
        klassi_valur_fiss = Referenza(7, token_valur_fiss(klassi_token), 0);
        부모상수 = Referenza(7, Word_valur_fiss("java/lang/Object"), 0); CODE_valur_fiss = Word_valur_fiss("Code"); 요구('{');
        while (!żball && 종류() != '}') {
            if (metodu_COUNT == 32) { żball_VALUE("too many methods"); break; }
            int aċċess_entrata = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = metodu_COUNT++;
            metodu_aċċess[FUNCTION_VALUE] = aċċess_entrata | 8;
            함수반환[FUNCTION_VALUE] = format_VALUE(); metodu_entrata_isem[FUNCTION_VALUE] = identifikatur_VALUE(); 요구('(');
            for (int 앞 = 0; 앞 < FUNCTION_VALUE; 앞++) if (이름같음(metodu_entrata_isem[앞], metodu_entrata_isem[FUNCTION_VALUE])) żball_VALUE("duplicate method (overloading unsupported)");
            while (!żball && 종류() != ')') {
                int 수 = metodu_argument_COUNT[FUNCTION_VALUE];
                if (수 == 16) { żball_VALUE("too many parameters"); break; }
                int TYPE_VALUE = format_VALUE(); if (TYPE_VALUE == 0) żball_VALUE("void parameter");
                metodu_argument_TYPE[FUNCTION_VALUE * 16 + 수] = TYPE_VALUE; metodu_argument_isem[FUNCTION_VALUE * 16 + 수] = identifikatur_VALUE();
                metodu_argument_COUNT[FUNCTION_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!żball && 받기(','));
            }
            함수본문[FUNCTION_VALUE] = pożizzjoni; 요구('{');
            int 중첩 = 1;
            while (pożizzjoni < token_COUNT && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                pożizzjoni++;
            }
            if (중첩 != 0) żball_VALUE("unclosed method body");
            metodu_ttermina[FUNCTION_VALUE] = pożizzjoni;
            metodu_isem_valur_fiss[FUNCTION_VALUE] = token_valur_fiss(metodu_entrata_isem[FUNCTION_VALUE]);
            karattru_tul = 0; 글추가('(');
            for (int 수 = 0; 수 < metodu_argument_COUNT[FUNCTION_VALUE]; 수++) żied_format(metodu_argument_TYPE[FUNCTION_VALUE * 16 + 수]);
            글추가(')'); żied_format(함수반환[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = karattru_valur_fiss();
        }
        요구('}'); if (pożizzjoni != token_COUNT) żball_VALUE("extra input after class");
    }
    static int sab_lokali(int isem) {
        for (int 수 = lokali_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokali_isem[수], isem)) return 수;
        żball_VALUE("unknown variable"); return 0;
    }
    static int żied_lokali(int isem, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lokali_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokali_isem[수], isem)) żball_VALUE("duplicate local variable");
        if (lokali_COUNT == 128) { żball_VALUE("too many locals"); return 0; }
        lokali_isem[lokali_COUNT] = isem; lokali_TYPE[lokali_COUNT] = TYPE_VALUE; 지역깊이[lokali_COUNT] = 깊이;
        return lokali_COUNT++;
    }
    static boolean numru_sħiħ_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokali_TYPE[수] <= 2 || lokali_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void kiteb_lokali(int 수) { 내보내기(lokali_TYPE[수] <= 2 || lokali_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void vverifika_TYPE(int attwali_data, int 기대) { if (attwali_data != 기대 && !(attwali_data == 5 && 기대 == 1)) żball_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        karattru_tul = 0; int serje = token_pożizzjoni[token_VALUE] + 1, 끝 = token_pożizzjoni[token_VALUE] + token_tul[token_VALUE] - 1;
        while (serje < 끝 && !żball) {
            int VALUE = sors[serje++];
            if (VALUE == '\\') {
                if (serje == 끝) { żball_VALUE("invalid escape"); break; }
                VALUE = sors[serje++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') żball_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int analizza_numru_sħiħ(int token_VALUE, boolean 음수) {
        if (token_tul[token_VALUE] > 1 && sors[token_pożizzjoni[token_VALUE]] == '0') żball_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < token_tul[token_VALUE]; 수++) {
            int ċifra_element = sors[token_pożizzjoni[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && ċifra_element > (음수 ? 8 : 7)) żball_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - ċifra_element;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = format_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { żball_VALUE("only file streams supported by new in source"); return 0; }
            String propjetarju_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            kmand(187, Referenza(7, Word_valur_fiss(propjetarju_VALUE), 0)); 내보내기(89);
            요구('('); vverifika_TYPE(espressjoni_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) żball_VALUE("input stream constructor arguments"); vverifika_TYPE(espressjoni_VALUE(), 2); 이어 = true; }
            요구(')');
            kmand(183, 외부참조(10, propjetarju_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = espressjoni_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(analizza_numru_sħiħ(pożizzjoni++, false)); return 1; }
        if (종류() == 258) { 문자읽기(pożizzjoni++); kmand(19, Referenza(8, karattru_valur_fiss(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(pożizzjoni++); if (karattru_tul != 1) żball_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Malti")) {
            요구('.'); 말요구("자체"); 요구('.');
            String propjetarju_VALUE = "", metodu_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, miżura = 0;
            if (TAKE_Word("출력")) {
                propjetarju_VALUE = "Malti/자체/출력"; 요구('.');
                if (TAKE_Word("kiteb_linja")) { metodu_VALUE = "kiteb_linja"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("kiteb")) { metodu_VALUE = "kiteb"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { metodu_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else żball_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                propjetarju_VALUE = "Malti/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("tul_VALUE")) { metodu_VALUE = "tul_VALUE"; 서술 = "(Ljava/lang/String;)I"; miżura = 1; }
                else if (TAKE_Word("kodiċi_tal_karattru_COUNT")) { metodu_VALUE = "kodiċi_tal_karattru_COUNT"; 서술 = "(Ljava/lang/String;)I"; miżura = 1; }
                else if (TAKE_Word("analizza_numru_sħiħ")) { metodu_VALUE = "analizza_numru_sħiħ"; 서술 = "(Ljava/lang/String;)I"; miżura = 1; }
                else if (TAKE_Word("kiteb_numru_sħiħ_VALUE")) { metodu_VALUE = "kiteb_numru_sħiħ_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; miżura = 3; }
                else if (TAKE_Word("같음")) { metodu_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; miżura = 2; }
                else if (TAKE_Word("ppejstja_SMS")) { metodu_VALUE = "ppejstja_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; miżura = 3; }
                else if (TAKE_Word("aqta_VALUE")) { metodu_VALUE = "aqta_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; miżura = 3; }
                else żball_VALUE("unknown Korean text method");
            } else if (TAKE_Word("fajl")) {
                propjetarju_VALUE = "Malti/자체/fajl"; 요구('.'); 가 = 3;
                if (TAKE_Word("읽기")) { metodu_VALUE = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; miżura = 3; }
                else if (TAKE_Word("kiteb")) { metodu_VALUE = "kiteb"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else żball_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                propjetarju_VALUE = "Malti/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { metodu_VALUE = "너비"; 서술 = "()I"; miżura = 1; }
                else if (TAKE_Word("높이")) { metodu_VALUE = "높이"; 서술 = "()I"; miżura = 1; }
                else if (TAKE_Word("사각형")) { metodu_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("지우기")) { metodu_VALUE = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metodu_VALUE = "기다리기"; 서술 = "()V"; }
                else żball_VALUE("unknown Korean framebuffer method");
            } else żball_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) vverifika_TYPE(espressjoni_VALUE(), 가);
            if (나 != 0) { 요구(','); vverifika_TYPE(espressjoni_VALUE(), 나); }
            if (다 != 0) { 요구(','); vverifika_TYPE(espressjoni_VALUE(), 다); }
            if (라 != 0) { 요구(','); vverifika_TYPE(espressjoni_VALUE(), 라); }
            if (마 != 0) { 요구(','); vverifika_TYPE(espressjoni_VALUE(), 마); }
            요구(')'); kmand(184, 외부참조(10, propjetarju_VALUE, metodu_VALUE, 서술)); return miżura;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); vverifika_TYPE(espressjoni_VALUE(), 3); 요구(')');
            kmand(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int isem = identifikatur_VALUE();
        if (받기('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < metodu_COUNT; 수++) if (이름같음(isem, metodu_entrata_isem[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { żball_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!żball && 종류() != ')') {
                if (수 >= metodu_argument_COUNT[FUNCTION_VALUE]) { żball_VALUE("too many arguments"); break; }
                vverifika_TYPE(espressjoni_VALUE(), metodu_argument_TYPE[FUNCTION_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != metodu_argument_COUNT[FUNCTION_VALUE]) żball_VALUE("argument count mismatch");
            kmand(184, Referenza(10, klassi_valur_fiss, Referenza(12, metodu_isem_valur_fiss[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return 함수반환[FUNCTION_VALUE];
        }
        int lokali_ambitu = sab_lokali(isem), TYPE_VALUE = lokali_TYPE[lokali_ambitu]; 지역읽기(lokali_ambitu);
        while (!żball) {
            if (받기('[')) { vverifika_TYPE(TYPE_VALUE, 4); vverifika_TYPE(espressjoni_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String propjetarju_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); kmand(182, 외부참조(10, propjetarju_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); kmand(182, 외부참조(10, propjetarju_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); vverifika_TYPE(espressjoni_VALUE(), 1); 요구(')'); kmand(182, 외부참조(10, propjetarju_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { żball_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { vverifika_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); kmand(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { żball_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { vverifika_TYPE(단항(), 2); 비교값(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(analizza_numru_sħiħ(pożizzjoni++, true));
            else { vverifika_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { vverifika_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!żball && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodifikar_VALUE = 종류(); pożizzjoni++; vverifika_TYPE(TYPE_VALUE, 1); vverifika_TYPE(단항(), 1);
            내보내기(kodifikar_VALUE == '*' ? 104 : kodifikar_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!żball && (종류() == '+' || 종류() == '-')) {
            int kodifikar_VALUE = 종류(); pożizzjoni++; int 경계 = CODE_daqqas, Lura_VALUE_TYPE = 곱식();
            if (kodifikar_VALUE == '+' && (TYPE_VALUE == 3 || Lura_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, Lura_VALUE_TYPE); TYPE_VALUE = 3; }
            else { vverifika_TYPE(TYPE_VALUE, 1); vverifika_TYPE(Lura_VALUE_TYPE, 1); 내보내기(kodifikar_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) żball_VALUE("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Lura_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 iġġenera 코드를 삽입한다.
        // RIGHT espressjoni_VALUE 내부의 peer_VALUE fergħa 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_daqqas;
        kmand(187, Referenza(7, Word_valur_fiss("java/lang/StringBuilder"), 0)); 내보내기(89);
        kmand(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); kmand(182, 붙임참조(앞형));
        if (żball) return;
        int tul_VALUE = CODE_daqqas - 끝;
        for (int 수 = 0; 수 < tul_VALUE; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + tul_VALUE] = CODE_VALUE[수];
        for (int 수 = 0; 수 < tul_VALUE; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        kmand(182, 붙임참조(Lura_VALUE_TYPE)); kmand(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int TYPE_VALUE = 합식();
        while (!żball && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodifikar_VALUE = 종류(); pożizzjoni++; vverifika_TYPE(TYPE_VALUE, 1); vverifika_TYPE(합식(), 1);
            비교값(kodifikar_VALUE == '<' ? 161 : kodifikar_VALUE == '>' ? 163 : kodifikar_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = 비교식();
        while (!żball && (종류() == 300 || 종류() == 301)) {
            int kodifikar_VALUE = 종류(); pożizzjoni++; int Lura_VALUE_TYPE = 비교식();
            if (TYPE_VALUE == 0 || Lura_VALUE_TYPE == 0) żball_VALUE("void expression");
            if (!(numru_sħiħ_TYPE(TYPE_VALUE) && numru_sħiħ_TYPE(Lura_VALUE_TYPE))) vverifika_TYPE(Lura_VALUE_TYPE, TYPE_VALUE);
            비교값((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (kodifikar_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!żball && 받기(304)) {
            vverifika_TYPE(TYPE_VALUE, 2); int 가 = fergħa(153); vverifika_TYPE(동등식(), 2); int 나 = fergħa(153);
            내보내기(4); int 끝 = fergħa(167); Link_VALUE(가, CODE_daqqas); Link_VALUE(나, CODE_daqqas); 내보내기(3); Link_VALUE(끝, CODE_daqqas); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int espressjoni_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!żball && 받기(305)) {
            vverifika_TYPE(TYPE_VALUE, 2); int 가 = fergħa(154); vverifika_TYPE(논리곱(), 2); int 나 = fergħa(154);
            내보내기(3); int 끝 = fergħa(167); Link_VALUE(가, CODE_daqqas); Link_VALUE(나, CODE_daqqas); 내보내기(4); Link_VALUE(끝, CODE_daqqas); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void kompitu_VALUE(boolean 선언허용) {
        if (Word_VALUE(pożizzjoni, "int") || Word_VALUE(pożizzjoni, "boolean") || Word_VALUE(pożizzjoni, "String") || Word_VALUE(pożizzjoni, "char")
            || Word_VALUE(pożizzjoni, "FileInputStream") || Word_VALUE(pożizzjoni, "FileOutputStream")) {
            if (!선언허용) żball_VALUE("declaration not allowed here");
            int TYPE_VALUE = format_VALUE(), isem = identifikatur_VALUE(); 요구('='); vverifika_TYPE(espressjoni_VALUE(), TYPE_VALUE);
            kiteb_lokali(żied_lokali(isem, TYPE_VALUE)); return;
        }
        int isem = identifikatur_VALUE(), lokali_ambitu = sab_lokali(isem);
        if (받기('=')) { vverifika_TYPE(espressjoni_VALUE(), lokali_TYPE[lokali_ambitu]); kiteb_lokali(lokali_ambitu); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodifikar_VALUE = 종류(); pożizzjoni++; 지역읽기(lokali_ambitu); int 경계 = CODE_daqqas, Lura_VALUE_TYPE = espressjoni_VALUE();
            if (kodifikar_VALUE == 308 && lokali_TYPE[lokali_ambitu] == 3) 결합(경계, 3, Lura_VALUE_TYPE);
            else {
                vverifika_TYPE(lokali_TYPE[lokali_ambitu], 1); vverifika_TYPE(Lura_VALUE_TYPE, 1);
                내보내기(kodifikar_VALUE == 308 ? 96 : kodifikar_VALUE == 309 ? 100 : kodifikar_VALUE == 310 ? 104 : kodifikar_VALUE == 311 ? 108 : 112);
                if (lokali_TYPE[lokali_ambitu] == 5) 내보내기(146);
            }
            kiteb_lokali(lokali_ambitu);
        }
        else if (종류() == 306 || 종류() == 307) {
            vverifika_TYPE(lokali_TYPE[lokali_ambitu], 1); 내보내기(132); 내보내기(lokali_ambitu); 내보내기(종류() == 306 ? 1 : 255); pożizzjoni++;
            if (lokali_TYPE[lokali_ambitu] == 5) { 지역읽기(lokali_ambitu); 내보내기(146); kiteb_lokali(lokali_ambitu); }
        } else żball_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        kmand(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean vojt_argument = 종류() == ')';
        int TYPE_VALUE = vojt_argument ? 0 : espressjoni_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !vojt_argument)) żball_VALUE("unsupported print argument");
        kmand(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean struzzjoni_VALUE() {
        if (żball) return false;
        if (깊이 > 32) { żball_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!żball && 종류() != '}') { if (반환) żball_VALUE("unreachable statement"); 반환 = struzzjoni_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < lokali_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : espressjoni_VALUE(); vverifika_TYPE(TYPE_VALUE, 함수반환[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); vverifika_TYPE(espressjoni_VALUE(), 2); 요구(')'); int FALSE_VALUE = fergħa(153);
            깊이++; boolean 가 = kontroll_struzzjoni(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = fergħa(167); Link_VALUE(FALSE_VALUE, CODE_daqqas); 깊이++; boolean 나 = kontroll_struzzjoni(); 깊이--; Link_VALUE(끝, CODE_daqqas); return 가 && 나; }
            Link_VALUE(FALSE_VALUE, CODE_daqqas); return false;
        }
        if (TAKE_Word("while")) {
            int serje = CODE_daqqas; 요구('('); vverifika_TYPE(espressjoni_VALUE(), 2); 요구(')'); int 끝 = fergħa(153);
            깊이++; kontroll_struzzjoni(); 깊이--; Link_VALUE(fergħa(167), serje); Link_VALUE(끝, CODE_daqqas); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') kompitu_VALUE(true); 요구(';');
            int kondizzjoni = CODE_daqqas; if (종류() == ';') 내보내기(4); else vverifika_TYPE(espressjoni_VALUE(), 2); 요구(';');
            int 끝 = fergħa(153), il_korp_tat_test = fergħa(167), aġġorna = CODE_daqqas;
            if (종류() != ')') kompitu_VALUE(false); 요구(')'); Link_VALUE(fergħa(167), kondizzjoni); Link_VALUE(il_korp_tat_test, CODE_daqqas);
            kontroll_struzzjoni(); Link_VALUE(fergħa(167), aġġorna); Link_VALUE(끝, CODE_daqqas);
            for (int 수 = 0; 수 < lokali_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(pożizzjoni, "System")) { 화면출력(); return false; }
        if (종류() == 256 && pożizzjoni + 1 < token_COUNT && (토큰종류[pożizzjoni + 1] == '(' || 토큰종류[pożizzjoni + 1] == '.')) {
            int TYPE_VALUE = espressjoni_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        kompitu_VALUE(true); 요구(';'); return false;
    }
    static boolean kontroll_struzzjoni() {
        if (Word_VALUE(pożizzjoni, "int") || Word_VALUE(pożizzjoni, "boolean") || Word_VALUE(pożizzjoni, "char") || Word_VALUE(pożizzjoni, "String")
            || Word_VALUE(pożizzjoni, "FileInputStream") || Word_VALUE(pożizzjoni, "FileOutputStream")) żball_VALUE("local declaration requires braces");
        return struzzjoni_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) żball_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void kiteb_klassi() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(valur_fiss_COUNT);
        for (int 수 = 0; 수 < valur_fiss_daqqas; 수++) 출바(valur_fiss_VALUE[수]);
        출짧(0x21); 출짧(klassi_valur_fiss); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(metodu_COUNT);
        for (int 수 = 0; 수 < metodu_COUNT; 수++) {
            출짧(metodu_aċċess[수]); 출짧(metodu_isem_valur_fiss[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_valur_fiss);
            출정(12 + metodu_tul[수]); 출짧(128); 출짧(함수지역[수]); 출정(metodu_tul[수]);
            for (int slott_entrata = 0; slott_entrata < metodu_tul[수]; slott_entrata++) 출바(CODE_VALUE[metodu_CODE[수] + slott_entrata]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int serje() {
        if (utent.인수개수() == 1 && 자바도구.같음(utent.인수(0), "-version")) {
            utent.kiteb("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (utent.인수개수() != 1) { utent.kiteb("Usage: javac FILE.java\n"); return 2; }
        int isem_daqqas = 자바도구.isem(fajl_isem_SMS, utent.인수(0));
        if (isem_daqqas < 6 || isem_daqqas > 62 || fajl_isem_SMS[isem_daqqas - 5] != '.' || fajl_isem_SMS[isem_daqqas - 4] != 'j'
            || fajl_isem_SMS[isem_daqqas - 3] != 'a' || fajl_isem_SMS[isem_daqqas - 2] != 'v' || fajl_isem_SMS[isem_daqqas - 1] != 'a') {
            utent.kiteb("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        sors_daqqas = utent.파일읽기(fajl_isem_SMS, sors);
        if (sors_daqqas < 0) { utent.kiteb("javac: cannot read source: "); 자바도구.수쓰기(sors_daqqas); utent.kiteb_karattru_VALUE(10); return 1; }
        sors_daqqas = 자바도구.원문해독(sors, sors_daqqas);
        if (sors_daqqas < 0) { utent.kiteb("javac error: invalid UTF-8 source\n"); return 1; }
        aqta_VALUE(); if (!żball) 선언읽기();
        if (!żball) {
            if (token_tul[klassi_token] != isem_daqqas - 5) żball_VALUE("class name must match file name");
            for (int 수 = 0; 수 < isem_daqqas - 5; 수++) if (sors[token_pożizzjoni[klassi_token] + 수] != fajl_isem_SMS[수]) żball_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < metodu_COUNT && !żball; 현재함수++) {
            pożizzjoni = 함수본문[현재함수]; metodu_CODE[현재함수] = CODE_daqqas; lokali_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metodu_argument_COUNT[현재함수]; 수++) żied_lokali(metodu_argument_isem[현재함수 * 16 + 수], metodu_argument_TYPE[현재함수 * 16 + 수]);
            boolean 반환 = struzzjoni_VALUE();
            if (!반환 && 함수반환[현재함수] != 0) żball_VALUE("missing return");
            // fergħa 뒤의 합류 지점은 반드시 attwali_data 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean numru_sħiħ = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(numru_sħiħ ? 3 : 1); 내보내기(numru_sħiħ ? 172 : 176); }
            if (pożizzjoni != metodu_ttermina[현재함수]) żball_VALUE("invalid method body");
            함수지역[현재함수] = lokali_COUNT; metodu_tul[현재함수] = CODE_daqqas - metodu_CODE[현재함수];
        }
        if (żball) return 1;
        kiteb_klassi(); if (żball) return 1;
        fajl_isem_SMS[isem_daqqas - 4] = 'c'; fajl_isem_SMS[isem_daqqas - 3] = 'l'; fajl_isem_SMS[isem_daqqas - 2] = 'a';
        fajl_isem_SMS[isem_daqqas - 1] = 's'; fajl_isem_SMS[isem_daqqas] = 's'; fajl_isem_SMS[isem_daqqas + 1] = 0;
        int miżura = utent.kiteb_fajl(fajl_isem_SMS, 출력, 출력크기);
        if (miżura < 0) { utent.kiteb("javac: cannot save class: "); 자바도구.수쓰기(miżura); utent.kiteb_karattru_VALUE(10); return 1; }
        utent.kiteb("Compiled: "); for (int 수 = 0; fajl_isem_SMS[수] != 0; 수++) utent.kiteb_karattru_VALUE(fajl_isem_SMS[수]);
        utent.kiteb(" (JVM class version 49)\n"); return 0;
    }
}
