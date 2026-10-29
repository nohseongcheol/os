// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turska.JTurOS.Mreža_stek;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bajt_VALUE 순서와 kontrolni_zbir 도구다. */
public final class Mreža_Alatke {
    private Mreža_Alatke() {
    }

    public static int 큰순서짧은정수(byte[] podaci, int pozicija) {
        proveriti_opseg(podaci, pozicija, 2);
        return ((podaci[pozicija] & 0xff) << 8) | (podaci[pozicija + 1] & 0xff);
    }

    public static long big_endian_ceo_broj(byte[] podaci, int pozicija) {
        proveriti_opseg(podaci, pozicija, 4);
        return ((long) (podaci[pozicija] & 0xff) << 24)
                | ((long) (podaci[pozicija + 1] & 0xff) << 16)
                | ((long) (podaci[pozicija + 2] & 0xff) << 8)
                | (podaci[pozicija + 3] & 0xffL);
    }

    public static int oblak_kontrolni_zbir(byte[] podaci, int koristiti, int 길이) {
        proveriti_opseg(podaci, koristiti, 길이);
        long SUM_VALUE = 0;
        int 끝 = koristiti + 길이;
        int pozicija = koristiti;
        while (pozicija + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(podaci, pozicija);
            pozicija += 2;
        }
        if (pozicija < 끝) {
            SUM_VALUE += (podaci[pozicija] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean informatičko_odeljenje_Ethernet_kadar(byte[] podaci) {
        return podaci != null && podaci.length >= 14;
    }

    public static int Ethernet_UPPER_protokol(byte[] podaci) {
        if (!informatičko_odeljenje_Ethernet_kadar(podaci)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(podaci, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] podaci, int pozicija) {
        if (podaci == null || pozicija < 0 || podaci.length - pozicija < 20) {
            return false;
        }
        int verzija_VALUE = (podaci[pozicija] >>> 4) & 0xf;
        int 머리길이 = (podaci[pozicija] & 0xf) * 4;
        return verzija_VALUE == 4 && 머리길이 >= 20 && podaci.length - pozicija >= 머리길이;
    }

    private static void proveriti_opseg(byte[] podaci, int koristiti, int 길이) {
        if (podaci == null || koristiti < 0 || 길이 < 0 || koristiti > podaci.length - 길이) {
            throw new IllegalArgumentException("Mreža_stek podaci 범위를 벗어났습니다.");
        }
    }
}

