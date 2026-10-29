// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java fonte_árvore -> 표준 버전 49 class compilador. */
public final class 자바컴파일러 {
    static int[] códigoFonte = new int[16384], saídaTexto = new int[16384], valor_do_código = new int[4096];
    static int[] token_Tipo = new int[2048], token_cargo = new int[2048], token_duração = new int[2048];
    static int[] constante_VALOR = new int[4096], constante_DESLOC = new int[512];
    static int[] 문자 = new int[512], nome_de_arquivo_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int fonte_dimensionar, token_CONT_NÚM, posição, CÓDIGO_dimensionar, constante_dimensionar, constante_CONT_NÚM = 1, saída_dimensionar, caractere_duração;
    static boolean erro;
    static int aula_token, aula_constante, pai_constante, CÓDIGO_constante;
    static int[] método_entrada_nome = new int[32], método_devolver = new int[32], método_argumento_CONT_NÚM = new int[32];
    static int[] método_argumento_nome = new int[512], método_argumento_TIPO = new int[512];
    static int[] corpo_do_método = new int[32], método_encerrar = new int[32], método_CÓDIGO = new int[32];
    static int[] método_duração = new int[32], 함수지역 = new int[32], método_nome_constante = new int[32], método_descritor_constante = new int[32];
    static int[] método_acesso = new int[32];
    static int método_CONT_NÚM, em_dia_método, local_CONT_NÚM, 깊이, 식깊이;
    static int[] local_nome = new int[128], local_TIPO = new int[128], 지역깊이 = new int[128];

