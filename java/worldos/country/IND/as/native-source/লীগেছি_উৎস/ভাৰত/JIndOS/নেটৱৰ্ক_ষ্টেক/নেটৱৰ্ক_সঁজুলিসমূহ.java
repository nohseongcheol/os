// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.নেটৱৰ্ক_ষ্টেক;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 বাইট_মান 순서와 검사합 도구다. */
public final class নেটৱৰ্ক_সঁজুলিসমূহ {
    private নেটৱৰ্ক_সঁজুলিসমূহ() {
    }

    public static int 큰순서짧은정수(byte[] ডাটা, int অৱস্থান) {
        범위확인(ডাটা, অৱস্থান, 2);
        return ((ডাটা[অৱস্থান] & 0xff) << 8) | (ডাটা[অৱস্থান + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ডাটা, int অৱস্থান) {
        범위확인(ডাটা, অৱস্থান, 4);
        return ((long) (ডাটা[অৱস্থান] & 0xff) << 24)
                | ((long) (ডাটা[অৱস্থান + 1] & 0xff) << 16)
                | ((long) (ডাটা[অৱস্থান + 2] & 0xff) << 8)
                | (ডাটা[অৱস্থান + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] ডাটা, int সঞ্চালন, int দৈর্ঘ্য_মান) {
        범위확인(ডাটা, সঞ্চালন, দৈর্ঘ্য_মান);
        long 합 = 0;
        int 끝 = সঞ্চালন + দৈর্ঘ্য_মান;
        int অৱস্থান = সঞ্চালন;
        while (অৱস্থান + 1 < 끝) {
            합 += 큰순서짧은정수(ডাটা, অৱস্থান);
            অৱস্থান += 2;
        }
        if (অৱস্থান < 끝) {
            합 += (ডাটা[অৱস্থান] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] ডাটা) {
        return ডাটা != null && ডাটা.length >= 14;
    }

    public static int 이더넷상위규약(byte[] ডাটা) {
        if (!이더넷틀인가(ডাটা)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ডাটা, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ডাটা, int অৱস্থান) {
        if (ডাটা == null || অৱস্থান < 0 || ডাটা.length - অৱস্থান < 20) {
            return false;
        }
        int সংস্কৰণ_মান = (ডাটা[অৱস্থান] >>> 4) & 0xf;
        int শিৰো_দৈর্ঘ্য = (ডাটা[অৱস্থান] & 0xf) * 4;
        return সংস্কৰণ_মান == 4 && শিৰো_দৈর্ঘ্য >= 20 && ডাটা.length - অৱস্থান >= শিৰো_দৈর্ঘ্য;
    }

    private static void 범위확인(byte[] ডাটা, int সঞ্চালন, int দৈর্ঘ্য_মান) {
        if (ডাটা == null || সঞ্চালন < 0 || দৈর্ঘ্য_মান < 0 || সঞ্চালন > ডাটা.length - দৈর্ঘ্য_মান) {
            throw new IllegalArgumentException("নেটৱৰ্ক_ষ্টেক ডাটা 범위를 벗어났습니다.");
        }
    }
}

