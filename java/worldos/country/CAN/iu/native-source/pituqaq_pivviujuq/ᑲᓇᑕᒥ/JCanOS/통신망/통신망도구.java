// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.통신망;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_atuutilik 순서와 검사합 도구다. */
public final class 통신망도구 {
    private 통신망도구() {
    }

    public static int 큰순서짧은정수(byte[] titiqqat, int 위치) {
        범위확인(titiqqat, 위치, 2);
        return ((titiqqat[위치] & 0xff) << 8) | (titiqqat[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] titiqqat, int 위치) {
        범위확인(titiqqat, 위치, 4);
        return ((long) (titiqqat[위치] & 0xff) << 24)
                | ((long) (titiqqat[위치 + 1] & 0xff) << 16)
                | ((long) (titiqqat[위치 + 2] & 0xff) << 8)
                | (titiqqat[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] titiqqat, int 시작, int takininga_atuutilik) {
        범위확인(titiqqat, 시작, takininga_atuutilik);
        long 합 = 0;
        int 끝 = 시작 + takininga_atuutilik;
        int 위치 = 시작;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(titiqqat, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (titiqqat[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] titiqqat) {
        return titiqqat != null && titiqqat.length >= 14;
    }

    public static int 이더넷상위규약(byte[] titiqqat) {
        if (!이더넷틀인가(titiqqat)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(titiqqat, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] titiqqat, int 위치) {
        if (titiqqat == null || 위치 < 0 || titiqqat.length - 위치 < 20) {
            return false;
        }
        int imaittuuninga_atuutilik = (titiqqat[위치] >>> 4) & 0xf;
        int Taijaugusinga_takininga = (titiqqat[위치] & 0xf) * 4;
        return imaittuuninga_atuutilik == 4 && Taijaugusinga_takininga >= 20 && titiqqat.length - 위치 >= Taijaugusinga_takininga;
    }

    private static void 범위확인(byte[] titiqqat, int 시작, int takininga_atuutilik) {
        if (titiqqat == null || 시작 < 0 || takininga_atuutilik < 0 || 시작 > titiqqat.length - takininga_atuutilik) {
            throw new IllegalArgumentException("통신망 titiqqat 범위를 벗어났습니다.");
        }
    }
}

