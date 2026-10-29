// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. ficheiro/operando_pilha/Referência/branch 경계를 Executar_comando 중 검사한다. */
public final class 자바가상기계 {
    static int[] ficheiro = new int[16384], nome_de_arquivo_SMS = new int[64];
    static int[] constante_tag = new int[512], 상가 = new int[512], constante_SEGUNDO_VALOR = new int[512], cadeia_Referência = new int[512];
    static int[] método_nome_SMS = new int[32], método_TIPO = new int[32], método_acesso = new int[32];
    static int[] método_START = new int[32], método_encerrar = new int[32], método_pilha = new int[32], 함수지역 = new int[32];
    static int[] método_argumento_CONT_NÚM = new int[32], método_argumento_TIPO = new int[512], método_devolver = new int[32];
    static int[] limite_VALOR = new int[16384];
    static int[] local_VALOR = new int[4096], local_TIPO = new int[4096], operando_pilha_VALOR = new int[4096], operando_pilha_TIPO = new int[4096];
    static int[] quadro_método = new int[32], quadro_cargo = new int[32], quadro_pilha = new int[32];
    static int[] heap_VALOR = new int[8192];
    static int Tamanho, leitura_cargo, constante_CONT_NÚM, método_CONT_NÚM, nome_da_classe, quadro_ÍNDICE = -1, heap_encerrar_cargo = 1, tipo_de_retorno;
    static boolean erro;

