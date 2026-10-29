// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** nucli_VALOR 안의 연결형 byte_VALOR flux_VALOR. Ethernet/TCP 패킷 스택이 아닌 루프백 socket capa_VALOR. */
public final class flux_xarxa {
    static int[] Estat_VALOR = new int[16], port_VALOR = new int[16], 짝 = new int[16], homòleg_port = new int[16], Espera_VALOR = new int[16], 묶임 = new int[16];
    static int[] frontal_VALOR = new int[16], 수 = new int[16], dades = new int[16 * 1024];
    static int Següent_element = 50000;
    static int verificar(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Estat_VALOR[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int número_de_port) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Estat_VALOR[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && port_VALOR[Loop_INDEX] == número_de_port) return true; return false; }
    public static int Crear_introducció() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Estat_VALOR[Loop_INDEX] == 0) { Estat_VALOR[Loop_INDEX] = 1; homòleg_port[Loop_INDEX] = port_VALOR[Loop_INDEX] = frontal_VALOR[Loop_INDEX] = 수[Loop_INDEX] = Espera_VALOR[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int enllaçar_extrem(int 열린파일번호, int 통신주소, int número_de_port) {
        int Loop_INDEX = verificar(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Estat_VALOR[Loop_INDEX] != 1 || número_de_port < 0 || número_de_port > 65535) return -22;
        if (número_de_port == 0) { do { número_de_port = Següent_element++; if (Següent_element > 65535) Següent_element = 50000; } while (사용중(número_de_port)); }
        if (사용중(número_de_port)) return -98; port_VALOR[Loop_INDEX] = número_de_port; 묶임[Loop_INDEX] = 1; Estat_VALOR[Loop_INDEX] = 2; return 0;
    }
    public static int escoltar_extrem(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = verificar(열린파일번호); if (Loop_INDEX < 0) return -9; if (Estat_VALOR[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; Estat_VALOR[Loop_INDEX] = 3; return 0; }
    public static int Connecta(int 열린파일번호, int 통신주소, int número_de_port) {
        int Loop_INDEX = verificar(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (número_de_port < 1 || número_de_port > 65535 || Estat_VALOR[Loop_INDEX] > 2) return -22;
        int rebre_pàgina = -1; for (int interna_càrrec = 0; interna_càrrec < 16; interna_càrrec++) if (Estat_VALOR[interna_càrrec] == 3 && port_VALOR[interna_càrrec] == número_de_port) rebre_pàgina = interna_càrrec;
        if (rebre_pàgina < 0) return -111;
        int 대기여부 = 0; for (int interna_càrrec = 0; interna_càrrec < 16; interna_càrrec++) if (Espera_VALOR[interna_càrrec] == rebre_pàgina + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Estat_VALOR[Loop_INDEX] == 1) { int 처리값 = enllaçar_extrem(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Crear_introducció(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        Estat_VALOR[Loop_INDEX] = Estat_VALOR[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; port_VALOR[다른번호] = número_de_port; homòleg_port[Loop_INDEX] = número_de_port; homòleg_port[다른번호] = port_VALOR[Loop_INDEX]; Espera_VALOR[다른번호] = rebre_pàgina + 1; return 0;
    }
    public static int acceptar_connexió(int 열린파일번호) { int Loop_INDEX = verificar(열린파일번호); if (Loop_INDEX < 0) return -9; if (Estat_VALOR[Loop_INDEX] != 3) return -22; for (int interna_càrrec = 0; interna_càrrec < 16; interna_càrrec++) if (Estat_VALOR[interna_càrrec] != 0 && Espera_VALOR[interna_càrrec] == Loop_INDEX + 1) { Espera_VALOR[interna_càrrec] = 0; return interna_càrrec + 40; } return -11; }
    public static int Escriptura(int 열린파일번호, int introducció_COMPT) {
        int Loop_INDEX = verificar(열린파일번호); if (Loop_INDEX < 0) return -9; if (Estat_VALOR[Loop_INDEX] != 4) return -107;
        if (introducció_COMPT < 0 || introducció_COMPT > 512) return -22; if (introducció_COMPT == 0) return 0;
        int interna_càrrec = 짝[Loop_INDEX]; if (interna_càrrec < 0) return -32; int total_COMPT = 1024 - 수[interna_càrrec]; if (total_COMPT == 0) return -11; if (total_COMPT > introducció_COMPT) total_COMPT = introducció_COMPT;
        for (int Comparació_càrrec = 0; Comparació_càrrec < total_COMPT; Comparació_càrrec++) dades[interna_càrrec * 1024 + (frontal_VALOR[interna_càrrec] + 수[interna_càrrec] + Comparació_càrrec) % 1024] = 되돌림망.desviar_VALOR[Comparació_càrrec]; 수[interna_càrrec] += total_COMPT; return total_COMPT;
    }
    public static int Lectura(int 열린파일번호, int introducció_COMPT) {
        int Loop_INDEX = verificar(열린파일번호); if (Loop_INDEX < 0) return -9; if (Estat_VALOR[Loop_INDEX] != 4) return -107; if (introducció_COMPT < 0 || introducció_COMPT > 512) return -22;
        if (introducció_COMPT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (introducció_COMPT > 수[Loop_INDEX]) introducció_COMPT = 수[Loop_INDEX];
        for (int Comparació_càrrec = 0; Comparació_càrrec < introducció_COMPT; Comparació_càrrec++) 되돌림망.desviar_VALOR[Comparació_càrrec] = dades[Loop_INDEX * 1024 + (frontal_VALOR[Loop_INDEX] + Comparació_càrrec) % 1024]; frontal_VALOR[Loop_INDEX] = (frontal_VALOR[Loop_INDEX] + introducció_COMPT) % 1024; 수[Loop_INDEX] -= introducció_COMPT; return introducció_COMPT;
    }
    public static int tancar_extrem_port(int 열린파일번호) { int Loop_INDEX = verificar(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALOR[Loop_INDEX]; }
    public static int tancar_homòleg_port(int 열린파일번호) { int Loop_INDEX = verificar(열린파일번호); return Loop_INDEX < 0 ? -9 : homòleg_port[Loop_INDEX]; }
    public static int Tanca(int 열린파일번호) {
        int Loop_INDEX = verificar(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Estat_VALOR[Loop_INDEX] == 3) for (int interna_càrrec = 0; interna_càrrec < 16; interna_càrrec++) if (Espera_VALOR[interna_càrrec] == Loop_INDEX + 1) { if (짝[interna_càrrec] >= 0) 짝[짝[interna_càrrec]] = -1; Estat_VALOR[interna_càrrec] = Espera_VALOR[interna_càrrec] = 묶임[interna_càrrec] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Estat_VALOR[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = Espera_VALOR[Loop_INDEX] = 0; return 0;
    }
}
