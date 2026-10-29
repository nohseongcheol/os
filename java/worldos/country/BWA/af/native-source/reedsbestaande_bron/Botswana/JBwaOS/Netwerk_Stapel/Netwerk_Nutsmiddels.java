// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.Netwerk_Stapel;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 greep_VALUE 순서와 검사합 도구다. */
public final class Netwerk_Nutsmiddels {
    private Netwerk_Nutsmiddels() {
    }

    public static int 큰순서짧은정수(byte[] data, int Posisie) {
        범위확인(data, Posisie, 2);
        return ((data[Posisie] & 0xff) << 8) | (data[Posisie + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] data, int Posisie) {
        범위확인(data, Posisie, 4);
        return ((long) (data[Posisie] & 0xff) << 24)
                | ((long) (data[Posisie + 1] & 0xff) << 16)
                | ((long) (data[Posisie + 2] & 0xff) << 8)
                | (data[Posisie + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] data, int Loop, int lengte_VALUE) {
        범위확인(data, Loop, lengte_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Loop + lengte_VALUE;
        int Posisie = Loop;
        while (Posisie + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(data, Posisie);
            Posisie += 2;
        }
        if (Posisie < 끝) {
            SUM_VALUE += (data[Posisie] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ethernet_UPPER_protokol(byte[] data) {
        if (!이더넷틀인가(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] data, int Posisie) {
        if (data == null || Posisie < 0 || data.length - Posisie < 20) {
            return false;
        }
        int weergawe_VALUE = (data[Posisie] >>> 4) & 0xf;
        int Loopkop_lengte = (data[Posisie] & 0xf) * 4;
        return weergawe_VALUE == 4 && Loopkop_lengte >= 20 && data.length - Posisie >= Loopkop_lengte;
    }

    private static void 범위확인(byte[] data, int Loop, int lengte_VALUE) {
        if (data == null || Loop < 0 || lengte_VALUE < 0 || Loop > data.length - lengte_VALUE) {
            throw new IllegalArgumentException("Netwerk_Stapel data 범위를 벗어났습니다.");
        }
    }
}

