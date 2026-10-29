// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Estados_Unidos.JUsaOS.Network_Stack;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VALUE 순서와 checksum 도구다. */
public final class Network_Mga_Tool {
    private Network_Mga_Tool() {
    }

    public static int 큰순서짧은정수(byte[] data, int posisyon) {
        범위확인(data, posisyon, 2);
        return ((data[posisyon] & 0xff) << 8) | (data[posisyon + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] data, int posisyon) {
        범위확인(data, posisyon, 4);
        return ((long) (data[posisyon] & 0xff) << 24)
                | ((long) (data[posisyon + 1] & 0xff) << 16)
                | ((long) (data[posisyon + 2] & 0xff) << 8)
                | (data[posisyon + 3] & 0xffL);
    }

    public static int cloud_checksum(byte[] data, int run, int haba_VALUE) {
        범위확인(data, run, haba_VALUE);
        long SUM_VALUE = 0;
        int 끝 = run + haba_VALUE;
        int posisyon = run;
        while (posisyon + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(data, posisyon);
            posisyon += 2;
        }
        if (posisyon < 끝) {
            SUM_VALUE += (data[posisyon] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean information_technology_Ethernet_frame(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ethernet_UPPER_protokol(byte[] data) {
        if (!information_technology_Ethernet_frame(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] data, int posisyon) {
        if (data == null || posisyon < 0 || data.length - posisyon < 20) {
            return false;
        }
        int bersyon_VALUE = (data[posisyon] >>> 4) & 0xf;
        int Header_haba = (data[posisyon] & 0xf) * 4;
        return bersyon_VALUE == 4 && Header_haba >= 20 && data.length - posisyon >= Header_haba;
    }

    private static void 범위확인(byte[] data, int run, int haba_VALUE) {
        if (data == null || run < 0 || haba_VALUE < 0 || run > data.length - haba_VALUE) {
            throw new IllegalArgumentException("Network_Stack data 범위를 벗어났습니다.");
        }
    }
}

