// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kernel_VALOR 안의 연결형 byte_VALOR fluxo_VALOR. Ethernet/TCP 패킷 스택이 아닌 루프백 socket capa_VALOR. */
public final class fluxo_Rede {
    static int[] Estado_VALOR = new int[16], porto_VALOR = new int[16], 짝 = new int[16], punto_porto = new int[16], agarda_VALOR = new int[16], 묶임 = new int[16];
    static int[] frontal_VALOR = new int[16], 수 = new int[16], datos = new int[16 * 1024];
    static int Seguinte_elemento = 50000;
    static int verificar(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Estado_VALOR[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int número_do_porto) { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (Estado_VALOR[Loop_ÍNDICE] != 0 && 묶임[Loop_ÍNDICE] != 0 && porto_VALOR[Loop_ÍNDICE] == número_do_porto) return true; return false; }
    public static int crear_introdución() {
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (Estado_VALOR[Loop_ÍNDICE] == 0) { Estado_VALOR[Loop_ÍNDICE] = 1; punto_porto[Loop_ÍNDICE] = porto_VALOR[Loop_ÍNDICE] = frontal_VALOR[Loop_ÍNDICE] = 수[Loop_ÍNDICE] = agarda_VALOR[Loop_ÍNDICE] = 묶임[Loop_ÍNDICE] = 0; 짝[Loop_ÍNDICE] = -1; return Loop_ÍNDICE + 40; }
        return -24;
    }
    public static int ligar_extremo(int 열린파일번호, int 통신주소, int número_do_porto) {
        int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Estado_VALOR[Loop_ÍNDICE] != 1 || número_do_porto < 0 || número_do_porto > 65535) return -22;
        if (número_do_porto == 0) { do { número_do_porto = Seguinte_elemento++; if (Seguinte_elemento > 65535) Seguinte_elemento = 50000; } while (사용중(número_do_porto)); }
        if (사용중(número_do_porto)) return -98; porto_VALOR[Loop_ÍNDICE] = número_do_porto; 묶임[Loop_ÍNDICE] = 1; Estado_VALOR[Loop_ÍNDICE] = 2; return 0;
    }
    public static int agardar_extremo(int 열린파일번호, int 연결대기한도) { int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9; if (Estado_VALOR[Loop_ÍNDICE] != 2 || 연결대기한도 < 1) return -22; Estado_VALOR[Loop_ÍNDICE] = 3; return 0; }
    public static int Conectar(int 열린파일번호, int 통신주소, int número_do_porto) {
        int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (número_do_porto < 1 || número_do_porto > 65535 || Estado_VALOR[Loop_ÍNDICE] > 2) return -22;
        int 수신쪽 = -1; for (int interna_cargo = 0; interna_cargo < 16; interna_cargo++) if (Estado_VALOR[interna_cargo] == 3 && porto_VALOR[interna_cargo] == número_do_porto) 수신쪽 = interna_cargo;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int interna_cargo = 0; interna_cargo < 16; interna_cargo++) if (agarda_VALOR[interna_cargo] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Estado_VALOR[Loop_ÍNDICE] == 1) { int 처리값 = ligar_extremo(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = crear_introdución(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        Estado_VALOR[Loop_ÍNDICE] = Estado_VALOR[다른번호] = 4; 짝[Loop_ÍNDICE] = 다른번호; 짝[다른번호] = Loop_ÍNDICE; porto_VALOR[다른번호] = número_do_porto; punto_porto[Loop_ÍNDICE] = número_do_porto; punto_porto[다른번호] = porto_VALOR[Loop_ÍNDICE]; agarda_VALOR[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int aceptar_conexión(int 열린파일번호) { int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9; if (Estado_VALOR[Loop_ÍNDICE] != 3) return -22; for (int interna_cargo = 0; interna_cargo < 16; interna_cargo++) if (Estado_VALOR[interna_cargo] != 0 && agarda_VALOR[interna_cargo] == Loop_ÍNDICE + 1) { agarda_VALOR[interna_cargo] = 0; return interna_cargo + 40; } return -11; }
    public static int Escritura(int 열린파일번호, int introdución_CONTAR) {
        int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9; if (Estado_VALOR[Loop_ÍNDICE] != 4) return -107;
        if (introdución_CONTAR < 0 || introdución_CONTAR > 512) return -22; if (introdución_CONTAR == 0) return 0;
        int interna_cargo = 짝[Loop_ÍNDICE]; if (interna_cargo < 0) return -32; int 총수 = 1024 - 수[interna_cargo]; if (총수 == 0) return -11; if (총수 > introdución_CONTAR) 총수 = introdución_CONTAR;
        for (int Comparación_cargo = 0; Comparación_cargo < 총수; Comparación_cargo++) datos[interna_cargo * 1024 + (frontal_VALOR[interna_cargo] + 수[interna_cargo] + Comparación_cargo) % 1024] = 되돌림망.Adiante_VALOR[Comparación_cargo]; 수[interna_cargo] += 총수; return 총수;
    }
    public static int Lectura(int 열린파일번호, int introdución_CONTAR) {
        int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9; if (Estado_VALOR[Loop_ÍNDICE] != 4) return -107; if (introdución_CONTAR < 0 || introdución_CONTAR > 512) return -22;
        if (introdución_CONTAR == 0) return 0; if (수[Loop_ÍNDICE] == 0) return 짝[Loop_ÍNDICE] < 0 ? 0 : -11; if (introdución_CONTAR > 수[Loop_ÍNDICE]) introdución_CONTAR = 수[Loop_ÍNDICE];
        for (int Comparación_cargo = 0; Comparación_cargo < introdución_CONTAR; Comparación_cargo++) 되돌림망.Adiante_VALOR[Comparación_cargo] = datos[Loop_ÍNDICE * 1024 + (frontal_VALOR[Loop_ÍNDICE] + Comparación_cargo) % 1024]; frontal_VALOR[Loop_ÍNDICE] = (frontal_VALOR[Loop_ÍNDICE] + introdución_CONTAR) % 1024; 수[Loop_ÍNDICE] -= introdución_CONTAR; return introdución_CONTAR;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_ÍNDICE = verificar(열린파일번호); return Loop_ÍNDICE < 0 ? -9 : porto_VALOR[Loop_ÍNDICE]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_ÍNDICE = verificar(열린파일번호); return Loop_ÍNDICE < 0 ? -9 : punto_porto[Loop_ÍNDICE]; }
    public static int Pechar(int 열린파일번호) {
        int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9;
        if (Estado_VALOR[Loop_ÍNDICE] == 3) for (int interna_cargo = 0; interna_cargo < 16; interna_cargo++) if (agarda_VALOR[interna_cargo] == Loop_ÍNDICE + 1) { if (짝[interna_cargo] >= 0) 짝[짝[interna_cargo]] = -1; Estado_VALOR[interna_cargo] = agarda_VALOR[interna_cargo] = 묶임[interna_cargo] = 0; }
        if (짝[Loop_ÍNDICE] >= 0) 짝[짝[Loop_ÍNDICE]] = -1; Estado_VALOR[Loop_ÍNDICE] = 묶임[Loop_ÍNDICE] = 수[Loop_ÍNDICE] = agarda_VALOR[Loop_ÍNDICE] = 0; return 0;
    }
}
