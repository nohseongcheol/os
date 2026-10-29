// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.ජාලය_කැටිය;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 බයිටය_අගය 순서와 검사합 도구다. */
public final class ජාලය_මෙවලම් {
    private ජාලය_මෙවලම්() {
    }

    public static int 큰순서짧은정수(byte[] දත්ත, int පිහිටීම) {
        범위확인(දත්ත, පිහිටීම, 2);
        return ((දත්ත[පිහිටීම] & 0xff) << 8) | (දත්ත[පිහිටීම + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] දත්ත, int පිහිටීම) {
        범위확인(දත්ත, පිහිටීම, 4);
        return ((long) (දත්ත[පිහිටීම] & 0xff) << 24)
                | ((long) (දත්ත[පිහිටීම + 1] & 0xff) << 16)
                | ((long) (දත්ත[පිහිටීම + 2] & 0xff) << 8)
                | (දත්ත[පිහිටීම + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] දත්ත, int ක්_රියාත්මක_කරන්න_2, int දිග_අගය) {
        범위확인(දත්ත, ක්_රියාත්මක_කරන්න_2, දිග_අගය);
        long 합 = 0;
        int 끝 = ක්_රියාත්මක_කරන්න_2 + දිග_අගය;
        int පිහිටීම = ක්_රියාත්මක_කරන්න_2;
        while (පිහිටීම + 1 < 끝) {
            합 += 큰순서짧은정수(දත්ත, පිහිටීම);
            පිහිටීම += 2;
        }
        if (පිහිටීම < 끝) {
            합 += (දත්ත[පිහිටීම] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] දත්ත) {
        return දත්ත != null && දත්ත.length >= 14;
    }

    public static int 이더넷상위규약(byte[] දත්ත) {
        if (!이더넷틀인가(දත්ත)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(දත්ත, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] දත්ත, int පිහිටීම) {
        if (දත්ත == null || පිහිටීම < 0 || දත්ත.length - පිහිටීම < 20) {
            return false;
        }
        int අනුවාදය_අගය = (දත්ත[පිහිටීම] >>> 4) & 0xf;
        int ශීර්ෂය_දිග = (දත්ත[පිහිටීම] & 0xf) * 4;
        return අනුවාදය_අගය == 4 && ශීර්ෂය_දිග >= 20 && දත්ත.length - පිහිටීම >= ශීර්ෂය_දිග;
    }

    private static void 범위확인(byte[] දත්ත, int ක්_රියාත්මක_කරන්න_2, int දිග_අගය) {
        if (දත්ත == null || ක්_රියාත්මක_කරන්න_2 < 0 || දිග_අගය < 0 || ක්_රියාත්මක_කරන්න_2 > දත්ත.length - දිග_අගය) {
            throw new IllegalArgumentException("ජාලය_කැටිය දත්ත 범위를 벗어났습니다.");
        }
    }
}

