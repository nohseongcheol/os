// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kernel_VALOR 안의 연결형 byte_VALOR fluxo_VALOR. Ethernet/TCP 패킷 스택이 아닌 루프백 socket camada_VALOR. */
public final class fluxo_rede {
    static int[] Estado_VALOR = new int[16], porta_VALOR = new int[16], 짝 = new int[16], par_porta = new int[16], aguarde_VALOR = new int[16], TI_limite = new int[16];
    static int[] câmera_frontal_VALOR = new int[16], número = new int[16], dados = new int[16 * 1024];
    static int Avançar_item = 50000;
    static int verificar(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Estado_VALOR[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int número_da_porta) { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (Estado_VALOR[Loop_ÍNDICE] != 0 && TI_limite[Loop_ÍNDICE] != 0 && porta_VALOR[Loop_ÍNDICE] == número_da_porta) return true; return false; }
    public static int Criar_entrada() {
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (Estado_VALOR[Loop_ÍNDICE] == 0) { Estado_VALOR[Loop_ÍNDICE] = 1; par_porta[Loop_ÍNDICE] = porta_VALOR[Loop_ÍNDICE] = câmera_frontal_VALOR[Loop_ÍNDICE] = número[Loop_ÍNDICE] = aguarde_VALOR[Loop_ÍNDICE] = TI_limite[Loop_ÍNDICE] = 0; 짝[Loop_ÍNDICE] = -1; return Loop_ÍNDICE + 40; }
        return -24;
    }
    public static int BIND_empresa(int 열린파일번호, int soquete_email, int número_da_porta) {
        int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9;
        if (soquete_email != 0 && soquete_email != 0x7f000001) return -99;
        if (Estado_VALOR[Loop_ÍNDICE] != 1 || número_da_porta < 0 || número_da_porta > 65535) return -22;
        if (número_da_porta == 0) { do { número_da_porta = Avançar_item++; if (Avançar_item > 65535) Avançar_item = 50000; } while (사용중(número_da_porta)); }
        if (사용중(número_da_porta)) return -98; porta_VALOR[Loop_ÍNDICE] = número_da_porta; TI_limite[Loop_ÍNDICE] = 1; Estado_VALOR[Loop_ÍNDICE] = 2; return 0;
    }
    public static int escutar_empresa(int 열린파일번호, int lista_de_pendências) { int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9; if (Estado_VALOR[Loop_ÍNDICE] != 2 || lista_de_pendências < 1) return -22; Estado_VALOR[Loop_ÍNDICE] = 3; return 0; }
    public static int Ligar(int 열린파일번호, int soquete_email, int número_da_porta) {
        int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9; if (soquete_email != 0x7f000001) return -101;
        if (número_da_porta < 1 || número_da_porta > 65535 || Estado_VALOR[Loop_ÍNDICE] > 2) return -22;
        int receber_página = -1; for (int interna_cargo = 0; interna_cargo < 16; interna_cargo++) if (Estado_VALOR[interna_cargo] == 3 && porta_VALOR[interna_cargo] == número_da_porta) receber_página = interna_cargo;
        if (receber_página < 0) return -111;
        int TI_na_fila = 0; for (int interna_cargo = 0; interna_cargo < 16; interna_cargo++) if (aguarde_VALOR[interna_cargo] == receber_página + 1) TI_na_fila++;
        if (TI_na_fila >= 4) return -11;
        if (Estado_VALOR[Loop_ÍNDICE] == 1) { int 처리값 = BIND_empresa(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Outros = Criar_entrada(); if (Outros < 0) return Outros; Outros -= 40;
        Estado_VALOR[Loop_ÍNDICE] = Estado_VALOR[Outros] = 4; 짝[Loop_ÍNDICE] = Outros; 짝[Outros] = Loop_ÍNDICE; porta_VALOR[Outros] = número_da_porta; par_porta[Loop_ÍNDICE] = número_da_porta; par_porta[Outros] = porta_VALOR[Loop_ÍNDICE]; aguarde_VALOR[Outros] = receber_página + 1; return 0;
    }
    public static int aceitar_conexão(int 열린파일번호) { int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9; if (Estado_VALOR[Loop_ÍNDICE] != 3) return -22; for (int interna_cargo = 0; interna_cargo < 16; interna_cargo++) if (Estado_VALOR[interna_cargo] != 0 && aguarde_VALOR[interna_cargo] == Loop_ÍNDICE + 1) { aguarde_VALOR[interna_cargo] = 0; return interna_cargo + 40; } return -11; }
    public static int Escrita(int 열린파일번호, int entrada_CONT_NÚM_8f7753a1) {
        int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9; if (Estado_VALOR[Loop_ÍNDICE] != 4) return -107;
        if (entrada_CONT_NÚM_8f7753a1 < 0 || entrada_CONT_NÚM_8f7753a1 > 512) return -22; if (entrada_CONT_NÚM_8f7753a1 == 0) return 0;
        int interna_cargo = 짝[Loop_ÍNDICE]; if (interna_cargo < 0) return -32; int total_CONT_NÚM = 1024 - número[interna_cargo]; if (total_CONT_NÚM == 0) return -11; if (total_CONT_NÚM > entrada_CONT_NÚM_8f7753a1) total_CONT_NÚM = entrada_CONT_NÚM_8f7753a1;
        for (int Comparação_cargo = 0; Comparação_cargo < total_CONT_NÚM; Comparação_cargo++) dados[interna_cargo * 1024 + (câmera_frontal_VALOR[interna_cargo] + número[interna_cargo] + Comparação_cargo) % 1024] = loopback_rede.Avançar_VALOR[Comparação_cargo]; número[interna_cargo] += total_CONT_NÚM; return total_CONT_NÚM;
    }
    public static int Leitura(int 열린파일번호, int entrada_CONT_NÚM_8f7753a1) {
        int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9; if (Estado_VALOR[Loop_ÍNDICE] != 4) return -107; if (entrada_CONT_NÚM_8f7753a1 < 0 || entrada_CONT_NÚM_8f7753a1 > 512) return -22;
        if (entrada_CONT_NÚM_8f7753a1 == 0) return 0; if (número[Loop_ÍNDICE] == 0) return 짝[Loop_ÍNDICE] < 0 ? 0 : -11; if (entrada_CONT_NÚM_8f7753a1 > número[Loop_ÍNDICE]) entrada_CONT_NÚM_8f7753a1 = número[Loop_ÍNDICE];
        for (int Comparação_cargo = 0; Comparação_cargo < entrada_CONT_NÚM_8f7753a1; Comparação_cargo++) loopback_rede.Avançar_VALOR[Comparação_cargo] = dados[Loop_ÍNDICE * 1024 + (câmera_frontal_VALOR[Loop_ÍNDICE] + Comparação_cargo) % 1024]; câmera_frontal_VALOR[Loop_ÍNDICE] = (câmera_frontal_VALOR[Loop_ÍNDICE] + entrada_CONT_NÚM_8f7753a1) % 1024; número[Loop_ÍNDICE] -= entrada_CONT_NÚM_8f7753a1; return entrada_CONT_NÚM_8f7753a1;
    }
    public static int leitura_empresa_porta(int 열린파일번호) { int Loop_ÍNDICE = verificar(열린파일번호); return Loop_ÍNDICE < 0 ? -9 : porta_VALOR[Loop_ÍNDICE]; }
    public static int leitura_par_porta(int 열린파일번호) { int Loop_ÍNDICE = verificar(열린파일번호); return Loop_ÍNDICE < 0 ? -9 : par_porta[Loop_ÍNDICE]; }
    public static int Fechar(int 열린파일번호) {
        int Loop_ÍNDICE = verificar(열린파일번호); if (Loop_ÍNDICE < 0) return -9;
        if (Estado_VALOR[Loop_ÍNDICE] == 3) for (int interna_cargo = 0; interna_cargo < 16; interna_cargo++) if (aguarde_VALOR[interna_cargo] == Loop_ÍNDICE + 1) { if (짝[interna_cargo] >= 0) 짝[짝[interna_cargo]] = -1; Estado_VALOR[interna_cargo] = aguarde_VALOR[interna_cargo] = TI_limite[interna_cargo] = 0; }
        if (짝[Loop_ÍNDICE] >= 0) 짝[짝[Loop_ÍNDICE]] = -1; Estado_VALOR[Loop_ÍNDICE] = TI_limite[Loop_ÍNDICE] = número[Loop_ÍNDICE] = aguarde_VALOR[Loop_ÍNDICE] = 0; return 0;
    }
}
