// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.نیٹ_ورک_گٹھا;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 بائٹ_قدر 순서와 검사합 도구다. */
public final class نیٹ_ورک_اوزار {
    private نیٹ_ورک_اوزار() {
    }

    public static int 큰순서짧은정수(byte[] کوائف, int 위치) {
        범위확인(کوائف, 위치, 2);
        return ((کوائف[위치] & 0xff) << 8) | (کوائف[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] کوائف, int 위치) {
        범위확인(کوائف, 위치, 4);
        return ((long) (کوائف[위치] & 0xff) << 24)
                | ((long) (کوائف[위치 + 1] & 0xff) << 16)
                | ((long) (کوائف[위치 + 2] & 0xff) << 8)
                | (کوائف[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] کوائف, int چلاؤ, int لمبائی_قدر) {
        범위확인(کوائف, چلاؤ, لمبائی_قدر);
        long 합 = 0;
        int 끝 = چلاؤ + لمبائی_قدر;
        int 위치 = چلاؤ;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(کوائف, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (کوائف[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] کوائف) {
        return کوائف != null && کوائف.length >= 14;
    }

    public static int 이더넷상위규약(byte[] کوائف) {
        if (!이더넷틀인가(کوائف)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(کوائف, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] کوائف, int 위치) {
        if (کوائف == null || 위치 < 0 || کوائف.length - 위치 < 20) {
            return false;
        }
        int ورژن_قدر = (کوائف[위치] >>> 4) & 0xf;
        int سرتحریر_لمبائی = (کوائف[위치] & 0xf) * 4;
        return ورژن_قدر == 4 && سرتحریر_لمبائی >= 20 && کوائف.length - 위치 >= سرتحریر_لمبائی;
    }

    private static void 범위확인(byte[] کوائف, int چلاؤ, int لمبائی_قدر) {
        if (کوائف == null || چلاؤ < 0 || لمبائی_قدر < 0 || چلاؤ > کوائف.length - لمبائی_قدر) {
            throw new IllegalArgumentException("نیٹ_ورک_گٹھا کوائف 범위를 벗어났습니다.");
        }
    }
}

