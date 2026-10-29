// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.Mreža_snop;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bajt_VALUE 순서와 kontrolni_zbir 도구다. */
public final class Mreža_Alati {
    private Mreža_Alati() {
    }

    public static int 큰순서짧은정수(byte[] podaci, int Pozicija) {
        범위확인(podaci, Pozicija, 2);
        return ((podaci[Pozicija] & 0xff) << 8) | (podaci[Pozicija + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] podaci, int Pozicija) {
        범위확인(podaci, Pozicija, 4);
        return ((long) (podaci[Pozicija] & 0xff) << 24)
                | ((long) (podaci[Pozicija + 1] & 0xff) << 16)
                | ((long) (podaci[Pozicija + 2] & 0xff) << 8)
                | (podaci[Pozicija + 3] & 0xffL);
    }

    public static int oblak_kontrolni_zbir(byte[] podaci, int Pokreni, int dužina_VALUE) {
        범위확인(podaci, Pokreni, dužina_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Pokreni + dužina_VALUE;
        int Pozicija = Pokreni;
        while (Pozicija + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(podaci, Pozicija);
            Pozicija += 2;
        }
        if (Pozicija < 끝) {
            SUM_VALUE += (podaci[Pozicija] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean odjel_za_informacijske_tehnologije_Ethernet_kadar(byte[] podaci) {
        return podaci != null && podaci.length >= 14;
    }

    public static int Ethernet_UPPER_protokol(byte[] podaci) {
        if (!odjel_za_informacijske_tehnologije_Ethernet_kadar(podaci)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(podaci, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] podaci, int Pozicija) {
        if (podaci == null || Pozicija < 0 || podaci.length - Pozicija < 20) {
            return false;
        }
        int verzija_VALUE = (podaci[Pozicija] >>> 4) & 0xf;
        int Zaglavlje_dužina = (podaci[Pozicija] & 0xf) * 4;
        return verzija_VALUE == 4 && Zaglavlje_dužina >= 20 && podaci.length - Pozicija >= Zaglavlje_dužina;
    }

    private static void 범위확인(byte[] podaci, int Pokreni, int dužina_VALUE) {
        if (podaci == null || Pokreni < 0 || dužina_VALUE < 0 || Pokreni > podaci.length - dužina_VALUE) {
            throw new IllegalArgumentException("Mreža_snop podaci 범위를 벗어났습니다.");
        }
    }
}

