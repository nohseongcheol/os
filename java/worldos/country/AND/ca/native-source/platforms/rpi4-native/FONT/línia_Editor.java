// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VALOR 경계를 지키는 삽입/삭제, 방향키, Ordre LOG_fila, Tab Completades_VALOR. */
public final class línia_Editor {
    static boolean línia_d_ordres;
    static int[] LOG_fila = new int[16 * 1024], LOG_durada = new int[16], Store_VALOR = new int[4096], 후보 = new int[64];
    static int LOG_COMPT, LOG_fila_finalitzar, Cerca_VALOR, 저장길이, Mida, cursor_VALOR, 후보수, 후보길이, Inici_finestra;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd segur_shell remot_mostrar run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String introducció_Llista, int Inici_càrrec, int finalitzar_càrrec, int 입력길이) {
        int byte_COMPT=0;
        for(int càrrec_INDEX=Inici_càrrec;càrrec_INDEX<finalitzar_càrrec;càrrec_INDEX++) {
            int codi_de_caràcter=introducció_Llista.charAt(càrrec_INDEX);
            if(codi_de_caràcter>=0xd800 && codi_de_caràcter<=0xdbff && càrrec_INDEX+1<finalitzar_càrrec)codi_de_caràcter=0x10000+((codi_de_caràcter-0xd800)<<10)+introducció_Llista.charAt(++càrrec_INDEX)-0xdc00;
            int 수=codi_de_caràcter<128?1:codi_de_caràcter<2048?2:codi_de_caràcter<65536?3:4;
            if(byte_COMPT+수>62)return;
            for(int SEQÜÈNCIA_VALOR=수-1;SEQÜÈNCIA_VALOR>=0;SEQÜÈNCIA_VALOR--)명령후보[byte_COMPT++]=수==1?codi_de_caràcter:SEQÜÈNCIA_VALOR==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(codi_de_caràcter>>(6*SEQÜÈNCIA_VALOR)):0x80|((codi_de_caràcter>>(6*SEQÜÈNCIA_VALOR))&63);
        }
        if(byte_COMPT<입력길이)return;
        for(int càrrec_INDEX=0;càrrec_INDEX<입력길이;càrrec_INDEX++)if(명령후보[càrrec_INDEX]!=명령해석기.línia[càrrec_INDEX])return;
        후보수++;후보길이=byte_COMPT+1;
        for(int càrrec_INDEX=0;càrrec_INDEX<byte_COMPT;càrrec_INDEX++)후보[càrrec_INDEX]=명령후보[càrrec_INDEX];후보[byte_COMPT]=' ';
    }
    static int frontal_VALOR(int tancar_cursor) { if (tancar_cursor > 0) { tancar_cursor--; while (tancar_cursor > 0 && (명령해석기.línia[tancar_cursor] & 192) == 128) tancar_cursor--; } return tancar_cursor; }
    static int ENRERE_VALOR(int tancar_cursor) { if (tancar_cursor < Mida) { tancar_cursor++; while (tancar_cursor < Mida && (명령해석기.línia[tancar_cursor] & 192) == 128) tancar_cursor++; } return tancar_cursor; }
    static int 폭(int Inici_càrrec, int destinació_VALOR_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Inici_càrrec; Loop_INDEX < destinació_VALOR_INDEX; Loop_INDEX++) { int byte_dades = 명령해석기.línia[Loop_INDEX]; if ((byte_dades & 192) == 128) continue; 글칸수 += byte_dades >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void tornar_ho_a_provar_VALOR() {
        단말.Escriptura("\r\u001b[2K");
        단말.Escriptura(línia_d_ordres ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 línia 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNES = Tauler.Terminal(13) & 65535; return COLUMNES - (línia_d_ordres ? 18 : 9); }
    static void 보이는줄() {
        if (cursor_VALOR < Inici_finestra) Inici_finestra = cursor_VALOR;
        while (폭(Inici_finestra, cursor_VALOR) > 보이는폭()) Inici_finestra = ENRERE_VALOR(Inici_finestra);
        int finalitzar_càrrec = Inici_finestra;
        while (finalitzar_càrrec < Mida && 폭(Inici_finestra, ENRERE_VALOR(finalitzar_càrrec)) <= 보이는폭()) finalitzar_càrrec = ENRERE_VALOR(finalitzar_càrrec);
        단말.Escriptura("\r\u001b["); 단말.수(línia_d_ordres ? 16 : 7); 단말.Escriptura("G\u001b[K");
        if (Inici_finestra > 0) 단말.문자('<');
        for (int Loop_INDEX = Inici_finestra; Loop_INDEX < finalitzar_càrrec; Loop_INDEX++) Tauler.직렬쓰기(명령해석기.línia[Loop_INDEX]);
        단말.문자(finalitzar_càrrec < Mida ? '>' : ' ');
        단말.Escriptura("\u001b["); 단말.수(폭(cursor_VALOR, finalitzar_càrrec) + 1); 단말.문자('D');
        가로보기 = Inici_finestra > 0 || finalitzar_càrrec < Mida || 폭(0, Mida) > 보이는폭();
    }
    static void Annexa_LOG() {
        if (!línia_d_ordres || Mida == 0 || Mida > 1024) return;
        if (LOG_COMPT > 0) {
            int 마지막자리 = (LOG_fila_finalitzar + 15) % 16; boolean 같은여부 = LOG_durada[마지막자리] == Mida;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Mida; Loop_INDEX++) if (LOG_fila[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.línia[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_durada[LOG_fila_finalitzar] = Mida; for (int Loop_INDEX = 0; Loop_INDEX < Mida; Loop_INDEX++) LOG_fila[LOG_fila_finalitzar * 1024 + Loop_INDEX] = 명령해석기.línia[Loop_INDEX];
        LOG_fila_finalitzar = (LOG_fila_finalitzar + 1) % 16; if (LOG_COMPT < 16) LOG_COMPT++;
    }
    static void 기록이동(int DELTA_VALOR) {
        if (!línia_d_ordres) return;
        if (Cerca_VALOR == 0 && DELTA_VALOR > 0) { 저장길이 = Mida; for (int Loop_INDEX = 0; Loop_INDEX < Mida; Loop_INDEX++) Store_VALOR[Loop_INDEX] = 명령해석기.línia[Loop_INDEX]; }
        int Següent_càrrec = Cerca_VALOR + DELTA_VALOR; if (Següent_càrrec < 0 || Següent_càrrec > LOG_COMPT) return; Cerca_VALOR = Següent_càrrec;
        if (Cerca_VALOR == 0) { Mida = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Mida; Loop_INDEX++) 명령해석기.línia[Loop_INDEX] = Store_VALOR[Loop_INDEX]; }
        else { int 보관칸 = (LOG_fila_finalitzar + 16 - Cerca_VALOR) % 16; Mida = LOG_durada[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Mida; Loop_INDEX++) 명령해석기.línia[Loop_INDEX] = LOG_fila[보관칸 * 1024 + Loop_INDEX]; }
        cursor_VALOR = Mida; tornar_ho_a_provar_VALOR();
    }
    static void mostrar_LOG() {
        for (int introducció_COMPT = 0; introducció_COMPT < LOG_COMPT; introducció_COMPT++) {
            int 보관칸 = (LOG_fila_finalitzar + 16 - LOG_COMPT + introducció_COMPT) % 16; 단말.수(introducció_COMPT + 1); 단말.Escriptura("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_durada[보관칸]; Loop_INDEX++) Tauler.직렬쓰기(LOG_fila[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] dades_MATRIU, int Inici_càrrec, int introducció_COMPT, int 접두말, int total_COMPT, boolean 폴더번호) {
        if (introducció_COMPT < total_COMPT || introducció_COMPT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < total_COMPT; Loop_INDEX++) if (dades_MATRIU[Inici_càrrec + Loop_INDEX] != 명령해석기.línia[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = introducció_COMPT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) 후보[Loop_INDEX] = dades_MATRIU[Inici_càrrec + Loop_INDEX]; 후보[introducció_COMPT] = 폴더번호 ? '/' : ' ';
    }
    static void Completades_VALOR() {
        if (!línia_d_ordres || cursor_VALOR != Mida) return;
        int 시작점 = Mida; while (시작점 > 0 && 명령해석기.línia[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Mida; Loop_INDEX++) if (명령해석기.línia[Loop_INDEX] == '/' || 명령해석기.línia[Loop_INDEX] == '"' || 명령해석기.línia[Loop_INDEX] == 39 || 명령해석기.línia[Loop_INDEX] == '\\') return;
        후보수 = 0; int introducció_COMPT = Mida - 시작점;
        if (시작점 == 0) {
            for(int índex_de_la_llista=0;índex_de_la_llista<2;índex_de_la_llista++) {
                String introducció_Llista=índex_de_la_llista==0?명령들:관리명령.Completades_Word();
                int tancar_cursor=0;
                while(tancar_cursor<introducció_Llista.length()) {
                    int finalitzar_càrrec=tancar_cursor;while(finalitzar_càrrec<introducció_Llista.length() && introducció_Llista.charAt(finalitzar_càrrec)!=' ')finalitzar_càrrec++;
                    명령후보넣기(introducció_Llista,tancar_cursor,finalitzar_càrrec,introducció_COMPT);tancar_cursor=finalitzar_càrrec+1;
                }
            }
        } else {
            Memòria_Fitxers.camí_Inici(1); Memòria_Fitxers.camí_byte(0, '.'); Memòria_Fitxers.normalitzar_VALOR();
            for (int Loop_INDEX = 0; Loop_INDEX < Memòria_Fitxers.arxiu_COMPT; Loop_INDEX++) {
                int Inici_càrrec = Memòria_Fitxers.introducció_Inici(Memòria_Fitxers.Nom, Loop_INDEX * 64, Memòria_Fitxers.이름길이[Loop_INDEX]);
                if (Inici_càrrec >= 0) 후보넣기(Memòria_Fitxers.Nom, Loop_INDEX * 64 + Inici_càrrec, Memòria_Fitxers.이름길이[Loop_INDEX] - Inici_càrrec, 시작점, introducció_COMPT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Inici_càrrec = Memòria_Fitxers.introducció_Inici(Memòria_Fitxers.directori_nom, Loop_INDEX * 64, Memòria_Fitxers.directori_durada[Loop_INDEX]);
                if (Inici_càrrec >= 0) 후보넣기(Memòria_Fitxers.directori_nom, Loop_INDEX * 64 + Inici_càrrec, Memòria_Fitxers.directori_durada[Loop_INDEX] - Inici_càrrec, 시작점, introducció_COMPT, true);
            }
        }
        if (후보수 != 1) { Tauler.직렬쓰기(7); return; }
        for (int Loop_INDEX = introducció_COMPT; Loop_INDEX < 후보길이 && Mida < 명령해석기.línia.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.línia[Mida++] = '\\';
            명령해석기.línia[Mida++] = 후보[Loop_INDEX];
        }
        cursor_VALOR = Mida; tornar_ho_a_provar_VALOR();
    }
    static int 탈출읽기() {
        int 시작점 = Tauler.밀리초();
        while (Tauler.밀리초() - 시작점 < 80) { int byte_dades = Tauler.직렬읽기(); if (byte_dades >= 0) return byte_dades; Tauler.RENDTO_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int introducció_COMPT = 0, finalitzar_càrrec = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int byte_dades = 탈출읽기(); if (byte_dades < 0) return; if (byte_dades >= '0' && byte_dades <= '9') introducció_COMPT = introducció_COMPT * 10 + byte_dades - '0'; else { finalitzar_càrrec = byte_dades; break; } }
        if (finalitzar_càrrec == 'A') 기록이동(1);
        else if (finalitzar_càrrec == 'B') 기록이동(-1);
        else if (finalitzar_càrrec == 'C') { cursor_VALOR = ENRERE_VALOR(cursor_VALOR); tornar_ho_a_provar_VALOR(); }
        else if (finalitzar_càrrec == 'D') { cursor_VALOR = frontal_VALOR(cursor_VALOR); tornar_ho_a_provar_VALOR(); }
        else if (finalitzar_càrrec == 'H' || finalitzar_càrrec == '~' && (introducció_COMPT == 1 || introducció_COMPT == 7)) { cursor_VALOR = 0; tornar_ho_a_provar_VALOR(); }
        else if (finalitzar_càrrec == 'F' || finalitzar_càrrec == '~' && (introducció_COMPT == 4 || introducció_COMPT == 8)) { cursor_VALOR = Mida; tornar_ho_a_provar_VALOR(); }
        else if (finalitzar_càrrec == '~' && introducció_COMPT == 3 && cursor_VALOR < Mida) {
            int Següent_càrrec = ENRERE_VALOR(cursor_VALOR); for (int Loop_INDEX = Següent_càrrec; Loop_INDEX < Mida; Loop_INDEX++) 명령해석기.línia[Loop_INDEX - Següent_càrrec + cursor_VALOR] = 명령해석기.línia[Loop_INDEX]; Mida -= Següent_càrrec - cursor_VALOR; tornar_ho_a_provar_VALOR();
        }
        else if (finalitzar_càrrec == '~' && (introducció_COMPT == 5 || introducció_COMPT == 6)) Tauler.Terminal(introducció_COMPT == 5 ? 5 : 6);
        else if (finalitzar_càrrec == '~' && introducció_COMPT == 24 && línia_d_ordres) { 명령해석기.Terminal(true); }
    }
    static int Lectura() {
        if (!finestra_sessió.이어읽기) { Mida = cursor_VALOR = Cerca_VALOR = Inici_finestra = 0; 가로보기 = false; }
        else { finestra_sessió.이어읽기 = false; tornar_ho_a_provar_VALOR(); } boolean sobreeiximent = false;
        while (true) {
            int byte_dades = Tauler.직렬읽기(); if (byte_dades == -4096) return -3;
            if (Tauler.Terminal(14) != 0) tornar_ho_a_provar_VALOR(); if (byte_dades < 0) { Tauler.RENDTO_CPU(); continue; }
            if (byte_dades == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = byte_dades == 13;
            if (byte_dades == 27) { 탈출(); continue; }
            if (byte_dades == 3) { 단말.Escriptura("^C\n"); return -1; }
            if (byte_dades == 4 && Mida == 0 && línia_d_ordres) { if (Tauler.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (byte_dades == 13 || byte_dades == 10) { 단말.문자(10); if (!sobreeiximent) Annexa_LOG(); return sobreeiximent ? -2 : Mida; }
            if (byte_dades == 9 && línia_d_ordres) { Completades_VALOR(); continue; }
            if (byte_dades == 1 || byte_dades == 5) { cursor_VALOR = byte_dades == 1 ? 0 : Mida; tornar_ho_a_provar_VALOR(); continue; }
            if (byte_dades == 8 || byte_dades == 127 || byte_dades == 21) {
                if (byte_dades == 21) { for (int Loop_INDEX = cursor_VALOR; Loop_INDEX < Mida; Loop_INDEX++) 명령해석기.línia[Loop_INDEX - cursor_VALOR] = 명령해석기.línia[Loop_INDEX]; Mida -= cursor_VALOR; cursor_VALOR = 0; }
                else if (cursor_VALOR > 0) { int 변경전 = frontal_VALOR(cursor_VALOR); for (int Loop_INDEX = cursor_VALOR; Loop_INDEX < Mida; Loop_INDEX++) 명령해석기.línia[Loop_INDEX - cursor_VALOR + 변경전] = 명령해석기.línia[Loop_INDEX]; Mida -= cursor_VALOR - 변경전; cursor_VALOR = 변경전; }
                tornar_ho_a_provar_VALOR(); continue;
            }
            if (byte_dades == 11) { Mida = cursor_VALOR; tornar_ho_a_provar_VALOR(); continue; }
            if (byte_dades < 32 && byte_dades != 9) continue;
            if (Mida == 명령해석기.línia.length) { sobreeiximent = true; continue; }
            for (int Loop_INDEX = Mida; Loop_INDEX > cursor_VALOR; Loop_INDEX--) 명령해석기.línia[Loop_INDEX] = 명령해석기.línia[Loop_INDEX - 1];
            명령해석기.línia[cursor_VALOR++] = byte_dades; Mida++;
            if (cursor_VALOR == Mida && !가로보기 && 폭(0, Mida) <= 보이는폭()) Tauler.직렬쓰기(byte_dades);
            else if (cursor_VALOR == Mida) 보이는줄(); else tornar_ho_a_provar_VALOR();
        }
    }
}
