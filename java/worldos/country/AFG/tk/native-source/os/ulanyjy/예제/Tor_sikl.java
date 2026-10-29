// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Ululyk/홀수 dowamlylyk_baha 데이터그램으로 hakyky_maglumat RTL8139 수신 sikl_baha 순환을 시험한다. */
public final class Tor_sikl {
    public static int Bitir() {
        if (ulanyjy.인수개수() != 1) { ulanyjy.Ýaz("Usage: run stress PORT\n"); return 2; }
        String Metin = ulanyjy.인수(0);
        int port_baha = 0;
        for (int indeks = 0; indeks < Metin.length(); indeks++) {
            if (Metin.charAt(indeks) < '0' || Metin.charAt(indeks) > '9' || port_baha > 6553) return 2;
            port_baha = port_baha * 10 + Metin.charAt(indeks) - '0';
        }
        if (port_baha < 1 || port_baha > 65535) return 2;
        int ryçag_baha = ulanyjy.aç_Tor(0);
        if (ryçag_baha < 0) return 3;
        int[] maglumat = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int dowamlylyk_baha = 1024 - (회차 & 1);
            for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) maglumat[indeks] = (indeks + 회차) & 255;
            if (ulanyjy.iber_maglumat(ryçag_baha, 0x0a000202, port_baha, maglumat, dowamlylyk_baha) != dowamlylyk_baha) return 4;
            if (ulanyjy.자료받기(ryçag_baha, maglumat, 300) != dowamlylyk_baha) return 5;
            for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) if (maglumat[indeks] != ((indeks + 회차) & 255)) return 6;
        }
        ulanyjy.ýap_Tor(ryçag_baha);
        ulanyjy.Ýaz("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
