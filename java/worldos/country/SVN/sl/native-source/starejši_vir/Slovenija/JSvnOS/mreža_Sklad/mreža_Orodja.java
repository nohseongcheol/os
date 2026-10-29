// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.mreža_Sklad;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bajt_VALUE 순서와 kontrolna_vsota 도구다. */
public final class mreža_Orodja {
    private mreža_Orodja() {
    }

    public static int 큰순서짧은정수(byte[] podatki, int Položaj) {
        preveriti_obseg(podatki, Položaj, 2);
        return ((podatki[Položaj] & 0xff) << 8) | (podatki[Položaj + 1] & 0xff);
    }

    public static long big_endian_celo_število(byte[] podatki, int Položaj) {
        preveriti_obseg(podatki, Položaj, 4);
        return ((long) (podatki[Položaj] & 0xff) << 24)
                | ((long) (podatki[Položaj + 1] & 0xff) << 16)
                | ((long) (podatki[Položaj + 2] & 0xff) << 8)
                | (podatki[Položaj + 3] & 0xffL);
    }

    public static int oblak_kontrolna_vsota(byte[] podatki, int Zaženi, int 길이) {
        preveriti_obseg(podatki, Zaženi, 길이);
        long SUM_VALUE = 0;
        int 끝 = Zaženi + 길이;
        int Položaj = Zaženi;
        while (Položaj + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(podatki, Položaj);
            Položaj += 2;
        }
        if (Položaj < 끝) {
            SUM_VALUE += (podatki[Položaj] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean informacijska_tehnologija_ethernet_okvir(byte[] podatki) {
        return podatki != null && podatki.length >= 14;
    }

    public static int ethernet_UPPER_protokol(byte[] podatki) {
        if (!informacijska_tehnologija_ethernet_okvir(podatki)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(podatki, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] podatki, int Položaj) {
        if (podatki == null || Položaj < 0 || podatki.length - Položaj < 20) {
            return false;
        }
        int različica_VALUE = (podatki[Položaj] >>> 4) & 0xf;
        int 머리길이 = (podatki[Položaj] & 0xf) * 4;
        return različica_VALUE == 4 && 머리길이 >= 20 && podatki.length - Položaj >= 머리길이;
    }

    private static void preveriti_obseg(byte[] podatki, int Zaženi, int 길이) {
        if (podatki == null || Zaženi < 0 || 길이 < 0 || Zaženi > podatki.length - 길이) {
            throw new IllegalArgumentException("mreža_Sklad podatki 범위를 벗어났습니다.");
        }
    }
}

