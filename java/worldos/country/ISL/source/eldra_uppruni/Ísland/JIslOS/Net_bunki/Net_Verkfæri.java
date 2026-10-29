// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.Net_bunki;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bæti_VALUE 순서와 prófsumma 도구다. */
public final class Net_Verkfæri {
    private Net_Verkfæri() {
    }

    public static int 큰순서짧은정수(byte[] gögn, int Staðsetning) {
        범위확인(gögn, Staðsetning, 2);
        return ((gögn[Staðsetning] & 0xff) << 8) | (gögn[Staðsetning + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] gögn, int Staðsetning) {
        범위확인(gögn, Staðsetning, 4);
        return ((long) (gögn[Staðsetning] & 0xff) << 24)
                | ((long) (gögn[Staðsetning + 1] & 0xff) << 16)
                | ((long) (gögn[Staðsetning + 2] & 0xff) << 8)
                | (gögn[Staðsetning + 3] & 0xffL);
    }

    public static int skýið_prófsumma(byte[] gögn, int Keyra_2, int lengd_VALUE) {
        범위확인(gögn, Keyra_2, lengd_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Keyra_2 + lengd_VALUE;
        int Staðsetning = Keyra_2;
        while (Staðsetning + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(gögn, Staðsetning);
            Staðsetning += 2;
        }
        if (Staðsetning < 끝) {
            SUM_VALUE += (gögn[Staðsetning] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean upplýsingatækni_Ethernet_ramma(byte[] gögn) {
        return gögn != null && gögn.length >= 14;
    }

    public static int Ethernet_UPPER_samskiptaregla(byte[] gögn) {
        if (!upplýsingatækni_Ethernet_ramma(gögn)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(gögn, 12);
    }

    public static boolean upplýsingatækni_verðfrávik_reiknings_4_samskiptaregla(byte[] gögn, int Staðsetning) {
        if (gögn == null || Staðsetning < 0 || gögn.length - Staðsetning < 20) {
            return false;
        }
        int útgáfa_VALUE = (gögn[Staðsetning] >>> 4) & 0xf;
        int Haus_lengd = (gögn[Staðsetning] & 0xf) * 4;
        return útgáfa_VALUE == 4 && Haus_lengd >= 20 && gögn.length - Staðsetning >= Haus_lengd;
    }

    private static void 범위확인(byte[] gögn, int Keyra_2, int lengd_VALUE) {
        if (gögn == null || Keyra_2 < 0 || lengd_VALUE < 0 || Keyra_2 > gögn.length - lengd_VALUE) {
            throw new IllegalArgumentException("Net_bunki gögn 범위를 벗어났습니다.");
        }
    }
}

