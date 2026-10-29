// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kjerne_VERDI 안의 연결형 byte_VERDI strøm_VERDI. Ethernet/TCP 패킷 스택이 아닌 루프백 socket lag_VERDI. */
public final class strøm_nettverk {
    static int[] status_VERDI = new int[16], port_VERDI = new int[16], 짝 = new int[16], node_port = new int[16], vent_VERDI = new int[16], informasjonssystemer_bundet = new int[16];
    static int[] frontkamera_VERDI = new int[16], nummer = new int[16], data = new int[16 * 1024];
    static int Neste_vare = 50000;
    static int bekrefte(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && status_VERDI[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int portnummer) { for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (status_VERDI[Loop_INDEKS] != 0 && informasjonssystemer_bundet[Loop_INDEKS] != 0 && port_VERDI[Loop_INDEKS] == portnummer) return true; return false; }
    public static int åpne_oppføring() {
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (status_VERDI[Loop_INDEKS] == 0) { status_VERDI[Loop_INDEKS] = 1; node_port[Loop_INDEKS] = port_VERDI[Loop_INDEKS] = frontkamera_VERDI[Loop_INDEKS] = nummer[Loop_INDEKS] = vent_VERDI[Loop_INDEKS] = informasjonssystemer_bundet[Loop_INDEKS] = 0; 짝[Loop_INDEKS] = -1; return Loop_INDEKS + 40; }
        return -24;
    }
    public static int BIND_deltaker(int 열린파일번호, int socket_e_post, int portnummer) {
        int Loop_INDEKS = bekrefte(열린파일번호); if (Loop_INDEKS < 0) return -9;
        if (socket_e_post != 0 && socket_e_post != 0x7f000001) return -99;
        if (status_VERDI[Loop_INDEKS] != 1 || portnummer < 0 || portnummer > 65535) return -22;
        if (portnummer == 0) { do { portnummer = Neste_vare++; if (Neste_vare > 65535) Neste_vare = 50000; } while (사용중(portnummer)); }
        if (사용중(portnummer)) return -98; port_VERDI[Loop_INDEKS] = portnummer; informasjonssystemer_bundet[Loop_INDEKS] = 1; status_VERDI[Loop_INDEKS] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int gjenværende_arbeid) { int Loop_INDEKS = bekrefte(열린파일번호); if (Loop_INDEKS < 0) return -9; if (status_VERDI[Loop_INDEKS] != 2 || gjenværende_arbeid < 1) return -22; status_VERDI[Loop_INDEKS] = 3; return 0; }
    public static int Koble_til(int 열린파일번호, int socket_e_post, int portnummer) {
        int Loop_INDEKS = bekrefte(열린파일번호); if (Loop_INDEKS < 0) return -9; if (socket_e_post != 0x7f000001) return -101;
        if (portnummer < 1 || portnummer > 65535 || status_VERDI[Loop_INDEKS] > 2) return -22;
        int motta_page = -1; for (int indre_kobling_plassere = 0; indre_kobling_plassere < 16; indre_kobling_plassere++) if (status_VERDI[indre_kobling_plassere] == 3 && port_VERDI[indre_kobling_plassere] == portnummer) motta_page = indre_kobling_plassere;
        if (motta_page < 0) return -111;
        int 대기여부 = 0; for (int indre_kobling_plassere = 0; indre_kobling_plassere < 16; indre_kobling_plassere++) if (vent_VERDI[indre_kobling_plassere] == motta_page + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (status_VERDI[Loop_INDEKS] == 1) { int 처리값 = BIND_deltaker(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Annet = åpne_oppføring(); if (Annet < 0) return Annet; Annet -= 40;
        status_VERDI[Loop_INDEKS] = status_VERDI[Annet] = 4; 짝[Loop_INDEKS] = Annet; 짝[Annet] = Loop_INDEKS; port_VERDI[Annet] = portnummer; node_port[Loop_INDEKS] = portnummer; node_port[Annet] = port_VERDI[Loop_INDEKS]; vent_VERDI[Annet] = motta_page + 1; return 0;
    }
    public static int godta_kontakt(int 열린파일번호) { int Loop_INDEKS = bekrefte(열린파일번호); if (Loop_INDEKS < 0) return -9; if (status_VERDI[Loop_INDEKS] != 3) return -22; for (int indre_kobling_plassere = 0; indre_kobling_plassere < 16; indre_kobling_plassere++) if (status_VERDI[indre_kobling_plassere] != 0 && vent_VERDI[indre_kobling_plassere] == Loop_INDEKS + 1) { vent_VERDI[indre_kobling_plassere] = 0; return indre_kobling_plassere + 40; } return -11; }
    public static int Skriv(int 열린파일번호, int oppføring_ANTALL) {
        int Loop_INDEKS = bekrefte(열린파일번호); if (Loop_INDEKS < 0) return -9; if (status_VERDI[Loop_INDEKS] != 4) return -107;
        if (oppføring_ANTALL < 0 || oppføring_ANTALL > 512) return -22; if (oppføring_ANTALL == 0) return 0;
        int indre_kobling_plassere = 짝[Loop_INDEKS]; if (indre_kobling_plassere < 0) return -32; int total_ANTALL = 1024 - nummer[indre_kobling_plassere]; if (total_ANTALL == 0) return -11; if (total_ANTALL > oppføring_ANTALL) total_ANTALL = oppføring_ANTALL;
        for (int Sammenligning_plassere = 0; Sammenligning_plassere < total_ANTALL; Sammenligning_plassere++) data[indre_kobling_plassere * 1024 + (frontkamera_VERDI[indre_kobling_plassere] + nummer[indre_kobling_plassere] + Sammenligning_plassere) % 1024] = tilbakekobling_nettverk.Frem_VERDI[Sammenligning_plassere]; nummer[indre_kobling_plassere] += total_ANTALL; return total_ANTALL;
    }
    public static int Les(int 열린파일번호, int oppføring_ANTALL) {
        int Loop_INDEKS = bekrefte(열린파일번호); if (Loop_INDEKS < 0) return -9; if (status_VERDI[Loop_INDEKS] != 4) return -107; if (oppføring_ANTALL < 0 || oppføring_ANTALL > 512) return -22;
        if (oppføring_ANTALL == 0) return 0; if (nummer[Loop_INDEKS] == 0) return 짝[Loop_INDEKS] < 0 ? 0 : -11; if (oppføring_ANTALL > nummer[Loop_INDEKS]) oppføring_ANTALL = nummer[Loop_INDEKS];
        for (int Sammenligning_plassere = 0; Sammenligning_plassere < oppføring_ANTALL; Sammenligning_plassere++) tilbakekobling_nettverk.Frem_VERDI[Sammenligning_plassere] = data[Loop_INDEKS * 1024 + (frontkamera_VERDI[Loop_INDEKS] + Sammenligning_plassere) % 1024]; frontkamera_VERDI[Loop_INDEKS] = (frontkamera_VERDI[Loop_INDEKS] + oppføring_ANTALL) % 1024; nummer[Loop_INDEKS] -= oppføring_ANTALL; return oppføring_ANTALL;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEKS = bekrefte(열린파일번호); return Loop_INDEKS < 0 ? -9 : port_VERDI[Loop_INDEKS]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEKS = bekrefte(열린파일번호); return Loop_INDEKS < 0 ? -9 : node_port[Loop_INDEKS]; }
    public static int Lukk(int 열린파일번호) {
        int Loop_INDEKS = bekrefte(열린파일번호); if (Loop_INDEKS < 0) return -9;
        if (status_VERDI[Loop_INDEKS] == 3) for (int indre_kobling_plassere = 0; indre_kobling_plassere < 16; indre_kobling_plassere++) if (vent_VERDI[indre_kobling_plassere] == Loop_INDEKS + 1) { if (짝[indre_kobling_plassere] >= 0) 짝[짝[indre_kobling_plassere]] = -1; status_VERDI[indre_kobling_plassere] = vent_VERDI[indre_kobling_plassere] = informasjonssystemer_bundet[indre_kobling_plassere] = 0; }
        if (짝[Loop_INDEKS] >= 0) 짝[짝[Loop_INDEKS]] = -1; status_VERDI[Loop_INDEKS] = informasjonssystemer_bundet[Loop_INDEKS] = nummer[Loop_INDEKS] = vent_VERDI[Loop_INDEKS] = 0; return 0;
    }
}
