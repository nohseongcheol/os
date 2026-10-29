// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package दक्षिण_अफ़्रीका.JZafOS.नेटवर्क_स्टैक;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 बाइट_मान 순서와 योगफल_की_जाँच 도구다. */
public final class नेटवर्क_उपकरण {
    private नेटवर्क_उपकरण() {
    }

    public static int 큰순서짧은정수(byte[] आँकड़े, int स्थान) {
        जाँचें_श्रेणी(आँकड़े, स्थान, 2);
        return ((आँकड़े[स्थान] & 0xff) << 8) | (आँकड़े[स्थान + 1] & 0xff);
    }

    public static long बिग_एंडियन_पूर्णांक(byte[] आँकड़े, int स्थान) {
        जाँचें_श्रेणी(आँकड़े, स्थान, 4);
        return ((long) (आँकड़े[स्थान] & 0xff) << 24)
                | ((long) (आँकड़े[स्थान + 1] & 0xff) << 16)
                | ((long) (आँकड़े[स्थान + 2] & 0xff) << 8)
                | (आँकड़े[स्थान + 3] & 0xffL);
    }

    public static int क्लाउड_योगफल_की_जाँच(byte[] आँकड़े, int चलाएँ, int 길이) {
        जाँचें_श्रेणी(आँकड़े, चलाएँ, 길이);
        long 합 = 0;
        int 끝 = चलाएँ + 길이;
        int स्थान = चलाएँ;
        while (स्थान + 1 < 끝) {
            합 += 큰순서짧은정수(आँकड़े, स्थान);
            स्थान += 2;
        }
        if (स्थान < 끝) {
            합 += (आँकड़े[स्थान] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] आँकड़े) {
        return आँकड़े != null && आँकड़े.length >= 14;
    }

    public static int 이더넷상위규약(byte[] आँकड़े) {
        if (!이더넷틀인가(आँकड़े)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(आँकड़े, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] आँकड़े, int स्थान) {
        if (आँकड़े == null || स्थान < 0 || आँकड़े.length - स्थान < 20) {
            return false;
        }
        int संस्करण_मान = (आँकड़े[स्थान] >>> 4) & 0xf;
        int 머리길이 = (आँकड़े[स्थान] & 0xf) * 4;
        return संस्करण_मान == 4 && 머리길이 >= 20 && आँकड़े.length - स्थान >= 머리길이;
    }

    private static void जाँचें_श्रेणी(byte[] आँकड़े, int चलाएँ, int 길이) {
        if (आँकड़े == null || चलाएँ < 0 || 길이 < 0 || चलाएँ > आँकड़े.length - 길이) {
            throw new IllegalArgumentException("नेटवर्क_स्टैक आँकड़े 범위를 벗어났습니다.");
        }
    }
}

