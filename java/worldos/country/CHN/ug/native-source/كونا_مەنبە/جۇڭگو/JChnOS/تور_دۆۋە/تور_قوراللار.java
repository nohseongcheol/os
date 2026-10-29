// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package جۇڭگو.JChnOS.تور_دۆۋە;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 بايت_قىممىتى 순서와 검사합 도구다. */
public final class تور_قوراللار {
    private تور_قوراللار() {
    }

    public static int 큰순서짧은정수(byte[] مەلۇمات, int ئورۇن) {
        범위확인(مەلۇمات, ئورۇن, 2);
        return ((مەلۇمات[ئورۇن] & 0xff) << 8) | (مەلۇمات[ئورۇن + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] مەلۇمات, int ئورۇن) {
        범위확인(مەلۇمات, ئورۇن, 4);
        return ((long) (مەلۇمات[ئورۇن] & 0xff) << 24)
                | ((long) (مەلۇمات[ئورۇن + 1] & 0xff) << 16)
                | ((long) (مەلۇمات[ئورۇن + 2] & 0xff) << 8)
                | (مەلۇمات[ئورۇن + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] مەلۇمات, int ئىجرا_قىل_2, int ئۇزۇنلۇق_قىممىتى) {
        범위확인(مەلۇمات, ئىجرا_قىل_2, ئۇزۇنلۇق_قىممىتى);
        long 합 = 0;
        int 끝 = ئىجرا_قىل_2 + ئۇزۇنلۇق_قىممىتى;
        int ئورۇن = ئىجرا_قىل_2;
        while (ئورۇن + 1 < 끝) {
            합 += 큰순서짧은정수(مەلۇمات, ئورۇن);
            ئورۇن += 2;
        }
        if (ئورۇن < 끝) {
            합 += (مەلۇمات[ئورۇن] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] مەلۇمات) {
        return مەلۇمات != null && مەلۇمات.length >= 14;
    }

    public static int 이더넷상위규약(byte[] مەلۇمات) {
        if (!이더넷틀인가(مەلۇمات)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(مەلۇمات, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] مەلۇمات, int ئورۇن) {
        if (مەلۇمات == null || ئورۇن < 0 || مەلۇمات.length - ئورۇن < 20) {
            return false;
        }
        int نەشىر_نومۇرى_قىممىتى = (مەلۇمات[ئورۇن] >>> 4) & 0xf;
        int بېشى_ئۇزۇنلۇق = (مەلۇمات[ئورۇن] & 0xf) * 4;
        return نەشىر_نومۇرى_قىممىتى == 4 && بېشى_ئۇزۇنلۇق >= 20 && مەلۇمات.length - ئورۇن >= بېشى_ئۇزۇنلۇق;
    }

    private static void 범위확인(byte[] مەلۇمات, int ئىجرا_قىل_2, int ئۇزۇنلۇق_قىممىتى) {
        if (مەلۇمات == null || ئىجرا_قىل_2 < 0 || ئۇزۇنلۇق_قىممىتى < 0 || ئىجرا_قىل_2 > مەلۇمات.length - ئۇزۇنلۇق_قىممىتى) {
            throw new IllegalArgumentException("تور_دۆۋە مەلۇمات 범위를 벗어났습니다.");
        }
    }
}

