// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kerne_VÆRDI 안의 연결형 byte_VÆRDI strøm_VÆRDI. Ethernet/TCP 패킷 스택이 아닌 루프백 socket lag_VÆRDI. */
public final class strøm_netværk {
    static int[] status_VÆRDI = new int[16], port_VÆRDI = new int[16], 짝 = new int[16], peer_port = new int[16], vent_VÆRDI = new int[16], it_bundet = new int[16];
    static int[] frontvendt_VÆRDI = new int[16], tal = new int[16], data = new int[16 * 1024];
    static int Næste_vare = 50000;
    static int bekræfte(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && status_VÆRDI[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int portnummer) { for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (status_VÆRDI[Loop_INDEKS] != 0 && it_bundet[Loop_INDEKS] != 0 && port_VÆRDI[Loop_INDEKS] == portnummer) return true; return false; }
    public static int åbne_post_81b8d99b() {
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (status_VÆRDI[Loop_INDEKS] == 0) { status_VÆRDI[Loop_INDEKS] = 1; peer_port[Loop_INDEKS] = port_VÆRDI[Loop_INDEKS] = frontvendt_VÆRDI[Loop_INDEKS] = tal[Loop_INDEKS] = vent_VÆRDI[Loop_INDEKS] = it_bundet[Loop_INDEKS] = 0; 짝[Loop_INDEKS] = -1; return Loop_INDEKS + 40; }
        return -24;
    }
    public static int BIND_slutpunkt(int 열린파일번호, int socket_mail, int portnummer) {
        int Loop_INDEKS = bekræfte(열린파일번호); if (Loop_INDEKS < 0) return -9;
        if (socket_mail != 0 && socket_mail != 0x7f000001) return -99;
        if (status_VÆRDI[Loop_INDEKS] != 1 || portnummer < 0 || portnummer > 65535) return -22;
        if (portnummer == 0) { do { portnummer = Næste_vare++; if (Næste_vare > 65535) Næste_vare = 50000; } while (사용중(portnummer)); }
        if (사용중(portnummer)) return -98; port_VÆRDI[Loop_INDEKS] = portnummer; it_bundet[Loop_INDEKS] = 1; status_VÆRDI[Loop_INDEKS] = 2; return 0;
    }
    public static int lytte_slutpunkt(int 열린파일번호, int ordrebeholdning) { int Loop_INDEKS = bekræfte(열린파일번호); if (Loop_INDEKS < 0) return -9; if (status_VÆRDI[Loop_INDEKS] != 2 || ordrebeholdning < 1) return -22; status_VÆRDI[Loop_INDEKS] = 3; return 0; }
    public static int Tilslut(int 열린파일번호, int socket_mail, int portnummer) {
        int Loop_INDEKS = bekræfte(열린파일번호); if (Loop_INDEKS < 0) return -9; if (socket_mail != 0x7f000001) return -101;
        if (portnummer < 1 || portnummer > 65535 || status_VÆRDI[Loop_INDEKS] > 2) return -22;
        int modtage_side = -1; for (int indre_placere = 0; indre_placere < 16; indre_placere++) if (status_VÆRDI[indre_placere] == 3 && port_VÆRDI[indre_placere] == portnummer) modtage_side = indre_placere;
        if (modtage_side < 0) return -111;
        int 대기여부 = 0; for (int indre_placere = 0; indre_placere < 16; indre_placere++) if (vent_VÆRDI[indre_placere] == modtage_side + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (status_VÆRDI[Loop_INDEKS] == 1) { int 처리값 = BIND_slutpunkt(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Andet = åbne_post_81b8d99b(); if (Andet < 0) return Andet; Andet -= 40;
        status_VÆRDI[Loop_INDEKS] = status_VÆRDI[Andet] = 4; 짝[Loop_INDEKS] = Andet; 짝[Andet] = Loop_INDEKS; port_VÆRDI[Andet] = portnummer; peer_port[Loop_INDEKS] = portnummer; peer_port[Andet] = port_VÆRDI[Loop_INDEKS]; vent_VÆRDI[Andet] = modtage_side + 1; return 0;
    }
    public static int acceptere_forbindelse(int 열린파일번호) { int Loop_INDEKS = bekræfte(열린파일번호); if (Loop_INDEKS < 0) return -9; if (status_VÆRDI[Loop_INDEKS] != 3) return -22; for (int indre_placere = 0; indre_placere < 16; indre_placere++) if (status_VÆRDI[indre_placere] != 0 && vent_VÆRDI[indre_placere] == Loop_INDEKS + 1) { vent_VÆRDI[indre_placere] = 0; return indre_placere + 40; } return -11; }
    public static int Skrive(int 열린파일번호, int post_TÆL_8f7753a1) {
        int Loop_INDEKS = bekræfte(열린파일번호); if (Loop_INDEKS < 0) return -9; if (status_VÆRDI[Loop_INDEKS] != 4) return -107;
        if (post_TÆL_8f7753a1 < 0 || post_TÆL_8f7753a1 > 512) return -22; if (post_TÆL_8f7753a1 == 0) return 0;
        int indre_placere = 짝[Loop_INDEKS]; if (indre_placere < 0) return -32; int i_alt_TÆL = 1024 - tal[indre_placere]; if (i_alt_TÆL == 0) return -11; if (i_alt_TÆL > post_TÆL_8f7753a1) i_alt_TÆL = post_TÆL_8f7753a1;
        for (int Sammenligning_placere = 0; Sammenligning_placere < i_alt_TÆL; Sammenligning_placere++) data[indre_placere * 1024 + (frontvendt_VÆRDI[indre_placere] + tal[indre_placere] + Sammenligning_placere) % 1024] = tilbagekobling_netværk.Frem_VÆRDI[Sammenligning_placere]; tal[indre_placere] += i_alt_TÆL; return i_alt_TÆL;
    }
    public static int Læse(int 열린파일번호, int post_TÆL_8f7753a1) {
        int Loop_INDEKS = bekræfte(열린파일번호); if (Loop_INDEKS < 0) return -9; if (status_VÆRDI[Loop_INDEKS] != 4) return -107; if (post_TÆL_8f7753a1 < 0 || post_TÆL_8f7753a1 > 512) return -22;
        if (post_TÆL_8f7753a1 == 0) return 0; if (tal[Loop_INDEKS] == 0) return 짝[Loop_INDEKS] < 0 ? 0 : -11; if (post_TÆL_8f7753a1 > tal[Loop_INDEKS]) post_TÆL_8f7753a1 = tal[Loop_INDEKS];
        for (int Sammenligning_placere = 0; Sammenligning_placere < post_TÆL_8f7753a1; Sammenligning_placere++) tilbagekobling_netværk.Frem_VÆRDI[Sammenligning_placere] = data[Loop_INDEKS * 1024 + (frontvendt_VÆRDI[Loop_INDEKS] + Sammenligning_placere) % 1024]; frontvendt_VÆRDI[Loop_INDEKS] = (frontvendt_VÆRDI[Loop_INDEKS] + post_TÆL_8f7753a1) % 1024; tal[Loop_INDEKS] -= post_TÆL_8f7753a1; return post_TÆL_8f7753a1;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEKS = bekræfte(열린파일번호); return Loop_INDEKS < 0 ? -9 : port_VÆRDI[Loop_INDEKS]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEKS = bekræfte(열린파일번호); return Loop_INDEKS < 0 ? -9 : peer_port[Loop_INDEKS]; }
    public static int Luk(int 열린파일번호) {
        int Loop_INDEKS = bekræfte(열린파일번호); if (Loop_INDEKS < 0) return -9;
        if (status_VÆRDI[Loop_INDEKS] == 3) for (int indre_placere = 0; indre_placere < 16; indre_placere++) if (vent_VÆRDI[indre_placere] == Loop_INDEKS + 1) { if (짝[indre_placere] >= 0) 짝[짝[indre_placere]] = -1; status_VÆRDI[indre_placere] = vent_VÆRDI[indre_placere] = it_bundet[indre_placere] = 0; }
        if (짝[Loop_INDEKS] >= 0) 짝[짝[Loop_INDEKS]] = -1; status_VÆRDI[Loop_INDEKS] = it_bundet[Loop_INDEKS] = tal[Loop_INDEKS] = vent_VÆRDI[Loop_INDEKS] = 0; return 0;
    }
}
