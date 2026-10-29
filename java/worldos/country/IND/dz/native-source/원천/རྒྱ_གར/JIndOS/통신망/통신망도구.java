// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package རྒྱ_གར.JIndOS.통신망;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 바이트 순서와 검사합 도구다. */
public final class 통신망도구 {
    private 통신망도구() {
    }

    public static int 큰순서짧은정수(byte[] 자료, int གནས_ས) {
        범위확인(자료, གནས_ས, 2);
        return ((자료[གནས_ས] & 0xff) << 8) | (자료[གནས_ས + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] 자료, int གནས_ས) {
        범위확인(자료, གནས_ས, 4);
        return ((long) (자료[གནས_ས] & 0xff) << 24)
                | ((long) (자료[གནས_ས + 1] & 0xff) << 16)
                | ((long) (자료[གནས_ས + 2] & 0xff) << 8)
                | (자료[གནས_ས + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] 자료, int གཡོག_བཀོལ, int 길이) {
        범위확인(자료, གཡོག_བཀོལ, 길이);
        long 합 = 0;
        int 끝 = གཡོག_བཀོལ + 길이;
        int གནས_ས = གཡོག_བཀོལ;
        while (གནས_ས + 1 < 끝) {
            합 += 큰순서짧은정수(자료, གནས_ས);
            གནས_ས += 2;
        }
        if (གནས_ས < 끝) {
            합 += (자료[གནས_ས] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] 자료) {
        return 자료 != null && 자료.length >= 14;
    }

    public static int 이더넷상위규약(byte[] 자료) {
        if (!이더넷틀인가(자료)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(자료, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] 자료, int གནས_ས) {
        if (자료 == null || གནས_ས < 0 || 자료.length - གནས_ས < 20) {
            return false;
        }
        int 판 = (자료[གནས_ས] >>> 4) & 0xf;
        int 머리길이 = (자료[གནས_ས] & 0xf) * 4;
        return 판 == 4 && 머리길이 >= 20 && 자료.length - གནས_ས >= 머리길이;
    }

    private static void 범위확인(byte[] 자료, int གཡོག_བཀོལ, int 길이) {
        if (자료 == null || གཡོག_བཀོལ < 0 || 길이 < 0 || གཡོག_བཀོལ > 자료.length - 길이) {
            throw new IllegalArgumentException("통신망 자료 범위를 벗어났습니다.");
        }
    }
}