    static void falha_VALOR(String 이유) {
        if (!erro) {
            espaço_do_utilizador.Escrita("javac error: "); espaço_do_utilizador.Escrita(이유);
            espaço_do_utilizador.Escrita(" at line ");
            int linha_de_entrada = 1, 끝 = posição < token_CONT_NÚM ? token_cargo[posição] : fonte_dimensionar;
            for (int número = 0; número < 끝; número++) if (códigoFonte[número] == 10) linha_de_entrada++;
            FerramentasJava.gravar_número(linha_de_entrada); espaço_do_utilizador.gravar_caractere_VALOR(10);
        }
        erro = true;
    }
    static boolean caractere_VALOR(int VALOR) { return 문자이름규칙.첫글자(VALOR); }
    static boolean dígito_VALOR(int VALOR) { return VALOR >= '0' && VALOR <= '9'; }
    static boolean 이름같음(int 가, int SEGUNDO_operando) {
        if (가 < 0 || SEGUNDO_operando < 0 || 가 >= token_CONT_NÚM || SEGUNDO_operando >= token_CONT_NÚM || token_duração[가] != token_duração[SEGUNDO_operando]) return false;
        for (int número = 0; número < token_duração[가]; número++) if (códigoFonte[token_cargo[가] + número] != códigoFonte[token_cargo[SEGUNDO_operando] + número]) return false;
        return true;
    }
    static boolean Word_VALOR(int token_VALOR, String Word_SMS) {
        if (token_VALOR < 0 || token_VALOR >= token_CONT_NÚM || token_duração[token_VALOR] != Word_SMS.length()) return false;
        for (int número = 0; número < Word_SMS.length(); número++) if (códigoFonte[token_cargo[token_VALOR] + número] != Word_SMS.charAt(número)) return false;
        return true;
    }
    static int Tipo_VALOR() { return posição < token_CONT_NÚM ? token_Tipo[posição] : 0; }
    static boolean receber(int VALOR) { if (Tipo_VALOR() != VALOR) return false; posição++; return true; }
    static void requisito_VALOR(int VALOR) { if (!receber(VALOR)) falha_VALOR("unexpected token"); }
    static boolean PEGAR_Word(String Word_SMS) { if (!Word_VALOR(posição, Word_SMS)) return false; posição++; return true; }
    static void 말요구(String Word_SMS) { if (!PEGAR_Word(Word_SMS)) falha_VALOR(Word_SMS); }
    static int identificador_VALOR() {
        int resultado = posição;
        if (Tipo_VALOR() != 256) falha_VALOR("identifier required"); else posição++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int iniciar = 0;
        for (int número = 0; número <= 예약어.length(); número++) {
            if (número == 예약어.length() || 예약어.charAt(número) == ' ') {
                boolean 같음 = número - iniciar == token_duração[resultado];
                for (int slot_entrada = iniciar; 같음 && slot_entrada < número; slot_entrada++) if (예약어.charAt(slot_entrada) != códigoFonte[token_cargo[resultado] + slot_entrada - iniciar]) 같음 = false;
                if (같음) falha_VALOR("reserved word cannot be an identifier");
                iniciar = número + 1;
            }
        }
        return resultado;
    }
    static void cortar_VALOR() {
        int número = 0;
        while (número < fonte_dimensionar && !erro) {
            int VALOR = códigoFonte[número], iniciar = número, Tipo_VALOR = VALOR;
            if (VALOR == 32 || VALOR == 9 || VALOR == 10 || VALOR == 13) { número++; continue; }
            if (VALOR == '/' && número + 1 < fonte_dimensionar && códigoFonte[número + 1] == '/') {
                while (número < fonte_dimensionar && códigoFonte[número] != 10) número++;
                continue;
            }
            if (VALOR == '/' && número + 1 < fonte_dimensionar && códigoFonte[número + 1] == '*') {
                número += 2;
                while (número + 1 < fonte_dimensionar && !(códigoFonte[número] == '*' && códigoFonte[número + 1] == '/')) número++;
                if (número + 1 >= fonte_dimensionar) { falha_VALOR("unterminated comment"); break; }
                número += 2; continue;
            }
            if (caractere_VALOR(VALOR)) { Tipo_VALOR = 256; while (número < fonte_dimensionar && 문자이름규칙.이어진글자(códigoFonte[número])) número++; }
            else if (dígito_VALOR(VALOR)) { Tipo_VALOR = 257; while (número < fonte_dimensionar && dígito_VALOR(códigoFonte[número])) número++; }
            else if (VALOR == '"' || VALOR == '\'') {
                Tipo_VALOR = VALOR == '"' ? 258 : 259; número++;
                while (número < fonte_dimensionar && códigoFonte[número] != VALOR && códigoFonte[número] != 10 && códigoFonte[número] != 13) {
                    if (códigoFonte[número] == '\\') número++;
                    número++;
                }
                if (número >= fonte_dimensionar || códigoFonte[número] != VALOR) { falha_VALOR("unterminated literal"); break; }
                número++;
            } else {
                número++;
                if (número < fonte_dimensionar) {
                    int Avançar_item = códigoFonte[número];
                    if (VALOR == '=' && Avançar_item == '=') Tipo_VALOR = 300;
                    if (VALOR == '!' && Avançar_item == '=') Tipo_VALOR = 301;
                    if (VALOR == '<' && Avançar_item == '=') Tipo_VALOR = 302;
                    if (VALOR == '>' && Avançar_item == '=') Tipo_VALOR = 303;
                    if (VALOR == '&' && Avançar_item == '&') Tipo_VALOR = 304;
                    if (VALOR == '|' && Avançar_item == '|') Tipo_VALOR = 305;
                    if (VALOR == '+' && Avançar_item == '+') Tipo_VALOR = 306;
                    if (VALOR == '-' && Avançar_item == '-') Tipo_VALOR = 307;
                    if (VALOR == '+' && Avançar_item == '=') Tipo_VALOR = 308;
                    if (VALOR == '-' && Avançar_item == '=') Tipo_VALOR = 309;
                    if (VALOR == '*' && Avançar_item == '=') Tipo_VALOR = 310;
                    if (VALOR == '/' && Avançar_item == '=') Tipo_VALOR = 311;
                    if (VALOR == '%' && Avançar_item == '=') Tipo_VALOR = 312;
                    if (Tipo_VALOR >= 300) número++;
                }
            }
            if (token_CONT_NÚM == token_Tipo.length - 1) { falha_VALOR("too many tokens (2047 maximum)"); break; }
            token_Tipo[token_CONT_NÚM] = Tipo_VALOR; token_cargo[token_CONT_NÚM] = iniciar; token_duração[token_CONT_NÚM++] = número - iniciar;
        }
    }
    static void gravar_constante_byte(int VALOR) {
        if (constante_dimensionar == constante_VALOR.length) { falha_VALOR("constant pool too large"); return; }
        constante_VALOR[constante_dimensionar++] = VALOR & 255;
    }
    static void 상짧(int VALOR) { gravar_constante_byte(VALOR >> 8); gravar_constante_byte(VALOR); }
    static int registro_constante(int iniciar) {
        for (int número = 1; número < constante_CONT_NÚM; número++) {
            int câmera_frontal_VALOR = constante_DESLOC[número], duração_VALOR = (número + 1 < constante_CONT_NÚM ? constante_DESLOC[número + 1] : iniciar) - câmera_frontal_VALOR;
            if (duração_VALOR != constante_dimensionar - iniciar) continue;
            boolean 같음 = true;
            for (int slot_entrada = 0; slot_entrada < duração_VALOR; slot_entrada++) if (constante_VALOR[câmera_frontal_VALOR + slot_entrada] != constante_VALOR[iniciar + slot_entrada]) 같음 = false;
            if (같음) { constante_dimensionar = iniciar; return número; }
        }
        if (constante_CONT_NÚM == constante_DESLOC.length) { falha_VALOR("too many constants"); return 0; }
        constante_DESLOC[constante_CONT_NÚM] = iniciar;
        return constante_CONT_NÚM++;
    }
    static void Acrescentar_SMS(int VALOR) {
        if (caractere_duração == 문자.length) { falha_VALOR("text too long"); return; }
        문자[caractere_duração++] = VALOR;
    }
    static void Acrescentar_Word(String Word_SMS) { for (int número = 0; número < Word_SMS.length(); número++) Acrescentar_SMS(Word_SMS.charAt(número)); }
    static int caractere_constante() {
        int iniciar = constante_dimensionar; gravar_constante_byte(1); 상짧(0);
        for (int número = 0; número < caractere_duração; número++) {
            int VALOR = 문자[número];
            if (VALOR > 0 && VALOR < 128) gravar_constante_byte(VALOR);
            else if (VALOR < 2048) { gravar_constante_byte(192 | VALOR >> 6); gravar_constante_byte(128 | VALOR & 63); }
            else { gravar_constante_byte(224 | VALOR >> 12); gravar_constante_byte(128 | VALOR >> 6 & 63); gravar_constante_byte(128 | VALOR & 63); }
        }
        if (erro) return 0;
        int duração_VALOR = constante_dimensionar - iniciar - 3;
        constante_VALOR[iniciar + 1] = duração_VALOR >> 8; constante_VALOR[iniciar + 2] = duração_VALOR & 255;
        return registro_constante(iniciar);
    }
    static int Word_constante(String Word_SMS) { caractere_duração = 0; Acrescentar_Word(Word_SMS); return caractere_constante(); }
    static int token_constante(int token_VALOR) {
        caractere_duração = 0;
        for (int número = 0; número < token_duração[token_VALOR]; número++) Acrescentar_SMS(códigoFonte[token_cargo[token_VALOR] + número]);
        return caractere_constante();
    }
    static int Referência(int Tipo_VALOR, int 가, int SEGUNDO_operando) {
        int iniciar = constante_dimensionar; gravar_constante_byte(Tipo_VALOR); 상짧(가);
        if (Tipo_VALOR == 9 || Tipo_VALOR == 10 || Tipo_VALOR == 12) 상짧(SEGUNDO_operando);
        return registro_constante(iniciar);
    }
    static int externo_Referência(int Tipo_VALOR, String proprietário_VALOR, String Nome, String 서술) {
        int proprietário_identificador = Referência(7, Word_constante(proprietário_VALOR), 0);
        int nome_CONT_NÚM = Word_constante(Nome), formato_CONT_NÚM = Word_constante(서술);
        return Referência(Tipo_VALOR, proprietário_identificador, Referência(12, nome_CONT_NÚM, formato_CONT_NÚM));
    }
    static void 내보내기(int VALOR) {
        if (CÓDIGO_dimensionar == valor_do_código.length) { falha_VALOR("bytecode too large"); return; }
        valor_do_código[CÓDIGO_dimensionar++] = VALOR & 255;
    }
    static void comando(int VALOR, int argumentos) { 내보내기(VALOR); 내보내기(argumentos >> 8); 내보내기(argumentos); }
    static void 수상수(int VALOR) {
        if (VALOR >= -1 && VALOR <= 5) { 내보내기(VALOR + 3); return; }
        int iniciar = constante_dimensionar; gravar_constante_byte(3); 상짧(VALOR >>> 16); 상짧(VALOR);
        comando(19, registro_constante(iniciar));
    }
    static int branch(int comando) { int resultado = CÓDIGO_dimensionar; comando(comando, 0); return resultado; }
    static void Link_VALOR(int branch, int alvo_objeto) {
        if (erro) return;
        int 거리 = alvo_objeto - branch;
        if (거리 < -32768 || 거리 > 32767 || branch < 0 || branch + 2 >= CÓDIGO_dimensionar) { falha_VALOR("invalid branch"); return; }
        valor_do_código[branch + 1] = 거리 >> 8 & 255; valor_do_código[branch + 2] = 거리 & 255;
    }
    static void Comparação_VALOR(int comando) {
        int VERDADEIRO_VALOR = branch(comando); 내보내기(3); int 끝 = branch(167);
        Link_VALOR(VERDADEIRO_VALOR, CÓDIGO_dimensionar); 내보내기(4); Link_VALOR(끝, CÓDIGO_dimensionar);
    }
    static int formato_VALOR() {
        if (PEGAR_Word("void")) return 0;
        if (PEGAR_Word("int")) return 1;
        if (PEGAR_Word("boolean")) return 2;
        if (PEGAR_Word("char")) return 5;
        if (PEGAR_Word("FileInputStream")) return 6;
        if (PEGAR_Word("FileOutputStream")) return 7;
        if (PEGAR_Word("String")) { if (receber('[')) { requisito_VALOR(']'); return 4; } return 3; }
        falha_VALOR("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Adicionar_formato(int TIPO_VALOR) {
        if (TIPO_VALOR == 0) Acrescentar_SMS('V');
        if (TIPO_VALOR == 1) Acrescentar_SMS('I');
        if (TIPO_VALOR == 2) Acrescentar_SMS('Z');
        if (TIPO_VALOR == 3) Acrescentar_Word("Ljava/lang/String;");
        if (TIPO_VALOR == 4) Acrescentar_Word("[Ljava/lang/String;");
        if (TIPO_VALOR == 5) Acrescentar_SMS('C');
        if (TIPO_VALOR == 6) Acrescentar_Word("Ljava/io/FileInputStream;");
        if (TIPO_VALOR == 7) Acrescentar_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws declaração. exceção Processo_VALOR_entrada 본문은 host javac를 사용한다.
    static void leitura_exceção_nome() {
        boolean 한국어묶음 = PEGAR_Word("Português");
        if (한국어묶음) { requisito_VALOR('.'); 말요구("nativo"); requisito_VALOR('.'); }
        if (!한국어묶음 && (PEGAR_Word("Exception") || PEGAR_Word("IOException"))) return;
        if (PEGAR_Word("exceção") || PEGAR_Word("execução_exceção") || PEGAR_Word("E_S_exceção") || PEGAR_Word("aguarde_TEMPOLIMITE_exceção") || PEGAR_Word("email_PROC_exceção") || PEGAR_Word("파일없음예외") || PEGAR_Word("comunicação_exceção") || PEGAR_Word("inválido_argumento_exceção") || PEGAR_Word("número_formato_falha") || PEGAR_Word("범위예외") || PEGAR_Word("limites_da_matriz_exceção") || PEGAR_Word("문자열범위예외") || PEGAR_Word("referência_nula_exceção") || PEGAR_Word("산술예외") || PEGAR_Word("Estado_exceção") || PEGAR_Word("TIPO_coerção_exceção") || PEGAR_Word("negativo_MATRIZ_dimensionar_falha") || PEGAR_Word("MATRIZ_Store_falha") || PEGAR_Word("thread_Estado_exceção") || PEGAR_Word("대기중단예외")) return;
        falha_VALOR("unsupported throws type");
    }
    static void leitura_declaração() {
        while (PEGAR_Word("import")) {
            if (Word_VALOR(posição, "Português")) leitura_exceção_nome();
            else {
                말요구("java"); requisito_VALOR('.'); 말요구("io"); requisito_VALOR('.');
                if (!(PEGAR_Word("FileInputStream") || PEGAR_Word("FileOutputStream") || PEGAR_Word("IOException"))) falha_VALOR("unsupported import");
            }
            requisito_VALOR(';');
        }
        PEGAR_Word("public"); PEGAR_Word("final"); 말요구("class"); aula_token = identificador_VALOR();
        aula_constante = Referência(7, token_constante(aula_token), 0);
        pai_constante = Referência(7, Word_constante("java/lang/Object"), 0); CÓDIGO_constante = Word_constante("Code"); requisito_VALOR('{');
        while (!erro && Tipo_VALOR() != '}') {
            if (método_CONT_NÚM == 32) { falha_VALOR("too many methods"); break; }
            int acesso_entrada = PEGAR_Word("public") ? 1 : PEGAR_Word("private") ? 2 : 0; 말요구("static");
            int FUNÇÃO_VALOR = método_CONT_NÚM++;
            método_acesso[FUNÇÃO_VALOR] = acesso_entrada | 8;
            método_devolver[FUNÇÃO_VALOR] = formato_VALOR(); método_entrada_nome[FUNÇÃO_VALOR] = identificador_VALOR(); requisito_VALOR('(');
            for (int câmera_frontal_VALOR = 0; câmera_frontal_VALOR < FUNÇÃO_VALOR; câmera_frontal_VALOR++) if (이름같음(método_entrada_nome[câmera_frontal_VALOR], método_entrada_nome[FUNÇÃO_VALOR])) falha_VALOR("duplicate method (overloading unsupported)");
            while (!erro && Tipo_VALOR() != ')') {
                int número = método_argumento_CONT_NÚM[FUNÇÃO_VALOR];
                if (número == 16) { falha_VALOR("too many parameters"); break; }
                int TIPO_VALOR = formato_VALOR(); if (TIPO_VALOR == 0) falha_VALOR("void parameter");
                método_argumento_TIPO[FUNÇÃO_VALOR * 16 + número] = TIPO_VALOR; método_argumento_nome[FUNÇÃO_VALOR * 16 + número] = identificador_VALOR();
                método_argumento_CONT_NÚM[FUNÇÃO_VALOR]++;
                if (!receber(',')) break;
            }
            requisito_VALOR(')');
            if (PEGAR_Word("throws")) {
                do { leitura_exceção_nome(); } while (!erro && receber(','));
            }
            corpo_do_método[FUNÇÃO_VALOR] = posição; requisito_VALOR('{');
            int aninhamento_VALOR = 1;
            while (posição < token_CONT_NÚM && aninhamento_VALOR > 0) {
                if (Tipo_VALOR() == '{') aninhamento_VALOR++;
                if (Tipo_VALOR() == '}') aninhamento_VALOR--;
                posição++;
            }
            if (aninhamento_VALOR != 0) falha_VALOR("unclosed method body");
            método_encerrar[FUNÇÃO_VALOR] = posição;
            método_nome_constante[FUNÇÃO_VALOR] = token_constante(método_entrada_nome[FUNÇÃO_VALOR]);
            caractere_duração = 0; Acrescentar_SMS('(');
            for (int número = 0; número < método_argumento_CONT_NÚM[FUNÇÃO_VALOR]; número++) Adicionar_formato(método_argumento_TIPO[FUNÇÃO_VALOR * 16 + número]);
            Acrescentar_SMS(')'); Adicionar_formato(método_devolver[FUNÇÃO_VALOR]); método_descritor_constante[FUNÇÃO_VALOR] = caractere_constante();
        }
        requisito_VALOR('}'); if (posição != token_CONT_NÚM) falha_VALOR("extra input after class");
    }
    static int PROCURAR_local(int Nome) {
        for (int número = local_CONT_NÚM - 1; número >= 0; número--) if (지역깊이[número] >= 0 && 이름같음(local_nome[número], Nome)) return número;
        falha_VALOR("unknown variable"); return 0;
    }
    static int Adicionar_local(int Nome, int TIPO_VALOR) {
        for (int número = 0; número < local_CONT_NÚM; número++) if (지역깊이[número] >= 0 && 이름같음(local_nome[número], Nome)) falha_VALOR("duplicate local variable");
        if (local_CONT_NÚM == 128) { falha_VALOR("too many locals"); return 0; }
        local_nome[local_CONT_NÚM] = Nome; local_TIPO[local_CONT_NÚM] = TIPO_VALOR; 지역깊이[local_CONT_NÚM] = 깊이;
        return local_CONT_NÚM++;
    }
    static boolean inteiro_TIPO(int TIPO_VALOR) { return TIPO_VALOR == 1 || TIPO_VALOR == 5; }
    static void leitura_local(int número) { 내보내기(local_TIPO[número] <= 2 || local_TIPO[número] == 5 ? 21 : 25); 내보내기(número); }
    static void gravar_local(int número) { 내보내기(local_TIPO[número] <= 2 || local_TIPO[número] == 5 ? 54 : 58); 내보내기(número); }
    static void verificar_TIPO(int real_dados, int 기대) { if (real_dados != 기대 && !(real_dados == 5 && 기대 == 1)) falha_VALOR("type mismatch"); }
    static void leitura_caractere_VALOR(int token_VALOR) {
        caractere_duração = 0; int iniciar = token_cargo[token_VALOR] + 1, 끝 = token_cargo[token_VALOR] + token_duração[token_VALOR] - 1;
        while (iniciar < 끝 && !erro) {
            int VALOR = códigoFonte[iniciar++];
            if (VALOR == '\\') {
                if (iniciar == 끝) { falha_VALOR("invalid escape"); break; }
                VALOR = códigoFonte[iniciar++];
                if (VALOR == 'n') VALOR = 10;
                else if (VALOR == 'r') VALOR = 13;
                else if (VALOR == 't') VALOR = 9;
                else if (VALOR == 'b') VALOR = 8;
                else if (VALOR == 'f') VALOR = 12;
                else if (VALOR != '\\' && VALOR != '"' && VALOR != '\'') falha_VALOR("unsupported escape");
            }
            Acrescentar_SMS(VALOR);
        }
    }
    static int analisar_inteiro(int token_VALOR, boolean negativo_VALOR) {
        if (token_duração[token_VALOR] > 1 && códigoFonte[token_cargo[token_VALOR]] == '0') falha_VALOR("octal literals unsupported");
        int VALOR = 0;
        for (int número = 0; número < token_duração[token_VALOR]; número++) {
            int dígito_item = códigoFonte[token_cargo[token_VALOR] + número] - '0';
            if (VALOR < -214748364 || VALOR == -214748364 && dígito_item > (negativo_VALOR ? 8 : 7)) falha_VALOR("integer literal out of range");
            VALOR = VALOR * 10 - dígito_item;
        }
        return negativo_VALOR ? VALOR : -VALOR;
    }
    static int 기본식() {
        if (PEGAR_Word("new")) {
            int TIPO_VALOR = formato_VALOR();
            if (TIPO_VALOR != 6 && TIPO_VALOR != 7) { falha_VALOR("only file streams supported by new in source"); return 0; }
            String proprietário_VALOR = TIPO_VALOR == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            comando(187, Referência(7, Word_constante(proprietário_VALOR), 0)); 내보내기(89);
            requisito_VALOR('('); verificar_TIPO(expressão_VALOR(), 3); boolean 이어 = false;
            if (receber(',')) { if (TIPO_VALOR != 7) falha_VALOR("input stream constructor arguments"); verificar_TIPO(expressão_VALOR(), 2); 이어 = true; }
            requisito_VALOR(')');
            comando(183, externo_Referência(10, proprietário_VALOR, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TIPO_VALOR;
        }
        if (receber('(')) { int TIPO_VALOR = expressão_VALOR(); requisito_VALOR(')'); return TIPO_VALOR; }
        if (Tipo_VALOR() == 257) { 수상수(analisar_inteiro(posição++, false)); return 1; }
        if (Tipo_VALOR() == 258) { leitura_caractere_VALOR(posição++); comando(19, Referência(8, caractere_constante(), 0)); return 3; }
        if (Tipo_VALOR() == 259) { leitura_caractere_VALOR(posição++); if (caractere_duração != 1) falha_VALOR("character literal length"); 수상수(문자[0]); return 5; }
        if (PEGAR_Word("true")) { 내보내기(4); return 2; }
        if (PEGAR_Word("false")) { 내보내기(3); return 2; }
        if (PEGAR_Word("Português")) {
            requisito_VALOR('.'); 말요구("nativo"); requisito_VALOR('.');
            String proprietário_VALOR = "", método_VALOR = "", 서술 = ""; int 가 = 0, SEGUNDO_operando = 0, 다 = 0, 라 = 0, 마 = 0, resultado = 0;
            if (PEGAR_Word("saídaTexto")) {
                proprietário_VALOR = "Português/nativo/saídaTexto"; requisito_VALOR('.');
                if (PEGAR_Word("gravar_linha")) { método_VALOR = "gravar_linha"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (PEGAR_Word("Escrita")) { método_VALOR = "Escrita"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (PEGAR_Word("gravar_número")) { método_VALOR = "gravar_número"; 서술 = "(I)V"; 가 = 1; }
                else falha_VALOR("unknown Korean output method");
            } else if (PEGAR_Word("문자")) {
                proprietário_VALOR = "Português/nativo/문자"; requisito_VALOR('.'); 가 = 3;
                if (PEGAR_Word("duração_VALOR")) { método_VALOR = "duração_VALOR"; 서술 = "(Ljava/lang/String;)I"; resultado = 1; }
                else if (PEGAR_Word("ponto_de_código_CONT_NÚM")) { método_VALOR = "ponto_de_código_CONT_NÚM"; 서술 = "(Ljava/lang/String;)I"; resultado = 1; }
                else if (PEGAR_Word("analisar_inteiro")) { método_VALOR = "analisar_inteiro"; 서술 = "(Ljava/lang/String;)I"; resultado = 1; }
                else if (PEGAR_Word("gravar_inteiro_VALOR")) { método_VALOR = "gravar_inteiro_VALOR"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; resultado = 3; }
                else if (PEGAR_Word("같음")) { método_VALOR = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SEGUNDO_operando = 3; resultado = 2; }
                else if (PEGAR_Word("colar_SMS")) { método_VALOR = "colar_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SEGUNDO_operando = 3; resultado = 3; }
                else if (PEGAR_Word("cortar_VALOR")) { método_VALOR = "cortar_VALOR"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SEGUNDO_operando = 1; 다 = 1; resultado = 3; }
                else falha_VALOR("unknown Korean text method");
            } else if (PEGAR_Word("ficheiro")) {
                proprietário_VALOR = "Português/nativo/ficheiro"; requisito_VALOR('.'); 가 = 3;
                if (PEGAR_Word("Leitura")) { método_VALOR = "Leitura"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; resultado = 3; }
                else if (PEGAR_Word("Escrita")) { método_VALOR = "Escrita"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SEGUNDO_operando = 3; }
                else falha_VALOR("unknown Korean file method");
            } else if (PEGAR_Word("tela")) {
                proprietário_VALOR = "Português/nativo/tela"; requisito_VALOR('.');
                if (PEGAR_Word("너비")) { método_VALOR = "너비"; 서술 = "()I"; resultado = 1; }
                else if (PEGAR_Word("altura_VALOR")) { método_VALOR = "altura_VALOR"; 서술 = "()I"; resultado = 1; }
                else if (PEGAR_Word("retângulo")) { método_VALOR = "retângulo"; 서술 = "(IIIII)V"; 가 = 1; SEGUNDO_operando = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (PEGAR_Word("apagar_entrada")) { método_VALOR = "apagar_entrada"; 서술 = "(I)V"; 가 = 1; }
                else if (PEGAR_Word("기다리기")) { método_VALOR = "기다리기"; 서술 = "()V"; }
                else falha_VALOR("unknown Korean framebuffer method");
            } else falha_VALOR("unsupported Korean library class");
            requisito_VALOR('('); if (가 != 0) verificar_TIPO(expressão_VALOR(), 가);
            if (SEGUNDO_operando != 0) { requisito_VALOR(','); verificar_TIPO(expressão_VALOR(), SEGUNDO_operando); }
            if (다 != 0) { requisito_VALOR(','); verificar_TIPO(expressão_VALOR(), 다); }
            if (라 != 0) { requisito_VALOR(','); verificar_TIPO(expressão_VALOR(), 라); }
            if (마 != 0) { requisito_VALOR(','); verificar_TIPO(expressão_VALOR(), 마); }
            requisito_VALOR(')'); comando(184, externo_Referência(10, proprietário_VALOR, método_VALOR, 서술)); return resultado;
        }
        if (PEGAR_Word("Integer")) {
            requisito_VALOR('.'); 말요구("parseInt"); requisito_VALOR('('); verificar_TIPO(expressão_VALOR(), 3); requisito_VALOR(')');
            comando(184, externo_Referência(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nome = identificador_VALOR();
        if (receber('(')) {
            int FUNÇÃO_VALOR = -1;
            for (int número = 0; número < método_CONT_NÚM; número++) if (이름같음(Nome, método_entrada_nome[número])) FUNÇÃO_VALOR = número;
            if (FUNÇÃO_VALOR < 0) { falha_VALOR("unknown static method"); return 0; }
            int número = 0;
            while (!erro && Tipo_VALOR() != ')') {
                if (número >= método_argumento_CONT_NÚM[FUNÇÃO_VALOR]) { falha_VALOR("too many arguments"); break; }
                verificar_TIPO(expressão_VALOR(), método_argumento_TIPO[FUNÇÃO_VALOR * 16 + número++]); if (!receber(',')) break;
            }
            requisito_VALOR(')'); if (número != método_argumento_CONT_NÚM[FUNÇÃO_VALOR]) falha_VALOR("argument count mismatch");
            comando(184, Referência(10, aula_constante, Referência(12, método_nome_constante[FUNÇÃO_VALOR], método_descritor_constante[FUNÇÃO_VALOR])));
            return método_devolver[FUNÇÃO_VALOR];
        }
        int local_Scope = PROCURAR_local(Nome), TIPO_VALOR = local_TIPO[local_Scope]; leitura_local(local_Scope);
        while (!erro) {
            if (receber('[')) { verificar_TIPO(TIPO_VALOR, 4); verificar_TIPO(expressão_VALOR(), 1); requisito_VALOR(']'); 내보내기(50); TIPO_VALOR = 3; }
            else if (receber('.')) {
                if (TIPO_VALOR == 6 || TIPO_VALOR == 7) {
                    String proprietário_VALOR = TIPO_VALOR == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (PEGAR_Word("close")) { requisito_VALOR('('); requisito_VALOR(')'); comando(182, externo_Referência(10, proprietário_VALOR, "close", "()V")); TIPO_VALOR = 0; }
                    else if (TIPO_VALOR == 6 && PEGAR_Word("read")) { requisito_VALOR('('); requisito_VALOR(')'); comando(182, externo_Referência(10, proprietário_VALOR, "read", "()I")); TIPO_VALOR = 1; }
                    else if (TIPO_VALOR == 7 && PEGAR_Word("write")) { requisito_VALOR('('); verificar_TIPO(expressão_VALOR(), 1); requisito_VALOR(')'); comando(182, externo_Referência(10, proprietário_VALOR, "write", "(I)V")); TIPO_VALOR = 0; }
                    else { falha_VALOR("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TIPO_VALOR == 4) { 내보내기(190); TIPO_VALOR = 1; }
                else { verificar_TIPO(TIPO_VALOR, 3); requisito_VALOR('('); requisito_VALOR(')'); comando(182, externo_Referência(10, "java/lang/String", "length", "()I")); TIPO_VALOR = 1; }
            } else break;
        }
        return TIPO_VALOR;
    }
    static int 단항() {
        if (++식깊이 > 64) { falha_VALOR("expression nesting too deep"); 식깊이--; return 0; }
        int TIPO_VALOR;
        if (receber('!')) { verificar_TIPO(단항(), 2); Comparação_VALOR(153); TIPO_VALOR = 2; }
        else if (receber('-')) {
            if (Tipo_VALOR() == 257) 수상수(analisar_inteiro(posição++, true));
            else { verificar_TIPO(단항(), 1); 내보내기(116); }
            TIPO_VALOR = 1;
        } else if (receber('+')) { verificar_TIPO(단항(), 1); TIPO_VALOR = 1; }
        else TIPO_VALOR = 기본식();
        식깊이--; return TIPO_VALOR;
    }
    static int 곱식() {
        int TIPO_VALOR = 단항();
        while (!erro && (Tipo_VALOR() == '*' || Tipo_VALOR() == '/' || Tipo_VALOR() == '%')) {
            int Codificação_VALOR = Tipo_VALOR(); posição++; verificar_TIPO(TIPO_VALOR, 1); verificar_TIPO(단항(), 1);
            내보내기(Codificação_VALOR == '*' ? 104 : Codificação_VALOR == '/' ? 108 : 112); TIPO_VALOR = 1;
        }
        return TIPO_VALOR;
    }
    static int 합식() {
        int TIPO_VALOR = 곱식();
        while (!erro && (Tipo_VALOR() == '+' || Tipo_VALOR() == '-')) {
            int Codificação_VALOR = Tipo_VALOR(); posição++; int limite_VALOR = CÓDIGO_dimensionar, BACK_tipo_de_valor = 곱식();
            if (Codificação_VALOR == '+' && (TIPO_VALOR == 3 || BACK_tipo_de_valor == 3)) { 결합(limite_VALOR, TIPO_VALOR, BACK_tipo_de_valor); TIPO_VALOR = 3; }
            else { verificar_TIPO(TIPO_VALOR, 1); verificar_TIPO(BACK_tipo_de_valor, 1); 내보내기(Codificação_VALOR == '+' ? 96 : 100); TIPO_VALOR = 1; }
        }
        return TIPO_VALOR;
    }
    static int conectado_Referência(int TIPO_VALOR) {
        if (TIPO_VALOR != 1 && TIPO_VALOR != 2 && TIPO_VALOR != 3 && TIPO_VALOR != 5) falha_VALOR("unsupported concatenation type");
        return externo_Referência(10, "java/lang/StringBuilder", "append", TIPO_VALOR == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TIPO_VALOR == 2 ? "(Z)Ljava/lang/StringBuilder;" : TIPO_VALOR == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int limite_VALOR, int câmera_frontal_tipo_de_valor, int BACK_tipo_de_valor) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 DIREITA valor_do_código 앞에 gerar 코드를 삽입한다.
        // DIREITA expressão_VALOR 내부의 par_VALOR branch 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CÓDIGO_dimensionar;
        comando(187, Referência(7, Word_constante("java/lang/StringBuilder"), 0)); 내보내기(89);
        comando(183, externo_Referência(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); comando(182, conectado_Referência(câmera_frontal_tipo_de_valor));
        if (erro) return;
        int duração_VALOR = CÓDIGO_dimensionar - 끝;
        for (int número = 0; número < duração_VALOR; número++) 삽입코드[número] = valor_do_código[끝 + número];
        for (int número = 끝 - 1; número >= limite_VALOR; número--) valor_do_código[número + duração_VALOR] = valor_do_código[número];
        for (int número = 0; número < duração_VALOR; número++) valor_do_código[limite_VALOR + número] = 삽입코드[número];
        comando(182, conectado_Referência(BACK_tipo_de_valor)); comando(182, externo_Referência(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Comparação_expressão() {
        int TIPO_VALOR = 합식();
        while (!erro && (Tipo_VALOR() == '<' || Tipo_VALOR() == '>' || Tipo_VALOR() == 302 || Tipo_VALOR() == 303)) {
            int Codificação_VALOR = Tipo_VALOR(); posição++; verificar_TIPO(TIPO_VALOR, 1); verificar_TIPO(합식(), 1);
            Comparação_VALOR(Codificação_VALOR == '<' ? 161 : Codificação_VALOR == '>' ? 163 : Codificação_VALOR == 302 ? 164 : 162); TIPO_VALOR = 2;
        }
        return TIPO_VALOR;
    }
    static int 동등식() {
        int TIPO_VALOR = Comparação_expressão();
        while (!erro && (Tipo_VALOR() == 300 || Tipo_VALOR() == 301)) {
            int Codificação_VALOR = Tipo_VALOR(); posição++; int BACK_tipo_de_valor = Comparação_expressão();
            if (TIPO_VALOR == 0 || BACK_tipo_de_valor == 0) falha_VALOR("void expression");
            if (!(inteiro_TIPO(TIPO_VALOR) && inteiro_TIPO(BACK_tipo_de_valor))) verificar_TIPO(BACK_tipo_de_valor, TIPO_VALOR);
            Comparação_VALOR((TIPO_VALOR <= 2 || TIPO_VALOR == 5 ? 159 : 165) + (Codificação_VALOR == 301 ? 1 : 0)); TIPO_VALOR = 2;
        }
        return TIPO_VALOR;
    }
    static int AND() {
        int TIPO_VALOR = 동등식();
        while (!erro && receber(304)) {
            verificar_TIPO(TIPO_VALOR, 2); int 가 = branch(153); verificar_TIPO(동등식(), 2); int SEGUNDO_operando = branch(153);
            내보내기(4); int 끝 = branch(167); Link_VALOR(가, CÓDIGO_dimensionar); Link_VALOR(SEGUNDO_operando, CÓDIGO_dimensionar); 내보내기(3); Link_VALOR(끝, CÓDIGO_dimensionar); TIPO_VALOR = 2;
        }
        return TIPO_VALOR;
    }
    static int expressão_VALOR() {
        int TIPO_VALOR = AND();
        while (!erro && receber(305)) {
            verificar_TIPO(TIPO_VALOR, 2); int 가 = branch(154); verificar_TIPO(AND(), 2); int SEGUNDO_operando = branch(154);
            내보내기(3); int 끝 = branch(167); Link_VALOR(가, CÓDIGO_dimensionar); Link_VALOR(SEGUNDO_operando, CÓDIGO_dimensionar); 내보내기(4); Link_VALOR(끝, CÓDIGO_dimensionar); TIPO_VALOR = 2;
        }
        return TIPO_VALOR;
    }
    static void tarefa_VALOR(boolean Permitir_declaração) {
        if (Word_VALOR(posição, "int") || Word_VALOR(posição, "boolean") || Word_VALOR(posição, "String") || Word_VALOR(posição, "char")
            || Word_VALOR(posição, "FileInputStream") || Word_VALOR(posição, "FileOutputStream")) {
            if (!Permitir_declaração) falha_VALOR("declaration not allowed here");
            int TIPO_VALOR = formato_VALOR(), Nome = identificador_VALOR(); requisito_VALOR('='); verificar_TIPO(expressão_VALOR(), TIPO_VALOR);
            gravar_local(Adicionar_local(Nome, TIPO_VALOR)); return;
        }
        int Nome = identificador_VALOR(), local_Scope = PROCURAR_local(Nome);
        if (receber('=')) { verificar_TIPO(expressão_VALOR(), local_TIPO[local_Scope]); gravar_local(local_Scope); }
        else if (Tipo_VALOR() >= 308 && Tipo_VALOR() <= 312) {
            int Codificação_VALOR = Tipo_VALOR(); posição++; leitura_local(local_Scope); int limite_VALOR = CÓDIGO_dimensionar, BACK_tipo_de_valor = expressão_VALOR();
            if (Codificação_VALOR == 308 && local_TIPO[local_Scope] == 3) 결합(limite_VALOR, 3, BACK_tipo_de_valor);
            else {
                verificar_TIPO(local_TIPO[local_Scope], 1); verificar_TIPO(BACK_tipo_de_valor, 1);
                내보내기(Codificação_VALOR == 308 ? 96 : Codificação_VALOR == 309 ? 100 : Codificação_VALOR == 310 ? 104 : Codificação_VALOR == 311 ? 108 : 112);
                if (local_TIPO[local_Scope] == 5) 내보내기(146);
            }
            gravar_local(local_Scope);
        }
        else if (Tipo_VALOR() == 306 || Tipo_VALOR() == 307) {
            verificar_TIPO(local_TIPO[local_Scope], 1); 내보내기(132); 내보내기(local_Scope); 내보내기(Tipo_VALOR() == 306 ? 1 : 255); posição++;
            if (local_TIPO[local_Scope] == 5) { leitura_local(local_Scope); 내보내기(146); gravar_local(local_Scope); }
        } else falha_VALOR("assignment or postfix increment required");
    }
    static void tela_saída() {
        말요구("System"); requisito_VALOR('.'); 말요구("out"); requisito_VALOR('.');
        boolean 줄바꿈 = PEGAR_Word("println"); if (!줄바꿈) 말요구("print"); requisito_VALOR('(');
        comando(178, externo_Referência(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean vazio_argumento = Tipo_VALOR() == ')';
        int TIPO_VALOR = vazio_argumento ? 0 : expressão_VALOR(); requisito_VALOR(')'); requisito_VALOR(';');
        String 서술 = TIPO_VALOR == 0 ? "()V" : TIPO_VALOR == 1 ? "(I)V" : TIPO_VALOR == 2 ? "(Z)V" : TIPO_VALOR == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TIPO_VALOR == 4 || TIPO_VALOR >= 6 || TIPO_VALOR == 0 && (!줄바꿈 || !vazio_argumento)) falha_VALOR("unsupported print argument");
        comando(182, externo_Referência(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean instrução_VALOR() {
        if (erro) return false;
        if (깊이 > 32) { falha_VALOR("statement nesting too deep"); return false; }
        if (receber('{')) {
            깊이++; boolean devolver_RC = false;
            while (!erro && Tipo_VALOR() != '}') { if (devolver_RC) falha_VALOR("unreachable statement"); devolver_RC = instrução_VALOR(); }
            requisito_VALOR('}'); for (int número = 0; número < local_CONT_NÚM; número++) if (지역깊이[número] == 깊이) 지역깊이[número] = -1;
            깊이--; return devolver_RC;
        }
        if (receber(';')) return false;
        if (PEGAR_Word("return")) {
            int TIPO_VALOR = Tipo_VALOR() == ';' ? 0 : expressão_VALOR(); verificar_TIPO(TIPO_VALOR, método_devolver[em_dia_método]); requisito_VALOR(';');
            내보내기(TIPO_VALOR == 0 ? 177 : TIPO_VALOR <= 2 || TIPO_VALOR == 5 ? 172 : 176); return true;
        }
        if (PEGAR_Word("if")) {
            requisito_VALOR('('); verificar_TIPO(expressão_VALOR(), 2); requisito_VALOR(')'); int FALSO_VALOR = branch(153);
            깊이++; boolean 가 = visual_instrução(); 깊이--;
            if (PEGAR_Word("else")) { int 끝 = branch(167); Link_VALOR(FALSO_VALOR, CÓDIGO_dimensionar); 깊이++; boolean SEGUNDO_operando = visual_instrução(); 깊이--; Link_VALOR(끝, CÓDIGO_dimensionar); return 가 && SEGUNDO_operando; }
            Link_VALOR(FALSO_VALOR, CÓDIGO_dimensionar); return false;
        }
        if (PEGAR_Word("while")) {
            int iniciar = CÓDIGO_dimensionar; requisito_VALOR('('); verificar_TIPO(expressão_VALOR(), 2); requisito_VALOR(')'); int 끝 = branch(153);
            깊이++; visual_instrução(); 깊이--; Link_VALOR(branch(167), iniciar); Link_VALOR(끝, CÓDIGO_dimensionar); return false;
        }
        if (PEGAR_Word("for")) {
            깊이++; requisito_VALOR('('); if (Tipo_VALOR() != ';') tarefa_VALOR(true); requisito_VALOR(';');
            int doença = CÓDIGO_dimensionar; if (Tipo_VALOR() == ';') 내보내기(4); else verificar_TIPO(expressão_VALOR(), 2); requisito_VALOR(';');
            int 끝 = branch(153), corpo_de_texto = branch(167), renovar = CÓDIGO_dimensionar;
            if (Tipo_VALOR() != ')') tarefa_VALOR(false); requisito_VALOR(')'); Link_VALOR(branch(167), doença); Link_VALOR(corpo_de_texto, CÓDIGO_dimensionar);
            visual_instrução(); Link_VALOR(branch(167), renovar); Link_VALOR(끝, CÓDIGO_dimensionar);
            for (int número = 0; número < local_CONT_NÚM; número++) if (지역깊이[número] == 깊이) 지역깊이[número] = -1;
            깊이--; return false;
        }
        if (Word_VALOR(posição, "System")) { tela_saída(); return false; }
        if (Tipo_VALOR() == 256 && posição + 1 < token_CONT_NÚM && (token_Tipo[posição + 1] == '(' || token_Tipo[posição + 1] == '.')) {
            int TIPO_VALOR = expressão_VALOR(); if (TIPO_VALOR != 0) 내보내기(87); requisito_VALOR(';'); return false;
        }
        tarefa_VALOR(true); requisito_VALOR(';'); return false;
    }
    static boolean visual_instrução() {
        if (Word_VALOR(posição, "int") || Word_VALOR(posição, "boolean") || Word_VALOR(posição, "char") || Word_VALOR(posição, "String")
            || Word_VALOR(posição, "FileInputStream") || Word_VALOR(posição, "FileOutputStream")) falha_VALOR("local declaration requires braces");
        return instrução_VALOR();
    }
    static void 출바(int VALOR) { if (saída_dimensionar == saídaTexto.length) falha_VALOR("class file too large"); else saídaTexto[saída_dimensionar++] = VALOR & 255; }
    static void 출짧(int VALOR) { 출바(VALOR >> 8); 출바(VALOR); }
    static void 출정(int VALOR) { 출짧(VALOR >>> 16); 출짧(VALOR); }
    static void gravar_aula() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(constante_CONT_NÚM);
        for (int número = 0; número < constante_dimensionar; número++) 출바(constante_VALOR[número]);
        출짧(0x21); 출짧(aula_constante); 출짧(pai_constante); 출짧(0); 출짧(0); 출짧(método_CONT_NÚM);
        for (int número = 0; número < método_CONT_NÚM; número++) {
            출짧(método_acesso[número]); 출짧(método_nome_constante[número]); 출짧(método_descritor_constante[número]); 출짧(1); 출짧(CÓDIGO_constante);
            출정(12 + método_duração[número]); 출짧(128); 출짧(함수지역[número]); 출정(método_duração[número]);
            for (int slot_entrada = 0; slot_entrada < método_duração[número]; slot_entrada++) 출바(valor_do_código[método_CÓDIGO[número] + slot_entrada]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int iniciar() {
        if (espaço_do_utilizador.인수개수() == 1 && FerramentasJava.같음(espaço_do_utilizador.argumentos(0), "-version")) {
            espaço_do_utilizador.Escrita("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (espaço_do_utilizador.인수개수() != 1) { espaço_do_utilizador.Escrita("Usage: javac FILE.java\n"); return 2; }
        int nome_dimensionar = FerramentasJava.Nome(nome_de_arquivo_SMS, espaço_do_utilizador.argumentos(0));
        if (nome_dimensionar < 6 || nome_dimensionar > 62 || nome_de_arquivo_SMS[nome_dimensionar - 5] != '.' || nome_de_arquivo_SMS[nome_dimensionar - 4] != 'j'
            || nome_de_arquivo_SMS[nome_dimensionar - 3] != 'a' || nome_de_arquivo_SMS[nome_dimensionar - 2] != 'v' || nome_de_arquivo_SMS[nome_dimensionar - 1] != 'a') {
            espaço_do_utilizador.Escrita("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        fonte_dimensionar = espaço_do_utilizador.leitura_Arquivo(nome_de_arquivo_SMS, códigoFonte);
        if (fonte_dimensionar < 0) { espaço_do_utilizador.Escrita("javac: cannot read source: "); FerramentasJava.gravar_número(fonte_dimensionar); espaço_do_utilizador.gravar_caractere_VALOR(10); return 1; }
        fonte_dimensionar = FerramentasJava.원문해독(códigoFonte, fonte_dimensionar);
        if (fonte_dimensionar < 0) { espaço_do_utilizador.Escrita("javac error: invalid UTF-8 source\n"); return 1; }
        cortar_VALOR(); if (!erro) leitura_declaração();
        if (!erro) {
            if (token_duração[aula_token] != nome_dimensionar - 5) falha_VALOR("class name must match file name");
            for (int número = 0; número < nome_dimensionar - 5; número++) if (códigoFonte[token_cargo[aula_token] + número] != nome_de_arquivo_SMS[número]) falha_VALOR("class name must match file name");
        }
        for (em_dia_método = 0; em_dia_método < método_CONT_NÚM && !erro; em_dia_método++) {
            posição = corpo_do_método[em_dia_método]; método_CÓDIGO[em_dia_método] = CÓDIGO_dimensionar; local_CONT_NÚM = 0; 깊이 = 0;
            for (int número = 0; número < método_argumento_CONT_NÚM[em_dia_método]; número++) Adicionar_local(método_argumento_nome[em_dia_método * 16 + número], método_argumento_TIPO[em_dia_método * 16 + número]);
            boolean devolver_RC = instrução_VALOR();
            if (!devolver_RC && método_devolver[em_dia_método] != 0) falha_VALOR("missing return");
            // branch 뒤의 합류 지점은 반드시 real_dados 명령이어야 한다 (버전 49 검증기).
            if (método_devolver[em_dia_método] == 0) 내보내기(177);
            else { boolean inteiro = método_devolver[em_dia_método] <= 2 || método_devolver[em_dia_método] == 5; 내보내기(inteiro ? 3 : 1); 내보내기(inteiro ? 172 : 176); }
            if (posição != método_encerrar[em_dia_método]) falha_VALOR("invalid method body");
            함수지역[em_dia_método] = local_CONT_NÚM; método_duração[em_dia_método] = CÓDIGO_dimensionar - método_CÓDIGO[em_dia_método];
        }
        if (erro) return 1;
        gravar_aula(); if (erro) return 1;
        nome_de_arquivo_SMS[nome_dimensionar - 4] = 'c'; nome_de_arquivo_SMS[nome_dimensionar - 3] = 'l'; nome_de_arquivo_SMS[nome_dimensionar - 2] = 'a';
        nome_de_arquivo_SMS[nome_dimensionar - 1] = 's'; nome_de_arquivo_SMS[nome_dimensionar] = 's'; nome_de_arquivo_SMS[nome_dimensionar + 1] = 0;
        int resultado = espaço_do_utilizador.gravar_Arquivo(nome_de_arquivo_SMS, saídaTexto, saída_dimensionar);
        if (resultado < 0) { espaço_do_utilizador.Escrita("javac: cannot save class: "); FerramentasJava.gravar_número(resultado); espaço_do_utilizador.gravar_caractere_VALOR(10); return 1; }
        espaço_do_utilizador.Escrita("Compiled: "); for (int número = 0; nome_de_arquivo_SMS[número] != 0; número++) espaço_do_utilizador.gravar_caractere_VALOR(nome_de_arquivo_SMS[número]);
        espaço_do_utilizador.Escrita(" (JVM class version 49)\n"); return 0;
    }
}
