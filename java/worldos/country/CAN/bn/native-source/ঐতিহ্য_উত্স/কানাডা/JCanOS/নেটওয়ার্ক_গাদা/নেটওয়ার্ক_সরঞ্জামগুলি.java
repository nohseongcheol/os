// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package কানাডা.JCanOS.নেটওয়ার্ক_গাদা;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 বাইট_মান 순서와 চেকসাম 도구다. */
public final class নেটওয়ার্ক_সরঞ্জামগুলি {
    private নেটওয়ার্ক_সরঞ্জামগুলি() {
    }

    public static int 큰순서짧은정수(byte[] ডাটা, int অবস্থান) {
        범위확인(ডাটা, অবস্থান, 2);
        return ((ডাটা[অবস্থান] & 0xff) << 8) | (ডাটা[অবস্থান + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ডাটা, int অবস্থান) {
        범위확인(ডাটা, অবস্থান, 4);
        return ((long) (ডাটা[অবস্থান] & 0xff) << 24)
                | ((long) (ডাটা[অবস্থান + 1] & 0xff) << 16)
                | ((long) (ডাটা[অবস্থান + 2] & 0xff) << 8)
                | (ডাটা[অবস্থান + 3] & 0xffL);
    }

    public static int ক্লাউড_চেকসাম(byte[] ডাটা, int চালনা, int দৈর্ঘ্য_মান) {
        범위확인(ডাটা, চালনা, দৈর্ঘ্য_মান);
        long 합 = 0;
        int 끝 = চালনা + দৈর্ঘ্য_মান;
        int অবস্থান = চালনা;
        while (অবস্থান + 1 < 끝) {
            합 += 큰순서짧은정수(ডাটা, অবস্থান);
            অবস্থান += 2;
        }
        if (অবস্থান < 끝) {
            합 += (ডাটা[অবস্থান] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean তথ্য_প্রযুক্তি_ইথারনেট_ফ্রেম(byte[] ডাটা) {
        return ডাটা != null && ডাটা.length >= 14;
    }

    public static int 이더넷상위규약(byte[] ডাটা) {
        if (!তথ্য_প্রযুক্তি_ইথারনেট_ফ্রেম(ডাটা)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ডাটা, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ডাটা, int অবস্থান) {
        if (ডাটা == null || অবস্থান < 0 || ডাটা.length - অবস্থান < 20) {
            return false;
        }
        int সংস্করণ_মান = (ডাটা[অবস্থান] >>> 4) & 0xf;
        int হেডার_দৈর্ঘ্য = (ডাটা[অবস্থান] & 0xf) * 4;
        return সংস্করণ_মান == 4 && হেডার_দৈর্ঘ্য >= 20 && ডাটা.length - অবস্থান >= হেডার_দৈর্ঘ্য;
    }

    private static void 범위확인(byte[] ডাটা, int চালনা, int দৈর্ঘ্য_মান) {
        if (ডাটা == null || চালনা < 0 || দৈর্ঘ্য_মান < 0 || চালনা > ডাটা.length - দৈর্ঘ্য_মান) {
            throw new IllegalArgumentException("নেটওয়ার্ক_গাদা ডাটা 범위를 벗어났습니다.");
        }
    }
}

