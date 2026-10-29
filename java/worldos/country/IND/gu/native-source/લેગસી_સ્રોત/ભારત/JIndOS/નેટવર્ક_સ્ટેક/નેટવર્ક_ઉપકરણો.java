// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ભારત.JIndOS.નેટવર્ક_સ્ટેક;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 બાઇટ_મૂલ્ય 순서와 ચેકસમ 도구다. */
public final class નેટવર્ક_ઉપકરણો {
    private નેટવર્ક_ઉપકરણો() {
    }

    public static int 큰순서짧은정수(byte[] ડેટા, int સ્થાન) {
        범위확인(ડેટા, સ્થાન, 2);
        return ((ડેટા[સ્થાન] & 0xff) << 8) | (ડેટા[સ્થાન + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ડેટા, int સ્થાન) {
        범위확인(ડેટા, સ્થાન, 4);
        return ((long) (ડેટા[સ્થાન] & 0xff) << 24)
                | ((long) (ડેટા[સ્થાન + 1] & 0xff) << 16)
                | ((long) (ડેટા[સ્થાન + 2] & 0xff) << 8)
                | (ડેટા[સ્થાન + 3] & 0xffL);
    }

    public static int ક્લાઉડ_ચેકસમ(byte[] ડેટા, int ચલાવો_2, int લંબાઈ_મૂલ્ય) {
        범위확인(ડેટા, ચલાવો_2, લંબાઈ_મૂલ્ય);
        long 합 = 0;
        int 끝 = ચલાવો_2 + લંબાઈ_મૂલ્ય;
        int સ્થાન = ચલાવો_2;
        while (સ્થાન + 1 < 끝) {
            합 += 큰순서짧은정수(ડેટા, સ્થાન);
            સ્થાન += 2;
        }
        if (સ્થાન < 끝) {
            합 += (ડેટા[સ્થાન] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean ઇન્ટરમિટેંટ_ઇથરનેટ_ફ્રેમ(byte[] ડેટા) {
        return ડેટા != null && ડેટા.length >= 14;
    }

    public static int 이더넷상위규약(byte[] ડેટા) {
        if (!ઇન્ટરમિટેંટ_ઇથરનેટ_ફ્રેમ(ડેટા)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ડેટા, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ડેટા, int સ્થાન) {
        if (ડેટા == null || સ્થાન < 0 || ડેટા.length - સ્થાન < 20) {
            return false;
        }
        int વર્ઝન_મૂલ્ય = (ડેટા[સ્થાન] >>> 4) & 0xf;
        int શીર્ષલેખ_લંબાઈ = (ડેટા[સ્થાન] & 0xf) * 4;
        return વર્ઝન_મૂલ્ય == 4 && શીર્ષલેખ_લંબાઈ >= 20 && ડેટા.length - સ્થાન >= શીર્ષલેખ_લંબાઈ;
    }

    private static void 범위확인(byte[] ડેટા, int ચલાવો_2, int લંબાઈ_મૂલ્ય) {
        if (ડેટા == null || ચલાવો_2 < 0 || લંબાઈ_મૂલ્ય < 0 || ચલાવો_2 > ડેટા.length - લંબાઈ_મૂલ્ય) {
            throw new IllegalArgumentException("નેટવર્ક_સ્ટેક ડેટા 범위를 벗어났습니다.");
        }
    }
}

