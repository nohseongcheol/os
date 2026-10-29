// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java fonte_árbore -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] FONTE = new int[16384], Saída = new int[16384], CÓDIGO_VALOR = new int[4096];
    static int[] 토큰종류 = new int[2048], ficha_cargo = new int[2048], ficha_duración = new int[2048];
    static int[] constante_VALOR = new int[4096], constante_DESPRAZAMENTO = new int[512];
    static int[] 문자 = new int[512], Ficheiro_nome_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int 원문크기, ficha_CONTAR, Posición, 코드크기, 상수크기, constante_CONTAR = 1, 출력크기, carácter_duración;
    static boolean ERRO;
    static int Clase_ficha, Clase_constante, 부모상수, CÓDIGO_constante;
    static int[] 함수이름 = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] 함수인수이름 = new int[512], 함수인수형 = new int[512];
    static int[] 함수본문 = new int[32], 함수끝 = new int[32], 함수코드 = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], 함수명상수 = new int[32], 함수서술 = new int[32];
    static int[] 함수권한 = new int[32];
    static int 함수수, 현재함수, local_CONTAR, 깊이, 식깊이;
    static int[] local_nome = new int[128], local_TIPO = new int[128], 지역깊이 = new int[128];

    static void erro_VALOR(String 이유) {
        if (!ERRO) {
            usuario.Escritura("javac error: "); usuario.Escritura(이유);
            usuario.Escritura(" at line ");
            int Liña = 1, 끝 = Posición < ficha_CONTAR ? ficha_cargo[Posición] : 원문크기;
            for (int 수 = 0; 수 < 끝; 수++) if (FONTE[수] == 10) Liña++;
            자바도구.수쓰기(Liña); usuario.escribir_carácter_VALOR(10);
        }
        ERRO = true;
    }
    static boolean carácter_VALOR(int VALOR) { return 문자이름규칙.첫글자(VALOR); }
    static boolean díxito_VALOR(int VALOR) { return VALOR >= '0' && VALOR <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= ficha_CONTAR || 나 >= ficha_CONTAR || ficha_duración[가] != ficha_duración[나]) return false;
        for (int 수 = 0; 수 < ficha_duración[가]; 수++) if (FONTE[ficha_cargo[가] + 수] != FONTE[ficha_cargo[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALOR(int ficha_VALOR, String Word_SMS) {
        if (ficha_VALOR < 0 || ficha_VALOR >= ficha_CONTAR || ficha_duración[ficha_VALOR] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (FONTE[ficha_cargo[ficha_VALOR] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Posición < ficha_CONTAR ? 토큰종류[Posición] : 0; }
    static boolean 받기(int VALOR) { if (종류() != VALOR) return false; Posición++; return true; }
    static void 요구(int VALOR) { if (!받기(VALOR)) erro_VALOR("unexpected token"); }
    static boolean COLLER_Word(String Word_SMS) { if (!Word_VALOR(Posición, Word_SMS)) return false; Posición++; return true; }
    static void 말요구(String Word_SMS) { if (!COLLER_Word(Word_SMS)) erro_VALOR(Word_SMS); }
    static int 식별자() {
        int RESULTANTE = Posición;
        if (종류() != 256) erro_VALOR("identifier required"); else Posición++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Executar_2 = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Executar_2 == ficha_duración[RESULTANTE];
                for (int 칸 = Executar_2; 같음 && 칸 < 수; 칸++) if (예약어.charAt(칸) != FONTE[ficha_cargo[RESULTANTE] + 칸 - Executar_2]) 같음 = false;
                if (같음) erro_VALOR("reserved word cannot be an identifier");
                Executar_2 = 수 + 1;
            }
        }
        return RESULTANTE;
    }
    static void cortar_VALOR() {
        int 수 = 0;
        while (수 < 원문크기 && !ERRO) {
            int VALOR = FONTE[수], Executar_2 = 수, 종류 = VALOR;
            if (VALOR == 32 || VALOR == 9 || VALOR == 10 || VALOR == 13) { 수++; continue; }
            if (VALOR == '/' && 수 + 1 < 원문크기 && FONTE[수 + 1] == '/') {
                while (수 < 원문크기 && FONTE[수] != 10) 수++;
                continue;
            }
            if (VALOR == '/' && 수 + 1 < 원문크기 && FONTE[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < 원문크기 && !(FONTE[수] == '*' && FONTE[수 + 1] == '/')) 수++;
                if (수 + 1 >= 원문크기) { erro_VALOR("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (carácter_VALOR(VALOR)) { 종류 = 256; while (수 < 원문크기 && 문자이름규칙.이어진글자(FONTE[수])) 수++; }
            else if (díxito_VALOR(VALOR)) { 종류 = 257; while (수 < 원문크기 && díxito_VALOR(FONTE[수])) 수++; }
            else if (VALOR == '"' || VALOR == '\'') {
                종류 = VALOR == '"' ? 258 : 259; 수++;
                while (수 < 원문크기 && FONTE[수] != VALOR && FONTE[수] != 10 && FONTE[수] != 13) {
                    if (FONTE[수] == '\\') 수++;
                    수++;
                }
                if (수 >= 원문크기 || FONTE[수] != VALOR) { erro_VALOR("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < 원문크기) {
                    int Seguinte_elemento = FONTE[수];
                    if (VALOR == '=' && Seguinte_elemento == '=') 종류 = 300;
                    if (VALOR == '!' && Seguinte_elemento == '=') 종류 = 301;
                    if (VALOR == '<' && Seguinte_elemento == '=') 종류 = 302;
                    if (VALOR == '>' && Seguinte_elemento == '=') 종류 = 303;
                    if (VALOR == '&' && Seguinte_elemento == '&') 종류 = 304;
                    if (VALOR == '|' && Seguinte_elemento == '|') 종류 = 305;
                    if (VALOR == '+' && Seguinte_elemento == '+') 종류 = 306;
                    if (VALOR == '-' && Seguinte_elemento == '-') 종류 = 307;
                    if (VALOR == '+' && Seguinte_elemento == '=') 종류 = 308;
                    if (VALOR == '-' && Seguinte_elemento == '=') 종류 = 309;
                    if (VALOR == '*' && Seguinte_elemento == '=') 종류 = 310;
                    if (VALOR == '/' && Seguinte_elemento == '=') 종류 = 311;
                    if (VALOR == '%' && Seguinte_elemento == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (ficha_CONTAR == 토큰종류.length - 1) { erro_VALOR("too many tokens (2047 maximum)"); break; }
            토큰종류[ficha_CONTAR] = 종류; ficha_cargo[ficha_CONTAR] = Executar_2; ficha_duración[ficha_CONTAR++] = 수 - Executar_2;
        }
    }
    static void escribir_constante_byte(int VALOR) {
        if (상수크기 == constante_VALOR.length) { erro_VALOR("constant pool too large"); return; }
        constante_VALOR[상수크기++] = VALOR & 255;
    }
    static void 상짧(int VALOR) { escribir_constante_byte(VALOR >> 8); escribir_constante_byte(VALOR); }
    static int rexistrarse_constante(int Executar_2) {
        for (int 수 = 1; 수 < constante_CONTAR; 수++) {
            int frontal_VALOR = constante_DESPRAZAMENTO[수], duración_VALOR = (수 + 1 < constante_CONTAR ? constante_DESPRAZAMENTO[수 + 1] : Executar_2) - frontal_VALOR;
            if (duración_VALOR != 상수크기 - Executar_2) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < duración_VALOR; 칸++) if (constante_VALOR[frontal_VALOR + 칸] != constante_VALOR[Executar_2 + 칸]) 같음 = false;
            if (같음) { 상수크기 = Executar_2; return 수; }
        }
        if (constante_CONTAR == constante_DESPRAZAMENTO.length) { erro_VALOR("too many constants"); return 0; }
        constante_DESPRAZAMENTO[constante_CONTAR] = Executar_2;
        return constante_CONTAR++;
    }
    static void Anexar_SMS(int VALOR) {
        if (carácter_duración == 문자.length) { erro_VALOR("text too long"); return; }
        문자[carácter_duración++] = VALOR;
    }
    static void Anexar_Word(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) Anexar_SMS(Word_SMS.charAt(수)); }
    static int carácter_constante() {
        int Executar_2 = 상수크기; escribir_constante_byte(1); 상짧(0);
        for (int 수 = 0; 수 < carácter_duración; 수++) {
            int VALOR = 문자[수];
            if (VALOR > 0 && VALOR < 128) escribir_constante_byte(VALOR);
            else if (VALOR < 2048) { escribir_constante_byte(192 | VALOR >> 6); escribir_constante_byte(128 | VALOR & 63); }
            else { escribir_constante_byte(224 | VALOR >> 12); escribir_constante_byte(128 | VALOR >> 6 & 63); escribir_constante_byte(128 | VALOR & 63); }
        }
        if (ERRO) return 0;
        int duración_VALOR = 상수크기 - Executar_2 - 3;
        constante_VALOR[Executar_2 + 1] = duración_VALOR >> 8; constante_VALOR[Executar_2 + 2] = duración_VALOR & 255;
        return rexistrarse_constante(Executar_2);
    }
    static int Word_constante(String Word_SMS) { carácter_duración = 0; Anexar_Word(Word_SMS); return carácter_constante(); }
    static int ficha_constante(int ficha_VALOR) {
        carácter_duración = 0;
        for (int 수 = 0; 수 < ficha_duración[ficha_VALOR]; 수++) Anexar_SMS(FONTE[ficha_cargo[ficha_VALOR] + 수]);
        return carácter_constante();
    }
    static int Material_de_referencia(int 종류, int 가, int 나) {
        int Executar_2 = 상수크기; escribir_constante_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return rexistrarse_constante(Executar_2);
    }
    static int externo_Material_de_referencia(int 종류, String propietario_VALOR, String Nome, String 서술) {
        int 주인 = Material_de_referencia(7, Word_constante(propietario_VALOR), 0);
        int nome_CONTAR = Word_constante(Nome), formato_CONTAR = Word_constante(서술);
        return Material_de_referencia(종류, 주인, Material_de_referencia(12, nome_CONTAR, formato_CONTAR));
    }
    static void 내보내기(int VALOR) {
        if (코드크기 == CÓDIGO_VALOR.length) { erro_VALOR("bytecode too large"); return; }
        CÓDIGO_VALOR[코드크기++] = VALOR & 255;
    }
    static void Orde(int VALOR, int Argumentos) { 내보내기(VALOR); 내보내기(Argumentos >> 8); 내보내기(Argumentos); }
    static void 수상수(int VALOR) {
        if (VALOR >= -1 && VALOR <= 5) { 내보내기(VALOR + 3); return; }
        int Executar_2 = 상수크기; escribir_constante_byte(3); 상짧(VALOR >>> 16); 상짧(VALOR);
        Orde(19, rexistrarse_constante(Executar_2));
    }
    static int ramificación(int Orde) { int RESULTANTE = 코드크기; Orde(Orde, 0); return RESULTANTE; }
    static void Ligar_VALOR(int ramificación, int obxectivo_obxecto) {
        if (ERRO) return;
        int 거리 = obxectivo_obxecto - ramificación;
        if (거리 < -32768 || 거리 > 32767 || ramificación < 0 || ramificación + 2 >= 코드크기) { erro_VALOR("invalid branch"); return; }
        CÓDIGO_VALOR[ramificación + 1] = 거리 >> 8 & 255; CÓDIGO_VALOR[ramificación + 2] = 거리 & 255;
    }
    static void Comparación_VALOR(int Orde) {
        int VERDADEIRO_VALOR = ramificación(Orde); 내보내기(3); int 끝 = ramificación(167);
        Ligar_VALOR(VERDADEIRO_VALOR, 코드크기); 내보내기(4); Ligar_VALOR(끝, 코드크기);
    }
    static int formato_VALOR() {
        if (COLLER_Word("void")) return 0;
        if (COLLER_Word("int")) return 1;
        if (COLLER_Word("boolean")) return 2;
        if (COLLER_Word("char")) return 5;
        if (COLLER_Word("FileInputStream")) return 6;
        if (COLLER_Word("FileOutputStream")) return 7;
        if (COLLER_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        erro_VALOR("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void engadir_formato(int TIPO_VALOR) {
        if (TIPO_VALOR == 0) Anexar_SMS('V');
        if (TIPO_VALOR == 1) Anexar_SMS('I');
        if (TIPO_VALOR == 2) Anexar_SMS('Z');
        if (TIPO_VALOR == 3) Anexar_Word("Ljava/lang/String;");
        if (TIPO_VALOR == 4) Anexar_Word("[Ljava/lang/String;");
        if (TIPO_VALOR == 5) Anexar_SMS('C');
        if (TIPO_VALOR == 6) Anexar_Word("Ljava/io/FileInputStream;");
        if (TIPO_VALOR == 7) Anexar_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws declaración. excepción Proceso_VALOR_introdución 본문은 hospedar javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = COLLER_Word("Galego");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (COLLER_Word("Exception") || COLLER_Word("IOException"))) return;
        if (COLLER_Word("excepción") || COLLER_Word("실행예외") || COLLER_Word("E_S_excepción") || COLLER_Word("agarda_TIMEOUT_excepción") || COLLER_Word("ENDEREZO_Busca_excepción") || COLLER_Word("파일없음예외") || COLLER_Word("통신예외") || COLLER_Word("non_válido_argumento_excepción") || COLLER_Word("숫자형식예외") || COLLER_Word("범위예외") || COLLER_Word("배열범위예외") || COLLER_Word("문자열범위예외") || COLLER_Word("NULO_Material_de_referencia_excepción") || COLLER_Word("산술예외") || COLLER_Word("Estado_excepción") || COLLER_Word("TIPO_conversión_excepción") || COLLER_Word("음수배열크기예외") || COLLER_Word("MATRIZ_Store_erro") || COLLER_Word("tema_Estado_excepción") || COLLER_Word("대기중단예외")) return;
        erro_VALOR("unsupported throws type");
    }
    static void 선언읽기() {
        while (COLLER_Word("import")) {
            if (Word_VALOR(Posición, "Galego")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(COLLER_Word("FileInputStream") || COLLER_Word("FileOutputStream") || COLLER_Word("IOException"))) erro_VALOR("unsupported import");
            }
            요구(';');
        }
        COLLER_Word("public"); COLLER_Word("final"); 말요구("class"); Clase_ficha = 식별자();
        Clase_constante = Material_de_referencia(7, ficha_constante(Clase_ficha), 0);
        부모상수 = Material_de_referencia(7, Word_constante("java/lang/Object"), 0); CÓDIGO_constante = Word_constante("Code"); 요구('{');
        while (!ERRO && 종류() != '}') {
            if (함수수 == 32) { erro_VALOR("too many methods"); break; }
            int acceso_introdución = COLLER_Word("public") ? 1 : COLLER_Word("private") ? 2 : 0; 말요구("static");
            int FUNCIÓN_VALOR = 함수수++;
            함수권한[FUNCIÓN_VALOR] = acceso_introdución | 8;
            함수반환[FUNCIÓN_VALOR] = formato_VALOR(); 함수이름[FUNCIÓN_VALOR] = 식별자(); 요구('(');
            for (int frontal_VALOR = 0; frontal_VALOR < FUNCIÓN_VALOR; frontal_VALOR++) if (이름같음(함수이름[frontal_VALOR], 함수이름[FUNCIÓN_VALOR])) erro_VALOR("duplicate method (overloading unsupported)");
            while (!ERRO && 종류() != ')') {
                int 수 = 함수인수수[FUNCIÓN_VALOR];
                if (수 == 16) { erro_VALOR("too many parameters"); break; }
                int TIPO_VALOR = formato_VALOR(); if (TIPO_VALOR == 0) erro_VALOR("void parameter");
                함수인수형[FUNCIÓN_VALOR * 16 + 수] = TIPO_VALOR; 함수인수이름[FUNCIÓN_VALOR * 16 + 수] = 식별자();
                함수인수수[FUNCIÓN_VALOR]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (COLLER_Word("throws")) {
                do { 예외이름읽기(); } while (!ERRO && 받기(','));
            }
            함수본문[FUNCIÓN_VALOR] = Posición; 요구('{');
            int aniñamento_VALOR = 1;
            while (Posición < ficha_CONTAR && aniñamento_VALOR > 0) {
                if (종류() == '{') aniñamento_VALOR++;
                if (종류() == '}') aniñamento_VALOR--;
                Posición++;
            }
            if (aniñamento_VALOR != 0) erro_VALOR("unclosed method body");
            함수끝[FUNCIÓN_VALOR] = Posición;
            함수명상수[FUNCIÓN_VALOR] = ficha_constante(함수이름[FUNCIÓN_VALOR]);
            carácter_duración = 0; Anexar_SMS('(');
            for (int 수 = 0; 수 < 함수인수수[FUNCIÓN_VALOR]; 수++) engadir_formato(함수인수형[FUNCIÓN_VALOR * 16 + 수]);
            Anexar_SMS(')'); engadir_formato(함수반환[FUNCIÓN_VALOR]); 함수서술[FUNCIÓN_VALOR] = carácter_constante();
        }
        요구('}'); if (Posición != ficha_CONTAR) erro_VALOR("extra input after class");
    }
    static int Busca_local(int Nome) {
        for (int 수 = local_CONTAR - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(local_nome[수], Nome)) return 수;
        erro_VALOR("unknown variable"); return 0;
    }
    static int engadir_local(int Nome, int TIPO_VALOR) {
        for (int 수 = 0; 수 < local_CONTAR; 수++) if (지역깊이[수] >= 0 && 이름같음(local_nome[수], Nome)) erro_VALOR("duplicate local variable");
        if (local_CONTAR == 128) { erro_VALOR("too many locals"); return 0; }
        local_nome[local_CONTAR] = Nome; local_TIPO[local_CONTAR] = TIPO_VALOR; 지역깊이[local_CONTAR] = 깊이;
        return local_CONTAR++;
    }
    static boolean número_enteiro_TIPO(int TIPO_VALOR) { return TIPO_VALOR == 1 || TIPO_VALOR == 5; }
    static void 지역읽기(int 수) { 내보내기(local_TIPO[수] <= 2 || local_TIPO[수] == 5 ? 21 : 25); 내보내기(수); }
    static void escribir_local(int 수) { 내보내기(local_TIPO[수] <= 2 || local_TIPO[수] == 5 ? 54 : 58); 내보내기(수); }
    static void verificar_TIPO(int real_datos, int 기대) { if (real_datos != 기대 && !(real_datos == 5 && 기대 == 1)) erro_VALOR("type mismatch"); }
    static void 문자읽기(int ficha_VALOR) {
        carácter_duración = 0; int Executar_2 = ficha_cargo[ficha_VALOR] + 1, 끝 = ficha_cargo[ficha_VALOR] + ficha_duración[ficha_VALOR] - 1;
        while (Executar_2 < 끝 && !ERRO) {
            int VALOR = FONTE[Executar_2++];
            if (VALOR == '\\') {
                if (Executar_2 == 끝) { erro_VALOR("invalid escape"); break; }
                VALOR = FONTE[Executar_2++];
                if (VALOR == 'n') VALOR = 10;
                else if (VALOR == 'r') VALOR = 13;
                else if (VALOR == 't') VALOR = 9;
                else if (VALOR == 'b') VALOR = 8;
                else if (VALOR == 'f') VALOR = 12;
                else if (VALOR != '\\' && VALOR != '"' && VALOR != '\'') erro_VALOR("unsupported escape");
            }
            Anexar_SMS(VALOR);
        }
    }
    static int analizar_número_enteiro(int ficha_VALOR, boolean 음수) {
        if (ficha_duración[ficha_VALOR] > 1 && FONTE[ficha_cargo[ficha_VALOR]] == '0') erro_VALOR("octal literals unsupported");
        int VALOR = 0;
        for (int 수 = 0; 수 < ficha_duración[ficha_VALOR]; 수++) {
            int díxito_elemento = FONTE[ficha_cargo[ficha_VALOR] + 수] - '0';
            if (VALOR < -214748364 || VALOR == -214748364 && díxito_elemento > (음수 ? 8 : 7)) erro_VALOR("integer literal out of range");
            VALOR = VALOR * 10 - díxito_elemento;
        }
        return 음수 ? VALOR : -VALOR;
    }
    static int 기본식() {
        if (COLLER_Word("new")) {
            int TIPO_VALOR = formato_VALOR();
            if (TIPO_VALOR != 6 && TIPO_VALOR != 7) { erro_VALOR("only file streams supported by new in source"); return 0; }
            String propietario_VALOR = TIPO_VALOR == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Orde(187, Material_de_referencia(7, Word_constante(propietario_VALOR), 0)); 내보내기(89);
            요구('('); verificar_TIPO(expresión_VALOR(), 3); boolean 이어 = false;
            if (받기(',')) { if (TIPO_VALOR != 7) erro_VALOR("input stream constructor arguments"); verificar_TIPO(expresión_VALOR(), 2); 이어 = true; }
            요구(')');
            Orde(183, externo_Material_de_referencia(10, propietario_VALOR, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TIPO_VALOR;
        }
        if (받기('(')) { int TIPO_VALOR = expresión_VALOR(); 요구(')'); return TIPO_VALOR; }
        if (종류() == 257) { 수상수(analizar_número_enteiro(Posición++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Posición++); Orde(19, Material_de_referencia(8, carácter_constante(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Posición++); if (carácter_duración != 1) erro_VALOR("character literal length"); 수상수(문자[0]); return 5; }
        if (COLLER_Word("true")) { 내보내기(4); return 2; }
        if (COLLER_Word("false")) { 내보내기(3); return 2; }
        if (COLLER_Word("Galego")) {
            요구('.'); 말요구("자체"); 요구('.');
            String propietario_VALOR = "", 메서드 = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, RESULTANTE = 0;
            if (COLLER_Word("Saída")) {
                propietario_VALOR = "Galego/자체/Saída"; 요구('.');
                if (COLLER_Word("escribir_liña")) { 메서드 = "escribir_liña"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (COLLER_Word("Escritura")) { 메서드 = "Escritura"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (COLLER_Word("수쓰기")) { 메서드 = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else erro_VALOR("unknown Korean output method");
            } else if (COLLER_Word("문자")) {
                propietario_VALOR = "Galego/자체/문자"; 요구('.'); 가 = 3;
                if (COLLER_Word("duración_VALOR")) { 메서드 = "duración_VALOR"; 서술 = "(Ljava/lang/String;)I"; RESULTANTE = 1; }
                else if (COLLER_Word("código_de_carácter_CONTAR")) { 메서드 = "código_de_carácter_CONTAR"; 서술 = "(Ljava/lang/String;)I"; RESULTANTE = 1; }
                else if (COLLER_Word("analizar_número_enteiro")) { 메서드 = "analizar_número_enteiro"; 서술 = "(Ljava/lang/String;)I"; RESULTANTE = 1; }
                else if (COLLER_Word("escribir_número_enteiro_VALOR")) { 메서드 = "escribir_número_enteiro_VALOR"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; RESULTANTE = 3; }
                else if (COLLER_Word("같음")) { 메서드 = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; RESULTANTE = 2; }
                else if (COLLER_Word("pegar_SMS")) { 메서드 = "pegar_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; RESULTANTE = 3; }
                else if (COLLER_Word("cortar_VALOR")) { 메서드 = "cortar_VALOR"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; RESULTANTE = 3; }
                else erro_VALOR("unknown Korean text method");
            } else if (COLLER_Word("Ficheiro")) {
                propietario_VALOR = "Galego/자체/Ficheiro"; 요구('.'); 가 = 3;
                if (COLLER_Word("Lectura")) { 메서드 = "Lectura"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; RESULTANTE = 3; }
                else if (COLLER_Word("Escritura")) { 메서드 = "Escritura"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else erro_VALOR("unknown Korean file method");
            } else if (COLLER_Word("화면")) {
                propietario_VALOR = "Galego/자체/화면"; 요구('.');
                if (COLLER_Word("너비")) { 메서드 = "너비"; 서술 = "()I"; RESULTANTE = 1; }
                else if (COLLER_Word("높이")) { 메서드 = "높이"; 서술 = "()I"; RESULTANTE = 1; }
                else if (COLLER_Word("사각형")) { 메서드 = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (COLLER_Word("borrar_introdución")) { 메서드 = "borrar_introdución"; 서술 = "(I)V"; 가 = 1; }
                else if (COLLER_Word("기다리기")) { 메서드 = "기다리기"; 서술 = "()V"; }
                else erro_VALOR("unknown Korean framebuffer method");
            } else erro_VALOR("unsupported Korean library class");
            요구('('); if (가 != 0) verificar_TIPO(expresión_VALOR(), 가);
            if (나 != 0) { 요구(','); verificar_TIPO(expresión_VALOR(), 나); }
            if (다 != 0) { 요구(','); verificar_TIPO(expresión_VALOR(), 다); }
            if (라 != 0) { 요구(','); verificar_TIPO(expresión_VALOR(), 라); }
            if (마 != 0) { 요구(','); verificar_TIPO(expresión_VALOR(), 마); }
            요구(')'); Orde(184, externo_Material_de_referencia(10, propietario_VALOR, 메서드, 서술)); return RESULTANTE;
        }
        if (COLLER_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); verificar_TIPO(expresión_VALOR(), 3); 요구(')');
            Orde(184, externo_Material_de_referencia(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nome = 식별자();
        if (받기('(')) {
            int FUNCIÓN_VALOR = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Nome, 함수이름[수])) FUNCIÓN_VALOR = 수;
            if (FUNCIÓN_VALOR < 0) { erro_VALOR("unknown static method"); return 0; }
            int 수 = 0;
            while (!ERRO && 종류() != ')') {
                if (수 >= 함수인수수[FUNCIÓN_VALOR]) { erro_VALOR("too many arguments"); break; }
                verificar_TIPO(expresión_VALOR(), 함수인수형[FUNCIÓN_VALOR * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[FUNCIÓN_VALOR]) erro_VALOR("argument count mismatch");
            Orde(184, Material_de_referencia(10, Clase_constante, Material_de_referencia(12, 함수명상수[FUNCIÓN_VALOR], 함수서술[FUNCIÓN_VALOR])));
            return 함수반환[FUNCIÓN_VALOR];
        }
        int local_Ámbito = Busca_local(Nome), TIPO_VALOR = local_TIPO[local_Ámbito]; 지역읽기(local_Ámbito);
        while (!ERRO) {
            if (받기('[')) { verificar_TIPO(TIPO_VALOR, 4); verificar_TIPO(expresión_VALOR(), 1); 요구(']'); 내보내기(50); TIPO_VALOR = 3; }
            else if (받기('.')) {
                if (TIPO_VALOR == 6 || TIPO_VALOR == 7) {
                    String propietario_VALOR = TIPO_VALOR == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (COLLER_Word("close")) { 요구('('); 요구(')'); Orde(182, externo_Material_de_referencia(10, propietario_VALOR, "close", "()V")); TIPO_VALOR = 0; }
                    else if (TIPO_VALOR == 6 && COLLER_Word("read")) { 요구('('); 요구(')'); Orde(182, externo_Material_de_referencia(10, propietario_VALOR, "read", "()I")); TIPO_VALOR = 1; }
                    else if (TIPO_VALOR == 7 && COLLER_Word("write")) { 요구('('); verificar_TIPO(expresión_VALOR(), 1); 요구(')'); Orde(182, externo_Material_de_referencia(10, propietario_VALOR, "write", "(I)V")); TIPO_VALOR = 0; }
                    else { erro_VALOR("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TIPO_VALOR == 4) { 내보내기(190); TIPO_VALOR = 1; }
                else { verificar_TIPO(TIPO_VALOR, 3); 요구('('); 요구(')'); Orde(182, externo_Material_de_referencia(10, "java/lang/String", "length", "()I")); TIPO_VALOR = 1; }
            } else break;
        }
        return TIPO_VALOR;
    }
    static int 단항() {
        if (++식깊이 > 64) { erro_VALOR("expression nesting too deep"); 식깊이--; return 0; }
        int TIPO_VALOR;
        if (받기('!')) { verificar_TIPO(단항(), 2); Comparación_VALOR(153); TIPO_VALOR = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(analizar_número_enteiro(Posición++, true));
            else { verificar_TIPO(단항(), 1); 내보내기(116); }
            TIPO_VALOR = 1;
        } else if (받기('+')) { verificar_TIPO(단항(), 1); TIPO_VALOR = 1; }
        else TIPO_VALOR = 기본식();
        식깊이--; return TIPO_VALOR;
    }
    static int 곱식() {
        int TIPO_VALOR = 단항();
        while (!ERRO && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int codificación_VALOR = 종류(); Posición++; verificar_TIPO(TIPO_VALOR, 1); verificar_TIPO(단항(), 1);
            내보내기(codificación_VALOR == '*' ? 104 : codificación_VALOR == '/' ? 108 : 112); TIPO_VALOR = 1;
        }
        return TIPO_VALOR;
    }
    static int 합식() {
        int TIPO_VALOR = 곱식();
        while (!ERRO && (종류() == '+' || 종류() == '-')) {
            int codificación_VALOR = 종류(); Posición++; int 경계 = 코드크기, ATRÁS_VALOR_TIPO = 곱식();
            if (codificación_VALOR == '+' && (TIPO_VALOR == 3 || ATRÁS_VALOR_TIPO == 3)) { 결합(경계, TIPO_VALOR, ATRÁS_VALOR_TIPO); TIPO_VALOR = 3; }
            else { verificar_TIPO(TIPO_VALOR, 1); verificar_TIPO(ATRÁS_VALOR_TIPO, 1); 내보내기(codificación_VALOR == '+' ? 96 : 100); TIPO_VALOR = 1; }
        }
        return TIPO_VALOR;
    }
    static int 붙임참조(int TIPO_VALOR) {
        if (TIPO_VALOR != 1 && TIPO_VALOR != 2 && TIPO_VALOR != 3 && TIPO_VALOR != 5) erro_VALOR("unsupported concatenation type");
        return externo_Material_de_referencia(10, "java/lang/StringBuilder", "append", TIPO_VALOR == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TIPO_VALOR == 2 ? "(Z)Ljava/lang/StringBuilder;" : TIPO_VALOR == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int frontal_VALOR_TIPO, int ATRÁS_VALOR_TIPO) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 DEREITA CÓDIGO_VALOR 앞에 xerar 코드를 삽입한다.
        // DEREITA expresión_VALOR 내부의 punto_VALOR ramificación 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        Orde(187, Material_de_referencia(7, Word_constante("java/lang/StringBuilder"), 0)); 내보내기(89);
        Orde(183, externo_Material_de_referencia(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Orde(182, 붙임참조(frontal_VALOR_TIPO));
        if (ERRO) return;
        int duración_VALOR = 코드크기 - 끝;
        for (int 수 = 0; 수 < duración_VALOR; 수++) 삽입코드[수] = CÓDIGO_VALOR[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CÓDIGO_VALOR[수 + duración_VALOR] = CÓDIGO_VALOR[수];
        for (int 수 = 0; 수 < duración_VALOR; 수++) CÓDIGO_VALOR[경계 + 수] = 삽입코드[수];
        Orde(182, 붙임참조(ATRÁS_VALOR_TIPO)); Orde(182, externo_Material_de_referencia(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Comparación_expresión() {
        int TIPO_VALOR = 합식();
        while (!ERRO && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int codificación_VALOR = 종류(); Posición++; verificar_TIPO(TIPO_VALOR, 1); verificar_TIPO(합식(), 1);
            Comparación_VALOR(codificación_VALOR == '<' ? 161 : codificación_VALOR == '>' ? 163 : codificación_VALOR == 302 ? 164 : 162); TIPO_VALOR = 2;
        }
        return TIPO_VALOR;
    }
    static int 동등식() {
        int TIPO_VALOR = Comparación_expresión();
        while (!ERRO && (종류() == 300 || 종류() == 301)) {
            int codificación_VALOR = 종류(); Posición++; int ATRÁS_VALOR_TIPO = Comparación_expresión();
            if (TIPO_VALOR == 0 || ATRÁS_VALOR_TIPO == 0) erro_VALOR("void expression");
            if (!(número_enteiro_TIPO(TIPO_VALOR) && número_enteiro_TIPO(ATRÁS_VALOR_TIPO))) verificar_TIPO(ATRÁS_VALOR_TIPO, TIPO_VALOR);
            Comparación_VALOR((TIPO_VALOR <= 2 || TIPO_VALOR == 5 ? 159 : 165) + (codificación_VALOR == 301 ? 1 : 0)); TIPO_VALOR = 2;
        }
        return TIPO_VALOR;
    }
    static int 논리곱() {
        int TIPO_VALOR = 동등식();
        while (!ERRO && 받기(304)) {
            verificar_TIPO(TIPO_VALOR, 2); int 가 = ramificación(153); verificar_TIPO(동등식(), 2); int 나 = ramificación(153);
            내보내기(4); int 끝 = ramificación(167); Ligar_VALOR(가, 코드크기); Ligar_VALOR(나, 코드크기); 내보내기(3); Ligar_VALOR(끝, 코드크기); TIPO_VALOR = 2;
        }
        return TIPO_VALOR;
    }
    static int expresión_VALOR() {
        int TIPO_VALOR = 논리곱();
        while (!ERRO && 받기(305)) {
            verificar_TIPO(TIPO_VALOR, 2); int 가 = ramificación(154); verificar_TIPO(논리곱(), 2); int 나 = ramificación(154);
            내보내기(3); int 끝 = ramificación(167); Ligar_VALOR(가, 코드크기); Ligar_VALOR(나, 코드크기); 내보내기(4); Ligar_VALOR(끝, 코드크기); TIPO_VALOR = 2;
        }
        return TIPO_VALOR;
    }
    static void tarefa_VALOR(boolean Permitir_declaración) {
        if (Word_VALOR(Posición, "int") || Word_VALOR(Posición, "boolean") || Word_VALOR(Posición, "String") || Word_VALOR(Posición, "char")
            || Word_VALOR(Posición, "FileInputStream") || Word_VALOR(Posición, "FileOutputStream")) {
            if (!Permitir_declaración) erro_VALOR("declaration not allowed here");
            int TIPO_VALOR = formato_VALOR(), Nome = 식별자(); 요구('='); verificar_TIPO(expresión_VALOR(), TIPO_VALOR);
            escribir_local(engadir_local(Nome, TIPO_VALOR)); return;
        }
        int Nome = 식별자(), local_Ámbito = Busca_local(Nome);
        if (받기('=')) { verificar_TIPO(expresión_VALOR(), local_TIPO[local_Ámbito]); escribir_local(local_Ámbito); }
        else if (종류() >= 308 && 종류() <= 312) {
            int codificación_VALOR = 종류(); Posición++; 지역읽기(local_Ámbito); int 경계 = 코드크기, ATRÁS_VALOR_TIPO = expresión_VALOR();
            if (codificación_VALOR == 308 && local_TIPO[local_Ámbito] == 3) 결합(경계, 3, ATRÁS_VALOR_TIPO);
            else {
                verificar_TIPO(local_TIPO[local_Ámbito], 1); verificar_TIPO(ATRÁS_VALOR_TIPO, 1);
                내보내기(codificación_VALOR == 308 ? 96 : codificación_VALOR == 309 ? 100 : codificación_VALOR == 310 ? 104 : codificación_VALOR == 311 ? 108 : 112);
                if (local_TIPO[local_Ámbito] == 5) 내보내기(146);
            }
            escribir_local(local_Ámbito);
        }
        else if (종류() == 306 || 종류() == 307) {
            verificar_TIPO(local_TIPO[local_Ámbito], 1); 내보내기(132); 내보내기(local_Ámbito); 내보내기(종류() == 306 ? 1 : 255); Posición++;
            if (local_TIPO[local_Ámbito] == 5) { 지역읽기(local_Ámbito); 내보내기(146); escribir_local(local_Ámbito); }
        } else erro_VALOR("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = COLLER_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Orde(178, externo_Material_de_referencia(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean baleiro_argumento = 종류() == ')';
        int TIPO_VALOR = baleiro_argumento ? 0 : expresión_VALOR(); 요구(')'); 요구(';');
        String 서술 = TIPO_VALOR == 0 ? "()V" : TIPO_VALOR == 1 ? "(I)V" : TIPO_VALOR == 2 ? "(Z)V" : TIPO_VALOR == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TIPO_VALOR == 4 || TIPO_VALOR >= 6 || TIPO_VALOR == 0 && (!줄바꿈 || !baleiro_argumento)) erro_VALOR("unsupported print argument");
        Orde(182, externo_Material_de_referencia(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean instrución_VALOR() {
        if (ERRO) return false;
        if (깊이 > 32) { erro_VALOR("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean devolver_medida = false;
            while (!ERRO && 종류() != '}') { if (devolver_medida) erro_VALOR("unreachable statement"); devolver_medida = instrución_VALOR(); }
            요구('}'); for (int 수 = 0; 수 < local_CONTAR; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return devolver_medida;
        }
        if (받기(';')) return false;
        if (COLLER_Word("return")) {
            int TIPO_VALOR = 종류() == ';' ? 0 : expresión_VALOR(); verificar_TIPO(TIPO_VALOR, 함수반환[현재함수]); 요구(';');
            내보내기(TIPO_VALOR == 0 ? 177 : TIPO_VALOR <= 2 || TIPO_VALOR == 5 ? 172 : 176); return true;
        }
        if (COLLER_Word("if")) {
            요구('('); verificar_TIPO(expresión_VALOR(), 2); 요구(')'); int FALSO_VALOR = ramificación(153);
            깊이++; boolean 가 = control_instrución(); 깊이--;
            if (COLLER_Word("else")) { int 끝 = ramificación(167); Ligar_VALOR(FALSO_VALOR, 코드크기); 깊이++; boolean 나 = control_instrución(); 깊이--; Ligar_VALOR(끝, 코드크기); return 가 && 나; }
            Ligar_VALOR(FALSO_VALOR, 코드크기); return false;
        }
        if (COLLER_Word("while")) {
            int Executar_2 = 코드크기; 요구('('); verificar_TIPO(expresión_VALOR(), 2); 요구(')'); int 끝 = ramificación(153);
            깊이++; control_instrución(); 깊이--; Ligar_VALOR(ramificación(167), Executar_2); Ligar_VALOR(끝, 코드크기); return false;
        }
        if (COLLER_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') tarefa_VALOR(true); 요구(';');
            int condición = 코드크기; if (종류() == ';') 내보내기(4); else verificar_TIPO(expresión_VALOR(), 2); 요구(';');
            int 끝 = ramificación(153), corpo_do_texto = ramificación(167), actualizar = 코드크기;
            if (종류() != ')') tarefa_VALOR(false); 요구(')'); Ligar_VALOR(ramificación(167), condición); Ligar_VALOR(corpo_do_texto, 코드크기);
            control_instrución(); Ligar_VALOR(ramificación(167), actualizar); Ligar_VALOR(끝, 코드크기);
            for (int 수 = 0; 수 < local_CONTAR; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALOR(Posición, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Posición + 1 < ficha_CONTAR && (토큰종류[Posición + 1] == '(' || 토큰종류[Posición + 1] == '.')) {
            int TIPO_VALOR = expresión_VALOR(); if (TIPO_VALOR != 0) 내보내기(87); 요구(';'); return false;
        }
        tarefa_VALOR(true); 요구(';'); return false;
    }
    static boolean control_instrución() {
        if (Word_VALOR(Posición, "int") || Word_VALOR(Posición, "boolean") || Word_VALOR(Posición, "char") || Word_VALOR(Posición, "String")
            || Word_VALOR(Posición, "FileInputStream") || Word_VALOR(Posición, "FileOutputStream")) erro_VALOR("local declaration requires braces");
        return instrución_VALOR();
    }
    static void 출바(int VALOR) { if (출력크기 == Saída.length) erro_VALOR("class file too large"); else Saída[출력크기++] = VALOR & 255; }
    static void 출짧(int VALOR) { 출바(VALOR >> 8); 출바(VALOR); }
    static void 출정(int VALOR) { 출짧(VALOR >>> 16); 출짧(VALOR); }
    static void escribir_Clase() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(constante_CONTAR);
        for (int 수 = 0; 수 < 상수크기; 수++) 출바(constante_VALOR[수]);
        출짧(0x21); 출짧(Clase_constante); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(함수권한[수]); 출짧(함수명상수[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CÓDIGO_constante);
            출정(12 + 함수길이[수]); 출짧(128); 출짧(함수지역[수]); 출정(함수길이[수]);
            for (int 칸 = 0; 칸 < 함수길이[수]; 칸++) 출바(CÓDIGO_VALOR[함수코드[수] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Executar_2() {
        if (usuario.인수개수() == 1 && 자바도구.같음(usuario.Argumentos(0), "-version")) {
            usuario.Escritura("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (usuario.인수개수() != 1) { usuario.Escritura("Usage: javac FILE.java\n"); return 2; }
        int 이름크기 = 자바도구.Nome(Ficheiro_nome_SMS, usuario.Argumentos(0));
        if (이름크기 < 6 || 이름크기 > 62 || Ficheiro_nome_SMS[이름크기 - 5] != '.' || Ficheiro_nome_SMS[이름크기 - 4] != 'j'
            || Ficheiro_nome_SMS[이름크기 - 3] != 'a' || Ficheiro_nome_SMS[이름크기 - 2] != 'v' || Ficheiro_nome_SMS[이름크기 - 1] != 'a') {
            usuario.Escritura("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        원문크기 = usuario.파일읽기(Ficheiro_nome_SMS, FONTE);
        if (원문크기 < 0) { usuario.Escritura("javac: cannot read source: "); 자바도구.수쓰기(원문크기); usuario.escribir_carácter_VALOR(10); return 1; }
        원문크기 = 자바도구.원문해독(FONTE, 원문크기);
        if (원문크기 < 0) { usuario.Escritura("javac error: invalid UTF-8 source\n"); return 1; }
        cortar_VALOR(); if (!ERRO) 선언읽기();
        if (!ERRO) {
            if (ficha_duración[Clase_ficha] != 이름크기 - 5) erro_VALOR("class name must match file name");
            for (int 수 = 0; 수 < 이름크기 - 5; 수++) if (FONTE[ficha_cargo[Clase_ficha] + 수] != Ficheiro_nome_SMS[수]) erro_VALOR("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !ERRO; 현재함수++) {
            Posición = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; local_CONTAR = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) engadir_local(함수인수이름[현재함수 * 16 + 수], 함수인수형[현재함수 * 16 + 수]);
            boolean devolver_medida = instrución_VALOR();
            if (!devolver_medida && 함수반환[현재함수] != 0) erro_VALOR("missing return");
            // ramificación 뒤의 합류 지점은 반드시 real_datos 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean número_enteiro = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(número_enteiro ? 3 : 1); 내보내기(número_enteiro ? 172 : 176); }
            if (Posición != 함수끝[현재함수]) erro_VALOR("invalid method body");
            함수지역[현재함수] = local_CONTAR; 함수길이[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (ERRO) return 1;
        escribir_Clase(); if (ERRO) return 1;
        Ficheiro_nome_SMS[이름크기 - 4] = 'c'; Ficheiro_nome_SMS[이름크기 - 3] = 'l'; Ficheiro_nome_SMS[이름크기 - 2] = 'a';
        Ficheiro_nome_SMS[이름크기 - 1] = 's'; Ficheiro_nome_SMS[이름크기] = 's'; Ficheiro_nome_SMS[이름크기 + 1] = 0;
        int RESULTANTE = usuario.escribir_Ficheiro(Ficheiro_nome_SMS, Saída, 출력크기);
        if (RESULTANTE < 0) { usuario.Escritura("javac: cannot save class: "); 자바도구.수쓰기(RESULTANTE); usuario.escribir_carácter_VALOR(10); return 1; }
        usuario.Escritura("Compiled: "); for (int 수 = 0; Ficheiro_nome_SMS[수] != 0; 수++) usuario.escribir_carácter_VALOR(Ficheiro_nome_SMS[수]);
        usuario.Escritura(" (JVM class version 49)\n"); return 0;
    }
}
