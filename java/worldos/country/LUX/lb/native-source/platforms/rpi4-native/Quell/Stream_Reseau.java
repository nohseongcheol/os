// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Kernel_VALUE 안의 연결형 Byte_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket Layer_VALUE. */
public final class Stream_Reseau {
    static int[] Status_VALUE = new int[16], Port_VALUE = new int[16], 짝 = new int[16], Peer_Port = new int[16], Waart_VALUE = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], Daten = new int[16 * 1024];
    static int Weider_Element = 50000;
    static int verifizéieren(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Status_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Status_VALUE[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && Port_VALUE[Loop_INDEX] == 접속번호) return true; return false; }
    public static int Create_Agab() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Status_VALUE[Loop_INDEX] == 0) { Status_VALUE[Loop_INDEX] = 1; Peer_Port[Loop_INDEX] = Port_VALUE[Loop_INDEX] = 앞[Loop_INDEX] = 수[Loop_INDEX] = Waart_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = verifizéieren(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Status_VALUE[Loop_INDEX] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = Weider_Element++; if (Weider_Element > 65535) Weider_Element = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; Port_VALUE[Loop_INDEX] = 접속번호; 묶임[Loop_INDEX] = 1; Status_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = verifizéieren(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; Status_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Verbannen(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = verifizéieren(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || Status_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 16; intern_Verknëppung_positionéieren++) if (Status_VALUE[intern_Verknëppung_positionéieren] == 3 && Port_VALUE[intern_Verknëppung_positionéieren] == 접속번호) 수신쪽 = intern_Verknëppung_positionéieren;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 16; intern_Verknëppung_positionéieren++) if (Waart_VALUE[intern_Verknëppung_positionéieren] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Status_VALUE[Loop_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Create_Agab(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        Status_VALUE[Loop_INDEX] = Status_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; Port_VALUE[다른번호] = 접속번호; Peer_Port[Loop_INDEX] = 접속번호; Peer_Port[다른번호] = Port_VALUE[Loop_INDEX]; Waart_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int acceptéieren_Verbindung(int 열린파일번호) { int Loop_INDEX = verifizéieren(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 3) return -22; for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 16; intern_Verknëppung_positionéieren++) if (Status_VALUE[intern_Verknëppung_positionéieren] != 0 && Waart_VALUE[intern_Verknëppung_positionéieren] == Loop_INDEX + 1) { Waart_VALUE[intern_Verknëppung_positionéieren] = 0; return intern_Verknëppung_positionéieren + 40; } return -11; }
    public static int schreiwen(int 열린파일번호, int Agab_COUNT) {
        int Loop_INDEX = verifizéieren(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 4) return -107;
        if (Agab_COUNT < 0 || Agab_COUNT > 512) return -22; if (Agab_COUNT == 0) return 0;
        int intern_Verknëppung_positionéieren = 짝[Loop_INDEX]; if (intern_Verknëppung_positionéieren < 0) return -32; int 총수 = 1024 - 수[intern_Verknëppung_positionéieren]; if (총수 == 0) return -11; if (총수 > Agab_COUNT) 총수 = Agab_COUNT;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) Daten[intern_Verknëppung_positionéieren * 1024 + (앞[intern_Verknëppung_positionéieren] + 수[intern_Verknëppung_positionéieren] + 비교자리) % 1024] = 되돌림망.Virun_VALUE[비교자리]; 수[intern_Verknëppung_positionéieren] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int Agab_COUNT) {
        int Loop_INDEX = verifizéieren(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 4) return -107; if (Agab_COUNT < 0 || Agab_COUNT > 512) return -22;
        if (Agab_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (Agab_COUNT > 수[Loop_INDEX]) Agab_COUNT = 수[Loop_INDEX];
        for (int 비교자리 = 0; 비교자리 < Agab_COUNT; 비교자리++) 되돌림망.Virun_VALUE[비교자리] = Daten[Loop_INDEX * 1024 + (앞[Loop_INDEX] + 비교자리) % 1024]; 앞[Loop_INDEX] = (앞[Loop_INDEX] + Agab_COUNT) % 1024; 수[Loop_INDEX] -= Agab_COUNT; return Agab_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = verifizéieren(열린파일번호); return Loop_INDEX < 0 ? -9 : Port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = verifizéieren(열린파일번호); return Loop_INDEX < 0 ? -9 : Peer_Port[Loop_INDEX]; }
    public static int Clôture(int 열린파일번호) {
        int Loop_INDEX = verifizéieren(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Status_VALUE[Loop_INDEX] == 3) for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 16; intern_Verknëppung_positionéieren++) if (Waart_VALUE[intern_Verknëppung_positionéieren] == Loop_INDEX + 1) { if (짝[intern_Verknëppung_positionéieren] >= 0) 짝[짝[intern_Verknëppung_positionéieren]] = -1; Status_VALUE[intern_Verknëppung_positionéieren] = Waart_VALUE[intern_Verknëppung_positionéieren] = 묶임[intern_Verknëppung_positionéieren] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Status_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = Waart_VALUE[Loop_INDEX] = 0; return 0;
    }
}
