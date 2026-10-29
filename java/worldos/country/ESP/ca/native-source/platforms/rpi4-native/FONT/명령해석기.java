// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 línia_d_ordres. oferta, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] línia = new int[4096], testimoni_VALOR = new int[4096], 시작점 = new int[32], durada_VALOR = new int[32];
    static int[] Editats_Índex = new int[16384], Editar_nom = new int[63];
    static int testimoni_COMPT, Editar_nom_durada, RESULTAT;
    static boolean 앞줄;
    static void 원바이트(int VALOR) { Tauler.직렬쓰기(VALOR); }
    static int 줄읽기() { return línia_Editor.Lectura(); }
    static boolean 나누기(int Mida) {
        int Posició = 0, 끝 = 0; testimoni_COMPT = 0;
        while (Posició < Mida) {
            while (Posició < Mida && (línia[Posició] == 32 || línia[Posició] == 9)) Posició++;
            if (Posició == Mida) break;
            if (testimoni_COMPT == 16) { 단말.Escriptura("Ordre analitzar_VALOR: 인수가 너무 많습니다\n"); return false; }
            시작점[testimoni_COMPT] = 끝; int oferta_VALOR = 0;
            while (Posició < Mida) {
                int VALOR = línia[Posició++];
                if (oferta_VALOR == 0 && (VALOR == 32 || VALOR == 9)) break;
                if (VALOR == oferta_VALOR) { oferta_VALOR = 0; continue; }
                if (oferta_VALOR == 0 && (VALOR == 39 || VALOR == 34)) { oferta_VALOR = VALOR; continue; }
                testimoni_VALOR[끝++] = VALOR;
            }
            if (oferta_VALOR != 0) { 단말.Escriptura("Ordre analitzar_VALOR: 따옴표가 닫히지 않았습니다\n"); return false; }
            durada_VALOR[testimoni_COMPT] = 끝 - 시작점[testimoni_COMPT]; testimoni_COMPT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= testimoni_COMPT) return false;
        int càrrec_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int codi_de_caràcter=Word_SMS.charAt(순번);
            if (codi_de_caràcter>=0xd800 && codi_de_caràcter<=0xdbff && 순번+1<Word_SMS.length()) codi_de_caràcter=0x10000+((codi_de_caràcter-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int byte_COMPT=codi_de_caràcter<128?1:codi_de_caràcter<2048?2:codi_de_caràcter<65536?3:4;
            for (int SEQÜÈNCIA_VALOR=byte_COMPT-1; SEQÜÈNCIA_VALOR>=0; SEQÜÈNCIA_VALOR--) {
                int VALOR=byte_COMPT==1?codi_de_caràcter:SEQÜÈNCIA_VALOR==byte_COMPT-1?(byte_COMPT==2?0xc0:byte_COMPT==3?0xe0:0xf0)|(codi_de_caràcter>>(6*SEQÜÈNCIA_VALOR)):0x80|((codi_de_caràcter>>(6*SEQÜÈNCIA_VALOR))&63);
                if (càrrec_INDEX>=durada_VALOR[INDEX] || testimoni_VALOR[시작점[INDEX]+càrrec_INDEX++]!=VALOR) return false;
            }
        }
        return càrrec_INDEX==durada_VALOR[INDEX];
    }
    static int Camí(int INDEX) {
        if (INDEX >= testimoni_COMPT) return -22;
        int RESULTAT = Memòria_Fitxers.camí_Inici(durada_VALOR[INDEX]); if (RESULTAT < 0) return RESULTAT;
        for (int Loop_INDEX = 0; Loop_INDEX < durada_VALOR[INDEX]; Loop_INDEX++) {
            RESULTAT = Memòria_Fitxers.camí_byte(Loop_INDEX, testimoni_VALOR[시작점[INDEX] + Loop_INDEX]); if (RESULTAT < 0) return RESULTAT;
        }
        return 0;
    }
    static void s_ha_produït_un_error(int INDEX) { RESULTAT = 1; 단말.Escriptura("s_ha_produït_un_error "); 단말.수(INDEX); 단말.문자(10); }
    static void visualitzar_VALOR() {
        if (testimoni_COMPT != 2) { 단말.Escriptura("사용법: cat Fitxer\n"); return; }
        int RESULTAT = Camí(1); if (RESULTAT < 0) { s_ha_produït_un_error(RESULTAT); return; }
        int Fitxer = Memòria_Fitxers.Obre(0); if (Fitxer < 0) { s_ha_produït_un_error(Fitxer); return; }
        while (true) { int VALOR = Memòria_Fitxers.Lectura(Fitxer); if (VALOR == 256) break; if (VALOR < 0) { s_ha_produït_un_error(VALOR); break; } 원바이트(VALOR); }
        Memòria_Fitxers.Tanca(Fitxer); 단말.문자(10);
    }
    static void Editar_VALOR() {
        if (testimoni_COMPT != 2) { 단말.Escriptura("사용법: edit Fitxer\n"); return; }
        int RESULTAT = Camí(1); if (RESULTAT < 0) { s_ha_produït_un_error(RESULTAT); return; }
        Editar_nom_durada = durada_VALOR[1];
        for (int Loop_INDEX = 0; Loop_INDEX < Editar_nom_durada; Loop_INDEX++) Editar_nom[Loop_INDEX] = testimoni_VALOR[시작점[1] + Loop_INDEX];
        단말.Escriptura("EDIT: Fitxer 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Mida = 0;
        while (true) {
            단말.Escriptura("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Escriptura("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && línia[0] == '.') break;
            if (입력 + 1 > Editats_Índex.length - Mida) { 단말.Escriptura("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Editats_Índex[Mida++] = línia[Loop_INDEX];
            Editats_Índex[Mida++] = 10;
        }
        Memòria_Fitxers.camí_Inici(Editar_nom_durada);
        for (int Loop_INDEX = 0; Loop_INDEX < Editar_nom_durada; Loop_INDEX++) Memòria_Fitxers.camí_byte(Loop_INDEX, Editar_nom[Loop_INDEX]);
        int Fitxer = Memòria_Fitxers.Obre(577); if (Fitxer < 0) { s_ha_produït_un_error(Fitxer); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Mida; Loop_INDEX++) Memòria_Fitxers.Escriptura(Fitxer, Editats_Índex[Loop_INDEX]);
        Memòria_Fitxers.Tanca(Fitxer); 단말.Escriptura("SAVED "); 단말.수(Mida); 단말.Escriptura("byte_VALOR(주기억 Fitxer)\n");
    }
    static int hexadecimal_VALOR(int VALOR) {
        if (VALOR >= '0' && VALOR <= '9') return VALOR - '0';
        if (VALOR >= 'a' && VALOR <= 'f') return VALOR - 'a' + 10;
        if (VALOR >= 'A' && VALOR <= 'F') return VALOR - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (testimoni_COMPT != 2) { 단말.Escriptura("사용법: load Fitxer | hex Fitxer\n"); return; }
        int RESULTAT = Camí(1); if (RESULTAT < 0) { s_ha_produït_un_error(RESULTAT); return; }
        if (!넣기) {
            int Fitxer = Memòria_Fitxers.Obre(0); if (Fitxer < 0) { s_ha_produït_un_error(Fitxer); return; }
            단말.Escriptura("HEX BEGIN "); 단말.수(Memòria_Fitxers.Mida(Fitxer)); 단말.문자(10);
            int introducció_COMPT = 0;
            while (true) {
                int VALOR = Memòria_Fitxers.Lectura(Fitxer); if (VALOR < 0 || VALOR == 256) break;
                단말.문자("0123456789abcdef".charAt(VALOR >> 4)); 단말.문자("0123456789abcdef".charAt(VALOR & 15));
                if (++introducció_COMPT % 32 == 0) 단말.문자(10);
            }
            if (introducció_COMPT % 32 != 0) 단말.문자(10);
            Memòria_Fitxers.Tanca(Fitxer); 단말.Escriptura("HEX END\n"); return;
        }
        Editar_nom_durada = durada_VALOR[1];
        for (int Loop_INDEX = 0; Loop_INDEX < Editar_nom_durada; Loop_INDEX++) Editar_nom[Loop_INDEX] = testimoni_VALOR[시작점[1] + Loop_INDEX];
        단말.Escriptura("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Mida = 0;
        while (true) {
            단말.Escriptura("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Escriptura("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && línia[0] == '.') break;
            int frontal_VALOR = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (línia[Loop_INDEX] == 32 || línia[Loop_INDEX] == 9) continue;
                int VALOR = hexadecimal_VALOR(línia[Loop_INDEX]);
                if (VALOR < 0 || Mida >= Editats_Índex.length) { 단말.Escriptura("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (frontal_VALOR < 0) frontal_VALOR = VALOR; else { Editats_Índex[Mida++] = frontal_VALOR * 16 + VALOR; frontal_VALOR = -1; }
            }
            if (frontal_VALOR >= 0) { 단말.Escriptura("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memòria_Fitxers.camí_Inici(Editar_nom_durada);
        for (int Loop_INDEX = 0; Loop_INDEX < Editar_nom_durada; Loop_INDEX++) Memòria_Fitxers.camí_byte(Loop_INDEX, Editar_nom[Loop_INDEX]);
        int Fitxer = Memòria_Fitxers.Obre(577); if (Fitxer < 0) { s_ha_produït_un_error(Fitxer); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Mida; Loop_INDEX++) Memòria_Fitxers.Escriptura(Fitxer, Editats_Índex[Loop_INDEX]);
        Memòria_Fitxers.Tanca(Fitxer); 단말.Escriptura("LOADED "); 단말.수(Mida); 단말.Escriptura("byte_VALOR(주기억 Fitxer)\n");
    }
    static int Eines(int INDEX) {
        return eina_introducció(INDEX, 1);
    }
    static int eina_introducció(int INDEX, int Executa_2) {
        if (testimoni_COMPT - Executa_2 > 8) return -22;
        Tauler.인수준비(testimoni_COMPT - Executa_2);
        for (int 첫값 = Executa_2; 첫값 < testimoni_COMPT; 첫값++) {
            if (durada_VALOR[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < durada_VALOR[첫값]; Loop_INDEX++) Tauler.arg_byte(첫값 - Executa_2, Loop_INDEX, testimoni_VALOR[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Tauler.리눅스파일실행() : INDEX < 0 ? Tauler.Executa_usuari_arxiu() : Tauler.execució_usuari_programa(INDEX);
    }
    static int PYTHON_paquet() {
        if (testimoni_COMPT > 8) return -22;
        Tauler.인수준비(testimoni_COMPT);
        String Camí = "/lib/paquet.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int càrrec_INDEX = 0;
        for (int 순번 = 0; 순번 < Camí.length(); 순번++) {
            int caràcter_VALOR = Camí.charAt(순번);
            if (caràcter_VALOR < 128) Tauler.arg_byte(0, càrrec_INDEX++, caràcter_VALOR);
            else { Tauler.arg_byte(0, càrrec_INDEX++, 0xe0 | (caràcter_VALOR >> 12)); Tauler.arg_byte(0, càrrec_INDEX++, 0x80 | ((caràcter_VALOR >> 6) & 63)); Tauler.arg_byte(0, càrrec_INDEX++, 0x80 | (caràcter_VALOR & 63)); }
        }
        for (int 순번 = 1; 순번 < testimoni_COMPT; 순번++) {
            if (durada_VALOR[순번] > 255) return -36;
            for (int caràcter_VALOR = 0; caràcter_VALOR < durada_VALOR[순번]; caràcter_VALOR++) Tauler.arg_byte(순번, caràcter_VALOR, testimoni_VALOR[시작점[순번] + caràcter_VALOR]);
        }
        return Tauler.execució_usuari_programa(12);
    }
    static int 실행형식() {
        int 처리값 = Camí(0); if (처리값 < 0) return 처리값;
        int Fitxer = Memòria_Fitxers.Obre(0); if (Fitxer < 0) return Fitxer;
        int 첫값 = Memòria_Fitxers.Lectura(Fitxer), byte_dades = Memòria_Fitxers.Lectura(Fitxer), codi_de_caràcter = Memòria_Fitxers.Lectura(Fitxer), 뒷값 = Memòria_Fitxers.Lectura(Fitxer);
        Memòria_Fitxers.Tanca(Fitxer);
        if (첫값 == 127 && byte_dades == 'E' && codi_de_caràcter == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_dades == 'K' && codi_de_caràcter == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        Tauler.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) Tauler.arg_byte(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return Tauler.execució_usuari_programa(INDEX);
    }
    static void SMS_byte(int Fitxer, int VALOR) { Memòria_Fitxers.Escriptura(Fitxer, VALOR); }
    static void estàtic_arxiu(String Nom, String contingut_VALOR) {
        // paquet 파일명은 ASCII. Fitxer 내용은 UTF-8로 저장한다.
        Memòria_Fitxers.camí_Inici(Nom.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Nom.length(); Loop_INDEX++) Memòria_Fitxers.camí_byte(Loop_INDEX, Nom.charAt(Loop_INDEX));
        int Fitxer = Memòria_Fitxers.Obre(193); if (Fitxer < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < contingut_VALOR.length(); Loop_INDEX++) {
            int codi_de_caràcter = contingut_VALOR.charAt(Loop_INDEX);
            if (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdbff && Loop_INDEX + 1 < contingut_VALOR.length()) codi_de_caràcter = 0x10000 + ((codi_de_caràcter - 0xd800) << 10) + contingut_VALOR.charAt(++Loop_INDEX) - 0xdc00;
            if (codi_de_caràcter < 128) SMS_byte(Fitxer, codi_de_caràcter);
            else {
                int 수 = codi_de_caràcter < 2048 ? 2 : codi_de_caràcter < 65536 ? 3 : 4;
                SMS_byte(Fitxer, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (codi_de_caràcter >> (6 * (수 - 1))));
                for (int introducció_COMPT = 수 - 1; introducció_COMPT > 0; introducció_COMPT--) SMS_byte(Fitxer, 0x80 | ((codi_de_caràcter >> (6 * (introducció_COMPT - 1))) & 63));
            }
        }
        Memòria_Fitxers.Tanca(Fitxer);
    }
    static void 한글도움말() {
        단말.Escriptura("F9 / Shift+Space: [EN] ↔ [ca]\n");
        단말.Escriptura("  [CA] keyboard; [EN] ASCII\n");
        단말.Escriptura("  # → ·\n");
        단말.Escriptura("  F9: EN ↔ ca | Ctrl+Shift+V: UTF-8\n");
        단말.Escriptura("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Escriptura("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nom) {
        int byte_COMPT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nom.length(); Loop_INDEX++) { int codi_de_caràcter = Nom.charAt(Loop_INDEX); if (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdfff) return -22; byte_COMPT += codi_de_caràcter < 128 ? 1 : codi_de_caràcter < 2048 ? 2 : 3; }
        int 처리값 = Memòria_Fitxers.camí_Inici(byte_COMPT); if (처리값 < 0) return 처리값;
        int càrrec_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nom.length(); Loop_INDEX++) {
            int codi_de_caràcter = Nom.charAt(Loop_INDEX);
            if (codi_de_caràcter < 128) Memòria_Fitxers.camí_byte(càrrec_INDEX++, codi_de_caràcter);
            else if (codi_de_caràcter < 2048) { Memòria_Fitxers.camí_byte(càrrec_INDEX++, 0xc0 | (codi_de_caràcter >> 6)); Memòria_Fitxers.camí_byte(càrrec_INDEX++, 0x80 | (codi_de_caràcter & 63)); }
            else { Memòria_Fitxers.camí_byte(càrrec_INDEX++, 0xe0 | (codi_de_caràcter >> 12)); Memòria_Fitxers.camí_byte(càrrec_INDEX++, 0x80 | ((codi_de_caràcter >> 6) & 63)); Memòria_Fitxers.camí_byte(càrrec_INDEX++, 0x80 | (codi_de_caràcter & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nom) {
        int 처리값 = 예제경로(Nom); if (처리값 < 0) return 처리값;
        처리값 = Memòria_Fitxers.Crear_directori(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nom, String dades) {
        int 처리값 = 예제경로(Nom); if (처리값 < 0) return 처리값;
        int Fitxer = Memòria_Fitxers.Obre(193); if (Fitxer == -17) return 0; if (Fitxer < 0) return Fitxer;
        for (int Loop_INDEX = 0; Loop_INDEX < dades.length(); Loop_INDEX += 2) {
            처리값 = Memòria_Fitxers.Escriptura(Fitxer, hexadecimal_VALOR(dades.charAt(Loop_INDEX)) * 16 + hexadecimal_VALOR(dades.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Memòria_Fitxers.Tanca(Fitxer); return 처리값; }
        }
        return Memòria_Fitxers.Tanca(Fitxer);
    }
    static void mostrar_ajuda() {
        sistema_eina.mostrar_ajuda();
        단말.Escriptura("sshd / segur_shell start|stop|status: SSH :22 (user, 장치별 contrasenya_VALOR)\n");
        단말.Escriptura("vncd / remot_mostrar start|stop|status: VNC :5900 (장치별 contrasenya_VALOR)\n");
        단말.Escriptura("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Escriptura("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Escriptura("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Escriptura("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Escriptura("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Escriptura("모서리 + 왼쪽 버튼 arrossegar_VALOR: Terminal Mida canviar_VALOR; terminal size: COLUMNA_VALOR/FILA_VALOR\n");
        단말.Escriptura("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Escriptura("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Escriptura("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Escriptura("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Escriptura("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Escriptura("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Escriptura("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Escriptura("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Escriptura("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Escriptura("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Escriptura("pip: MicroPython font_arbre instal_lar_VALOR; allotjar --network --pip 필요; /lib는 RAM\n");
        단말.Escriptura("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Escriptura("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Escriptura("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Escriptura("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && Tauler.Terminal(2) != 0) { Tauler.Terminal(0); 단말.Escriptura("TERMINAL CLOSED\n"); }
        else if (Tauler.Terminal(1) < 0) s_ha_produït_un_error(-19);
        else 단말.Escriptura("TERMINAL READY — ca terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Ordre() {
        if (testimoni_COMPT == 0) return;
        if (sistema_eina.Executa_ordre()) return;
        if (같음(0,"sshd") || 같음(0,"segur_shell") || 같음(0,"vncd") || 같음(0,"remot_mostrar")) {
            int 종류=같음(0,"vncd")||같음(0,"remot_mostrar")?1:0;
            int Acció=같음(1,"start")||같음(1,"Executa_2")?1:같음(1,"stop")||같음(1,"Atura")?0:2;
            int Estat_VALOR=Tauler.vigilància(종류,Acció);
            if(Estat_VALOR<0)s_ha_produït_un_error(Estat_VALOR);else 단말.Escriptura(Tauler.vigilància(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else mostrar_ajuda(); }
        else if (같음(0, "info") || 같음(0, "i")) nucli.msinfo32_exe();
        else if (같음(0, "pwd")) { Memòria_Fitxers.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (testimoni_COMPT == 1) { Memòria_Fitxers.camí_Inici(1); 처리값 = Memòria_Fitxers.camí_byte(0, '/'); } else 처리값 = testimoni_COMPT == 2 ? Camí(1) : -22;
            if (처리값 >= 0) 처리값 = Memòria_Fitxers.canviar_directori(); if (처리값 < 0) s_ha_produït_un_error(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int arg_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (testimoni_COMPT == arg_INDEX) { Memòria_Fitxers.camí_Inici(1); 처리값 = Memòria_Fitxers.camí_byte(0, '.'); } else 처리값 = testimoni_COMPT == arg_INDEX + 1 ? Camí(arg_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Memòria_Fitxers.경로목록(); if (처리값 < 0) s_ha_produït_un_error(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) shell_Eines.arxiu_cas(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) shell_Eines.copiar_VALOR(같음(0, "mv"));
        else if (같음(0, "cat")) shell_Eines.visualitzar_VALOR();
        else if (같음(0, "wc")) shell_Eines.세기();
        else if (같음(0, "grep")) shell_Eines.BUSCA_introducció();
        else if (같음(0, "head") || 같음(0, "tail")) shell_Eines.머리(같음(0, "tail"));
        else if (같음(0, "tee")) shell_Eines.escriure_Junts();
        else if (같음(0, "env")) shell_sintaxi.mostrar_entorn();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (testimoni_COMPT == 1) shell_sintaxi.mostrar_entorn();
            for (int Loop_INDEX = 1; Loop_INDEX < testimoni_COMPT; Loop_INDEX++) { int 처리값 = shell_sintaxi.entorn_Configuració(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { RESULTAT = 처리값; 단말.Escriptura("Ordre analitzar_VALOR: 변수 이름이 잘못되었거나 예약된 이름이거나 entorn 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) shell_sintaxi.Executa_arxiu();
        else if (같음(0, "true")) RESULTAT = 0;
        else if (같음(0, "false")) RESULTAT = 1;
        else if (같음(0, "history")) línia_Editor.mostrar_LOG();
        else if (같음(0, "exit")) {
            if (shell_sintaxi.깊이 > 0) { RESULTAT = testimoni_COMPT == 1 ? shell_sintaxi.Estat_VALOR : shell_Eines.dígit_VALOR(1); if (RESULTAT < 0 || RESULTAT > 255) RESULTAT = 2; shell_sintaxi.script_finalitzar = true; }
            else if (Tauler.Terminal(2) != 0) Terminal(true);
            else 단말.Escriptura("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Editar_VALOR();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (testimoni_COMPT < 2) { RESULTAT = 2; 단말.Escriptura("사용법: rm Fitxer...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < testimoni_COMPT; Loop_INDEX++) { int 처리값 = Camí(Loop_INDEX); if (처리값 == 0) 처리값 = Memòria_Fitxers.esborrar_introducció(); if (처리값 < 0) s_ha_produït_un_error(처리값); }
        }
        else if (같음(0, "echo")) {
            int Inici_càrrec = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Inici_càrrec; 첫값 < testimoni_COMPT; 첫값++) { if (첫값 > Inici_càrrec) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < durada_VALOR[첫값]; Loop_INDEX++) Tauler.직렬쓰기(testimoni_VALOR[시작점[첫값] + Loop_INDEX]); }
            if (Inici_càrrec == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Escriptura("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_paquet() : Eines(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); RESULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !shell_sintaxi.연결중) { 단말.Escriptura("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Eines(13); RESULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Eines(15); RESULTAT = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaxi.연결중) { 단말.Escriptura("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Eines(16); RESULTAT = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaxi.연결중) { 단말.Escriptura("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Mida = Tauler.Terminal(13); 단말.Escriptura("TERMINAL SIZE "); 단말.수(Mida & 65535); 단말.문자('x'); 단말.수(Mida >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Tauler.Terminal(9); escriptori.Executa_ordre(); }
        else if (같음(0, "c")) nucli.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) nucli.작업시험();
        else if (같음(0, "g")) nucli.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) nucli.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Tauler.execució_usuari_programa(0); if (처리값 == 0) 단말.Escriptura("ELF DEMO PASS\n"); else s_ha_produït_un_error(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? eina_introducció(-2, 2) : Eines(-1); RESULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !shell_sintaxi.연결중) { 단말.Escriptura("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) nucli.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Tauler.transferència_de_fitxers_servei(1); if (처리값 < 0) s_ha_produït_un_error(처리값); else { 단말.Escriptura("FTP listening "); sistema_eina.escriure_ADREÇA(Tauler.xarxa_estat(0,0)); 단말.Escriptura(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Tauler.transferència_de_fitxers_servei(0); 단말.Escriptura("FTP stopped\n"); }
            else 단말.Escriptura(Tauler.transferència_de_fitxers_servei(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { paquet.Prepara(); 단말.Escriptura("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Idioma = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (testimoni_COMPT != 2 || Idioma < 0) 단말.Escriptura("example java|c|python: Sortida, Fitxer, 네트워크, 그래픽, Java Swing Finestra 예제\n");
            else { int 처리값 = 예제꾸러미.instal_lar_VALOR(Idioma); if (처리값 < 0) { s_ha_produït_un_error(처리값); if (처리값 == -28) 단말.Escriptura("RAM full: remove unused files, then retry example\n"); } else 단말.Escriptura("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALOR = 실행형식();
            if (format_VALOR == 1 || format_VALOR == 2) {
                int 처리값 = eina_introducció(format_VALOR == 1 ? -1 : 14, 0); RESULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !shell_sintaxi.연결중) { 단말.Escriptura("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALOR == 0) { RESULTAT = 126; 단말.Escriptura("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { RESULTAT = 127; 단말.Escriptura("Unknown command. help: commands\n"); }
        }
    }
    public static void Executa_ordre() {
        paquet.Prepara();
        for (int Idioma = 0; Idioma < 3; Idioma++) { int 처리값 = 예제꾸러미.instal_lar_VALOR(Idioma); if (처리값 < 0) s_ha_produït_un_error(처리값); }
        mostrar_ajuda();
        while (true) {
            finestra_sessió.Procés_VALOR_introducció(); if (finestra_sessió.재개()) continue;
            if (!finestra_sessió.이어읽기) 단말.Escriptura("jkoros-native> "); línia_Editor.línia_d_ordres = true; Tauler.remot_Espera(1); int Mida = 줄읽기(); Tauler.remot_Espera(0); línia_Editor.línia_d_ordres = false;
            if (Mida == -3) continue;
            if (Mida == -2) 단말.Escriptura("Ordre analitzar_VALOR: 명령줄이 너무 깁니다\n");
            if (Mida >= 0) { shell_sintaxi.script_finalitzar = false; shell_sintaxi.Executa_ordre(línia, 0, Mida, 0); } else shell_sintaxi.Estat_VALOR = 130;
            Tauler.finalitzar_remot_ordre(shell_sintaxi.Estat_VALOR);
            línia_Editor.Mida = línia_Editor.cursor_VALOR = línia_Editor.Inici_finestra = 0;
        }
    }
}
