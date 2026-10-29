// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VALOR 경계를 지키는 삽입/삭제, 방향키, comando LOG_linha, Tab concluído_VALOR. */
public final class editor_de_linha {
    static boolean linha_de_comando;
    static int[] LOG_linha = new int[16 * 1024], LOG_duração = new int[16], Store_VALOR = new int[4096], candidato = new int[64];
    static int LOG_CONT_NÚM, LOG_linha_encerrar, busca_VALOR, 저장길이, Tamanho, cursor_VALOR, candidato_CONT_NÚM, candidato_duração, START_janela;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd SSH remoto_visor run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] comando_candidato = new int[128];
    static void Adicionar_comando_candidato(String entrada_Lista_f07b3200, int START_cargo, int encerrar_cargo, int entrada_duração) {
        int byte_CONT_NÚM=0;
        for(int cargo_ÍNDICE=START_cargo;cargo_ÍNDICE<encerrar_cargo;cargo_ÍNDICE++) {
            int ponto_de_código=entrada_Lista_f07b3200.charAt(cargo_ÍNDICE);
            if(ponto_de_código>=0xd800 && ponto_de_código<=0xdbff && cargo_ÍNDICE+1<encerrar_cargo)ponto_de_código=0x10000+((ponto_de_código-0xd800)<<10)+entrada_Lista_f07b3200.charAt(++cargo_ÍNDICE)-0xdc00;
            int número=ponto_de_código<128?1:ponto_de_código<2048?2:ponto_de_código<65536?3:4;
            if(byte_CONT_NÚM+número>62)return;
            for(int SEQUÊNCIA_VALOR=número-1;SEQUÊNCIA_VALOR>=0;SEQUÊNCIA_VALOR--)comando_candidato[byte_CONT_NÚM++]=número==1?ponto_de_código:SEQUÊNCIA_VALOR==número-1?(número==2?0xc0:número==3?0xe0:0xf0)|(ponto_de_código>>(6*SEQUÊNCIA_VALOR)):0x80|((ponto_de_código>>(6*SEQUÊNCIA_VALOR))&63);
        }
        if(byte_CONT_NÚM<entrada_duração)return;
        for(int cargo_ÍNDICE=0;cargo_ÍNDICE<entrada_duração;cargo_ÍNDICE++)if(comando_candidato[cargo_ÍNDICE]!=InterpretadorComandos.linha_de_entrada[cargo_ÍNDICE])return;
        candidato_CONT_NÚM++;candidato_duração=byte_CONT_NÚM+1;
        for(int cargo_ÍNDICE=0;cargo_ÍNDICE<byte_CONT_NÚM;cargo_ÍNDICE++)candidato[cargo_ÍNDICE]=comando_candidato[cargo_ÍNDICE];candidato[byte_CONT_NÚM]=' ';
    }
    static int câmera_frontal_VALOR(int leitura_cursor) { if (leitura_cursor > 0) { leitura_cursor--; while (leitura_cursor > 0 && (InterpretadorComandos.linha_de_entrada[leitura_cursor] & 192) == 128) leitura_cursor--; } return leitura_cursor; }
    static int BACK_VALOR(int leitura_cursor) { if (leitura_cursor < Tamanho) { leitura_cursor++; while (leitura_cursor < Tamanho && (InterpretadorComandos.linha_de_entrada[leitura_cursor] & 192) == 128) leitura_cursor++; } return leitura_cursor; }
    static int 폭(int START_cargo, int destino_VALOR_ÍNDICE) {
        int 글칸수 = 0;
        for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < destino_VALOR_ÍNDICE; Loop_ÍNDICE++) { int byte_dados = InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE]; if ((byte_dados & 192) == 128) continue; 글칸수 += byte_dados >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void repetir_VALOR() {
        단말.Escrita("\r\u001b[2K");
        단말.Escrita(linha_de_comando ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 linha_de_entrada 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLS = Quadro.terminal(13) & 65535; return COLS - (linha_de_comando ? 18 : 9); }
    static void 보이는줄() {
        if (cursor_VALOR < START_janela) START_janela = cursor_VALOR;
        while (폭(START_janela, cursor_VALOR) > 보이는폭()) START_janela = BACK_VALOR(START_janela);
        int encerrar_cargo = START_janela;
        while (encerrar_cargo < Tamanho && 폭(START_janela, BACK_VALOR(encerrar_cargo)) <= 보이는폭()) encerrar_cargo = BACK_VALOR(encerrar_cargo);
        단말.Escrita("\r\u001b["); 단말.número(linha_de_comando ? 16 : 7); 단말.Escrita("G\u001b[K");
        if (START_janela > 0) 단말.문자('<');
        for (int Loop_ÍNDICE = START_janela; Loop_ÍNDICE < encerrar_cargo; Loop_ÍNDICE++) Quadro.직렬쓰기(InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE]);
        단말.문자(encerrar_cargo < Tamanho ? '>' : ' ');
        단말.Escrita("\u001b["); 단말.número(폭(cursor_VALOR, encerrar_cargo) + 1); 단말.문자('D');
        가로보기 = START_janela > 0 || encerrar_cargo < Tamanho || 폭(0, Tamanho) > 보이는폭();
    }
    static void Acrescentar_LOG() {
        if (!linha_de_comando || Tamanho == 0 || Tamanho > 1024) return;
        if (LOG_CONT_NÚM > 0) {
            int 마지막자리 = (LOG_linha_encerrar + 15) % 16; boolean 같은여부 = LOG_duração[마지막자리] == Tamanho;
            for (int Loop_ÍNDICE = 0; 같은여부 && Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) if (LOG_linha[마지막자리 * 1024 + Loop_ÍNDICE] != InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_duração[LOG_linha_encerrar] = Tamanho; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) LOG_linha[LOG_linha_encerrar * 1024 + Loop_ÍNDICE] = InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE];
        LOG_linha_encerrar = (LOG_linha_encerrar + 1) % 16; if (LOG_CONT_NÚM < 16) LOG_CONT_NÚM++;
    }
    static void 기록이동(int DELTA_VALOR) {
        if (!linha_de_comando) return;
        if (busca_VALOR == 0 && DELTA_VALOR > 0) { 저장길이 = Tamanho; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) Store_VALOR[Loop_ÍNDICE] = InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE]; }
        int Avançar_cargo = busca_VALOR + DELTA_VALOR; if (Avançar_cargo < 0 || Avançar_cargo > LOG_CONT_NÚM) return; busca_VALOR = Avançar_cargo;
        if (busca_VALOR == 0) { Tamanho = 저장길이; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE] = Store_VALOR[Loop_ÍNDICE]; }
        else { int 보관칸 = (LOG_linha_encerrar + 16 - busca_VALOR) % 16; Tamanho = LOG_duração[보관칸]; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE] = LOG_linha[보관칸 * 1024 + Loop_ÍNDICE]; }
        cursor_VALOR = Tamanho; repetir_VALOR();
    }
    static void mostrar_LOG() {
        for (int entrada_CONT_NÚM_8f7753a1 = 0; entrada_CONT_NÚM_8f7753a1 < LOG_CONT_NÚM; entrada_CONT_NÚM_8f7753a1++) {
            int 보관칸 = (LOG_linha_encerrar + 16 - LOG_CONT_NÚM + entrada_CONT_NÚM_8f7753a1) % 16; 단말.número(entrada_CONT_NÚM_8f7753a1 + 1); 단말.Escrita("  ");
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < LOG_duração[보관칸]; Loop_ÍNDICE++) Quadro.직렬쓰기(LOG_linha[보관칸 * 1024 + Loop_ÍNDICE]); 단말.문자(10);
        }
    }
    static void Adicionar_candidato(int[] dados_MATRIZ, int START_cargo, int entrada_CONT_NÚM_8f7753a1, int 접두말, int total_CONT_NÚM, boolean Diretório_número) {
        if (entrada_CONT_NÚM_8f7753a1 < total_CONT_NÚM || entrada_CONT_NÚM_8f7753a1 > 62) return;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < total_CONT_NÚM; Loop_ÍNDICE++) if (dados_MATRIZ[START_cargo + Loop_ÍNDICE] != InterpretadorComandos.linha_de_entrada[접두말 + Loop_ÍNDICE]) return;
        candidato_CONT_NÚM++; candidato_duração = entrada_CONT_NÚM_8f7753a1 + 1;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) candidato[Loop_ÍNDICE] = dados_MATRIZ[START_cargo + Loop_ÍNDICE]; candidato[entrada_CONT_NÚM_8f7753a1] = Diretório_número ? '/' : ' ';
    }
    static void concluído_VALOR() {
        if (!linha_de_comando || cursor_VALOR != Tamanho) return;
        int 시작점 = Tamanho; while (시작점 > 0 && InterpretadorComandos.linha_de_entrada[시작점 - 1] != ' ') 시작점--;
        for (int Loop_ÍNDICE = 시작점; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) if (InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE] == '/' || InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE] == '"' || InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE] == 39 || InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE] == '\\') return;
        candidato_CONT_NÚM = 0; int entrada_CONT_NÚM_8f7753a1 = Tamanho - 시작점;
        if (시작점 == 0) {
            for(int índice_de_lista=0;índice_de_lista<2;índice_de_lista++) {
                String entrada_Lista_f07b3200=índice_de_lista==0?명령들:관리명령.concluído_Word();
                int leitura_cursor=0;
                while(leitura_cursor<entrada_Lista_f07b3200.length()) {
                    int encerrar_cargo=leitura_cursor;while(encerrar_cargo<entrada_Lista_f07b3200.length() && entrada_Lista_f07b3200.charAt(encerrar_cargo)!=' ')encerrar_cargo++;
                    Adicionar_comando_candidato(entrada_Lista_f07b3200,leitura_cursor,encerrar_cargo,entrada_CONT_NÚM_8f7753a1);leitura_cursor=encerrar_cargo+1;
                }
            }
        } else {
            FicheirosMemória.caminho_START(1); FicheirosMemória.caminho_byte(0, '.'); FicheirosMemória.normalizar_VALOR();
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < FicheirosMemória.Arquivo_CONT_NÚM; Loop_ÍNDICE++) {
                int START_cargo = FicheirosMemória.entrada_START(FicheirosMemória.Nome, Loop_ÍNDICE * 64, FicheirosMemória.이름길이[Loop_ÍNDICE]);
                if (START_cargo >= 0) Adicionar_candidato(FicheirosMemória.Nome, Loop_ÍNDICE * 64 + START_cargo, FicheirosMemória.이름길이[Loop_ÍNDICE] - START_cargo, 시작점, entrada_CONT_NÚM_8f7753a1, false);
            }
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) {
                int START_cargo = FicheirosMemória.entrada_START(FicheirosMemória.Diretório_nome, Loop_ÍNDICE * 64, FicheirosMemória.Diretório_duração[Loop_ÍNDICE]);
                if (START_cargo >= 0) Adicionar_candidato(FicheirosMemória.Diretório_nome, Loop_ÍNDICE * 64 + START_cargo, FicheirosMemória.Diretório_duração[Loop_ÍNDICE] - START_cargo, 시작점, entrada_CONT_NÚM_8f7753a1, true);
            }
        }
        if (candidato_CONT_NÚM != 1) { Quadro.직렬쓰기(7); return; }
        for (int Loop_ÍNDICE = entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE < candidato_duração && Tamanho < InterpretadorComandos.linha_de_entrada.length - 1; Loop_ÍNDICE++) {
            if (candidato[Loop_ÍNDICE] == ' ' && Loop_ÍNDICE != candidato_duração - 1) InterpretadorComandos.linha_de_entrada[Tamanho++] = '\\';
            InterpretadorComandos.linha_de_entrada[Tamanho++] = candidato[Loop_ÍNDICE];
        }
        cursor_VALOR = Tamanho; repetir_VALOR();
    }
    static int 탈출읽기() {
        int 시작점 = Quadro.밀리초();
        while (Quadro.밀리초() - 시작점 < 80) { int byte_dados = Quadro.직렬읽기(); if (byte_dados >= 0) return byte_dados; Quadro.LUCRO_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int entrada_CONT_NÚM_8f7753a1 = 0, encerrar_cargo = -1;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 12; Loop_ÍNDICE++) { int byte_dados = 탈출읽기(); if (byte_dados < 0) return; if (byte_dados >= '0' && byte_dados <= '9') entrada_CONT_NÚM_8f7753a1 = entrada_CONT_NÚM_8f7753a1 * 10 + byte_dados - '0'; else { encerrar_cargo = byte_dados; break; } }
        if (encerrar_cargo == 'A') 기록이동(1);
        else if (encerrar_cargo == 'B') 기록이동(-1);
        else if (encerrar_cargo == 'C') { cursor_VALOR = BACK_VALOR(cursor_VALOR); repetir_VALOR(); }
        else if (encerrar_cargo == 'D') { cursor_VALOR = câmera_frontal_VALOR(cursor_VALOR); repetir_VALOR(); }
        else if (encerrar_cargo == 'H' || encerrar_cargo == '~' && (entrada_CONT_NÚM_8f7753a1 == 1 || entrada_CONT_NÚM_8f7753a1 == 7)) { cursor_VALOR = 0; repetir_VALOR(); }
        else if (encerrar_cargo == 'F' || encerrar_cargo == '~' && (entrada_CONT_NÚM_8f7753a1 == 4 || entrada_CONT_NÚM_8f7753a1 == 8)) { cursor_VALOR = Tamanho; repetir_VALOR(); }
        else if (encerrar_cargo == '~' && entrada_CONT_NÚM_8f7753a1 == 3 && cursor_VALOR < Tamanho) {
            int Avançar_cargo = BACK_VALOR(cursor_VALOR); for (int Loop_ÍNDICE = Avançar_cargo; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE - Avançar_cargo + cursor_VALOR] = InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE]; Tamanho -= Avançar_cargo - cursor_VALOR; repetir_VALOR();
        }
        else if (encerrar_cargo == '~' && (entrada_CONT_NÚM_8f7753a1 == 5 || entrada_CONT_NÚM_8f7753a1 == 6)) Quadro.terminal(entrada_CONT_NÚM_8f7753a1 == 5 ? 5 : 6);
        else if (encerrar_cargo == '~' && entrada_CONT_NÚM_8f7753a1 == 24 && linha_de_comando) { InterpretadorComandos.terminal(true); }
    }
    static int Leitura() {
        if (!janela_sessão.이어읽기) { Tamanho = cursor_VALOR = busca_VALOR = START_janela = 0; 가로보기 = false; }
        else { janela_sessão.이어읽기 = false; repetir_VALOR(); } boolean estouro = false;
        while (true) {
            int byte_dados = Quadro.직렬읽기(); if (byte_dados == -4096) return -3;
            if (Quadro.terminal(14) != 0) repetir_VALOR(); if (byte_dados < 0) { Quadro.LUCRO_CPU(); continue; }
            if (byte_dados == 10 && InterpretadorComandos.Anterior_linha) { InterpretadorComandos.Anterior_linha = false; continue; } InterpretadorComandos.Anterior_linha = byte_dados == 13;
            if (byte_dados == 27) { 탈출(); continue; }
            if (byte_dados == 3) { 단말.Escrita("^C\n"); return -1; }
            if (byte_dados == 4 && Tamanho == 0 && linha_de_comando) { if (Quadro.terminal(2) != 0) InterpretadorComandos.terminal(true); return -1; }
            if (byte_dados == 13 || byte_dados == 10) { 단말.문자(10); if (!estouro) Acrescentar_LOG(); return estouro ? -2 : Tamanho; }
            if (byte_dados == 9 && linha_de_comando) { concluído_VALOR(); continue; }
            if (byte_dados == 1 || byte_dados == 5) { cursor_VALOR = byte_dados == 1 ? 0 : Tamanho; repetir_VALOR(); continue; }
            if (byte_dados == 8 || byte_dados == 127 || byte_dados == 21) {
                if (byte_dados == 21) { for (int Loop_ÍNDICE = cursor_VALOR; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE - cursor_VALOR] = InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE]; Tamanho -= cursor_VALOR; cursor_VALOR = 0; }
                else if (cursor_VALOR > 0) { int 변경전 = câmera_frontal_VALOR(cursor_VALOR); for (int Loop_ÍNDICE = cursor_VALOR; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE - cursor_VALOR + 변경전] = InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE]; Tamanho -= cursor_VALOR - 변경전; cursor_VALOR = 변경전; }
                repetir_VALOR(); continue;
            }
            if (byte_dados == 11) { Tamanho = cursor_VALOR; repetir_VALOR(); continue; }
            if (byte_dados < 32 && byte_dados != 9) continue;
            if (Tamanho == InterpretadorComandos.linha_de_entrada.length) { estouro = true; continue; }
            for (int Loop_ÍNDICE = Tamanho; Loop_ÍNDICE > cursor_VALOR; Loop_ÍNDICE--) InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE] = InterpretadorComandos.linha_de_entrada[Loop_ÍNDICE - 1];
            InterpretadorComandos.linha_de_entrada[cursor_VALOR++] = byte_dados; Tamanho++;
            if (cursor_VALOR == Tamanho && !가로보기 && 폭(0, Tamanho) <= 보이는폭()) Quadro.직렬쓰기(byte_dados);
            else if (cursor_VALOR == Tamanho) 보이는줄(); else repetir_VALOR();
        }
    }
}
