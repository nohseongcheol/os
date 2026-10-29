// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.통신망;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 waai_ajutuu 순서와 검사합 도구다. */
public final class 통신망도구 {
    private 통신망도구() {
    }

    public static int 큰순서짧은정수(byte[] atijaaya, int 위치) {
        범위확인(atijaaya, 위치, 2);
        return ((atijaaya[위치] & 0xff) << 8) | (atijaaya[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] atijaaya, int 위치) {
        범위확인(atijaaya, 위치, 4);
        return ((long) (atijaaya[위치] & 0xff) << 24)
                | ((long) (atijaaya[위치 + 1] & 0xff) << 16)
                | ((long) (atijaaya[위치 + 2] & 0xff) << 8)
                | (atijaaya[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] atijaaya, int 시작, int akaliaa_ajutuu) {
        범위확인(atijaaya, 시작, akaliaa_ajutuu);
        long 합 = 0;
        int 끝 = 시작 + akaliaa_ajutuu;
        int 위치 = 시작;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(atijaaya, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (atijaaya[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] atijaaya) {
        return atijaaya != null && atijaaya.length >= 14;
    }

    public static int 이더넷상위규약(byte[] atijaaya) {
        if (!이더넷틀인가(atijaaya)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(atijaaya, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] atijaaya, int 위치) {
        if (atijaaya == null || 위치 < 0 || atijaaya.length - 위치 < 20) {
            return false;
        }
        int 판 = (atijaaya[위치] >>> 4) & 0xf;
        int o_ttiakii_akaliaa = (atijaaya[위치] & 0xf) * 4;
        return 판 == 4 && o_ttiakii_akaliaa >= 20 && atijaaya.length - 위치 >= o_ttiakii_akaliaa;
    }

    private static void 범위확인(byte[] atijaaya, int 시작, int akaliaa_ajutuu) {
        if (atijaaya == null || 시작 < 0 || akaliaa_ajutuu < 0 || 시작 > atijaaya.length - akaliaa_ajutuu) {
            throw new IllegalArgumentException("통신망 atijaaya 범위를 벗어났습니다.");
        }
    }
}

