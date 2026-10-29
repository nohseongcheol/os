// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.Nettverk_Stabel;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VALUE 순서와 kontrollsum 도구다. */
public final class Nettverk_Verktøy {
    private Nettverk_Verktøy() {
    }

    public static int 큰순서짧은정수(byte[] data, int Posisjon) {
        범위확인(data, Posisjon, 2);
        return ((data[Posisjon] & 0xff) << 8) | (data[Posisjon + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] data, int Posisjon) {
        범위확인(data, Posisjon, 4);
        return ((long) (data[Posisjon] & 0xff) << 24)
                | ((long) (data[Posisjon + 1] & 0xff) << 16)
                | ((long) (data[Posisjon + 2] & 0xff) << 8)
                | (data[Posisjon + 3] & 0xffL);
    }

    public static int sky_kontrollsum(byte[] data, int Køyr_2, int lengd_VALUE) {
        범위확인(data, Køyr_2, lengd_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Køyr_2 + lengd_VALUE;
        int Posisjon = Køyr_2;
        while (Posisjon + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(data, Posisjon);
            Posisjon += 2;
        }
        if (Posisjon < 끝) {
            SUM_VALUE += (data[Posisjon] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean informasjonsteknologi_Ethernet_rute(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ethernet_UPPER_protokoll(byte[] data) {
        if (!informasjonsteknologi_Ethernet_rute(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] data, int Posisjon) {
        if (data == null || Posisjon < 0 || data.length - Posisjon < 20) {
            return false;
        }
        int versjon_VALUE = (data[Posisjon] >>> 4) & 0xf;
        int hode_lengd = (data[Posisjon] & 0xf) * 4;
        return versjon_VALUE == 4 && hode_lengd >= 20 && data.length - Posisjon >= hode_lengd;
    }

    private static void 범위확인(byte[] data, int Køyr_2, int lengd_VALUE) {
        if (data == null || Køyr_2 < 0 || lengd_VALUE < 0 || Køyr_2 > data.length - lengd_VALUE) {
            throw new IllegalArgumentException("Nettverk_Stabel data 범위를 벗어났습니다.");
        }
    }
}

