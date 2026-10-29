// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VALOR 경계를 지키는 삽입/삭제, 방향키, Orde LOG_fila, Tab Completadas_VALOR. */
public final class liña_Editor {
    static boolean liña_de_comandos;
    static int[] LOG_fila = new int[16 * 1024], LOG_duración = new int[16], Store_VALOR = new int[4096], 후보 = new int[64];
    static int LOG_CONTAR, LOG_fila_finalizar, ACHAR_VALOR, 저장길이, Tamaño, cursor_VALOR, 후보수, 후보길이, START_ventá;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd seguro_shell remoto_mostrar run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String introdución_Lista, int START_cargo, int finalizar_cargo, int 입력길이) {
        int byte_CONTAR=0;
        for(int cargo_ÍNDICE=START_cargo;cargo_ÍNDICE<finalizar_cargo;cargo_ÍNDICE++) {
            int código_de_carácter=introdución_Lista.charAt(cargo_ÍNDICE);
            if(código_de_carácter>=0xd800 && código_de_carácter<=0xdbff && cargo_ÍNDICE+1<finalizar_cargo)código_de_carácter=0x10000+((código_de_carácter-0xd800)<<10)+introdución_Lista.charAt(++cargo_ÍNDICE)-0xdc00;
            int 수=código_de_carácter<128?1:código_de_carácter<2048?2:código_de_carácter<65536?3:4;
            if(byte_CONTAR+수>62)return;
            for(int SECUENCIA_VALOR=수-1;SECUENCIA_VALOR>=0;SECUENCIA_VALOR--)명령후보[byte_CONTAR++]=수==1?código_de_carácter:SECUENCIA_VALOR==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(código_de_carácter>>(6*SECUENCIA_VALOR)):0x80|((código_de_carácter>>(6*SECUENCIA_VALOR))&63);
        }
        if(byte_CONTAR<입력길이)return;
        for(int cargo_ÍNDICE=0;cargo_ÍNDICE<입력길이;cargo_ÍNDICE++)if(명령후보[cargo_ÍNDICE]!=명령해석기.Liña[cargo_ÍNDICE])return;
        후보수++;후보길이=byte_CONTAR+1;
        for(int cargo_ÍNDICE=0;cargo_ÍNDICE<byte_CONTAR;cargo_ÍNDICE++)후보[cargo_ÍNDICE]=명령후보[cargo_ÍNDICE];후보[byte_CONTAR]=' ';
    }
    static int frontal_VALOR(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Liña[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int ATRÁS_VALOR(int 읽는자리) { if (읽는자리 < Tamaño) { 읽는자리++; while (읽는자리 < Tamaño && (명령해석기.Liña[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_cargo, int destino_VALOR_ÍNDICE) {
        int 글칸수 = 0;
        for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < destino_VALOR_ÍNDICE; Loop_ÍNDICE++) { int byte_datos = 명령해석기.Liña[Loop_ÍNDICE]; if ((byte_datos & 192) == 128) continue; 글칸수 += byte_datos >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Escritura("\r\u001b[2K");
        단말.Escritura(liña_de_comandos ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Liña 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNAS = Panel.Terminal(13) & 65535; return COLUMNAS - (liña_de_comandos ? 18 : 9); }
    static void 보이는줄() {
        if (cursor_VALOR < START_ventá) START_ventá = cursor_VALOR;
        while (폭(START_ventá, cursor_VALOR) > 보이는폭()) START_ventá = ATRÁS_VALOR(START_ventá);
        int finalizar_cargo = START_ventá;
        while (finalizar_cargo < Tamaño && 폭(START_ventá, ATRÁS_VALOR(finalizar_cargo)) <= 보이는폭()) finalizar_cargo = ATRÁS_VALOR(finalizar_cargo);
        단말.Escritura("\r\u001b["); 단말.수(liña_de_comandos ? 16 : 7); 단말.Escritura("G\u001b[K");
        if (START_ventá > 0) 단말.문자('<');
        for (int Loop_ÍNDICE = START_ventá; Loop_ÍNDICE < finalizar_cargo; Loop_ÍNDICE++) Panel.직렬쓰기(명령해석기.Liña[Loop_ÍNDICE]);
        단말.문자(finalizar_cargo < Tamaño ? '>' : ' ');
        단말.Escritura("\u001b["); 단말.수(폭(cursor_VALOR, finalizar_cargo) + 1); 단말.문자('D');
        가로보기 = START_ventá > 0 || finalizar_cargo < Tamaño || 폭(0, Tamaño) > 보이는폭();
    }
    static void Anexar_LOG() {
        if (!liña_de_comandos || Tamaño == 0 || Tamaño > 1024) return;
        if (LOG_CONTAR > 0) {
            int 마지막자리 = (LOG_fila_finalizar + 15) % 16; boolean 같은여부 = LOG_duración[마지막자리] == Tamaño;
            for (int Loop_ÍNDICE = 0; 같은여부 && Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) if (LOG_fila[마지막자리 * 1024 + Loop_ÍNDICE] != 명령해석기.Liña[Loop_ÍNDICE]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_duración[LOG_fila_finalizar] = Tamaño; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) LOG_fila[LOG_fila_finalizar * 1024 + Loop_ÍNDICE] = 명령해석기.Liña[Loop_ÍNDICE];
        LOG_fila_finalizar = (LOG_fila_finalizar + 1) % 16; if (LOG_CONTAR < 16) LOG_CONTAR++;
    }
    static void 기록이동(int DELTA_VALOR) {
        if (!liña_de_comandos) return;
        if (ACHAR_VALOR == 0 && DELTA_VALOR > 0) { 저장길이 = Tamaño; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) Store_VALOR[Loop_ÍNDICE] = 명령해석기.Liña[Loop_ÍNDICE]; }
        int Seguinte_cargo = ACHAR_VALOR + DELTA_VALOR; if (Seguinte_cargo < 0 || Seguinte_cargo > LOG_CONTAR) return; ACHAR_VALOR = Seguinte_cargo;
        if (ACHAR_VALOR == 0) { Tamaño = 저장길이; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) 명령해석기.Liña[Loop_ÍNDICE] = Store_VALOR[Loop_ÍNDICE]; }
        else { int 보관칸 = (LOG_fila_finalizar + 16 - ACHAR_VALOR) % 16; Tamaño = LOG_duración[보관칸]; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) 명령해석기.Liña[Loop_ÍNDICE] = LOG_fila[보관칸 * 1024 + Loop_ÍNDICE]; }
        cursor_VALOR = Tamaño; 다시();
    }
    static void mostrar_LOG() {
        for (int introdución_CONTAR = 0; introdución_CONTAR < LOG_CONTAR; introdución_CONTAR++) {
            int 보관칸 = (LOG_fila_finalizar + 16 - LOG_CONTAR + introdución_CONTAR) % 16; 단말.수(introdución_CONTAR + 1); 단말.Escritura("  ");
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < LOG_duración[보관칸]; Loop_ÍNDICE++) Panel.직렬쓰기(LOG_fila[보관칸 * 1024 + Loop_ÍNDICE]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] datos_MATRIZ, int START_cargo, int introdución_CONTAR, int 접두말, int 총수, boolean 폴더번호) {
        if (introdución_CONTAR < 총수 || introdución_CONTAR > 62) return;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 총수; Loop_ÍNDICE++) if (datos_MATRIZ[START_cargo + Loop_ÍNDICE] != 명령해석기.Liña[접두말 + Loop_ÍNDICE]) return;
        후보수++; 후보길이 = introdución_CONTAR + 1;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) 후보[Loop_ÍNDICE] = datos_MATRIZ[START_cargo + Loop_ÍNDICE]; 후보[introdución_CONTAR] = 폴더번호 ? '/' : ' ';
    }
    static void Completadas_VALOR() {
        if (!liña_de_comandos || cursor_VALOR != Tamaño) return;
        int 시작점 = Tamaño; while (시작점 > 0 && 명령해석기.Liña[시작점 - 1] != ' ') 시작점--;
        for (int Loop_ÍNDICE = 시작점; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) if (명령해석기.Liña[Loop_ÍNDICE] == '/' || 명령해석기.Liña[Loop_ÍNDICE] == '"' || 명령해석기.Liña[Loop_ÍNDICE] == 39 || 명령해석기.Liña[Loop_ÍNDICE] == '\\') return;
        후보수 = 0; int introdución_CONTAR = Tamaño - 시작점;
        if (시작점 == 0) {
            for(int Lista_ÍNDICE=0;Lista_ÍNDICE<2;Lista_ÍNDICE++) {
                String introdución_Lista=Lista_ÍNDICE==0?명령들:관리명령.Completadas_Word();
                int 읽는자리=0;
                while(읽는자리<introdución_Lista.length()) {
                    int finalizar_cargo=읽는자리;while(finalizar_cargo<introdución_Lista.length() && introdución_Lista.charAt(finalizar_cargo)!=' ')finalizar_cargo++;
                    명령후보넣기(introdución_Lista,읽는자리,finalizar_cargo,introdución_CONTAR);읽는자리=finalizar_cargo+1;
                }
            }
        } else {
            Memoria_Ficheiros.camiño_START(1); Memoria_Ficheiros.camiño_byte(0, '.'); Memoria_Ficheiros.organizar_VALOR();
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Memoria_Ficheiros.Ficheiro_CONTAR; Loop_ÍNDICE++) {
                int START_cargo = Memoria_Ficheiros.introdución_START(Memoria_Ficheiros.Nome, Loop_ÍNDICE * 64, Memoria_Ficheiros.이름길이[Loop_ÍNDICE]);
                if (START_cargo >= 0) 후보넣기(Memoria_Ficheiros.Nome, Loop_ÍNDICE * 64 + START_cargo, Memoria_Ficheiros.이름길이[Loop_ÍNDICE] - START_cargo, 시작점, introdución_CONTAR, false);
            }
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) {
                int START_cargo = Memoria_Ficheiros.introdución_START(Memoria_Ficheiros.directorio_nome, Loop_ÍNDICE * 64, Memoria_Ficheiros.directorio_duración[Loop_ÍNDICE]);
                if (START_cargo >= 0) 후보넣기(Memoria_Ficheiros.directorio_nome, Loop_ÍNDICE * 64 + START_cargo, Memoria_Ficheiros.directorio_duración[Loop_ÍNDICE] - START_cargo, 시작점, introdución_CONTAR, true);
            }
        }
        if (후보수 != 1) { Panel.직렬쓰기(7); return; }
        for (int Loop_ÍNDICE = introdución_CONTAR; Loop_ÍNDICE < 후보길이 && Tamaño < 명령해석기.Liña.length - 1; Loop_ÍNDICE++) {
            if (후보[Loop_ÍNDICE] == ' ' && Loop_ÍNDICE != 후보길이 - 1) 명령해석기.Liña[Tamaño++] = '\\';
            명령해석기.Liña[Tamaño++] = 후보[Loop_ÍNDICE];
        }
        cursor_VALOR = Tamaño; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = Panel.밀리초();
        while (Panel.밀리초() - 시작점 < 80) { int byte_datos = Panel.직렬읽기(); if (byte_datos >= 0) return byte_datos; Panel.suspender_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int introdución_CONTAR = 0, finalizar_cargo = -1;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 12; Loop_ÍNDICE++) { int byte_datos = 탈출읽기(); if (byte_datos < 0) return; if (byte_datos >= '0' && byte_datos <= '9') introdución_CONTAR = introdución_CONTAR * 10 + byte_datos - '0'; else { finalizar_cargo = byte_datos; break; } }
        if (finalizar_cargo == 'A') 기록이동(1);
        else if (finalizar_cargo == 'B') 기록이동(-1);
        else if (finalizar_cargo == 'C') { cursor_VALOR = ATRÁS_VALOR(cursor_VALOR); 다시(); }
        else if (finalizar_cargo == 'D') { cursor_VALOR = frontal_VALOR(cursor_VALOR); 다시(); }
        else if (finalizar_cargo == 'H' || finalizar_cargo == '~' && (introdución_CONTAR == 1 || introdución_CONTAR == 7)) { cursor_VALOR = 0; 다시(); }
        else if (finalizar_cargo == 'F' || finalizar_cargo == '~' && (introdución_CONTAR == 4 || introdución_CONTAR == 8)) { cursor_VALOR = Tamaño; 다시(); }
        else if (finalizar_cargo == '~' && introdución_CONTAR == 3 && cursor_VALOR < Tamaño) {
            int Seguinte_cargo = ATRÁS_VALOR(cursor_VALOR); for (int Loop_ÍNDICE = Seguinte_cargo; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) 명령해석기.Liña[Loop_ÍNDICE - Seguinte_cargo + cursor_VALOR] = 명령해석기.Liña[Loop_ÍNDICE]; Tamaño -= Seguinte_cargo - cursor_VALOR; 다시();
        }
        else if (finalizar_cargo == '~' && (introdución_CONTAR == 5 || introdución_CONTAR == 6)) Panel.Terminal(introdución_CONTAR == 5 ? 5 : 6);
        else if (finalizar_cargo == '~' && introdución_CONTAR == 24 && liña_de_comandos) { 명령해석기.Terminal(true); }
    }
    static int Lectura() {
        if (!ventá_sesión.이어읽기) { Tamaño = cursor_VALOR = ACHAR_VALOR = START_ventá = 0; 가로보기 = false; }
        else { ventá_sesión.이어읽기 = false; 다시(); } boolean 넘침여부 = false;
        while (true) {
            int byte_datos = Panel.직렬읽기(); if (byte_datos == -4096) return -3;
            if (Panel.Terminal(14) != 0) 다시(); if (byte_datos < 0) { Panel.suspender_CPU(); continue; }
            if (byte_datos == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = byte_datos == 13;
            if (byte_datos == 27) { 탈출(); continue; }
            if (byte_datos == 3) { 단말.Escritura("^C\n"); return -1; }
            if (byte_datos == 4 && Tamaño == 0 && liña_de_comandos) { if (Panel.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (byte_datos == 13 || byte_datos == 10) { 단말.문자(10); if (!넘침여부) Anexar_LOG(); return 넘침여부 ? -2 : Tamaño; }
            if (byte_datos == 9 && liña_de_comandos) { Completadas_VALOR(); continue; }
            if (byte_datos == 1 || byte_datos == 5) { cursor_VALOR = byte_datos == 1 ? 0 : Tamaño; 다시(); continue; }
            if (byte_datos == 8 || byte_datos == 127 || byte_datos == 21) {
                if (byte_datos == 21) { for (int Loop_ÍNDICE = cursor_VALOR; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) 명령해석기.Liña[Loop_ÍNDICE - cursor_VALOR] = 명령해석기.Liña[Loop_ÍNDICE]; Tamaño -= cursor_VALOR; cursor_VALOR = 0; }
                else if (cursor_VALOR > 0) { int 변경전 = frontal_VALOR(cursor_VALOR); for (int Loop_ÍNDICE = cursor_VALOR; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) 명령해석기.Liña[Loop_ÍNDICE - cursor_VALOR + 변경전] = 명령해석기.Liña[Loop_ÍNDICE]; Tamaño -= cursor_VALOR - 변경전; cursor_VALOR = 변경전; }
                다시(); continue;
            }
            if (byte_datos == 11) { Tamaño = cursor_VALOR; 다시(); continue; }
            if (byte_datos < 32 && byte_datos != 9) continue;
            if (Tamaño == 명령해석기.Liña.length) { 넘침여부 = true; continue; }
            for (int Loop_ÍNDICE = Tamaño; Loop_ÍNDICE > cursor_VALOR; Loop_ÍNDICE--) 명령해석기.Liña[Loop_ÍNDICE] = 명령해석기.Liña[Loop_ÍNDICE - 1];
            명령해석기.Liña[cursor_VALOR++] = byte_datos; Tamaño++;
            if (cursor_VALOR == Tamaño && !가로보기 && 폭(0, Tamaño) <= 보이는폭()) Panel.직렬쓰기(byte_datos);
            else if (cursor_VALOR == Tamaño) 보이는줄(); else 다시();
        }
    }
}
