// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int san_baha(String Metin) {
        if (Metin == null || Metin.length() == 0) return -1;
        int 결과 = 0;
        for (int indeks = 0; indeks < Metin.length(); indeks++) {
            int baha = Metin.charAt(indeks) - '0';
            if (baha < 0 || baha > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + baha;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int salgy(String Metin) {
        if (Metin == null) return 0;
        int baha = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int indeks = 0; indeks <= Metin.length(); indeks++) {
            int 문자 = indeks == Metin.length() ? '.' : Metin.charAt(indeks);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | baha; 부분++; baha = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                baha = baha * 10 + 문자 - '0';
                if (++자릿수 > 3 || baha > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int Bitir() {
        if (ulanyjy.인수개수() != 3) { ulanyjy.Ýaz("Usage: run udp IP PORT TEXT\n"); return 2; }
        int salgy = salgy(ulanyjy.인수(0)), port_baha = san_baha(ulanyjy.인수(1));
        String Mazmun_baha = ulanyjy.인수(2);
        if (salgy == 0 || port_baha < 1 || Mazmun_baha.length() > 1024) { ulanyjy.Ýaz("Bad destination\n"); return 2; }
        int ryçag_baha = ulanyjy.aç_Tor(0);
        if (ryçag_baha < 0) { ulanyjy.Ýaz("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] maglumat = new int[1024];
        for (int indeks = 0; indeks < Mazmun_baha.length(); indeks++) maglumat[indeks] = Mazmun_baha.charAt(indeks);
        if (ulanyjy.iber_maglumat(ryçag_baha, salgy, port_baha, maglumat, Mazmun_baha.length()) < 0) {
            ulanyjy.Ýaz("UDP SEND FAILED\n"); ulanyjy.ýap_Tor(ryçag_baha); return 4;
        }
        ulanyjy.Ýaz("UDP SENT\n");
        int 받은길이 = ulanyjy.자료받기(ryçag_baha, maglumat, 1500);
        boolean 같음 = 받은길이 == Mazmun_baha.length() && ulanyjy.보낸주소(ryçag_baha) == salgy && ulanyjy.보낸창구(ryçag_baha) == port_baha;
        if (같음) for (int indeks = 0; indeks < 받은길이; indeks++) if (maglumat[indeks] != Mazmun_baha.charAt(indeks)) 같음 = false;
        ulanyjy.ýap_Tor(ryçag_baha);
        if (받은길이 < 0) { ulanyjy.Ýaz("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        ulanyjy.Ýaz(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
