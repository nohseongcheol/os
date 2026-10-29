// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interativo shell 문법. 파이프는 순차 Executar_comando, 환경은 같은 셸에서 공유한다. */
public final class shell_sintaxe {
    static int[] códigoFonte = new int[4 * 4096], Tipo_VALOR = new int[4 * 128], iniciar = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] variável_nome = new int[16 * 32], variável_dados = new int[16 * 256], 이름길이 = new int[16], VALOR_duração = new int[16];
    static int[] script_VALOR = new int[4 * 16384];
    static int Estado_VALOR, 깊이, 쓴수;
    static boolean 연결중, script_encerrar, extensão_erro;
    static boolean nome_caractere(int ponto_de_código) { return ponto_de_código >= 'a' && ponto_de_código <= 'z' || ponto_de_código >= 'A' && ponto_de_código <= 'Z' || ponto_de_código == '_' || ponto_de_código >= 128; }
    static boolean 이름뒤(int ponto_de_código) { return nome_caractere(ponto_de_código) || ponto_de_código >= '0' && ponto_de_código <= '9'; }
    static void erro(String texto) { Quadro.입출력전환(0); 단말.Escrita("comando analisar_VALOR: "); 단말.Escrita(texto); 단말.문자(10); Estado_VALOR = 2; }
    static int Leitura(int entrada_CONT_NÚM_8f7753a1, int 중첩깊이) {
        int em_dia_ÍNDICE = 0, total_CONT_NÚM = 0, BASE_cargo = 중첩깊이 * 4096, caractere_especial = 중첩깊이 * 128;
        while (em_dia_ÍNDICE < entrada_CONT_NÚM_8f7753a1) {
            while (em_dia_ÍNDICE < entrada_CONT_NÚM_8f7753a1 && (códigoFonte[BASE_cargo + em_dia_ÍNDICE] == 32 || códigoFonte[BASE_cargo + em_dia_ÍNDICE] == 9)) em_dia_ÍNDICE++;
            if (em_dia_ÍNDICE == entrada_CONT_NÚM_8f7753a1 || códigoFonte[BASE_cargo + em_dia_ÍNDICE] == '#') break;
            if (total_CONT_NÚM == 128) { erro("낱말이 너무 많습니다"); return -1; }
            int START_cargo = em_dia_ÍNDICE, ponto_de_código = códigoFonte[BASE_cargo + em_dia_ÍNDICE], dados_Tipo = 0;
            if (ponto_de_código == ';') { dados_Tipo = 1; em_dia_ÍNDICE++; }
            else if (ponto_de_código == '&') { if (em_dia_ÍNDICE + 1 >= entrada_CONT_NÚM_8f7753a1 || códigoFonte[BASE_cargo + em_dia_ÍNDICE + 1] != '&') { erro("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } dados_Tipo = 2; em_dia_ÍNDICE += 2; }
            else if (ponto_de_código == '|') { em_dia_ÍNDICE++; dados_Tipo = em_dia_ÍNDICE < entrada_CONT_NÚM_8f7753a1 && códigoFonte[BASE_cargo + em_dia_ÍNDICE] == '|' ? 3 : 4; if (dados_Tipo == 3) em_dia_ÍNDICE++; }
            else if (ponto_de_código == '>') { em_dia_ÍNDICE++; dados_Tipo = em_dia_ÍNDICE < entrada_CONT_NÚM_8f7753a1 && códigoFonte[BASE_cargo + em_dia_ÍNDICE] == '>' ? 6 : 5; if (dados_Tipo == 6) em_dia_ÍNDICE++; }
            else if (ponto_de_código == '<') { dados_Tipo = 7; em_dia_ÍNDICE++; }
            else {
                int Citação = 0;
                while (em_dia_ÍNDICE < entrada_CONT_NÚM_8f7753a1) {
                    ponto_de_código = códigoFonte[BASE_cargo + em_dia_ÍNDICE];
                    if (ponto_de_código == '`' && Citação != 39 || ponto_de_código == '$' && Citação != 39 && em_dia_ÍNDICE + 1 < entrada_CONT_NÚM_8f7753a1 && códigoFonte[BASE_cargo + em_dia_ÍNDICE + 1] == '(') { erro("comando resultado 치환은 지원하지 않습니다"); return -1; }
                    if (ponto_de_código == '\\' && Citação != 39) { if (++em_dia_ÍNDICE == entrada_CONT_NÚM_8f7753a1) { erro("linha_de_entrada 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } em_dia_ÍNDICE++; continue; }
                    if (ponto_de_código == Citação) { Citação = 0; em_dia_ÍNDICE++; continue; }
                    if (Citação == 0 && (ponto_de_código == 39 || ponto_de_código == 34)) { Citação = ponto_de_código; em_dia_ÍNDICE++; continue; }
                    if (Citação == 0 && (ponto_de_código == 32 || ponto_de_código == 9 || ponto_de_código == ';' || ponto_de_código == '&' || ponto_de_código == '|' || ponto_de_código == '<' || ponto_de_código == '>')) break;
                    em_dia_ÍNDICE++;
                }
                if (Citação != 0) { erro("따옴표가 닫히지 않았습니다"); return -1; }
                if (em_dia_ÍNDICE < entrada_CONT_NÚM_8f7753a1 && (códigoFonte[BASE_cargo + em_dia_ÍNDICE] == '>' || códigoFonte[BASE_cargo + em_dia_ÍNDICE] == '<')) {
                    boolean 수치 = em_dia_ÍNDICE > START_cargo;
                    for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < em_dia_ÍNDICE; Loop_ÍNDICE++) if (códigoFonte[BASE_cargo + Loop_ÍNDICE] < '0' || códigoFonte[BASE_cargo + Loop_ÍNDICE] > '9') 수치 = false;
                    if (수치) { erro("번호를 지정한 ficheiro descritor_entrada E_S 전환은 지원하지 않습니다"); return -1; }
                }
            }
            Tipo_VALOR[caractere_especial + total_CONT_NÚM] = dados_Tipo; iniciar[caractere_especial + total_CONT_NÚM] = START_cargo; 끝[caractere_especial + total_CONT_NÚM] = em_dia_ÍNDICE; total_CONT_NÚM++;
        }
        boolean 낱말 = false;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < total_CONT_NÚM; Loop_ÍNDICE++) {
            int 임시값 = Tipo_VALOR[caractere_especial + Loop_ÍNDICE];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_ÍNDICE == total_CONT_NÚM || Tipo_VALOR[caractere_especial + Loop_ÍNDICE] != 0) { erro("E_S 전환에 ficheiro 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_ÍNDICE == total_CONT_NÚM - 1 && 임시값 != 1) { erro("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (total_CONT_NÚM > 0 && !낱말 && Tipo_VALOR[caractere_especial + total_CONT_NÚM - 1] != 1) { erro("명령이 빠졌습니다"); return -1; }
        return total_CONT_NÚM;
    }
    static boolean alcance_SMS(int[] dados_MATRIZ, int local_START, int entrada_CONT_NÚM_8f7753a1, String caractere_cargo) {
        if (entrada_CONT_NÚM_8f7753a1 != caractere_cargo.length()) return false; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) if (dados_MATRIZ[local_START + Loop_ÍNDICE] != caractere_cargo.charAt(Loop_ÍNDICE)) return false; return true;
    }
    static void 넣기(int byte_dados) {
        if (쓴수 >= InterpretadorComandos.token_VALOR.length) { if (!extensão_erro) erro("변수를 펼친 명령이 너무 깁니다"); extensão_erro = true; return; }
        InterpretadorComandos.token_VALOR[쓴수++] = byte_dados;
    }
    static void variável_VALOR(int[] dados_MATRIZ, int START_cargo, int entrada_CONT_NÚM_8f7753a1) {
        if (alcance_SMS(dados_MATRIZ, START_cargo, entrada_CONT_NÚM_8f7753a1, "PWD")) { 넣기('/'); for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < FicheirosMemória.em_dia_duração; Loop_ÍNDICE++) 넣기(FicheirosMemória.em_dia_item[Loop_ÍNDICE]); return; }
        if (alcance_SMS(dados_MATRIZ, START_cargo, entrada_CONT_NÚM_8f7753a1, "HOME")) { 넣기('/'); return; }
        if (alcance_SMS(dados_MATRIZ, START_cargo, entrada_CONT_NÚM_8f7753a1, "?")) {
            int dados_VALOR = Estado_VALOR, dígito = 100; boolean 시작여부 = false;
            while (dígito > 0) { int à_direita_VALOR = dados_VALOR / dígito; if (à_direita_VALOR != 0 || 시작여부 || dígito == 1) { 넣기('0' + à_direita_VALOR); 시작여부 = true; } dados_VALOR %= dígito; dígito /= 10; } return;
        }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (이름길이[Loop_ÍNDICE] == entrada_CONT_NÚM_8f7753a1) {
            boolean set = true; for (int interna_cargo = 0; interna_cargo < entrada_CONT_NÚM_8f7753a1; interna_cargo++) if (variável_nome[Loop_ÍNDICE * 32 + interna_cargo] != dados_MATRIZ[START_cargo + interna_cargo]) set = false;
            if (set) { for (int interna_cargo = 0; interna_cargo < VALOR_duração[Loop_ÍNDICE]; interna_cargo++) 넣기(variável_dados[Loop_ÍNDICE * 256 + interna_cargo]); return; }
        }
    }
    static boolean Word_VALOR(int 낱말번호, int 중첩깊이) {
        int leitura_cursor = iniciar[중첩깊이 * 128 + 낱말번호], encerrar_cargo = 끝[중첩깊이 * 128 + 낱말번호], BASE_cargo = 중첩깊이 * 4096, Citação = 0;
        if (leitura_cursor < encerrar_cargo && códigoFonte[BASE_cargo + leitura_cursor] == '~' && (leitura_cursor + 1 == encerrar_cargo || códigoFonte[BASE_cargo + leitura_cursor + 1] == '/')) { 넣기('/'); leitura_cursor++; }
        while (leitura_cursor < encerrar_cargo) {
            int ponto_de_código = códigoFonte[BASE_cargo + leitura_cursor++];
            if (ponto_de_código == Citação) { Citação = 0; continue; }
            if (Citação == 0 && (ponto_de_código == 39 || ponto_de_código == 34)) { Citação = ponto_de_código; continue; }
            if (ponto_de_código == '\\' && Citação != 39) { int Avançar_cargo = códigoFonte[BASE_cargo + leitura_cursor++]; if (Citação == 34 && Avançar_cargo != '$' && Avançar_cargo != '"' && Avançar_cargo != '\\') 넣기('\\'); 넣기(Avançar_cargo); continue; }
            if (ponto_de_código == '$' && Citação != 39 && leitura_cursor < encerrar_cargo) {
                boolean 중괄호자리 = códigoFonte[BASE_cargo + leitura_cursor] == '{'; if (중괄호자리) leitura_cursor++;
                int 처음자리 = leitura_cursor;
                if (leitura_cursor < encerrar_cargo && códigoFonte[BASE_cargo + leitura_cursor] == '?') leitura_cursor++;
                else while (leitura_cursor < encerrar_cargo && 이름뒤(códigoFonte[BASE_cargo + leitura_cursor])) leitura_cursor++;
                if (중괄호자리 && (leitura_cursor == encerrar_cargo || códigoFonte[BASE_cargo + leitura_cursor] != '}')) { erro("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (leitura_cursor == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                variável_VALOR(códigoFonte, BASE_cargo + 처음자리, leitura_cursor - 처음자리); if (중괄호자리) leitura_cursor++; continue;
            }
            넣기(ponto_de_código);
        }
        return !extensão_erro;
    }
    static int ambiente_Configurações(int argumento_ÍNDICE, boolean remover) {
        int local_START = InterpretadorComandos.시작점[argumento_ÍNDICE], encerrar_cargo = local_START + InterpretadorComandos.duração_VALOR[argumento_ÍNDICE], 같음자리 = local_START;
        while (같음자리 < encerrar_cargo && InterpretadorComandos.token_VALOR[같음자리] != '=') 같음자리++;
        int entrada_CONT_NÚM_8f7753a1 = 같음자리 - local_START;
        if (entrada_CONT_NÚM_8f7753a1 < 1 || entrada_CONT_NÚM_8f7753a1 > 31 || !nome_caractere(InterpretadorComandos.token_VALOR[local_START]) || !remover && 같음자리 == encerrar_cargo || encerrar_cargo - 같음자리 - 1 > 255) return 2;
        for (int Loop_ÍNDICE = local_START; Loop_ÍNDICE < 같음자리; Loop_ÍNDICE++) if (!이름뒤(InterpretadorComandos.token_VALOR[Loop_ÍNDICE])) return 2;
        if (alcance_SMS(InterpretadorComandos.token_VALOR, local_START, entrada_CONT_NÚM_8f7753a1, "PWD") || alcance_SMS(InterpretadorComandos.token_VALOR, local_START, entrada_CONT_NÚM_8f7753a1, "HOME")) return 2;
        int 찾은여부 = -1, TI_vazio_Estado = -1;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) {
            if (이름길이[Loop_ÍNDICE] == 0) TI_vazio_Estado = Loop_ÍNDICE;
            if (이름길이[Loop_ÍNDICE] != entrada_CONT_NÚM_8f7753a1) continue;
            boolean set = true; for (int interna_cargo = 0; interna_cargo < entrada_CONT_NÚM_8f7753a1; interna_cargo++) if (variável_nome[Loop_ÍNDICE * 32 + interna_cargo] != InterpretadorComandos.token_VALOR[local_START + interna_cargo]) set = false;
            if (set) 찾은여부 = Loop_ÍNDICE;
        }
        if (remover) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = TI_vazio_Estado; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = entrada_CONT_NÚM_8f7753a1; VALOR_duração[찾은여부] = encerrar_cargo - 같음자리 - 1;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) variável_nome[찾은여부 * 32 + Loop_ÍNDICE] = InterpretadorComandos.token_VALOR[local_START + Loop_ÍNDICE];
        for (int Loop_ÍNDICE = 같음자리 + 1; Loop_ÍNDICE < encerrar_cargo; Loop_ÍNDICE++) variável_dados[찾은여부 * 256 + Loop_ÍNDICE - 같음자리 - 1] = InterpretadorComandos.token_VALOR[Loop_ÍNDICE];
        return 0;
    }
    static void mostrar_ambiente() {
        단말.Escrita("HOME=/\nPWD="); FicheirosMemória.em_dia_gravar(); 단말.문자(10);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (이름길이[Loop_ÍNDICE] > 0) {
            for (int interna_cargo = 0; interna_cargo < 이름길이[Loop_ÍNDICE]; interna_cargo++) Quadro.직렬쓰기(variável_nome[Loop_ÍNDICE * 32 + interna_cargo]); 단말.문자('=');
            for (int interna_cargo = 0; interna_cargo < VALOR_duração[Loop_ÍNDICE]; interna_cargo++) Quadro.직렬쓰기(variável_dados[Loop_ÍNDICE * 256 + interna_cargo]); 단말.문자(10);
        }
    }
    static void Executar_comando(int[] dados_MATRIZ, int 시작변위, int entrada_CONT_NÚM_8f7753a1, int 중첩깊이) {
        if (중첩깊이 >= 4 || entrada_CONT_NÚM_8f7753a1 > 4096) { erro("comando 파일의 aninhamento_VALOR 또는 linha_de_entrada duração_VALOR 제한을 넘었습니다"); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) códigoFonte[중첩깊이 * 4096 + Loop_ÍNDICE] = dados_MATRIZ[시작변위 + Loop_ÍNDICE];
        int total_CONT_NÚM = Leitura(entrada_CONT_NÚM_8f7753a1, 중첩깊이); if (total_CONT_NÚM < 0) return;
        int leitura_cursor = 0, 조건성립 = 1;
        while (leitura_cursor < total_CONT_NÚM) {
            int Grupo_encerrar = leitura_cursor;
            while (Grupo_encerrar < total_CONT_NÚM && (Tipo_VALOR[중첩깊이 * 128 + Grupo_encerrar] == 0 || Tipo_VALOR[중첩깊이 * 128 + Grupo_encerrar] >= 4)) Grupo_encerrar++;
            boolean Executar_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && Estado_VALOR == 0 || 조건성립 == 3 && Estado_VALOR != 0;
            if (Executar_cc685ae5) {
                boolean Anterior_item_ÍNDICE = false;
                while (leitura_cursor < Grupo_encerrar) {
                    int Avançar_cargo = leitura_cursor; while (Avançar_cargo < Grupo_encerrar && Tipo_VALOR[중첩깊이 * 128 + Avançar_cargo] != 4) Avançar_cargo++;
                    boolean Conexão_fluxo = Avançar_cargo < Grupo_encerrar; int entrada_página = -1, saída_página = -1, 출력방식 = 0;
                    InterpretadorComandos.token_CONT_NÚM = 0; 쓴수 = 0; extensão_erro = false;
                    for (int Loop_ÍNDICE = leitura_cursor; Loop_ÍNDICE < Avançar_cargo; Loop_ÍNDICE++) {
                        int dados_Tipo = Tipo_VALOR[중첩깊이 * 128 + Loop_ÍNDICE];
                        if (dados_Tipo >= 5) { if (dados_Tipo == 7) { if (entrada_página >= 0) { erro("entrada_VALOR 전환이 겹쳤습니다"); return; } entrada_página = ++Loop_ÍNDICE; } else { if (saída_página >= 0) { erro("saídaTexto 전환이 겹쳤습니다"); return; } saída_página = ++Loop_ÍNDICE; 출력방식 = dados_Tipo; } continue; }
                        if (InterpretadorComandos.token_CONT_NÚM == 32) { erro("인수가 너무 많습니다"); return; }
                        int argumento_ÍNDICE = InterpretadorComandos.token_CONT_NÚM++; InterpretadorComandos.시작점[argumento_ÍNDICE] = 쓴수;
                        if (!Word_VALOR(Loop_ÍNDICE, 중첩깊이)) return;
                        InterpretadorComandos.duração_VALOR[argumento_ÍNDICE] = 쓴수 - InterpretadorComandos.시작점[argumento_ÍNDICE];
                    }
                    연결중 = Anterior_item_ÍNDICE || Conexão_fluxo || entrada_página >= 0 || saída_página >= 0;
                    if (연결중 && (InterpretadorComandos.같음(0, "vi") || InterpretadorComandos.같음(0, "edit") || InterpretadorComandos.같음(0, "load") || InterpretadorComandos.같음(0, "gui") || InterpretadorComandos.같음(0, "terminal") || InterpretadorComandos.같음(0, "sh") || InterpretadorComandos.같음(0, "source"))) { erro("interativo 명령과 comando 파일은 E_S 전환이나 fluxo_VALOR 연결에 쓸 número 없습니다"); return; }
                    셸입출력.iniciar(Anterior_item_ÍNDICE, Conexão_fluxo);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int entrada_cargo_206f1c6d = 입출력바꿈 == 0 ? entrada_página : saída_página; if (entrada_cargo_206f1c6d < 0) continue;
                        int START_cargo = 쓴수; if (!Word_VALOR(entrada_cargo_206f1c6d, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = FicheirosMemória.caminho_START(쓴수 - START_cargo);
                        for (int interna_cargo = START_cargo; 처리값 >= 0 && interna_cargo < 쓴수; interna_cargo++) 처리값 = FicheirosMemória.caminho_byte(interna_cargo - START_cargo, InterpretadorComandos.token_VALOR[interna_cargo]);
                        if (처리값 >= 0) 처리값 = FicheirosMemória.Abrir(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); InterpretadorComandos.erro(처리값); Estado_VALOR = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.arquivo_de_entrada = 처리값; else 셸입출력.arquivo_de_saída = 처리값;
                    }
                    셸입출력.Permitir_interativo = 중첩깊이 == 0 && leitura_cursor == 0 && Avançar_cargo == total_CONT_NÚM;
                    깊이 = 중첩깊이; InterpretadorComandos.resultado = 0; Quadro.입출력전환(1);
                    InterpretadorComandos.comando();
                    Quadro.terminal(3);
                    int 반환값 = InterpretadorComandos.resultado, fluxo_erro = 셸입출력.falha_VALOR;
                    셸입출력.끝(); 연결중 = false;
                    Estado_VALOR = fluxo_erro < 0 ? 1 : 반환값;
                    if (fluxo_erro < 0) { InterpretadorComandos.erro(fluxo_erro); return; }
                    if (script_encerrar || 반환값 == -1005) return;
                    Anterior_item_ÍNDICE = true; leitura_cursor = Avançar_cargo + 1;
                }
            }
            if (Grupo_encerrar < total_CONT_NÚM) 조건성립 = Tipo_VALOR[중첩깊이 * 128 + Grupo_encerrar];
            leitura_cursor = Grupo_encerrar + 1;
        }
    }
    static void Executar_Arquivo() {
        if (InterpretadorComandos.token_CONT_NÚM != 2 || 깊이 >= 3) { InterpretadorComandos.resultado = 2; 단말.Escrita("사용법: sh ficheiro (aninhamento_VALOR 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = InterpretadorComandos.caminho(1); if (처리값 >= 0) 처리값 = FicheirosMemória.Abrir(0);
        if (처리값 < 0) { InterpretadorComandos.erro(처리값); return; }
        int entrada_CONT_NÚM_8f7753a1 = 0, byte_dados;
        while ((byte_dados = FicheirosMemória.Leitura(처리값)) != 256 && byte_dados >= 0 && entrada_CONT_NÚM_8f7753a1 < 16384) script_VALOR[중첩깊이 * 16384 + entrada_CONT_NÚM_8f7753a1++] = byte_dados;
        FicheirosMemória.Fechar(처리값); Quadro.입출력전환(0);
        for (int leitura_cursor = 0; leitura_cursor < entrada_CONT_NÚM_8f7753a1 && !script_encerrar;) {
            int encerrar_cargo = leitura_cursor; while (encerrar_cargo < entrada_CONT_NÚM_8f7753a1 && script_VALOR[중첩깊이 * 16384 + encerrar_cargo] != 10) encerrar_cargo++;
            int válido_duração = encerrar_cargo - leitura_cursor; if (válido_duração > 0 && script_VALOR[중첩깊이 * 16384 + encerrar_cargo - 1] == 13) válido_duração--;
            Executar_comando(script_VALOR, 중첩깊이 * 16384 + leitura_cursor, válido_duração, 중첩깊이); leitura_cursor = encerrar_cargo + 1;
        }
        InterpretadorComandos.resultado = Estado_VALOR; script_encerrar = false; 깊이 = 중첩깊이 - 1;
    }
}
