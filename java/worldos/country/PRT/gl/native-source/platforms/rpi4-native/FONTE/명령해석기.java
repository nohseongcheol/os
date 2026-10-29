// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 liña_de_comandos. Cita, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Liña = new int[4096], ficha_VALOR = new int[4096], 시작점 = new int[32], duración_VALOR = new int[32];
    static int[] Edición_Contido = new int[16384], editar_nome = new int[63];
    static int ficha_CONTAR, editar_nome_duración, RESULTANTE;
    static boolean 앞줄;
    static void 원바이트(int VALOR) { Panel.직렬쓰기(VALOR); }
    static int 줄읽기() { return liña_Editor.Lectura(); }
    static boolean 나누기(int Tamaño) {
        int Posición = 0, 끝 = 0; ficha_CONTAR = 0;
        while (Posición < Tamaño) {
            while (Posición < Tamaño && (Liña[Posición] == 32 || Liña[Posición] == 9)) Posición++;
            if (Posición == Tamaño) break;
            if (ficha_CONTAR == 16) { 단말.Escritura("Orde analizar_VALOR: 인수가 너무 많습니다\n"); return false; }
            시작점[ficha_CONTAR] = 끝; int Cita_VALOR = 0;
            while (Posición < Tamaño) {
                int VALOR = Liña[Posición++];
                if (Cita_VALOR == 0 && (VALOR == 32 || VALOR == 9)) break;
                if (VALOR == Cita_VALOR) { Cita_VALOR = 0; continue; }
                if (Cita_VALOR == 0 && (VALOR == 39 || VALOR == 34)) { Cita_VALOR = VALOR; continue; }
                ficha_VALOR[끝++] = VALOR;
            }
            if (Cita_VALOR != 0) { 단말.Escritura("Orde analizar_VALOR: 따옴표가 닫히지 않았습니다\n"); return false; }
            duración_VALOR[ficha_CONTAR] = 끝 - 시작점[ficha_CONTAR]; ficha_CONTAR++;
        }
        return true;
    }
    static boolean 같음(int ÍNDICE, String Word_SMS) {
        if (ÍNDICE >= ficha_CONTAR) return false;
        int cargo_ÍNDICE=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int código_de_carácter=Word_SMS.charAt(순번);
            if (código_de_carácter>=0xd800 && código_de_carácter<=0xdbff && 순번+1<Word_SMS.length()) código_de_carácter=0x10000+((código_de_carácter-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int byte_CONTAR=código_de_carácter<128?1:código_de_carácter<2048?2:código_de_carácter<65536?3:4;
            for (int SECUENCIA_VALOR=byte_CONTAR-1; SECUENCIA_VALOR>=0; SECUENCIA_VALOR--) {
                int VALOR=byte_CONTAR==1?código_de_carácter:SECUENCIA_VALOR==byte_CONTAR-1?(byte_CONTAR==2?0xc0:byte_CONTAR==3?0xe0:0xf0)|(código_de_carácter>>(6*SECUENCIA_VALOR)):0x80|((código_de_carácter>>(6*SECUENCIA_VALOR))&63);
                if (cargo_ÍNDICE>=duración_VALOR[ÍNDICE] || ficha_VALOR[시작점[ÍNDICE]+cargo_ÍNDICE++]!=VALOR) return false;
            }
        }
        return cargo_ÍNDICE==duración_VALOR[ÍNDICE];
    }
    static int CAMIÑO(int ÍNDICE) {
        if (ÍNDICE >= ficha_CONTAR) return -22;
        int RESULTANTE = Memoria_Ficheiros.camiño_START(duración_VALOR[ÍNDICE]); if (RESULTANTE < 0) return RESULTANTE;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < duración_VALOR[ÍNDICE]; Loop_ÍNDICE++) {
            RESULTANTE = Memoria_Ficheiros.camiño_byte(Loop_ÍNDICE, ficha_VALOR[시작점[ÍNDICE] + Loop_ÍNDICE]); if (RESULTANTE < 0) return RESULTANTE;
        }
        return 0;
    }
    static void ERRO(int ÍNDICE) { RESULTANTE = 1; 단말.Escritura("ERRO "); 단말.수(ÍNDICE); 단말.문자(10); }
    static void ver_VALOR() {
        if (ficha_CONTAR != 2) { 단말.Escritura("사용법: cat Ficheiro\n"); return; }
        int RESULTANTE = CAMIÑO(1); if (RESULTANTE < 0) { ERRO(RESULTANTE); return; }
        int Ficheiro = Memoria_Ficheiros.Abrir(0); if (Ficheiro < 0) { ERRO(Ficheiro); return; }
        while (true) { int VALOR = Memoria_Ficheiros.Lectura(Ficheiro); if (VALOR == 256) break; if (VALOR < 0) { ERRO(VALOR); break; } 원바이트(VALOR); }
        Memoria_Ficheiros.Pechar(Ficheiro); 단말.문자(10);
    }
    static void editar_VALOR() {
        if (ficha_CONTAR != 2) { 단말.Escritura("사용법: edit Ficheiro\n"); return; }
        int RESULTANTE = CAMIÑO(1); if (RESULTANTE < 0) { ERRO(RESULTANTE); return; }
        editar_nome_duración = duración_VALOR[1];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < editar_nome_duración; Loop_ÍNDICE++) editar_nome[Loop_ÍNDICE] = ficha_VALOR[시작점[1] + Loop_ÍNDICE];
        단말.Escritura("EDIT: Ficheiro 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Tamaño = 0;
        while (true) {
            단말.Escritura("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Escritura("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Liña[0] == '.') break;
            if (입력 + 1 > Edición_Contido.length - Tamaño) { 단말.Escritura("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 입력; Loop_ÍNDICE++) Edición_Contido[Tamaño++] = Liña[Loop_ÍNDICE];
            Edición_Contido[Tamaño++] = 10;
        }
        Memoria_Ficheiros.camiño_START(editar_nome_duración);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < editar_nome_duración; Loop_ÍNDICE++) Memoria_Ficheiros.camiño_byte(Loop_ÍNDICE, editar_nome[Loop_ÍNDICE]);
        int Ficheiro = Memoria_Ficheiros.Abrir(577); if (Ficheiro < 0) { ERRO(Ficheiro); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) Memoria_Ficheiros.Escritura(Ficheiro, Edición_Contido[Loop_ÍNDICE]);
        Memoria_Ficheiros.Pechar(Ficheiro); 단말.Escritura("SAVED "); 단말.수(Tamaño); 단말.Escritura("byte_VALOR(주기억 Ficheiro)\n");
    }
    static int hexadecimal_VALOR(int VALOR) {
        if (VALOR >= '0' && VALOR <= '9') return VALOR - '0';
        if (VALOR >= 'a' && VALOR <= 'f') return VALOR - 'a' + 10;
        if (VALOR >= 'A' && VALOR <= 'F') return VALOR - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (ficha_CONTAR != 2) { 단말.Escritura("사용법: load Ficheiro | hex Ficheiro\n"); return; }
        int RESULTANTE = CAMIÑO(1); if (RESULTANTE < 0) { ERRO(RESULTANTE); return; }
        if (!넣기) {
            int Ficheiro = Memoria_Ficheiros.Abrir(0); if (Ficheiro < 0) { ERRO(Ficheiro); return; }
            단말.Escritura("HEX BEGIN "); 단말.수(Memoria_Ficheiros.Tamaño(Ficheiro)); 단말.문자(10);
            int introdución_CONTAR = 0;
            while (true) {
                int VALOR = Memoria_Ficheiros.Lectura(Ficheiro); if (VALOR < 0 || VALOR == 256) break;
                단말.문자("0123456789abcdef".charAt(VALOR >> 4)); 단말.문자("0123456789abcdef".charAt(VALOR & 15));
                if (++introdución_CONTAR % 32 == 0) 단말.문자(10);
            }
            if (introdución_CONTAR % 32 != 0) 단말.문자(10);
            Memoria_Ficheiros.Pechar(Ficheiro); 단말.Escritura("HEX END\n"); return;
        }
        editar_nome_duración = duración_VALOR[1];
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < editar_nome_duración; Loop_ÍNDICE++) editar_nome[Loop_ÍNDICE] = ficha_VALOR[시작점[1] + Loop_ÍNDICE];
        단말.Escritura("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Tamaño = 0;
        while (true) {
            단말.Escritura("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Escritura("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Liña[0] == '.') break;
            int frontal_VALOR = -1;
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 입력; Loop_ÍNDICE++) {
                if (Liña[Loop_ÍNDICE] == 32 || Liña[Loop_ÍNDICE] == 9) continue;
                int VALOR = hexadecimal_VALOR(Liña[Loop_ÍNDICE]);
                if (VALOR < 0 || Tamaño >= Edición_Contido.length) { 단말.Escritura("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (frontal_VALOR < 0) frontal_VALOR = VALOR; else { Edición_Contido[Tamaño++] = frontal_VALOR * 16 + VALOR; frontal_VALOR = -1; }
            }
            if (frontal_VALOR >= 0) { 단말.Escritura("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memoria_Ficheiros.camiño_START(editar_nome_duración);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < editar_nome_duración; Loop_ÍNDICE++) Memoria_Ficheiros.camiño_byte(Loop_ÍNDICE, editar_nome[Loop_ÍNDICE]);
        int Ficheiro = Memoria_Ficheiros.Abrir(577); if (Ficheiro < 0) { ERRO(Ficheiro); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) Memoria_Ficheiros.Escritura(Ficheiro, Edición_Contido[Loop_ÍNDICE]);
        Memoria_Ficheiros.Pechar(Ficheiro); 단말.Escritura("LOADED "); 단말.수(Tamaño); 단말.Escritura("byte_VALOR(주기억 Ficheiro)\n");
    }
    static int Ferramentas(int ÍNDICE) {
        return ferramenta_introdución(ÍNDICE, 1);
    }
    static int ferramenta_introdución(int ÍNDICE, int Executar_2) {
        if (ficha_CONTAR - Executar_2 > 8) return -22;
        Panel.인수준비(ficha_CONTAR - Executar_2);
        for (int 첫값 = Executar_2; 첫값 < ficha_CONTAR; 첫값++) {
            if (duración_VALOR[첫값] > 255) return -36;
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < duración_VALOR[첫값]; Loop_ÍNDICE++) Panel.argumento_byte(첫값 - Executar_2, Loop_ÍNDICE, ficha_VALOR[시작점[첫값] + Loop_ÍNDICE]);
        }
        return ÍNDICE == -2 ? Panel.리눅스파일실행() : ÍNDICE < 0 ? Panel.executar_usuario_Ficheiro() : Panel.executar_usuario_apl(ÍNDICE);
    }
    static int PYTHON_paquete() {
        if (ficha_CONTAR > 8) return -22;
        Panel.인수준비(ficha_CONTAR);
        String CAMIÑO = "/lib/paquete.py";
        // Java 문자열을 셸의 UTF-8 Argumentos 버퍼에 기록한다.
        int cargo_ÍNDICE = 0;
        for (int 순번 = 0; 순번 < CAMIÑO.length(); 순번++) {
            int carácter_VALOR = CAMIÑO.charAt(순번);
            if (carácter_VALOR < 128) Panel.argumento_byte(0, cargo_ÍNDICE++, carácter_VALOR);
            else { Panel.argumento_byte(0, cargo_ÍNDICE++, 0xe0 | (carácter_VALOR >> 12)); Panel.argumento_byte(0, cargo_ÍNDICE++, 0x80 | ((carácter_VALOR >> 6) & 63)); Panel.argumento_byte(0, cargo_ÍNDICE++, 0x80 | (carácter_VALOR & 63)); }
        }
        for (int 순번 = 1; 순번 < ficha_CONTAR; 순번++) {
            if (duración_VALOR[순번] > 255) return -36;
            for (int carácter_VALOR = 0; carácter_VALOR < duración_VALOR[순번]; carácter_VALOR++) Panel.argumento_byte(순번, carácter_VALOR, ficha_VALOR[시작점[순번] + carácter_VALOR]);
        }
        return Panel.executar_usuario_apl(12);
    }
    static int 실행형식() {
        int 처리값 = CAMIÑO(0); if (처리값 < 0) return 처리값;
        int Ficheiro = Memoria_Ficheiros.Abrir(0); if (Ficheiro < 0) return Ficheiro;
        int 첫값 = Memoria_Ficheiros.Lectura(Ficheiro), byte_datos = Memoria_Ficheiros.Lectura(Ficheiro), código_de_carácter = Memoria_Ficheiros.Lectura(Ficheiro), 뒷값 = Memoria_Ficheiros.Lectura(Ficheiro);
        Memoria_Ficheiros.Pechar(Ficheiro);
        if (첫값 == 127 && byte_datos == 'E' && código_de_carácter == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_datos == 'K' && código_de_carácter == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int ÍNDICE, String Argumentos) {
        Panel.인수준비(1);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Argumentos.length(); Loop_ÍNDICE++) Panel.argumento_byte(0, Loop_ÍNDICE, Argumentos.charAt(Loop_ÍNDICE));
        return Panel.executar_usuario_apl(ÍNDICE);
    }
    static void SMS_byte(int Ficheiro, int VALOR) { Memoria_Ficheiros.Escritura(Ficheiro, VALOR); }
    static void estático_Ficheiro(String Nome, String Contido_VALOR) {
        // paquete 파일명은 ASCII. Ficheiro 내용은 UTF-8로 저장한다.
        Memoria_Ficheiros.camiño_START(Nome.length());
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Nome.length(); Loop_ÍNDICE++) Memoria_Ficheiros.camiño_byte(Loop_ÍNDICE, Nome.charAt(Loop_ÍNDICE));
        int Ficheiro = Memoria_Ficheiros.Abrir(193); if (Ficheiro < 0) return;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Contido_VALOR.length(); Loop_ÍNDICE++) {
            int código_de_carácter = Contido_VALOR.charAt(Loop_ÍNDICE);
            if (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdbff && Loop_ÍNDICE + 1 < Contido_VALOR.length()) código_de_carácter = 0x10000 + ((código_de_carácter - 0xd800) << 10) + Contido_VALOR.charAt(++Loop_ÍNDICE) - 0xdc00;
            if (código_de_carácter < 128) SMS_byte(Ficheiro, código_de_carácter);
            else {
                int 수 = código_de_carácter < 2048 ? 2 : código_de_carácter < 65536 ? 3 : 4;
                SMS_byte(Ficheiro, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (código_de_carácter >> (6 * (수 - 1))));
                for (int introdución_CONTAR = 수 - 1; introdución_CONTAR > 0; introdución_CONTAR--) SMS_byte(Ficheiro, 0x80 | ((código_de_carácter >> (6 * (introdución_CONTAR - 1))) & 63));
            }
        }
        Memoria_Ficheiros.Pechar(Ficheiro);
    }
    static void 한글도움말() {
        단말.Escritura("F9 / Shift+Space: [EN] ↔ [gl]\n");
        단말.Escritura("  [GL] keyboard; [EN] ASCII\n");
        단말.Escritura("  a → a\n");
        단말.Escritura("  F9: EN ↔ gl | Ctrl+Shift+V: UTF-8\n");
        단말.Escritura("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Escritura("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nome) {
        int byte_CONTAR = 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Nome.length(); Loop_ÍNDICE++) { int código_de_carácter = Nome.charAt(Loop_ÍNDICE); if (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdfff) return -22; byte_CONTAR += código_de_carácter < 128 ? 1 : código_de_carácter < 2048 ? 2 : 3; }
        int 처리값 = Memoria_Ficheiros.camiño_START(byte_CONTAR); if (처리값 < 0) return 처리값;
        int cargo_ÍNDICE = 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Nome.length(); Loop_ÍNDICE++) {
            int código_de_carácter = Nome.charAt(Loop_ÍNDICE);
            if (código_de_carácter < 128) Memoria_Ficheiros.camiño_byte(cargo_ÍNDICE++, código_de_carácter);
            else if (código_de_carácter < 2048) { Memoria_Ficheiros.camiño_byte(cargo_ÍNDICE++, 0xc0 | (código_de_carácter >> 6)); Memoria_Ficheiros.camiño_byte(cargo_ÍNDICE++, 0x80 | (código_de_carácter & 63)); }
            else { Memoria_Ficheiros.camiño_byte(cargo_ÍNDICE++, 0xe0 | (código_de_carácter >> 12)); Memoria_Ficheiros.camiño_byte(cargo_ÍNDICE++, 0x80 | ((código_de_carácter >> 6) & 63)); Memoria_Ficheiros.camiño_byte(cargo_ÍNDICE++, 0x80 | (código_de_carácter & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nome) {
        int 처리값 = 예제경로(Nome); if (처리값 < 0) return 처리값;
        처리값 = Memoria_Ficheiros.crear_directorio(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nome, String datos) {
        int 처리값 = 예제경로(Nome); if (처리값 < 0) return 처리값;
        int Ficheiro = Memoria_Ficheiros.Abrir(193); if (Ficheiro == -17) return 0; if (Ficheiro < 0) return Ficheiro;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < datos.length(); Loop_ÍNDICE += 2) {
            처리값 = Memoria_Ficheiros.Escritura(Ficheiro, hexadecimal_VALOR(datos.charAt(Loop_ÍNDICE)) * 16 + hexadecimal_VALOR(datos.charAt(Loop_ÍNDICE + 1)));
            if (처리값 < 0) { Memoria_Ficheiros.Pechar(Ficheiro); return 처리값; }
        }
        return Memoria_Ficheiros.Pechar(Ficheiro);
    }
    static void mostrar_axuda() {
        sistema_ferramenta.mostrar_axuda();
        단말.Escritura("sshd / seguro_shell start|stop|status: SSH :22 (user, 장치별 contrasinal_VALOR)\n");
        단말.Escritura("vncd / remoto_mostrar start|stop|status: VNC :5900 (장치별 contrasinal_VALOR)\n");
        단말.Escritura("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Escritura("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Escritura("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Escritura("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Escritura("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Escritura("모서리 + 왼쪽 버튼 arrastrar_VALOR: Terminal Tamaño modificar_VALOR; terminal size: COLUMNA_VALOR/FILA_VALOR\n");
        단말.Escritura("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Escritura("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Escritura("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Escritura("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Escritura("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Escritura("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Escritura("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Escritura("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Escritura("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Escritura("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Escritura("pip: MicroPython fonte_árbore instalar_VALOR; hospedar --network --pip 필요; /lib는 RAM\n");
        단말.Escritura("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Escritura("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Escritura("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Escritura("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && Panel.Terminal(2) != 0) { Panel.Terminal(0); 단말.Escritura("TERMINAL CLOSED\n"); }
        else if (Panel.Terminal(1) < 0) ERRO(-19);
        else 단말.Escritura("TERMINAL READY — gl terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Orde() {
        if (ficha_CONTAR == 0) return;
        if (sistema_ferramenta.executar_comando()) return;
        if (같음(0,"sshd") || 같음(0,"seguro_shell") || 같음(0,"vncd") || 같음(0,"remoto_mostrar")) {
            int 종류=같음(0,"vncd")||같음(0,"remoto_mostrar")?1:0;
            int Acción=같음(1,"start")||같음(1,"Executar_2")?1:같음(1,"stop")||같음(1,"Deter")?0:2;
            int Estado_VALOR=Panel.vixilancia(종류,Acción);
            if(Estado_VALOR<0)ERRO(Estado_VALOR);else 단말.Escritura(Panel.vixilancia(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else mostrar_axuda(); }
        else if (같음(0, "info") || 같음(0, "i")) kernel.msinfo32_exe();
        else if (같음(0, "pwd")) { Memoria_Ficheiros.ao_corrente_escribir(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (ficha_CONTAR == 1) { Memoria_Ficheiros.camiño_START(1); 처리값 = Memoria_Ficheiros.camiño_byte(0, '/'); } else 처리값 = ficha_CONTAR == 2 ? CAMIÑO(1) : -22;
            if (처리값 >= 0) 처리값 = Memoria_Ficheiros.modificar_directorio(); if (처리값 < 0) ERRO(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argumento_ÍNDICE = 같음(1, "-l") ? 2 : 1, 처리값;
            if (ficha_CONTAR == argumento_ÍNDICE) { Memoria_Ficheiros.camiño_START(1); 처리값 = Memoria_Ficheiros.camiño_byte(0, '.'); } else 처리값 = ficha_CONTAR == argumento_ÍNDICE + 1 ? CAMIÑO(argumento_ÍNDICE) : -22;
            if (처리값 >= 0) 처리값 = Memoria_Ficheiros.경로목록(); if (처리값 < 0) ERRO(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) shell_Ferramentas.Ficheiro_caso(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) shell_Ferramentas.copiar_VALOR(같음(0, "mv"));
        else if (같음(0, "cat")) shell_Ferramentas.ver_VALOR();
        else if (같음(0, "wc")) shell_Ferramentas.세기();
        else if (같음(0, "grep")) shell_Ferramentas.Busca_introdución();
        else if (같음(0, "head") || 같음(0, "tail")) shell_Ferramentas.머리(같음(0, "tail"));
        else if (같음(0, "tee")) shell_Ferramentas.escribir_Xuntos();
        else if (같음(0, "env")) shell_sintaxe.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (ficha_CONTAR == 1) shell_sintaxe.환경보기();
            for (int Loop_ÍNDICE = 1; Loop_ÍNDICE < ficha_CONTAR; Loop_ÍNDICE++) { int 처리값 = shell_sintaxe.환경설정(Loop_ÍNDICE, 같음(0, "unset")); if (처리값 != 0) { RESULTANTE = 처리값; 단말.Escritura("Orde analizar_VALOR: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) shell_sintaxe.executar_Ficheiro();
        else if (같음(0, "true")) RESULTANTE = 0;
        else if (같음(0, "false")) RESULTANTE = 1;
        else if (같음(0, "history")) liña_Editor.mostrar_LOG();
        else if (같음(0, "exit")) {
            if (shell_sintaxe.깊이 > 0) { RESULTANTE = ficha_CONTAR == 1 ? shell_sintaxe.Estado_VALOR : shell_Ferramentas.díxito_VALOR(1); if (RESULTANTE < 0 || RESULTANTE > 255) RESULTANTE = 2; shell_sintaxe.script_finalizar = true; }
            else if (Panel.Terminal(2) != 0) Terminal(true);
            else 단말.Escritura("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) editar_VALOR();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (ficha_CONTAR < 2) { RESULTANTE = 2; 단말.Escritura("사용법: rm Ficheiro...\n"); }
            for (int Loop_ÍNDICE = 1; Loop_ÍNDICE < ficha_CONTAR; Loop_ÍNDICE++) { int 처리값 = CAMIÑO(Loop_ÍNDICE); if (처리값 == 0) 처리값 = Memoria_Ficheiros.borrar_introdución(); if (처리값 < 0) ERRO(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_cargo = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_cargo; 첫값 < ficha_CONTAR; 첫값++) { if (첫값 > START_cargo) 단말.문자(32); for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < duración_VALOR[첫값]; Loop_ÍNDICE++) Panel.직렬쓰기(ficha_VALOR[시작점[첫값] + Loop_ÍNDICE]); }
            if (START_cargo == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Escritura("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_paquete() : Ferramentas(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); RESULTANTE = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !shell_sintaxe.연결중) { 단말.Escritura("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Ferramentas(13); RESULTANTE = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Ferramentas(15); RESULTANTE = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaxe.연결중) { 단말.Escritura("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Ferramentas(16); RESULTANTE = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaxe.연결중) { 단말.Escritura("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Tamaño = Panel.Terminal(13); 단말.Escritura("TERMINAL SIZE "); 단말.수(Tamaño & 65535); 단말.문자('x'); 단말.수(Tamaño >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Panel.Terminal(9); escritorio.executar_comando(); }
        else if (같음(0, "c")) kernel.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kernel.작업시험();
        else if (같음(0, "g")) kernel.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kernel.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Panel.executar_usuario_apl(0); if (처리값 == 0) 단말.Escritura("ELF DEMO PASS\n"); else ERRO(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? ferramenta_introdución(-2, 2) : Ferramentas(-1); RESULTANTE = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !shell_sintaxe.연결중) { 단말.Escritura("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kernel.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Panel.transferencia_de_ficheiros_servizo(1); if (처리값 < 0) ERRO(처리값); else { 단말.Escritura("FTP listening "); sistema_ferramenta.escribir_ENDEREZO(Panel.Rede_estado(0,0)); 단말.Escritura(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Panel.transferencia_de_ficheiros_servizo(0); 단말.Escritura("FTP stopped\n"); }
            else 단말.Escritura(Panel.transferencia_de_ficheiros_servizo(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { paquete.준비(); 단말.Escritura("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Idioma = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (ficha_CONTAR != 2 || Idioma < 0) 단말.Escritura("example java|c|python: Saída, Ficheiro, 네트워크, 그래픽, Java Swing Xanela 예제\n");
            else { int 처리값 = 예제꾸러미.instalar_VALOR(Idioma); if (처리값 < 0) { ERRO(처리값); if (처리값 == -28) 단말.Escritura("RAM full: remove unused files, then retry example\n"); } else 단말.Escritura("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formato_VALOR = 실행형식();
            if (formato_VALOR == 1 || formato_VALOR == 2) {
                int 처리값 = ferramenta_introdución(formato_VALOR == 1 ? -1 : 14, 0); RESULTANTE = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !shell_sintaxe.연결중) { 단말.Escritura("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (formato_VALOR == 0) { RESULTANTE = 126; 단말.Escritura("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { RESULTANTE = 127; 단말.Escritura("Unknown command. help: commands\n"); }
        }
    }
    public static void executar_comando() {
        paquete.준비();
        for (int Idioma = 0; Idioma < 3; Idioma++) { int 처리값 = 예제꾸러미.instalar_VALOR(Idioma); if (처리값 < 0) ERRO(처리값); }
        mostrar_axuda();
        while (true) {
            ventá_sesión.Proceso_VALOR_introdución(); if (ventá_sesión.재개()) continue;
            if (!ventá_sesión.이어읽기) 단말.Escritura("jkoros-native> "); liña_Editor.liña_de_comandos = true; Panel.remoto_agarda(1); int Tamaño = 줄읽기(); Panel.remoto_agarda(0); liña_Editor.liña_de_comandos = false;
            if (Tamaño == -3) continue;
            if (Tamaño == -2) 단말.Escritura("Orde analizar_VALOR: 명령줄이 너무 깁니다\n");
            if (Tamaño >= 0) { shell_sintaxe.script_finalizar = false; shell_sintaxe.executar_comando(Liña, 0, Tamaño, 0); } else shell_sintaxe.Estado_VALOR = 130;
            Panel.finalizar_remoto_comando(shell_sintaxe.Estado_VALOR);
            liña_Editor.Tamaño = liña_Editor.cursor_VALOR = liña_Editor.START_ventá = 0;
        }
    }
}
