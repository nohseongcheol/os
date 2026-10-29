// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java sursă_arborescență -> 표준 버전 49 class compilator. */
public final class 자바컴파일러 {
    static int[] SURSĂ = new int[16384], Rezultat = new int[16384], cod_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_poziție = new int[2048], token_lungime = new int[2048];
    static int[] constantă_VALUE = new int[4096], constantă_OFFSET = new int[512];
    static int[] 문자 = new int[512], nume_de_fișier_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int sursă_dimensiona, token_COUNT, Poziție, cod_dimensiona, constantă_dimensiona, constantă_COUNT = 1, 출력크기, caracter_lungime;
    static boolean eroare;
    static int Clasă_token, Clasă_constantă, părinte_constantă, cod_constantă;
    static int[] metodă_intrare_nume = new int[32], metodă_restitui = new int[32], metodă_argument_COUNT = new int[32];
    static int[] metodă_argument_nume = new int[512], metodă_argument_Tip = new int[512];
    static int[] metodă_corp = new int[32], metodă_termina_un_apel = new int[32], metodă_cod = new int[32];
    static int[] metodă_lungime = new int[32], 함수지역 = new int[32], metodă_nume_constantă = new int[32], 함수서술 = new int[32];
    static int[] metodă_acces = new int[32];
    static int metodă_COUNT, curent_metodă, local_COUNT, 깊이, 식깊이;
    static int[] local_nume = new int[128], local_Tip = new int[128], 지역깊이 = new int[128];

