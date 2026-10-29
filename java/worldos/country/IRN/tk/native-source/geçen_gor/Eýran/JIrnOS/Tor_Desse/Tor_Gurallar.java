// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eýran.JIrnOS.Tor_Desse;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 baýt_baha 순서와 검사합 도구다. */
public final class Tor_Gurallar {
    private Tor_Gurallar() {
    }

    public static int 큰순서짧은정수(byte[] maglumat, int 위치) {
        범위확인(maglumat, 위치, 2);
        return ((maglumat[위치] & 0xff) << 8) | (maglumat[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] maglumat, int 위치) {
        범위확인(maglumat, 위치, 4);
        return ((long) (maglumat[위치] & 0xff) << 24)
                | ((long) (maglumat[위치 + 1] & 0xff) << 16)
                | ((long) (maglumat[위치 + 2] & 0xff) << 8)
                | (maglumat[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] maglumat, int Bitir, int dowamlylyk_baha) {
        범위확인(maglumat, Bitir, dowamlylyk_baha);
        long 합 = 0;
        int 끝 = Bitir + dowamlylyk_baha;
        int 위치 = Bitir;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(maglumat, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (maglumat[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] maglumat) {
        return maglumat != null && maglumat.length >= 14;
    }

    public static int 이더넷상위규약(byte[] maglumat) {
        if (!이더넷틀인가(maglumat)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(maglumat, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] maglumat, int 위치) {
        if (maglumat == null || 위치 < 0 || maglumat.length - 위치 < 20) {
            return false;
        }
        int wersiýa_baha = (maglumat[위치] >>> 4) & 0xf;
        int At_dowamlylyk = (maglumat[위치] & 0xf) * 4;
        return wersiýa_baha == 4 && At_dowamlylyk >= 20 && maglumat.length - 위치 >= At_dowamlylyk;
    }

    private static void 범위확인(byte[] maglumat, int Bitir, int dowamlylyk_baha) {
        if (maglumat == null || Bitir < 0 || dowamlylyk_baha < 0 || Bitir > maglumat.length - dowamlylyk_baha) {
            throw new IllegalArgumentException("Tor_Desse maglumat 범위를 벗어났습니다.");
        }
    }
}

