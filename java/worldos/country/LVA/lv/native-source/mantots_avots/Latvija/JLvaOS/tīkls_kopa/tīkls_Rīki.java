// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.tīkls_kopa;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VALUE 순서와 kontrolsumma 도구다. */
public final class tīkls_Rīki {
    private tīkls_Rīki() {
    }

    public static int 큰순서짧은정수(byte[] dati, int Novietojums) {
        čeks_diapazons(dati, Novietojums, 2);
        return ((dati[Novietojums] & 0xff) << 8) | (dati[Novietojums + 1] & 0xff);
    }

    public static long resngala_vesels_skaitlis(byte[] dati, int Novietojums) {
        čeks_diapazons(dati, Novietojums, 4);
        return ((long) (dati[Novietojums] & 0xff) << 24)
                | ((long) (dati[Novietojums + 1] & 0xff) << 16)
                | ((long) (dati[Novietojums + 2] & 0xff) << 8)
                | (dati[Novietojums + 3] & 0xffL);
    }

    public static int mākonis_kontrolsumma(byte[] dati, int Palaist, int 길이) {
        čeks_diapazons(dati, Palaist, 길이);
        long SUM_VALUE = 0;
        int 끝 = Palaist + 길이;
        int Novietojums = Palaist;
        while (Novietojums + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(dati, Novietojums);
            Novietojums += 2;
        }
        if (Novietojums < 끝) {
            SUM_VALUE += (dati[Novietojums] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean informācijas_tehnoloģija_Ethernet_kadrs(byte[] dati) {
        return dati != null && dati.length >= 14;
    }

    public static int Ethernet_UPPER_protokols(byte[] dati) {
        if (!informācijas_tehnoloģija_Ethernet_kadrs(dati)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(dati, 12);
    }

    public static boolean informācijas_tehnoloģija_RCN_4_protokols(byte[] dati, int Novietojums) {
        if (dati == null || Novietojums < 0 || dati.length - Novietojums < 20) {
            return false;
        }
        int versija_VALUE = (dati[Novietojums] >>> 4) & 0xf;
        int 머리길이 = (dati[Novietojums] & 0xf) * 4;
        return versija_VALUE == 4 && 머리길이 >= 20 && dati.length - Novietojums >= 머리길이;
    }

    private static void čeks_diapazons(byte[] dati, int Palaist, int 길이) {
        if (dati == null || Palaist < 0 || 길이 < 0 || Palaist > dati.length - 길이) {
            throw new IllegalArgumentException("tīkls_kopa dati 범위를 벗어났습니다.");
        }
    }
}

