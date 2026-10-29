// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 dereje_baha: 단일 ýadro_baha 안의 IPv4/UDP 루프백 geçir_baha.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * tamamla_utuk 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] port_baha = new int[8];
    static int[] salgy = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] dowamlylyk_baha = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] maglumat = new int[32 * 512];
    static int[] ugrukdyr_baha = new int[512];
    static int 다음창구 = 49152;
    static int barla(int indeks) { return indeks >= 32 && indeks < 40 && 사용[indeks - 32] != 0 ? indeks - 32 : -1; }
    static boolean 겹침(int indeks) {
        for (int ýer_girizmeklik = 0; ýer_girizmeklik < 8; ýer_girizmeklik++) if (사용[ýer_girizmeklik] != 0 && port_baha[ýer_girizmeklik] == indeks) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = 다음창구++;
            if (다음창구 > 65535) 다음창구 = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int döretmek_girizmeklik(int 영역, int 종류, int ýumuş_baha_102996da) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (ýumuş_baha_102996da != 0 && ýumuş_baha_102996da != 17)) return -93;
        for (int ýer_girizmeklik = 0; ýer_girizmeklik < 8; ýer_girizmeklik++) if (사용[ýer_girizmeklik] == 0) {
            사용[ýer_girizmeklik] = 1; port_baha[ýer_girizmeklik] = 0; salgy[ýer_girizmeklik] = 0; 앞[ýer_girizmeklik] = 0; 개수[ýer_girizmeklik] = 0; 받은창구[ýer_girizmeklik] = 0;
            return ýer_girizmeklik + 32;
        }
        return -24;
    }
    public static int 묶기(int indeks, int Tor_salgy, int 창구번호) {
        int ýer_girizmeklik = barla(indeks);
        if (ýer_girizmeklik < 0) return -9;
        if (Tor_salgy != 0 && Tor_salgy != 0x7f000001) return -99;
        if (port_baha[ýer_girizmeklik] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        port_baha[ýer_girizmeklik] = 창구번호; salgy[ýer_girizmeklik] = Tor_salgy; return 0;
    }
    public static int 자료넣기(int indeks, int baha) {
        if (indeks < 0 || indeks >= 512) return -22;
        ugrukdyr_baha[indeks] = baha & 255; return 0;
    }
    public static int 자료읽기(int indeks) { return indeks >= 0 && indeks < 512 ? ugrukdyr_baha[indeks] : -22; }
    public static int iber(int indeks, int Tor_salgy, int 창구번호, int Ululyk) {
        int ýer_girizmeklik = barla(indeks);
        if (ýer_girizmeklik < 0) return -9;
        if (Tor_salgy != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Ululyk < 0 || Ululyk > 512) return -90;
        if (port_baha[ýer_girizmeklik] == 0) {
            int 결과 = 묶기(indeks, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int barylmaly_ýer_baha = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && port_baha[후보] == 창구번호) barylmaly_ýer_baha = 후보;
        if (barylmaly_ýer_baha < 0) return -111;
        if (개수[barylmaly_ýer_baha] == 4) return -11;
        int 자리 = barylmaly_ýer_baha * 4 + (앞[barylmaly_ýer_baha] + 개수[barylmaly_ýer_baha]) % 4;
        for (int baýt_baha = 0; baýt_baha < Ululyk; baýt_baha++) maglumat[자리 * 512 + baýt_baha] = ugrukdyr_baha[baýt_baha];
        dowamlylyk_baha[자리] = Ululyk; 보낸창구[자리] = port_baha[ýer_girizmeklik]; 개수[barylmaly_ýer_baha]++;
        return Ululyk;
    }
    public static int 받기(int indeks, int 용량) {
        int ýer_girizmeklik = barla(indeks);
        if (ýer_girizmeklik < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[ýer_girizmeklik] == 0) return -11;
        int 자리 = ýer_girizmeklik * 4 + 앞[ýer_girizmeklik];
        int Ululyk = dowamlylyk_baha[자리] < 용량 ? dowamlylyk_baha[자리] : 용량;
        for (int baýt_baha = 0; baýt_baha < Ululyk; baýt_baha++) ugrukdyr_baha[baýt_baha] = maglumat[자리 * 512 + baýt_baha];
        받은창구[ýer_girizmeklik] = 보낸창구[자리]; 앞[ýer_girizmeklik] = (앞[ýer_girizmeklik] + 1) % 4; 개수[ýer_girizmeklik]--;
        return Ululyk;
    }
    public static int 창구읽기(int indeks) { int ýer_girizmeklik = barla(indeks); return ýer_girizmeklik < 0 ? -9 : port_baha[ýer_girizmeklik]; }
    public static int 주소읽기(int indeks) { int ýer_girizmeklik = barla(indeks); return ýer_girizmeklik < 0 ? -9 : salgy[ýer_girizmeklik]; }
    public static int 보낸곳(int indeks) { int ýer_girizmeklik = barla(indeks); return ýer_girizmeklik < 0 ? -9 : 받은창구[ýer_girizmeklik]; }
    public static int Ýap(int indeks) {
        int ýer_girizmeklik = barla(indeks); if (ýer_girizmeklik < 0) return -9;
        사용[ýer_girizmeklik] = 0; 개수[ýer_girizmeklik] = 0; port_baha[ýer_girizmeklik] = 0; return 0;
    }
}
