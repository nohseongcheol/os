// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. ficheiro/operando_pilha/Referência/branch 경계를 Executar_comando 중 검사한다. */
public final class 자바가상기계 {
    static int[] ficheiro = new int[16 * 16384], arquivo_temporário = new int[16384], nome_de_arquivo_SMS = new int[512];
    static int[] constante_tag = new int[8192], 상가 = new int[8192], constante_SEGUNDO_VALOR = new int[8192], cadeia_Referência = new int[8192];
    static int[] método_nome_SMS = new int[512], método_TIPO = new int[512], método_acesso = new int[512], método_proprietário = new int[512];
    static int[] método_START = new int[512], método_encerrar = new int[512], método_pilha = new int[512], 함수지역 = new int[512];
    static int[] método_argumento_CONT_NÚM = new int[512], método_argumento_TIPO = new int[8192], método_devolver = new int[512];
    static int[] limite_VALOR = new int[16 * 16384];
    static int[] local_VALOR = new int[16384], local_TIPO = new int[16384], operando_pilha_VALOR = new int[16384], operando_pilha_TIPO = new int[16384];
    static int[] quadro_método = new int[128], quadro_cargo = new int[128], quadro_pilha = new int[128], quadro_instrução = new int[128], inicializar_quadro = new int[128];
    static int[] aula_Definição_nome = new int[16], aula_Definição_dimensionar = new int[16], aula_Definição_pai = new int[16], aula_Definição_Estado = new int[16], aula_slot_CONT_NÚM = new int[16], inicializar_aula_Definição = new int[16];
    static int[] aula_interface = new int[16 * 16], aula_interface_CONT_NÚM = new int[16];
    static int[] slot_nome = new int[512], slot_TIPO = new int[512], slot_proprietário = new int[512], slot_Permissões = new int[512], slot_cargo = new int[512], slot_dados = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] heap_VALOR = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], heap_Referência = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], elemento_da_matriz = new int[32768], Store_inteiro = new int[256];
    static int Tamanho, leitura_cargo, método_CONT_NÚM, nome_da_classe, quadro_ÍNDICE = -1, heap_encerrar_cargo = 1, tipo_de_retorno;
    static int aula_Definição_CONT_NÚM, slot_CONT_NÚM, 잡기수, 현재읽는종, 던진객체, 잠시수, visor_CONT_NÚM, Coleção_CONT_NÚM;
    static int em_dia_thread, contagem_de_threads = 1, entrada_aula_Definição;
    static int[] thread_quadro = new int[4], thread_Estado = new int[4], thread_objeto = new int[4], thread_alvo = new int[4], 가닥대기 = new int[4];
    static boolean erro, solicitação_de_alteração;
    static int[] bloquear_proprietário = new int[32768], 잠금깊이 = new int[32768], quadro_bloquear = new int[128], aula_bloquear = new int[16], aula_thread = new int[16];

    static void falha_VALOR(String Word_SMS) {
        if (erro) return;
        int área_CÓDIGO = 0;
        if (FerramentasJava.같음(Word_SMS, "ArithmeticException: / by zero")) área_CÓDIGO = 4;
        if (FerramentasJava.같음(Word_SMS, "NullPointerException") || FerramentasJava.같음(Word_SMS, "null or invalid array")) área_CÓDIGO = 5;
        if (FerramentasJava.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) área_CÓDIGO = 7;
        if (FerramentasJava.같음(Word_SMS, "StringIndexOutOfBoundsException")) área_CÓDIGO = 8;
        if (FerramentasJava.같음(Word_SMS, "NumberFormatException")) área_CÓDIGO = 10;
        if (FerramentasJava.같음(Word_SMS, "FileNotFoundException: file open failed")) área_CÓDIGO = 12;
        if (FerramentasJava.같음(Word_SMS, "IOException: stream closed") || FerramentasJava.같음(Word_SMS, "IOException: read failed") || FerramentasJava.같음(Word_SMS, "IOException: write failed")) área_CÓDIGO = 11;
        if (FerramentasJava.같음(Word_SMS, "ClassCastException")) área_CÓDIGO = 14;
        if (FerramentasJava.같음(Word_SMS, "NegativeArraySizeException")) área_CÓDIGO = 15;
        if (área_CÓDIGO != 0 && quadro_ÍNDICE >= 0) { 예외던짐(área_CÓDIGO, Word_SMS); return; }
        espaço_do_utilizador.Escrita("JVM error: "); espaço_do_utilizador.Escrita(Word_SMS); espaço_do_utilizador.gravar_caractere_VALOR(10); erro = true;
    }
    static boolean recortar(int iniciar, int duração_VALOR) {
        if (iniciar < 0 || iniciar >= ficheiro.length || duração_VALOR < 0) return false;
        int aula_Definição = iniciar / 16384;
        return iniciar % 16384 <= aula_Definição_dimensionar[aula_Definição] && duração_VALOR <= aula_Definição_dimensionar[aula_Definição] - iniciar % 16384;
    }
    static int byte_VALOR() {
        if (!recortar(leitura_cargo, 1)) { falha_VALOR("truncated class file"); return 0; }
        return ficheiro[leitura_cargo++];
    }
    static int 짧은수() { return byte_VALOR() << 8 | byte_VALOR(); }
    static int inteiro() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int duração_VALOR) { if (!recortar(leitura_cargo, duração_VALOR)) falha_VALOR("invalid attribute size"); else leitura_cargo += duração_VALOR; }
    static boolean cheque_constante(int número, int Tipo_VALOR) {
        if (número <= 0 || número >= constante_tag.length || constante_tag[número] != Tipo_VALOR) { falha_VALOR("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_alcance(int iniciar, int duração_VALOR, String Word_SMS) {
        if (!recortar(iniciar, duração_VALOR)) return false;
        int leitura_cursor = iniciar, 끝 = iniciar + duração_VALOR;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Word_SMS.length(); Loop_ÍNDICE++) {
            int ponto_de_código = Word_SMS.charAt(Loop_ÍNDICE);
            if (ponto_de_código > 0 && ponto_de_código < 128) { if (leitura_cursor >= 끝 || ficheiro[leitura_cursor++] != ponto_de_código) return false; }
            else if (ponto_de_código < 2048) {
                if (leitura_cursor + 2 > 끝 || ficheiro[leitura_cursor++] != (192 | (ponto_de_código >> 6)) || ficheiro[leitura_cursor++] != (128 | (ponto_de_código & 63))) return false;
            } else if (leitura_cursor + 3 > 끝 || ficheiro[leitura_cursor++] != (224 | (ponto_de_código >> 12)) || ficheiro[leitura_cursor++] != (128 | ((ponto_de_código >> 6) & 63)) || ficheiro[leitura_cursor++] != (128 | (ponto_de_código & 63))) return false;
        }
        return leitura_cursor == 끝;
    }
    static boolean Word_SMS(int constante_VALOR, String Word_SMS) { return cheque_constante(constante_VALOR, 1) && SMS_alcance(상가[constante_VALOR], constante_SEGUNDO_VALOR[constante_VALOR], Word_SMS); }
    static boolean 같은말(int 가, int SEGUNDO_operando) {
        if (!cheque_constante(가, 1) || !cheque_constante(SEGUNDO_operando, 1) || constante_SEGUNDO_VALOR[가] != constante_SEGUNDO_VALOR[SEGUNDO_operando]) return false;
        for (int número = 0; número < constante_SEGUNDO_VALOR[가]; número++) if (ficheiro[상가[가] + número] != ficheiro[상가[SEGUNDO_operando] + número]) return false;
        return true;
    }
    static int nome_da_classe_SMS(int número) { return cheque_constante(número, 7) && cheque_constante(상가[número], 1) ? 상가[número] : 0; }
    static int Referência_nome(int número) { return cheque_constante(número, 12) && cheque_constante(상가[número], 1) ? 상가[número] : 0; }
    static int tipo_de_referência(int número) { return cheque_constante(número, 12) && cheque_constante(constante_SEGUNDO_VALOR[número], 1) ? constante_SEGUNDO_VALOR[número] : 0; }
    static int descritor_TIPO(int 끝, boolean vazio_TIPO) {
        if (leitura_cargo >= 끝) { falha_VALOR("invalid descriptor"); return 0; }
        int VALOR = byte_VALOR();
        if (VALOR == 'V' && vazio_TIPO) return 0;
        if (VALOR == 'I' || VALOR == 'B' || VALOR == 'C' || VALOR == 'S' || VALOR == 'Z') return 1;
        if (VALOR == '[') { descritor_TIPO(끝, false); return 2; }
        if (VALOR == 'L') {
            int iniciar = leitura_cargo;
            while (leitura_cargo < 끝 && ficheiro[leitura_cargo] != ';') leitura_cargo++;
            if (leitura_cargo == 끝 || leitura_cargo == iniciar) falha_VALOR("invalid reference descriptor");
            else leitura_cargo++;
            return 2;
        }
        falha_VALOR("unsupported descriptor type"); return 0;
    }
    static void leitura_descritor(int FUNÇÃO_VALOR) {
        int Anterior_item = leitura_cargo, número = método_TIPO[FUNÇÃO_VALOR];
        if (!cheque_constante(número, 1)) return;
        leitura_cargo = 상가[número]; int 끝 = leitura_cargo + constante_SEGUNDO_VALOR[número];
        if (byte_VALOR() != '(') falha_VALOR("invalid method descriptor");
        int item_CONT_NÚM = 0;
        while (!erro && leitura_cargo < 끝 && ficheiro[leitura_cargo] != ')') {
            if (item_CONT_NÚM == 16) { falha_VALOR("too many method arguments"); break; }
            método_argumento_TIPO[FUNÇÃO_VALOR * 16 + item_CONT_NÚM++] = descritor_TIPO(끝, false);
        }
        if (leitura_cargo >= 끝 || byte_VALOR() != ')') falha_VALOR("invalid method descriptor");
        método_devolver[FUNÇÃO_VALOR] = descritor_TIPO(끝, true); método_argumento_CONT_NÚM[FUNÇÃO_VALOR] = item_CONT_NÚM;
        if (leitura_cargo != 끝) falha_VALOR("invalid method descriptor");
        leitura_cargo = Anterior_item;
    }
    static int leitura_constante_ÍNDICE() { int VALOR = 짧은수(); return VALOR == 0 ? 0 : 현재읽는종 * 512 + VALOR; }
    static int leitura_opcode_constante() { return método_proprietário[quadro_método[quadro_ÍNDICE]] * 512 + 명짧(); }
    static void ignorar_atributo() {
        int item_CONT_NÚM = 짧은수();
        for (int número = 0; número < item_CONT_NÚM && !erro; número++) { cheque_constante(leitura_constante_ÍNDICE(), 1); 건너(inteiro()); }
    }
    static int comando_duração(int VALOR) {
        if (VALOR == 16 || VALOR == 18 || VALOR == 21 || VALOR == 25 || VALOR == 54 || VALOR == 58 || VALOR == 188) return 2;
        if (VALOR == 17 || VALOR == 19 || VALOR == 132 || VALOR >= 153 && VALOR <= 167
            || VALOR >= 178 && VALOR <= 184 || VALOR == 187 || VALOR == 189 || VALOR == 192 || VALOR == 193 || VALOR == 198 || VALOR == 199) return 3;
        if (VALOR == 185 || VALOR == 200) return 5;
        if (VALOR >= 0 && VALOR <= 8 || VALOR >= 26 && VALOR <= 29 || VALOR >= 42 && VALOR <= 46 || VALOR >= 50 && VALOR <= 53
            || VALOR >= 59 && VALOR <= 62 || VALOR >= 75 && VALOR <= 79 || VALOR >= 83 && VALOR <= 95
            || VALOR == 96 || VALOR == 100 || VALOR == 104 || VALOR == 108 || VALOR == 112 || VALOR == 116
            || VALOR == 120 || VALOR == 122 || VALOR == 124 || VALOR == 126 || VALOR == 128 || VALOR == 130
            || VALOR >= 145 && VALOR <= 147 || VALOR == 172 || VALOR == 176 || VALOR == 177 || VALOR == 190 || VALOR == 191
            || VALOR == 194 || VALOR == 195) return 1;
        return 0;
    }
    static int cargo_inteiro(int leitura_cursor) {
        if (!recortar(leitura_cursor, 4)) { falha_VALOR("truncated bytecode operand"); return 0; }
        return ficheiro[leitura_cursor] << 24 | ficheiro[leitura_cursor + 1] << 16 | ficheiro[leitura_cursor + 2] << 8 | ficheiro[leitura_cursor + 3];
    }
    static int leitura_duração(int leitura_cursor, int iniciar, int 끝) {
        int VALOR = ficheiro[leitura_cursor], duração_VALOR = comando_duração(VALOR);
        if (VALOR == 170 || VALOR == 171) {
            int BASE_cargo = leitura_cursor + 1;
            while ((BASE_cargo - iniciar) % 4 != 0) BASE_cargo++;
            if (끝 - BASE_cargo < (VALOR == 170 ? 12 : 8)) return 0;
            int entrada_CONT_NÚM_8f7753a1 = VALOR == 170 ? cargo_inteiro(BASE_cargo + 8) - cargo_inteiro(BASE_cargo + 4) + 1 : cargo_inteiro(BASE_cargo + 4);
            if (entrada_CONT_NÚM_8f7753a1 < 0 || entrada_CONT_NÚM_8f7753a1 > 2048) return 0;
            duração_VALOR = BASE_cargo - leitura_cursor + (VALOR == 170 ? 12 + 4 * entrada_CONT_NÚM_8f7753a1 : 8 + 8 * entrada_CONT_NÚM_8f7753a1);
        }
        if (VALOR == 196 && leitura_cursor + 1 < 끝) {
            int Word_dados = ficheiro[leitura_cursor + 1]; duração_VALOR = Word_dados == 132 ? 6 : (Word_dados == 21 || Word_dados == 25 || Word_dados == 54 || Word_dados == 58) ? 4 : 0;
        }
        return duração_VALOR > 0 && duração_VALOR <= 끝 - leitura_cursor ? duração_VALOR : 0;
    }
    static void cheque_destino_VALOR(int destino_VALOR, int FUNÇÃO_VALOR) {
        if (destino_VALOR < método_START[FUNÇÃO_VALOR] || destino_VALOR >= método_encerrar[FUNÇÃO_VALOR] || limite_VALOR[destino_VALOR] != FUNÇÃO_VALOR + 1) falha_VALOR("invalid branch target");
    }
    static void leitura_aula(int aula_Definição) {
        현재읽는종 = aula_Definição; leitura_cargo = aula_Definição * 16384; Tamanho = leitura_cargo + aula_Definição_dimensionar[aula_Definição];
        if (inteiro() != 0xcafebabe) { falha_VALOR("not a class file"); return; }
        int 부판 = 짧은수(), versão_VALOR = 짧은수();
        if (versão_VALOR < 45 || versão_VALOR > 52 || 부판 != 0) { falha_VALOR("supported class versions: 45..52, minor 0"); return; }
        int constante_CONT_NÚM = 짧은수(), BASE_cargo = aula_Definição * 512;
        if (constante_CONT_NÚM < 1 || constante_CONT_NÚM > 512) { falha_VALOR("constant pool limit (511)"); return; }
        for (int entrada_CONT_NÚM_8f7753a1 = 1; entrada_CONT_NÚM_8f7753a1 < constante_CONT_NÚM && !erro; entrada_CONT_NÚM_8f7753a1++) {
            int número = BASE_cargo + entrada_CONT_NÚM_8f7753a1, Tipo_VALOR = byte_VALOR(); constante_tag[número] = Tipo_VALOR;
            if (Tipo_VALOR == 1) { constante_SEGUNDO_VALOR[número] = 짧은수(); 상가[número] = leitura_cargo; 건너(constante_SEGUNDO_VALOR[número]); }
            else if (Tipo_VALOR == 3) 상가[número] = inteiro();
            else if (Tipo_VALOR == 7 || Tipo_VALOR == 8) 상가[número] = leitura_constante_ÍNDICE();
            else if (Tipo_VALOR == 9 || Tipo_VALOR == 10 || Tipo_VALOR == 11 || Tipo_VALOR == 12) { 상가[número] = leitura_constante_ÍNDICE(); constante_SEGUNDO_VALOR[número] = leitura_constante_ÍNDICE(); }
            else falha_VALOR("unsupported constant type");
        }
        int Permissão_VALOR = 짧은수();
        if ((Permissão_VALOR & (0x2000 | 0x4000)) != 0) falha_VALOR("annotation/enum class unsupported");
        aula_Definição_nome[aula_Definição] = nome_da_classe_SMS(leitura_constante_ÍNDICE());
        aula_Definição_pai[aula_Definição] = nome_da_classe_SMS(leitura_constante_ÍNDICE());
        int interface_CONT_NÚM = 짧은수(); if (interface_CONT_NÚM > 16) { falha_VALOR("interface count limit"); return; }
        aula_interface_CONT_NÚM[aula_Definição] = interface_CONT_NÚM;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < interface_CONT_NÚM; Loop_ÍNDICE++) aula_interface[aula_Definição * 16 + Loop_ÍNDICE] = nome_da_classe_SMS(leitura_constante_ÍNDICE());
        int Campo_CONT_NÚM = 짧은수();
        if (Campo_CONT_NÚM > 512 - slot_CONT_NÚM) { falha_VALOR("field count limit (512)"); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Campo_CONT_NÚM && !erro; Loop_ÍNDICE++) {
            int Arquivo_ÍNDICE = slot_CONT_NÚM++; slot_proprietário[Arquivo_ÍNDICE] = aula_Definição; slot_Permissões[Arquivo_ÍNDICE] = 짧은수(); slot_nome[Arquivo_ÍNDICE] = leitura_constante_ÍNDICE(); slot_TIPO[Arquivo_ÍNDICE] = leitura_constante_ÍNDICE();
            cheque_constante(slot_nome[Arquivo_ÍNDICE], 1); cheque_constante(slot_TIPO[Arquivo_ÍNDICE], 1);
            int 보존값 = leitura_cargo; leitura_cargo = 상가[slot_TIPO[Arquivo_ÍNDICE]]; int área_CÓDIGO = descritor_TIPO(leitura_cargo + constante_SEGUNDO_VALOR[slot_TIPO[Arquivo_ÍNDICE]], false); leitura_cargo = 보존값;
            if ((slot_Permissões[Arquivo_ÍNDICE] & 8) == 0) slot_cargo[Arquivo_ÍNDICE] = aula_slot_CONT_NÚM[aula_Definição]++;
            int atributo_dados = 짧은수();
            for (int interna_cargo = 0; interna_cargo < atributo_dados && !erro; interna_cargo++) {
                int nome_constante = leitura_constante_ÍNDICE(), válido_duração = inteiro();
                if (Word_SMS(nome_constante, "ConstantValue") && válido_duração == 2) {
                    int dados_VALOR = leitura_constante_ÍNDICE();
                    if (área_CÓDIGO == 1 && cheque_constante(dados_VALOR, 3)) slot_dados[Arquivo_ÍNDICE] = 상가[dados_VALOR];
                    else if (área_CÓDIGO == 2 && cheque_constante(dados_VALOR, 8)) slot_dados[Arquivo_ÍNDICE] = constante_SMS(상가[dados_VALOR]);
                } else 건너(válido_duração);
            }
        }
        int item_CONT_NÚM = 짧은수();
        if (item_CONT_NÚM > 512 - método_CONT_NÚM) { falha_VALOR("method count limit (512)"); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < item_CONT_NÚM && !erro; Loop_ÍNDICE++) {
            int número = método_CONT_NÚM++; método_proprietário[número] = aula_Definição;
            método_acesso[número] = 짧은수(); método_nome_SMS[número] = leitura_constante_ÍNDICE(); método_TIPO[número] = leitura_constante_ÍNDICE();
            cheque_constante(método_nome_SMS[número], 1); leitura_descritor(número);
            if ((método_acesso[número] & 8) == 0) {
                if (método_argumento_CONT_NÚM[número] == 16) { falha_VALOR("too many instance method arguments"); return; }
                for (int Comparação_cargo = método_argumento_CONT_NÚM[número]; Comparação_cargo > 0; Comparação_cargo--) método_argumento_TIPO[número * 16 + Comparação_cargo] = método_argumento_TIPO[número * 16 + Comparação_cargo - 1];
                método_argumento_TIPO[número * 16] = 2; método_argumento_CONT_NÚM[número]++;
            }
            if ((método_acesso[número] & 0x100) != 0) falha_VALOR("user native method unsupported");
            if (Word_SMS(método_nome_SMS[número], "<clinit>")) inicializar_aula_Definição[aula_Definição] = número + 1;
            for (int câmera_frontal_VALOR = 0; câmera_frontal_VALOR < número; câmera_frontal_VALOR++) if (método_proprietário[câmera_frontal_VALOR] == aula_Definição && 같은말(método_nome_SMS[câmera_frontal_VALOR], método_nome_SMS[número]) && 같은말(método_TIPO[câmera_frontal_VALOR], método_TIPO[número])) falha_VALOR("duplicate method");
            int atributo_CONT_NÚM = 짧은수();
            for (int valor_do_atributo = 0; valor_do_atributo < atributo_CONT_NÚM && !erro; valor_do_atributo++) {
                int Nome = leitura_constante_ÍNDICE(), duração_VALOR = inteiro(), iniciar = leitura_cargo;
                if (!recortar(iniciar, duração_VALOR)) { falha_VALOR("truncated method attribute"); break; }
                if (Word_SMS(Nome, "Code")) {
                    if (método_START[número] != 0) falha_VALOR("duplicate Code attribute");
                    método_pilha[número] = 짧은수(); 함수지역[número] = 짧은수(); int CÓDIGO_duração = inteiro();
                    if (método_pilha[número] > 128 || 함수지역[número] > 128 || 함수지역[número] < método_argumento_CONT_NÚM[número]
                        || CÓDIGO_duração < 1 || CÓDIGO_duração > 8192) falha_VALOR("method memory limits exceeded");
                    método_START[número] = leitura_cargo; 건너(CÓDIGO_duração); método_encerrar[número] = leitura_cargo;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { falha_VALOR("exception table limit"); return; }
                    for (int interna_cargo = 0; interna_cargo < 잡는수; interna_cargo++) {
                        int erro_Referência = 잡기수++; 잡기함수[erro_Referência] = número;
                        잡기시작[erro_Referência] = método_START[número] + 짧은수(); 잡기끝[erro_Referência] = método_START[número] + 짧은수();
                        잡기위치[erro_Referência] = método_START[número] + 짧은수(); int 부호값 = leitura_constante_ÍNDICE(); 잡기종[erro_Referência] = 부호값 == 0 ? 0 : nome_da_classe_SMS(부호값);
                    }
                    ignorar_atributo();
                    if (leitura_cargo != iniciar + duração_VALOR) falha_VALOR("Code attribute size mismatch");
                } else 건너(duração_VALOR);
            }
            if ((método_acesso[número] & 0x400) != 0) continue;
            if (método_START[número] == 0) falha_VALOR("missing Code attribute");
            int slot_entrada = método_START[número];
            while (slot_entrada < método_encerrar[número] && !erro) {
                int duração_VALOR = leitura_duração(slot_entrada, método_START[número], método_encerrar[número]);
                if (duração_VALOR == 0) { falha_VALOR("unsupported or truncated bytecode"); break; }
                limite_VALOR[slot_entrada] = número + 1; slot_entrada += duração_VALOR;
            }
            slot_entrada = método_START[número];
            while (slot_entrada < método_encerrar[número] && !erro) {
                int VALOR = ficheiro[slot_entrada];
                if (VALOR >= 153 && VALOR <= 167 || VALOR == 198 || VALOR == 199) cheque_destino_VALOR(slot_entrada + (short)(ficheiro[slot_entrada + 1] << 8 | ficheiro[slot_entrada + 2]), número);
                if (VALOR == 200) cheque_destino_VALOR(slot_entrada + cargo_inteiro(slot_entrada + 1), número);
                if (VALOR == 170 || VALOR == 171) {
                    int leitura_cursor = slot_entrada + 1; while ((leitura_cursor - método_START[número]) % 4 != 0) leitura_cursor++;
                    cheque_destino_VALOR(slot_entrada + cargo_inteiro(leitura_cursor), número);
                    int entrada_CONT_NÚM_8f7753a1 = VALOR == 170 ? cargo_inteiro(leitura_cursor + 8) - cargo_inteiro(leitura_cursor + 4) + 1 : cargo_inteiro(leitura_cursor + 4);
                    leitura_cursor += VALOR == 170 ? 12 : 8;
                    for (int interna_cargo = 0; interna_cargo < entrada_CONT_NÚM_8f7753a1; interna_cargo++) cheque_destino_VALOR(slot_entrada + cargo_inteiro(leitura_cursor + interna_cargo * (VALOR == 170 ? 4 : 8) + (VALOR == 170 ? 0 : 4)), número);
                }
                slot_entrada += leitura_duração(slot_entrada, método_START[número], método_encerrar[número]);
            }
            for (int interna_cargo = 0; interna_cargo < 잡기수; interna_cargo++) if (잡기함수[interna_cargo] == número) {
                cheque_destino_VALOR(잡기시작[interna_cargo], número); cheque_destino_VALOR(잡기위치[interna_cargo], número);
                if (잡기끝[interna_cargo] != método_encerrar[número]) cheque_destino_VALOR(잡기끝[interna_cargo], número);
                if (잡기시작[interna_cargo] >= 잡기끝[interna_cargo]) falha_VALOR("invalid exception range");
            }
        }
        if (!erro) ignorar_atributo();
        if (leitura_cargo != Tamanho) falha_VALOR("extra class file data");
    }
    static int alocar_Armazenamento(int Tipo_VALOR, int duração_VALOR) { return 새기억(Tipo_VALOR, duração_VALOR); }
    static boolean objeto_VALOR(int Referência, int Tipo_VALOR) {
        if (!TI_válido_objeto(Referência)) return false;
        if (heap_VALOR[Referência] != Tipo_VALOR) { falha_VALOR("object type mismatch"); return false; }
        return true;
    }
    static int constante_SMS(int ÍNDICE) {
        if (!cheque_constante(ÍNDICE, 1)) return 0;
        if (cadeia_Referência[ÍNDICE] != 0) return cadeia_Referência[ÍNDICE];
        int Referência = alocar_Armazenamento(1, constante_SEGUNDO_VALOR[ÍNDICE]); if (erro) return 0;
        int 끝 = 상가[ÍNDICE] + constante_SEGUNDO_VALOR[ÍNDICE], número = 상가[ÍNDICE], duração_VALOR = 0;
        while (número < 끝 && !erro) {
            int VALOR = ficheiro[número++];
            if (VALOR == 0) falha_VALOR("invalid modified UTF-8");
            else if (VALOR >= 192 && VALOR <= 223 && número < 끝) {
                int Avançar_item = ficheiro[número++];
                if ((Avançar_item & 192) != 128) falha_VALOR("invalid modified UTF-8");
                VALOR = (VALOR & 31) << 6 | Avançar_item & 63;
                if (VALOR != 0 && VALOR < 128) falha_VALOR("overlong modified UTF-8");
            } else if (VALOR >= 224 && VALOR <= 239 && número + 1 < 끝) {
                int 가 = ficheiro[número++], SEGUNDO_operando = ficheiro[número++];
                if ((가 & 192) != 128 || (SEGUNDO_operando & 192) != 128) falha_VALOR("invalid modified UTF-8");
                VALOR = (VALOR & 15) << 12 | (가 & 63) << 6 | SEGUNDO_operando & 63;
                if (VALOR < 2048) falha_VALOR("overlong modified UTF-8");
            } else if (VALOR >= 128) falha_VALOR("invalid modified UTF-8");
            heap_VALOR[Referência + 2 + duração_VALOR++] = VALOR;
        }
        heap_VALOR[Referência + 1] = duração_VALOR; cadeia_Referência[ÍNDICE] = Referência; return Referência;
    }
    static int host_caractere(String VALOR) {
        int Referência = alocar_Armazenamento(1, VALOR.length()); if (erro) return 0;
        for (int número = 0; número < VALOR.length(); número++) heap_VALOR[Referência + 2 + número] = VALOR.charAt(número);
        return Referência;
    }
    static void gravar_SMS(int Referência) {
        if (Referência == 0) { espaço_do_utilizador.Escrita("null"); return; }
        if (!objeto_VALOR(Referência, 1)) return;
        for (int número = 0; número < heap_VALOR[Referência + 1]; número++) espaço_do_utilizador.gravar_caractere_VALOR(heap_VALOR[Referência + 2 + número]);
    }
    static int dígito_caractere(int VALOR) {
        int Referência = alocar_Armazenamento(1, 11); if (erro) return 0;
        int duração_VALOR = 0;
        if (VALOR < 0) heap_VALOR[Referência + 2 + duração_VALOR++] = '-'; else VALOR = -VALOR;
        int cargo_ÍNDICE = 1000000000; boolean iniciar = false;
        while (cargo_ÍNDICE != 0) {
            int número = -(VALOR / cargo_ÍNDICE);
            if (número != 0 || iniciar || cargo_ÍNDICE == 1) { heap_VALOR[Referência + 2 + duração_VALOR++] = '0' + número; iniciar = true; }
            VALOR %= cargo_ÍNDICE; cargo_ÍNDICE /= 10;
        }
        heap_VALOR[Referência + 1] = duração_VALOR; return Referência;
    }
    static int 정수해독(int Referência) {
        if (!objeto_VALOR(Referência, 1)) return 0;
        int duração_VALOR = heap_VALOR[Referência + 1], número = 0, VALOR = 0; boolean negativo_VALOR = false;
        if (duração_VALOR > 0 && (heap_VALOR[Referência + 2] == '-' || heap_VALOR[Referência + 2] == '+')) { negativo_VALOR = heap_VALOR[Referência + 2] == '-'; número++; }
        if (número == duração_VALOR) falha_VALOR("NumberFormatException");
        for (; número < duração_VALOR && !erro; número++) {
            int dígito_VALOR = heap_VALOR[Referência + 2 + número] - '0';
            if (dígito_VALOR < 0 || dígito_VALOR > 9 || VALOR < -214748364 || VALOR == -214748364 && dígito_VALOR > (negativo_VALOR ? 8 : 7)) falha_VALOR("NumberFormatException");
            VALOR = VALOR * 10 - dígito_VALOR;
        }
        return negativo_VALOR ? VALOR : -VALOR;
    }
    static void 넣기(int VALOR, int TIPO_VALOR) {
        if (erro) return;
        if (quadro_ÍNDICE < 0 || quadro_pilha[quadro_ÍNDICE] >= método_pilha[quadro_método[quadro_ÍNDICE]]) { falha_VALOR("operand stack overflow"); return; }
        int slot_entrada = quadro_ÍNDICE * 128 + quadro_pilha[quadro_ÍNDICE]++; operando_pilha_VALOR[slot_entrada] = VALOR; operando_pilha_TIPO[slot_entrada] = TIPO_VALOR;
    }
    static int 빼기(int TIPO_VALOR) {
        if (erro) return 0;
        if (quadro_ÍNDICE < 0 || quadro_pilha[quadro_ÍNDICE] < 1) { falha_VALOR("operand stack underflow"); return 0; }
        int slot_entrada = quadro_ÍNDICE * 128 + --quadro_pilha[quadro_ÍNDICE]; tipo_de_retorno = operando_pilha_TIPO[slot_entrada];
        if (TIPO_VALOR != 0 && tipo_de_retorno != TIPO_VALOR) falha_VALOR("operand type mismatch");
        if (tipo_de_retorno == 2) proteger_VALOR(operando_pilha_VALOR[slot_entrada]);
        return operando_pilha_VALOR[slot_entrada];
    }
    static void leitura_local(int ÍNDICE, int TIPO_VALOR) {
        if (ÍNDICE >= 함수지역[quadro_método[quadro_ÍNDICE]] || ÍNDICE < 0 || local_TIPO[quadro_ÍNDICE * 128 + ÍNDICE] != TIPO_VALOR) { falha_VALOR("invalid or uninitialized local"); return; }
        넣기(local_VALOR[quadro_ÍNDICE * 128 + ÍNDICE], TIPO_VALOR);
    }
    static void gravar_local(int ÍNDICE, int TIPO_VALOR) {
        if (ÍNDICE >= 함수지역[quadro_método[quadro_ÍNDICE]] || ÍNDICE < 0) { falha_VALOR("local index out of range"); return; }
        int VALOR = 빼기(TIPO_VALOR); local_VALOR[quadro_ÍNDICE * 128 + ÍNDICE] = VALOR; local_TIPO[quadro_ÍNDICE * 128 + ÍNDICE] = TIPO_VALOR;
    }
    static int leitura_opcode_byte() {
        int posição = quadro_cargo[quadro_ÍNDICE];
        if (posição < método_START[quadro_método[quadro_ÍNDICE]] || posição >= método_encerrar[quadro_método[quadro_ÍNDICE]]) { falha_VALOR("instruction pointer out of range"); return 0; }
        quadro_cargo[quadro_ÍNDICE]++; return ficheiro[posição];
    }
    static int 명짧() { return leitura_opcode_byte() << 8 | leitura_opcode_byte(); }
    static void mover_VALOR(int posição) {
        int FUNÇÃO_VALOR = quadro_método[quadro_ÍNDICE];
        if (posição < método_START[FUNÇÃO_VALOR] || posição >= método_encerrar[FUNÇÃO_VALOR] || limite_VALOR[posição] != FUNÇÃO_VALOR + 1) falha_VALOR("invalid branch target");
        else quadro_cargo[quadro_ÍNDICE] = posição;
    }
    static void 호출(int FUNÇÃO_VALOR) {
        if (quadro_ÍNDICE % 32 == 31) { falha_VALOR("call stack limit (32)"); return; }
        int Avançar_item = quadro_ÍNDICE + 1;
        for (int número = 0; número < 128; número++) local_TIPO[Avançar_item * 128 + número] = 0;
        for (int número = método_argumento_CONT_NÚM[FUNÇÃO_VALOR] - 1; número >= 0; número--) {
            local_VALOR[Avançar_item * 128 + número] = 빼기(método_argumento_TIPO[FUNÇÃO_VALOR * 16 + número]); local_TIPO[Avançar_item * 128 + número] = método_argumento_TIPO[FUNÇÃO_VALOR * 16 + número];
        }
        if (erro) return;
        quadro_ÍNDICE = Avançar_item; inicializar_quadro[quadro_ÍNDICE] = 0; quadro_método[quadro_ÍNDICE] = FUNÇÃO_VALOR; quadro_cargo[quadro_ÍNDICE] = método_START[FUNÇÃO_VALOR]; quadro_pilha[quadro_ÍNDICE] = 0;
    }
    static void devolver_RC(int TIPO_VALOR) {
        if (TIPO_VALOR != método_devolver[quadro_método[quadro_ÍNDICE]]) { falha_VALOR("return type mismatch"); return; }
        int VALOR = TIPO_VALOR == 0 ? 0 : 빼기(TIPO_VALOR);
        if (inicializar_quadro[quadro_ÍNDICE] != 0) aula_Definição_Estado[inicializar_quadro[quadro_ÍNDICE] - 1] = 2;
        if (quadro_bloquear[quadro_ÍNDICE] != 0) { lançar_bloquear(quadro_bloquear[quadro_ÍNDICE]); quadro_bloquear[quadro_ÍNDICE] = 0; }
        quadro_ÍNDICE--; if (quadro_ÍNDICE >= em_dia_thread * 32 && TIPO_VALOR != 0) 넣기(VALOR, TIPO_VALOR);
    }
    static int[] fluxo_nome_de_arquivo = new int[64];
    static void Arquivo_fluxo_Ligar(int proprietário_VALOR, int Nome, int formato_VALOR, int comando) {
        boolean saídaTexto = Word_SMS(proprietário_VALOR, "java/io/FileOutputStream");
        int Tipo_VALOR = saídaTexto ? 6 : 5;
        if (comando == 183 && Word_SMS(Nome, "<init>")) {
            boolean 이어 = false;
            if (saídaTexto && Word_SMS(formato_VALOR, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formato_VALOR, "(Ljava/lang/String;)V")) { falha_VALOR("unsupported file stream constructor"); return; }
            int Arquivo_entrada_nome = 빼기(2), fluxo_VALOR = 빼기(2);
            if (!objeto_VALOR(Arquivo_entrada_nome, 1) || !objeto_VALOR(fluxo_VALOR, Tipo_VALOR) || erro) return;
            if (heap_VALOR[fluxo_VALOR + 3] != 0) { falha_VALOR("file stream already initialized"); return; }
            int duração_VALOR = heap_VALOR[Arquivo_entrada_nome + 1];
            if (duração_VALOR < 1 || duração_VALOR > 63) { falha_VALOR("invalid file name length"); return; }
            for (int slot_entrada = 0; slot_entrada < duração_VALOR; slot_entrada++) {
                int VALOR = heap_VALOR[Arquivo_entrada_nome + 2 + slot_entrada];
                if (VALOR < 1) { falha_VALOR("invalid file stream path"); return; }
                fluxo_nome_de_arquivo[slot_entrada] = VALOR;
            }
            fluxo_nome_de_arquivo[duração_VALOR] = 0;
            int descritor_entrada = espaço_do_utilizador.abrir_Arquivo_descritor(fluxo_nome_de_arquivo, saídaTexto ? (이어 ? 1089 : 577) : 0);
            if (descritor_entrada < 0) { falha_VALOR("FileNotFoundException: file open failed"); return; }
            heap_VALOR[fluxo_VALOR + 2] = descritor_entrada; heap_VALOR[fluxo_VALOR + 3] = 1;
            return;
        }
        if (comando != 182) { falha_VALOR("invalid file stream invocation"); return; }
        if ((saídaTexto && Word_SMS(Nome, "write") || !saídaTexto && Word_SMS(Nome, "read"))
            && (Word_SMS(formato_VALOR, saídaTexto ? "([B)V" : "([B)I") || Word_SMS(formato_VALOR, saídaTexto ? "([BII)V" : "([BII)I"))) {
            boolean recortar_VALOR = Word_SMS(formato_VALOR, saídaTexto ? "([BII)V" : "([BII)I");
            int entrada_CONT_NÚM_8f7753a1 = recortar_VALOR ? 빼기(1) : 0, 시작점 = recortar_VALOR ? 빼기(1) : 0, dados_MATRIZ = 빼기(2), objeto_Referência = 빼기(2);
            if (!objeto_VALOR(dados_MATRIZ, 20) || !objeto_VALOR(objeto_Referência, Tipo_VALOR)) return;
            if (!recortar_VALOR) entrada_CONT_NÚM_8f7753a1 = heap_VALOR[dados_MATRIZ + 1];
            if (시작점 < 0 || entrada_CONT_NÚM_8f7753a1 < 0 || 시작점 > heap_VALOR[dados_MATRIZ + 1] - entrada_CONT_NÚM_8f7753a1) { 예외던짐(6, "file buffer bounds"); return; }
            if (heap_VALOR[objeto_Referência + 3] == 0 || heap_VALOR[objeto_Referência + 2] < 0) { falha_VALOR("IOException: stream closed"); return; }
            int concluído_CONT_NÚM = 0;
            while (concluído_CONT_NÚM < entrada_CONT_NÚM_8f7753a1 && !erro) {
                int 반환값 = saídaTexto ? espaço_do_utilizador.파일한바이트쓰기(heap_VALOR[objeto_Referência + 2], heap_VALOR[dados_MATRIZ + 2 + 시작점 + concluído_CONT_NÚM]) : espaço_do_utilizador.파일한바이트읽기(heap_VALOR[objeto_Referência + 2]);
                if (반환값 < 0) { falha_VALOR(saídaTexto ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!saídaTexto && 반환값 == 256) break;
                if (!saídaTexto) heap_VALOR[dados_MATRIZ + 2 + 시작점 + concluído_CONT_NÚM] = (byte)반환값;
                concluído_CONT_NÚM++;
            }
            if (!saídaTexto) 넣기(entrada_CONT_NÚM_8f7753a1 != 0 && concluído_CONT_NÚM == 0 ? -1 : concluído_CONT_NÚM, 1);
            return;
        }
        if (saídaTexto && Word_SMS(Nome, "flush") && Word_SMS(formato_VALOR, "()V")) { int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, Tipo_VALOR) && heap_VALOR[objeto_Referência + 2] < 0) falha_VALOR("IOException: stream closed"); return; }
        int Acção = -1, VALOR = 0;
        if (Word_SMS(Nome, "close") && Word_SMS(formato_VALOR, "()V")) Acção = 0;
        if (!saídaTexto && Word_SMS(Nome, "read") && Word_SMS(formato_VALOR, "()I")) Acção = 1;
        if (saídaTexto && Word_SMS(Nome, "write") && Word_SMS(formato_VALOR, "(I)V")) { Acção = 2; VALOR = 빼기(1); }
        if (Acção < 0) { falha_VALOR("unsupported file stream method"); return; }
        int fluxo_VALOR = 빼기(2);
        if (!objeto_VALOR(fluxo_VALOR, Tipo_VALOR) || erro) return;
        if (heap_VALOR[fluxo_VALOR + 3] == 0) { falha_VALOR("uninitialized file stream"); return; }
        int descritor_entrada = heap_VALOR[fluxo_VALOR + 2];
        if (Acção == 0) {
            if (descritor_entrada >= 0 && espaço_do_utilizador.Close_Arquivo_descritor(descritor_entrada) < 0) falha_VALOR("IOException: close failed");
            heap_VALOR[fluxo_VALOR + 2] = -1; return;
        }
        if (descritor_entrada < 0) { falha_VALOR("IOException: stream closed"); return; }
        if (Acção == 1) {
            int resultado = espaço_do_utilizador.파일한바이트읽기(descritor_entrada);
            if (resultado < -1) falha_VALOR("IOException: read failed"); else 넣기(resultado == 256 ? -1 : resultado, 1);
        } else if (espaço_do_utilizador.파일한바이트쓰기(descritor_entrada, VALOR) != 1) falha_VALOR("IOException: write failed");
    }
    static void Ligar_método(int ÍNDICE, int comando) {
        if (ÍNDICE <= 0 || ÍNDICE >= constante_tag.length || (constante_tag[ÍNDICE] != 10 && constante_tag[ÍNDICE] != 11)) { falha_VALOR("invalid method reference"); return; }
        int proprietário_VALOR = nome_da_classe_SMS(상가[ÍNDICE]), Nome = Referência_nome(constante_SEGUNDO_VALOR[ÍNDICE]), formato_VALOR = tipo_de_referência(constante_SEGUNDO_VALOR[ÍNDICE]);
        if (erro) return;
        if (기본호출(proprietário_VALOR, Nome, formato_VALOR, comando)) return;
        if (Word_SMS(proprietário_VALOR, "java/io/FileInputStream") || Word_SMS(proprietário_VALOR, "java/io/FileOutputStream")) {
            Arquivo_fluxo_Ligar(proprietário_VALOR, Nome, formato_VALOR, comando); return;
        }
        if (comando == 184 && Word_SMS(proprietário_VALOR, "java/lang/Integer") && Word_SMS(Nome, "parseInt") && Word_SMS(formato_VALOR, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (comando == 182 && Word_SMS(proprietário_VALOR, "java/io/PrintStream") && (Word_SMS(Nome, "println") || Word_SMS(Nome, "print"))) {
            int TIPO_VALOR = 0, VALOR = 0;
            if (Word_SMS(formato_VALOR, "(I)V")) { TIPO_VALOR = 1; VALOR = 빼기(1); }
            else if (Word_SMS(formato_VALOR, "(Z)V")) { TIPO_VALOR = 2; VALOR = 빼기(1); }
            else if (Word_SMS(formato_VALOR, "(C)V")) { TIPO_VALOR = 3; VALOR = 빼기(1); }
            else if (Word_SMS(formato_VALOR, "(Ljava/lang/String;)V")) { TIPO_VALOR = 4; VALOR = 빼기(2); }
            else if (!Word_SMS(formato_VALOR, "()V") || !Word_SMS(Nome, "println")) falha_VALOR("unsupported print descriptor");
            if (빼기(2) != -1) falha_VALOR("invalid PrintStream receiver");
            if (erro) return;
            if (TIPO_VALOR == 1) FerramentasJava.gravar_número(VALOR);
            if (TIPO_VALOR == 2) espaço_do_utilizador.Escrita(VALOR == 0 ? "false" : "true");
            if (TIPO_VALOR == 3) espaço_do_utilizador.gravar_caractere_VALOR(VALOR & 65535);
            if (TIPO_VALOR == 4) gravar_SMS(VALOR);
            if (Word_SMS(Nome, "println")) espaço_do_utilizador.gravar_caractere_VALOR(10);
            return;
        }
        if (comando == 182 && Word_SMS(proprietário_VALOR, "java/lang/String")) {
            if (Word_SMS(Nome, "length") && Word_SMS(formato_VALOR, "()I")) {
                int Referência = 빼기(2); if (objeto_VALOR(Referência, 1)) 넣기(heap_VALOR[Referência + 1], 1); return;
            }
            if (Word_SMS(Nome, "charAt") && Word_SMS(formato_VALOR, "(I)C")) {
                int subscrito_VALOR = 빼기(1), Referência = 빼기(2);
                if (objeto_VALOR(Referência, 1)) {
                    if (subscrito_VALOR < 0 || subscrito_VALOR >= heap_VALOR[Referência + 1]) falha_VALOR("StringIndexOutOfBoundsException"); else 넣기(heap_VALOR[Referência + 2 + subscrito_VALOR], 1);
                }
                return;
            }
        }
        if (Word_SMS(proprietário_VALOR, "java/lang/StringBuilder")) {
            if (comando == 183 && Word_SMS(Nome, "<init>") && Word_SMS(formato_VALOR, "()V")) { objeto_VALOR(빼기(2), 4); return; }
            if (comando == 182 && Word_SMS(Nome, "toString") && Word_SMS(formato_VALOR, "()Ljava/lang/String;")) {
                int Referência = 빼기(2); if (objeto_VALOR(Referência, 4)) 넣기(heap_VALOR[Referência + 2] == 0 ? host_caractere("") : heap_VALOR[Referência + 2], 2); return;
            }
            if (comando == 182 && Word_SMS(Nome, "append")) {
                int texto = 0;
                if (Word_SMS(formato_VALOR, "(I)Ljava/lang/StringBuilder;")) texto = dígito_caractere(빼기(1));
                else if (Word_SMS(formato_VALOR, "(Z)Ljava/lang/StringBuilder;")) texto = host_caractere(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formato_VALOR, "(C)Ljava/lang/StringBuilder;")) {
                    int VALOR = 빼기(1); texto = alocar_Armazenamento(1, 1); if (!erro) heap_VALOR[texto + 2] = VALOR & 65535;
                }
                else if (Word_SMS(formato_VALOR, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { texto = 빼기(2); if (texto == 0) texto = host_caractere("null"); }
                else { falha_VALOR("unsupported StringBuilder append"); return; }
                int Referência = 빼기(2); if (!objeto_VALOR(Referência, 4) || !objeto_VALOR(texto, 1)) return;
                int câmera_frontal_VALOR = heap_VALOR[Referência + 2], câmera_frontal_VALOR_duração = câmera_frontal_VALOR == 0 ? 0 : heap_VALOR[câmera_frontal_VALOR + 1], BACK_VALOR_duração = heap_VALOR[texto + 1];
                int 새글 = alocar_Armazenamento(1, câmera_frontal_VALOR_duração + BACK_VALOR_duração); if (erro) return;
                for (int número = 0; número < câmera_frontal_VALOR_duração; número++) heap_VALOR[새글 + 2 + número] = heap_VALOR[câmera_frontal_VALOR + 2 + número];
                for (int número = 0; número < BACK_VALOR_duração; número++) heap_VALOR[새글 + 2 + câmera_frontal_VALOR_duração + número] = heap_VALOR[texto + 2 + número];
                heap_VALOR[Referência + 2] = 새글; 넣기(Referência, 2); return;
            }
        }
        int aula_Definição = PROCURAR_aula_Definição(proprietário_VALOR); if (aula_Definição < 0 || erro) return;
        int Arquivo_ÍNDICE = PROCURAR_método(aula_Definição, Nome, formato_VALOR);
        if (Arquivo_ÍNDICE < 0) {
            for (int ponto_de_código = aula_Definição, entrada_CONT_NÚM_8f7753a1 = 0; ponto_de_código >= 0 && entrada_CONT_NÚM_8f7753a1 < 16; entrada_CONT_NÚM_8f7753a1++, ponto_de_código = pai_aula(ponto_de_código))
                if (Word_SMS(aula_Definição_pai[ponto_de_código], "java/lang/Thread")) { 가닥호출(Nome, formato_VALOR, comando); return; }
            falha_VALOR("NoSuchMethodError"); return;
        }
        if (((método_acesso[Arquivo_ÍNDICE] & 8) != 0) != (comando == 184)) { falha_VALOR("method static/instance mismatch"); return; }
        if (comando == 184) { if (!inicializar(método_proprietário[Arquivo_ÍNDICE], quadro_instrução[quadro_ÍNDICE])) return; }
        else {
            int leitura_cursor = quadro_pilha[quadro_ÍNDICE] - método_argumento_CONT_NÚM[Arquivo_ÍNDICE];
            if (leitura_cursor < 0 || operando_pilha_TIPO[quadro_ÍNDICE * 128 + leitura_cursor] != 2) { falha_VALOR("invalid method receiver"); return; }
            int objeto_Referência = operando_pilha_VALOR[quadro_ÍNDICE * 128 + leitura_cursor];
            if (!TI_válido_objeto(objeto_Referência)) return;
            if (heap_VALOR[objeto_Referência] < 32 || !종포함(heap_VALOR[objeto_Referência] - 32, proprietário_VALOR)) { falha_VALOR("method receiver type mismatch"); return; }
            if (comando != 183) Arquivo_ÍNDICE = PROCURAR_método(heap_VALOR[objeto_Referência] - 32, Nome, formato_VALOR);
        }
        if (Arquivo_ÍNDICE < 0 || (método_acesso[Arquivo_ÍNDICE] & 0x400) != 0) { falha_VALOR("AbstractMethodError"); return; }
        int bloquear_Referência = 0;
        if ((método_acesso[Arquivo_ÍNDICE] & 32) != 0) {
            if (comando == 184) { int ponto_de_código = método_proprietário[Arquivo_ÍNDICE]; if (aula_bloquear[ponto_de_código] == 0) aula_bloquear[ponto_de_código] = alocar_Armazenamento(8, 0); bloquear_Referência = aula_bloquear[ponto_de_código]; }
            else bloquear_Referência = operando_pilha_VALOR[quadro_ÍNDICE * 128 + quadro_pilha[quadro_ÍNDICE] - método_argumento_CONT_NÚM[Arquivo_ÍNDICE]];
            if (!잠금얻기(bloquear_Referência)) { if (!erro) quadro_cargo[quadro_ÍNDICE] = quadro_instrução[quadro_ÍNDICE]; return; }
        }
        호출(Arquivo_ÍNDICE); if (!erro) quadro_bloquear[quadro_ÍNDICE] = bloquear_Referência;
    }
    static boolean 배열저장가능(int MATRIZ_Referência, int dados_VALOR) {
        if (dados_VALOR == 0 || elemento_da_matriz[MATRIZ_Referência] == 0) return true;
        boolean 성공여부 = elemento_da_matriz[MATRIZ_Referência] == -1 ? (dados_VALOR > 0 && dados_VALOR < heap_encerrar_cargo && heap_VALOR[dados_VALOR] == 1) : 맞는객체(dados_VALOR, elemento_da_matriz[MATRIZ_Referência]);
        if (!성공여부 && !erro) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int MATRIZ_slot(int Referência, int subscrito_VALOR, int TIPO_VALOR) {
        if (!objeto_VALOR(Referência, TIPO_VALOR)) return 0;
        if (subscrito_VALOR < 0 || subscrito_VALOR >= heap_VALOR[Referência + 1]) { falha_VALOR("ArrayIndexOutOfBoundsException"); return 0; }
        return Referência + 2 + subscrito_VALOR;
    }
    static void Executar_comando() {
        int 남음 = 500000, fragmento_VALOR = 100;
        while (true) {
            if (erro) { if (던진객체 != 0) alça_exceção(); if (erro || quadro_ÍNDICE < em_dia_thread * 32) break; }
            if (quadro_ÍNDICE < em_dia_thread * 32 || solicitação_de_alteração || --fragmento_VALOR == 0) { if (!mudar_thread()) break; fragmento_VALOR = 100; }
            if (quadro_ÍNDICE == 0 && aula_Definição_Estado[entrada_aula_Definição] != 2 && !inicializar(entrada_aula_Definição, quadro_cargo[quadro_ÍNDICE])) continue;
            if (quadro_ÍNDICE == em_dia_thread * 32 && em_dia_thread != 0 && (método_acesso[quadro_método[quadro_ÍNDICE]] & 32) != 0 && quadro_bloquear[quadro_ÍNDICE] == 0) {
                int objeto_Referência = thread_alvo[em_dia_thread]; if (!잠금얻기(objeto_Referência)) { if (erro) break; continue; } quadro_bloquear[quadro_ÍNDICE] = objeto_Referência;
            }
            잠시수 = 0;
            if (--남음 == 0) { falha_VALOR("instruction limit (500000)"); break; }
            int iniciar = quadro_cargo[quadro_ÍNDICE]; quadro_instrução[quadro_ÍNDICE] = iniciar; int VALOR = leitura_opcode_byte();
            if (erro) break;
            if (VALOR == 0) continue;
            if (VALOR == 1) { 넣기(0, 2); continue; }
            if (VALOR >= 2 && VALOR <= 8) { 넣기(VALOR - 3, 1); continue; }
            if (VALOR == 16) { 넣기((byte)leitura_opcode_byte(), 1); continue; }
            if (VALOR == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALOR == 18 || VALOR == 19) {
                int número = método_proprietário[quadro_método[quadro_ÍNDICE]] * 512 + (VALOR == 18 ? leitura_opcode_byte() : 명짧());
                if (número <= 0 || número >= constante_tag.length) falha_VALOR("invalid ldc constant");
                else if (constante_tag[número] == 3) 넣기(상가[número], 1);
                else if (constante_tag[número] == 8) 넣기(constante_SMS(상가[número]), 2);
                else falha_VALOR("unsupported ldc constant");
                continue;
            }
            if (VALOR == 21 || VALOR == 25) { leitura_local(leitura_opcode_byte(), VALOR == 21 ? 1 : 2); continue; }
            if (VALOR >= 26 && VALOR <= 29) { leitura_local(VALOR - 26, 1); continue; }
            if (VALOR >= 42 && VALOR <= 45) { leitura_local(VALOR - 42, 2); continue; }
            if (VALOR == 54 || VALOR == 58) { gravar_local(leitura_opcode_byte(), VALOR == 54 ? 1 : 2); continue; }
            if (VALOR >= 59 && VALOR <= 62) { gravar_local(VALOR - 59, 1); continue; }
            if (VALOR >= 75 && VALOR <= 78) { gravar_local(VALOR - 75, 2); continue; }
            if (VALOR == 46 || VALOR >= 50 && VALOR <= 53) {
                int entrada_cargo_206f1c6d = 빼기(1), objeto_Referência = 빼기(2), área_CÓDIGO = VALOR == 46 ? 2 : VALOR == 50 ? 3 : VALOR == 51 ? 20 : VALOR == 52 ? 22 : 23;
                if (VALOR == 51 && objeto_Referência > 0 && objeto_Referência < heap_encerrar_cargo && heap_VALOR[objeto_Referência] == 21) área_CÓDIGO = 21;
                int leitura_cursor = MATRIZ_slot(objeto_Referência, entrada_cargo_206f1c6d, área_CÓDIGO); if (!erro) 넣기(heap_VALOR[leitura_cursor], VALOR == 50 ? 2 : 1); continue;
            }
            if (VALOR == 79 || VALOR >= 83 && VALOR <= 86) {
                int entrada_Referência = 빼기(VALOR == 83 ? 2 : 1), entrada_cargo_206f1c6d = 빼기(1), objeto_Referência = 빼기(2), área_CÓDIGO = VALOR == 79 ? 2 : VALOR == 83 ? 3 : VALOR == 84 ? 20 : VALOR == 85 ? 22 : 23;
                if (VALOR == 84 && objeto_Referência > 0 && objeto_Referência < heap_encerrar_cargo && heap_VALOR[objeto_Referência] == 21) área_CÓDIGO = 21;
                int leitura_cursor = MATRIZ_slot(objeto_Referência, entrada_cargo_206f1c6d, área_CÓDIGO);
                if (!erro && área_CÓDIGO == 3 && !배열저장가능(objeto_Referência, entrada_Referência)) continue;
                if (!erro) heap_VALOR[leitura_cursor] = área_CÓDIGO == 20 ? (byte)entrada_Referência : área_CÓDIGO == 21 ? entrada_Referência & 1 : área_CÓDIGO == 22 ? (char)entrada_Referência : área_CÓDIGO == 23 ? (short)entrada_Referência : entrada_Referência;
                continue;
            }
            if (VALOR >= 87 && VALOR <= 95) { pilha_instrução(VALOR); continue; }
            if (VALOR == 96 || VALOR == 100 || VALOR == 104 || VALOR == 108 || VALOR == 112 || VALOR == 120
                || VALOR == 122 || VALOR == 124 || VALOR == 126 || VALOR == 128 || VALOR == 130) {
                int SEGUNDO_operando = 빼기(1), 가 = 빼기(1), resultado = 0;
                if ((VALOR == 108 || VALOR == 112) && SEGUNDO_operando == 0) { falha_VALOR("ArithmeticException: / by zero"); continue; }
                if (VALOR == 96) resultado = 가 + SEGUNDO_operando;
                if (VALOR == 100) resultado = 가 - SEGUNDO_operando;
                if (VALOR == 104) resultado = 가 * SEGUNDO_operando;
                if (VALOR == 108) resultado = 가 / SEGUNDO_operando;
                if (VALOR == 112) resultado = 가 % SEGUNDO_operando;
                if (VALOR == 120) resultado = 가 << SEGUNDO_operando;
                if (VALOR == 122) resultado = 가 >> SEGUNDO_operando;
                if (VALOR == 124) resultado = 가 >>> SEGUNDO_operando;
                if (VALOR == 126) resultado = 가 & SEGUNDO_operando;
                if (VALOR == 128) resultado = 가 | SEGUNDO_operando;
                if (VALOR == 130) resultado = 가 ^ SEGUNDO_operando;
                넣기(resultado, 1); continue;
            }
            if (VALOR == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALOR == 132) {
                int local_Scope = leitura_opcode_byte(), incremento_etapa = (byte)leitura_opcode_byte(); leitura_local(local_Scope, 1); 넣기(빼기(1) + incremento_etapa, 1); gravar_local(local_Scope, 1); continue;
            }
            if (VALOR >= 145 && VALOR <= 147) {
                int número = 빼기(1); 넣기(VALOR == 145 ? (byte)número : VALOR == 146 ? (char)número : (short)número, 1); continue;
            }
            if (VALOR >= 153 && VALOR <= 167 || VALOR == 198 || VALOR == 199) {
                int destino_VALOR = iniciar + (short)명짧(); boolean 갈까 = VALOR == 167;
                if (VALOR >= 153 && VALOR <= 158) {
                    int número = 빼기(1); 갈까 = VALOR == 153 ? número == 0 : VALOR == 154 ? número != 0 : VALOR == 155 ? número < 0 : VALOR == 156 ? número >= 0 : VALOR == 157 ? número > 0 : número <= 0;
                } else if (VALOR >= 159 && VALOR <= 166) {
                    int SEGUNDO_operando = 빼기(VALOR >= 165 ? 2 : 1), 가 = 빼기(VALOR >= 165 ? 2 : 1);
                    갈까 = VALOR == 159 || VALOR == 165 ? 가 == SEGUNDO_operando : VALOR == 160 || VALOR == 166 ? 가 != SEGUNDO_operando : VALOR == 161 ? 가 < SEGUNDO_operando : VALOR == 162 ? 가 >= SEGUNDO_operando : VALOR == 163 ? 가 > SEGUNDO_operando : 가 <= SEGUNDO_operando;
                } else if (VALOR == 198 || VALOR == 199) { int número = 빼기(2); 갈까 = VALOR == 198 ? número == 0 : número != 0; }
                if (갈까) mover_VALOR(destino_VALOR); continue;
            }
            if (VALOR == 172 || VALOR == 176 || VALOR == 177) { devolver_RC(VALOR == 172 ? 1 : VALOR == 176 ? 2 : 0); continue; }
            if (VALOR >= 178 && VALOR <= 181) { 필드호출(leitura_opcode_constante(), VALOR, iniciar); continue; }
            if (VALOR >= 182 && VALOR <= 185) {
                int 부호값 = leitura_opcode_constante();
                if (VALOR == 185) { int total_CONT_NÚM = leitura_opcode_byte(); if (total_CONT_NÚM == 0 || leitura_opcode_byte() != 0) { falha_VALOR("invalid invokeinterface operands"); continue; } }
                Ligar_método(부호값, VALOR); continue;
            }
            if (VALOR == 187) { 새객체(nome_da_classe_SMS(leitura_opcode_constante()), iniciar); continue; }
            if (VALOR == 188 || VALOR == 189) {
                int área_CÓDIGO = 3, componente = 0;
                if (VALOR == 188) { int 임시값 = leitura_opcode_byte(); área_CÓDIGO = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else componente = nome_da_classe_SMS(leitura_opcode_constante());
                if (área_CÓDIGO == 0) { falha_VALOR("unsupported primitive array type"); continue; }
                int válido_duração = 빼기(1), objeto_Referência = alocar_Armazenamento(área_CÓDIGO, válido_duração); if (!erro) elemento_da_matriz[objeto_Referência] = componente; 넣기(objeto_Referência, 2); continue;
            }
            if (VALOR == 190) {
                int objeto_Referência = 빼기(2);
                if (TI_válido_objeto(objeto_Referência)) { int Comparação_cargo = heap_VALOR[objeto_Referência]; if (Comparação_cargo != 2 && Comparação_cargo != 3 && (Comparação_cargo < 20 || Comparação_cargo > 23)) falha_VALOR("not an array"); else 넣기(heap_VALOR[objeto_Referência + 1], 1); }
                continue;
            }
            if (VALOR == 191) {
                int objeto_Referência = 빼기(2); if (TI_válido_objeto(objeto_Referência)) { if (heap_VALOR[objeto_Referência] != 9) falha_VALOR("athrow requires supported Throwable"); else { 던진객체 = objeto_Referência; erro = true; } }
                continue;
            }
            if (VALOR == 192 || VALOR == 193) {
                int nome_constante = nome_da_classe_SMS(leitura_opcode_constante()), objeto_Referência = 빼기(2); boolean set = 맞는객체(objeto_Referência, nome_constante);
                if (VALOR == 193) 넣기(objeto_Referência != 0 && set ? 1 : 0, 1);
                else { if (!set && !erro) falha_VALOR("ClassCastException"); 넣기(objeto_Referência, 2); }
                continue;
            }
            if (VALOR == 170 || VALOR == 171) {
                int leitura_cursor = iniciar + 1, Arquivo_ÍNDICE = quadro_método[quadro_ÍNDICE], Chave_Referência = 빼기(1);
                while ((leitura_cursor - método_START[Arquivo_ÍNDICE]) % 4 != 0) leitura_cursor++;
                int alvo_email = cargo_inteiro(leitura_cursor);
                if (VALOR == 170) { int 낮은값 = cargo_inteiro(leitura_cursor + 4), 높은값 = cargo_inteiro(leitura_cursor + 8); if (Chave_Referência >= 낮은값 && Chave_Referência <= 높은값) alvo_email = cargo_inteiro(leitura_cursor + 12 + (Chave_Referência - 낮은값) * 4); }
                else { int total_CONT_NÚM = cargo_inteiro(leitura_cursor + 4); for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < total_CONT_NÚM; Loop_ÍNDICE++) if (cargo_inteiro(leitura_cursor + 8 + Loop_ÍNDICE * 8) == Chave_Referência) alvo_email = cargo_inteiro(leitura_cursor + 12 + Loop_ÍNDICE * 8); }
                mover_VALOR(iniciar + alvo_email); continue;
            }
            if (VALOR == 200) { mover_VALOR(iniciar + cargo_inteiro(iniciar + 1)); continue; }
            if (VALOR == 194 || VALOR == 195) {
                int objeto_Referência = 빼기(2);
                if (VALOR == 195) lançar_bloquear(objeto_Referência);
                else if (!잠금얻기(objeto_Referência) && !erro) { 넣기(objeto_Referência, 2); quadro_cargo[quadro_ÍNDICE] = iniciar; }
                continue;
            }
            if (VALOR == 196) {
                int comando_CÓDIGO = leitura_opcode_byte(), entrada_cargo_206f1c6d = 명짧();
                if (comando_CÓDIGO == 21 || comando_CÓDIGO == 25) leitura_local(entrada_cargo_206f1c6d, comando_CÓDIGO == 21 ? 1 : 2);
                else if (comando_CÓDIGO == 54 || comando_CÓDIGO == 58) gravar_local(entrada_cargo_206f1c6d, comando_CÓDIGO == 54 ? 1 : 2);
                else if (comando_CÓDIGO == 132) { int DELTA_VALOR = (short)명짧(); leitura_local(entrada_cargo_206f1c6d, 1); 넣기(빼기(1) + DELTA_VALOR, 1); gravar_local(entrada_cargo_206f1c6d, 1); }
                else falha_VALOR("unsupported wide opcode");
                continue;
            }
            falha_VALOR("unsupported bytecode");
        }
    }
    static int PROCURAR_aula_Definição(int Nome) {
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < aula_Definição_CONT_NÚM; Loop_ÍNDICE++) if (aula_Definição_nome[Loop_ÍNDICE] != 0 && 같은말(aula_Definição_nome[Loop_ÍNDICE], Nome)) return Loop_ÍNDICE;
        return carga_aula_Definição(constante_SMS(Nome));
    }
    static int carga_aula_Definição(int nome_cadeia) {
        if (!objeto_VALOR(nome_cadeia, 1)) return -1;
        int duração_VALOR = heap_VALOR[nome_cadeia + 1];
        if (duração_VALOR < 1 || duração_VALOR > 505 || aula_Definição_CONT_NÚM == 16) { falha_VALOR("class name/count limit"); return -1; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < duração_VALOR; Loop_ÍNDICE++) { int ponto_de_código = heap_VALOR[nome_cadeia + 2 + Loop_ÍNDICE]; nome_de_arquivo_SMS[Loop_ÍNDICE] = ponto_de_código == '/' ? '.' : ponto_de_código; }
        nome_de_arquivo_SMS[duração_VALOR] = '.'; nome_de_arquivo_SMS[duração_VALOR + 1] = 'c'; nome_de_arquivo_SMS[duração_VALOR + 2] = 'l'; nome_de_arquivo_SMS[duração_VALOR + 3] = 'a'; nome_de_arquivo_SMS[duração_VALOR + 4] = 's'; nome_de_arquivo_SMS[duração_VALOR + 5] = 's'; nome_de_arquivo_SMS[duração_VALOR + 6] = 0;
        int Tamanho = espaço_do_utilizador.leitura_Arquivo(nome_de_arquivo_SMS, arquivo_temporário);
        if (Tamanho < 0) { falha_VALOR("ClassNotFoundException"); return -1; }
        int aula_Definição = aula_Definição_CONT_NÚM++; aula_Definição_dimensionar[aula_Definição] = Tamanho;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) ficheiro[aula_Definição * 16384 + Loop_ÍNDICE] = arquivo_temporário[Loop_ÍNDICE];
        leitura_aula(aula_Definição); if (erro) return -1;
        int real_dados = constante_SMS(aula_Definição_nome[aula_Definição]);
        if (!textos_iguais(real_dados, nome_cadeia, true)) { falha_VALOR("class name does not match file"); return -1; }
        int pai_VALOR = aula_Definição_pai[aula_Definição];
        if (pai_VALOR != 0 && !Word_SMS(pai_VALOR, "java/lang/Object") && !Word_SMS(pai_VALOR, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 repetir_VALOR 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = PROCURAR_aula_Definição(pai_VALOR);
            if (erro || 위 < 0) return -1;
            int leitura_cursor = 위, fase_CONT_NÚM = 0;
            while (leitura_cursor >= 0 && fase_CONT_NÚM++ < 16) {
                if (leitura_cursor == aula_Definição) { falha_VALOR("cyclic inheritance"); return -1; }
                leitura_cursor = pai_aula(leitura_cursor);
            }
            int 시작변위 = aula_slot_CONT_NÚM[위];
            for (int Arquivo_ÍNDICE = 0; Arquivo_ÍNDICE < slot_CONT_NÚM; Arquivo_ÍNDICE++) if (slot_proprietário[Arquivo_ÍNDICE] == aula_Definição && (slot_Permissões[Arquivo_ÍNDICE] & 8) == 0) slot_cargo[Arquivo_ÍNDICE] += 시작변위;
            aula_slot_CONT_NÚM[aula_Definição] += 시작변위;
        }
        return aula_Definição;
    }
    static int pai_aula(int aula_Definição) {
        int Nome = aula_Definição_pai[aula_Definição];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < aula_Definição_CONT_NÚM; Loop_ÍNDICE++) if (Nome != 0 && aula_Definição_nome[Loop_ÍNDICE] != 0 && 같은말(aula_Definição_nome[Loop_ÍNDICE], Nome)) return Loop_ÍNDICE;
        return -1;
    }
    static int PROCURAR_método(int aula_Definição, int Nome, int formato_VALOR) {
        for (int 깊이 = 0; aula_Definição >= 0 && 깊이 < 16; 깊이++, aula_Definição = pai_aula(aula_Definição)) {
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < método_CONT_NÚM; Loop_ÍNDICE++) if (método_proprietário[Loop_ÍNDICE] == aula_Definição && 같은말(método_nome_SMS[Loop_ÍNDICE], Nome) && 같은말(método_TIPO[Loop_ÍNDICE], formato_VALOR)) return Loop_ÍNDICE;
        }
        return -1;
    }
    static int nome_método(int aula_Definição, String Nome, String formato_VALOR) {
        for (int 깊이 = 0; aula_Definição >= 0 && 깊이 < 16; 깊이++, aula_Definição = pai_aula(aula_Definição))
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < método_CONT_NÚM; Loop_ÍNDICE++) if (método_proprietário[Loop_ÍNDICE] == aula_Definição && Word_SMS(método_nome_SMS[Loop_ÍNDICE], Nome) && Word_SMS(método_TIPO[Loop_ÍNDICE], formato_VALOR)) return Loop_ÍNDICE;
        return -1;
    }
    static int TIPO_Tipo(int Nome) { return ficheiro[상가[Nome]] == 'L' || ficheiro[상가[Nome]] == '[' ? 2 : 1; }
    static boolean inicializar(int aula_Definição, int comando_START) {
        if (aula_Definição < 0 || erro) return false;
        if (aula_Definição_Estado[aula_Definição] == 3) { falha_VALOR("NoClassDefFoundError: initialization failed"); return false; }
        if (aula_Definição_Estado[aula_Definição] == 1 && aula_thread[aula_Definição] != em_dia_thread) { quadro_cargo[quadro_ÍNDICE] = comando_START; solicitação_de_alteração = true; return false; }
        if (aula_Definição_Estado[aula_Definição] != 0) return true;
        int 위 = pai_aula(aula_Definição);
        if (위 >= 0 && !inicializar(위, comando_START)) return false;
        aula_Definição_Estado[aula_Definição] = 1; aula_thread[aula_Definição] = em_dia_thread;
        if (inicializar_aula_Definição[aula_Definição] != 0) {
            quadro_cargo[quadro_ÍNDICE] = comando_START;
            호출(inicializar_aula_Definição[aula_Definição] - 1); if (!erro) inicializar_quadro[quadro_ÍNDICE] = aula_Definição + 1;
            return false;
        }
        aula_Definição_Estado[aula_Definição] = 2; return true;
    }
    static void 필드호출(int ÍNDICE, int comando, int iniciar) {
        if (!cheque_constante(ÍNDICE, 9)) return;
        int proprietário_VALOR = nome_da_classe_SMS(상가[ÍNDICE]), Nome = Referência_nome(constante_SEGUNDO_VALOR[ÍNDICE]), formato_VALOR = tipo_de_referência(constante_SEGUNDO_VALOR[ÍNDICE]);
        if (Word_SMS(proprietário_VALOR, "java/lang/System") && (Word_SMS(Nome, "out") || Word_SMS(Nome, "err")) && Word_SMS(formato_VALOR, "Ljava/io/PrintStream;") && comando == 178) { 넣기(-1, 2); return; }
        int aula_Definição = PROCURAR_aula_Definição(proprietário_VALOR); if (aula_Definição < 0 || erro) return;
        int 찾음 = -1;
        for (int leitura_cursor = aula_Definição, 깊이 = 0; leitura_cursor >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, leitura_cursor = pai_aula(leitura_cursor))
            for (int Arquivo_ÍNDICE = 0; Arquivo_ÍNDICE < slot_CONT_NÚM; Arquivo_ÍNDICE++) if (slot_proprietário[Arquivo_ÍNDICE] == leitura_cursor && 같은말(slot_nome[Arquivo_ÍNDICE], Nome) && 같은말(slot_TIPO[Arquivo_ÍNDICE], formato_VALOR)) 찾음 = Arquivo_ÍNDICE;
        if (찾음 < 0) { falha_VALOR("NoSuchFieldError"); return; }
        boolean estático_VALOR = comando == 178 || comando == 179;
        if (estático_VALOR != ((slot_Permissões[찾음] & 8) != 0)) { falha_VALOR("field static/instance mismatch"); return; }
        if (estático_VALOR && !inicializar(slot_proprietário[찾음], iniciar)) return;
        int TIPO_VALOR = TIPO_Tipo(formato_VALOR), VALOR = 0;
        if (comando == 179 || comando == 181) VALOR = 빼기(TIPO_VALOR);
        if (estático_VALOR) { if (comando == 178) 넣기(slot_dados[찾음], TIPO_VALOR); else if (!erro) slot_dados[찾음] = VALOR; return; }
        int objeto_Referência = 빼기(2);
        if (!TI_válido_objeto(objeto_Referência)) return;
        if (heap_VALOR[objeto_Referência] < 32 || !종포함(heap_VALOR[objeto_Referência] - 32, proprietário_VALOR)) { falha_VALOR("field receiver type mismatch"); return; }
        int 보관칸 = objeto_Referência + 2 + slot_cargo[찾음];
        if (comando == 180) 넣기(heap_VALOR[보관칸], TIPO_VALOR);
        else if (!erro) { heap_VALOR[보관칸] = VALOR; heap_Referência[보관칸] = TIPO_VALOR == 2 ? 1 : 0; }
    }
    static boolean 종포함(int aula_Definição, int Nome) {
        for (int 중첩깊이 = 0; aula_Definição >= 0 && 중첩깊이 < 16; 중첩깊이++, aula_Definição = pai_aula(aula_Definição)) {
            if (같은말(aula_Definição_nome[aula_Definição], Nome) || (aula_Definição_pai[aula_Definição] != 0 && 같은말(aula_Definição_pai[aula_Definição], Nome))) return true;
            for (int interna_cargo = 0; interna_cargo < aula_interface_CONT_NÚM[aula_Definição]; interna_cargo++) if (같은말(aula_interface[aula_Definição * 16 + interna_cargo], Nome)) return true;
        }
        return false;
    }
    static boolean textos_iguais(int 첫값, int byte_dados, boolean caminho) {
        if (첫값 == byte_dados) return true;
        if (첫값 <= 0 || byte_dados <= 0 || heap_VALOR[첫값] != 1 || heap_VALOR[byte_dados] != 1 || heap_VALOR[첫값 + 1] != heap_VALOR[byte_dados + 1]) return false;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < heap_VALOR[첫값 + 1]; Loop_ÍNDICE++) {
            int coordenada_X = heap_VALOR[첫값 + 2 + Loop_ÍNDICE], Y_coordenada = heap_VALOR[byte_dados + 2 + Loop_ÍNDICE];
            if (caminho) { if (coordenada_X == '.') coordenada_X = '/'; if (Y_coordenada == '.') Y_coordenada = '/'; }
            if (coordenada_X != Y_coordenada) return false;
        }
        return true;
    }
    static boolean TI_válido_objeto(int objeto_Referência) {
        if (objeto_Referência == 0) { falha_VALOR("NullPointerException"); return false; }
        if (objeto_Referência < 1 || objeto_Referência >= heap_encerrar_cargo || 힙폭[objeto_Referência] < 2 || heap_VALOR[objeto_Referência] == 0) { falha_VALOR("invalid object reference"); return false; }
        return true;
    }
    static void proteger_VALOR(int objeto_Referência) {
        if (objeto_Referência > 0 && objeto_Referência < heap_encerrar_cargo && 힙폭[objeto_Referência] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objeto_Referência;
    }
    static void mostrar_VALOR(int objeto_Referência) {
        if (objeto_Referência > 0 && objeto_Referência < heap_encerrar_cargo && 힙폭[objeto_Referência] >= 2 && heap_VALOR[objeto_Referência] != 0 && 힙표시[objeto_Referência] == 0) {
            힙표시[objeto_Referência] = 1; 표시대기[visor_CONT_NÚM++] = objeto_Referência;
        }
    }
    static void 수거() {
        visor_CONT_NÚM = 0; Coleção_CONT_NÚM++;
        for (int cheque_cargo = 1; cheque_cargo < heap_encerrar_cargo; cheque_cargo += 힙폭[cheque_cargo]) 힙표시[cheque_cargo] = 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < cadeia_Referência.length; Loop_ÍNDICE++) mostrar_VALOR(cadeia_Referência[Loop_ÍNDICE]);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < slot_CONT_NÚM; Loop_ÍNDICE++) if ((slot_Permissões[Loop_ÍNDICE] & 8) != 0 && TIPO_Tipo(slot_TIPO[Loop_ÍNDICE]) == 2) mostrar_VALOR(slot_dados[Loop_ÍNDICE]);
        for (int 임시값 = 0; 임시값 < contagem_de_threads; 임시값++) {
            mostrar_VALOR(thread_objeto[임시값]); mostrar_VALOR(thread_alvo[임시값]);
            int 꼭대기자리 = 임시값 == em_dia_thread ? quadro_ÍNDICE : thread_quadro[임시값];
            for (int Arquivo_ÍNDICE = 임시값 * 32; Arquivo_ÍNDICE <= 꼭대기자리; Arquivo_ÍNDICE++) {
                for (int interna_cargo = 0; interna_cargo < 함수지역[quadro_método[Arquivo_ÍNDICE]]; interna_cargo++) if (local_TIPO[Arquivo_ÍNDICE * 128 + interna_cargo] == 2) mostrar_VALOR(local_VALOR[Arquivo_ÍNDICE * 128 + interna_cargo]);
                for (int interna_cargo = 0; interna_cargo < quadro_pilha[Arquivo_ÍNDICE]; interna_cargo++) if (operando_pilha_TIPO[Arquivo_ÍNDICE * 128 + interna_cargo] == 2) mostrar_VALOR(operando_pilha_VALOR[Arquivo_ÍNDICE * 128 + interna_cargo]);
            }
        }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < tela_Referência.length; Loop_ÍNDICE++) mostrar_VALOR(tela_Referência[Loop_ÍNDICE]);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 나중수; Loop_ÍNDICE++) mostrar_VALOR(나중실행[Loop_ÍNDICE]);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Store_inteiro.length; Loop_ÍNDICE++) mostrar_VALOR(Store_inteiro[Loop_ÍNDICE]);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < aula_Definição_CONT_NÚM; Loop_ÍNDICE++) mostrar_VALOR(aula_bloquear[Loop_ÍNDICE]);
        for (int cheque_cargo = 1; cheque_cargo < heap_encerrar_cargo; cheque_cargo += 힙폭[cheque_cargo]) if (잠금깊이[cheque_cargo] > 0) mostrar_VALOR(cheque_cargo);
        mostrar_VALOR(던진객체);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 잠시수; Loop_ÍNDICE++) mostrar_VALOR(잠시참조[Loop_ÍNDICE]);
        while (visor_CONT_NÚM > 0) {
            int objeto_Referência = 표시대기[--visor_CONT_NÚM], área_CÓDIGO = heap_VALOR[objeto_Referência];
            for (int Loop_ÍNDICE = objeto_Referência + 2; Loop_ÍNDICE < objeto_Referência + 힙폭[objeto_Referência]; Loop_ÍNDICE++) if (área_CÓDIGO == 3 || área_CÓDIGO == 4 || heap_Referência[Loop_ÍNDICE] != 0) mostrar_VALOR(heap_VALOR[Loop_ÍNDICE]);
        }
        for (int cheque_cargo = 1; cheque_cargo < heap_encerrar_cargo; cheque_cargo += 힙폭[cheque_cargo]) if (힙표시[cheque_cargo] == 0) heap_VALOR[cheque_cargo] = 0;
        for (int cheque_cargo = 1; cheque_cargo < heap_encerrar_cargo; cheque_cargo += 힙폭[cheque_cargo]) if (heap_VALOR[cheque_cargo] == 0) {
            while (cheque_cargo + 힙폭[cheque_cargo] < heap_encerrar_cargo && heap_VALOR[cheque_cargo + 힙폭[cheque_cargo]] == 0) { int Avançar_cargo = cheque_cargo + 힙폭[cheque_cargo]; 힙폭[cheque_cargo] += 힙폭[Avançar_cargo]; 힙폭[Avançar_cargo] = 0; }
            if (cheque_cargo + 힙폭[cheque_cargo] == heap_encerrar_cargo) { heap_encerrar_cargo = cheque_cargo; break; }
        }
    }
    static int 새기억(int Tipo_VALOR, int duração_VALOR) {
        if (duração_VALOR < 0) { falha_VALOR("NegativeArraySizeException"); return 0; }
        if (duração_VALOR > heap_VALOR.length - 3) { falha_VALOR("object heap exhausted"); return 0; }
        int 필요수 = duração_VALOR + 2, objeto_Referência = 0;
        if (필요수 <= heap_VALOR.length - heap_encerrar_cargo) { objeto_Referência = heap_encerrar_cargo; heap_encerrar_cargo += 필요수; }
        else {
            수거();
            for (int leitura_cursor = 1; leitura_cursor < heap_encerrar_cargo; leitura_cursor += 힙폭[leitura_cursor]) if (heap_VALOR[leitura_cursor] == 0 && 힙폭[leitura_cursor] >= 필요수) { objeto_Referência = leitura_cursor; break; }
            if (objeto_Referência != 0) {
                int 남은길이 = 힙폭[objeto_Referência] - 필요수;
                if (남은길이 >= 2) { 힙폭[objeto_Referência + 필요수] = 남은길이; heap_VALOR[objeto_Referência + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= heap_VALOR.length - heap_encerrar_cargo) { objeto_Referência = heap_encerrar_cargo; heap_encerrar_cargo += 필요수; }
        }
        if (objeto_Referência == 0) { falha_VALOR("object heap exhausted"); return 0; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 필요수; Loop_ÍNDICE++) { heap_VALOR[objeto_Referência + Loop_ÍNDICE] = 0; heap_Referência[objeto_Referência + Loop_ÍNDICE] = 0; 힙폭[objeto_Referência + Loop_ÍNDICE] = 0; }
        elemento_da_matriz[objeto_Referência] = 0;
        힙폭[objeto_Referência] = 필요수; heap_VALOR[objeto_Referência] = Tipo_VALOR; heap_VALOR[objeto_Referência + 1] = duração_VALOR; proteger_VALOR(objeto_Referência); return objeto_Referência;
    }
    static int exceção_aula(String nome_constante) {
        if (FerramentasJava.같음(nome_constante, "java/lang/Throwable")) return 1;
        if (FerramentasJava.같음(nome_constante, "java/lang/Exception")) return 2;
        if (FerramentasJava.같음(nome_constante, "java/lang/RuntimeException")) return 3;
        if (FerramentasJava.같음(nome_constante, "java/lang/ArithmeticException")) return 4;
        if (FerramentasJava.같음(nome_constante, "java/lang/NullPointerException")) return 5;
        if (FerramentasJava.같음(nome_constante, "java/lang/IndexOutOfBoundsException")) return 6;
        if (FerramentasJava.같음(nome_constante, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (FerramentasJava.같음(nome_constante, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (FerramentasJava.같음(nome_constante, "java/lang/IllegalArgumentException")) return 9;
        if (FerramentasJava.같음(nome_constante, "java/lang/NumberFormatException")) return 10;
        if (FerramentasJava.같음(nome_constante, "java/io/IOException")) return 11;
        if (FerramentasJava.같음(nome_constante, "java/io/FileNotFoundException")) return 12;
        if (FerramentasJava.같음(nome_constante, "java/lang/IllegalStateException")) return 13;
        if (FerramentasJava.같음(nome_constante, "java/lang/ClassCastException")) return 14;
        if (FerramentasJava.같음(nome_constante, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int exceção_constante(int Nome) {
        for (int Loop_ÍNDICE = 1; Loop_ÍNDICE <= 41; Loop_ÍNDICE++) if (Word_SMS(Nome, exceção_nome(Loop_ÍNDICE))) return Loop_ÍNDICE;
        return 0;
    }
    static String exceção_nome(int conta_VALOR) {
        if (conta_VALOR == 40) return "java/lang/InterruptedException";
        if (conta_VALOR == 41) return "Português/nativo/대기중단예외";
        if (conta_VALOR == 39) return "java/net/SocketException";
        if (conta_VALOR == 20) return "Português/nativo/exceção";
        if (conta_VALOR == 21) return "Português/nativo/execução_exceção";
        if (conta_VALOR == 22) return "Português/nativo/E_S_exceção";
        if (conta_VALOR == 23) return "Português/nativo/aguarde_TEMPOLIMITE_exceção";
        if (conta_VALOR == 24) return "Português/nativo/email_PROC_exceção";
        if (conta_VALOR == 25) return "Português/nativo/파일없음예외";
        if (conta_VALOR == 26) return "Português/nativo/comunicação_exceção";
        if (conta_VALOR == 27) return "Português/nativo/inválido_argumento_exceção";
        if (conta_VALOR == 28) return "Português/nativo/número_formato_falha";
        if (conta_VALOR == 29) return "Português/nativo/범위예외";
        if (conta_VALOR == 30) return "Português/nativo/limites_da_matriz_exceção";
        if (conta_VALOR == 31) return "Português/nativo/문자열범위예외";
        if (conta_VALOR == 32) return "Português/nativo/referência_nula_exceção";
        if (conta_VALOR == 33) return "Português/nativo/산술예외";
        if (conta_VALOR == 34) return "Português/nativo/Estado_exceção";
        if (conta_VALOR == 35) return "Português/nativo/TIPO_coerção_exceção";
        if (conta_VALOR == 36) return "Português/nativo/negativo_MATRIZ_dimensionar_falha";
        if (conta_VALOR == 37) return "Português/nativo/MATRIZ_Store_falha";
        if (conta_VALOR == 38) return "Português/nativo/thread_Estado_exceção";
        if (conta_VALOR == 1) return "java/lang/Throwable"; if (conta_VALOR == 2) return "java/lang/Exception";
        if (conta_VALOR == 3) return "java/lang/RuntimeException"; if (conta_VALOR == 4) return "java/lang/ArithmeticException";
        if (conta_VALOR == 5) return "java/lang/NullPointerException"; if (conta_VALOR == 6) return "java/lang/IndexOutOfBoundsException";
        if (conta_VALOR == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (conta_VALOR == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (conta_VALOR == 9) return "java/lang/IllegalArgumentException"; if (conta_VALOR == 10) return "java/lang/NumberFormatException";
        if (conta_VALOR == 11) return "java/io/IOException"; if (conta_VALOR == 12) return "java/io/FileNotFoundException";
        if (conta_VALOR == 17) return "java/lang/ArrayStoreException";
        if (conta_VALOR == 18) return "java/net/UnknownHostException";
        if (conta_VALOR == 19) return "java/net/SocketTimeoutException";
        if (conta_VALOR == 16) return "java/lang/IllegalThreadStateException";
        if (conta_VALOR == 13) return "java/lang/IllegalStateException"; if (conta_VALOR == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int exceção_pai(int conta_VALOR) {
        if (conta_VALOR == 40) return 2;
        if (conta_VALOR == 41) return 40;
        if (conta_VALOR == 39) return 11;
        if (conta_VALOR == 1) return 0;
        if (conta_VALOR == 2) return 1;
        if (conta_VALOR == 3) return 2;
        if (conta_VALOR == 4) return 3;
        if (conta_VALOR == 5) return 3;
        if (conta_VALOR == 6) return 3;
        if (conta_VALOR == 7) return 6;
        if (conta_VALOR == 8) return 6;
        if (conta_VALOR == 9) return 3;
        if (conta_VALOR == 10) return 9;
        if (conta_VALOR == 11) return 2;
        if (conta_VALOR == 12) return 11;
        if (conta_VALOR == 13) return 3;
        if (conta_VALOR == 14) return 3;
        if (conta_VALOR == 15) return 3;
        if (conta_VALOR == 16) return 9;
        if (conta_VALOR == 17) return 3;
        if (conta_VALOR == 18) return 11;
        if (conta_VALOR == 19) return 11;
        if (conta_VALOR == 20) return 2;
        if (conta_VALOR == 21) return 3;
        if (conta_VALOR == 22) return 11;
        if (conta_VALOR == 23) return 22;
        if (conta_VALOR == 24) return 22;
        if (conta_VALOR == 25) return 22;
        if (conta_VALOR == 26) return 22;
        if (conta_VALOR == 27) return 9;
        if (conta_VALOR == 28) return 27;
        if (conta_VALOR == 29) return 6;
        if (conta_VALOR == 30) return 29;
        if (conta_VALOR == 31) return 29;
        if (conta_VALOR == 32) return 5;
        if (conta_VALOR == 33) return 4;
        if (conta_VALOR == 34) return 13;
        if (conta_VALOR == 35) return 14;
        if (conta_VALOR == 36) return 15;
        if (conta_VALOR == 37) return 17;
        if (conta_VALOR == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int valor_real, int 요구값) {
        for (int 깊이 = 0; valor_real != 0 && 깊이 < 16; 깊이++, valor_real = exceção_pai(valor_real))
            if (valor_real == 요구값) return true;
        return false;
    }
    static void 예외던짐(int conta_VALOR, String LEIAME_Referência) {
        int objeto_Referência = 새기억(9, 2); if (erro) return;
        heap_VALOR[objeto_Referência + 2] = conta_VALOR; heap_VALOR[objeto_Referência + 3] = host_caractere(LEIAME_Referência); heap_Referência[objeto_Referência + 3] = 1;
        던진객체 = objeto_Referência; erro = true;
    }
    static boolean 맞는객체(int objeto_Referência, int Nome) {
        if (objeto_Referência == 0) return true;
        if (!TI_válido_objeto(objeto_Referência)) return false;
        int área_CÓDIGO = heap_VALOR[objeto_Referência];
        if (Word_SMS(Nome, "java/lang/Object")) return true;
        if (área_CÓDIGO >= 32) return 종포함(área_CÓDIGO - 32, Nome);
        if (área_CÓDIGO == 9) { int alvo_email = exceção_constante(Nome); return alvo_email != 0 && 예외포함(heap_VALOR[objeto_Referência + 2], alvo_email); }
        if (área_CÓDIGO == 1) return Word_SMS(Nome, "java/lang/String") || Word_SMS(Nome, "java/lang/CharSequence");
        if (área_CÓDIGO == 4) return Word_SMS(Nome, "java/lang/StringBuilder") || Word_SMS(Nome, "java/lang/CharSequence");
        if (área_CÓDIGO == 10) return Word_SMS(Nome, "java/util/ArrayList") || Word_SMS(Nome, "java/util/List");
        if (área_CÓDIGO == 11) return Word_SMS(Nome, "java/util/HashMap") || Word_SMS(Nome, "java/util/Map");
        if (área_CÓDIGO == 12) return Word_SMS(Nome, "java/lang/Integer") || Word_SMS(Nome, "java/lang/Number");
        if (área_CÓDIGO >= 24 && área_CÓDIGO <= 28 && heap_VALOR[objeto_Referência + 13] != 0) return 한국어화면종(Nome) == área_CÓDIGO || Word_SMS(Nome, "Português/nativo/tela_elemento");
        if (área_CÓDIGO >= 24 && área_CÓDIGO <= 28) return (한국어화면종(Nome) == 0 && tela_aula(Nome) == área_CÓDIGO) || Word_SMS(Nome, "java/awt/Component") || Word_SMS(Nome, "java/awt/Container") || Word_SMS(Nome, "javax/swing/JComponent");
        if (área_CÓDIGO == 29) return Word_SMS(Nome, heap_VALOR[objeto_Referência + 3] != 0 ? "Português/nativo/Ação_aviso" : "java/awt/event/ActionEvent");
        if (área_CÓDIGO == 30) return Word_SMS(Nome, "java/awt/FlowLayout") || Word_SMS(Nome, "java/awt/LayoutManager");
        if (área_CÓDIGO == 17) return Word_SMS(Nome, "java/net/Socket");
        if (área_CÓDIGO == 18) return Word_SMS(Nome, "java/net/ServerSocket");
        if (área_CÓDIGO == 19) return Word_SMS(Nome, heap_VALOR[objeto_Referência + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (área_CÓDIGO == 14) return Word_SMS(Nome, "java/net/InetAddress");
        if (área_CÓDIGO == 15) return Word_SMS(Nome, "java/net/DatagramSocket");
        if (área_CÓDIGO == 16) return Word_SMS(Nome, "java/net/DatagramPacket");
        if (área_CÓDIGO == 13) return Word_SMS(Nome, heap_VALOR[objeto_Referência + 3] != 0 ? "Português/nativo/tarefaSegundoPlano" : "java/lang/Thread");
        if (área_CÓDIGO == 2) return Word_SMS(Nome, "[I"); if (área_CÓDIGO == 20) return Word_SMS(Nome, "[B"); if (área_CÓDIGO == 21) return Word_SMS(Nome, "[Z");
        if (área_CÓDIGO == 22) return Word_SMS(Nome, "[C"); if (área_CÓDIGO == 23) return Word_SMS(Nome, "[S");
        if (área_CÓDIGO != 3) return false;
        if (Word_SMS(Nome, "[Ljava/lang/Object;")) return true;
        int componente = elemento_da_matriz[objeto_Referência];
        if (componente == -1) return Word_SMS(Nome, "[Ljava/lang/String;") || Word_SMS(Nome, "[Ljava/lang/CharSequence;");
        if (componente == 0) return false;
        if (배열종비교(componente, Nome)) return true;
        if ((Word_SMS(componente, "java/lang/String") || Word_SMS(componente, "java/lang/StringBuilder")) && Word_SMS(Nome, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < aula_Definição_CONT_NÚM; Loop_ÍNDICE++) if (같은말(aula_Definição_nome[Loop_ÍNDICE], componente)) {
            for (int ponto_de_código = Loop_ÍNDICE, 중첩깊이 = 0; ponto_de_código >= 0 && 중첩깊이 < 16; 중첩깊이++, ponto_de_código = pai_aula(ponto_de_código)) {
                if (배열종비교(aula_Definição_pai[ponto_de_código], Nome)) return true;
                for (int interna_cargo = 0; interna_cargo < aula_interface_CONT_NÚM[ponto_de_código]; interna_cargo++) if (배열종비교(aula_interface[ponto_de_código * 16 + interna_cargo], Nome)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nome_constante, int descritor) {
        int cheque_cargo = 상가[descritor], entrada_CONT_NÚM_8f7753a1 = constante_SEGUNDO_VALOR[descritor];
        if (nome_constante == 0 || entrada_CONT_NÚM_8f7753a1 < 4 || ficheiro[cheque_cargo] != '[' || ficheiro[cheque_cargo + 1] != 'L' || ficheiro[cheque_cargo + entrada_CONT_NÚM_8f7753a1 - 1] != ';' || constante_SEGUNDO_VALOR[nome_constante] != entrada_CONT_NÚM_8f7753a1 - 3) return false;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1 - 3; Loop_ÍNDICE++) if (ficheiro[상가[nome_constante] + Loop_ÍNDICE] != ficheiro[cheque_cargo + 2 + Loop_ÍNDICE]) return false;
        return true;
    }
    static void alça_exceção() {
        if (던진객체 == 0) return;
        erro = false;
        while (quadro_ÍNDICE >= em_dia_thread * 32) {
            int Arquivo_ÍNDICE = quadro_método[quadro_ÍNDICE], leitura_cursor = quadro_instrução[quadro_ÍNDICE];
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 잡기수; Loop_ÍNDICE++) if (잡기함수[Loop_ÍNDICE] == Arquivo_ÍNDICE && leitura_cursor >= 잡기시작[Loop_ÍNDICE] && leitura_cursor < 잡기끝[Loop_ÍNDICE]
                && (잡기종[Loop_ÍNDICE] == 0 || 맞는객체(던진객체, 잡기종[Loop_ÍNDICE]))) {
                quadro_cargo[quadro_ÍNDICE] = 잡기위치[Loop_ÍNDICE]; quadro_pilha[quadro_ÍNDICE] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (inicializar_quadro[quadro_ÍNDICE] != 0) aula_Definição_Estado[inicializar_quadro[quadro_ÍNDICE] - 1] = 3;
            if (quadro_bloquear[quadro_ÍNDICE] != 0) { lançar_bloquear(quadro_bloquear[quadro_ÍNDICE]); quadro_bloquear[quadro_ÍNDICE] = 0; }
            quadro_ÍNDICE--;
        }
        espaço_do_utilizador.Escrita("Uncaught ");
        if (heap_VALOR[던진객체] == 9) { espaço_do_utilizador.Escrita(exceção_nome(heap_VALOR[던진객체 + 2])); espaço_do_utilizador.Escrita(": "); gravar_SMS(heap_VALOR[던진객체 + 3]); }
        else espaço_do_utilizador.Escrita("user exception");
        espaço_do_utilizador.gravar_caractere_VALOR(10); 던진객체 = 0; erro = true;
    }
    // 이 JVM의 operando_pilha 항목은 em_dia_item category-1(int/reference)만 허용한다.
    static void pilha_instrução(int comando_CÓDIGO) {
        int 첫값 = 빼기(0), 첫형식 = tipo_de_retorno;
        if (comando_CÓDIGO == 87) return;
        if (comando_CÓDIGO == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_dados = 빼기(0), SEGUNDO_formato = tipo_de_retorno;
        if (comando_CÓDIGO == 88) return;
        if (comando_CÓDIGO == 90) { 넣기(첫값, 첫형식); 넣기(byte_dados, SEGUNDO_formato); 넣기(첫값, 첫형식); return; }
        if (comando_CÓDIGO == 92) { 넣기(byte_dados, SEGUNDO_formato); 넣기(첫값, 첫형식); 넣기(byte_dados, SEGUNDO_formato); 넣기(첫값, 첫형식); return; }
        if (comando_CÓDIGO == 95) { 넣기(첫값, 첫형식); 넣기(byte_dados, SEGUNDO_formato); return; }
        int ponto_de_código = 빼기(0), 셋째형식 = tipo_de_retorno;
        if (comando_CÓDIGO == 91) { 넣기(첫값, 첫형식); 넣기(ponto_de_código, 셋째형식); 넣기(byte_dados, SEGUNDO_formato); 넣기(첫값, 첫형식); return; }
        if (comando_CÓDIGO == 93) { 넣기(byte_dados, SEGUNDO_formato); 넣기(첫값, 첫형식); 넣기(ponto_de_código, 셋째형식); 넣기(byte_dados, SEGUNDO_formato); 넣기(첫값, 첫형식); return; }
        int à_direita_VALOR = 빼기(0), 넷째형식 = tipo_de_retorno;
        넣기(byte_dados, SEGUNDO_formato); 넣기(첫값, 첫형식); 넣기(à_direita_VALOR, 넷째형식); 넣기(ponto_de_código, 셋째형식); 넣기(byte_dados, SEGUNDO_formato); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nome_constante, int 시작점) {
        int área_CÓDIGO = 0, válido_duração = 0, exceção_Referência = exceção_constante(nome_constante);
        if (Word_SMS(nome_constante, "java/lang/StringBuilder")) { área_CÓDIGO = 4; válido_duração = 1; }
        if (Word_SMS(nome_constante, "java/io/FileInputStream")) { área_CÓDIGO = 5; válido_duração = 2; }
        if (Word_SMS(nome_constante, "java/io/FileOutputStream")) { área_CÓDIGO = 6; válido_duração = 2; }
        if (exceção_Referência != 0) { área_CÓDIGO = 9; válido_duração = 2; }
        if (Word_SMS(nome_constante, "java/util/ArrayList")) { área_CÓDIGO = 10; válido_duração = 2; }
        if (Word_SMS(nome_constante, "java/util/HashMap")) { área_CÓDIGO = 11; válido_duração = 2; }
        if (Word_SMS(nome_constante, "java/lang/Integer")) { área_CÓDIGO = 12; válido_duração = 1; }
        if (Word_SMS(nome_constante, "java/net/Socket")) { área_CÓDIGO = 17; válido_duração = 5; }
        if (Word_SMS(nome_constante, "java/net/ServerSocket")) { área_CÓDIGO = 18; válido_duração = 5; }
        if (Word_SMS(nome_constante, "java/net/DatagramSocket")) { área_CÓDIGO = 15; válido_duração = 3; }
        if (Word_SMS(nome_constante, "java/net/DatagramPacket")) { área_CÓDIGO = 16; válido_duração = 4; }
        if (Word_SMS(nome_constante, "java/lang/Thread") || Word_SMS(nome_constante, "Português/nativo/tarefaSegundoPlano")) { área_CÓDIGO = 13; válido_duração = 2; }
        if (Word_SMS(nome_constante, "java/lang/Object")) { área_CÓDIGO = 8; }
        if (área_CÓDIGO == 0 && tela_aula(nome_constante) != 0) { área_CÓDIGO = tela_aula(nome_constante); válido_duração = 12; }
        if (área_CÓDIGO == 0) {
            int ponto_de_código = PROCURAR_aula_Definição(nome_constante); if (ponto_de_código < 0 || erro || !inicializar(ponto_de_código, 시작점)) return;
            área_CÓDIGO = 32 + ponto_de_código; válido_duração = aula_slot_CONT_NÚM[ponto_de_código];
        }
        int objeto_Referência = alocar_Armazenamento(área_CÓDIGO, válido_duração); if (erro) return;
        if (área_CÓDIGO == 13 && Word_SMS(nome_constante, "Português/nativo/tarefaSegundoPlano")) heap_VALOR[objeto_Referência + 3] = 1;
        if (área_CÓDIGO >= 24 && área_CÓDIGO <= 28 && 한국어화면종(nome_constante) != 0) heap_VALOR[objeto_Referência + 13] = 1;
        if (área_CÓDIGO == 5 || área_CÓDIGO == 6 || área_CÓDIGO == 15 || área_CÓDIGO == 17 || área_CÓDIGO == 18) heap_VALOR[objeto_Referência + 2] = -1;
        if (área_CÓDIGO == 9) heap_VALOR[objeto_Referência + 2] = exceção_Referência;
        넣기(objeto_Referência, 2);
    }
    static boolean 값같음(int 첫값, int byte_dados) {
        if (첫값 == byte_dados) return true;
        if (첫값 == 0 || byte_dados == 0 || 첫값 < 0 || byte_dados < 0 || 첫값 >= heap_encerrar_cargo || byte_dados >= heap_encerrar_cargo) return false;
        if (heap_VALOR[첫값] == 1 && heap_VALOR[byte_dados] == 1) return textos_iguais(첫값, byte_dados, false);
        return heap_VALOR[첫값] == 12 && heap_VALOR[byte_dados] == 12 && heap_VALOR[첫값 + 2] == heap_VALOR[byte_dados + 2];
    }
    static int SMS_fragmento(int objeto_Referência, int START_cargo, int encerrar_cargo) {
        if (!objeto_VALOR(objeto_Referência, 1)) return 0;
        if (START_cargo < 0 || encerrar_cargo < START_cargo || encerrar_cargo > heap_VALOR[objeto_Referência + 1]) { falha_VALOR("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = alocar_Armazenamento(1, encerrar_cargo - START_cargo); if (erro) return 0;
        for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < encerrar_cargo; Loop_ÍNDICE++) heap_VALOR[반환값 + 2 + Loop_ÍNDICE - START_cargo] = heap_VALOR[objeto_Referência + 2 + Loop_ÍNDICE];
        return 반환값;
    }
    static int unir_SMS(int 첫값, int byte_dados) {
        if (!objeto_VALOR(첫값, 1) || !objeto_VALOR(byte_dados, 1)) return 0;
        int entrada_CONT_NÚM_8f7753a1 = heap_VALOR[첫값 + 1], método_ÍNDICE = heap_VALOR[byte_dados + 1], 반환값 = alocar_Armazenamento(1, entrada_CONT_NÚM_8f7753a1 + método_ÍNDICE); if (erro) return 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) heap_VALOR[반환값 + 2 + Loop_ÍNDICE] = heap_VALOR[첫값 + 2 + Loop_ÍNDICE];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < método_ÍNDICE; Loop_ÍNDICE++) heap_VALOR[반환값 + 2 + entrada_CONT_NÚM_8f7753a1 + Loop_ÍNDICE] = heap_VALOR[byte_dados + 2 + Loop_ÍNDICE];
        return 반환값;
    }
    static boolean 기본호출(int proprietário, int nome_constante, int descritor_constante, int comando_CÓDIGO) {
        if (Word_SMS(proprietário, "Português/nativo/실행인수") && comando_CÓDIGO == 184) {
            if (Word_SMS(nome_constante, "item_CONT_NÚM") && Word_SMS(descritor_constante, "()I")) { 넣기(espaço_do_utilizador.인수개수() - 1, 1); return true; }
            if (Word_SMS(nome_constante, "texto") && Word_SMS(descritor_constante, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= espaço_do_utilizador.인수개수() - 1) 예외던짐(29, "Executar_comando argumentos 범위를 벗어났습니다");
                else 넣기(host_caractere(espaço_do_utilizador.argumentos(순번 + 1)), 2);
                return true;
            }
            falha_VALOR("지원하지 않는 Português Executar_comando argumentos 호출"); return true;
        }
        if (Word_SMS(proprietário, "Português/nativo/tarefaSegundoPlano")) { Processo_thread(nome_constante, descritor_constante, comando_CÓDIGO, true); return true; }
        if (한국어화면소유(proprietário)) { 한국어화면호출(proprietário, nome_constante, descritor_constante, comando_CÓDIGO); return true; }
        if (tela_proprietário(proprietário)) { 화면호출(proprietário, nome_constante, descritor_constante, comando_CÓDIGO); return true; }
        if (Word_SMS(proprietário, "java/net/Socket") || Word_SMS(proprietário, "java/net/ServerSocket") || Word_SMS(proprietário, "java/io/InputStream") || Word_SMS(proprietário, "java/io/OutputStream")) { 흐름호출(proprietário, nome_constante, descritor_constante, comando_CÓDIGO); return true; }
        if (Word_SMS(proprietário, "Português/nativo/kernel_VALOR") && comando_CÓDIGO == 184) {
            if (Word_SMS(nome_constante, "화면너비") && Word_SMS(descritor_constante, "()I")) { 넣기(espaço_do_utilizador.화면너비(), 1); return true; }
            if (Word_SMS(nome_constante, "tela_altura") && Word_SMS(descritor_constante, "()I")) { 넣기(espaço_do_utilizador.tela_altura(), 1); return true; }
            if (Word_SMS(nome_constante, "밀리초") && Word_SMS(descritor_constante, "()I")) { 넣기(espaço_do_utilizador.밀리초(), 1); return true; }
            if (Word_SMS(nome_constante, "그림대기") && Word_SMS(descritor_constante, "()I")) { 넣기(espaço_do_utilizador.그림대기(), 1); return true; }
            if (Word_SMS(nome_constante, "retângulo") && Word_SMS(descritor_constante, "(IIIII)I")) { int 색상 = 빼기(1), altura_VALOR = 빼기(1), 너비 = 빼기(1), Y_coordenada = 빼기(1), coordenada_X = 빼기(1); 넣기(espaço_do_utilizador.retângulo(coordenada_X, Y_coordenada, 너비, altura_VALOR, 색상), 1); return true; }
        }
        if (Word_SMS(proprietário, "java/net/InetAddress") || Word_SMS(proprietário, "java/net/DatagramPacket") || Word_SMS(proprietário, "java/net/DatagramSocket")) { 통신호출(proprietário, nome_constante, descritor_constante, comando_CÓDIGO); return true; }
        if (Word_SMS(proprietário, "java/lang/Thread")) { 가닥호출(nome_constante, descritor_constante, comando_CÓDIGO); return true; }
        if (Word_SMS(proprietário, "java/lang/Object")) {
            if (Word_SMS(nome_constante, "<init>") && Word_SMS(descritor_constante, "()V") && comando_CÓDIGO == 183) { TI_válido_objeto(빼기(2)); return true; }
            if (Word_SMS(nome_constante, "equals") && Word_SMS(descritor_constante, "(Ljava/lang/Object;)Z")) { int byte_dados = 빼기(2), 첫값 = 빼기(2); if (TI_válido_objeto(첫값)) 넣기(첫값 == byte_dados ? 1 : 0, 1); return true; }
        }
        if (exceção_constante(proprietário) != 0) {
            if (Word_SMS(nome_constante, "<init>") && comando_CÓDIGO == 183 && (Word_SMS(descritor_constante, "()V") || Word_SMS(descritor_constante, "(Ljava/lang/String;)V"))) {
                int aviso_1dd14da4 = Word_SMS(descritor_constante, "()V") ? 0 : 빼기(2), objeto_Referência = 빼기(2);
                if (objeto_VALOR(objeto_Referência, 9)) { heap_VALOR[objeto_Referência + 3] = aviso_1dd14da4; heap_Referência[objeto_Referência + 3] = 1; } return true;
            }
            if ((Word_SMS(nome_constante, "getMessage") || Word_SMS(nome_constante, "설명")) && Word_SMS(descritor_constante, "()Ljava/lang/String;")) { int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, 9)) 넣기(heap_VALOR[objeto_Referência + 3], 2); return true; }
        }
        if (Word_SMS(proprietário, "java/lang/String")) {
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "getBytes") && (Word_SMS(descritor_constante, "()[B") || Word_SMS(descritor_constante, "(Ljava/lang/String;)[B"))) {
                int Codificação_nome = Word_SMS(descritor_constante, "()[B") ? 0 : 빼기(2), objeto_Referência = 빼기(2);
                if (!objeto_VALOR(objeto_Referência, 1)) return true;
                if (Codificação_nome != 0 && !textos_iguais(Codificação_nome, host_caractere("UTF-8"), false) && !textos_iguais(Codificação_nome, host_caractere("UTF8"), false) && !textos_iguais(Codificação_nome, host_caractere("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int entrada_CONT_NÚM_8f7753a1 = heap_VALOR[objeto_Referência + 1], 반환값 = alocar_Armazenamento(20, entrada_CONT_NÚM_8f7753a1 * 3), 사용수 = 0; if (erro) return true;
                for (int interna_cargo = 0; interna_cargo < entrada_CONT_NÚM_8f7753a1; interna_cargo++) {
                    int ponto_de_código = heap_VALOR[objeto_Referência + 2 + interna_cargo];
                    if (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdbff && interna_cargo + 1 < entrada_CONT_NÚM_8f7753a1 && heap_VALOR[objeto_Referência + 3 + interna_cargo] >= 0xdc00 && heap_VALOR[objeto_Referência + 3 + interna_cargo] <= 0xdfff) ponto_de_código = 0x10000 + ((ponto_de_código - 0xd800) << 10) + heap_VALOR[objeto_Referência + 2 + ++interna_cargo] - 0xdc00;
                    else if (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdfff) ponto_de_código = '?';
                    if (ponto_de_código < 128) heap_VALOR[반환값 + 2 + 사용수++] = ponto_de_código;
                    else { int byte_CONT_NÚM = ponto_de_código < 2048 ? 2 : ponto_de_código < 65536 ? 3 : 4; heap_VALOR[반환값 + 2 + 사용수++] = (byte)((byte_CONT_NÚM == 2 ? 192 : byte_CONT_NÚM == 3 ? 224 : 240) | ponto_de_código >> (6 * (byte_CONT_NÚM - 1))); for (int Comparação_cargo = byte_CONT_NÚM - 1; Comparação_cargo > 0; Comparação_cargo--) heap_VALOR[반환값 + 2 + 사용수++] = (byte)(128 | ponto_de_código >> (6 * (Comparação_cargo - 1)) & 63); }
                }
                heap_VALOR[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "valueOf") && Word_SMS(descritor_constante, "(I)Ljava/lang/String;")) { 넣기(dígito_caractere(빼기(1)), 2); return true; }
            if (comando_CÓDIGO != 182) return false;
            if (Word_SMS(nome_constante, "equals") && Word_SMS(descritor_constante, "(Ljava/lang/Object;)Z")) { int byte_dados = 빼기(2), 첫값 = 빼기(2); if (objeto_VALOR(첫값, 1)) 넣기(textos_iguais(첫값, byte_dados, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(nome_constante, "isEmpty") && Word_SMS(descritor_constante, "()Z")) { int 첫값 = 빼기(2); if (objeto_VALOR(첫값, 1)) 넣기(heap_VALOR[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(nome_constante, "substring") && (Word_SMS(descritor_constante, "(I)Ljava/lang/String;") || Word_SMS(descritor_constante, "(II)Ljava/lang/String;"))) {
                boolean SEGUNDO_VALOR = Word_SMS(descritor_constante, "(II)Ljava/lang/String;"); int encerrar_cargo = SEGUNDO_VALOR ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objeto_VALOR(첫값, 1)) 넣기(SMS_fragmento(첫값, 시작점, SEGUNDO_VALOR ? encerrar_cargo : heap_VALOR[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(nome_constante, "concat") && Word_SMS(descritor_constante, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_dados = 빼기(2), 첫값 = 빼기(2); 넣기(unir_SMS(첫값, byte_dados), 2); return true; }
            if (Word_SMS(nome_constante, "hashCode") && Word_SMS(descritor_constante, "()I")) { int 첫값 = 빼기(2), hash_VALOR = 0; if (objeto_VALOR(첫값, 1)) { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < heap_VALOR[첫값 + 1]; Loop_ÍNDICE++) hash_VALOR = hash_VALOR * 31 + heap_VALOR[첫값 + 2 + Loop_ÍNDICE]; 넣기(hash_VALOR, 1); } return true; }
            if (Word_SMS(nome_constante, "toString") && Word_SMS(descritor_constante, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objeto_VALOR(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(proprietário, "java/lang/Integer")) {
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "valueOf") && Word_SMS(descritor_constante, "(I)Ljava/lang/Integer;")) { int dados_VALOR = 빼기(1), objeto_Referência = dados_VALOR >= -128 && dados_VALOR <= 127 ? Store_inteiro[dados_VALOR + 128] : 0; if (objeto_Referência == 0) { objeto_Referência = alocar_Armazenamento(12, 1); if (!erro) { heap_VALOR[objeto_Referência + 2] = dados_VALOR; if (dados_VALOR >= -128 && dados_VALOR <= 127) Store_inteiro[dados_VALOR + 128] = objeto_Referência; } } 넣기(objeto_Referência, 2); return true; }
            if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>") && Word_SMS(descritor_constante, "(I)V")) { int dados_VALOR = 빼기(1), objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, 12)) heap_VALOR[objeto_Referência + 2] = dados_VALOR; return true; }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "intValue") && Word_SMS(descritor_constante, "()I")) { int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, 12)) 넣기(heap_VALOR[objeto_Referência + 2], 1); return true; }
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "toString") && Word_SMS(descritor_constante, "(I)Ljava/lang/String;")) { 넣기(dígito_caractere(빼기(1)), 2); return true; }
        }
        if (Word_SMS(proprietário, "java/lang/Math") && comando_CÓDIGO == 184) {
            if (Word_SMS(nome_constante, "abs") && Word_SMS(descritor_constante, "(I)I")) { int leitura_VALOR = 빼기(1); 넣기(leitura_VALOR < 0 ? -leitura_VALOR : leitura_VALOR, 1); return true; }
            if ((Word_SMS(nome_constante, "min") || Word_SMS(nome_constante, "max")) && Word_SMS(descritor_constante, "(II)I")) { int byte_dados = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(nome_constante, "min") ? (첫값 < byte_dados ? 첫값 : byte_dados) : (첫값 > byte_dados ? 첫값 : byte_dados), 1); return true; }
        }
        if (Word_SMS(proprietário, "java/lang/System") && comando_CÓDIGO == 184) {
            if (Word_SMS(nome_constante, "gc") && Word_SMS(descritor_constante, "()V")) { 수거(); return true; }
            if (Word_SMS(nome_constante, "arraycopy") && Word_SMS(descritor_constante, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int entrada_CONT_NÚM_8f7753a1 = 빼기(1), destino_VALOR_ÍNDICE = 빼기(1), byte_dados = 빼기(2), START_cargo = 빼기(1), 첫값 = 빼기(2);
                if (TI_válido_objeto(첫값) && TI_válido_objeto(byte_dados)) {
                    int área_CÓDIGO = heap_VALOR[첫값];
                    if (heap_VALOR[byte_dados] != área_CÓDIGO || (área_CÓDIGO != 2 && área_CÓDIGO != 3 && (área_CÓDIGO < 20 || área_CÓDIGO > 23))) falha_VALOR("arraycopy type mismatch");
                    else if (entrada_CONT_NÚM_8f7753a1 < 0 || START_cargo < 0 || destino_VALOR_ÍNDICE < 0 || START_cargo > heap_VALOR[첫값 + 1] - entrada_CONT_NÚM_8f7753a1 || destino_VALOR_ÍNDICE > heap_VALOR[byte_dados + 1] - entrada_CONT_NÚM_8f7753a1) falha_VALOR("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_dados && destino_VALOR_ÍNDICE > START_cargo) { for (int Loop_ÍNDICE = entrada_CONT_NÚM_8f7753a1 - 1; Loop_ÍNDICE >= 0; Loop_ÍNDICE--) heap_VALOR[byte_dados + 2 + destino_VALOR_ÍNDICE + Loop_ÍNDICE] = heap_VALOR[첫값 + 2 + START_cargo + Loop_ÍNDICE]; }
                    else { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1 && !erro; Loop_ÍNDICE++) { int dados_VALOR = heap_VALOR[첫값 + 2 + START_cargo + Loop_ÍNDICE]; if (área_CÓDIGO != 3 || 배열저장가능(byte_dados, dados_VALOR)) heap_VALOR[byte_dados + 2 + destino_VALOR_ÍNDICE + Loop_ÍNDICE] = dados_VALOR; } }
                }
                return true;
            }
        }
        if (Word_SMS(proprietário, "java/util/ArrayList") || Word_SMS(proprietário, "java/util/List") || Word_SMS(proprietário, "java/util/HashMap") || Word_SMS(proprietário, "java/util/Map")) {
            모음호출(proprietário, nome_constante, descritor_constante, comando_CÓDIGO); return true;
        }
        return false;
    }
    static void 모음늘리기(int objeto_Referência, int 필요수) {
        int Anterior_VALOR = heap_VALOR[objeto_Referência + 2], capacidade_dados = Anterior_VALOR == 0 ? 0 : heap_VALOR[Anterior_VALOR + 1];
        if (capacidade_dados >= 필요수) return;
        int Avançar_cargo = capacidade_dados < 8 ? 8 : capacidade_dados * 2; if (Avançar_cargo < 필요수) Avançar_cargo = 필요수;
        int dados_MATRIZ = alocar_Armazenamento(3, Avançar_cargo); if (erro) return;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < capacidade_dados; Loop_ÍNDICE++) heap_VALOR[dados_MATRIZ + 2 + Loop_ÍNDICE] = heap_VALOR[Anterior_VALOR + 2 + Loop_ÍNDICE];
        heap_VALOR[objeto_Referência + 2] = dados_MATRIZ; heap_Referência[objeto_Referência + 2] = 1;
    }
    static void 모음호출(int proprietário, int nome_constante, int descritor_constante, int comando_CÓDIGO) {
        boolean 대응참조 = Word_SMS(proprietário, "java/util/HashMap") || Word_SMS(proprietário, "java/util/Map"); int área_CÓDIGO = 대응참조 ? 11 : 10;
        if (Word_SMS(nome_constante, "<init>") && comando_CÓDIGO == 183 && Word_SMS(descritor_constante, "()V")) { int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, área_CÓDIGO)) 모음늘리기(objeto_Referência, 8); return; }
        if (comando_CÓDIGO != 182 && comando_CÓDIGO != 185) { falha_VALOR("invalid collection invocation"); return; }
        if (Word_SMS(nome_constante, "size") && Word_SMS(descritor_constante, "()I") || Word_SMS(nome_constante, "isEmpty") && Word_SMS(descritor_constante, "()Z")) {
            int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, área_CÓDIGO)) 넣기(Word_SMS(nome_constante, "size") ? heap_VALOR[objeto_Referência + 3] : heap_VALOR[objeto_Referência + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(nome_constante, "clear") && Word_SMS(descritor_constante, "()V")) { int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, área_CÓDIGO)) { int dados_MATRIZ = heap_VALOR[objeto_Referência + 2]; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < heap_VALOR[dados_MATRIZ + 1]; Loop_ÍNDICE++) heap_VALOR[dados_MATRIZ + 2 + Loop_ÍNDICE] = 0; heap_VALOR[objeto_Referência + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(nome_constante, "add") && Word_SMS(descritor_constante, "(Ljava/lang/Object;)Z")) {
            int dados_VALOR = 빼기(2), objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, 10)) return;
            int entrada_CONT_NÚM_8f7753a1 = heap_VALOR[objeto_Referência + 3]; 모음늘리기(objeto_Referência, entrada_CONT_NÚM_8f7753a1 + 1); if (!erro) { heap_VALOR[heap_VALOR[objeto_Referência + 2] + 2 + entrada_CONT_NÚM_8f7753a1] = dados_VALOR; heap_VALOR[objeto_Referência + 3] = entrada_CONT_NÚM_8f7753a1 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(nome_constante, "get") || Word_SMS(nome_constante, "remove")) && Word_SMS(descritor_constante, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(nome_constante, "set") && Word_SMS(descritor_constante, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean TI_Atribuído = Word_SMS(nome_constante, "set"); int dados_VALOR = TI_Atribuído ? 빼기(2) : 0, entrada_cargo_206f1c6d = 빼기(1), objeto_Referência = 빼기(2);
            if (!objeto_VALOR(objeto_Referência, 10)) return;
            int entrada_CONT_NÚM_8f7753a1 = heap_VALOR[objeto_Referência + 3], dados_MATRIZ = heap_VALOR[objeto_Referência + 2];
            if (entrada_cargo_206f1c6d < 0 || entrada_cargo_206f1c6d >= entrada_CONT_NÚM_8f7753a1) { 예외던짐(6, "list index"); return; }
            int Anterior_VALOR = heap_VALOR[dados_MATRIZ + 2 + entrada_cargo_206f1c6d];
            if (TI_Atribuído) heap_VALOR[dados_MATRIZ + 2 + entrada_cargo_206f1c6d] = dados_VALOR;
            if (Word_SMS(nome_constante, "remove")) { for (int Loop_ÍNDICE = entrada_cargo_206f1c6d + 1; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) heap_VALOR[dados_MATRIZ + 1 + Loop_ÍNDICE] = heap_VALOR[dados_MATRIZ + 2 + Loop_ÍNDICE]; heap_VALOR[dados_MATRIZ + 1 + entrada_CONT_NÚM_8f7753a1] = 0; heap_VALOR[objeto_Referência + 3] = entrada_CONT_NÚM_8f7753a1 - 1; }
            넣기(Anterior_VALOR, 2); return;
        }
        if (대응참조 && (Word_SMS(nome_constante, "get") || Word_SMS(nome_constante, "remove")) && Word_SMS(descritor_constante, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nome_constante, "put") && Word_SMS(descritor_constante, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nome_constante, "containsKey") && Word_SMS(descritor_constante, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(nome_constante, "put"), remover = Word_SMS(nome_constante, "remove");
            int dados_VALOR = 넣기여부 ? 빼기(2) : 0, Chave_Referência = 빼기(2), objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, 11)) return;
            int entrada_CONT_NÚM_8f7753a1 = heap_VALOR[objeto_Referência + 3], dados_MATRIZ = heap_VALOR[objeto_Referência + 2], 찾은여부 = -1;
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) if (값같음(Chave_Referência, heap_VALOR[dados_MATRIZ + 2 + 2 * Loop_ÍNDICE])) { 찾은여부 = Loop_ÍNDICE; break; }
            int Anterior_VALOR = 찾은여부 < 0 ? 0 : heap_VALOR[dados_MATRIZ + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objeto_Referência, (entrada_CONT_NÚM_8f7753a1 + 1) * 2); dados_MATRIZ = heap_VALOR[objeto_Referência + 2]; 찾은여부 = entrada_CONT_NÚM_8f7753a1; if (!erro) heap_VALOR[objeto_Referência + 3] = entrada_CONT_NÚM_8f7753a1 + 1; }
                if (!erro) { heap_VALOR[dados_MATRIZ + 2 + 2 * 찾은여부] = Chave_Referência; heap_VALOR[dados_MATRIZ + 3 + 2 * 찾은여부] = dados_VALOR; }
            }
            if (remover && 찾은여부 >= 0) { for (int Loop_ÍNDICE = 찾은여부 + 1; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) { heap_VALOR[dados_MATRIZ + 2 * Loop_ÍNDICE] = heap_VALOR[dados_MATRIZ + 2 + 2 * Loop_ÍNDICE]; heap_VALOR[dados_MATRIZ + 1 + 2 * Loop_ÍNDICE] = heap_VALOR[dados_MATRIZ + 3 + 2 * Loop_ÍNDICE]; } heap_VALOR[dados_MATRIZ + 2 * entrada_CONT_NÚM_8f7753a1] = 0; heap_VALOR[dados_MATRIZ + 1 + 2 * entrada_CONT_NÚM_8f7753a1] = 0; heap_VALOR[objeto_Referência + 3] = entrada_CONT_NÚM_8f7753a1 - 1; }
            if (Word_SMS(nome_constante, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Anterior_VALOR, 2);
            return;
        }
        falha_VALOR("unsupported collection method");
    }
    static boolean 잠금얻기(int objeto_Referência) {
        if (!TI_válido_objeto(objeto_Referência)) return false;
        if (잠금깊이[objeto_Referência] != 0 && bloquear_proprietário[objeto_Referência] != em_dia_thread + 1) { solicitação_de_alteração = true; return false; }
        bloquear_proprietário[objeto_Referência] = em_dia_thread + 1; 잠금깊이[objeto_Referência]++; return true;
    }
    static void lançar_bloquear(int objeto_Referência) {
        if (!TI_válido_objeto(objeto_Referência)) return;
        if (잠금깊이[objeto_Referência] == 0 || bloquear_proprietário[objeto_Referência] != em_dia_thread + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objeto_Referência] == 0) bloquear_proprietário[objeto_Referência] = 0;
    }
    static boolean mudar_thread() {
        thread_quadro[em_dia_thread] = quadro_ÍNDICE;
        if (quadro_ÍNDICE < em_dia_thread * 32) thread_Estado[em_dia_thread] = 3;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < contagem_de_threads; Loop_ÍNDICE++) if (thread_Estado[Loop_ÍNDICE] == 2 && thread_Estado[가닥대기[Loop_ÍNDICE]] == 3) thread_Estado[Loop_ÍNDICE] = 1;
        for (int Loop_ÍNDICE = 1; Loop_ÍNDICE <= contagem_de_threads; Loop_ÍNDICE++) {
            int Avançar_cargo = (em_dia_thread + Loop_ÍNDICE) % contagem_de_threads;
            if (thread_Estado[Avançar_cargo] == 1) { em_dia_thread = Avançar_cargo; quadro_ÍNDICE = thread_quadro[Avançar_cargo]; solicitação_de_alteração = false; return true; }
        }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < contagem_de_threads; Loop_ÍNDICE++) if (thread_Estado[Loop_ÍNDICE] != 3) { falha_VALOR("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nome_constante, int descritor_constante, int comando_CÓDIGO) { Processo_thread(nome_constante, descritor_constante, comando_CÓDIGO, false); }
    static void Processo_thread(int nome_constante, int descritor_constante, int comando_CÓDIGO, boolean Português) {
        if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, Português ? "LUCRO_Tarefa" : "yield") && Word_SMS(descritor_constante, "()V")) { solicitação_de_alteração = true; return; }
        if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "currentThread") && Word_SMS(descritor_constante, "()Ljava/lang/Thread;")) { 넣기(thread_objeto[em_dia_thread], 2); return; }
        if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>") && (Word_SMS(descritor_constante, "()V") || Word_SMS(descritor_constante, Português ? "(LPortuguês/nativo/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int alvo_email = Word_SMS(descritor_constante, "()V") ? 0 : 빼기(2), objeto_Referência = 빼기(2);
            if (!TI_válido_objeto(objeto_Referência)) return;
            if (heap_VALOR[objeto_Referência] == 13) { heap_VALOR[objeto_Referência + 2] = alvo_email; heap_Referência[objeto_Referência + 2] = 1; }
            else if (alvo_email != 0) falha_VALOR("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (comando_CÓDIGO == 182 && (Word_SMS(nome_constante, Português ? "START_Tarefa" : "start") || Word_SMS(nome_constante, Português ? "기다리기" : "join")) && Word_SMS(descritor_constante, "()V") || comando_CÓDIGO == 182 && Word_SMS(nome_constante, Português ? "살아있는가" : "isAlive") && Word_SMS(descritor_constante, "()Z")) {
            int objeto_Referência = 빼기(2); if (!TI_válido_objeto(objeto_Referência)) return;
            int conta_VALOR = -1; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < contagem_de_threads; Loop_ÍNDICE++) if (thread_objeto[Loop_ÍNDICE] == objeto_Referência) conta_VALOR = Loop_ÍNDICE;
            if (Word_SMS(nome_constante, Português ? "살아있는가" : "isAlive")) { 넣기(conta_VALOR >= 0 && thread_Estado[conta_VALOR] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(nome_constante, Português ? "기다리기" : "join")) { if (conta_VALOR >= 0 && thread_Estado[conta_VALOR] != 3) { 가닥대기[em_dia_thread] = conta_VALOR; thread_Estado[em_dia_thread] = 2; solicitação_de_alteração = true; } return; }
            if (conta_VALOR >= 0) { 예외던짐(Português ? 38 : 16, "thread already started"); return; }
            if (contagem_de_threads == 4) { falha_VALOR("thread limit (4 including main)"); return; }
            int alvo_email = heap_VALOR[objeto_Referência] == 13 ? heap_VALOR[objeto_Referência + 2] : objeto_Referência;
            int Arquivo_ÍNDICE = alvo_email > 0 && heap_VALOR[alvo_email] >= 32 ? nome_método(heap_VALOR[alvo_email] - 32, Português ? "Executar" : "run", "()V") : -1;
            if (alvo_email != 0 && Arquivo_ÍNDICE < 0) { falha_VALOR("Runnable.run required"); return; }
            conta_VALOR = contagem_de_threads++; thread_objeto[conta_VALOR] = objeto_Referência; thread_alvo[conta_VALOR] = alvo_email;
            int quadro = conta_VALOR * 32; thread_quadro[conta_VALOR] = Arquivo_ÍNDICE < 0 ? quadro - 1 : quadro; thread_Estado[conta_VALOR] = Arquivo_ÍNDICE < 0 ? 3 : 1;
            if (Arquivo_ÍNDICE >= 0) { quadro_método[quadro] = Arquivo_ÍNDICE; quadro_cargo[quadro] = método_START[Arquivo_ÍNDICE]; local_VALOR[quadro * 128] = alvo_email; local_TIPO[quadro * 128] = 2; }
            return;
        }
        falha_VALOR("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], email_SMS = new int[16];
    static int local_email() { return email_objeto(0x7f000001); }
    static int email_objeto(int VALOR) { int objeto_Referência = alocar_Armazenamento(14, 1); if (!erro) heap_VALOR[objeto_Referência + 2] = VALOR; return objeto_Referência; }
    static int 주소해독(int objeto_Referência) {
        if (objeto_Referência == 0 || textos_iguais(objeto_Referência, host_caractere("localhost"), false)) return 0x7f000001;
        if (!objeto_VALOR(objeto_Referência, 1)) return 0;
        int dados_VALOR = 0, total_CONT_NÚM = 0, email_byte = 0, 자릿수 = 0, entrada_CONT_NÚM_8f7753a1 = heap_VALOR[objeto_Referência + 1];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE <= entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) {
            int ponto_de_código = Loop_ÍNDICE == entrada_CONT_NÚM_8f7753a1 ? '.' : heap_VALOR[objeto_Referência + 2 + Loop_ÍNDICE];
            if (ponto_de_código == '.') { if (자릿수 == 0 || total_CONT_NÚM == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } dados_VALOR = dados_VALOR << 8 | email_byte; total_CONT_NÚM++; email_byte = 자릿수 = 0; }
            else { if (ponto_de_código < '0' || ponto_de_código > '9' || ++자릿수 > 3 || (email_byte = email_byte * 10 + ponto_de_código - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (total_CONT_NÚM != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return dados_VALOR;
    }
    static int email_caractere(int dados_VALOR) {
        int entrada_CONT_NÚM_8f7753a1 = 0;
        for (int deslocar = 24; deslocar >= 0; deslocar -= 8) {
            int email_byte = dados_VALOR >>> deslocar & 255;
            if (email_byte >= 100) email_SMS[entrada_CONT_NÚM_8f7753a1++] = '0' + email_byte / 100;
            if (email_byte >= 10) email_SMS[entrada_CONT_NÚM_8f7753a1++] = '0' + email_byte / 10 % 10;
            email_SMS[entrada_CONT_NÚM_8f7753a1++] = '0' + email_byte % 10; if (deslocar != 0) email_SMS[entrada_CONT_NÚM_8f7753a1++] = '.';
        }
        int objeto_Referência = alocar_Armazenamento(1, entrada_CONT_NÚM_8f7753a1); if (!erro) for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) heap_VALOR[objeto_Referência + 2 + Loop_ÍNDICE] = email_SMS[Loop_ÍNDICE]; return objeto_Referência;
    }
    static void 통신호출(int proprietário, int nome_constante, int descritor_constante, int comando_CÓDIGO) {
        if (Word_SMS(proprietário, "java/net/InetAddress")) {
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "getLoopbackAddress") && Word_SMS(descritor_constante, "()Ljava/net/InetAddress;")) { 넣기(local_email(), 2); return; }
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "getByName") && Word_SMS(descritor_constante, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int dados_VALOR = 주소해독(빼기(2)); if (던진객체 == 0 && !erro) 넣기(email_objeto(dados_VALOR), 2); return;
            }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "getHostAddress") && Word_SMS(descritor_constante, "()Ljava/lang/String;")) { int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, 14)) 넣기(email_caractere(heap_VALOR[objeto_Referência + 2]), 2); return; }
        }
        if (Word_SMS(proprietário, "java/net/DatagramPacket")) {
            if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>") && (Word_SMS(descritor_constante, "([BI)V") || Word_SMS(descritor_constante, "([BILjava/net/InetAddress;I)V"))) {
                boolean destino_VALOR_Referência = Word_SMS(descritor_constante, "([BILjava/net/InetAddress;I)V"); int número_da_porta = destino_VALOR_Referência ? 빼기(1) : 0, email_Referência = destino_VALOR_Referência ? 빼기(2) : 0;
                int entrada_CONT_NÚM_8f7753a1 = 빼기(1), dados_MATRIZ = 빼기(2), objeto_Referência = 빼기(2);
                if (!objeto_VALOR(objeto_Referência, 16) || !objeto_VALOR(dados_MATRIZ, 20)) return;
                if (entrada_CONT_NÚM_8f7753a1 < 0 || entrada_CONT_NÚM_8f7753a1 > heap_VALOR[dados_MATRIZ + 1] || número_da_porta < 0 || número_da_porta > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (email_Referência != 0 && !objeto_VALOR(email_Referência, 14)) return;
                heap_VALOR[objeto_Referência + 2] = dados_MATRIZ; heap_Referência[objeto_Referência + 2] = 1; heap_VALOR[objeto_Referência + 3] = entrada_CONT_NÚM_8f7753a1;
                heap_VALOR[objeto_Referência + 4] = email_Referência; heap_Referência[objeto_Referência + 4] = 1; heap_VALOR[objeto_Referência + 5] = número_da_porta; return;
            }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "setLength") && Word_SMS(descritor_constante, "(I)V")) {
                int entrada_CONT_NÚM_8f7753a1 = 빼기(1), objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, 16)) return;
                if (entrada_CONT_NÚM_8f7753a1 < 0 || entrada_CONT_NÚM_8f7753a1 > heap_VALOR[heap_VALOR[objeto_Referência + 2] + 1]) 예외던짐(9, "invalid datagram length"); else heap_VALOR[objeto_Referência + 3] = entrada_CONT_NÚM_8f7753a1; return;
            }
            if (comando_CÓDIGO == 182 && (Word_SMS(nome_constante, "getData") && Word_SMS(descritor_constante, "()[B") || Word_SMS(nome_constante, "getLength") && Word_SMS(descritor_constante, "()I") || Word_SMS(nome_constante, "getAddress") && Word_SMS(descritor_constante, "()Ljava/net/InetAddress;") || Word_SMS(nome_constante, "getPort") && Word_SMS(descritor_constante, "()I"))) {
                int objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, 16)) return;
                int entrada_cargo_206f1c6d = Word_SMS(nome_constante, "getData") ? 2 : Word_SMS(nome_constante, "getLength") ? 3 : Word_SMS(nome_constante, "getAddress") ? 4 : 5;
                넣기(heap_VALOR[objeto_Referência + entrada_cargo_206f1c6d], entrada_cargo_206f1c6d == 2 || entrada_cargo_206f1c6d == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(proprietário, "java/net/DatagramSocket")) {
            if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>") && (Word_SMS(descritor_constante, "()V") || Word_SMS(descritor_constante, "(I)V"))) {
                int número_da_porta = Word_SMS(descritor_constante, "()V") ? 0 : 빼기(1), objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, 15)) return;
                if (número_da_porta < 0 || número_da_porta > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = espaço_do_utilizador.abrir_rede(número_da_porta); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else heap_VALOR[objeto_Referência + 2] = 열린파일번호; return;
            }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "setSoTimeout") && Word_SMS(descritor_constante, "(I)V")) {
                int 밀리초값 = 빼기(1), objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_VALOR[objeto_Referência + 3] = 밀리초값; return;
            }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "getLocalPort") && Word_SMS(descritor_constante, "()I")) { int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, 15)) 넣기(heap_VALOR[objeto_Referência + 2] < 0 ? -1 : espaço_do_utilizador.rede_porta(heap_VALOR[objeto_Referência + 2]), 1); return; }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "isClosed") && Word_SMS(descritor_constante, "()Z")) { int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, 15)) 넣기(heap_VALOR[objeto_Referência + 2] < 0 ? 1 : 0, 1); return; }
            if (comando_CÓDIGO == 182 && Word_SMS(nome_constante, "close") && Word_SMS(descritor_constante, "()V")) { int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, 15) && heap_VALOR[objeto_Referência + 2] >= 0) { espaço_do_utilizador.Close_Arquivo_descritor(heap_VALOR[objeto_Referência + 2]); heap_VALOR[objeto_Referência + 2] = -1; } return; }
            if (comando_CÓDIGO == 182 && (Word_SMS(nome_constante, "send") || Word_SMS(nome_constante, "receive")) && Word_SMS(descritor_constante, "(Ljava/net/DatagramPacket;)V")) {
                int pacote = 빼기(2), objeto_Referência = 빼기(2); if (!objeto_VALOR(pacote, 16) || !objeto_VALOR(objeto_Referência, 15)) return;
                int dados_MATRIZ = heap_VALOR[pacote + 2], válido_duração = heap_VALOR[pacote + 3], 열린파일번호 = heap_VALOR[objeto_Referência + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(nome_constante, "send")) {
                    if (!objeto_VALOR(heap_VALOR[pacote + 4], 14)) return;
                    if (válido_duração > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < válido_duração; Loop_ÍNDICE++) 통신임시[Loop_ÍNDICE] = heap_VALOR[dados_MATRIZ + 2 + Loop_ÍNDICE];
                    if (espaço_do_utilizador.enviar_rede(열린파일번호, heap_VALOR[heap_VALOR[pacote + 4] + 2], heap_VALOR[pacote + 5], 통신임시, válido_duração) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int entrada_CONT_NÚM_8f7753a1 = espaço_do_utilizador.receber_rede(열린파일번호, 통신임시, válido_duração > 512 ? 512 : válido_duração);
                    if (entrada_CONT_NÚM_8f7753a1 == -11) {
                        int hora_atual = espaço_do_utilizador.밀리초();
                        if (heap_VALOR[objeto_Referência + 4] == 0) heap_VALOR[objeto_Referência + 4] = hora_atual + 1;
                        if (heap_VALOR[objeto_Referência + 3] > 0 && hora_atual - (heap_VALOR[objeto_Referência + 4] - 1) >= heap_VALOR[objeto_Referência + 3]) { heap_VALOR[objeto_Referência + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objeto_Referência, 2); 넣기(pacote, 2); quadro_cargo[quadro_ÍNDICE] = quadro_instrução[quadro_ÍNDICE]; solicitação_de_alteração = true; return;
                    }
                    heap_VALOR[objeto_Referência + 4] = 0;
                    if (entrada_CONT_NÚM_8f7753a1 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) heap_VALOR[dados_MATRIZ + 2 + Loop_ÍNDICE] = (byte)통신임시[Loop_ÍNDICE];
                    heap_VALOR[pacote + 3] = entrada_CONT_NÚM_8f7753a1; heap_VALOR[pacote + 4] = email_objeto(통신임시[513]); heap_Referência[pacote + 4] = 1; heap_VALOR[pacote + 5] = 통신임시[512];
                }
                return;
            }
        }
        falha_VALOR("unsupported java.net method");
    }
    static boolean 흐름대기(int objeto_Referência) {
        int hora_atual = espaço_do_utilizador.밀리초();
        if (heap_VALOR[objeto_Referência + 5] == 0) heap_VALOR[objeto_Referência + 5] = hora_atual + 1;
        if (heap_VALOR[objeto_Referência + 3] > 0 && hora_atual - (heap_VALOR[objeto_Referência + 5] - 1) >= heap_VALOR[objeto_Referência + 3]) { heap_VALOR[objeto_Referência + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        quadro_cargo[quadro_ÍNDICE] = quadro_instrução[quadro_ÍNDICE]; solicitação_de_alteração = true; return true;
    }
    static void 흐름호출(int proprietário, int nome_constante, int descritor_constante, int comando_CÓDIGO) {
        boolean receber_página = Word_SMS(proprietário, "java/net/ServerSocket"), fluxo = Word_SMS(proprietário, "java/io/InputStream") || Word_SMS(proprietário, "java/io/OutputStream");
        if (!fluxo && comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>")) {
            boolean TI_vazio_Estado = Word_SMS(descritor_constante, "()V"), 이름지정여부 = Word_SMS(descritor_constante, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(descritor_constante, "(Ljava/net/InetAddress;I)V");
            if (!(TI_vazio_Estado || receber_página && Word_SMS(descritor_constante, "(I)V") || !receber_página && (이름지정여부 || 주소지정여부))) { falha_VALOR("unsupported socket constructor"); return; }
            int número_da_porta = TI_vazio_Estado ? 0 : 빼기(1), email_Referência = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objeto_Referência = 빼기(2);
            if (!objeto_VALOR(objeto_Referência, receber_página ? 18 : 17)) return;
            if (número_da_porta < 0 || número_da_porta > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objeto_VALOR(email_Referência, 14)) return;
            int ID_de_rede = 이름지정여부 ? 주소해독(email_Referência) : 주소지정여부 ? heap_VALOR[email_Referência + 2] : 0x7f000001;
            if (erro || 던진객체 != 0) return;
            int 열린파일번호 = espaço_do_utilizador.fluxo_visual(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = TI_vazio_Estado ? 0 : receber_página ? espaço_do_utilizador.fluxo_visual(1, 열린파일번호, número_da_porta) : espaço_do_utilizador.Conexão_fluxo(열린파일번호, ID_de_rede, número_da_porta);
            if (처리값 < 0) { espaço_do_utilizador.Close_Arquivo_descritor(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            heap_VALOR[objeto_Referência + 2] = 열린파일번호; heap_VALOR[objeto_Referência + 4] = número_da_porta; heap_VALOR[objeto_Referência + 6] = TI_vazio_Estado ? 0 : 1; return;
        }
        if (!fluxo && Word_SMS(nome_constante, "setSoTimeout") && Word_SMS(descritor_constante, "(I)V")) { int 밀리초값 = 빼기(1), objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, receber_página ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_VALOR[objeto_Referência + 3] = 밀리초값; return; }
        if (!fluxo && Word_SMS(nome_constante, "close") && Word_SMS(descritor_constante, "()V")) { int objeto_Referência = 빼기(2); if (objeto_VALOR(objeto_Referência, receber_página ? 18 : 17) && heap_VALOR[objeto_Referência + 2] >= 0) { espaço_do_utilizador.Close_Arquivo_descritor(heap_VALOR[objeto_Referência + 2]); heap_VALOR[objeto_Referência + 2] = -1; } return; }
        if (!fluxo && (Word_SMS(nome_constante, "getLocalPort") || Word_SMS(nome_constante, "getPort") || Word_SMS(nome_constante, "isClosed") || Word_SMS(nome_constante, "isConnected"))) {
            int objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, receber_página ? 18 : 17)) return;
            넣기(Word_SMS(nome_constante, "isClosed") ? heap_VALOR[objeto_Referência + 2] < 0 ? 1 : 0 : Word_SMS(nome_constante, "isConnected") ? heap_VALOR[objeto_Referência + 6] : Word_SMS(nome_constante, "getPort") ? heap_VALOR[objeto_Referência + 4] : heap_VALOR[objeto_Referência + 2] < 0 ? -1 : espaço_do_utilizador.fluxo_visual(4, heap_VALOR[objeto_Referência + 2], 0), 1); return;
        }
        if (receber_página && Word_SMS(nome_constante, "accept") && Word_SMS(descritor_constante, "()Ljava/net/Socket;")) {
            int objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, 18)) return; int 열린파일번호 = espaço_do_utilizador.fluxo_visual(3, heap_VALOR[objeto_Referência + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objeto_Referência)) 넣기(objeto_Referência, 2); return; }
            heap_VALOR[objeto_Referência + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = alocar_Armazenamento(17, 5); if (erro) { espaço_do_utilizador.Close_Arquivo_descritor(열린파일번호); return; } heap_VALOR[반환값 + 2] = 열린파일번호; heap_VALOR[반환값 + 4] = espaço_do_utilizador.fluxo_visual(5, 열린파일번호, 0); heap_VALOR[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!receber_página && !fluxo && ((Word_SMS(nome_constante, "getInputStream") && Word_SMS(descritor_constante, "()Ljava/io/InputStream;")) || (Word_SMS(nome_constante, "getOutputStream") && Word_SMS(descritor_constante, "()Ljava/io/OutputStream;")))) {
            int objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, 17)) return; if (heap_VALOR[objeto_Referência + 2] < 0 || heap_VALOR[objeto_Referência + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = alocar_Armazenamento(19, 4); if (erro) return; heap_VALOR[반환값 + 2] = objeto_Referência; heap_Referência[반환값 + 2] = 1; heap_VALOR[반환값 + 3] = Word_SMS(nome_constante, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (fluxo) {
            boolean 읽기여부 = Word_SMS(nome_constante, "read"), TI_gravar_cirurgia = Word_SMS(nome_constante, "write"), bloco = Word_SMS(descritor_constante, "([B)I") || Word_SMS(descritor_constante, "([B)V"), TI_SUBMATRIZ = Word_SMS(descritor_constante, "([BII)I") || Word_SMS(descritor_constante, "([BII)V");
            int entrada_CONT_NÚM_8f7753a1 = TI_SUBMATRIZ ? 빼기(1) : 0, 시작변위 = TI_SUBMATRIZ ? 빼기(1) : 0, dados_MATRIZ = bloco || TI_SUBMATRIZ ? 빼기(2) : 0;
            int dados_VALOR = TI_gravar_cirurgia && Word_SMS(descritor_constante, "(I)V") ? 빼기(1) : 0, objeto_Referência = 빼기(2);
            if (!objeto_VALOR(objeto_Referência, 19)) return; int pai_Referência = heap_VALOR[objeto_Referência + 2], 열린파일번호 = heap_VALOR[pai_Referência + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(nome_constante, "close") && Word_SMS(descritor_constante, "()V")) { espaço_do_utilizador.Close_Arquivo_descritor(열린파일번호); heap_VALOR[pai_Referência + 2] = -1; return; }
            if (Word_SMS(nome_constante, "flush") && Word_SMS(descritor_constante, "()V")) return;
            if ((!읽기여부 && !TI_gravar_cirurgia) || 읽기여부 != (heap_VALOR[objeto_Referência + 3] == 0)) { falha_VALOR("unsupported stream operation"); return; }
            if (bloco || TI_SUBMATRIZ) { if (!objeto_VALOR(dados_MATRIZ, 20)) return; if (bloco) entrada_CONT_NÚM_8f7753a1 = heap_VALOR[dados_MATRIZ + 1]; if (시작변위 < 0 || entrada_CONT_NÚM_8f7753a1 < 0 || 시작변위 > heap_VALOR[dados_MATRIZ + 1] - entrada_CONT_NÚM_8f7753a1) { 예외던짐(6, "stream array bounds"); return; } }
            else entrada_CONT_NÚM_8f7753a1 = 1;
            if (entrada_CONT_NÚM_8f7753a1 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int concluído_CONT_NÚM = TI_gravar_cirurgia ? heap_VALOR[objeto_Referência + 4] : 0, 처리값 = 0;
            while (concluído_CONT_NÚM < entrada_CONT_NÚM_8f7753a1) {
                처리값 = 읽기여부 ? espaço_do_utilizador.파일한바이트읽기(열린파일번호) : espaço_do_utilizador.파일한바이트쓰기(열린파일번호, bloco || TI_SUBMATRIZ ? heap_VALOR[dados_MATRIZ + 2 + 시작변위 + concluído_CONT_NÚM] : dados_VALOR);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bloco || TI_SUBMATRIZ)) heap_VALOR[dados_MATRIZ + 2 + 시작변위 + concluído_CONT_NÚM] = (byte)처리값;
                concluído_CONT_NÚM++; if (읽기여부 && !(bloco || TI_SUBMATRIZ)) break;
            }
            if (처리값 == -11 && (TI_gravar_cirurgia || concluído_CONT_NÚM == 0)) {
                heap_VALOR[objeto_Referência + 4] = concluído_CONT_NÚM;
                if (흐름대기(pai_Referência)) { 넣기(objeto_Referência, 2); if (bloco || TI_SUBMATRIZ) 넣기(dados_MATRIZ, 2); if (TI_SUBMATRIZ) { 넣기(시작변위, 1); 넣기(entrada_CONT_NÚM_8f7753a1, 1); } if (TI_gravar_cirurgia && !(bloco || TI_SUBMATRIZ)) 넣기(dados_VALOR, 1); } return;
            }
            heap_VALOR[objeto_Referência + 4] = 0; heap_VALOR[pai_Referência + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(concluído_CONT_NÚM == 0 && 처리값 == 256 ? -1 : bloco || TI_SUBMATRIZ ? concluído_CONT_NÚM : 처리값, 1); return;
        }
        falha_VALOR("unsupported Socket/ServerSocket method");
    }
    static int[] tela_Referência = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nome_constante) {
        if (Word_SMS(nome_constante, "Português/nativo/Janela")) return 24;
        if (Word_SMS(nome_constante, "Português/nativo/Etiqueta")) return 26;
        if (Word_SMS(nome_constante, "Português/nativo/botão")) return 27;
        if (Word_SMS(nome_constante, "Português/nativo/campo_de_texto")) return 28;
        if (Word_SMS(nome_constante, "Português/nativo/Ação_aviso")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nome_constante) {
        return 한국어화면종(nome_constante) != 0 || Word_SMS(nome_constante, "Português/nativo/tela_elemento") || Word_SMS(nome_constante, "Português/nativo/Evento_Fila");
    }
    static int tela_aula(int nome_constante) {
        int 한국어종 = 한국어화면종(nome_constante); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(nome_constante, "javax/swing/JFrame")) return 24;
        if (Word_SMS(nome_constante, "javax/swing/JPanel")) return 25;
        if (Word_SMS(nome_constante, "javax/swing/JLabel")) return 26;
        if (Word_SMS(nome_constante, "javax/swing/JButton")) return 27;
        if (Word_SMS(nome_constante, "javax/swing/JTextField")) return 28;
        if (Word_SMS(nome_constante, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(nome_constante, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean tela_proprietário(int nome_constante) {
        return tela_aula(nome_constante) != 0 || Word_SMS(nome_constante, "java/awt/Component") || Word_SMS(nome_constante, "java/awt/Container") || Word_SMS(nome_constante, "javax/swing/JComponent") || Word_SMS(nome_constante, "javax/swing/AbstractButton") || Word_SMS(nome_constante, "javax/swing/text/JTextComponent") || Word_SMS(nome_constante, "javax/swing/SwingUtilities");
    }
    static boolean tela_objeto(int objeto_Referência) { if (!TI_válido_objeto(objeto_Referência)) return false; if (heap_VALOR[objeto_Referência] < 24 || heap_VALOR[objeto_Referência] > 28) { falha_VALOR("unsupported Swing receiver"); return false; } return true; }
    static void set_tela_caractere(int objeto_Referência, int SMS_Referência) {
        if (SMS_Referência != 0 && !objeto_VALOR(SMS_Referência, 1)) return;
        int entrada_CONT_NÚM_8f7753a1 = SMS_Referência == 0 ? 0 : heap_VALOR[SMS_Referência + 1]; if (entrada_CONT_NÚM_8f7753a1 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) 화면글임시[Loop_ÍNDICE] = heap_VALOR[SMS_Referência + 2 + Loop_ÍNDICE];
        if (espaço_do_utilizador.tela_SMS(heap_VALOR[objeto_Referência + 2], 화면글임시, entrada_CONT_NÚM_8f7753a1) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        heap_VALOR[objeto_Referência + 3] = SMS_Referência; heap_Referência[objeto_Referência + 3] = 1;
    }
    static int leitura_tela_caractere(int objeto_Referência) {
        int conta_VALOR = heap_VALOR[objeto_Referência + 2], entrada_CONT_NÚM_8f7753a1 = espaço_do_utilizador.tela_conexão(8, conta_VALOR, 0, 0, 0, 0), 사용수 = 0;
        if (entrada_CONT_NÚM_8f7753a1 < 0) { falha_VALOR("GUI text read failed"); return 0; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) { int 부호값 = espaço_do_utilizador.tela_conexão(9, conta_VALOR, Loop_ÍNDICE, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = alocar_Armazenamento(1, 사용수); if (!erro) for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 사용수; Loop_ÍNDICE++) heap_VALOR[반환값 + 2 + Loop_ÍNDICE] = 화면글임시[Loop_ÍNDICE]; return 반환값;
    }
    /* Português 객체를 직접 만들고 kernel_VALOR tela 기능에 연결한다. Swing objeto_VALOR/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int proprietário, int nome_constante, int descritor_constante, int comando_CÓDIGO) {
        if (Word_SMS(proprietário, "Português/nativo/Evento_Fila")) {
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "나중에실행") && Word_SMS(descritor_constante, "(LPortuguês/nativo/실행할일;)V")) {
                int Tarefa_Ação = 빼기(2); if (!TI_válido_objeto(Tarefa_Ação)) return;
                if (나중수 == 8) { falha_VALOR("tela 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = Tarefa_Ação; return;
            }
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "사건처리중인가") && Word_SMS(descritor_constante, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            falha_VALOR("지원하지 않는 Português tela 일정 호출"); return;
        }
        if (Word_SMS(proprietário, "Português/nativo/Ação_aviso")) {
            int aviso = 빼기(2); if (!objeto_VALOR(aviso, 29) || heap_VALOR[aviso + 3] == 0) return;
            if (Word_SMS(nome_constante, "origem_do_evento") && Word_SMS(descritor_constante, "()LPortuguês/nativo/tela_elemento;")) 넣기(heap_VALOR[aviso + 2], 2);
            else if (Word_SMS(nome_constante, "comando_SMS") && Word_SMS(descritor_constante, "()Ljava/lang/String;")) 넣기(leitura_tela_caractere(heap_VALOR[aviso + 2]), 2);
            else if (Word_SMS(nome_constante, "ÍNDICE") && Word_SMS(descritor_constante, "()I")) 넣기(1001, 1);
            else falha_VALOR("지원하지 않는 Português Acção aviso 호출"); return;
        }
        if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>")) {
            int Tipo_VALOR = 한국어화면종(proprietário), 받이 = 0, 가로 = 0, Vertical_cargo = 0, 폭 = 0, altura_VALOR = 0;
            if (Tipo_VALOR == 24 && Word_SMS(descritor_constante, "(Ljava/lang/String;II)V")) {
                altura_VALOR = 빼기(1); 폭 = 빼기(1); 가로 = (espaço_do_utilizador.화면너비() - 폭) / 2; Vertical_cargo = (espaço_do_utilizador.tela_altura() - altura_VALOR) / 2;
            } else if ((Tipo_VALOR == 26 || Tipo_VALOR == 28) && Word_SMS(descritor_constante, "(Ljava/lang/String;IIII)V") || Tipo_VALOR == 27 && Word_SMS(descritor_constante, "(Ljava/lang/String;IIIILPortuguês/nativo/동작받이;)V")) {
                if (Tipo_VALOR == 27) 받이 = 빼기(2);
                altura_VALOR = 빼기(1); 폭 = 빼기(1); Vertical_cargo = 빼기(1); 가로 = 빼기(1);
            } else { falha_VALOR("지원하지 않는 Português tela 생성자"); return; }
            int texto = 빼기(2), elemento_VALOR = 빼기(2); if (!tela_objeto(elemento_VALOR)) return;
            if (폭 < 1 || altura_VALOR < 1 || 가로 < 0 || Vertical_cargo < 0 || 폭 > espaço_do_utilizador.화면너비() - 가로 || altura_VALOR > espaço_do_utilizador.tela_altura() - Vertical_cargo) { 예외던짐(27, "tela 영역을 벗어난 크기입니다"); return; }
            int ÍNDICE = espaço_do_utilizador.tela_conexão(0, Tipo_VALOR - 23, 0, 0, 0, 0);
            if (ÍNDICE < 1 || ÍNDICE > 32) { falha_VALOR("tela elemento_VALOR 자리가 가득 찼습니다"); return; }
            heap_VALOR[elemento_VALOR + 2] = ÍNDICE; tela_Referência[ÍNDICE - 1] = elemento_VALOR;
            heap_VALOR[elemento_VALOR + 5] = 가로; heap_VALOR[elemento_VALOR + 6] = Vertical_cargo; heap_VALOR[elemento_VALOR + 7] = 폭; heap_VALOR[elemento_VALOR + 8] = altura_VALOR; heap_VALOR[elemento_VALOR + 10] = 2;
            heap_VALOR[elemento_VALOR + 4] = 받이; heap_Referência[elemento_VALOR + 4] = 1; heap_VALOR[elemento_VALOR + 12] = 1;
            espaço_do_utilizador.tela_conexão(1, ÍNDICE, 가로, Vertical_cargo, 폭, altura_VALOR);
            if (Tipo_VALOR == 24) espaço_do_utilizador.tela_conexão(7, ÍNDICE, 2, 0, 0, 0);
            set_tela_caractere(elemento_VALOR, texto); return;
        }
        if (comando_CÓDIGO != 182) { falha_VALOR("잘못된 Português tela 호출 comando"); return; }
        if (Word_SMS(nome_constante, "gravar_SMS") && Word_SMS(descritor_constante, "(Ljava/lang/String;)V")) {
            int texto = 빼기(2), elemento_VALOR = 빼기(2); if (tela_objeto(elemento_VALOR)) set_tela_caractere(elemento_VALOR, texto); return;
        }
        if (Word_SMS(nome_constante, "leitura_SMS") && Word_SMS(descritor_constante, "()Ljava/lang/String;")) {
            int elemento_VALOR = 빼기(2); if (tela_objeto(elemento_VALOR)) 넣기(leitura_tela_caractere(elemento_VALOR), 2); return;
        }
        if (Word_SMS(nome_constante, "동작맡기기") && Word_SMS(descritor_constante, "(LPortuguês/nativo/동작받이;)V")) {
            int 받이 = 빼기(2), elemento_VALOR = 빼기(2);
            if (tela_objeto(elemento_VALOR)) { heap_VALOR[elemento_VALOR + 4] = 받이; heap_Referência[elemento_VALOR + 4] = 1; heap_VALOR[elemento_VALOR + 12] = 1; } return;
        }
        if (Word_SMS(nome_constante, "Adicionar_elemento") && Word_SMS(descritor_constante, "(LPortuguês/nativo/tela_elemento;)V")) {
            int filho_VALOR = 빼기(2), pai_VALOR = 빼기(2); if (!tela_objeto(filho_VALOR) || !tela_objeto(pai_VALOR)) return;
            if (espaço_do_utilizador.tela_conexão(2, heap_VALOR[pai_VALOR + 2], heap_VALOR[filho_VALOR + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 tela 부모입니다"); return; }
            heap_VALOR[filho_VALOR + 11] = pai_VALOR; heap_Referência[filho_VALOR + 11] = 1; return;
        }
        if (Word_SMS(nome_constante, "자리정하기") && Word_SMS(descritor_constante, "(IIII)V")) {
            int altura_VALOR = 빼기(1), 폭 = 빼기(1), Vertical_cargo = 빼기(1), 가로 = 빼기(1), elemento_VALOR = 빼기(2); if (!tela_objeto(elemento_VALOR)) return;
            if (espaço_do_utilizador.tela_conexão(1, heap_VALOR[elemento_VALOR + 2], 가로, Vertical_cargo, 폭, altura_VALOR) < 0) { 예외던짐(27, "tela 영역을 벗어난 자리입니다"); return; }
            heap_VALOR[elemento_VALOR + 5] = 가로; heap_VALOR[elemento_VALOR + 6] = Vertical_cargo; heap_VALOR[elemento_VALOR + 7] = 폭; heap_VALOR[elemento_VALOR + 8] = altura_VALOR; return;
        }
        if ((Word_SMS(nome_constante, "mostrar_janela") || Word_SMS(nome_constante, "Fechar")) && Word_SMS(descritor_constante, "()V")) {
            boolean Visibilidade_VALOR = Word_SMS(nome_constante, "mostrar_janela"); int elemento_VALOR = 빼기(2); if (!tela_objeto(elemento_VALOR)) return;
            if (espaço_do_utilizador.tela_conexão(Visibilidade_VALOR ? 3 : 4, heap_VALOR[elemento_VALOR + 2], Visibilidade_VALOR ? 1 : 0, 0, 0, 0) < 0) { falha_VALOR("화면은 interativo 명령에서 실행해야 합니다"); return; }
            heap_VALOR[elemento_VALOR + 9] = Visibilidade_VALOR ? 1 : 0; return;
        }
        if (Word_SMS(nome_constante, "보이는가") && Word_SMS(descritor_constante, "()Z")) { int elemento_VALOR = 빼기(2); if (tela_objeto(elemento_VALOR)) 넣기(heap_VALOR[elemento_VALOR + 9], 1); return; }
        falha_VALOR("지원하지 않는 Português tela método_VALOR");
    }
    static void 화면호출(int proprietário, int nome_constante, int descritor_constante, int comando_CÓDIGO) {
        if (Word_SMS(proprietário, "javax/swing/SwingUtilities")) {
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "invokeLater") && Word_SMS(descritor_constante, "(Ljava/lang/Runnable;)V")) { int objeto_Referência = 빼기(2); if (!TI_válido_objeto(objeto_Referência)) return; if (나중수 == 8) { falha_VALOR("invokeLater queue full"); return; } 나중실행[나중수++] = objeto_Referência; return; }
            if (comando_CÓDIGO == 184 && Word_SMS(nome_constante, "isEventDispatchThread") && Word_SMS(descritor_constante, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            falha_VALOR("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(proprietário, "java/awt/event/ActionEvent")) {
            int objeto_Referência = 빼기(2); if (!objeto_VALOR(objeto_Referência, 29)) return;
            if (Word_SMS(nome_constante, "getSource") && Word_SMS(descritor_constante, "()Ljava/lang/Object;")) 넣기(heap_VALOR[objeto_Referência + 2], 2);
            else if (Word_SMS(nome_constante, "getActionCommand") && Word_SMS(descritor_constante, "()Ljava/lang/String;")) 넣기(leitura_tela_caractere(heap_VALOR[objeto_Referência + 2]), 2);
            else if (Word_SMS(nome_constante, "getID") && Word_SMS(descritor_constante, "()I")) 넣기(1001, 1);
            else falha_VALOR("unsupported ActionEvent method"); return;
        }
        if (comando_CÓDIGO == 183 && Word_SMS(nome_constante, "<init>")) {
            int COLS = 0, SMS_Referência = 0;
            if (Word_SMS(descritor_constante, "(I)V")) COLS = 빼기(1);
            else if (Word_SMS(descritor_constante, "(Ljava/lang/String;I)V")) { COLS = 빼기(1); SMS_Referência = 빼기(2); }
            else if (Word_SMS(descritor_constante, "(Ljava/lang/String;)V")) SMS_Referência = 빼기(2);
            else if (Word_SMS(descritor_constante, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(descritor_constante, "()V")) { falha_VALOR("unsupported Swing constructor"); return; }
            int objeto_Referência = 빼기(2); if (!TI_válido_objeto(objeto_Referência)) return;
            if (heap_VALOR[objeto_Referência] == 30) { falha_VALOR("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!tela_objeto(objeto_Referência) || COLS < 0) return;
            int conta_VALOR = espaço_do_utilizador.tela_conexão(0, heap_VALOR[objeto_Referência] - 23, 0, 0, 0, 0);
            if (conta_VALOR < 1 || conta_VALOR > 32) { falha_VALOR("GUI widget slots exhausted"); return; }
            heap_VALOR[objeto_Referência + 2] = conta_VALOR; tela_Referência[conta_VALOR - 1] = objeto_Referência; heap_VALOR[objeto_Referência + 5] = heap_VALOR[objeto_Referência] == 24 ? 130 : 16; heap_VALOR[objeto_Referência + 6] = heap_VALOR[objeto_Referência] == 24 ? 110 : 16;
            heap_VALOR[objeto_Referência + 7] = heap_VALOR[objeto_Referência] == 24 ? 380 : 220; heap_VALOR[objeto_Referência + 8] = heap_VALOR[objeto_Referência] == 24 ? 240 : 28; heap_VALOR[objeto_Referência + 10] = 1;
            set_tela_caractere(objeto_Referência, SMS_Referência); return;
        }
        if (Word_SMS(nome_constante, "setText") || Word_SMS(nome_constante, "setTitle")) { int SMS_Referência = 빼기(2), objeto_Referência = 빼기(2); if (tela_objeto(objeto_Referência) && Word_SMS(descritor_constante, "(Ljava/lang/String;)V")) set_tela_caractere(objeto_Referência, SMS_Referência); return; }
        if (Word_SMS(nome_constante, "getText") || Word_SMS(nome_constante, "getTitle")) { int objeto_Referência = 빼기(2); if (tela_objeto(objeto_Referência) && Word_SMS(descritor_constante, "()Ljava/lang/String;")) 넣기(leitura_tela_caractere(objeto_Referência), 2); return; }
        if (Word_SMS(nome_constante, "addActionListener") && Word_SMS(descritor_constante, "(Ljava/awt/event/ActionListener;)V")) { int receber_Referência = 빼기(2), objeto_Referência = 빼기(2); if (tela_objeto(objeto_Referência)) { heap_VALOR[objeto_Referência + 4] = receber_Referência; heap_Referência[objeto_Referência + 4] = 1; } return; }
        if (Word_SMS(nome_constante, "getContentPane") && Word_SMS(descritor_constante, "()Ljava/awt/Container;")) { int objeto_Referência = 빼기(2); if (tela_objeto(objeto_Referência)) 넣기(objeto_Referência, 2); return; }
        if (Word_SMS(nome_constante, "setLayout") && Word_SMS(descritor_constante, "(Ljava/awt/LayoutManager;)V")) { int Layout_Referência = 빼기(2), objeto_Referência = 빼기(2); if (tela_objeto(objeto_Referência) && Layout_Referência != 0) falha_VALOR("only absolute layout (null) is supported"); return; }
        if (Word_SMS(nome_constante, "add") && (Word_SMS(descritor_constante, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(descritor_constante, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Layout_doença = Word_SMS(descritor_constante, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Layout_doença) 빼기(2);
            int filho_Referência = 빼기(2), objeto_Referência = 빼기(2); if (!tela_objeto(filho_Referência) || !tela_objeto(objeto_Referência)) return;
            if (espaço_do_utilizador.tela_conexão(2, heap_VALOR[objeto_Referência + 2], heap_VALOR[filho_Referência + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            heap_VALOR[filho_Referência + 11] = objeto_Referência; heap_Referência[filho_Referência + 11] = 1; if (!Layout_doença) 넣기(filho_Referência, 2); return;
        }
        if (Word_SMS(nome_constante, "setBounds") && Word_SMS(descritor_constante, "(IIII)V")) {
            int altura_VALOR = 빼기(1), 너비 = 빼기(1), Y_coordenada = 빼기(1), coordenada_X = 빼기(1), objeto_Referência = 빼기(2); if (!tela_objeto(objeto_Referência)) return;
            if (espaço_do_utilizador.tela_conexão(1, heap_VALOR[objeto_Referência + 2], coordenada_X, Y_coordenada, 너비, altura_VALOR) < 0) { 예외던짐(9, "GUI bounds"); return; }
            heap_VALOR[objeto_Referência + 5] = coordenada_X; heap_VALOR[objeto_Referência + 6] = Y_coordenada; heap_VALOR[objeto_Referência + 7] = 너비; heap_VALOR[objeto_Referência + 8] = altura_VALOR; return;
        }
        if (Word_SMS(nome_constante, "setSize") && Word_SMS(descritor_constante, "(II)V")) {
            int altura_VALOR = 빼기(1), 너비 = 빼기(1), objeto_Referência = 빼기(2); if (!tela_objeto(objeto_Referência)) return;
            if (espaço_do_utilizador.tela_conexão(1, heap_VALOR[objeto_Referência + 2], heap_VALOR[objeto_Referência + 5], heap_VALOR[objeto_Referência + 6], 너비, altura_VALOR) < 0) 예외던짐(9, "GUI size"); else { heap_VALOR[objeto_Referência + 7] = 너비; heap_VALOR[objeto_Referência + 8] = altura_VALOR; } return;
        }
        if (Word_SMS(nome_constante, "setLocationRelativeTo") && Word_SMS(descritor_constante, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objeto_Referência = 빼기(2); if (!tela_objeto(objeto_Referência)) return; if (상대배치 != 0) { falha_VALOR("only screen centering supported"); return; } heap_VALOR[objeto_Referência + 5] = (espaço_do_utilizador.화면너비() - heap_VALOR[objeto_Referência + 7]) / 2; heap_VALOR[objeto_Referência + 6] = (espaço_do_utilizador.tela_altura() - heap_VALOR[objeto_Referência + 8]) / 2; espaço_do_utilizador.tela_conexão(1, heap_VALOR[objeto_Referência + 2], heap_VALOR[objeto_Referência + 5], heap_VALOR[objeto_Referência + 6], heap_VALOR[objeto_Referência + 7], heap_VALOR[objeto_Referência + 8]); return; }
        if (Word_SMS(nome_constante, "setDefaultCloseOperation") && Word_SMS(descritor_constante, "(I)V")) { int Policy = 빼기(1), objeto_Referência = 빼기(2); if (tela_objeto(objeto_Referência)) { if (Policy < 0 || Policy > 3) 예외던짐(9, "close policy"); else { heap_VALOR[objeto_Referência + 10] = Policy; espaço_do_utilizador.tela_conexão(7, heap_VALOR[objeto_Referência + 2], Policy, 0, 0, 0); } } return; }
        if (Word_SMS(nome_constante, "setVisible") && Word_SMS(descritor_constante, "(Z)V")) { int dados_VALOR = 빼기(1), objeto_Referência = 빼기(2); if (tela_objeto(objeto_Referência)) { int 처리값 = espaço_do_utilizador.tela_conexão(3, heap_VALOR[objeto_Referência + 2], dados_VALOR, 0, 0, 0); if (처리값 < 0) falha_VALOR("Swing requires a standalone interactive command"); else heap_VALOR[objeto_Referência + 9] = dados_VALOR; } return; }
        if (Word_SMS(nome_constante, "dispose") && Word_SMS(descritor_constante, "()V")) { int objeto_Referência = 빼기(2); if (tela_objeto(objeto_Referência)) { espaço_do_utilizador.tela_conexão(4, heap_VALOR[objeto_Referência + 2], 0, 0, 0, 0); heap_VALOR[objeto_Referência + 9] = 0; } return; }
        if (Word_SMS(nome_constante, "repaint") || Word_SMS(nome_constante, "validate")) { int objeto_Referência = 빼기(2); if (!tela_objeto(objeto_Referência) || !Word_SMS(descritor_constante, "()V")) return; espaço_do_utilizador.tela_conexão(1, heap_VALOR[objeto_Referência + 2], heap_VALOR[objeto_Referência + 5], heap_VALOR[objeto_Referência + 6], heap_VALOR[objeto_Referência + 7], heap_VALOR[objeto_Referência + 8]); return; }
        if (Word_SMS(nome_constante, "isVisible") && Word_SMS(descritor_constante, "()Z")) { int objeto_Referência = 빼기(2); if (tela_objeto(objeto_Referência)) 넣기(heap_VALOR[objeto_Referência + 9], 1); return; }
        falha_VALOR("unsupported Swing method (native subset)");
    }
    static void expedir_Evento(int alvo_email, int Evento_número, boolean Português) {
        if (alvo_email < 1 || heap_VALOR[alvo_email] < 32) { falha_VALOR("Java event listener required"); return; }
        int Arquivo_ÍNDICE = nome_método(heap_VALOR[alvo_email] - 32, Evento_número == 0 ? (Português ? "Executar" : "run") : (Português ? "receber_Ação" : "actionPerformed"), Evento_número == 0 ? "()V" : (Português ? "(LPortuguês/nativo/Ação_aviso;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Arquivo_ÍNDICE < 0) { falha_VALOR("event callback missing"); return; }
        em_dia_thread = 0; contagem_de_threads = 1; quadro_ÍNDICE = 0; thread_Estado[0] = 1; quadro_pilha[0] = 0; quadro_bloquear[0] = inicializar_quadro[0] = 0; solicitação_de_alteração = false;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 128; Loop_ÍNDICE++) { local_VALOR[Loop_ÍNDICE] = local_TIPO[Loop_ÍNDICE] = 0; }
        quadro_método[0] = Arquivo_ÍNDICE; quadro_cargo[0] = método_START[Arquivo_ÍNDICE]; local_VALOR[0] = alvo_email; local_TIPO[0] = 2;
        if (Evento_número != 0) { local_VALOR[1] = Evento_número; local_TIPO[1] = 2; }
        사건중 = true; Executar_comando(); 사건중 = false;
    }
    static void tela_Eventos() {
        while (!erro) {
            if (나중수 > 0) { int alvo_email = 나중실행[0], Português = 나중한국어[0]; for (int Loop_ÍNDICE = 1; Loop_ÍNDICE < 나중수; Loop_ÍNDICE++) { 나중실행[Loop_ÍNDICE - 1] = 나중실행[Loop_ÍNDICE]; 나중한국어[Loop_ÍNDICE - 1] = 나중한국어[Loop_ÍNDICE]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; expedir_Evento(alvo_email, 0, Português != 0); continue; }
            if (espaço_do_utilizador.tela_conexão(6, 0, 0, 0, 0, 0) == 0) return;
            int Evento_número = espaço_do_utilizador.tela_conexão(5, 0, 0, 0, 0, 0); if (Evento_número == 0) continue;
            if (Evento_número < 0) { falha_VALOR("GUI event I/O failed"); return; }
            int conta_VALOR = Evento_número & 65535; if (conta_VALOR < 1 || conta_VALOR > 32) continue; int objeto_Referência = tela_Referência[conta_VALOR - 1]; if (objeto_Referência == 0) continue;
            if ((Evento_número & 65536) != 0) {
                if (heap_VALOR[objeto_Referência + 10] != 0) heap_VALOR[objeto_Referência + 9] = 0;
                if (heap_VALOR[objeto_Referência + 10] == 3) for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 32; Loop_ÍNDICE++) if (tela_Referência[Loop_ÍNDICE] != 0 && heap_VALOR[tela_Referência[Loop_ÍNDICE]] == 24) espaço_do_utilizador.tela_conexão(4, Loop_ÍNDICE + 1, 0, 0, 0, 0);
            } else if (heap_VALOR[objeto_Referência + 4] != 0) {
                int LEIAME_Referência = alocar_Armazenamento(29, 2); if (erro) return; heap_VALOR[LEIAME_Referência + 2] = objeto_Referência; heap_VALOR[LEIAME_Referência + 3] = heap_VALOR[objeto_Referência + 12]; heap_Referência[LEIAME_Referência + 2] = 1; expedir_Evento(heap_VALOR[objeto_Referência + 4], LEIAME_Referência, heap_VALOR[objeto_Referência + 12] != 0);
            }
        }
    }
    public static int iniciar() {
        if (espaço_do_utilizador.인수개수() == 1 && FerramentasJava.같음(espaço_do_utilizador.argumentos(0), "-version")) {
            espaço_do_utilizador.Escrita("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (espaço_do_utilizador.인수개수() < 1) { espaço_do_utilizador.Escrita("Usage: java CLASS [ARGS]\n"); return 2; }
        entrada_aula_Definição = carga_aula_Definição(host_caractere(espaço_do_utilizador.argumentos(0))); if (erro || entrada_aula_Definição < 0) return 1;
        int ponto_de_entrada_VALOR = nome_método(entrada_aula_Definição, "iniciar", "()V");
        boolean 한국어진입 = ponto_de_entrada_VALOR >= 0 && (método_acesso[ponto_de_entrada_VALOR] & 9) == 9;
        if (!한국어진입) ponto_de_entrada_VALOR = nome_método(entrada_aula_Definição, "main", "([Ljava/lang/String;)V");
        if (ponto_de_entrada_VALOR < 0 || (método_acesso[ponto_de_entrada_VALOR] & 9) != 9) falha_VALOR("public static void iniciar() or main(String[] args) required");
        if (erro) return 1;
        int argumentos = alocar_Armazenamento(3, espaço_do_utilizador.인수개수() - 1); elemento_da_matriz[argumentos] = -1;
        for (int número = 1; número < espaço_do_utilizador.인수개수() && !erro; número++) heap_VALOR[argumentos + 1 + número] = host_caractere(espaço_do_utilizador.argumentos(número));
        quadro_ÍNDICE = 0; quadro_método[0] = ponto_de_entrada_VALOR; quadro_cargo[0] = método_START[ponto_de_entrada_VALOR]; local_VALOR[0] = 한국어진입 ? 0 : argumentos; local_TIPO[0] = 한국어진입 ? 0 : 2;
        thread_Estado[0] = 1; thread_objeto[0] = alocar_Armazenamento(13, 2);
        Executar_comando(); if (!erro) tela_Eventos(); return erro ? 1 : 0;
    }
}
