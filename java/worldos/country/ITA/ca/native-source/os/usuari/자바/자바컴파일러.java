// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java font_arbre -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] FONT = new int[16384], Sortida = new int[16384], CODI_VALOR = new int[4096];
    static int[] 토큰종류 = new int[2048], testimoni_càrrec = new int[2048], testimoni_durada = new int[2048];
    static int[] 상수 = new int[4096], 상수위치 = new int[512];
    static int[] 문자 = new int[512], nom_d_arxiu_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int font_canviar_la_mida, testimoni_COMPT, Posició, CODI_canviar_la_mida, 상수크기, 상수수 = 1, 출력크기, caràcter_durada;
    static boolean s_ha_produït_un_error;
    static int Classe_testimoni, 클래스상수, 부모상수, 코드상수;
    static int[] 함수이름 = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] 함수인수이름 = new int[512], 함수인수형 = new int[512];
    static int[] 함수본문 = new int[32], 함수끝 = new int[32], 함수코드 = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], 함수명상수 = new int[32], 함수서술 = new int[32];
    static int[] 함수권한 = new int[32];
    static int 함수수, 현재함수, local_COMPT, 깊이, 식깊이;
    static int[] local_nom = new int[128], local_TIPUS = new int[128], 지역깊이 = new int[128];

    static void error_VALOR(String 이유) {
        if (!s_ha_produït_un_error) {
            usuari.Escriptura("javac error: "); usuari.Escriptura(이유);
            usuari.Escriptura(" at line ");
            int línia = 1, 끝 = Posició < testimoni_COMPT ? testimoni_càrrec[Posició] : font_canviar_la_mida;
            for (int 수 = 0; 수 < 끝; 수++) if (FONT[수] == 10) línia++;
            자바도구.수쓰기(línia); usuari.escriure_caràcter_VALOR(10);
        }
        s_ha_produït_un_error = true;
    }
    static boolean caràcter_VALOR(int VALOR) { return 문자이름규칙.첫글자(VALOR); }
    static boolean dígit_VALOR(int VALOR) { return VALOR >= '0' && VALOR <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= testimoni_COMPT || 나 >= testimoni_COMPT || testimoni_durada[가] != testimoni_durada[나]) return false;
        for (int 수 = 0; 수 < testimoni_durada[가]; 수++) if (FONT[testimoni_càrrec[가] + 수] != FONT[testimoni_càrrec[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALOR(int testimoni_VALOR, String Word_SMS) {
        if (testimoni_VALOR < 0 || testimoni_VALOR >= testimoni_COMPT || testimoni_durada[testimoni_VALOR] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (FONT[testimoni_càrrec[testimoni_VALOR] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Posició < testimoni_COMPT ? 토큰종류[Posició] : 0; }
    static boolean rebre(int VALOR) { if (종류() != VALOR) return false; Posició++; return true; }
    static void requisit_VALOR(int VALOR) { if (!rebre(VALOR)) error_VALOR("unexpected token"); }
    static boolean PREN_Word(String Word_SMS) { if (!Word_VALOR(Posició, Word_SMS)) return false; Posició++; return true; }
    static void 말요구(String Word_SMS) { if (!PREN_Word(Word_SMS)) error_VALOR(Word_SMS); }
    static int identificador_VALOR() {
        int RESULTAT = Posició;
        if (종류() != 256) error_VALOR("identifier required"); else Posició++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Executa_2 = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Executa_2 == testimoni_durada[RESULTAT];
                for (int 칸 = Executa_2; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != FONT[testimoni_càrrec[RESULTAT] + 칸 - Executa_2]) 같음 = false;
                if (같음) error_VALOR("reserved word cannot be an identifier");
                Executa_2 = 수 + 1;
            }
        }
        return RESULTAT;
    }
    static void tallar_VALOR() {
        int 수 = 0;
        while (수 < font_canviar_la_mida && !s_ha_produït_un_error) {
            int VALOR = FONT[수], Executa_2 = 수, 종류 = VALOR;
            if (VALOR == 32 || VALOR == 9 || VALOR == 10 || VALOR == 13) { 수++; continue; }
            if (VALOR == '/' && 수 + 1 < font_canviar_la_mida && FONT[수 + 1] == '/') {
                while (수 < font_canviar_la_mida && FONT[수] != 10) 수++;
                continue;
            }
            if (VALOR == '/' && 수 + 1 < font_canviar_la_mida && FONT[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < font_canviar_la_mida && !(FONT[수] == '*' && FONT[수 + 1] == '/')) 수++;
                if (수 + 1 >= font_canviar_la_mida) { error_VALOR("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (caràcter_VALOR(VALOR)) { 종류 = 256; while (수 < font_canviar_la_mida && 문자이름규칙.이어진글자(FONT[수])) 수++; }
            else if (dígit_VALOR(VALOR)) { 종류 = 257; while (수 < font_canviar_la_mida && dígit_VALOR(FONT[수])) 수++; }
            else if (VALOR == '"' || VALOR == '\'') {
                종류 = VALOR == '"' ? 258 : 259; 수++;
                while (수 < font_canviar_la_mida && FONT[수] != VALOR && FONT[수] != 10 && FONT[수] != 13) {
                    if (FONT[수] == '\\') 수++;
                    수++;
                }
                if (수 >= font_canviar_la_mida || FONT[수] != VALOR) { error_VALOR("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < font_canviar_la_mida) {
                    int Següent_element = FONT[수];
                    if (VALOR == '=' && Següent_element == '=') 종류 = 300;
                    if (VALOR == '!' && Següent_element == '=') 종류 = 301;
                    if (VALOR == '<' && Següent_element == '=') 종류 = 302;
                    if (VALOR == '>' && Següent_element == '=') 종류 = 303;
                    if (VALOR == '&' && Següent_element == '&') 종류 = 304;
                    if (VALOR == '|' && Següent_element == '|') 종류 = 305;
                    if (VALOR == '+' && Següent_element == '+') 종류 = 306;
                    if (VALOR == '-' && Següent_element == '-') 종류 = 307;
                    if (VALOR == '+' && Següent_element == '=') 종류 = 308;
                    if (VALOR == '-' && Següent_element == '=') 종류 = 309;
                    if (VALOR == '*' && Següent_element == '=') 종류 = 310;
                    if (VALOR == '/' && Següent_element == '=') 종류 = 311;
                    if (VALOR == '%' && Següent_element == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (testimoni_COMPT == 토큰종류.length - 1) { error_VALOR("too many tokens (2047 maximum)"); break; }
            토큰종류[testimoni_COMPT] = 종류; testimoni_càrrec[testimoni_COMPT] = Executa_2; testimoni_durada[testimoni_COMPT++] = 수 - Executa_2;
        }
    }
    static void 상바(int VALOR) {
        if (상수크기 == 상수.length) { error_VALOR("constant pool too large"); return; }
        상수[상수크기++] = VALOR & 255;
    }
    static void 상짧(int VALOR) { 상바(VALOR >> 8); 상바(VALOR); }
    static int 상등록(int Executa_2) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int frontal_VALOR = 상수위치[수], durada_VALOR = (수 + 1 < 상수수 ? 상수위치[수 + 1] : Executa_2) - frontal_VALOR;
            if (durada_VALOR != 상수크기 - Executa_2) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < durada_VALOR; 칸++) if (상수[frontal_VALOR + 칸] != 상수[Executa_2 + 칸]) 같음 = false;
            if (같음) { 상수크기 = Executa_2; return 수; }
        }
        if (상수수 == 상수위치.length) { error_VALOR("too many constants"); return 0; }
        상수위치[상수수] = Executa_2;
        return 상수수++;
    }
    static void Annexa_SMS(int VALOR) {
        if (caràcter_durada == 문자.length) { error_VALOR("text too long"); return; }
        문자[caràcter_durada++] = VALOR;
    }
    static void Annexa_Word(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) Annexa_SMS(Word_SMS.charAt(수)); }
    static int 문자상수() {
        int Executa_2 = 상수크기; 상바(1); 상짧(0);
        for (int 수 = 0; 수 < caràcter_durada; 수++) {
            int VALOR = 문자[수];
            if (VALOR > 0 && VALOR < 128) 상바(VALOR);
            else if (VALOR < 2048) { 상바(192 | VALOR >> 6); 상바(128 | VALOR & 63); }
            else { 상바(224 | VALOR >> 12); 상바(128 | VALOR >> 6 & 63); 상바(128 | VALOR & 63); }
        }
        if (s_ha_produït_un_error) return 0;
        int durada_VALOR = 상수크기 - Executa_2 - 3;
        상수[Executa_2 + 1] = durada_VALOR >> 8; 상수[Executa_2 + 2] = durada_VALOR & 255;
        return 상등록(Executa_2);
    }
    static int 말상수(String Word_SMS) { caràcter_durada = 0; Annexa_Word(Word_SMS); return 문자상수(); }
    static int 토큰상수(int testimoni_VALOR) {
        caràcter_durada = 0;
        for (int 수 = 0; 수 < testimoni_durada[testimoni_VALOR]; 수++) Annexa_SMS(FONT[testimoni_càrrec[testimoni_VALOR] + 수]);
        return 문자상수();
    }
    static int Referència(int 종류, int 가, int 나) {
        int Executa_2 = 상수크기; 상바(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return 상등록(Executa_2);
    }
    static int extern_Referència(int 종류, String propietari_VALOR, String Nom, String 서술) {
        int propietari_identificador = Referència(7, 말상수(propietari_VALOR), 0);
        int nom_COMPT = 말상수(Nom), format_COMPT = 말상수(서술);
        return Referència(종류, propietari_identificador, Referència(12, nom_COMPT, format_COMPT));
    }
    static void 내보내기(int VALOR) {
        if (CODI_canviar_la_mida == CODI_VALOR.length) { error_VALOR("bytecode too large"); return; }
        CODI_VALOR[CODI_canviar_la_mida++] = VALOR & 255;
    }
    static void Ordre(int VALOR, int 인수) { 내보내기(VALOR); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALOR) {
        if (VALOR >= -1 && VALOR <= 5) { 내보내기(VALOR + 3); return; }
        int Executa_2 = 상수크기; 상바(3); 상짧(VALOR >>> 16); 상짧(VALOR);
        Ordre(19, 상등록(Executa_2));
    }
    static int branca(int Ordre) { int RESULTAT = CODI_canviar_la_mida; Ordre(Ordre, 0); return RESULTAT; }
    static void enllaç_VALOR(int branca, int objectiu_objecte) {
        if (s_ha_produït_un_error) return;
        int 거리 = objectiu_objecte - branca;
        if (거리 < -32768 || 거리 > 32767 || branca < 0 || branca + 2 >= CODI_canviar_la_mida) { error_VALOR("invalid branch"); return; }
        CODI_VALOR[branca + 1] = 거리 >> 8 & 255; CODI_VALOR[branca + 2] = 거리 & 255;
    }
    static void Comparació_VALOR(int Ordre) {
        int CERT_VALOR = branca(Ordre); 내보내기(3); int 끝 = branca(167);
        enllaç_VALOR(CERT_VALOR, CODI_canviar_la_mida); 내보내기(4); enllaç_VALOR(끝, CODI_canviar_la_mida);
    }
    static int format_VALOR() {
        if (PREN_Word("void")) return 0;
        if (PREN_Word("int")) return 1;
        if (PREN_Word("boolean")) return 2;
        if (PREN_Word("char")) return 5;
        if (PREN_Word("FileInputStream")) return 6;
        if (PREN_Word("FileOutputStream")) return 7;
        if (PREN_Word("String")) { if (rebre('[')) { requisit_VALOR(']'); return 4; } return 3; }
        error_VALOR("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void afegir_format(int TIPUS_VALOR) {
        if (TIPUS_VALOR == 0) Annexa_SMS('V');
        if (TIPUS_VALOR == 1) Annexa_SMS('I');
        if (TIPUS_VALOR == 2) Annexa_SMS('Z');
        if (TIPUS_VALOR == 3) Annexa_Word("Ljava/lang/String;");
        if (TIPUS_VALOR == 4) Annexa_Word("[Ljava/lang/String;");
        if (TIPUS_VALOR == 5) Annexa_SMS('C');
        if (TIPUS_VALOR == 6) Annexa_Word("Ljava/io/FileInputStream;");
        if (TIPUS_VALOR == 7) Annexa_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws declaració. excepció Procés_VALOR_introducció 본문은 allotjar javac를 사용한다.
    static void tancar_excepció_nom() {
        boolean 한국어묶음 = PREN_Word("Català");
        if (한국어묶음) { requisit_VALOR('.'); 말요구("propi"); requisit_VALOR('.'); }
        if (!한국어묶음 && (PREN_Word("Exception") || PREN_Word("IOException"))) return;
        if (PREN_Word("excepció") || PREN_Word("실행예외") || PREN_Word("E_S_excepció") || PREN_Word("Espera_TIMEOUT_excepció") || PREN_Word("ADREÇA_Cerca_excepció") || PREN_Word("파일없음예외") || PREN_Word("통신예외") || PREN_Word("invàlid_arg_excepció") || PREN_Word("숫자형식예외") || PREN_Word("범위예외") || PREN_Word("배열범위예외") || PREN_Word("문자열범위예외") || PREN_Word("NUL_Referència_excepció") || PREN_Word("산술예외") || PREN_Word("Estat_excepció") || PREN_Word("TIPUS_conversió_excepció") || PREN_Word("음수배열크기예외") || PREN_Word("MATRIU_Store_error") || PREN_Word("fil_Estat_excepció") || PREN_Word("대기중단예외")) return;
        error_VALOR("unsupported throws type");
    }
    static void tancar_declaració() {
        while (PREN_Word("import")) {
            if (Word_VALOR(Posició, "Català")) tancar_excepció_nom();
            else {
                말요구("java"); requisit_VALOR('.'); 말요구("io"); requisit_VALOR('.');
                if (!(PREN_Word("FileInputStream") || PREN_Word("FileOutputStream") || PREN_Word("IOException"))) error_VALOR("unsupported import");
            }
            requisit_VALOR(';');
        }
        PREN_Word("public"); PREN_Word("final"); 말요구("class"); Classe_testimoni = identificador_VALOR();
        클래스상수 = Referència(7, 토큰상수(Classe_testimoni), 0);
        부모상수 = Referència(7, 말상수("java/lang/Object"), 0); 코드상수 = 말상수("Code"); requisit_VALOR('{');
        while (!s_ha_produït_un_error && 종류() != '}') {
            if (함수수 == 32) { error_VALOR("too many methods"); break; }
            int accés_introducció = PREN_Word("public") ? 1 : PREN_Word("private") ? 2 : 0; 말요구("static");
            int FUNCIÓ_VALOR = 함수수++;
            함수권한[FUNCIÓ_VALOR] = accés_introducció | 8;
            함수반환[FUNCIÓ_VALOR] = format_VALOR(); 함수이름[FUNCIÓ_VALOR] = identificador_VALOR(); requisit_VALOR('(');
            for (int frontal_VALOR = 0; frontal_VALOR < FUNCIÓ_VALOR; frontal_VALOR++) if (이름같음(함수이름[frontal_VALOR], 함수이름[FUNCIÓ_VALOR])) error_VALOR("duplicate method (overloading unsupported)");
            while (!s_ha_produït_un_error && 종류() != ')') {
                int 수 = 함수인수수[FUNCIÓ_VALOR];
                if (수 == 16) { error_VALOR("too many parameters"); break; }
                int TIPUS_VALOR = format_VALOR(); if (TIPUS_VALOR == 0) error_VALOR("void parameter");
                함수인수형[FUNCIÓ_VALOR * 16 + 수] = TIPUS_VALOR; 함수인수이름[FUNCIÓ_VALOR * 16 + 수] = identificador_VALOR();
                함수인수수[FUNCIÓ_VALOR]++;
                if (!rebre(',')) break;
            }
            requisit_VALOR(')');
            if (PREN_Word("throws")) {
                do { tancar_excepció_nom(); } while (!s_ha_produït_un_error && rebre(','));
            }
            함수본문[FUNCIÓ_VALOR] = Posició; requisit_VALOR('{');
            int imbricació_VALOR = 1;
            while (Posició < testimoni_COMPT && imbricació_VALOR > 0) {
                if (종류() == '{') imbricació_VALOR++;
                if (종류() == '}') imbricació_VALOR--;
                Posició++;
            }
            if (imbricació_VALOR != 0) error_VALOR("unclosed method body");
            함수끝[FUNCIÓ_VALOR] = Posició;
            함수명상수[FUNCIÓ_VALOR] = 토큰상수(함수이름[FUNCIÓ_VALOR]);
            caràcter_durada = 0; Annexa_SMS('(');
            for (int 수 = 0; 수 < 함수인수수[FUNCIÓ_VALOR]; 수++) afegir_format(함수인수형[FUNCIÓ_VALOR * 16 + 수]);
            Annexa_SMS(')'); afegir_format(함수반환[FUNCIÓ_VALOR]); 함수서술[FUNCIÓ_VALOR] = 문자상수();
        }
        requisit_VALOR('}'); if (Posició != testimoni_COMPT) error_VALOR("extra input after class");
    }
    static int BUSCA_local(int Nom) {
        for (int 수 = local_COMPT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(local_nom[수], Nom)) return 수;
        error_VALOR("unknown variable"); return 0;
    }
    static int afegir_local(int Nom, int TIPUS_VALOR) {
        for (int 수 = 0; 수 < local_COMPT; 수++) if (지역깊이[수] >= 0 && 이름같음(local_nom[수], Nom)) error_VALOR("duplicate local variable");
        if (local_COMPT == 128) { error_VALOR("too many locals"); return 0; }
        local_nom[local_COMPT] = Nom; local_TIPUS[local_COMPT] = TIPUS_VALOR; 지역깊이[local_COMPT] = 깊이;
        return local_COMPT++;
    }
    static boolean 정수형(int TIPUS_VALOR) { return TIPUS_VALOR == 1 || TIPUS_VALOR == 5; }
    static void tancar_local(int 수) { 내보내기(local_TIPUS[수] <= 2 || local_TIPUS[수] == 5 ? 21 : 25); 내보내기(수); }
    static void escriure_local(int 수) { 내보내기(local_TIPUS[수] <= 2 || local_TIPUS[수] == 5 ? 54 : 58); 내보내기(수); }
    static void verificar_TIPUS(int real_dades, int 기대) { if (real_dades != 기대 && !(real_dades == 5 && 기대 == 1)) error_VALOR("type mismatch"); }
    static void tancar_caràcter_VALOR(int testimoni_VALOR) {
        caràcter_durada = 0; int Executa_2 = testimoni_càrrec[testimoni_VALOR] + 1, 끝 = testimoni_càrrec[testimoni_VALOR] + testimoni_durada[testimoni_VALOR] - 1;
        while (Executa_2 < 끝 && !s_ha_produït_un_error) {
            int VALOR = FONT[Executa_2++];
            if (VALOR == '\\') {
                if (Executa_2 == 끝) { error_VALOR("invalid escape"); break; }
                VALOR = FONT[Executa_2++];
                if (VALOR == 'n') VALOR = 10;
                else if (VALOR == 'r') VALOR = 13;
                else if (VALOR == 't') VALOR = 9;
                else if (VALOR == 'b') VALOR = 8;
                else if (VALOR == 'f') VALOR = 12;
                else if (VALOR != '\\' && VALOR != '"' && VALOR != '\'') error_VALOR("unsupported escape");
            }
            Annexa_SMS(VALOR);
        }
    }
    static int 정수읽기(int testimoni_VALOR, boolean 음수) {
        if (testimoni_durada[testimoni_VALOR] > 1 && FONT[testimoni_càrrec[testimoni_VALOR]] == '0') error_VALOR("octal literals unsupported");
        int VALOR = 0;
        for (int 수 = 0; 수 < testimoni_durada[testimoni_VALOR]; 수++) {
            int dígit_element = FONT[testimoni_càrrec[testimoni_VALOR] + 수] - '0';
            if (VALOR < -214748364 || VALOR == -214748364 && dígit_element > (음수 ? 8 : 7)) error_VALOR("integer literal out of range");
            VALOR = VALOR * 10 - dígit_element;
        }
        return 음수 ? VALOR : -VALOR;
    }
    static int 기본식() {
        if (PREN_Word("new")) {
            int TIPUS_VALOR = format_VALOR();
            if (TIPUS_VALOR != 6 && TIPUS_VALOR != 7) { error_VALOR("only file streams supported by new in source"); return 0; }
            String propietari_VALOR = TIPUS_VALOR == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Ordre(187, Referència(7, 말상수(propietari_VALOR), 0)); 내보내기(89);
            requisit_VALOR('('); verificar_TIPUS(expressió_VALOR(), 3); boolean 이어 = false;
            if (rebre(',')) { if (TIPUS_VALOR != 7) error_VALOR("input stream constructor arguments"); verificar_TIPUS(expressió_VALOR(), 2); 이어 = true; }
            requisit_VALOR(')');
            Ordre(183, extern_Referència(10, propietari_VALOR, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TIPUS_VALOR;
        }
        if (rebre('(')) { int TIPUS_VALOR = expressió_VALOR(); requisit_VALOR(')'); return TIPUS_VALOR; }
        if (종류() == 257) { 수상수(정수읽기(Posició++, false)); return 1; }
        if (종류() == 258) { tancar_caràcter_VALOR(Posició++); Ordre(19, Referència(8, 문자상수(), 0)); return 3; }
        if (종류() == 259) { tancar_caràcter_VALOR(Posició++); if (caràcter_durada != 1) error_VALOR("character literal length"); 수상수(문자[0]); return 5; }
        if (PREN_Word("true")) { 내보내기(4); return 2; }
        if (PREN_Word("false")) { 내보내기(3); return 2; }
        if (PREN_Word("Català")) {
            requisit_VALOR('.'); 말요구("propi"); requisit_VALOR('.');
            String propietari_VALOR = "", 메서드 = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, RESULTAT = 0;
            if (PREN_Word("Sortida")) {
                propietari_VALOR = "Català/propi/Sortida"; requisit_VALOR('.');
                if (PREN_Word("escriure_línia")) { 메서드 = "escriure_línia"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (PREN_Word("Escriptura")) { 메서드 = "Escriptura"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (PREN_Word("수쓰기")) { 메서드 = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else error_VALOR("unknown Korean output method");
            } else if (PREN_Word("문자")) {
                propietari_VALOR = "Català/propi/문자"; requisit_VALOR('.'); 가 = 3;
                if (PREN_Word("durada_VALOR")) { 메서드 = "durada_VALOR"; 서술 = "(Ljava/lang/String;)I"; RESULTAT = 1; }
                else if (PREN_Word("codi_de_caràcter_COMPT")) { 메서드 = "codi_de_caràcter_COMPT"; 서술 = "(Ljava/lang/String;)I"; RESULTAT = 1; }
                else if (PREN_Word("정수읽기")) { 메서드 = "정수읽기"; 서술 = "(Ljava/lang/String;)I"; RESULTAT = 1; }
                else if (PREN_Word("정수쓰기")) { 메서드 = "정수쓰기"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; RESULTAT = 3; }
                else if (PREN_Word("같음")) { 메서드 = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; RESULTAT = 2; }
                else if (PREN_Word("enganxar_SMS")) { 메서드 = "enganxar_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; RESULTAT = 3; }
                else if (PREN_Word("tallar_VALOR")) { 메서드 = "tallar_VALOR"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; RESULTAT = 3; }
                else error_VALOR("unknown Korean text method");
            } else if (PREN_Word("Fitxer")) {
                propietari_VALOR = "Català/propi/Fitxer"; requisit_VALOR('.'); 가 = 3;
                if (PREN_Word("Lectura")) { 메서드 = "Lectura"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; RESULTAT = 3; }
                else if (PREN_Word("Escriptura")) { 메서드 = "Escriptura"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else error_VALOR("unknown Korean file method");
            } else if (PREN_Word("화면")) {
                propietari_VALOR = "Català/propi/화면"; requisit_VALOR('.');
                if (PREN_Word("너비")) { 메서드 = "너비"; 서술 = "()I"; RESULTAT = 1; }
                else if (PREN_Word("높이")) { 메서드 = "높이"; 서술 = "()I"; RESULTAT = 1; }
                else if (PREN_Word("사각형")) { 메서드 = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (PREN_Word("esborrar_introducció")) { 메서드 = "esborrar_introducció"; 서술 = "(I)V"; 가 = 1; }
                else if (PREN_Word("기다리기")) { 메서드 = "기다리기"; 서술 = "()V"; }
                else error_VALOR("unknown Korean framebuffer method");
            } else error_VALOR("unsupported Korean library class");
            requisit_VALOR('('); if (가 != 0) verificar_TIPUS(expressió_VALOR(), 가);
            if (나 != 0) { requisit_VALOR(','); verificar_TIPUS(expressió_VALOR(), 나); }
            if (다 != 0) { requisit_VALOR(','); verificar_TIPUS(expressió_VALOR(), 다); }
            if (라 != 0) { requisit_VALOR(','); verificar_TIPUS(expressió_VALOR(), 라); }
            if (마 != 0) { requisit_VALOR(','); verificar_TIPUS(expressió_VALOR(), 마); }
            requisit_VALOR(')'); Ordre(184, extern_Referència(10, propietari_VALOR, 메서드, 서술)); return RESULTAT;
        }
        if (PREN_Word("Integer")) {
            requisit_VALOR('.'); 말요구("parseInt"); requisit_VALOR('('); verificar_TIPUS(expressió_VALOR(), 3); requisit_VALOR(')');
            Ordre(184, extern_Referència(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nom = identificador_VALOR();
        if (rebre('(')) {
            int FUNCIÓ_VALOR = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Nom, 함수이름[수])) FUNCIÓ_VALOR = 수;
            if (FUNCIÓ_VALOR < 0) { error_VALOR("unknown static method"); return 0; }
            int 수 = 0;
            while (!s_ha_produït_un_error && 종류() != ')') {
                if (수 >= 함수인수수[FUNCIÓ_VALOR]) { error_VALOR("too many arguments"); break; }
                verificar_TIPUS(expressió_VALOR(), 함수인수형[FUNCIÓ_VALOR * 16 + 수++]); if (!rebre(',')) break;
            }
            requisit_VALOR(')'); if (수 != 함수인수수[FUNCIÓ_VALOR]) error_VALOR("argument count mismatch");
            Ordre(184, Referència(10, 클래스상수, Referència(12, 함수명상수[FUNCIÓ_VALOR], 함수서술[FUNCIÓ_VALOR])));
            return 함수반환[FUNCIÓ_VALOR];
        }
        int local_Àmbit = BUSCA_local(Nom), TIPUS_VALOR = local_TIPUS[local_Àmbit]; tancar_local(local_Àmbit);
        while (!s_ha_produït_un_error) {
            if (rebre('[')) { verificar_TIPUS(TIPUS_VALOR, 4); verificar_TIPUS(expressió_VALOR(), 1); requisit_VALOR(']'); 내보내기(50); TIPUS_VALOR = 3; }
            else if (rebre('.')) {
                if (TIPUS_VALOR == 6 || TIPUS_VALOR == 7) {
                    String propietari_VALOR = TIPUS_VALOR == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (PREN_Word("close")) { requisit_VALOR('('); requisit_VALOR(')'); Ordre(182, extern_Referència(10, propietari_VALOR, "close", "()V")); TIPUS_VALOR = 0; }
                    else if (TIPUS_VALOR == 6 && PREN_Word("read")) { requisit_VALOR('('); requisit_VALOR(')'); Ordre(182, extern_Referència(10, propietari_VALOR, "read", "()I")); TIPUS_VALOR = 1; }
                    else if (TIPUS_VALOR == 7 && PREN_Word("write")) { requisit_VALOR('('); verificar_TIPUS(expressió_VALOR(), 1); requisit_VALOR(')'); Ordre(182, extern_Referència(10, propietari_VALOR, "write", "(I)V")); TIPUS_VALOR = 0; }
                    else { error_VALOR("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TIPUS_VALOR == 4) { 내보내기(190); TIPUS_VALOR = 1; }
                else { verificar_TIPUS(TIPUS_VALOR, 3); requisit_VALOR('('); requisit_VALOR(')'); Ordre(182, extern_Referència(10, "java/lang/String", "length", "()I")); TIPUS_VALOR = 1; }
            } else break;
        }
        return TIPUS_VALOR;
    }
    static int 단항() {
        if (++식깊이 > 64) { error_VALOR("expression nesting too deep"); 식깊이--; return 0; }
        int TIPUS_VALOR;
        if (rebre('!')) { verificar_TIPUS(단항(), 2); Comparació_VALOR(153); TIPUS_VALOR = 2; }
        else if (rebre('-')) {
            if (종류() == 257) 수상수(정수읽기(Posició++, true));
            else { verificar_TIPUS(단항(), 1); 내보내기(116); }
            TIPUS_VALOR = 1;
        } else if (rebre('+')) { verificar_TIPUS(단항(), 1); TIPUS_VALOR = 1; }
        else TIPUS_VALOR = 기본식();
        식깊이--; return TIPUS_VALOR;
    }
    static int 곱식() {
        int TIPUS_VALOR = 단항();
        while (!s_ha_produït_un_error && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int codificació_VALOR = 종류(); Posició++; verificar_TIPUS(TIPUS_VALOR, 1); verificar_TIPUS(단항(), 1);
            내보내기(codificació_VALOR == '*' ? 104 : codificació_VALOR == '/' ? 108 : 112); TIPUS_VALOR = 1;
        }
        return TIPUS_VALOR;
    }
    static int 합식() {
        int TIPUS_VALOR = 곱식();
        while (!s_ha_produït_un_error && (종류() == '+' || 종류() == '-')) {
            int codificació_VALOR = 종류(); Posició++; int 경계 = CODI_canviar_la_mida, ENRERE_VALOR_TIPUS = 곱식();
            if (codificació_VALOR == '+' && (TIPUS_VALOR == 3 || ENRERE_VALOR_TIPUS == 3)) { 결합(경계, TIPUS_VALOR, ENRERE_VALOR_TIPUS); TIPUS_VALOR = 3; }
            else { verificar_TIPUS(TIPUS_VALOR, 1); verificar_TIPUS(ENRERE_VALOR_TIPUS, 1); 내보내기(codificació_VALOR == '+' ? 96 : 100); TIPUS_VALOR = 1; }
        }
        return TIPUS_VALOR;
    }
    static int 붙임참조(int TIPUS_VALOR) {
        if (TIPUS_VALOR != 1 && TIPUS_VALOR != 2 && TIPUS_VALOR != 3 && TIPUS_VALOR != 5) error_VALOR("unsupported concatenation type");
        return extern_Referència(10, "java/lang/StringBuilder", "append", TIPUS_VALOR == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TIPUS_VALOR == 2 ? "(Z)Ljava/lang/StringBuilder;" : TIPUS_VALOR == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int frontal_VALOR_TIPUS, int ENRERE_VALOR_TIPUS) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 DRETA CODI_VALOR 앞에 generar 코드를 삽입한다.
        // DRETA expressió_VALOR 내부의 homòleg_VALOR branca 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODI_canviar_la_mida;
        Ordre(187, Referència(7, 말상수("java/lang/StringBuilder"), 0)); 내보내기(89);
        Ordre(183, extern_Referència(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Ordre(182, 붙임참조(frontal_VALOR_TIPUS));
        if (s_ha_produït_un_error) return;
        int durada_VALOR = CODI_canviar_la_mida - 끝;
        for (int 수 = 0; 수 < durada_VALOR; 수++) 삽입코드[수] = CODI_VALOR[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODI_VALOR[수 + durada_VALOR] = CODI_VALOR[수];
        for (int 수 = 0; 수 < durada_VALOR; 수++) CODI_VALOR[경계 + 수] = 삽입코드[수];
        Ordre(182, 붙임참조(ENRERE_VALOR_TIPUS)); Ordre(182, extern_Referència(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Comparació_expressió() {
        int TIPUS_VALOR = 합식();
        while (!s_ha_produït_un_error && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int codificació_VALOR = 종류(); Posició++; verificar_TIPUS(TIPUS_VALOR, 1); verificar_TIPUS(합식(), 1);
            Comparació_VALOR(codificació_VALOR == '<' ? 161 : codificació_VALOR == '>' ? 163 : codificació_VALOR == 302 ? 164 : 162); TIPUS_VALOR = 2;
        }
        return TIPUS_VALOR;
    }
    static int 동등식() {
        int TIPUS_VALOR = Comparació_expressió();
        while (!s_ha_produït_un_error && (종류() == 300 || 종류() == 301)) {
            int codificació_VALOR = 종류(); Posició++; int ENRERE_VALOR_TIPUS = Comparació_expressió();
            if (TIPUS_VALOR == 0 || ENRERE_VALOR_TIPUS == 0) error_VALOR("void expression");
            if (!(정수형(TIPUS_VALOR) && 정수형(ENRERE_VALOR_TIPUS))) verificar_TIPUS(ENRERE_VALOR_TIPUS, TIPUS_VALOR);
            Comparació_VALOR((TIPUS_VALOR <= 2 || TIPUS_VALOR == 5 ? 159 : 165) + (codificació_VALOR == 301 ? 1 : 0)); TIPUS_VALOR = 2;
        }
        return TIPUS_VALOR;
    }
    static int 논리곱() {
        int TIPUS_VALOR = 동등식();
        while (!s_ha_produït_un_error && rebre(304)) {
            verificar_TIPUS(TIPUS_VALOR, 2); int 가 = branca(153); verificar_TIPUS(동등식(), 2); int 나 = branca(153);
            내보내기(4); int 끝 = branca(167); enllaç_VALOR(가, CODI_canviar_la_mida); enllaç_VALOR(나, CODI_canviar_la_mida); 내보내기(3); enllaç_VALOR(끝, CODI_canviar_la_mida); TIPUS_VALOR = 2;
        }
        return TIPUS_VALOR;
    }
    static int expressió_VALOR() {
        int TIPUS_VALOR = 논리곱();
        while (!s_ha_produït_un_error && rebre(305)) {
            verificar_TIPUS(TIPUS_VALOR, 2); int 가 = branca(154); verificar_TIPUS(논리곱(), 2); int 나 = branca(154);
            내보내기(3); int 끝 = branca(167); enllaç_VALOR(가, CODI_canviar_la_mida); enllaç_VALOR(나, CODI_canviar_la_mida); 내보내기(4); enllaç_VALOR(끝, CODI_canviar_la_mida); TIPUS_VALOR = 2;
        }
        return TIPUS_VALOR;
    }
    static void tasca_VALOR(boolean Permet_declaració) {
        if (Word_VALOR(Posició, "int") || Word_VALOR(Posició, "boolean") || Word_VALOR(Posició, "String") || Word_VALOR(Posició, "char")
            || Word_VALOR(Posició, "FileInputStream") || Word_VALOR(Posició, "FileOutputStream")) {
            if (!Permet_declaració) error_VALOR("declaration not allowed here");
            int TIPUS_VALOR = format_VALOR(), Nom = identificador_VALOR(); requisit_VALOR('='); verificar_TIPUS(expressió_VALOR(), TIPUS_VALOR);
            escriure_local(afegir_local(Nom, TIPUS_VALOR)); return;
        }
        int Nom = identificador_VALOR(), local_Àmbit = BUSCA_local(Nom);
        if (rebre('=')) { verificar_TIPUS(expressió_VALOR(), local_TIPUS[local_Àmbit]); escriure_local(local_Àmbit); }
        else if (종류() >= 308 && 종류() <= 312) {
            int codificació_VALOR = 종류(); Posició++; tancar_local(local_Àmbit); int 경계 = CODI_canviar_la_mida, ENRERE_VALOR_TIPUS = expressió_VALOR();
            if (codificació_VALOR == 308 && local_TIPUS[local_Àmbit] == 3) 결합(경계, 3, ENRERE_VALOR_TIPUS);
            else {
                verificar_TIPUS(local_TIPUS[local_Àmbit], 1); verificar_TIPUS(ENRERE_VALOR_TIPUS, 1);
                내보내기(codificació_VALOR == 308 ? 96 : codificació_VALOR == 309 ? 100 : codificació_VALOR == 310 ? 104 : codificació_VALOR == 311 ? 108 : 112);
                if (local_TIPUS[local_Àmbit] == 5) 내보내기(146);
            }
            escriure_local(local_Àmbit);
        }
        else if (종류() == 306 || 종류() == 307) {
            verificar_TIPUS(local_TIPUS[local_Àmbit], 1); 내보내기(132); 내보내기(local_Àmbit); 내보내기(종류() == 306 ? 1 : 255); Posició++;
            if (local_TIPUS[local_Àmbit] == 5) { tancar_local(local_Àmbit); 내보내기(146); escriure_local(local_Àmbit); }
        } else error_VALOR("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); requisit_VALOR('.'); 말요구("out"); requisit_VALOR('.');
        boolean 줄바꿈 = PREN_Word("println"); if (!줄바꿈) 말요구("print"); requisit_VALOR('(');
        Ordre(178, extern_Referència(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int TIPUS_VALOR = 빈인수 ? 0 : expressió_VALOR(); requisit_VALOR(')'); requisit_VALOR(';');
        String 서술 = TIPUS_VALOR == 0 ? "()V" : TIPUS_VALOR == 1 ? "(I)V" : TIPUS_VALOR == 2 ? "(Z)V" : TIPUS_VALOR == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TIPUS_VALOR == 4 || TIPUS_VALOR >= 6 || TIPUS_VALOR == 0 && (!줄바꿈 || !빈인수)) error_VALOR("unsupported print argument");
        Ordre(182, extern_Referència(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean instrucció_VALOR() {
        if (s_ha_produït_un_error) return false;
        if (깊이 > 32) { error_VALOR("statement nesting too deep"); return false; }
        if (rebre('{')) {
            깊이++; boolean tornar_les_tasques_mesura = false;
            while (!s_ha_produït_un_error && 종류() != '}') { if (tornar_les_tasques_mesura) error_VALOR("unreachable statement"); tornar_les_tasques_mesura = instrucció_VALOR(); }
            requisit_VALOR('}'); for (int 수 = 0; 수 < local_COMPT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return tornar_les_tasques_mesura;
        }
        if (rebre(';')) return false;
        if (PREN_Word("return")) {
            int TIPUS_VALOR = 종류() == ';' ? 0 : expressió_VALOR(); verificar_TIPUS(TIPUS_VALOR, 함수반환[현재함수]); requisit_VALOR(';');
            내보내기(TIPUS_VALOR == 0 ? 177 : TIPUS_VALOR <= 2 || TIPUS_VALOR == 5 ? 172 : 176); return true;
        }
        if (PREN_Word("if")) {
            requisit_VALOR('('); verificar_TIPUS(expressió_VALOR(), 2); requisit_VALOR(')'); int FALS_VALOR = branca(153);
            깊이++; boolean 가 = control_instrucció(); 깊이--;
            if (PREN_Word("else")) { int 끝 = branca(167); enllaç_VALOR(FALS_VALOR, CODI_canviar_la_mida); 깊이++; boolean 나 = control_instrucció(); 깊이--; enllaç_VALOR(끝, CODI_canviar_la_mida); return 가 && 나; }
            enllaç_VALOR(FALS_VALOR, CODI_canviar_la_mida); return false;
        }
        if (PREN_Word("while")) {
            int Executa_2 = CODI_canviar_la_mida; requisit_VALOR('('); verificar_TIPUS(expressió_VALOR(), 2); requisit_VALOR(')'); int 끝 = branca(153);
            깊이++; control_instrucció(); 깊이--; enllaç_VALOR(branca(167), Executa_2); enllaç_VALOR(끝, CODI_canviar_la_mida); return false;
        }
        if (PREN_Word("for")) {
            깊이++; requisit_VALOR('('); if (종류() != ';') tasca_VALOR(true); requisit_VALOR(';');
            int condició = CODI_canviar_la_mida; if (종류() == ';') 내보내기(4); else verificar_TIPUS(expressió_VALOR(), 2); requisit_VALOR(';');
            int 끝 = branca(153), text_del_cos = branca(167), actualitzar = CODI_canviar_la_mida;
            if (종류() != ')') tasca_VALOR(false); requisit_VALOR(')'); enllaç_VALOR(branca(167), condició); enllaç_VALOR(text_del_cos, CODI_canviar_la_mida);
            control_instrucció(); enllaç_VALOR(branca(167), actualitzar); enllaç_VALOR(끝, CODI_canviar_la_mida);
            for (int 수 = 0; 수 < local_COMPT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALOR(Posició, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Posició + 1 < testimoni_COMPT && (토큰종류[Posició + 1] == '(' || 토큰종류[Posició + 1] == '.')) {
            int TIPUS_VALOR = expressió_VALOR(); if (TIPUS_VALOR != 0) 내보내기(87); requisit_VALOR(';'); return false;
        }
        tasca_VALOR(true); requisit_VALOR(';'); return false;
    }
    static boolean control_instrucció() {
        if (Word_VALOR(Posició, "int") || Word_VALOR(Posició, "boolean") || Word_VALOR(Posició, "char") || Word_VALOR(Posició, "String")
            || Word_VALOR(Posició, "FileInputStream") || Word_VALOR(Posició, "FileOutputStream")) error_VALOR("local declaration requires braces");
        return instrucció_VALOR();
    }
    static void 출바(int VALOR) { if (출력크기 == Sortida.length) error_VALOR("class file too large"); else Sortida[출력크기++] = VALOR & 255; }
    static void 출짧(int VALOR) { 출바(VALOR >> 8); 출바(VALOR); }
    static void 출정(int VALOR) { 출짧(VALOR >>> 16); 출짧(VALOR); }
    static void escriure_Classe() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < 상수크기; 수++) 출바(상수[수]);
        출짧(0x21); 출짧(클래스상수); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(함수권한[수]); 출짧(함수명상수[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + 함수길이[수]); 출짧(128); 출짧(함수지역[수]); 출정(함수길이[수]);
            for (int 칸 = 0; 칸 < 함수길이[수]; 칸++) 출바(CODI_VALOR[함수코드[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Executa_2() {
        if (usuari.인수개수() == 1 && 자바도구.같음(usuari.인수(0), "-version")) {
            usuari.Escriptura("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (usuari.인수개수() != 1) { usuari.Escriptura("Usage: javac FILE.java\n"); return 2; }
        int nom_canviar_la_mida = 자바도구.Nom(nom_d_arxiu_SMS, usuari.인수(0));
        if (nom_canviar_la_mida < 6 || nom_canviar_la_mida > 62 || nom_d_arxiu_SMS[nom_canviar_la_mida - 5] != '.' || nom_d_arxiu_SMS[nom_canviar_la_mida - 4] != 'j'
            || nom_d_arxiu_SMS[nom_canviar_la_mida - 3] != 'a' || nom_d_arxiu_SMS[nom_canviar_la_mida - 2] != 'v' || nom_d_arxiu_SMS[nom_canviar_la_mida - 1] != 'a') {
            usuari.Escriptura("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        font_canviar_la_mida = usuari.tancar_arxiu(nom_d_arxiu_SMS, FONT);
        if (font_canviar_la_mida < 0) { usuari.Escriptura("javac: cannot read source: "); 자바도구.수쓰기(font_canviar_la_mida); usuari.escriure_caràcter_VALOR(10); return 1; }
        font_canviar_la_mida = 자바도구.원문해독(FONT, font_canviar_la_mida);
        if (font_canviar_la_mida < 0) { usuari.Escriptura("javac error: invalid UTF-8 source\n"); return 1; }
        tallar_VALOR(); if (!s_ha_produït_un_error) tancar_declaració();
        if (!s_ha_produït_un_error) {
            if (testimoni_durada[Classe_testimoni] != nom_canviar_la_mida - 5) error_VALOR("class name must match file name");
            for (int 수 = 0; 수 < nom_canviar_la_mida - 5; 수++) if (FONT[testimoni_càrrec[Classe_testimoni] + 수] != nom_d_arxiu_SMS[수]) error_VALOR("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !s_ha_produït_un_error; 현재함수++) {
            Posició = 함수본문[현재함수]; 함수코드[현재함수] = CODI_canviar_la_mida; local_COMPT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) afegir_local(함수인수이름[현재함수 * 16 + 수], 함수인수형[현재함수 * 16 + 수]);
            boolean tornar_les_tasques_mesura = instrucció_VALOR();
            if (!tornar_les_tasques_mesura && 함수반환[현재함수] != 0) error_VALOR("missing return");
            // branca 뒤의 합류 지점은 반드시 real_dades 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean 정수 = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(정수 ? 3 : 1); 내보내기(정수 ? 172 : 176); }
            if (Posició != 함수끝[현재함수]) error_VALOR("invalid method body");
            함수지역[현재함수] = local_COMPT; 함수길이[현재함수] = CODI_canviar_la_mida - 함수코드[현재함수];
        }
        if (s_ha_produït_un_error) return 1;
        escriure_Classe(); if (s_ha_produït_un_error) return 1;
        nom_d_arxiu_SMS[nom_canviar_la_mida - 4] = 'c'; nom_d_arxiu_SMS[nom_canviar_la_mida - 3] = 'l'; nom_d_arxiu_SMS[nom_canviar_la_mida - 2] = 'a';
        nom_d_arxiu_SMS[nom_canviar_la_mida - 1] = 's'; nom_d_arxiu_SMS[nom_canviar_la_mida] = 's'; nom_d_arxiu_SMS[nom_canviar_la_mida + 1] = 0;
        int RESULTAT = usuari.escriure_arxiu(nom_d_arxiu_SMS, Sortida, 출력크기);
        if (RESULTAT < 0) { usuari.Escriptura("javac: cannot save class: "); 자바도구.수쓰기(RESULTAT); usuari.escriure_caràcter_VALOR(10); return 1; }
        usuari.Escriptura("Compiled: "); for (int 수 = 0; nom_d_arxiu_SMS[수] != 0; 수++) usuari.escriure_caràcter_VALOR(nom_d_arxiu_SMS[수]);
        usuari.Escriptura(" (JVM class version 49)\n"); return 0;
    }
}
