// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kernel_VALORE 안의 연결형 byte_VALORE Stream_VALORE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket layer_VALORE. */
public final class Stream_rete {
    static int[] Stato_VALORE = new int[16], porta_VALORE = new int[16], 짝 = new int[16], peer_porta = new int[16], aspetta_VALORE = new int[16], reparto_IT_limite = new int[16];
    static int[] frontale_VALORE = new int[16], numero = new int[16], dati = new int[16 * 1024];
    static int Avanti_articolo = 50000;
    static int verificare(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Stato_VALORE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int numero_di_porta) { for (int Loop_INDICE = 0; Loop_INDICE < 16; Loop_INDICE++) if (Stato_VALORE[Loop_INDICE] != 0 && reparto_IT_limite[Loop_INDICE] != 0 && porta_VALORE[Loop_INDICE] == numero_di_porta) return true; return false; }
    public static int Crea_voce() {
        for (int Loop_INDICE = 0; Loop_INDICE < 16; Loop_INDICE++) if (Stato_VALORE[Loop_INDICE] == 0) { Stato_VALORE[Loop_INDICE] = 1; peer_porta[Loop_INDICE] = porta_VALORE[Loop_INDICE] = frontale_VALORE[Loop_INDICE] = numero[Loop_INDICE] = aspetta_VALORE[Loop_INDICE] = reparto_IT_limite[Loop_INDICE] = 0; 짝[Loop_INDICE] = -1; return Loop_INDICE + 40; }
        return -24;
    }
    public static int BIND_endpoint(int 열린파일번호, int socket_e_mail, int numero_di_porta) {
        int Loop_INDICE = verificare(열린파일번호); if (Loop_INDICE < 0) return -9;
        if (socket_e_mail != 0 && socket_e_mail != 0x7f000001) return -99;
        if (Stato_VALORE[Loop_INDICE] != 1 || numero_di_porta < 0 || numero_di_porta > 65535) return -22;
        if (numero_di_porta == 0) { do { numero_di_porta = Avanti_articolo++; if (Avanti_articolo > 65535) Avanti_articolo = 50000; } while (사용중(numero_di_porta)); }
        if (사용중(numero_di_porta)) return -98; porta_VALORE[Loop_INDICE] = numero_di_porta; reparto_IT_limite[Loop_INDICE] = 1; Stato_VALORE[Loop_INDICE] = 2; return 0;
    }
    public static int essere_in_ascolto_endpoint(int 열린파일번호, int backlog) { int Loop_INDICE = verificare(열린파일번호); if (Loop_INDICE < 0) return -9; if (Stato_VALORE[Loop_INDICE] != 2 || backlog < 1) return -22; Stato_VALORE[Loop_INDICE] = 3; return 0; }
    public static int Connetti(int 열린파일번호, int socket_e_mail, int numero_di_porta) {
        int Loop_INDICE = verificare(열린파일번호); if (Loop_INDICE < 0) return -9; if (socket_e_mail != 0x7f000001) return -101;
        if (numero_di_porta < 1 || numero_di_porta > 65535 || Stato_VALORE[Loop_INDICE] > 2) return -22;
        int ricevere_pagina = -1; for (int inner_funzione = 0; inner_funzione < 16; inner_funzione++) if (Stato_VALORE[inner_funzione] == 3 && porta_VALORE[inner_funzione] == numero_di_porta) ricevere_pagina = inner_funzione;
        if (ricevere_pagina < 0) return -111;
        int 대기여부 = 0; for (int inner_funzione = 0; inner_funzione < 16; inner_funzione++) if (aspetta_VALORE[inner_funzione] == ricevere_pagina + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Stato_VALORE[Loop_INDICE] == 1) { int 처리값 = BIND_endpoint(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Altro = Crea_voce(); if (Altro < 0) return Altro; Altro -= 40;
        Stato_VALORE[Loop_INDICE] = Stato_VALORE[Altro] = 4; 짝[Loop_INDICE] = Altro; 짝[Altro] = Loop_INDICE; porta_VALORE[Altro] = numero_di_porta; peer_porta[Loop_INDICE] = numero_di_porta; peer_porta[Altro] = porta_VALORE[Loop_INDICE]; aspetta_VALORE[Altro] = ricevere_pagina + 1; return 0;
    }
    public static int accettare_connessione(int 열린파일번호) { int Loop_INDICE = verificare(열린파일번호); if (Loop_INDICE < 0) return -9; if (Stato_VALORE[Loop_INDICE] != 3) return -22; for (int inner_funzione = 0; inner_funzione < 16; inner_funzione++) if (Stato_VALORE[inner_funzione] != 0 && aspetta_VALORE[inner_funzione] == Loop_INDICE + 1) { aspetta_VALORE[inner_funzione] = 0; return inner_funzione + 40; } return -11; }
    public static int Scrittura(int 열린파일번호, int voce_CONTA_NUMERI) {
        int Loop_INDICE = verificare(열린파일번호); if (Loop_INDICE < 0) return -9; if (Stato_VALORE[Loop_INDICE] != 4) return -107;
        if (voce_CONTA_NUMERI < 0 || voce_CONTA_NUMERI > 512) return -22; if (voce_CONTA_NUMERI == 0) return 0;
        int inner_funzione = 짝[Loop_INDICE]; if (inner_funzione < 0) return -32; int totale_CONTA_NUMERI = 1024 - numero[inner_funzione]; if (totale_CONTA_NUMERI == 0) return -11; if (totale_CONTA_NUMERI > voce_CONTA_NUMERI) totale_CONTA_NUMERI = voce_CONTA_NUMERI;
        for (int Confronto_funzione = 0; Confronto_funzione < totale_CONTA_NUMERI; Confronto_funzione++) dati[inner_funzione * 1024 + (frontale_VALORE[inner_funzione] + numero[inner_funzione] + Confronto_funzione) % 1024] = loopback_rete.Avanti_VALORE[Confronto_funzione]; numero[inner_funzione] += totale_CONTA_NUMERI; return totale_CONTA_NUMERI;
    }
    public static int Lettura(int 열린파일번호, int voce_CONTA_NUMERI) {
        int Loop_INDICE = verificare(열린파일번호); if (Loop_INDICE < 0) return -9; if (Stato_VALORE[Loop_INDICE] != 4) return -107; if (voce_CONTA_NUMERI < 0 || voce_CONTA_NUMERI > 512) return -22;
        if (voce_CONTA_NUMERI == 0) return 0; if (numero[Loop_INDICE] == 0) return 짝[Loop_INDICE] < 0 ? 0 : -11; if (voce_CONTA_NUMERI > numero[Loop_INDICE]) voce_CONTA_NUMERI = numero[Loop_INDICE];
        for (int Confronto_funzione = 0; Confronto_funzione < voce_CONTA_NUMERI; Confronto_funzione++) loopback_rete.Avanti_VALORE[Confronto_funzione] = dati[Loop_INDICE * 1024 + (frontale_VALORE[Loop_INDICE] + Confronto_funzione) % 1024]; frontale_VALORE[Loop_INDICE] = (frontale_VALORE[Loop_INDICE] + voce_CONTA_NUMERI) % 1024; numero[Loop_INDICE] -= voce_CONTA_NUMERI; return voce_CONTA_NUMERI;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDICE = verificare(열린파일번호); return Loop_INDICE < 0 ? -9 : porta_VALORE[Loop_INDICE]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDICE = verificare(열린파일번호); return Loop_INDICE < 0 ? -9 : peer_porta[Loop_INDICE]; }
    public static int Chiudi(int 열린파일번호) {
        int Loop_INDICE = verificare(열린파일번호); if (Loop_INDICE < 0) return -9;
        if (Stato_VALORE[Loop_INDICE] == 3) for (int inner_funzione = 0; inner_funzione < 16; inner_funzione++) if (aspetta_VALORE[inner_funzione] == Loop_INDICE + 1) { if (짝[inner_funzione] >= 0) 짝[짝[inner_funzione]] = -1; Stato_VALORE[inner_funzione] = aspetta_VALORE[inner_funzione] = reparto_IT_limite[inner_funzione] = 0; }
        if (짝[Loop_INDICE] >= 0) 짝[짝[Loop_INDICE]] = -1; Stato_VALORE[Loop_INDICE] = reparto_IT_limite[Loop_INDICE] = numero[Loop_INDICE] = aspetta_VALORE[Loop_INDICE] = 0; return 0;
    }
}