    static void eroare_VALUE(String 이유) {
        if (!eroare) {
            utilizator.Scriere("javac error: "); utilizator.Scriere(이유);
            utilizator.Scriere(" at line ");
            int Linie = 1, 끝 = Poziție < token_COUNT ? token_poziție[Poziție] : sursă_dimensiona;
            for (int 수 = 0; 수 < 끝; 수++) if (SURSĂ[수] == 10) Linie++;
            자바도구.수쓰기(Linie); utilizator.scriere_caracter_VALUE(10);
        }
        eroare = true;
    }
    static boolean caracter_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean cifră_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int SECOND_operand) {
        if (가 < 0 || SECOND_operand < 0 || 가 >= token_COUNT || SECOND_operand >= token_COUNT || token_lungime[가] != token_lungime[SECOND_operand]) return false;
        for (int 수 = 0; 수 < token_lungime[가]; 수++) if (SURSĂ[token_poziție[가] + 수] != SURSĂ[token_poziție[SECOND_operand] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int token_VALUE, String Word_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || token_lungime[token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (SURSĂ[token_poziție[token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Poziție < token_COUNT ? 토큰종류[Poziție] : 0; }
    static boolean primi(int VALUE) { if (종류() != VALUE) return false; Poziție++; return true; }
    static void cerință_VALUE(int VALUE) { if (!primi(VALUE)) eroare_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Poziție, Word_SMS)) return false; Poziție++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) eroare_VALUE(Word_SMS); }
    static int identificator_VALUE() {
        int KR = Poziție;
        if (종류() != 256) eroare_VALUE("identifier required"); else Poziție++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Pornește = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Pornește == token_lungime[KR];
                for (int 칸 = Pornește; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != SURSĂ[token_poziție[KR] + 칸 - Pornește]) 같음 = false;
                if (같음) eroare_VALUE("reserved word cannot be an identifier");
                Pornește = 수 + 1;
            }
        }
        return KR;
    }
    static void decupa_VALUE() {
        int 수 = 0;
        while (수 < sursă_dimensiona && !eroare) {
            int VALUE = SURSĂ[수], Pornește = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < sursă_dimensiona && SURSĂ[수 + 1] == '/') {
                while (수 < sursă_dimensiona && SURSĂ[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < sursă_dimensiona && SURSĂ[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < sursă_dimensiona && !(SURSĂ[수] == '*' && SURSĂ[수 + 1] == '/')) 수++;
                if (수 + 1 >= sursă_dimensiona) { eroare_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (caracter_VALUE(VALUE)) { 종류 = 256; while (수 < sursă_dimensiona && 문자이름규칙.이어진글자(SURSĂ[수])) 수++; }
            else if (cifră_VALUE(VALUE)) { 종류 = 257; while (수 < sursă_dimensiona && cifră_VALUE(SURSĂ[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < sursă_dimensiona && SURSĂ[수] != VALUE && SURSĂ[수] != 10 && SURSĂ[수] != 13) {
                    if (SURSĂ[수] == '\\') 수++;
                    수++;
                }
                if (수 >= sursă_dimensiona || SURSĂ[수] != VALUE) { eroare_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < sursă_dimensiona) {
                    int Următorul_element = SURSĂ[수];
                    if (VALUE == '=' && Următorul_element == '=') 종류 = 300;
                    if (VALUE == '!' && Următorul_element == '=') 종류 = 301;
                    if (VALUE == '<' && Următorul_element == '=') 종류 = 302;
                    if (VALUE == '>' && Următorul_element == '=') 종류 = 303;
                    if (VALUE == '&' && Următorul_element == '&') 종류 = 304;
                    if (VALUE == '|' && Următorul_element == '|') 종류 = 305;
                    if (VALUE == '+' && Următorul_element == '+') 종류 = 306;
                    if (VALUE == '-' && Următorul_element == '-') 종류 = 307;
                    if (VALUE == '+' && Următorul_element == '=') 종류 = 308;
                    if (VALUE == '-' && Următorul_element == '=') 종류 = 309;
                    if (VALUE == '*' && Următorul_element == '=') 종류 = 310;
                    if (VALUE == '/' && Următorul_element == '=') 종류 = 311;
                    if (VALUE == '%' && Următorul_element == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_COUNT == 토큰종류.length - 1) { eroare_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_poziție[token_COUNT] = Pornește; token_lungime[token_COUNT++] = 수 - Pornește;
        }
    }
    static void scriere_constantă_byte(int VALUE) {
        if (constantă_dimensiona == constantă_VALUE.length) { eroare_VALUE("constant pool too large"); return; }
        constantă_VALUE[constantă_dimensiona++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { scriere_constantă_byte(VALUE >> 8); scriere_constantă_byte(VALUE); }
    static int registru_constantă(int Pornește) {
        for (int 수 = 1; 수 < constantă_COUNT; 수++) {
            int frontală_VALUE = constantă_OFFSET[수], lungime_VALUE = (수 + 1 < constantă_COUNT ? constantă_OFFSET[수 + 1] : Pornește) - frontală_VALUE;
            if (lungime_VALUE != constantă_dimensiona - Pornește) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < lungime_VALUE; 칸++) if (constantă_VALUE[frontală_VALUE + 칸] != constantă_VALUE[Pornește + 칸]) 같음 = false;
            if (같음) { constantă_dimensiona = Pornește; return 수; }
        }
        if (constantă_COUNT == constantă_OFFSET.length) { eroare_VALUE("too many constants"); return 0; }
        constantă_OFFSET[constantă_COUNT] = Pornește;
        return constantă_COUNT++;
    }
    static void adăuga_SMS(int VALUE) {
        if (caracter_lungime == 문자.length) { eroare_VALUE("text too long"); return; }
        문자[caracter_lungime++] = VALUE;
    }
    static void adăuga_Word(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) adăuga_SMS(Word_SMS.charAt(수)); }
    static int caracter_constantă() {
        int Pornește = constantă_dimensiona; scriere_constantă_byte(1); 상짧(0);
        for (int 수 = 0; 수 < caracter_lungime; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) scriere_constantă_byte(VALUE);
            else if (VALUE < 2048) { scriere_constantă_byte(192 | VALUE >> 6); scriere_constantă_byte(128 | VALUE & 63); }
            else { scriere_constantă_byte(224 | VALUE >> 12); scriere_constantă_byte(128 | VALUE >> 6 & 63); scriere_constantă_byte(128 | VALUE & 63); }
        }
        if (eroare) return 0;
        int lungime_VALUE = constantă_dimensiona - Pornește - 3;
        constantă_VALUE[Pornește + 1] = lungime_VALUE >> 8; constantă_VALUE[Pornește + 2] = lungime_VALUE & 255;
        return registru_constantă(Pornește);
    }
    static int Word_constantă(String Word_SMS) { caracter_lungime = 0; adăuga_Word(Word_SMS); return caracter_constantă(); }
    static int token_constantă(int token_VALUE) {
        caracter_lungime = 0;
        for (int 수 = 0; 수 < token_lungime[token_VALUE]; 수++) adăuga_SMS(SURSĂ[token_poziție[token_VALUE] + 수]);
        return caracter_constantă();
    }
    static int referință(int 종류, int 가, int SECOND_operand) {
        int Pornește = constantă_dimensiona; scriere_constantă_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SECOND_operand);
        return registru_constantă(Pornește);
    }
    static int extern_referință(int 종류, String proprietar_VALUE, String Nume, String 서술) {
        int proprietar_identificator = referință(7, Word_constantă(proprietar_VALUE), 0);
        int nume_COUNT = Word_constantă(Nume), format_COUNT = Word_constantă(서술);
        return referință(종류, proprietar_identificator, referință(12, nume_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (cod_dimensiona == cod_VALUE.length) { eroare_VALUE("bytecode too large"); return; }
        cod_VALUE[cod_dimensiona++] = VALUE & 255;
    }
    static void Comandă(int VALUE, int Argumente) { 내보내기(VALUE); 내보내기(Argumente >> 8); 내보내기(Argumente); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Pornește = constantă_dimensiona; scriere_constantă_byte(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Comandă(19, registru_constantă(Pornește));
    }
    static int ramură(int Comandă) { int KR = cod_dimensiona; Comandă(Comandă, 0); return KR; }
    static void Link_VALUE(int ramură, int țintă_obiect) {
        if (eroare) return;
        int 거리 = țintă_obiect - ramură;
        if (거리 < -32768 || 거리 > 32767 || ramură < 0 || ramură + 2 >= cod_dimensiona) { eroare_VALUE("invalid branch"); return; }
        cod_VALUE[ramură + 1] = 거리 >> 8 & 255; cod_VALUE[ramură + 2] = 거리 & 255;
    }
    static void Comparație_VALUE(int Comandă) {
        int TRUE_VALUE = ramură(Comandă); 내보내기(3); int 끝 = ramură(167);
        Link_VALUE(TRUE_VALUE, cod_dimensiona); 내보내기(4); Link_VALUE(끝, cod_dimensiona);
    }
    static int format_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (primi('[')) { cerință_VALUE(']'); return 4; } return 3; }
        eroare_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void adăuga_format(int Tip_VALUE) {
        if (Tip_VALUE == 0) adăuga_SMS('V');
        if (Tip_VALUE == 1) adăuga_SMS('I');
        if (Tip_VALUE == 2) adăuga_SMS('Z');
        if (Tip_VALUE == 3) adăuga_Word("Ljava/lang/String;");
        if (Tip_VALUE == 4) adăuga_Word("[Ljava/lang/String;");
        if (Tip_VALUE == 5) adăuga_SMS('C');
        if (Tip_VALUE == 6) adăuga_Word("Ljava/io/FileInputStream;");
        if (Tip_VALUE == 7) adăuga_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws declarație. excepție Proces_VALUE_intrare 본문은 gazdă javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Română");
        if (한국어묶음) { cerință_VALUE('.'); 말요구("propriu"); cerință_VALUE('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("excepție") || TAKE_Word("executare_excepție") || TAKE_Word("I_O_excepție") || TAKE_Word("대기시간초과예외") || TAKE_Word("adresa_LOOKUP_excepție") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("nul_argument_excepție") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NUL_referință_excepție") || TAKE_Word("산술예외") || TAKE_Word("Stare_excepție") || TAKE_Word("Tip_cast_excepție") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_eroare") || TAKE_Word("fir_Stare_excepție") || TAKE_Word("대기중단예외")) return;
        eroare_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Poziție, "Română")) 예외이름읽기();
            else {
                말요구("java"); cerință_VALUE('.'); 말요구("io"); cerință_VALUE('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) eroare_VALUE("unsupported import");
            }
            cerință_VALUE(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); Clasă_token = identificator_VALUE();
        Clasă_constantă = referință(7, token_constantă(Clasă_token), 0);
        părinte_constantă = referință(7, Word_constantă("java/lang/Object"), 0); cod_constantă = Word_constantă("Code"); cerință_VALUE('{');
        while (!eroare && 종류() != '}') {
            if (metodă_COUNT == 32) { eroare_VALUE("too many methods"); break; }
            int acces_intrare = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int funcție_VALUE = metodă_COUNT++;
            metodă_acces[funcție_VALUE] = acces_intrare | 8;
            metodă_restitui[funcție_VALUE] = format_VALUE(); metodă_intrare_nume[funcție_VALUE] = identificator_VALUE(); cerință_VALUE('(');
            for (int frontală_VALUE = 0; frontală_VALUE < funcție_VALUE; frontală_VALUE++) if (이름같음(metodă_intrare_nume[frontală_VALUE], metodă_intrare_nume[funcție_VALUE])) eroare_VALUE("duplicate method (overloading unsupported)");
            while (!eroare && 종류() != ')') {
                int 수 = metodă_argument_COUNT[funcție_VALUE];
                if (수 == 16) { eroare_VALUE("too many parameters"); break; }
                int Tip_VALUE = format_VALUE(); if (Tip_VALUE == 0) eroare_VALUE("void parameter");
                metodă_argument_Tip[funcție_VALUE * 16 + 수] = Tip_VALUE; metodă_argument_nume[funcție_VALUE * 16 + 수] = identificator_VALUE();
                metodă_argument_COUNT[funcție_VALUE]++;
                if (!primi(',')) break;
            }
            cerință_VALUE(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!eroare && primi(','));
            }
            metodă_corp[funcție_VALUE] = Poziție; cerință_VALUE('{');
            int imbricare_VALUE = 1;
            while (Poziție < token_COUNT && imbricare_VALUE > 0) {
                if (종류() == '{') imbricare_VALUE++;
                if (종류() == '}') imbricare_VALUE--;
                Poziție++;
            }
            if (imbricare_VALUE != 0) eroare_VALUE("unclosed method body");
            metodă_termina_un_apel[funcție_VALUE] = Poziție;
            metodă_nume_constantă[funcție_VALUE] = token_constantă(metodă_intrare_nume[funcție_VALUE]);
            caracter_lungime = 0; adăuga_SMS('(');
            for (int 수 = 0; 수 < metodă_argument_COUNT[funcție_VALUE]; 수++) adăuga_format(metodă_argument_Tip[funcție_VALUE * 16 + 수]);
            adăuga_SMS(')'); adăuga_format(metodă_restitui[funcție_VALUE]); 함수서술[funcție_VALUE] = caracter_constantă();
        }
        cerință_VALUE('}'); if (Poziție != token_COUNT) eroare_VALUE("extra input after class");
    }
    static int FIND_local(int Nume) {
        for (int 수 = local_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(local_nume[수], Nume)) return 수;
        eroare_VALUE("unknown variable"); return 0;
    }
    static int adăuga_local(int Nume, int Tip_VALUE) {
        for (int 수 = 0; 수 < local_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(local_nume[수], Nume)) eroare_VALUE("duplicate local variable");
        if (local_COUNT == 128) { eroare_VALUE("too many locals"); return 0; }
        local_nume[local_COUNT] = Nume; local_Tip[local_COUNT] = Tip_VALUE; 지역깊이[local_COUNT] = 깊이;
        return local_COUNT++;
    }
    static boolean întreg_Tip(int Tip_VALUE) { return Tip_VALUE == 1 || Tip_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(local_Tip[수] <= 2 || local_Tip[수] == 5 ? 21 : 25); 내보내기(수); }
    static void scriere_local(int 수) { 내보내기(local_Tip[수] <= 2 || local_Tip[수] == 5 ? 54 : 58); 내보내기(수); }
    static void verifica_Tip(int real_date, int 기대) { if (real_date != 기대 && !(real_date == 5 && 기대 == 1)) eroare_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        caracter_lungime = 0; int Pornește = token_poziție[token_VALUE] + 1, 끝 = token_poziție[token_VALUE] + token_lungime[token_VALUE] - 1;
        while (Pornește < 끝 && !eroare) {
            int VALUE = SURSĂ[Pornește++];
            if (VALUE == '\\') {
                if (Pornește == 끝) { eroare_VALUE("invalid escape"); break; }
                VALUE = SURSĂ[Pornește++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') eroare_VALUE("unsupported escape");
            }
            adăuga_SMS(VALUE);
        }
    }
    static int analiza_întreg(int token_VALUE, boolean 음수) {
        if (token_lungime[token_VALUE] > 1 && SURSĂ[token_poziție[token_VALUE]] == '0') eroare_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < token_lungime[token_VALUE]; 수++) {
            int cifră_element = SURSĂ[token_poziție[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && cifră_element > (음수 ? 8 : 7)) eroare_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - cifră_element;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int Tip_VALUE = format_VALUE();
            if (Tip_VALUE != 6 && Tip_VALUE != 7) { eroare_VALUE("only file streams supported by new in source"); return 0; }
            String proprietar_VALUE = Tip_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Comandă(187, referință(7, Word_constantă(proprietar_VALUE), 0)); 내보내기(89);
            cerință_VALUE('('); verifica_Tip(expresie_VALUE(), 3); boolean 이어 = false;
            if (primi(',')) { if (Tip_VALUE != 7) eroare_VALUE("input stream constructor arguments"); verifica_Tip(expresie_VALUE(), 2); 이어 = true; }
            cerință_VALUE(')');
            Comandă(183, extern_referință(10, proprietar_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return Tip_VALUE;
        }
        if (primi('(')) { int Tip_VALUE = expresie_VALUE(); cerință_VALUE(')'); return Tip_VALUE; }
        if (종류() == 257) { 수상수(analiza_întreg(Poziție++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Poziție++); Comandă(19, referință(8, caracter_constantă(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Poziție++); if (caracter_lungime != 1) eroare_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Română")) {
            cerință_VALUE('.'); 말요구("propriu"); cerință_VALUE('.');
            String proprietar_VALUE = "", metodă_VALUE = "", 서술 = ""; int 가 = 0, SECOND_operand = 0, 다 = 0, 라 = 0, 마 = 0, KR = 0;
            if (TAKE_Word("Rezultat")) {
                proprietar_VALUE = "Română/propriu/Rezultat"; cerință_VALUE('.');
                if (TAKE_Word("scriere_linie")) { metodă_VALUE = "scriere_linie"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Scriere")) { metodă_VALUE = "Scriere"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { metodă_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else eroare_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                proprietar_VALUE = "Română/propriu/문자"; cerință_VALUE('.'); 가 = 3;
                if (TAKE_Word("lungime_VALUE")) { metodă_VALUE = "lungime_VALUE"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAKE_Word("cod_caracter_COUNT")) { metodă_VALUE = "cod_caracter_COUNT"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAKE_Word("analiza_întreg")) { metodă_VALUE = "analiza_întreg"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAKE_Word("scriere_întreg_VALUE")) { metodă_VALUE = "scriere_întreg_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; KR = 3; }
                else if (TAKE_Word("같음")) { metodă_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECOND_operand = 3; KR = 2; }
                else if (TAKE_Word("lipi_SMS")) { metodă_VALUE = "lipi_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECOND_operand = 3; KR = 3; }
                else if (TAKE_Word("decupa_VALUE")) { metodă_VALUE = "decupa_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECOND_operand = 1; 다 = 1; KR = 3; }
                else eroare_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Fișier")) {
                proprietar_VALUE = "Română/propriu/Fișier"; cerință_VALUE('.'); 가 = 3;
                if (TAKE_Word("Citire")) { metodă_VALUE = "Citire"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; KR = 3; }
                else if (TAKE_Word("Scriere")) { metodă_VALUE = "Scriere"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECOND_operand = 3; }
                else eroare_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                proprietar_VALUE = "Română/propriu/화면"; cerință_VALUE('.');
                if (TAKE_Word("너비")) { metodă_VALUE = "너비"; 서술 = "()I"; KR = 1; }
                else if (TAKE_Word("높이")) { metodă_VALUE = "높이"; 서술 = "()I"; KR = 1; }
                else if (TAKE_Word("dreptunghi")) { metodă_VALUE = "dreptunghi"; 서술 = "(IIIII)V"; 가 = 1; SECOND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("șterge_intrare")) { metodă_VALUE = "șterge_intrare"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metodă_VALUE = "기다리기"; 서술 = "()V"; }
                else eroare_VALUE("unknown Korean framebuffer method");
            } else eroare_VALUE("unsupported Korean library class");
            cerință_VALUE('('); if (가 != 0) verifica_Tip(expresie_VALUE(), 가);
            if (SECOND_operand != 0) { cerință_VALUE(','); verifica_Tip(expresie_VALUE(), SECOND_operand); }
            if (다 != 0) { cerință_VALUE(','); verifica_Tip(expresie_VALUE(), 다); }
            if (라 != 0) { cerință_VALUE(','); verifica_Tip(expresie_VALUE(), 라); }
            if (마 != 0) { cerință_VALUE(','); verifica_Tip(expresie_VALUE(), 마); }
            cerință_VALUE(')'); Comandă(184, extern_referință(10, proprietar_VALUE, metodă_VALUE, 서술)); return KR;
        }
        if (TAKE_Word("Integer")) {
            cerință_VALUE('.'); 말요구("parseInt"); cerință_VALUE('('); verifica_Tip(expresie_VALUE(), 3); cerință_VALUE(')');
            Comandă(184, extern_referință(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nume = identificator_VALUE();
        if (primi('(')) {
            int funcție_VALUE = -1;
            for (int 수 = 0; 수 < metodă_COUNT; 수++) if (이름같음(Nume, metodă_intrare_nume[수])) funcție_VALUE = 수;
            if (funcție_VALUE < 0) { eroare_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!eroare && 종류() != ')') {
                if (수 >= metodă_argument_COUNT[funcție_VALUE]) { eroare_VALUE("too many arguments"); break; }
                verifica_Tip(expresie_VALUE(), metodă_argument_Tip[funcție_VALUE * 16 + 수++]); if (!primi(',')) break;
            }
            cerință_VALUE(')'); if (수 != metodă_argument_COUNT[funcție_VALUE]) eroare_VALUE("argument count mismatch");
            Comandă(184, referință(10, Clasă_constantă, referință(12, metodă_nume_constantă[funcție_VALUE], 함수서술[funcție_VALUE])));
            return metodă_restitui[funcție_VALUE];
        }
        int local_gamă = FIND_local(Nume), Tip_VALUE = local_Tip[local_gamă]; 지역읽기(local_gamă);
        while (!eroare) {
            if (primi('[')) { verifica_Tip(Tip_VALUE, 4); verifica_Tip(expresie_VALUE(), 1); cerință_VALUE(']'); 내보내기(50); Tip_VALUE = 3; }
            else if (primi('.')) {
                if (Tip_VALUE == 6 || Tip_VALUE == 7) {
                    String proprietar_VALUE = Tip_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { cerință_VALUE('('); cerință_VALUE(')'); Comandă(182, extern_referință(10, proprietar_VALUE, "close", "()V")); Tip_VALUE = 0; }
                    else if (Tip_VALUE == 6 && TAKE_Word("read")) { cerință_VALUE('('); cerință_VALUE(')'); Comandă(182, extern_referință(10, proprietar_VALUE, "read", "()I")); Tip_VALUE = 1; }
                    else if (Tip_VALUE == 7 && TAKE_Word("write")) { cerință_VALUE('('); verifica_Tip(expresie_VALUE(), 1); cerință_VALUE(')'); Comandă(182, extern_referință(10, proprietar_VALUE, "write", "(I)V")); Tip_VALUE = 0; }
                    else { eroare_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (Tip_VALUE == 4) { 내보내기(190); Tip_VALUE = 1; }
                else { verifica_Tip(Tip_VALUE, 3); cerință_VALUE('('); cerință_VALUE(')'); Comandă(182, extern_referință(10, "java/lang/String", "length", "()I")); Tip_VALUE = 1; }
            } else break;
        }
        return Tip_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { eroare_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int Tip_VALUE;
        if (primi('!')) { verifica_Tip(단항(), 2); Comparație_VALUE(153); Tip_VALUE = 2; }
        else if (primi('-')) {
            if (종류() == 257) 수상수(analiza_întreg(Poziție++, true));
            else { verifica_Tip(단항(), 1); 내보내기(116); }
            Tip_VALUE = 1;
        } else if (primi('+')) { verifica_Tip(단항(), 1); Tip_VALUE = 1; }
        else Tip_VALUE = 기본식();
        식깊이--; return Tip_VALUE;
    }
    static int 곱식() {
        int Tip_VALUE = 단항();
        while (!eroare && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int codificare_VALUE = 종류(); Poziție++; verifica_Tip(Tip_VALUE, 1); verifica_Tip(단항(), 1);
            내보내기(codificare_VALUE == '*' ? 104 : codificare_VALUE == '/' ? 108 : 112); Tip_VALUE = 1;
        }
        return Tip_VALUE;
    }
    static int 합식() {
        int Tip_VALUE = 곱식();
        while (!eroare && (종류() == '+' || 종류() == '-')) {
            int codificare_VALUE = 종류(); Poziție++; int 경계 = cod_dimensiona, ÎNAPOI_VALUE_Tip = 곱식();
            if (codificare_VALUE == '+' && (Tip_VALUE == 3 || ÎNAPOI_VALUE_Tip == 3)) { 결합(경계, Tip_VALUE, ÎNAPOI_VALUE_Tip); Tip_VALUE = 3; }
            else { verifica_Tip(Tip_VALUE, 1); verifica_Tip(ÎNAPOI_VALUE_Tip, 1); 내보내기(codificare_VALUE == '+' ? 96 : 100); Tip_VALUE = 1; }
        }
        return Tip_VALUE;
    }
    static int 붙임참조(int Tip_VALUE) {
        if (Tip_VALUE != 1 && Tip_VALUE != 2 && Tip_VALUE != 3 && Tip_VALUE != 5) eroare_VALUE("unsupported concatenation type");
        return extern_referință(10, "java/lang/StringBuilder", "append", Tip_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : Tip_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : Tip_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int frontală_VALUE_Tip, int ÎNAPOI_VALUE_Tip) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT cod_VALUE 앞에 genera 코드를 삽입한다.
        // RIGHT expresie_VALUE 내부의 pereche_VALUE ramură 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = cod_dimensiona;
        Comandă(187, referință(7, Word_constantă("java/lang/StringBuilder"), 0)); 내보내기(89);
        Comandă(183, extern_referință(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Comandă(182, 붙임참조(frontală_VALUE_Tip));
        if (eroare) return;
        int lungime_VALUE = cod_dimensiona - 끝;
        for (int 수 = 0; 수 < lungime_VALUE; 수++) 삽입코드[수] = cod_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) cod_VALUE[수 + lungime_VALUE] = cod_VALUE[수];
        for (int 수 = 0; 수 < lungime_VALUE; 수++) cod_VALUE[경계 + 수] = 삽입코드[수];
        Comandă(182, 붙임참조(ÎNAPOI_VALUE_Tip)); Comandă(182, extern_referință(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Comparație_expresie() {
        int Tip_VALUE = 합식();
        while (!eroare && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int codificare_VALUE = 종류(); Poziție++; verifica_Tip(Tip_VALUE, 1); verifica_Tip(합식(), 1);
            Comparație_VALUE(codificare_VALUE == '<' ? 161 : codificare_VALUE == '>' ? 163 : codificare_VALUE == 302 ? 164 : 162); Tip_VALUE = 2;
        }
        return Tip_VALUE;
    }
    static int 동등식() {
        int Tip_VALUE = Comparație_expresie();
        while (!eroare && (종류() == 300 || 종류() == 301)) {
            int codificare_VALUE = 종류(); Poziție++; int ÎNAPOI_VALUE_Tip = Comparație_expresie();
            if (Tip_VALUE == 0 || ÎNAPOI_VALUE_Tip == 0) eroare_VALUE("void expression");
            if (!(întreg_Tip(Tip_VALUE) && întreg_Tip(ÎNAPOI_VALUE_Tip))) verifica_Tip(ÎNAPOI_VALUE_Tip, Tip_VALUE);
            Comparație_VALUE((Tip_VALUE <= 2 || Tip_VALUE == 5 ? 159 : 165) + (codificare_VALUE == 301 ? 1 : 0)); Tip_VALUE = 2;
        }
        return Tip_VALUE;
    }
    static int AND() {
        int Tip_VALUE = 동등식();
        while (!eroare && primi(304)) {
            verifica_Tip(Tip_VALUE, 2); int 가 = ramură(153); verifica_Tip(동등식(), 2); int SECOND_operand = ramură(153);
            내보내기(4); int 끝 = ramură(167); Link_VALUE(가, cod_dimensiona); Link_VALUE(SECOND_operand, cod_dimensiona); 내보내기(3); Link_VALUE(끝, cod_dimensiona); Tip_VALUE = 2;
        }
        return Tip_VALUE;
    }
    static int expresie_VALUE() {
        int Tip_VALUE = AND();
        while (!eroare && primi(305)) {
            verifica_Tip(Tip_VALUE, 2); int 가 = ramură(154); verifica_Tip(AND(), 2); int SECOND_operand = ramură(154);
            내보내기(3); int 끝 = ramură(167); Link_VALUE(가, cod_dimensiona); Link_VALUE(SECOND_operand, cod_dimensiona); 내보내기(4); Link_VALUE(끝, cod_dimensiona); Tip_VALUE = 2;
        }
        return Tip_VALUE;
    }
    static void atribuire_VALUE(boolean permite_declarație) {
        if (Word_VALUE(Poziție, "int") || Word_VALUE(Poziție, "boolean") || Word_VALUE(Poziție, "String") || Word_VALUE(Poziție, "char")
            || Word_VALUE(Poziție, "FileInputStream") || Word_VALUE(Poziție, "FileOutputStream")) {
            if (!permite_declarație) eroare_VALUE("declaration not allowed here");
            int Tip_VALUE = format_VALUE(), Nume = identificator_VALUE(); cerință_VALUE('='); verifica_Tip(expresie_VALUE(), Tip_VALUE);
            scriere_local(adăuga_local(Nume, Tip_VALUE)); return;
        }
        int Nume = identificator_VALUE(), local_gamă = FIND_local(Nume);
        if (primi('=')) { verifica_Tip(expresie_VALUE(), local_Tip[local_gamă]); scriere_local(local_gamă); }
        else if (종류() >= 308 && 종류() <= 312) {
            int codificare_VALUE = 종류(); Poziție++; 지역읽기(local_gamă); int 경계 = cod_dimensiona, ÎNAPOI_VALUE_Tip = expresie_VALUE();
            if (codificare_VALUE == 308 && local_Tip[local_gamă] == 3) 결합(경계, 3, ÎNAPOI_VALUE_Tip);
            else {
                verifica_Tip(local_Tip[local_gamă], 1); verifica_Tip(ÎNAPOI_VALUE_Tip, 1);
                내보내기(codificare_VALUE == 308 ? 96 : codificare_VALUE == 309 ? 100 : codificare_VALUE == 310 ? 104 : codificare_VALUE == 311 ? 108 : 112);
                if (local_Tip[local_gamă] == 5) 내보내기(146);
            }
            scriere_local(local_gamă);
        }
        else if (종류() == 306 || 종류() == 307) {
            verifica_Tip(local_Tip[local_gamă], 1); 내보내기(132); 내보내기(local_gamă); 내보내기(종류() == 306 ? 1 : 255); Poziție++;
            if (local_Tip[local_gamă] == 5) { 지역읽기(local_gamă); 내보내기(146); scriere_local(local_gamă); }
        } else eroare_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); cerință_VALUE('.'); 말요구("out"); cerință_VALUE('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); cerință_VALUE('(');
        Comandă(178, extern_referință(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int Tip_VALUE = 빈인수 ? 0 : expresie_VALUE(); cerință_VALUE(')'); cerință_VALUE(';');
        String 서술 = Tip_VALUE == 0 ? "()V" : Tip_VALUE == 1 ? "(I)V" : Tip_VALUE == 2 ? "(Z)V" : Tip_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (Tip_VALUE == 4 || Tip_VALUE >= 6 || Tip_VALUE == 0 && (!줄바꿈 || !빈인수)) eroare_VALUE("unsupported print argument");
        Comandă(182, extern_referință(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean declarație_VALUE() {
        if (eroare) return false;
        if (깊이 > 32) { eroare_VALUE("statement nesting too deep"); return false; }
        if (primi('{')) {
            깊이++; boolean restitui_KR = false;
            while (!eroare && 종류() != '}') { if (restitui_KR) eroare_VALUE("unreachable statement"); restitui_KR = declarație_VALUE(); }
            cerință_VALUE('}'); for (int 수 = 0; 수 < local_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return restitui_KR;
        }
        if (primi(';')) return false;
        if (TAKE_Word("return")) {
            int Tip_VALUE = 종류() == ';' ? 0 : expresie_VALUE(); verifica_Tip(Tip_VALUE, metodă_restitui[curent_metodă]); cerință_VALUE(';');
            내보내기(Tip_VALUE == 0 ? 177 : Tip_VALUE <= 2 || Tip_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            cerință_VALUE('('); verifica_Tip(expresie_VALUE(), 2); cerință_VALUE(')'); int FALSE_VALUE = ramură(153);
            깊이++; boolean 가 = control_declarație(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = ramură(167); Link_VALUE(FALSE_VALUE, cod_dimensiona); 깊이++; boolean SECOND_operand = control_declarație(); 깊이--; Link_VALUE(끝, cod_dimensiona); return 가 && SECOND_operand; }
            Link_VALUE(FALSE_VALUE, cod_dimensiona); return false;
        }
        if (TAKE_Word("while")) {
            int Pornește = cod_dimensiona; cerință_VALUE('('); verifica_Tip(expresie_VALUE(), 2); cerință_VALUE(')'); int 끝 = ramură(153);
            깊이++; control_declarație(); 깊이--; Link_VALUE(ramură(167), Pornește); Link_VALUE(끝, cod_dimensiona); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; cerință_VALUE('('); if (종류() != ';') atribuire_VALUE(true); cerință_VALUE(';');
            int condiție = cod_dimensiona; if (종류() == ';') 내보내기(4); else verifica_Tip(expresie_VALUE(), 2); cerință_VALUE(';');
            int 끝 = ramură(153), text_corp = ramură(167), reîmprospăta = cod_dimensiona;
            if (종류() != ')') atribuire_VALUE(false); cerință_VALUE(')'); Link_VALUE(ramură(167), condiție); Link_VALUE(text_corp, cod_dimensiona);
            control_declarație(); Link_VALUE(ramură(167), reîmprospăta); Link_VALUE(끝, cod_dimensiona);
            for (int 수 = 0; 수 < local_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Poziție, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Poziție + 1 < token_COUNT && (토큰종류[Poziție + 1] == '(' || 토큰종류[Poziție + 1] == '.')) {
            int Tip_VALUE = expresie_VALUE(); if (Tip_VALUE != 0) 내보내기(87); cerință_VALUE(';'); return false;
        }
        atribuire_VALUE(true); cerință_VALUE(';'); return false;
    }
    static boolean control_declarație() {
        if (Word_VALUE(Poziție, "int") || Word_VALUE(Poziție, "boolean") || Word_VALUE(Poziție, "char") || Word_VALUE(Poziție, "String")
            || Word_VALUE(Poziție, "FileInputStream") || Word_VALUE(Poziție, "FileOutputStream")) eroare_VALUE("local declaration requires braces");
        return declarație_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == Rezultat.length) eroare_VALUE("class file too large"); else Rezultat[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void scriere_Clasă() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(constantă_COUNT);
        for (int 수 = 0; 수 < constantă_dimensiona; 수++) 출바(constantă_VALUE[수]);
        출짧(0x21); 출짧(Clasă_constantă); 출짧(părinte_constantă); 출짧(0); 출짧(0); 출짧(metodă_COUNT);
        for (int 수 = 0; 수 < metodă_COUNT; 수++) {
            출짧(metodă_acces[수]); 출짧(metodă_nume_constantă[수]); 출짧(함수서술[수]); 출짧(1); 출짧(cod_constantă);
            출정(12 + metodă_lungime[수]); 출짧(128); 출짧(함수지역[수]); 출정(metodă_lungime[수]);
            for (int 칸 = 0; 칸 < metodă_lungime[수]; 칸++) 출바(cod_VALUE[metodă_cod[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Pornește() {
        if (utilizator.인수개수() == 1 && 자바도구.같음(utilizator.Argumente(0), "-version")) {
            utilizator.Scriere("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (utilizator.인수개수() != 1) { utilizator.Scriere("Usage: javac FILE.java\n"); return 2; }
        int nume_dimensiona = 자바도구.Nume(nume_de_fișier_SMS, utilizator.Argumente(0));
        if (nume_dimensiona < 6 || nume_dimensiona > 62 || nume_de_fișier_SMS[nume_dimensiona - 5] != '.' || nume_de_fișier_SMS[nume_dimensiona - 4] != 'j'
            || nume_de_fișier_SMS[nume_dimensiona - 3] != 'a' || nume_de_fișier_SMS[nume_dimensiona - 2] != 'v' || nume_de_fișier_SMS[nume_dimensiona - 1] != 'a') {
            utilizator.Scriere("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        sursă_dimensiona = utilizator.파일읽기(nume_de_fișier_SMS, SURSĂ);
        if (sursă_dimensiona < 0) { utilizator.Scriere("javac: cannot read source: "); 자바도구.수쓰기(sursă_dimensiona); utilizator.scriere_caracter_VALUE(10); return 1; }
        sursă_dimensiona = 자바도구.원문해독(SURSĂ, sursă_dimensiona);
        if (sursă_dimensiona < 0) { utilizator.Scriere("javac error: invalid UTF-8 source\n"); return 1; }
        decupa_VALUE(); if (!eroare) 선언읽기();
        if (!eroare) {
            if (token_lungime[Clasă_token] != nume_dimensiona - 5) eroare_VALUE("class name must match file name");
            for (int 수 = 0; 수 < nume_dimensiona - 5; 수++) if (SURSĂ[token_poziție[Clasă_token] + 수] != nume_de_fișier_SMS[수]) eroare_VALUE("class name must match file name");
        }
        for (curent_metodă = 0; curent_metodă < metodă_COUNT && !eroare; curent_metodă++) {
            Poziție = metodă_corp[curent_metodă]; metodă_cod[curent_metodă] = cod_dimensiona; local_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metodă_argument_COUNT[curent_metodă]; 수++) adăuga_local(metodă_argument_nume[curent_metodă * 16 + 수], metodă_argument_Tip[curent_metodă * 16 + 수]);
            boolean restitui_KR = declarație_VALUE();
            if (!restitui_KR && metodă_restitui[curent_metodă] != 0) eroare_VALUE("missing return");
            // ramură 뒤의 합류 지점은 반드시 real_date 명령이어야 한다 (버전 49 검증기).
            if (metodă_restitui[curent_metodă] == 0) 내보내기(177);
            else { boolean întreg = metodă_restitui[curent_metodă] <= 2 || metodă_restitui[curent_metodă] == 5; 내보내기(întreg ? 3 : 1); 내보내기(întreg ? 172 : 176); }
            if (Poziție != metodă_termina_un_apel[curent_metodă]) eroare_VALUE("invalid method body");
            함수지역[curent_metodă] = local_COUNT; metodă_lungime[curent_metodă] = cod_dimensiona - metodă_cod[curent_metodă];
        }
        if (eroare) return 1;
        scriere_Clasă(); if (eroare) return 1;
        nume_de_fișier_SMS[nume_dimensiona - 4] = 'c'; nume_de_fișier_SMS[nume_dimensiona - 3] = 'l'; nume_de_fișier_SMS[nume_dimensiona - 2] = 'a';
        nume_de_fișier_SMS[nume_dimensiona - 1] = 's'; nume_de_fișier_SMS[nume_dimensiona] = 's'; nume_de_fișier_SMS[nume_dimensiona + 1] = 0;
        int KR = utilizator.scriere_Fișier(nume_de_fișier_SMS, Rezultat, 출력크기);
        if (KR < 0) { utilizator.Scriere("javac: cannot save class: "); 자바도구.수쓰기(KR); utilizator.scriere_caracter_VALUE(10); return 1; }
        utilizator.Scriere("Compiled: "); for (int 수 = 0; nume_de_fișier_SMS[수] != 0; 수++) utilizator.scriere_caracter_VALUE(nume_de_fișier_SMS[수]);
        utilizator.Scriere(" (JVM class version 49)\n"); return 0;
    }
}