    static void falha_VALOR(String Word_SMS) {
        if (!erro) { espaço_do_utilizador.Escrita("JVM error: "); espaço_do_utilizador.Escrita(Word_SMS); espaço_do_utilizador.gravar_caractere_VALOR(10); }
        erro = true;
    }
    static boolean recortar(int iniciar, int duração_VALOR) { return iniciar >= 0 && duração_VALOR >= 0 && iniciar <= Tamanho - duração_VALOR; }
    static int byte_VALOR() {
        if (!recortar(leitura_cargo, 1)) { falha_VALOR("truncated class file"); return 0; }
        return ficheiro[leitura_cargo++];
    }
    static int 짧은수() { return byte_VALOR() << 8 | byte_VALOR(); }
    static int inteiro() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int duração_VALOR) { if (!recortar(leitura_cargo, duração_VALOR)) falha_VALOR("invalid attribute size"); else leitura_cargo += duração_VALOR; }
    static boolean cheque_constante(int número, int Tipo_VALOR) {
        if (número <= 0 || número >= constante_CONT_NÚM || constante_tag[número] != Tipo_VALOR) { falha_VALOR("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_alcance(int iniciar, int duração_VALOR, String Word_SMS) {
        if (!recortar(iniciar, duração_VALOR) || duração_VALOR != Word_SMS.length()) return false;
        for (int número = 0; número < duração_VALOR; número++) if (ficheiro[iniciar + número] != Word_SMS.charAt(número)) return false;
        return true;
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
    static void ignorar_atributo() {
        int item_CONT_NÚM = 짧은수();
        for (int número = 0; número < item_CONT_NÚM && !erro; número++) { cheque_constante(짧은수(), 1); 건너(inteiro()); }
    }
    static int comando_duração(int VALOR) {
        if (VALOR == 16 || VALOR == 18 || VALOR == 21 || VALOR == 25 || VALOR == 54 || VALOR == 58 || VALOR == 188) return 2;
        if (VALOR == 17 || VALOR == 19 || VALOR == 132 || VALOR >= 153 && VALOR <= 167
            || VALOR >= 178 && VALOR <= 184 || VALOR == 187 || VALOR == 189 || VALOR == 192 || VALOR == 198 || VALOR == 199) return 3;
        if (VALOR >= 0 && VALOR <= 8 || VALOR >= 26 && VALOR <= 29 || VALOR >= 42 && VALOR <= 46 || VALOR == 50
            || VALOR >= 59 && VALOR <= 62 || VALOR >= 75 && VALOR <= 79 || VALOR == 83 || VALOR == 87 || VALOR == 89 || VALOR == 95
            || VALOR == 96 || VALOR == 100 || VALOR == 104 || VALOR == 108 || VALOR == 112 || VALOR == 116
            || VALOR == 120 || VALOR == 122 || VALOR == 124 || VALOR == 126 || VALOR == 128 || VALOR == 130
            || VALOR >= 145 && VALOR <= 147 || VALOR == 172 || VALOR == 176 || VALOR == 177 || VALOR == 190) return 1;
        return 0;
    }
    static void leitura_aula() {
        if (inteiro() != 0xcafebabe) falha_VALOR("not a class file");
        int 부판 = 짧은수(), versão_VALOR = 짧은수();
        if (versão_VALOR < 45 || versão_VALOR > 52 || 부판 != 0) falha_VALOR("supported class versions: 45..52, minor 0");
        constante_CONT_NÚM = 짧은수();
        if (constante_CONT_NÚM < 1 || constante_CONT_NÚM > 512) { falha_VALOR("constant pool limit (511)"); return; }
        for (int número = 1; número < constante_CONT_NÚM && !erro; número++) {
            int Tipo_VALOR = byte_VALOR(); constante_tag[número] = Tipo_VALOR;
            if (Tipo_VALOR == 1) { constante_SEGUNDO_VALOR[número] = 짧은수(); 상가[número] = leitura_cargo; 건너(constante_SEGUNDO_VALOR[número]); }
            else if (Tipo_VALOR == 3) 상가[número] = inteiro();
            else if (Tipo_VALOR == 7 || Tipo_VALOR == 8) 상가[número] = 짧은수();
            else if (Tipo_VALOR == 9 || Tipo_VALOR == 10 || Tipo_VALOR == 12) { 상가[número] = 짧은수(); constante_SEGUNDO_VALOR[número] = 짧은수(); }
            else falha_VALOR("unsupported constant type");
        }
        int Permissão_VALOR = 짧은수();
        if ((Permissão_VALOR & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) falha_VALOR("unsupported class flags");
        nome_da_classe = nome_da_classe_SMS(짧은수());
        if (!Word_SMS(nome_da_classe_SMS(짧은수()), "java/lang/Object")) falha_VALOR("inheritance unsupported");
        if (짧은수() != 0) falha_VALOR("interfaces unsupported");
        if (짧은수() != 0) falha_VALOR("fields unsupported");
        método_CONT_NÚM = 짧은수();
        if (método_CONT_NÚM < 1 || método_CONT_NÚM > 32) { falha_VALOR("method count limit (32)"); return; }
        for (int número = 0; número < método_CONT_NÚM && !erro; número++) {
            método_acesso[número] = 짧은수(); método_nome_SMS[número] = 짧은수(); método_TIPO[número] = 짧은수();
            cheque_constante(método_nome_SMS[número], 1); leitura_descritor(número);
            if ((método_acesso[número] & (0x100 | 0x400 | 0x20)) != 0) falha_VALOR("native, abstract and synchronized methods unsupported");
            if ((método_acesso[número] & 8) == 0 && !Word_SMS(método_nome_SMS[número], "<init>")) falha_VALOR("instance methods unsupported");
            if (Word_SMS(método_nome_SMS[número], "<clinit>")) falha_VALOR("class initializers unsupported");
            for (int câmera_frontal_VALOR = 0; câmera_frontal_VALOR < número; câmera_frontal_VALOR++) if (같은말(método_nome_SMS[câmera_frontal_VALOR], método_nome_SMS[número]) && 같은말(método_TIPO[câmera_frontal_VALOR], método_TIPO[número])) falha_VALOR("duplicate method");
            int item_CONT_NÚM = 짧은수();
            for (int valor_do_atributo = 0; valor_do_atributo < item_CONT_NÚM && !erro; valor_do_atributo++) {
                int Nome = 짧은수(), duração_VALOR = inteiro(), iniciar = leitura_cargo;
                if (!recortar(iniciar, duração_VALOR)) { falha_VALOR("truncated method attribute"); break; }
                if (Word_SMS(Nome, "Code")) {
                    if (método_START[número] != 0) falha_VALOR("duplicate Code attribute");
                    método_pilha[número] = 짧은수(); 함수지역[número] = 짧은수(); int CÓDIGO_duração = inteiro();
                    if (método_pilha[número] > 128 || 함수지역[número] > 128 || 함수지역[número] < método_argumento_CONT_NÚM[número]
                        || CÓDIGO_duração < 1 || CÓDIGO_duração > 8192) falha_VALOR("method memory limits exceeded");
                    método_START[número] = leitura_cargo; 건너(CÓDIGO_duração); método_encerrar[número] = leitura_cargo;
                    if (짧은수() != 0) falha_VALOR("exception handlers unsupported");
                    ignorar_atributo();
                    if (leitura_cargo != iniciar + duração_VALOR) falha_VALOR("Code attribute size mismatch");
                } else 건너(duração_VALOR);
            }
            if (método_START[número] == 0) falha_VALOR("missing Code attribute");
            int slot_entrada = método_START[número];
            while (slot_entrada < método_encerrar[número] && !erro) {
                int duração_VALOR = comando_duração(ficheiro[slot_entrada]);
                if (duração_VALOR == 0 || duração_VALOR > método_encerrar[número] - slot_entrada) { falha_VALOR("unsupported or truncated bytecode"); break; }
                limite_VALOR[slot_entrada] = número + 1; slot_entrada += duração_VALOR;
            }
            // 실행하지 않는 경로에도 잘못된 branch 목적지를 허용하지 않는다.
            slot_entrada = método_START[número];
            while (slot_entrada < método_encerrar[número] && !erro) {
                int VALOR = ficheiro[slot_entrada];
                if (VALOR >= 153 && VALOR <= 167 || VALOR == 198 || VALOR == 199) {
                    int destino_VALOR = slot_entrada + (short)(ficheiro[slot_entrada + 1] << 8 | ficheiro[slot_entrada + 2]);
                    if (destino_VALOR < método_START[número] || destino_VALOR >= método_encerrar[número] || limite_VALOR[destino_VALOR] != número + 1) falha_VALOR("invalid branch target");
                }
                slot_entrada += comando_duração(VALOR);
            }
        }
        if (!erro) ignorar_atributo();
        if (leitura_cargo != Tamanho) falha_VALOR("extra class file data");
    }
    static int alocar_Armazenamento(int Tipo_VALOR, int duração_VALOR) {
        if (duração_VALOR < 0 || duração_VALOR > heap_VALOR.length - heap_encerrar_cargo - 2) { falha_VALOR("object heap exhausted or negative array size"); return 0; }
        int Referência = heap_encerrar_cargo; heap_encerrar_cargo += duração_VALOR + 2; heap_VALOR[Referência] = Tipo_VALOR; heap_VALOR[Referência + 1] = duração_VALOR;
        return Referência;
    }
    static boolean objeto_VALOR(int Referência, int Tipo_VALOR) {
        if (Referência < 1 || Referência >= heap_encerrar_cargo - 1 || heap_VALOR[Referência] != Tipo_VALOR) { falha_VALOR("null or invalid object reference"); return false; }
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
        if (quadro_ÍNDICE == 31) { falha_VALOR("call stack limit (32)"); return; }
        int Avançar_item = quadro_ÍNDICE + 1;
        for (int número = 0; número < 128; número++) local_TIPO[Avançar_item * 128 + número] = 0;
        for (int número = método_argumento_CONT_NÚM[FUNÇÃO_VALOR] - 1; número >= 0; número--) {
            local_VALOR[Avançar_item * 128 + número] = 빼기(método_argumento_TIPO[FUNÇÃO_VALOR * 16 + número]); local_TIPO[Avançar_item * 128 + número] = método_argumento_TIPO[FUNÇÃO_VALOR * 16 + número];
        }
        quadro_ÍNDICE = Avançar_item; quadro_método[quadro_ÍNDICE] = FUNÇÃO_VALOR; quadro_cargo[quadro_ÍNDICE] = método_START[FUNÇÃO_VALOR]; quadro_pilha[quadro_ÍNDICE] = 0;
    }
    static void devolver_RC(int TIPO_VALOR) {
        if (TIPO_VALOR != método_devolver[quadro_método[quadro_ÍNDICE]]) { falha_VALOR("return type mismatch"); return; }
        int VALOR = TIPO_VALOR == 0 ? 0 : 빼기(TIPO_VALOR);
        quadro_ÍNDICE--; if (quadro_ÍNDICE >= 0 && TIPO_VALOR != 0) 넣기(VALOR, TIPO_VALOR);
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
                if (VALOR < 1 || VALOR > 127) { falha_VALOR("file stream paths currently require ASCII"); return; }
                fluxo_nome_de_arquivo[slot_entrada] = VALOR;
            }
            fluxo_nome_de_arquivo[duração_VALOR] = 0;
            int descritor_entrada = espaço_do_utilizador.abrir_Arquivo_descritor(fluxo_nome_de_arquivo, saídaTexto ? (이어 ? 1089 : 577) : 0);
            if (descritor_entrada < 0) { falha_VALOR("FileNotFoundException: file open failed"); return; }
            heap_VALOR[fluxo_VALOR + 2] = descritor_entrada; heap_VALOR[fluxo_VALOR + 3] = 1;
            return;
        }
        if (comando != 182) { falha_VALOR("invalid file stream invocation"); return; }
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
            if (resultado < -1) falha_VALOR("IOException: read failed"); else 넣기(resultado, 1);
        } else if (espaço_do_utilizador.파일한바이트쓰기(descritor_entrada, VALOR) != 1) falha_VALOR("IOException: write failed");
    }
    static void Ligar_método(int ÍNDICE, int comando) {
        if (!cheque_constante(ÍNDICE, 10)) return;
        int proprietário_VALOR = nome_da_classe_SMS(상가[ÍNDICE]), Nome = Referência_nome(constante_SEGUNDO_VALOR[ÍNDICE]), formato_VALOR = tipo_de_referência(constante_SEGUNDO_VALOR[ÍNDICE]);
        if (erro) return;
        if (같은말(proprietário_VALOR, nome_da_classe)) {
            if (comando != 184) { falha_VALOR("only static user methods are supported"); return; }
            for (int número = 0; número < método_CONT_NÚM; número++) if (같은말(Nome, método_nome_SMS[número]) && 같은말(formato_VALOR, método_TIPO[número])) {
                if ((método_acesso[número] & 8) == 0) falha_VALOR("method is not static"); else 호출(número);
                return;
            }
            falha_VALOR("NoSuchMethodError"); return;
        }
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
        falha_VALOR("unsupported library method");
    }
    static int MATRIZ_slot(int Referência, int subscrito_VALOR, int TIPO_VALOR) {
        if (!objeto_VALOR(Referência, TIPO_VALOR)) return 0;
        if (subscrito_VALOR < 0 || subscrito_VALOR >= heap_VALOR[Referência + 1]) { falha_VALOR("ArrayIndexOutOfBoundsException"); return 0; }
        return Referência + 2 + subscrito_VALOR;
    }
    static void Executar_comando() {
        int 남음 = 500000;
        while (quadro_ÍNDICE >= 0 && !erro) {
            if (--남음 == 0) { falha_VALOR("instruction limit (500000)"); break; }
            int iniciar = quadro_cargo[quadro_ÍNDICE], VALOR = leitura_opcode_byte();
            if (erro) break;
            if (VALOR == 0) continue;
            if (VALOR == 1) { 넣기(0, 2); continue; }
            if (VALOR >= 2 && VALOR <= 8) { 넣기(VALOR - 3, 1); continue; }
            if (VALOR == 16) { 넣기((byte)leitura_opcode_byte(), 1); continue; }
            if (VALOR == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALOR == 18 || VALOR == 19) {
                int número = VALOR == 18 ? leitura_opcode_byte() : 명짧();
                if (número <= 0 || número >= constante_CONT_NÚM) falha_VALOR("invalid ldc constant");
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
            if (VALOR == 46 || VALOR == 50) {
                int subscrito_VALOR = 빼기(1), Referência = 빼기(2), slot_entrada = MATRIZ_slot(Referência, subscrito_VALOR, VALOR == 46 ? 2 : 3);
                if (!erro) 넣기(heap_VALOR[slot_entrada], VALOR == 46 ? 1 : 2); continue;
            }
            if (VALOR == 79 || VALOR == 83) {
                int item_elemento = 빼기(VALOR == 79 ? 1 : 2), subscrito_VALOR = 빼기(1), Referência = 빼기(2), slot_entrada = MATRIZ_slot(Referência, subscrito_VALOR, VALOR == 79 ? 2 : 3);
                if (VALOR == 83 && item_elemento != 0) objeto_VALOR(item_elemento, 1);
                if (!erro) heap_VALOR[slot_entrada] = item_elemento; continue;
            }
            if (VALOR == 87) { 빼기(0); continue; }
            if (VALOR == 89) { int 가 = 빼기(0), TIPO_VALOR = tipo_de_retorno; 넣기(가, TIPO_VALOR); 넣기(가, TIPO_VALOR); continue; }
            if (VALOR == 95) { int 가 = 빼기(0), 가형 = tipo_de_retorno, SEGUNDO_operando = 빼기(0), SEGUNDO_operando_TIPO = tipo_de_retorno; 넣기(가, 가형); 넣기(SEGUNDO_operando, SEGUNDO_operando_TIPO); continue; }
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
            if (VALOR == 178) {
                int número = 명짧(); if (!cheque_constante(número, 9)) continue;
                if (!Word_SMS(nome_da_classe_SMS(상가[número]), "java/lang/System") || !Word_SMS(Referência_nome(constante_SEGUNDO_VALOR[número]), "out")
                    || !Word_SMS(tipo_de_referência(constante_SEGUNDO_VALOR[número]), "Ljava/io/PrintStream;")) falha_VALOR("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALOR == 182 || VALOR == 183 || VALOR == 184) { Ligar_método(명짧(), VALOR); continue; }
            if (VALOR == 187) {
                int Nome = nome_da_classe_SMS(명짧());
                if (Word_SMS(Nome, "java/lang/StringBuilder")) 넣기(alocar_Armazenamento(4, 1), 2);
                else if (Word_SMS(Nome, "java/io/FileInputStream") || Word_SMS(Nome, "java/io/FileOutputStream")) {
                    int Referência = alocar_Armazenamento(Word_SMS(Nome, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!erro) { heap_VALOR[Referência + 2] = -1; 넣기(Referência, 2); }
                } else falha_VALOR("unsupported object construction");
                continue;
            }
            if (VALOR == 188 || VALOR == 189) {
                if (VALOR == 188) { if (leitura_opcode_byte() != 10) falha_VALOR("only int[] newarray is supported"); }
                else if (!Word_SMS(nome_da_classe_SMS(명짧()), "java/lang/String")) falha_VALOR("only String[] anewarray is supported");
                int duração_VALOR = 빼기(1); 넣기(alocar_Armazenamento(VALOR == 188 ? 2 : 3, duração_VALOR), 2); continue;
            }
            if (VALOR == 190) {
                int Referência = 빼기(2);
                if (Referência < 1 || Referência >= heap_encerrar_cargo - 1 || (heap_VALOR[Referência] != 2 && heap_VALOR[Referência] != 3)) falha_VALOR("null or invalid array");
                else 넣기(heap_VALOR[Referência + 1], 1); continue;
            }
            if (VALOR == 192) {
                int Nome = nome_da_classe_SMS(명짧()), Referência = 빼기(2);
                if (!Word_SMS(Nome, "java/lang/String")) falha_VALOR("unsupported checkcast");
                else if (Referência != 0) objeto_VALOR(Referência, 1);
                넣기(Referência, 2); continue;
            }
            falha_VALOR("unsupported bytecode");
        }
    }
    public static int iniciar() {
        if (espaço_do_utilizador.인수개수() == 1 && FerramentasJava.같음(espaço_do_utilizador.argumentos(0), "-version")) {
            espaço_do_utilizador.Escrita("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (espaço_do_utilizador.인수개수() < 1) { espaço_do_utilizador.Escrita("Usage: java CLASS [ARGS]\n"); return 2; }
        int duração_VALOR = FerramentasJava.Nome(nome_de_arquivo_SMS, espaço_do_utilizador.argumentos(0));
        if (duração_VALOR < 1 || duração_VALOR > 57) { espaço_do_utilizador.Escrita("java: invalid class name\n"); return 2; }
        nome_de_arquivo_SMS[duração_VALOR] = '.'; nome_de_arquivo_SMS[duração_VALOR + 1] = 'c'; nome_de_arquivo_SMS[duração_VALOR + 2] = 'l'; nome_de_arquivo_SMS[duração_VALOR + 3] = 'a'; nome_de_arquivo_SMS[duração_VALOR + 4] = 's'; nome_de_arquivo_SMS[duração_VALOR + 5] = 's';
        Tamanho = espaço_do_utilizador.leitura_Arquivo(nome_de_arquivo_SMS, ficheiro);
        if (Tamanho < 0) { espaço_do_utilizador.Escrita("java: cannot read class: "); FerramentasJava.gravar_número(Tamanho); espaço_do_utilizador.gravar_caractere_VALOR(10); return 1; }
        leitura_aula(); if (erro) return 1;
        int caractere_nome = constante_SMS(nome_da_classe);
        if (!erro && heap_VALOR[caractere_nome + 1] != duração_VALOR) falha_VALOR("class name does not match file");
        for (int número = 0; número < duração_VALOR && !erro; número++) if (heap_VALOR[caractere_nome + 2 + número] != nome_de_arquivo_SMS[número]) falha_VALOR("class name does not match file");
        int ponto_de_entrada_VALOR = -1;
        for (int número = 0; número < método_CONT_NÚM; número++) if (Word_SMS(método_nome_SMS[número], "main") && Word_SMS(método_TIPO[número], "([Ljava/lang/String;)V") && (método_acesso[número] & 9) == 9) ponto_de_entrada_VALOR = número;
        if (ponto_de_entrada_VALOR < 0) falha_VALOR("public static void main(String[] args) required");
        if (erro) return 1;
        int argumentos = alocar_Armazenamento(3, espaço_do_utilizador.인수개수() - 1);
        for (int número = 1; número < espaço_do_utilizador.인수개수() && !erro; número++) heap_VALOR[argumentos + 1 + número] = host_caractere(espaço_do_utilizador.argumentos(número));
        quadro_ÍNDICE = 0; quadro_método[0] = ponto_de_entrada_VALOR; quadro_cargo[0] = método_START[ponto_de_entrada_VALOR]; local_VALOR[0] = argumentos; local_TIPO[0] = 2;
        Executar_comando(); return erro ? 1 : 0;
    }
}
