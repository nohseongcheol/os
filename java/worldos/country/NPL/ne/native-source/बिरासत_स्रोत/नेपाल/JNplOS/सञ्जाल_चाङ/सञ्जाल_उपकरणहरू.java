// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाल.JNplOS.सञ्जाल_चाङ;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 बाइट_मान 순서와 검사합 도구다. */
public final class सञ्जाल_उपकरणहरू {
    private सञ्जाल_उपकरणहरू() {
    }

    public static int 큰순서짧은정수(byte[] लगत, int स्थिति) {
        범위확인(लगत, स्थिति, 2);
        return ((लगत[स्थिति] & 0xff) << 8) | (लगत[स्थिति + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] लगत, int स्थिति) {
        범위확인(लगत, स्थिति, 4);
        return ((long) (लगत[स्थिति] & 0xff) << 24)
                | ((long) (लगत[स्थिति + 1] & 0xff) << 16)
                | ((long) (लगत[स्थिति + 2] & 0xff) << 8)
                | (लगत[स्थिति + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] लगत, int चलाउनुहोस्, int लम्बाइ_मान) {
        범위확인(लगत, चलाउनुहोस्, लम्बाइ_मान);
        long 합 = 0;
        int 끝 = चलाउनुहोस् + लम्बाइ_मान;
        int स्थिति = चलाउनुहोस्;
        while (स्थिति + 1 < 끝) {
            합 += 큰순서짧은정수(लगत, स्थिति);
            स्थिति += 2;
        }
        if (स्थिति < 끝) {
            합 += (लगत[स्थिति] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] लगत) {
        return लगत != null && लगत.length >= 14;
    }

    public static int 이더넷상위규약(byte[] लगत) {
        if (!이더넷틀인가(लगत)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(लगत, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] लगत, int स्थिति) {
        if (लगत == null || स्थिति < 0 || लगत.length - स्थिति < 20) {
            return false;
        }
        int संस्करण_मान = (लगत[स्थिति] >>> 4) & 0xf;
        int हेडर_लम्बाइ = (लगत[स्थिति] & 0xf) * 4;
        return संस्करण_मान == 4 && हेडर_लम्बाइ >= 20 && लगत.length - स्थिति >= हेडर_लम्बाइ;
    }

    private static void 범위확인(byte[] लगत, int चलाउनुहोस्, int लम्बाइ_मान) {
        if (लगत == null || चलाउनुहोस् < 0 || लम्बाइ_मान < 0 || चलाउनुहोस् > लगत.length - लम्बाइ_मान) {
            throw new IllegalArgumentException("सञ्जाल_चाङ लगत 범위를 벗어났습니다.");
        }
    }
}

