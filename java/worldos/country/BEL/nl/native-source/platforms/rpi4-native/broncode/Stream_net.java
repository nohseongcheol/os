// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kernel_WAARDE 안의 연결형 byte_WAARDE Stream_WAARDE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket laag_WAARDE. */
public final class Stream_net {
    static int[] Status_WAARDE = new int[16], poort_WAARDE = new int[16], 짝 = new int[16], peer_poort = new int[16], wachten_WAARDE = new int[16], informatie_grens = new int[16];
    static int[] voorkant_WAARDE = new int[16], nummer = new int[16], gegevens = new int[16 * 1024];
    static int Volgende_item = 50000;
    static int bevestigen(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Status_WAARDE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int poortnummer) { for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) if (Status_WAARDE[lus_INDEX] != 0 && informatie_grens[lus_INDEX] != 0 && poort_WAARDE[lus_INDEX] == poortnummer) return true; return false; }
    public static int maken_invoer() {
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) if (Status_WAARDE[lus_INDEX] == 0) { Status_WAARDE[lus_INDEX] = 1; peer_poort[lus_INDEX] = poort_WAARDE[lus_INDEX] = voorkant_WAARDE[lus_INDEX] = nummer[lus_INDEX] = wachten_WAARDE[lus_INDEX] = informatie_grens[lus_INDEX] = 0; 짝[lus_INDEX] = -1; return lus_INDEX + 40; }
        return -24;
    }
    public static int BIND_eindpunt(int 열린파일번호, int socket_ADRES, int poortnummer) {
        int lus_INDEX = bevestigen(열린파일번호); if (lus_INDEX < 0) return -9;
        if (socket_ADRES != 0 && socket_ADRES != 0x7f000001) return -99;
        if (Status_WAARDE[lus_INDEX] != 1 || poortnummer < 0 || poortnummer > 65535) return -22;
        if (poortnummer == 0) { do { poortnummer = Volgende_item++; if (Volgende_item > 65535) Volgende_item = 50000; } while (사용중(poortnummer)); }
        if (사용중(poortnummer)) return -98; poort_WAARDE[lus_INDEX] = poortnummer; informatie_grens[lus_INDEX] = 1; Status_WAARDE[lus_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int achterstand) { int lus_INDEX = bevestigen(열린파일번호); if (lus_INDEX < 0) return -9; if (Status_WAARDE[lus_INDEX] != 2 || achterstand < 1) return -22; Status_WAARDE[lus_INDEX] = 3; return 0; }
    public static int Verbinden(int 열린파일번호, int socket_ADRES, int poortnummer) {
        int lus_INDEX = bevestigen(열린파일번호); if (lus_INDEX < 0) return -9; if (socket_ADRES != 0x7f000001) return -101;
        if (poortnummer < 1 || poortnummer > 65535 || Status_WAARDE[lus_INDEX] > 2) return -22;
        int ontvangen_page = -1; for (int inner_functie = 0; inner_functie < 16; inner_functie++) if (Status_WAARDE[inner_functie] == 3 && poort_WAARDE[inner_functie] == poortnummer) ontvangen_page = inner_functie;
        if (ontvangen_page < 0) return -111;
        int 대기여부 = 0; for (int inner_functie = 0; inner_functie < 16; inner_functie++) if (wachten_WAARDE[inner_functie] == ontvangen_page + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Status_WAARDE[lus_INDEX] == 1) { int 처리값 = BIND_eindpunt(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Overige = maken_invoer(); if (Overige < 0) return Overige; Overige -= 40;
        Status_WAARDE[lus_INDEX] = Status_WAARDE[Overige] = 4; 짝[lus_INDEX] = Overige; 짝[Overige] = lus_INDEX; poort_WAARDE[Overige] = poortnummer; peer_poort[lus_INDEX] = poortnummer; peer_poort[Overige] = poort_WAARDE[lus_INDEX]; wachten_WAARDE[Overige] = ontvangen_page + 1; return 0;
    }
    public static int accepteren_verbinding(int 열린파일번호) { int lus_INDEX = bevestigen(열린파일번호); if (lus_INDEX < 0) return -9; if (Status_WAARDE[lus_INDEX] != 3) return -22; for (int inner_functie = 0; inner_functie < 16; inner_functie++) if (Status_WAARDE[inner_functie] != 0 && wachten_WAARDE[inner_functie] == lus_INDEX + 1) { wachten_WAARDE[inner_functie] = 0; return inner_functie + 40; } return -11; }
    public static int Schrijven(int 열린파일번호, int invoer_AANTAL_8f7753a1) {
        int lus_INDEX = bevestigen(열린파일번호); if (lus_INDEX < 0) return -9; if (Status_WAARDE[lus_INDEX] != 4) return -107;
        if (invoer_AANTAL_8f7753a1 < 0 || invoer_AANTAL_8f7753a1 > 512) return -22; if (invoer_AANTAL_8f7753a1 == 0) return 0;
        int inner_functie = 짝[lus_INDEX]; if (inner_functie < 0) return -32; int totaal_AANTAL = 1024 - nummer[inner_functie]; if (totaal_AANTAL == 0) return -11; if (totaal_AANTAL > invoer_AANTAL_8f7753a1) totaal_AANTAL = invoer_AANTAL_8f7753a1;
        for (int Vergelijking_functie = 0; Vergelijking_functie < totaal_AANTAL; Vergelijking_functie++) gegevens[inner_functie * 1024 + (voorkant_WAARDE[inner_functie] + nummer[inner_functie] + Vergelijking_functie) % 1024] = loopback_net.Vooruit_WAARDE[Vergelijking_functie]; nummer[inner_functie] += totaal_AANTAL; return totaal_AANTAL;
    }
    public static int Lezen(int 열린파일번호, int invoer_AANTAL_8f7753a1) {
        int lus_INDEX = bevestigen(열린파일번호); if (lus_INDEX < 0) return -9; if (Status_WAARDE[lus_INDEX] != 4) return -107; if (invoer_AANTAL_8f7753a1 < 0 || invoer_AANTAL_8f7753a1 > 512) return -22;
        if (invoer_AANTAL_8f7753a1 == 0) return 0; if (nummer[lus_INDEX] == 0) return 짝[lus_INDEX] < 0 ? 0 : -11; if (invoer_AANTAL_8f7753a1 > nummer[lus_INDEX]) invoer_AANTAL_8f7753a1 = nummer[lus_INDEX];
        for (int Vergelijking_functie = 0; Vergelijking_functie < invoer_AANTAL_8f7753a1; Vergelijking_functie++) loopback_net.Vooruit_WAARDE[Vergelijking_functie] = gegevens[lus_INDEX * 1024 + (voorkant_WAARDE[lus_INDEX] + Vergelijking_functie) % 1024]; voorkant_WAARDE[lus_INDEX] = (voorkant_WAARDE[lus_INDEX] + invoer_AANTAL_8f7753a1) % 1024; nummer[lus_INDEX] -= invoer_AANTAL_8f7753a1; return invoer_AANTAL_8f7753a1;
    }
    public static int 창구읽기(int 열린파일번호) { int lus_INDEX = bevestigen(열린파일번호); return lus_INDEX < 0 ? -9 : poort_WAARDE[lus_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int lus_INDEX = bevestigen(열린파일번호); return lus_INDEX < 0 ? -9 : peer_poort[lus_INDEX]; }
    public static int Sluiten(int 열린파일번호) {
        int lus_INDEX = bevestigen(열린파일번호); if (lus_INDEX < 0) return -9;
        if (Status_WAARDE[lus_INDEX] == 3) for (int inner_functie = 0; inner_functie < 16; inner_functie++) if (wachten_WAARDE[inner_functie] == lus_INDEX + 1) { if (짝[inner_functie] >= 0) 짝[짝[inner_functie]] = -1; Status_WAARDE[inner_functie] = wachten_WAARDE[inner_functie] = informatie_grens[inner_functie] = 0; }
        if (짝[lus_INDEX] >= 0) 짝[짝[lus_INDEX]] = -1; Status_WAARDE[lus_INDEX] = informatie_grens[lus_INDEX] = nummer[lus_INDEX] = wachten_WAARDE[lus_INDEX] = 0; return 0;
    }
}
