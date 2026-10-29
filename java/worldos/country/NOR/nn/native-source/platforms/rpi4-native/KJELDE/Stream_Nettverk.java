// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kjerne_VALUE 안의 연결형 byte_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket lag_VALUE. */
public final class Stream_Nettverk {
    static int[] status_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], node_port = new int[16], vent_VALUE = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], data = new int[16 * 1024];
    static int Neste_vare = 50000;
    static int stadfeste(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && status_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int portnummer) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (status_VALUE[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == portnummer) return true; return false; }
    public static int Opprett_oppføring() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (status_VALUE[Loop_INDEX] == 0) { status_VALUE[Loop_INDEX] = 1; node_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = 앞[Loop_INDEX] = 수[Loop_INDEX] = vent_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_endepunkt(int 열린파일번호, int 통신주소, int portnummer) {
        int Loop_INDEX = stadfeste(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (status_VALUE[Loop_INDEX] != 1 || portnummer < 0 || portnummer > 65535) return -22;
        if (portnummer == 0) { do { portnummer = Neste_vare++; if (Neste_vare > 65535) Neste_vare = 50000; } while (사용중(portnummer)); }
        if (사용중(portnummer)) return -98; port_VALUE[Loop_INDEX] = portnummer; 묶임[Loop_INDEX] = 1; status_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int lytte_endepunkt(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = stadfeste(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; status_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Kopla_til(int 열린파일번호, int 통신주소, int portnummer) {
        int Loop_INDEX = stadfeste(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (portnummer < 1 || portnummer > 65535 || status_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int indre_kopling_plassere = 0; indre_kopling_plassere < 16; indre_kopling_plassere++) if (status_VALUE[indre_kopling_plassere] == 3 && port_VALUE[indre_kopling_plassere] == portnummer) 수신쪽 = indre_kopling_plassere;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int indre_kopling_plassere = 0; indre_kopling_plassere < 16; indre_kopling_plassere++) if (vent_VALUE[indre_kopling_plassere] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (status_VALUE[Loop_INDEX] == 1) { int 처리값 = BIND_endepunkt(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Opprett_oppføring(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        status_VALUE[Loop_INDEX] = status_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; port_VALUE[다른번호] = portnummer; node_port[Loop_INDEX] = portnummer; node_port[다른번호] = port_VALUE[Loop_INDEX]; vent_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int godta_kontakt(int 열린파일번호) { int Loop_INDEX = stadfeste(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 3) return -22; for (int indre_kopling_plassere = 0; indre_kopling_plassere < 16; indre_kopling_plassere++) if (status_VALUE[indre_kopling_plassere] != 0 && vent_VALUE[indre_kopling_plassere] == Loop_INDEX + 1) { vent_VALUE[indre_kopling_plassere] = 0; return indre_kopling_plassere + 40; } return -11; }
    public static int Skriv(int 열린파일번호, int oppføring_COUNT) {
        int Loop_INDEX = stadfeste(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 4) return -107;
        if (oppføring_COUNT < 0 || oppføring_COUNT > 512) return -22; if (oppføring_COUNT == 0) return 0;
        int indre_kopling_plassere = 짝[Loop_INDEX]; if (indre_kopling_plassere < 0) return -32; int 총수 = 1024 - 수[indre_kopling_plassere]; if (총수 == 0) return -11; if (총수 > oppføring_COUNT) 총수 = oppføring_COUNT;
        for (int Samanlikning_plassere = 0; Samanlikning_plassere < 총수; Samanlikning_plassere++) data[indre_kopling_plassere * 1024 + (앞[indre_kopling_plassere] + 수[indre_kopling_plassere] + Samanlikning_plassere) % 1024] = 되돌림망.Fram_VALUE[Samanlikning_plassere]; 수[indre_kopling_plassere] += 총수; return 총수;
    }
    public static int Les(int 열린파일번호, int oppføring_COUNT) {
        int Loop_INDEX = stadfeste(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 4) return -107; if (oppføring_COUNT < 0 || oppføring_COUNT > 512) return -22;
        if (oppføring_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (oppføring_COUNT > 수[Loop_INDEX]) oppføring_COUNT = 수[Loop_INDEX];
        for (int Samanlikning_plassere = 0; Samanlikning_plassere < oppføring_COUNT; Samanlikning_plassere++) 되돌림망.Fram_VALUE[Samanlikning_plassere] = data[Loop_INDEX * 1024 + (앞[Loop_INDEX] + Samanlikning_plassere) % 1024]; 앞[Loop_INDEX] = (앞[Loop_INDEX] + oppføring_COUNT) % 1024; 수[Loop_INDEX] -= oppføring_COUNT; return oppføring_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = stadfeste(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = stadfeste(열린파일번호); return Loop_INDEX < 0 ? -9 : node_port[Loop_INDEX]; }
    public static int Lukk(int 열린파일번호) {
        int Loop_INDEX = stadfeste(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (status_VALUE[Loop_INDEX] == 3) for (int indre_kopling_plassere = 0; indre_kopling_plassere < 16; indre_kopling_plassere++) if (vent_VALUE[indre_kopling_plassere] == Loop_INDEX + 1) { if (짝[indre_kopling_plassere] >= 0) 짝[짝[indre_kopling_plassere]] = -1; status_VALUE[indre_kopling_plassere] = vent_VALUE[indre_kopling_plassere] = 묶임[indre_kopling_plassere] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; status_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = vent_VALUE[Loop_INDEX] = 0; return 0;
    }
}
