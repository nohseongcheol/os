// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turqi.JTurOS.rrjet_Stivë;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bajt_VALUE 순서와 kontrolli_i_shumës 도구다. */
public final class rrjet_Mjete {
    private rrjet_Mjete() {
    }

    public static int 큰순서짧은정수(byte[] të_dhëna, int Pozicioni) {
        범위확인(të_dhëna, Pozicioni, 2);
        return ((të_dhëna[Pozicioni] & 0xff) << 8) | (të_dhëna[Pozicioni + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] të_dhëna, int Pozicioni) {
        범위확인(të_dhëna, Pozicioni, 4);
        return ((long) (të_dhëna[Pozicioni] & 0xff) << 24)
                | ((long) (të_dhëna[Pozicioni + 1] & 0xff) << 16)
                | ((long) (të_dhëna[Pozicioni + 2] & 0xff) << 8)
                | (të_dhëna[Pozicioni + 3] & 0xffL);
    }

    public static int Internet_kontrolli_i_shumës(byte[] të_dhëna, int Ekzekuto, int gjatësi_VALUE) {
        범위확인(të_dhëna, Ekzekuto, gjatësi_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Ekzekuto + gjatësi_VALUE;
        int Pozicioni = Ekzekuto;
        while (Pozicioni + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(të_dhëna, Pozicioni);
            Pozicioni += 2;
        }
        if (Pozicioni < 끝) {
            SUM_VALUE += (të_dhëna[Pozicioni] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean teknologjia_e_informacionit_Eternet_kuadër(byte[] të_dhëna) {
        return të_dhëna != null && të_dhëna.length >= 14;
    }

    public static int Eternet_UPPER_protokoll(byte[] të_dhëna) {
        if (!teknologjia_e_informacionit_Eternet_kuadër(të_dhëna)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(të_dhëna, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] të_dhëna, int Pozicioni) {
        if (të_dhëna == null || Pozicioni < 0 || të_dhëna.length - Pozicioni < 20) {
            return false;
        }
        int version_VALUE = (të_dhëna[Pozicioni] >>> 4) & 0xf;
        int Kreu_gjatësi = (të_dhëna[Pozicioni] & 0xf) * 4;
        return version_VALUE == 4 && Kreu_gjatësi >= 20 && të_dhëna.length - Pozicioni >= Kreu_gjatësi;
    }

    private static void 범위확인(byte[] të_dhëna, int Ekzekuto, int gjatësi_VALUE) {
        if (të_dhëna == null || Ekzekuto < 0 || gjatësi_VALUE < 0 || Ekzekuto > të_dhëna.length - gjatësi_VALUE) {
            throw new IllegalArgumentException("rrjet_Stivë të_dhëna 범위를 벗어났습니다.");
        }
    }
}

