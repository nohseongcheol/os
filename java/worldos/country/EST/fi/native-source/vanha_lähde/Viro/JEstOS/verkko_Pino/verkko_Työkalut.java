// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Viro.JEstOS.verkko_Pino;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 tavu_ARVO 순서와 tarkistussumma 도구다. */
public final class verkko_Työkalut {
    private verkko_Työkalut() {
    }

    public static int 큰순서짧은정수(byte[] data, int paikka) {
        sekki_alue(data, paikka, 2);
        return ((data[paikka] & 0xff) << 8) | (data[paikka + 1] & 0xff);
    }

    public static long big_endian_kokonaisluku(byte[] data, int paikka) {
        sekki_alue(data, paikka, 4);
        return ((long) (data[paikka] & 0xff) << 24)
                | ((long) (data[paikka + 1] & 0xff) << 16)
                | ((long) (data[paikka + 2] & 0xff) << 8)
                | (data[paikka + 3] & 0xffL);
    }

    public static int pilvi_tarkistussumma(byte[] data, int Suorita_2, int kesto_ARVO) {
        sekki_alue(data, Suorita_2, kesto_ARVO);
        long SUM_ARVO = 0;
        int 끝 = Suorita_2 + kesto_ARVO;
        int paikka = Suorita_2;
        while (paikka + 1 < 끝) {
            SUM_ARVO += 큰순서짧은정수(data, paikka);
            paikka += 2;
        }
        if (paikka < 끝) {
            SUM_ARVO += (data[paikka] & 0xff) << 8;
        }
        while ((SUM_ARVO >>> 16) != 0) {
            SUM_ARVO = (SUM_ARVO & 0xffff) + (SUM_ARVO >>> 16);
        }
        return (int) (~SUM_ARVO) & 0xffff;
    }

    public static boolean tietojärjestelmät_Ethernet_kuva(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ethernet_ISOT_protokolla(byte[] data) {
        if (!tietojärjestelmät_Ethernet_kuva(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean tietojärjestelmät_IPV_4_protokolla(byte[] data, int paikka) {
        if (data == null || paikka < 0 || data.length - paikka < 20) {
            return false;
        }
        int versio_ARVO = (data[paikka] >>> 4) & 0xf;
        int otsikko_kesto = (data[paikka] & 0xf) * 4;
        return versio_ARVO == 4 && otsikko_kesto >= 20 && data.length - paikka >= otsikko_kesto;
    }

    private static void sekki_alue(byte[] data, int Suorita_2, int kesto_ARVO) {
        if (data == null || Suorita_2 < 0 || kesto_ARVO < 0 || Suorita_2 > data.length - kesto_ARVO) {
            throw new IllegalArgumentException("verkko_Pino data 범위를 벗어났습니다.");
        }
    }
}

