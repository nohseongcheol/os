// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** khenele_boleng 안의 연결형 paete_boleng Stream_boleng. Ethernet/TCP 패킷 스택이 아닌 루프백 socket llaga_boleng. */
public final class Stream_Netweke {
    static int[] boemo_boleng = new int[16], phote_boleng = new int[16], 짝 = new int[16], sedirišwa_sa_legoro_le_tee_phote = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], data = new int[16 * 1024];
    static int 다음 = 50000;
    static int kgonthiša(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && boemo_boleng[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 16; ditaelopoeletšwa_lokela++) if (boemo_boleng[ditaelopoeletšwa_lokela] != 0 && 묶임[ditaelopoeletšwa_lokela] != 0 && phote_boleng[ditaelopoeletšwa_lokela] == 접속번호) return true; return false; }
    public static int 만들기() {
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 16; ditaelopoeletšwa_lokela++) if (boemo_boleng[ditaelopoeletšwa_lokela] == 0) { boemo_boleng[ditaelopoeletšwa_lokela] = 1; sedirišwa_sa_legoro_le_tee_phote[ditaelopoeletšwa_lokela] = phote_boleng[ditaelopoeletšwa_lokela] = 앞[ditaelopoeletšwa_lokela] = 수[ditaelopoeletšwa_lokela] = 대기[ditaelopoeletšwa_lokela] = 묶임[ditaelopoeletšwa_lokela] = 0; 짝[ditaelopoeletšwa_lokela] = -1; return ditaelopoeletšwa_lokela + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int ditaelopoeletšwa_lokela = kgonthiša(열린파일번호); if (ditaelopoeletšwa_lokela < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (boemo_boleng[ditaelopoeletšwa_lokela] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; phote_boleng[ditaelopoeletšwa_lokela] = 접속번호; 묶임[ditaelopoeletšwa_lokela] = 1; boemo_boleng[ditaelopoeletšwa_lokela] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int ditaelopoeletšwa_lokela = kgonthiša(열린파일번호); if (ditaelopoeletšwa_lokela < 0) return -9; if (boemo_boleng[ditaelopoeletšwa_lokela] != 2 || 연결대기한도 < 1) return -22; boemo_boleng[ditaelopoeletšwa_lokela] = 3; return 0; }
    public static int Ikgokaganye(int 열린파일번호, int 통신주소, int 접속번호) {
        int ditaelopoeletšwa_lokela = kgonthiša(열린파일번호); if (ditaelopoeletšwa_lokela < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || boemo_boleng[ditaelopoeletšwa_lokela] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (boemo_boleng[안쪽자리] == 3 && phote_boleng[안쪽자리] == 접속번호) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (boemo_boleng[ditaelopoeletšwa_lokela] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = 만들기(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        boemo_boleng[ditaelopoeletšwa_lokela] = boemo_boleng[다른번호] = 4; 짝[ditaelopoeletšwa_lokela] = 다른번호; 짝[다른번호] = ditaelopoeletšwa_lokela; phote_boleng[다른번호] = 접속번호; sedirišwa_sa_legoro_le_tee_phote[ditaelopoeletšwa_lokela] = 접속번호; sedirišwa_sa_legoro_le_tee_phote[다른번호] = phote_boleng[ditaelopoeletšwa_lokela]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int amogela_kgokaganya(int 열린파일번호) { int ditaelopoeletšwa_lokela = kgonthiša(열린파일번호); if (ditaelopoeletšwa_lokela < 0) return -9; if (boemo_boleng[ditaelopoeletšwa_lokela] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (boemo_boleng[안쪽자리] != 0 && 대기[안쪽자리] == ditaelopoeletšwa_lokela + 1) { 대기[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int Ngwala(int 열린파일번호, int 항목수) {
        int ditaelopoeletšwa_lokela = kgonthiša(열린파일번호); if (ditaelopoeletšwa_lokela < 0) return -9; if (boemo_boleng[ditaelopoeletšwa_lokela] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[ditaelopoeletšwa_lokela]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) data[안쪽자리 * 1024 + (앞[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.romela_pele_boleng[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int Bala(int 열린파일번호, int 항목수) {
        int ditaelopoeletšwa_lokela = kgonthiša(열린파일번호); if (ditaelopoeletšwa_lokela < 0) return -9; if (boemo_boleng[ditaelopoeletšwa_lokela] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[ditaelopoeletšwa_lokela] == 0) return 짝[ditaelopoeletšwa_lokela] < 0 ? 0 : -11; if (항목수 > 수[ditaelopoeletšwa_lokela]) 항목수 = 수[ditaelopoeletšwa_lokela];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.romela_pele_boleng[비교자리] = data[ditaelopoeletšwa_lokela * 1024 + (앞[ditaelopoeletšwa_lokela] + 비교자리) % 1024]; 앞[ditaelopoeletšwa_lokela] = (앞[ditaelopoeletšwa_lokela] + 항목수) % 1024; 수[ditaelopoeletšwa_lokela] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int ditaelopoeletšwa_lokela = kgonthiša(열린파일번호); return ditaelopoeletšwa_lokela < 0 ? -9 : phote_boleng[ditaelopoeletšwa_lokela]; }
    public static int 상대창구읽기(int 열린파일번호) { int ditaelopoeletšwa_lokela = kgonthiša(열린파일번호); return ditaelopoeletšwa_lokela < 0 ? -9 : sedirišwa_sa_legoro_le_tee_phote[ditaelopoeletšwa_lokela]; }
    public static int Tswalela(int 열린파일번호) {
        int ditaelopoeletšwa_lokela = kgonthiša(열린파일번호); if (ditaelopoeletšwa_lokela < 0) return -9;
        if (boemo_boleng[ditaelopoeletšwa_lokela] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == ditaelopoeletšwa_lokela + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; boemo_boleng[안쪽자리] = 대기[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[ditaelopoeletšwa_lokela] >= 0) 짝[짝[ditaelopoeletšwa_lokela]] = -1; boemo_boleng[ditaelopoeletšwa_lokela] = 묶임[ditaelopoeletšwa_lokela] = 수[ditaelopoeletšwa_lokela] = 대기[ditaelopoeletšwa_lokela] = 0; return 0;
    }
}
