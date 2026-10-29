// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاڪستان.JPakOS.نيٽ_ورڪ_اڀرڻ;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 بائٽ_قدر 순서와 검사합 도구다. */
public final class نيٽ_ورڪ_اوزار {
    private نيٽ_ورڪ_اوزار() {
    }

    public static int 큰순서짧은정수(byte[] ڪوائف, int 위치) {
        범위확인(ڪوائف, 위치, 2);
        return ((ڪوائف[위치] & 0xff) << 8) | (ڪوائف[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ڪوائف, int 위치) {
        범위확인(ڪوائف, 위치, 4);
        return ((long) (ڪوائف[위치] & 0xff) << 24)
                | ((long) (ڪوائف[위치 + 1] & 0xff) << 16)
                | ((long) (ڪوائف[위치 + 2] & 0xff) << 8)
                | (ڪوائف[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] ڪوائف, int هلائڻ, int لمبائي_قدر) {
        범위확인(ڪوائف, هلائڻ, لمبائي_قدر);
        long 합 = 0;
        int 끝 = هلائڻ + لمبائي_قدر;
        int 위치 = هلائڻ;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(ڪوائف, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (ڪوائف[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] ڪوائف) {
        return ڪوائف != null && ڪوائف.length >= 14;
    }

    public static int 이더넷상위규약(byte[] ڪوائف) {
        if (!이더넷틀인가(ڪوائف)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ڪوائف, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ڪوائف, int 위치) {
        if (ڪوائف == null || 위치 < 0 || ڪوائف.length - 위치 < 20) {
            return false;
        }
        int ورزين_قدر = (ڪوائف[위치] >>> 4) & 0xf;
        int هيڊر_لمبائي = (ڪوائف[위치] & 0xf) * 4;
        return ورزين_قدر == 4 && هيڊر_لمبائي >= 20 && ڪوائف.length - 위치 >= هيڊر_لمبائي;
    }

    private static void 범위확인(byte[] ڪوائف, int هلائڻ, int لمبائي_قدر) {
        if (ڪوائف == null || هلائڻ < 0 || لمبائي_قدر < 0 || هلائڻ > ڪوائف.length - لمبائي_قدر) {
            throw new IllegalArgumentException("نيٽ_ورڪ_اڀرڻ ڪوائف 범위를 벗어났습니다.");
        }
    }
}

