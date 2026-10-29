// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Uganda.JUgaOS.Mtandao_Mpororo;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 baiti_thamani 순서와 jumla 도구다. */
public final class Mtandao_Zana {
    private Mtandao_Zana() {
    }

    public static int 큰순서짧은정수(byte[] data, int 위치) {
        범위확인(data, 위치, 2);
        return ((data[위치] & 0xff) << 8) | (data[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] data, int 위치) {
        범위확인(data, 위치, 4);
        return ((long) (data[위치] & 0xff) << 24)
                | ((long) (data[위치 + 1] & 0xff) << 16)
                | ((long) (data[위치 + 2] & 0xff) << 8)
                | (data[위치 + 3] & 0xffL);
    }

    public static int wingu_jumla(byte[] data, int endesha, int urefu_thamani) {
        범위확인(data, endesha, urefu_thamani);
        long 합 = 0;
        int 끝 = endesha + urefu_thamani;
        int 위치 = endesha;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(data, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (data[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean teknolojia_ya_maelezo_Ethaneti_fremu(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int 이더넷상위규약(byte[] data) {
        if (!teknolojia_ya_maelezo_Ethaneti_fremu(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] data, int 위치) {
        if (data == null || 위치 < 0 || data.length - 위치 < 20) {
            return false;
        }
        int toleo_thamani = (data[위치] >>> 4) & 0xf;
        int kichwa_urefu = (data[위치] & 0xf) * 4;
        return toleo_thamani == 4 && kichwa_urefu >= 20 && data.length - 위치 >= kichwa_urefu;
    }

    private static void 범위확인(byte[] data, int endesha, int urefu_thamani) {
        if (data == null || endesha < 0 || urefu_thamani < 0 || endesha > data.length - urefu_thamani) {
            throw new IllegalArgumentException("Mtandao_Mpororo data 범위를 벗어났습니다.");
        }
    }
}

