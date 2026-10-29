// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Srbija.JSrbOS.mreža_hrpa;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bajt_VALUE 순서와 kontrolni_zbroj 도구다. */
public final class mreža_Alati {
    private mreža_Alati() {
    }

    public static int 큰순서짧은정수(byte[] podaci, int Položaj) {
        범위확인(podaci, Položaj, 2);
        return ((podaci[Položaj] & 0xff) << 8) | (podaci[Položaj + 1] & 0xff);
    }

    public static long veliki_endijan_cijeli_broj(byte[] podaci, int Položaj) {
        범위확인(podaci, Položaj, 4);
        return ((long) (podaci[Položaj] & 0xff) << 24)
                | ((long) (podaci[Položaj + 1] & 0xff) << 16)
                | ((long) (podaci[Položaj + 2] & 0xff) << 8)
                | (podaci[Položaj + 3] & 0xffL);
    }

    public static int oblak_kontrolni_zbroj(byte[] podaci, int Pokreni, int 길이) {
        범위확인(podaci, Pokreni, 길이);
        long SUM_VALUE = 0;
        int 끝 = Pokreni + 길이;
        int Položaj = Pokreni;
        while (Položaj + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(podaci, Položaj);
            Položaj += 2;
        }
        if (Položaj < 끝) {
            SUM_VALUE += (podaci[Položaj] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean odjel_informacijske_tehnologije_Ethernet_kadar(byte[] podaci) {
        return podaci != null && podaci.length >= 14;
    }

    public static int Ethernet_UPPER_protokol(byte[] podaci) {
        if (!odjel_informacijske_tehnologije_Ethernet_kadar(podaci)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(podaci, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] podaci, int Položaj) {
        if (podaci == null || Položaj < 0 || podaci.length - Položaj < 20) {
            return false;
        }
        int verzija_VALUE = (podaci[Položaj] >>> 4) & 0xf;
        int 머리길이 = (podaci[Položaj] & 0xf) * 4;
        return verzija_VALUE == 4 && 머리길이 >= 20 && podaci.length - Položaj >= 머리길이;
    }

    private static void 범위확인(byte[] podaci, int Pokreni, int 길이) {
        if (podaci == null || Pokreni < 0 || 길이 < 0 || Pokreni > podaci.length - 길이) {
            throw new IllegalArgumentException("mreža_hrpa podaci 범위를 벗어났습니다.");
        }
    }
}

