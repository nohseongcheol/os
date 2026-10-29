// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Y_Deyrnas_Unedig.JGbrOS.Rhwydwaith_pentwr;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 beit_VALUE 순서와 prawfswm 도구다. */
public final class Rhwydwaith_Offer {
    private Rhwydwaith_Offer() {
    }

    public static int 큰순서짧은정수(byte[] data, int safle) {
        범위확인(data, safle, 2);
        return ((data[safle] & 0xff) << 8) | (data[safle + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] data, int safle) {
        범위확인(data, safle, 4);
        return ((long) (data[safle] & 0xff) << 24)
                | ((long) (data[safle + 1] & 0xff) << 16)
                | ((long) (data[safle + 2] & 0xff) << 8)
                | (data[safle + 3] & 0xffL);
    }

    public static int cwmwl_prawfswm(byte[] data, int Gweithredu_2, int hyd_VALUE) {
        범위확인(data, Gweithredu_2, hyd_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Gweithredu_2 + hyd_VALUE;
        int safle = Gweithredu_2;
        while (safle + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(data, safle);
            safle += 2;
        }
        if (safle < 끝) {
            SUM_VALUE += (data[safle] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean technoleg_gwybodaeth_Ether_rwyd_ffrâm(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ether_rwyd_UPPER_protocol(byte[] data) {
        if (!technoleg_gwybodaeth_Ether_rwyd_ffrâm(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] data, int safle) {
        if (data == null || safle < 0 || data.length - safle < 20) {
            return false;
        }
        int fersiwn_VALUE = (data[safle] >>> 4) & 0xf;
        int Pennyn_hyd = (data[safle] & 0xf) * 4;
        return fersiwn_VALUE == 4 && Pennyn_hyd >= 20 && data.length - safle >= Pennyn_hyd;
    }

    private static void 범위확인(byte[] data, int Gweithredu_2, int hyd_VALUE) {
        if (data == null || Gweithredu_2 < 0 || hyd_VALUE < 0 || Gweithredu_2 > data.length - hyd_VALUE) {
            throw new IllegalArgumentException("Rhwydwaith_pentwr data 범위를 벗어났습니다.");
        }
    }
}

