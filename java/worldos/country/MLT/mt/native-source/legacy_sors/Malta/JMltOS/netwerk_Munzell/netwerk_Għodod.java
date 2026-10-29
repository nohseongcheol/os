// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.netwerk_Munzell;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VALUE 순서와 검사합 도구다. */
public final class netwerk_Għodod {
    private netwerk_Għodod() {
    }

    public static int 큰순서짧은정수(byte[] data, int pożizzjoni) {
        범위확인(data, pożizzjoni, 2);
        return ((data[pożizzjoni] & 0xff) << 8) | (data[pożizzjoni + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] data, int pożizzjoni) {
        범위확인(data, pożizzjoni, 4);
        return ((long) (data[pożizzjoni] & 0xff) << 24)
                | ((long) (data[pożizzjoni + 1] & 0xff) << 16)
                | ((long) (data[pożizzjoni + 2] & 0xff) << 8)
                | (data[pożizzjoni + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] data, int serje, int tul_VALUE) {
        범위확인(data, serje, tul_VALUE);
        long SUM_VALUE = 0;
        int 끝 = serje + tul_VALUE;
        int pożizzjoni = serje;
        while (pożizzjoni + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(data, pożizzjoni);
            pożizzjoni += 2;
        }
        if (pożizzjoni < 끝) {
            SUM_VALUE += (data[pożizzjoni] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ethernet_UPPER_protokoll(byte[] data) {
        if (!이더넷틀인가(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] data, int pożizzjoni) {
        if (data == null || pożizzjoni < 0 || data.length - pożizzjoni < 20) {
            return false;
        }
        int verżjoni_VALUE = (data[pożizzjoni] >>> 4) & 0xf;
        int Intestazzjoni_tul = (data[pożizzjoni] & 0xf) * 4;
        return verżjoni_VALUE == 4 && Intestazzjoni_tul >= 20 && data.length - pożizzjoni >= Intestazzjoni_tul;
    }

    private static void 범위확인(byte[] data, int serje, int tul_VALUE) {
        if (data == null || serje < 0 || tul_VALUE < 0 || serje > data.length - tul_VALUE) {
            throw new IllegalArgumentException("netwerk_Munzell data 범위를 벗어났습니다.");
        }
    }
}

