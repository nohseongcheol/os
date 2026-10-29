// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 linha_de_comando. Citação, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class InterpretadorComandos {
    static int[] linha_de_entrada = new int[4096], token_VALOR = new int[4096], 시작점 = new int[32], duração_VALOR = new int[32];
    static int[] Editado_Sumário = new int[16384], Editar_nome = new int[63];
    static int token_CONT_NÚM, Editar_nome_duração, resultado;
    static boolean Anterior_linha;
    static void 원바이트(int VALOR) { Quadro.직렬쓰기(VALOR); }
    static int ler_linha_de_entrada() { return editor_de_linha.Leitura(); }
    static boolean 나누기(int Tamanho) {
        int posição = 0, 끝 = 0; token_CONT_NÚM = 0;
        while (posição < Tamanho) {
            while (posição < Tamanho && (linha_de_entrada[posição] == 32 || linha_de_entrada[posição] == 9)) posição++;
            if (posição == Tamanho) break;
            if (token_CONT_NÚM == 16) { 단말.Escrita("comando analisar_VALOR: 인수가 너무 많습니다\n"); return false; }
            시작점[token_CONT_NÚM] = 끝; int Citação_VALOR = 0;
            while (posição < Tamanho) {
                int VALOR = linha_de_entrada[posição++];
                if (Citação_VALOR == 0 && (VALOR == 32 || VALOR == 9)) break;
                if (VALOR == Citação_VALOR) { Citação_VALOR = 0; continue; }
                if (Citação_VALOR == 0 && (VALOR == 39 || VALOR == 34)) { Citação_VALOR = VALOR; continue; }
                token_VALOR[끝++] = VALOR;
            }
            if (Citação_VALOR != 0) { 단말.Escrita("comando analisar_VALOR: 따옴표가 닫히지 않았습니다\n"); return false; }
            duração_VALOR[token_CONT_NÚM] = 끝 - 시작점[token_CONT_NÚM]; token_CONT_NÚM++;
        }
        return true;
    }
    static boolean 같음(int ÍNDICE, String Word_SMS) {
        if (ÍNDICE >= token_CONT_NÚM) return false;
        int cargo_ÍNDICE=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int ponto_de_código=Word_SMS.charAt(순번);
            if (ponto_de_código>=0xd800 && ponto_de_código<=0xdbff && 순번+1<Word_SMS.length()) ponto_de_código=0x10000+((ponto_de_código-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int byte_CONT_NÚM=ponto_de_código<128?1:ponto_de_código<2048?2:ponto_de_código<65536?3:4;
            for (int SEQUÊNCIA_VALOR=byte_CONT_NÚM-1; SEQUÊNCIA_VALOR>=0; SEQUÊNCIA_VALOR--) {
                int VALOR=byte_CONT_NÚM==1?ponto_de_código:SEQUÊNCIA_VALOR==byte_CONT_NÚM-1?(byte_CONT_NÚM==2?0xc0:byte_CONT_NÚM==3?0xe0:0xf0)|(ponto_de_código>>(6*SEQUÊNCIA_VALOR)):0x80|((ponto_de_código>>(6*SEQUÊNCIA_VALOR))&63);
                if (cargo_ÍNDICE>=duração_VALOR[ÍNDICE] || token_VALOR[시작점[ÍNDICE]+cargo_ÍNDICE++]!=VALOR) return false;
            }
        }
        return cargo_ÍNDICE==duração_VALOR[ÍNDICE];
    }
    static int caminho(int ÍNDICE) {
        if (ÍNDICE >= token_CONT_NÚM) return -22;
        int resultado = FicheirosMemória.caminho_START(duração_VALOR[ÍNDICE]); if (resultado < 0) return resultado;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < duração_VALOR[ÍNDICE]; Loop_ÍNDICE++) {
            resultado = FicheirosMemória.caminho_byte(Loop_ÍNDICE, token_VALOR[시작점[ÍNDICE] + Loop_ÍNDICE]); if (resultado < 0) return resultado;
        }
        return 0;
    }
    static void erro(int ÍNDICE) { resultado = 1; 단말.Escrita("erro "); 단말.número(ÍNDICE); 단말.문자(10); }
    static void Exibir_VALOR() {
        if (token_CONT_NÚM != 2) { 단말.Escrita("사용법: cat ficheiro\n"); return; }
        int resultado = caminho(1); if (resultado < 0) { erro(resultado); return; }
        int ficheiro = FicheirosMemória.Abrir(0); if (ficheiro < 0) { erro(ficheiro); return; }
        while (true) { int VALOR = FicheirosMemória.Leitura(ficheiro); if (VALOR == 256) break; if (VALOR < 0) { erro(VALOR); break; } 원바이트(VALOR); }
        FicheirosMemória.Fechar(ficheiro); 단말.문자(10);
    }
    static void Editar_VALOR() {
        if (token_CONT_NÚM != 2) { 단말.Escrita("사용법: edit ficheiro\n"); return; }
        int resultado = caminho(1); if (resultado < 0) { erro(resultado); return; }
        Editar_nome_duração = duração_VALOR[1];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Editar_nome_duração; Loop_ÍNDICE++) Editar_nome[Loop_ÍNDICE] = token_VALOR[시작점[1] + Loop_ÍNDICE];
        단말.Escrita("EDIT: ficheiro 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Tamanho = 0;
        while (true) {
            단말.Escrita("edit> "); int entrada_VALOR = ler_linha_de_entrada();
            if (entrada_VALOR < 0) { 단말.Escrita("EDIT CANCELLED\n"); return; }
            if (entrada_VALOR == 1 && linha_de_entrada[0] == '.') break;
            if (entrada_VALOR + 1 > Editado_Sumário.length - Tamanho) { 단말.Escrita("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_VALOR; Loop_ÍNDICE++) Editado_Sumário[Tamanho++] = linha_de_entrada[Loop_ÍNDICE];
            Editado_Sumário[Tamanho++] = 10;
        }
        FicheirosMemória.caminho_START(Editar_nome_duração);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Editar_nome_duração; Loop_ÍNDICE++) FicheirosMemória.caminho_byte(Loop_ÍNDICE, Editar_nome[Loop_ÍNDICE]);
        int ficheiro = FicheirosMemória.Abrir(577); if (ficheiro < 0) { erro(ficheiro); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) FicheirosMemória.Escrita(ficheiro, Editado_Sumário[Loop_ÍNDICE]);
        FicheirosMemória.Fechar(ficheiro); 단말.Escrita("SAVED "); 단말.número(Tamanho); 단말.Escrita("byte_VALOR(주기억 ficheiro)\n");
    }
    static int valor_hexadecimal(int VALOR) {
        if (VALOR >= '0' && VALOR <= '9') return VALOR - '0';
        if (VALOR >= 'a' && VALOR <= 'f') return VALOR - 'a' + 10;
        if (VALOR >= 'A' && VALOR <= 'F') return VALOR - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_CONT_NÚM != 2) { 단말.Escrita("사용법: load ficheiro | hex ficheiro\n"); return; }
        int resultado = caminho(1); if (resultado < 0) { erro(resultado); return; }
        if (!넣기) {
            int ficheiro = FicheirosMemória.Abrir(0); if (ficheiro < 0) { erro(ficheiro); return; }
            단말.Escrita("HEX BEGIN "); 단말.número(FicheirosMemória.Tamanho(ficheiro)); 단말.문자(10);
            int entrada_CONT_NÚM_8f7753a1 = 0;
            while (true) {
                int VALOR = FicheirosMemória.Leitura(ficheiro); if (VALOR < 0 || VALOR == 256) break;
                단말.문자("0123456789abcdef".charAt(VALOR >> 4)); 단말.문자("0123456789abcdef".charAt(VALOR & 15));
                if (++entrada_CONT_NÚM_8f7753a1 % 32 == 0) 단말.문자(10);
            }
            if (entrada_CONT_NÚM_8f7753a1 % 32 != 0) 단말.문자(10);
            FicheirosMemória.Fechar(ficheiro); 단말.Escrita("HEX END\n"); return;
        }
        Editar_nome_duração = duração_VALOR[1];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Editar_nome_duração; Loop_ÍNDICE++) Editar_nome[Loop_ÍNDICE] = token_VALOR[시작점[1] + Loop_ÍNDICE];
        단말.Escrita("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Tamanho = 0;
        while (true) {
            단말.Escrita("hex> "); int entrada_VALOR = ler_linha_de_entrada();
            if (entrada_VALOR < 0) { 단말.Escrita("LOAD CANCELLED\n"); return; }
            if (entrada_VALOR == 1 && linha_de_entrada[0] == '.') break;
            int câmera_frontal_VALOR = -1;
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_VALOR; Loop_ÍNDICE++) {
                if (linha_de_entrada[Loop_ÍNDICE] == 32 || linha_de_entrada[Loop_ÍNDICE] == 9) continue;
                int VALOR = valor_hexadecimal(linha_de_entrada[Loop_ÍNDICE]);
                if (VALOR < 0 || Tamanho >= Editado_Sumário.length) { 단말.Escrita("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (câmera_frontal_VALOR < 0) câmera_frontal_VALOR = VALOR; else { Editado_Sumário[Tamanho++] = câmera_frontal_VALOR * 16 + VALOR; câmera_frontal_VALOR = -1; }
            }
            if (câmera_frontal_VALOR >= 0) { 단말.Escrita("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        FicheirosMemória.caminho_START(Editar_nome_duração);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Editar_nome_duração; Loop_ÍNDICE++) FicheirosMemória.caminho_byte(Loop_ÍNDICE, Editar_nome[Loop_ÍNDICE]);
        int ficheiro = FicheirosMemória.Abrir(577); if (ficheiro < 0) { erro(ficheiro); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) FicheirosMemória.Escrita(ficheiro, Editado_Sumário[Loop_ÍNDICE]);
        FicheirosMemória.Fechar(ficheiro); 단말.Escrita("LOADED "); 단말.número(Tamanho); 단말.Escrita("byte_VALOR(주기억 ficheiro)\n");
    }
    static int ferramentas(int ÍNDICE) {
        return ferramenta_entrada(ÍNDICE, 1);
    }
    static int ferramenta_entrada(int ÍNDICE, int iniciar) {
        if (token_CONT_NÚM - iniciar > 8) return -22;
        Quadro.인수준비(token_CONT_NÚM - iniciar);
        for (int 첫값 = iniciar; 첫값 < token_CONT_NÚM; 첫값++) {
            if (duração_VALOR[첫값] > 255) return -36;
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < duração_VALOR[첫값]; Loop_ÍNDICE++) Quadro.argumento_byte(첫값 - iniciar, Loop_ÍNDICE, token_VALOR[시작점[첫값] + Loop_ÍNDICE]);
        }
        return ÍNDICE == -2 ? Quadro.리눅스파일실행() : ÍNDICE < 0 ? Quadro.Executar_usuário_Arquivo() : Quadro.executar_usuário_app(ÍNDICE);
    }
    static int PYTHON_grupo() {
        if (token_CONT_NÚM > 8) return -22;
        Quadro.인수준비(token_CONT_NÚM);
        String caminho = "/lib/grupo.py";
        // Java 문자열을 셸의 UTF-8 argumentos 버퍼에 기록한다.
        int cargo_ÍNDICE = 0;
        for (int 순번 = 0; 순번 < caminho.length(); 순번++) {
            int caractere_VALOR = caminho.charAt(순번);
            if (caractere_VALOR < 128) Quadro.argumento_byte(0, cargo_ÍNDICE++, caractere_VALOR);
            else { Quadro.argumento_byte(0, cargo_ÍNDICE++, 0xe0 | (caractere_VALOR >> 12)); Quadro.argumento_byte(0, cargo_ÍNDICE++, 0x80 | ((caractere_VALOR >> 6) & 63)); Quadro.argumento_byte(0, cargo_ÍNDICE++, 0x80 | (caractere_VALOR & 63)); }
        }
        for (int 순번 = 1; 순번 < token_CONT_NÚM; 순번++) {
            if (duração_VALOR[순번] > 255) return -36;
            for (int caractere_VALOR = 0; caractere_VALOR < duração_VALOR[순번]; caractere_VALOR++) Quadro.argumento_byte(순번, caractere_VALOR, token_VALOR[시작점[순번] + caractere_VALOR]);
        }
        return Quadro.executar_usuário_app(12);
    }
    static int execução_formato() {
        int 처리값 = caminho(0); if (처리값 < 0) return 처리값;
        int ficheiro = FicheirosMemória.Abrir(0); if (ficheiro < 0) return ficheiro;
        int 첫값 = FicheirosMemória.Leitura(ficheiro), byte_dados = FicheirosMemória.Leitura(ficheiro), ponto_de_código = FicheirosMemória.Leitura(ficheiro), à_direita_VALOR = FicheirosMemória.Leitura(ficheiro);
        FicheirosMemória.Fechar(ficheiro);
        if (첫값 == 127 && byte_dados == 'E' && ponto_de_código == 'L' && à_direita_VALOR == 'F') return 1;
        if (첫값 == 'P' && byte_dados == 'K' && ponto_de_código == 3 && à_direita_VALOR == 4) return 2;
        return 0;
    }
    static int 예제실행(int ÍNDICE, String argumentos) {
        Quadro.인수준비(1);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < argumentos.length(); Loop_ÍNDICE++) Quadro.argumento_byte(0, Loop_ÍNDICE, argumentos.charAt(Loop_ÍNDICE));
        return Quadro.executar_usuário_app(ÍNDICE);
    }
    static void SMS_byte(int ficheiro, int VALOR) { FicheirosMemória.Escrita(ficheiro, VALOR); }
    static void estático_Arquivo(String Nome, String Conteúdo_VALOR) {
        // grupo 파일명은 ASCII. ficheiro 내용은 UTF-8로 저장한다.
        FicheirosMemória.caminho_START(Nome.length());
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Nome.length(); Loop_ÍNDICE++) FicheirosMemória.caminho_byte(Loop_ÍNDICE, Nome.charAt(Loop_ÍNDICE));
        int ficheiro = FicheirosMemória.Abrir(193); if (ficheiro < 0) return;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Conteúdo_VALOR.length(); Loop_ÍNDICE++) {
            int ponto_de_código = Conteúdo_VALOR.charAt(Loop_ÍNDICE);
            if (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdbff && Loop_ÍNDICE + 1 < Conteúdo_VALOR.length()) ponto_de_código = 0x10000 + ((ponto_de_código - 0xd800) << 10) + Conteúdo_VALOR.charAt(++Loop_ÍNDICE) - 0xdc00;
            if (ponto_de_código < 128) SMS_byte(ficheiro, ponto_de_código);
            else {
                int número = ponto_de_código < 2048 ? 2 : ponto_de_código < 65536 ? 3 : 4;
                SMS_byte(ficheiro, (número == 2 ? 0xc0 : número == 3 ? 0xe0 : 0xf0) | (ponto_de_código >> (6 * (número - 1))));
                for (int entrada_CONT_NÚM_8f7753a1 = número - 1; entrada_CONT_NÚM_8f7753a1 > 0; entrada_CONT_NÚM_8f7753a1--) SMS_byte(ficheiro, 0x80 | ((ponto_de_código >> (6 * (entrada_CONT_NÚM_8f7753a1 - 1))) & 63));
            }
        }
        FicheirosMemória.Fechar(ficheiro);
    }
    static void 한글도움말() {
        단말.Escrita("F9 ou Shift+Space ativa a escrita em português.\n");
        단말.Escrita("  [PT] keyboard; [EN] ASCII\n");
        단말.Escrita("  ; → ç\n");
        단말.Escrita("  F9: EN ↔ Português | Ctrl+Shift+V: UTF-8\n");
        단말.Escrita("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Escrita("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nome) {
        int byte_CONT_NÚM = 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Nome.length(); Loop_ÍNDICE++) { int ponto_de_código = Nome.charAt(Loop_ÍNDICE); if (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdfff) return -22; byte_CONT_NÚM += ponto_de_código < 128 ? 1 : ponto_de_código < 2048 ? 2 : 3; }
        int 처리값 = FicheirosMemória.caminho_START(byte_CONT_NÚM); if (처리값 < 0) return 처리값;
        int cargo_ÍNDICE = 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Nome.length(); Loop_ÍNDICE++) {
            int ponto_de_código = Nome.charAt(Loop_ÍNDICE);
            if (ponto_de_código < 128) FicheirosMemória.caminho_byte(cargo_ÍNDICE++, ponto_de_código);
            else if (ponto_de_código < 2048) { FicheirosMemória.caminho_byte(cargo_ÍNDICE++, 0xc0 | (ponto_de_código >> 6)); FicheirosMemória.caminho_byte(cargo_ÍNDICE++, 0x80 | (ponto_de_código & 63)); }
            else { FicheirosMemória.caminho_byte(cargo_ÍNDICE++, 0xe0 | (ponto_de_código >> 12)); FicheirosMemória.caminho_byte(cargo_ÍNDICE++, 0x80 | ((ponto_de_código >> 6) & 63)); FicheirosMemória.caminho_byte(cargo_ÍNDICE++, 0x80 | (ponto_de_código & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nome) {
        int 처리값 = 예제경로(Nome); if (처리값 < 0) return 처리값;
        처리값 = FicheirosMemória.Criar_Diretório(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nome, String dados) {
        int 처리값 = 예제경로(Nome); if (처리값 < 0) return 처리값;
        int ficheiro = FicheirosMemória.Abrir(193); if (ficheiro == -17) return 0; if (ficheiro < 0) return ficheiro;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < dados.length(); Loop_ÍNDICE += 2) {
            처리값 = FicheirosMemória.Escrita(ficheiro, valor_hexadecimal(dados.charAt(Loop_ÍNDICE)) * 16 + valor_hexadecimal(dados.charAt(Loop_ÍNDICE + 1)));
            if (처리값 < 0) { FicheirosMemória.Fechar(ficheiro); return 처리값; }
        }
        return FicheirosMemória.Fechar(ficheiro);
    }
    static void mostrar_ajuda() {
        Sistema_ferramenta.mostrar_ajuda();
        단말.Escrita("sshd / SSH start|stop|status: SSH :22 (user, 장치별 senha_VALOR)\n");
        단말.Escrita("vncd / remoto_visor start|stop|status: VNC :5900 (장치별 senha_VALOR)\n");
        단말.Escrita("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Escrita("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Escrita("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Escrita("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Escrita("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Escrita("모서리 + 왼쪽 버튼 arrastar_VALOR: terminal Tamanho alterar_VALOR; terminal size: COL_VALOR/LIN_VALOR\n");
        단말.Escrita("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Escrita("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Escrita("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Escrita("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Escrita("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Escrita("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Escrita("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Escrita("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Escrita("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Escrita("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Escrita("pip: MicroPython fonte_árvore instalar_VALOR; host --network --pip 필요; /lib는 RAM\n");
        단말.Escrita("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Escrita("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Escrita("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Escrita("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void terminal(boolean 전환여부) {
        if (전환여부 && Quadro.terminal(2) != 0) { Quadro.terminal(0); 단말.Escrita("TERMINAL CLOSED\n"); }
        else if (Quadro.terminal(1) < 0) erro(-19);
        else 단말.Escrita("TERMINAL READY — Português terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void comando() {
        if (token_CONT_NÚM == 0) return;
        if (Sistema_ferramenta.Executar_comando()) return;
        if (같음(0,"sshd") || 같음(0,"SSH") || 같음(0,"vncd") || 같음(0,"remoto_visor")) {
            int Tipo_VALOR=같음(0,"vncd")||같음(0,"remoto_visor")?1:0;
            int Acção=같음(1,"start")||같음(1,"iniciar")?1:같음(1,"stop")||같음(1,"Parar")?0:2;
            int Estado_VALOR=Quadro.sombreamento(Tipo_VALOR,Acção);
            if(Estado_VALOR<0)erro(Estado_VALOR);else 단말.Escrita(Quadro.sombreamento(Tipo_VALOR,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else mostrar_ajuda(); }
        else if (같음(0, "info") || 같음(0, "i")) Núcleo.msinfo32_exe();
        else if (같음(0, "pwd")) { FicheirosMemória.em_dia_gravar(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_CONT_NÚM == 1) { FicheirosMemória.caminho_START(1); 처리값 = FicheirosMemória.caminho_byte(0, '/'); } else 처리값 = token_CONT_NÚM == 2 ? caminho(1) : -22;
            if (처리값 >= 0) 처리값 = FicheirosMemória.alterar_Diretório(); if (처리값 < 0) erro(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argumento_ÍNDICE = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_CONT_NÚM == argumento_ÍNDICE) { FicheirosMemória.caminho_START(1); 처리값 = FicheirosMemória.caminho_byte(0, '.'); } else 처리값 = token_CONT_NÚM == argumento_ÍNDICE + 1 ? caminho(argumento_ÍNDICE) : -22;
            if (처리값 >= 0) 처리값 = FicheirosMemória.경로목록(); if (처리값 < 0) erro(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) shell_Ferramentas.Arquivo_cargo(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) shell_Ferramentas.copiar_VALOR(같음(0, "mv"));
        else if (같음(0, "cat")) shell_Ferramentas.Exibir_VALOR();
        else if (같음(0, "wc")) shell_Ferramentas.세기();
        else if (같음(0, "grep")) shell_Ferramentas.PROCURAR_entrada();
        else if (같음(0, "head") || 같음(0, "tail")) shell_Ferramentas.HEAD_VALOR(같음(0, "tail"));
        else if (같음(0, "tee")) shell_Ferramentas.gravar_Juntos();
        else if (같음(0, "env")) shell_sintaxe.mostrar_ambiente();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_CONT_NÚM == 1) shell_sintaxe.mostrar_ambiente();
            for (int Loop_ÍNDICE = 1; Loop_ÍNDICE < token_CONT_NÚM; Loop_ÍNDICE++) { int 처리값 = shell_sintaxe.ambiente_Configurações(Loop_ÍNDICE, 같음(0, "unset")); if (처리값 != 0) { resultado = 처리값; 단말.Escrita("comando analisar_VALOR: variável_VALOR 이름이 잘못되었거나 예약된 이름이거나 ambiente 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) shell_sintaxe.Executar_Arquivo();
        else if (같음(0, "true")) resultado = 0;
        else if (같음(0, "false")) resultado = 1;
        else if (같음(0, "history")) editor_de_linha.mostrar_LOG();
        else if (같음(0, "exit")) {
            if (shell_sintaxe.깊이 > 0) { resultado = token_CONT_NÚM == 1 ? shell_sintaxe.Estado_VALOR : shell_Ferramentas.dígito_VALOR(1); if (resultado < 0 || resultado > 255) resultado = 2; shell_sintaxe.script_encerrar = true; }
            else if (Quadro.terminal(2) != 0) terminal(true);
            else 단말.Escrita("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Editar_VALOR();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_CONT_NÚM < 2) { resultado = 2; 단말.Escrita("사용법: rm ficheiro...\n"); }
            for (int Loop_ÍNDICE = 1; Loop_ÍNDICE < token_CONT_NÚM; Loop_ÍNDICE++) { int 처리값 = caminho(Loop_ÍNDICE); if (처리값 == 0) 처리값 = FicheirosMemória.apagar_entrada(); if (처리값 < 0) erro(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_cargo = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_cargo; 첫값 < token_CONT_NÚM; 첫값++) { if (첫값 > START_cargo) 단말.문자(32); for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < duração_VALOR[첫값]; Loop_ÍNDICE++) Quadro.직렬쓰기(token_VALOR[시작점[첫값] + Loop_ÍNDICE]); }
            if (START_cargo == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Escrita("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_grupo() : ferramentas(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); resultado = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !shell_sintaxe.연결중) { 단말.Escrita("exit "); 단말.número(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = ferramentas(13); resultado = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = ferramentas(15); resultado = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaxe.연결중) { 단말.Escrita("exit "); 단말.número(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = ferramentas(16); resultado = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaxe.연결중) { 단말.Escrita("exit "); 단말.número(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Tamanho = Quadro.terminal(13); 단말.Escrita("TERMINAL SIZE "); 단말.número(Tamanho & 65535); 단말.문자('x'); 단말.número(Tamanho >>> 16); 단말.문자(10); }
            else terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Quadro.terminal(9); desktop.Executar_comando(); }
        else if (같음(0, "c")) Núcleo.teste_C();
        else if (같음(0, "tasks") || 같음(0, "t")) Núcleo.teste_Tasks();
        else if (같음(0, "g")) Núcleo.tela();
        else if (같음(0, "selftest") || 같음(0, "u")) Núcleo.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Quadro.executar_usuário_app(0); if (처리값 == 0) 단말.Escrita("ELF DEMO PASS\n"); else erro(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? ferramenta_entrada(-2, 2) : ferramentas(-1); resultado = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !shell_sintaxe.연결중) { 단말.Escrita("exit "); 단말.número(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) Núcleo.teste_Rede();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Quadro.transferência_de_arquivo_serviço(1); if (처리값 < 0) erro(처리값); else { 단말.Escrita("FTP listening "); Sistema_ferramenta.gravar_email(Quadro.rede_Status(0,0)); 단말.Escrita(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Quadro.transferência_de_arquivo_serviço(0); 단말.Escrita("FTP stopped\n"); }
            else 단말.Escrita(Quadro.transferência_de_arquivo_serviço(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { grupo.Preparar(); 단말.Escrita("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Idioma = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_CONT_NÚM != 2 || Idioma < 0) 단말.Escrita("example java|c|python: saídaTexto, ficheiro, 네트워크, 그래픽, Java Swing Janela 예제\n");
            else { int 처리값 = 예제꾸러미.instalar_VALOR(Idioma); if (처리값 < 0) { erro(처리값); if (처리값 == -28) 단말.Escrita("RAM full: remove unused files, then retry example\n"); } else 단말.Escrita("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formato_VALOR = execução_formato();
            if (formato_VALOR == 1 || formato_VALOR == 2) {
                int 처리값 = ferramenta_entrada(formato_VALOR == 1 ? -1 : 14, 0); resultado = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !shell_sintaxe.연결중) { 단말.Escrita("exit "); 단말.número(처리값); 단말.문자(10); }
            } else if (formato_VALOR == 0) { resultado = 126; 단말.Escrita("실행할 número 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { resultado = 127; 단말.Escrita("Unknown command. help: commands\n"); }
        }
    }
    public static void Executar_comando() {
        grupo.Preparar();
        for (int Idioma = 0; Idioma < 3; Idioma++) { int 처리값 = 예제꾸러미.instalar_VALOR(Idioma); if (처리값 < 0) erro(처리값); }
        mostrar_ajuda();
        while (true) {
            janela_sessão.Processo_VALOR_entrada(); if (janela_sessão.CV_execução()) continue;
            if (!janela_sessão.이어읽기) 단말.Escrita("jkoros-native> "); editor_de_linha.linha_de_comando = true; Quadro.remoto_aguarde(1); int Tamanho = ler_linha_de_entrada(); Quadro.remoto_aguarde(0); editor_de_linha.linha_de_comando = false;
            if (Tamanho == -3) continue;
            if (Tamanho == -2) 단말.Escrita("comando analisar_VALOR: 명령줄이 너무 깁니다\n");
            if (Tamanho >= 0) { shell_sintaxe.script_encerrar = false; shell_sintaxe.Executar_comando(linha_de_entrada, 0, Tamanho, 0); } else shell_sintaxe.Estado_VALOR = 130;
            Quadro.encerrar_remoto_comando(shell_sintaxe.Estado_VALOR);
            editor_de_linha.Tamanho = editor_de_linha.cursor_VALOR = editor_de_linha.START_janela = 0;
        }
    }
}
