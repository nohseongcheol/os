// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ýadro_baha 안의 연결형 baýt_baha Stream_baha. Ethernet/TCP 패킷 스택이 아닌 루프백 socket dereje_baha. */
public final class Stream_Tor {
    static int[] ýagdaý_baha = new int[16], port_baha = new int[16], 짝 = new int[16], deň_derejeli_düwün_port = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], maglumat = new int[16 * 1024];
    static int 다음 = 50000;
    static int barla(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && ýagdaý_baha[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int sikl_indeks = 0; sikl_indeks < 16; sikl_indeks++) if (ýagdaý_baha[sikl_indeks] != 0 && 묶임[sikl_indeks] != 0 && port_baha[sikl_indeks] == 접속번호) return true; return false; }
    public static int döretmek_girizmeklik() {
        for (int sikl_indeks = 0; sikl_indeks < 16; sikl_indeks++) if (ýagdaý_baha[sikl_indeks] == 0) { ýagdaý_baha[sikl_indeks] = 1; deň_derejeli_düwün_port[sikl_indeks] = port_baha[sikl_indeks] = 앞[sikl_indeks] = 수[sikl_indeks] = 대기[sikl_indeks] = 묶임[sikl_indeks] = 0; 짝[sikl_indeks] = -1; return sikl_indeks + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int sikl_indeks = barla(열린파일번호); if (sikl_indeks < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (ýagdaý_baha[sikl_indeks] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; port_baha[sikl_indeks] = 접속번호; 묶임[sikl_indeks] = 1; ýagdaý_baha[sikl_indeks] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int sikl_indeks = barla(열린파일번호); if (sikl_indeks < 0) return -9; if (ýagdaý_baha[sikl_indeks] != 2 || 연결대기한도 < 1) return -22; ýagdaý_baha[sikl_indeks] = 3; return 0; }
    public static int Birikme(int 열린파일번호, int 통신주소, int 접속번호) {
        int sikl_indeks = barla(열린파일번호); if (sikl_indeks < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || ýagdaý_baha[sikl_indeks] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (ýagdaý_baha[안쪽자리] == 3 && port_baha[안쪽자리] == 접속번호) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (ýagdaý_baha[sikl_indeks] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = döretmek_girizmeklik(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        ýagdaý_baha[sikl_indeks] = ýagdaý_baha[다른번호] = 4; 짝[sikl_indeks] = 다른번호; 짝[다른번호] = sikl_indeks; port_baha[다른번호] = 접속번호; deň_derejeli_düwün_port[sikl_indeks] = 접속번호; deň_derejeli_düwün_port[다른번호] = port_baha[sikl_indeks]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int kabul_et_birikme(int 열린파일번호) { int sikl_indeks = barla(열린파일번호); if (sikl_indeks < 0) return -9; if (ýagdaý_baha[sikl_indeks] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (ýagdaý_baha[안쪽자리] != 0 && 대기[안쪽자리] == sikl_indeks + 1) { 대기[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int Ýaz(int 열린파일번호, int 항목수) {
        int sikl_indeks = barla(열린파일번호); if (sikl_indeks < 0) return -9; if (ýagdaý_baha[sikl_indeks] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[sikl_indeks]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) maglumat[안쪽자리 * 1024 + (앞[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.ugrukdyr_baha[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int Oka(int 열린파일번호, int 항목수) {
        int sikl_indeks = barla(열린파일번호); if (sikl_indeks < 0) return -9; if (ýagdaý_baha[sikl_indeks] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[sikl_indeks] == 0) return 짝[sikl_indeks] < 0 ? 0 : -11; if (항목수 > 수[sikl_indeks]) 항목수 = 수[sikl_indeks];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.ugrukdyr_baha[비교자리] = maglumat[sikl_indeks * 1024 + (앞[sikl_indeks] + 비교자리) % 1024]; 앞[sikl_indeks] = (앞[sikl_indeks] + 항목수) % 1024; 수[sikl_indeks] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int sikl_indeks = barla(열린파일번호); return sikl_indeks < 0 ? -9 : port_baha[sikl_indeks]; }
    public static int 상대창구읽기(int 열린파일번호) { int sikl_indeks = barla(열린파일번호); return sikl_indeks < 0 ? -9 : deň_derejeli_düwün_port[sikl_indeks]; }
    public static int Ýap(int 열린파일번호) {
        int sikl_indeks = barla(열린파일번호); if (sikl_indeks < 0) return -9;
        if (ýagdaý_baha[sikl_indeks] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == sikl_indeks + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; ýagdaý_baha[안쪽자리] = 대기[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[sikl_indeks] >= 0) 짝[짝[sikl_indeks]] = -1; ýagdaý_baha[sikl_indeks] = 묶임[sikl_indeks] = 수[sikl_indeks] = 대기[sikl_indeks] = 0; return 0;
    }
}
