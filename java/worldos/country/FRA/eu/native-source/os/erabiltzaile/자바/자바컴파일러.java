// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java iturburu_zuhaitz -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] ITURBURUA = new int[16384], Irteera = new int[16384], KODE_balio = new int[4096];
    static int[] 토큰종류 = new int[2048], token_kargu = new int[2048], token_luzera = new int[2048];
    static int[] konstante_balio = new int[4096], konstante_Geruzak = new int[512];
    static int[] 문자 = new int[512], fitxategi_izen_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int 원문크기, token_ZENBATU, Posizioa, 코드크기, 상수크기, konstante_ZENBATU = 1, 출력크기, karaktere_luzera;
    static boolean errorea;
    static int Gela_token, Gela_konstante, 부모상수, KODE_konstante;
    static int[] 함수이름 = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] 함수인수이름 = new int[512], 함수인수형 = new int[512];
    static int[] 함수본문 = new int[32], 함수끝 = new int[32], 함수코드 = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], 함수명상수 = new int[32], 함수서술 = new int[32];
    static int[] 함수권한 = new int[32];
    static int 함수수, 현재함수, lokal_ZENBATU, 깊이, 식깊이;
    static int[] lokal_izen = new int[128], lokal_MOTA = new int[128], 지역깊이 = new int[128];

    static void hutsegite_balio(String 이유) {
        if (!errorea) {
            erabiltzaile.Idatzi("javac error: "); erabiltzaile.Idatzi(이유);
            erabiltzaile.Idatzi(" at line ");
            int Marra = 1, 끝 = Posizioa < token_ZENBATU ? token_kargu[Posizioa] : 원문크기;
            for (int 수 = 0; 수 < 끝; 수++) if (ITURBURUA[수] == 10) Marra++;
            자바도구.수쓰기(Marra); erabiltzaile.idatzi_karaktere_balio(10);
        }
        errorea = true;
    }
    static boolean karaktere_balio(int balio) { return 문자이름규칙.첫글자(balio); }
    static boolean digitu_balio(int balio) { return balio >= '0' && balio <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= token_ZENBATU || 나 >= token_ZENBATU || token_luzera[가] != token_luzera[나]) return false;
        for (int 수 = 0; 수 < token_luzera[가]; 수++) if (ITURBURUA[token_kargu[가] + 수] != ITURBURUA[token_kargu[나] + 수]) return false;
        return true;
    }
    static boolean Word_balio(int token_balio, String Word_SMS) {
        if (token_balio < 0 || token_balio >= token_ZENBATU || token_luzera[token_balio] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (ITURBURUA[token_kargu[token_balio] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Posizioa < token_ZENBATU ? 토큰종류[Posizioa] : 0; }
    static boolean 받기(int balio) { if (종류() != balio) return false; Posizioa++; return true; }
    static void 요구(int balio) { if (!받기(balio)) hutsegite_balio("unexpected token"); }
    static boolean HARTU_Word(String Word_SMS) { if (!Word_balio(Posizioa, Word_SMS)) return false; Posizioa++; return true; }
    static void 말요구(String Word_SMS) { if (!HARTU_Word(Word_SMS)) hutsegite_balio(Word_SMS); }
    static int identifikatzaile_balio() {
        int EMAITZA = Posizioa;
        if (종류() != 256) hutsegite_balio("identifier required"); else Posizioa++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Exekutatu_2 = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Exekutatu_2 == token_luzera[EMAITZA];
                for (int 칸 = Exekutatu_2; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != ITURBURUA[token_kargu[EMAITZA] + 칸 - Exekutatu_2]) 같음 = false;
                if (같음) hutsegite_balio("reserved word cannot be an identifier");
                Exekutatu_2 = 수 + 1;
            }
        }
        return EMAITZA;
    }
    static void ebaki_balio() {
        int 수 = 0;
        while (수 < 원문크기 && !errorea) {
            int balio = ITURBURUA[수], Exekutatu_2 = 수, 종류 = balio;
            if (balio == 32 || balio == 9 || balio == 10 || balio == 13) { 수++; continue; }
            if (balio == '/' && 수 + 1 < 원문크기 && ITURBURUA[수 + 1] == '/') {
                while (수 < 원문크기 && ITURBURUA[수] != 10) 수++;
                continue;
            }
            if (balio == '/' && 수 + 1 < 원문크기 && ITURBURUA[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < 원문크기 && !(ITURBURUA[수] == '*' && ITURBURUA[수 + 1] == '/')) 수++;
                if (수 + 1 >= 원문크기) { hutsegite_balio("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (karaktere_balio(balio)) { 종류 = 256; while (수 < 원문크기 && 문자이름규칙.이어진글자(ITURBURUA[수])) 수++; }
            else if (digitu_balio(balio)) { 종류 = 257; while (수 < 원문크기 && digitu_balio(ITURBURUA[수])) 수++; }
            else if (balio == '"' || balio == '\'') {
                종류 = balio == '"' ? 258 : 259; 수++;
                while (수 < 원문크기 && ITURBURUA[수] != balio && ITURBURUA[수] != 10 && ITURBURUA[수] != 13) {
                    if (ITURBURUA[수] == '\\') 수++;
                    수++;
                }
                if (수 >= 원문크기 || ITURBURUA[수] != balio) { hutsegite_balio("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < 원문크기) {
                    int Hurrengoa_elementu = ITURBURUA[수];
                    if (balio == '=' && Hurrengoa_elementu == '=') 종류 = 300;
                    if (balio == '!' && Hurrengoa_elementu == '=') 종류 = 301;
                    if (balio == '<' && Hurrengoa_elementu == '=') 종류 = 302;
                    if (balio == '>' && Hurrengoa_elementu == '=') 종류 = 303;
                    if (balio == '&' && Hurrengoa_elementu == '&') 종류 = 304;
                    if (balio == '|' && Hurrengoa_elementu == '|') 종류 = 305;
                    if (balio == '+' && Hurrengoa_elementu == '+') 종류 = 306;
                    if (balio == '-' && Hurrengoa_elementu == '-') 종류 = 307;
                    if (balio == '+' && Hurrengoa_elementu == '=') 종류 = 308;
                    if (balio == '-' && Hurrengoa_elementu == '=') 종류 = 309;
                    if (balio == '*' && Hurrengoa_elementu == '=') 종류 = 310;
                    if (balio == '/' && Hurrengoa_elementu == '=') 종류 = 311;
                    if (balio == '%' && Hurrengoa_elementu == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_ZENBATU == 토큰종류.length - 1) { hutsegite_balio("too many tokens (2047 maximum)"); break; }
            토큰종류[token_ZENBATU] = 종류; token_kargu[token_ZENBATU] = Exekutatu_2; token_luzera[token_ZENBATU++] = 수 - Exekutatu_2;
        }
    }
    static void idatzi_konstante_byte(int balio) {
        if (상수크기 == konstante_balio.length) { hutsegite_balio("constant pool too large"); return; }
        konstante_balio[상수크기++] = balio & 255;
    }
    static void 상짧(int balio) { idatzi_konstante_byte(balio >> 8); idatzi_konstante_byte(balio); }
    static int izena_eman_konstante(int Exekutatu_2) {
        for (int 수 = 1; 수 < konstante_ZENBATU; 수++) {
            int aurrekoa_balio = konstante_Geruzak[수], luzera_balio = (수 + 1 < konstante_ZENBATU ? konstante_Geruzak[수 + 1] : Exekutatu_2) - aurrekoa_balio;
            if (luzera_balio != 상수크기 - Exekutatu_2) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < luzera_balio; 칸++) if (konstante_balio[aurrekoa_balio + 칸] != konstante_balio[Exekutatu_2 + 칸]) 같음 = false;
            if (같음) { 상수크기 = Exekutatu_2; return 수; }
        }
        if (konstante_ZENBATU == konstante_Geruzak.length) { hutsegite_balio("too many constants"); return 0; }
        konstante_Geruzak[konstante_ZENBATU] = Exekutatu_2;
        return konstante_ZENBATU++;
    }
    static void Erantsi_SMS(int balio) {
        if (karaktere_luzera == 문자.length) { hutsegite_balio("text too long"); return; }
        문자[karaktere_luzera++] = balio;
    }
    static void Erantsi_Word(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) Erantsi_SMS(Word_SMS.charAt(수)); }
    static int karaktere_konstante() {
        int Exekutatu_2 = 상수크기; idatzi_konstante_byte(1); 상짧(0);
        for (int 수 = 0; 수 < karaktere_luzera; 수++) {
            int balio = 문자[수];
            if (balio > 0 && balio < 128) idatzi_konstante_byte(balio);
            else if (balio < 2048) { idatzi_konstante_byte(192 | balio >> 6); idatzi_konstante_byte(128 | balio & 63); }
            else { idatzi_konstante_byte(224 | balio >> 12); idatzi_konstante_byte(128 | balio >> 6 & 63); idatzi_konstante_byte(128 | balio & 63); }
        }
        if (errorea) return 0;
        int luzera_balio = 상수크기 - Exekutatu_2 - 3;
        konstante_balio[Exekutatu_2 + 1] = luzera_balio >> 8; konstante_balio[Exekutatu_2 + 2] = luzera_balio & 255;
        return izena_eman_konstante(Exekutatu_2);
    }
    static int Word_konstante(String Word_SMS) { karaktere_luzera = 0; Erantsi_Word(Word_SMS); return karaktere_konstante(); }
    static int token_konstante(int token_balio) {
        karaktere_luzera = 0;
        for (int 수 = 0; 수 < token_luzera[token_balio]; 수++) Erantsi_SMS(ITURBURUA[token_kargu[token_balio] + 수]);
        return karaktere_konstante();
    }
    static int Erreferentzia_materiala(int 종류, int 가, int 나) {
        int Exekutatu_2 = 상수크기; idatzi_konstante_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return izena_eman_konstante(Exekutatu_2);
    }
    static int 외부참조(int 종류, String jabe_balio, String Izena, String 서술) {
        int jabe_identifikatzaile = Erreferentzia_materiala(7, Word_konstante(jabe_balio), 0);
        int izen_ZENBATU = Word_konstante(Izena), formatu_ZENBATU = Word_konstante(서술);
        return Erreferentzia_materiala(종류, jabe_identifikatzaile, Erreferentzia_materiala(12, izen_ZENBATU, formatu_ZENBATU));
    }
    static void 내보내기(int balio) {
        if (코드크기 == KODE_balio.length) { hutsegite_balio("bytecode too large"); return; }
        KODE_balio[코드크기++] = balio & 255;
    }
    static void Komandoa(int balio, int Argumentuak) { 내보내기(balio); 내보내기(Argumentuak >> 8); 내보내기(Argumentuak); }
    static void 수상수(int balio) {
        if (balio >= -1 && balio <= 5) { 내보내기(balio + 3); return; }
        int Exekutatu_2 = 상수크기; idatzi_konstante_byte(3); 상짧(balio >>> 16); 상짧(balio);
        Komandoa(19, izena_eman_konstante(Exekutatu_2));
    }
    static int adar(int Komandoa) { int EMAITZA = 코드크기; Komandoa(Komandoa, 0); return EMAITZA; }
    static void lotu_balio(int adar, int helburu_objektu) {
        if (errorea) return;
        int 거리 = helburu_objektu - adar;
        if (거리 < -32768 || 거리 > 32767 || adar < 0 || adar + 2 >= 코드크기) { hutsegite_balio("invalid branch"); return; }
        KODE_balio[adar + 1] = 거리 >> 8 & 255; KODE_balio[adar + 2] = 거리 & 255;
    }
    static void Konparazioa_balio(int Komandoa) {
        int EGIAZKOA_balio = adar(Komandoa); 내보내기(3); int 끝 = adar(167);
        lotu_balio(EGIAZKOA_balio, 코드크기); 내보내기(4); lotu_balio(끝, 코드크기);
    }
    static int formatu_balio() {
        if (HARTU_Word("void")) return 0;
        if (HARTU_Word("int")) return 1;
        if (HARTU_Word("boolean")) return 2;
        if (HARTU_Word("char")) return 5;
        if (HARTU_Word("FileInputStream")) return 6;
        if (HARTU_Word("FileOutputStream")) return 7;
        if (HARTU_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        hutsegite_balio("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void gehitu_formatu(int MOTA_balio) {
        if (MOTA_balio == 0) Erantsi_SMS('V');
        if (MOTA_balio == 1) Erantsi_SMS('I');
        if (MOTA_balio == 2) Erantsi_SMS('Z');
        if (MOTA_balio == 3) Erantsi_Word("Ljava/lang/String;");
        if (MOTA_balio == 4) Erantsi_Word("[Ljava/lang/String;");
        if (MOTA_balio == 5) Erantsi_SMS('C');
        if (MOTA_balio == 6) Erantsi_Word("Ljava/io/FileInputStream;");
        if (MOTA_balio == 7) Erantsi_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklarazio. salbuespen prozesu_balio_sarrera 본문은 Ostalari javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = HARTU_Word("Euskara");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (HARTU_Word("Exception") || HARTU_Word("IOException"))) return;
        if (HARTU_Word("salbuespen") || HARTU_Word("실행예외") || HARTU_Word("S_I_salbuespen") || HARTU_Word("itxaron_DENBORA_MUGA_salbuespen") || HARTU_Word("helbide_BEGIRATU_salbuespen") || HARTU_Word("파일없음예외") || HARTU_Word("통신예외") || HARTU_Word("baliogabe_arg_salbuespen") || HARTU_Word("숫자형식예외") || HARTU_Word("범위예외") || HARTU_Word("배열범위예외") || HARTU_Word("문자열범위예외") || HARTU_Word("nulu_Erreferentzia_materiala_salbuespen") || HARTU_Word("산술예외") || HARTU_Word("Egoera_salbuespen") || HARTU_Word("MOTA_igorri_salbuespen") || HARTU_Word("음수배열크기예외") || HARTU_Word("matrize_Store_hutsegite") || HARTU_Word("hari_Egoera_salbuespen") || HARTU_Word("대기중단예외")) return;
        hutsegite_balio("unsupported throws type");
    }
    static void 선언읽기() {
        while (HARTU_Word("import")) {
            if (Word_balio(Posizioa, "Euskara")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(HARTU_Word("FileInputStream") || HARTU_Word("FileOutputStream") || HARTU_Word("IOException"))) hutsegite_balio("unsupported import");
            }
            요구(';');
        }
        HARTU_Word("public"); HARTU_Word("final"); 말요구("class"); Gela_token = identifikatzaile_balio();
        Gela_konstante = Erreferentzia_materiala(7, token_konstante(Gela_token), 0);
        부모상수 = Erreferentzia_materiala(7, Word_konstante("java/lang/Object"), 0); KODE_konstante = Word_konstante("Code"); 요구('{');
        while (!errorea && 종류() != '}') {
            if (함수수 == 32) { hutsegite_balio("too many methods"); break; }
            int atzitu_sarrera = HARTU_Word("public") ? 1 : HARTU_Word("private") ? 2 : 0; 말요구("static");
            int FUNTZIOA_balio = 함수수++;
            함수권한[FUNTZIOA_balio] = atzitu_sarrera | 8;
            함수반환[FUNTZIOA_balio] = formatu_balio(); 함수이름[FUNTZIOA_balio] = identifikatzaile_balio(); 요구('(');
            for (int aurrekoa_balio = 0; aurrekoa_balio < FUNTZIOA_balio; aurrekoa_balio++) if (이름같음(함수이름[aurrekoa_balio], 함수이름[FUNTZIOA_balio])) hutsegite_balio("duplicate method (overloading unsupported)");
            while (!errorea && 종류() != ')') {
                int 수 = 함수인수수[FUNTZIOA_balio];
                if (수 == 16) { hutsegite_balio("too many parameters"); break; }
                int MOTA_balio = formatu_balio(); if (MOTA_balio == 0) hutsegite_balio("void parameter");
                함수인수형[FUNTZIOA_balio * 16 + 수] = MOTA_balio; 함수인수이름[FUNTZIOA_balio * 16 + 수] = identifikatzaile_balio();
                함수인수수[FUNTZIOA_balio]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (HARTU_Word("throws")) {
                do { 예외이름읽기(); } while (!errorea && 받기(','));
            }
            함수본문[FUNTZIOA_balio] = Posizioa; 요구('{');
            int habiaratze_balio = 1;
            while (Posizioa < token_ZENBATU && habiaratze_balio > 0) {
                if (종류() == '{') habiaratze_balio++;
                if (종류() == '}') habiaratze_balio--;
                Posizioa++;
            }
            if (habiaratze_balio != 0) hutsegite_balio("unclosed method body");
            함수끝[FUNTZIOA_balio] = Posizioa;
            함수명상수[FUNTZIOA_balio] = token_konstante(함수이름[FUNTZIOA_balio]);
            karaktere_luzera = 0; Erantsi_SMS('(');
            for (int 수 = 0; 수 < 함수인수수[FUNTZIOA_balio]; 수++) gehitu_formatu(함수인수형[FUNTZIOA_balio * 16 + 수]);
            Erantsi_SMS(')'); gehitu_formatu(함수반환[FUNTZIOA_balio]); 함수서술[FUNTZIOA_balio] = karaktere_konstante();
        }
        요구('}'); if (Posizioa != token_ZENBATU) hutsegite_balio("extra input after class");
    }
    static int Bilatu_lokal(int Izena) {
        for (int 수 = lokal_ZENBATU - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokal_izen[수], Izena)) return 수;
        hutsegite_balio("unknown variable"); return 0;
    }
    static int gehitu_lokal(int Izena, int MOTA_balio) {
        for (int 수 = 0; 수 < lokal_ZENBATU; 수++) if (지역깊이[수] >= 0 && 이름같음(lokal_izen[수], Izena)) hutsegite_balio("duplicate local variable");
        if (lokal_ZENBATU == 128) { hutsegite_balio("too many locals"); return 0; }
        lokal_izen[lokal_ZENBATU] = Izena; lokal_MOTA[lokal_ZENBATU] = MOTA_balio; 지역깊이[lokal_ZENBATU] = 깊이;
        return lokal_ZENBATU++;
    }
    static boolean osoko_zenbaki_MOTA(int MOTA_balio) { return MOTA_balio == 1 || MOTA_balio == 5; }
    static void 지역읽기(int 수) { 내보내기(lokal_MOTA[수] <= 2 || lokal_MOTA[수] == 5 ? 21 : 25); 내보내기(수); }
    static void idatzi_lokal(int 수) { 내보내기(lokal_MOTA[수] <= 2 || lokal_MOTA[수] == 5 ? 54 : 58); 내보내기(수); }
    static void egiaztatu_MOTA(int benetako_datuak, int 기대) { if (benetako_datuak != 기대 && !(benetako_datuak == 5 && 기대 == 1)) hutsegite_balio("type mismatch"); }
    static void 문자읽기(int token_balio) {
        karaktere_luzera = 0; int Exekutatu_2 = token_kargu[token_balio] + 1, 끝 = token_kargu[token_balio] + token_luzera[token_balio] - 1;
        while (Exekutatu_2 < 끝 && !errorea) {
            int balio = ITURBURUA[Exekutatu_2++];
            if (balio == '\\') {
                if (Exekutatu_2 == 끝) { hutsegite_balio("invalid escape"); break; }
                balio = ITURBURUA[Exekutatu_2++];
                if (balio == 'n') balio = 10;
                else if (balio == 'r') balio = 13;
                else if (balio == 't') balio = 9;
                else if (balio == 'b') balio = 8;
                else if (balio == 'f') balio = 12;
                else if (balio != '\\' && balio != '"' && balio != '\'') hutsegite_balio("unsupported escape");
            }
            Erantsi_SMS(balio);
        }
    }
    static int analizatu_osoko_zenbaki(int token_balio, boolean 음수) {
        if (token_luzera[token_balio] > 1 && ITURBURUA[token_kargu[token_balio]] == '0') hutsegite_balio("octal literals unsupported");
        int balio = 0;
        for (int 수 = 0; 수 < token_luzera[token_balio]; 수++) {
            int digitu_elementu = ITURBURUA[token_kargu[token_balio] + 수] - '0';
            if (balio < -214748364 || balio == -214748364 && digitu_elementu > (음수 ? 8 : 7)) hutsegite_balio("integer literal out of range");
            balio = balio * 10 - digitu_elementu;
        }
        return 음수 ? balio : -balio;
    }
    static int 기본식() {
        if (HARTU_Word("new")) {
            int MOTA_balio = formatu_balio();
            if (MOTA_balio != 6 && MOTA_balio != 7) { hutsegite_balio("only file streams supported by new in source"); return 0; }
            String jabe_balio = MOTA_balio == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Komandoa(187, Erreferentzia_materiala(7, Word_konstante(jabe_balio), 0)); 내보내기(89);
            요구('('); egiaztatu_MOTA(adierazpen_balio(), 3); boolean 이어 = false;
            if (받기(',')) { if (MOTA_balio != 7) hutsegite_balio("input stream constructor arguments"); egiaztatu_MOTA(adierazpen_balio(), 2); 이어 = true; }
            요구(')');
            Komandoa(183, 외부참조(10, jabe_balio, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return MOTA_balio;
        }
        if (받기('(')) { int MOTA_balio = adierazpen_balio(); 요구(')'); return MOTA_balio; }
        if (종류() == 257) { 수상수(analizatu_osoko_zenbaki(Posizioa++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Posizioa++); Komandoa(19, Erreferentzia_materiala(8, karaktere_konstante(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Posizioa++); if (karaktere_luzera != 1) hutsegite_balio("character literal length"); 수상수(문자[0]); return 5; }
        if (HARTU_Word("true")) { 내보내기(4); return 2; }
        if (HARTU_Word("false")) { 내보내기(3); return 2; }
        if (HARTU_Word("Euskara")) {
            요구('.'); 말요구("자체"); 요구('.');
            String jabe_balio = "", 메서드 = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, EMAITZA = 0;
            if (HARTU_Word("Irteera")) {
                jabe_balio = "Euskara/자체/Irteera"; 요구('.');
                if (HARTU_Word("idatzi_lerro")) { 메서드 = "idatzi_lerro"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (HARTU_Word("Idatzi")) { 메서드 = "Idatzi"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (HARTU_Word("수쓰기")) { 메서드 = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else hutsegite_balio("unknown Korean output method");
            } else if (HARTU_Word("문자")) {
                jabe_balio = "Euskara/자체/문자"; 요구('.'); 가 = 3;
                if (HARTU_Word("luzera_balio")) { 메서드 = "luzera_balio"; 서술 = "(Ljava/lang/String;)I"; EMAITZA = 1; }
                else if (HARTU_Word("karaktere_kode_ZENBATU")) { 메서드 = "karaktere_kode_ZENBATU"; 서술 = "(Ljava/lang/String;)I"; EMAITZA = 1; }
                else if (HARTU_Word("analizatu_osoko_zenbaki")) { 메서드 = "analizatu_osoko_zenbaki"; 서술 = "(Ljava/lang/String;)I"; EMAITZA = 1; }
                else if (HARTU_Word("idatzi_osoko_zenbaki_balio")) { 메서드 = "idatzi_osoko_zenbaki_balio"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; EMAITZA = 3; }
                else if (HARTU_Word("같음")) { 메서드 = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; EMAITZA = 2; }
                else if (HARTU_Word("itsatsi_SMS")) { 메서드 = "itsatsi_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; EMAITZA = 3; }
                else if (HARTU_Word("ebaki_balio")) { 메서드 = "ebaki_balio"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; EMAITZA = 3; }
                else hutsegite_balio("unknown Korean text method");
            } else if (HARTU_Word("Fitxategia")) {
                jabe_balio = "Euskara/자체/Fitxategia"; 요구('.'); 가 = 3;
                if (HARTU_Word("Irakurri")) { 메서드 = "Irakurri"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; EMAITZA = 3; }
                else if (HARTU_Word("Idatzi")) { 메서드 = "Idatzi"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else hutsegite_balio("unknown Korean file method");
            } else if (HARTU_Word("화면")) {
                jabe_balio = "Euskara/자체/화면"; 요구('.');
                if (HARTU_Word("너비")) { 메서드 = "너비"; 서술 = "()I"; EMAITZA = 1; }
                else if (HARTU_Word("높이")) { 메서드 = "높이"; 서술 = "()I"; EMAITZA = 1; }
                else if (HARTU_Word("사각형")) { 메서드 = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (HARTU_Word("ezabatu_sarrera")) { 메서드 = "ezabatu_sarrera"; 서술 = "(I)V"; 가 = 1; }
                else if (HARTU_Word("기다리기")) { 메서드 = "기다리기"; 서술 = "()V"; }
                else hutsegite_balio("unknown Korean framebuffer method");
            } else hutsegite_balio("unsupported Korean library class");
            요구('('); if (가 != 0) egiaztatu_MOTA(adierazpen_balio(), 가);
            if (나 != 0) { 요구(','); egiaztatu_MOTA(adierazpen_balio(), 나); }
            if (다 != 0) { 요구(','); egiaztatu_MOTA(adierazpen_balio(), 다); }
            if (라 != 0) { 요구(','); egiaztatu_MOTA(adierazpen_balio(), 라); }
            if (마 != 0) { 요구(','); egiaztatu_MOTA(adierazpen_balio(), 마); }
            요구(')'); Komandoa(184, 외부참조(10, jabe_balio, 메서드, 서술)); return EMAITZA;
        }
        if (HARTU_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); egiaztatu_MOTA(adierazpen_balio(), 3); 요구(')');
            Komandoa(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Izena = identifikatzaile_balio();
        if (받기('(')) {
            int FUNTZIOA_balio = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Izena, 함수이름[수])) FUNTZIOA_balio = 수;
            if (FUNTZIOA_balio < 0) { hutsegite_balio("unknown static method"); return 0; }
            int 수 = 0;
            while (!errorea && 종류() != ')') {
                if (수 >= 함수인수수[FUNTZIOA_balio]) { hutsegite_balio("too many arguments"); break; }
                egiaztatu_MOTA(adierazpen_balio(), 함수인수형[FUNTZIOA_balio * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[FUNTZIOA_balio]) hutsegite_balio("argument count mismatch");
            Komandoa(184, Erreferentzia_materiala(10, Gela_konstante, Erreferentzia_materiala(12, 함수명상수[FUNTZIOA_balio], 함수서술[FUNTZIOA_balio])));
            return 함수반환[FUNTZIOA_balio];
        }
        int lokal_esparru = Bilatu_lokal(Izena), MOTA_balio = lokal_MOTA[lokal_esparru]; 지역읽기(lokal_esparru);
        while (!errorea) {
            if (받기('[')) { egiaztatu_MOTA(MOTA_balio, 4); egiaztatu_MOTA(adierazpen_balio(), 1); 요구(']'); 내보내기(50); MOTA_balio = 3; }
            else if (받기('.')) {
                if (MOTA_balio == 6 || MOTA_balio == 7) {
                    String jabe_balio = MOTA_balio == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (HARTU_Word("close")) { 요구('('); 요구(')'); Komandoa(182, 외부참조(10, jabe_balio, "close", "()V")); MOTA_balio = 0; }
                    else if (MOTA_balio == 6 && HARTU_Word("read")) { 요구('('); 요구(')'); Komandoa(182, 외부참조(10, jabe_balio, "read", "()I")); MOTA_balio = 1; }
                    else if (MOTA_balio == 7 && HARTU_Word("write")) { 요구('('); egiaztatu_MOTA(adierazpen_balio(), 1); 요구(')'); Komandoa(182, 외부참조(10, jabe_balio, "write", "(I)V")); MOTA_balio = 0; }
                    else { hutsegite_balio("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (MOTA_balio == 4) { 내보내기(190); MOTA_balio = 1; }
                else { egiaztatu_MOTA(MOTA_balio, 3); 요구('('); 요구(')'); Komandoa(182, 외부참조(10, "java/lang/String", "length", "()I")); MOTA_balio = 1; }
            } else break;
        }
        return MOTA_balio;
    }
    static int 단항() {
        if (++식깊이 > 64) { hutsegite_balio("expression nesting too deep"); 식깊이--; return 0; }
        int MOTA_balio;
        if (받기('!')) { egiaztatu_MOTA(단항(), 2); Konparazioa_balio(153); MOTA_balio = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(analizatu_osoko_zenbaki(Posizioa++, true));
            else { egiaztatu_MOTA(단항(), 1); 내보내기(116); }
            MOTA_balio = 1;
        } else if (받기('+')) { egiaztatu_MOTA(단항(), 1); MOTA_balio = 1; }
        else MOTA_balio = 기본식();
        식깊이--; return MOTA_balio;
    }
    static int 곱식() {
        int MOTA_balio = 단항();
        while (!errorea && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodeketa_balio = 종류(); Posizioa++; egiaztatu_MOTA(MOTA_balio, 1); egiaztatu_MOTA(단항(), 1);
            내보내기(kodeketa_balio == '*' ? 104 : kodeketa_balio == '/' ? 108 : 112); MOTA_balio = 1;
        }
        return MOTA_balio;
    }
    static int 합식() {
        int MOTA_balio = 곱식();
        while (!errorea && (종류() == '+' || 종류() == '-')) {
            int kodeketa_balio = 종류(); Posizioa++; int 경계 = 코드크기, ATZERA_balio_MOTA = 곱식();
            if (kodeketa_balio == '+' && (MOTA_balio == 3 || ATZERA_balio_MOTA == 3)) { 결합(경계, MOTA_balio, ATZERA_balio_MOTA); MOTA_balio = 3; }
            else { egiaztatu_MOTA(MOTA_balio, 1); egiaztatu_MOTA(ATZERA_balio_MOTA, 1); 내보내기(kodeketa_balio == '+' ? 96 : 100); MOTA_balio = 1; }
        }
        return MOTA_balio;
    }
    static int 붙임참조(int MOTA_balio) {
        if (MOTA_balio != 1 && MOTA_balio != 2 && MOTA_balio != 3 && MOTA_balio != 5) hutsegite_balio("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", MOTA_balio == 1 ? "(I)Ljava/lang/StringBuilder;"
            : MOTA_balio == 2 ? "(Z)Ljava/lang/StringBuilder;" : MOTA_balio == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int aurrekoa_balio_MOTA, int ATZERA_balio_MOTA) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 ESKUIN KODE_balio 앞에 sortu 코드를 삽입한다.
        // ESKUIN adierazpen_balio 내부의 pareko_balio adar 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        Komandoa(187, Erreferentzia_materiala(7, Word_konstante("java/lang/StringBuilder"), 0)); 내보내기(89);
        Komandoa(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Komandoa(182, 붙임참조(aurrekoa_balio_MOTA));
        if (errorea) return;
        int luzera_balio = 코드크기 - 끝;
        for (int 수 = 0; 수 < luzera_balio; 수++) 삽입코드[수] = KODE_balio[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) KODE_balio[수 + luzera_balio] = KODE_balio[수];
        for (int 수 = 0; 수 < luzera_balio; 수++) KODE_balio[경계 + 수] = 삽입코드[수];
        Komandoa(182, 붙임참조(ATZERA_balio_MOTA)); Komandoa(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Konparazioa_adierazpen() {
        int MOTA_balio = 합식();
        while (!errorea && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodeketa_balio = 종류(); Posizioa++; egiaztatu_MOTA(MOTA_balio, 1); egiaztatu_MOTA(합식(), 1);
            Konparazioa_balio(kodeketa_balio == '<' ? 161 : kodeketa_balio == '>' ? 163 : kodeketa_balio == 302 ? 164 : 162); MOTA_balio = 2;
        }
        return MOTA_balio;
    }
    static int 동등식() {
        int MOTA_balio = Konparazioa_adierazpen();
        while (!errorea && (종류() == 300 || 종류() == 301)) {
            int kodeketa_balio = 종류(); Posizioa++; int ATZERA_balio_MOTA = Konparazioa_adierazpen();
            if (MOTA_balio == 0 || ATZERA_balio_MOTA == 0) hutsegite_balio("void expression");
            if (!(osoko_zenbaki_MOTA(MOTA_balio) && osoko_zenbaki_MOTA(ATZERA_balio_MOTA))) egiaztatu_MOTA(ATZERA_balio_MOTA, MOTA_balio);
            Konparazioa_balio((MOTA_balio <= 2 || MOTA_balio == 5 ? 159 : 165) + (kodeketa_balio == 301 ? 1 : 0)); MOTA_balio = 2;
        }
        return MOTA_balio;
    }
    static int 논리곱() {
        int MOTA_balio = 동등식();
        while (!errorea && 받기(304)) {
            egiaztatu_MOTA(MOTA_balio, 2); int 가 = adar(153); egiaztatu_MOTA(동등식(), 2); int 나 = adar(153);
            내보내기(4); int 끝 = adar(167); lotu_balio(가, 코드크기); lotu_balio(나, 코드크기); 내보내기(3); lotu_balio(끝, 코드크기); MOTA_balio = 2;
        }
        return MOTA_balio;
    }
    static int adierazpen_balio() {
        int MOTA_balio = 논리곱();
        while (!errorea && 받기(305)) {
            egiaztatu_MOTA(MOTA_balio, 2); int 가 = adar(154); egiaztatu_MOTA(논리곱(), 2); int 나 = adar(154);
            내보내기(3); int 끝 = adar(167); lotu_balio(가, 코드크기); lotu_balio(나, 코드크기); 내보내기(4); lotu_balio(끝, 코드크기); MOTA_balio = 2;
        }
        return MOTA_balio;
    }
    static void lan_balio_031eac11(boolean Onartu_deklarazio) {
        if (Word_balio(Posizioa, "int") || Word_balio(Posizioa, "boolean") || Word_balio(Posizioa, "String") || Word_balio(Posizioa, "char")
            || Word_balio(Posizioa, "FileInputStream") || Word_balio(Posizioa, "FileOutputStream")) {
            if (!Onartu_deklarazio) hutsegite_balio("declaration not allowed here");
            int MOTA_balio = formatu_balio(), Izena = identifikatzaile_balio(); 요구('='); egiaztatu_MOTA(adierazpen_balio(), MOTA_balio);
            idatzi_lokal(gehitu_lokal(Izena, MOTA_balio)); return;
        }
        int Izena = identifikatzaile_balio(), lokal_esparru = Bilatu_lokal(Izena);
        if (받기('=')) { egiaztatu_MOTA(adierazpen_balio(), lokal_MOTA[lokal_esparru]); idatzi_lokal(lokal_esparru); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodeketa_balio = 종류(); Posizioa++; 지역읽기(lokal_esparru); int 경계 = 코드크기, ATZERA_balio_MOTA = adierazpen_balio();
            if (kodeketa_balio == 308 && lokal_MOTA[lokal_esparru] == 3) 결합(경계, 3, ATZERA_balio_MOTA);
            else {
                egiaztatu_MOTA(lokal_MOTA[lokal_esparru], 1); egiaztatu_MOTA(ATZERA_balio_MOTA, 1);
                내보내기(kodeketa_balio == 308 ? 96 : kodeketa_balio == 309 ? 100 : kodeketa_balio == 310 ? 104 : kodeketa_balio == 311 ? 108 : 112);
                if (lokal_MOTA[lokal_esparru] == 5) 내보내기(146);
            }
            idatzi_lokal(lokal_esparru);
        }
        else if (종류() == 306 || 종류() == 307) {
            egiaztatu_MOTA(lokal_MOTA[lokal_esparru], 1); 내보내기(132); 내보내기(lokal_esparru); 내보내기(종류() == 306 ? 1 : 255); Posizioa++;
            if (lokal_MOTA[lokal_esparru] == 5) { 지역읽기(lokal_esparru); 내보내기(146); idatzi_lokal(lokal_esparru); }
        } else hutsegite_balio("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = HARTU_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Komandoa(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int MOTA_balio = 빈인수 ? 0 : adierazpen_balio(); 요구(')'); 요구(';');
        String 서술 = MOTA_balio == 0 ? "()V" : MOTA_balio == 1 ? "(I)V" : MOTA_balio == 2 ? "(Z)V" : MOTA_balio == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (MOTA_balio == 4 || MOTA_balio >= 6 || MOTA_balio == 0 && (!줄바꿈 || !빈인수)) hutsegite_balio("unsupported print argument");
        Komandoa(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean instrukzio_balio() {
        if (errorea) return false;
        if (깊이 > 32) { hutsegite_balio("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean itzuli_neurria = false;
            while (!errorea && 종류() != '}') { if (itzuli_neurria) hutsegite_balio("unreachable statement"); itzuli_neurria = instrukzio_balio(); }
            요구('}'); for (int 수 = 0; 수 < lokal_ZENBATU; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return itzuli_neurria;
        }
        if (받기(';')) return false;
        if (HARTU_Word("return")) {
            int MOTA_balio = 종류() == ';' ? 0 : adierazpen_balio(); egiaztatu_MOTA(MOTA_balio, 함수반환[현재함수]); 요구(';');
            내보내기(MOTA_balio == 0 ? 177 : MOTA_balio <= 2 || MOTA_balio == 5 ? 172 : 176); return true;
        }
        if (HARTU_Word("if")) {
            요구('('); egiaztatu_MOTA(adierazpen_balio(), 2); 요구(')'); int FALTSUA_balio = adar(153);
            깊이++; boolean 가 = kontrol_instrukzio(); 깊이--;
            if (HARTU_Word("else")) { int 끝 = adar(167); lotu_balio(FALTSUA_balio, 코드크기); 깊이++; boolean 나 = kontrol_instrukzio(); 깊이--; lotu_balio(끝, 코드크기); return 가 && 나; }
            lotu_balio(FALTSUA_balio, 코드크기); return false;
        }
        if (HARTU_Word("while")) {
            int Exekutatu_2 = 코드크기; 요구('('); egiaztatu_MOTA(adierazpen_balio(), 2); 요구(')'); int 끝 = adar(153);
            깊이++; kontrol_instrukzio(); 깊이--; lotu_balio(adar(167), Exekutatu_2); lotu_balio(끝, 코드크기); return false;
        }
        if (HARTU_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') lan_balio_031eac11(true); 요구(';');
            int baldintza = 코드크기; if (종류() == ';') 내보내기(4); else egiaztatu_MOTA(adierazpen_balio(), 2); 요구(';');
            int 끝 = adar(153), testu_nagusi = adar(167), freskatu = 코드크기;
            if (종류() != ')') lan_balio_031eac11(false); 요구(')'); lotu_balio(adar(167), baldintza); lotu_balio(testu_nagusi, 코드크기);
            kontrol_instrukzio(); lotu_balio(adar(167), freskatu); lotu_balio(끝, 코드크기);
            for (int 수 = 0; 수 < lokal_ZENBATU; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_balio(Posizioa, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Posizioa + 1 < token_ZENBATU && (토큰종류[Posizioa + 1] == '(' || 토큰종류[Posizioa + 1] == '.')) {
            int MOTA_balio = adierazpen_balio(); if (MOTA_balio != 0) 내보내기(87); 요구(';'); return false;
        }
        lan_balio_031eac11(true); 요구(';'); return false;
    }
    static boolean kontrol_instrukzio() {
        if (Word_balio(Posizioa, "int") || Word_balio(Posizioa, "boolean") || Word_balio(Posizioa, "char") || Word_balio(Posizioa, "String")
            || Word_balio(Posizioa, "FileInputStream") || Word_balio(Posizioa, "FileOutputStream")) hutsegite_balio("local declaration requires braces");
        return instrukzio_balio();
    }
    static void 출바(int balio) { if (출력크기 == Irteera.length) hutsegite_balio("class file too large"); else Irteera[출력크기++] = balio & 255; }
    static void 출짧(int balio) { 출바(balio >> 8); 출바(balio); }
    static void 출정(int balio) { 출짧(balio >>> 16); 출짧(balio); }
    static void idatzi_Gela() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstante_ZENBATU);
        for (int 수 = 0; 수 < 상수크기; 수++) 출바(konstante_balio[수]);
        출짧(0x21); 출짧(Gela_konstante); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(함수권한[수]); 출짧(함수명상수[수]); 출짧(함수서술[수]); 출짧(1); 출짧(KODE_konstante);
            출정(12 + 함수길이[수]); 출짧(128); 출짧(함수지역[수]); 출정(함수길이[수]);
            for (int 칸 = 0; 칸 < 함수길이[수]; 칸++) 출바(KODE_balio[함수코드[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Exekutatu_2() {
        if (erabiltzaile.인수개수() == 1 && 자바도구.같음(erabiltzaile.Argumentuak(0), "-version")) {
            erabiltzaile.Idatzi("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (erabiltzaile.인수개수() != 1) { erabiltzaile.Idatzi("Usage: javac FILE.java\n"); return 2; }
        int 이름크기 = 자바도구.Izena(fitxategi_izen_SMS, erabiltzaile.Argumentuak(0));
        if (이름크기 < 6 || 이름크기 > 62 || fitxategi_izen_SMS[이름크기 - 5] != '.' || fitxategi_izen_SMS[이름크기 - 4] != 'j'
            || fitxategi_izen_SMS[이름크기 - 3] != 'a' || fitxategi_izen_SMS[이름크기 - 2] != 'v' || fitxategi_izen_SMS[이름크기 - 1] != 'a') {
            erabiltzaile.Idatzi("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        원문크기 = erabiltzaile.파일읽기(fitxategi_izen_SMS, ITURBURUA);
        if (원문크기 < 0) { erabiltzaile.Idatzi("javac: cannot read source: "); 자바도구.수쓰기(원문크기); erabiltzaile.idatzi_karaktere_balio(10); return 1; }
        원문크기 = 자바도구.원문해독(ITURBURUA, 원문크기);
        if (원문크기 < 0) { erabiltzaile.Idatzi("javac error: invalid UTF-8 source\n"); return 1; }
        ebaki_balio(); if (!errorea) 선언읽기();
        if (!errorea) {
            if (token_luzera[Gela_token] != 이름크기 - 5) hutsegite_balio("class name must match file name");
            for (int 수 = 0; 수 < 이름크기 - 5; 수++) if (ITURBURUA[token_kargu[Gela_token] + 수] != fitxategi_izen_SMS[수]) hutsegite_balio("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !errorea; 현재함수++) {
            Posizioa = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; lokal_ZENBATU = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) gehitu_lokal(함수인수이름[현재함수 * 16 + 수], 함수인수형[현재함수 * 16 + 수]);
            boolean itzuli_neurria = instrukzio_balio();
            if (!itzuli_neurria && 함수반환[현재함수] != 0) hutsegite_balio("missing return");
            // adar 뒤의 합류 지점은 반드시 benetako_datuak 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean osoko_zenbaki = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(osoko_zenbaki ? 3 : 1); 내보내기(osoko_zenbaki ? 172 : 176); }
            if (Posizioa != 함수끝[현재함수]) hutsegite_balio("invalid method body");
            함수지역[현재함수] = lokal_ZENBATU; 함수길이[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (errorea) return 1;
        idatzi_Gela(); if (errorea) return 1;
        fitxategi_izen_SMS[이름크기 - 4] = 'c'; fitxategi_izen_SMS[이름크기 - 3] = 'l'; fitxategi_izen_SMS[이름크기 - 2] = 'a';
        fitxategi_izen_SMS[이름크기 - 1] = 's'; fitxategi_izen_SMS[이름크기] = 's'; fitxategi_izen_SMS[이름크기 + 1] = 0;
        int EMAITZA = erabiltzaile.idatzi_fitxategi(fitxategi_izen_SMS, Irteera, 출력크기);
        if (EMAITZA < 0) { erabiltzaile.Idatzi("javac: cannot save class: "); 자바도구.수쓰기(EMAITZA); erabiltzaile.idatzi_karaktere_balio(10); return 1; }
        erabiltzaile.Idatzi("Compiled: "); for (int 수 = 0; fitxategi_izen_SMS[수] != 0; 수++) erabiltzaile.idatzi_karaktere_balio(fitxategi_izen_SMS[수]);
        erabiltzaile.Idatzi(" (JVM class version 49)\n"); return 0;
    }
}
