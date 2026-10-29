// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Румъния.JRouOS.мрежа_стек;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 байт_стойност 순서와 контролна_сума 도구다. */
public final class мрежа_Инструменти {
    private мрежа_Инструменти() {
    }

    public static int 큰순서짧은정수(byte[] данни, int Позиция) {
        проверявам_обхват(данни, Позиция, 2);
        return ((данни[Позиция] & 0xff) << 8) | (данни[Позиция + 1] & 0xff);
    }

    public static long първо_старшия_бит_с_водещ_старши_бит_цяло_число(byte[] данни, int Позиция) {
        проверявам_обхват(данни, Позиция, 4);
        return ((long) (данни[Позиция] & 0xff) << 24)
                | ((long) (данни[Позиция + 1] & 0xff) << 16)
                | ((long) (данни[Позиция + 2] & 0xff) << 8)
                | (данни[Позиция + 3] & 0xffL);
    }

    public static int облак_контролна_сума(byte[] данни, int Стартиране, int 길이) {
        проверявам_обхват(данни, Стартиране, 길이);
        long 합 = 0;
        int 끝 = Стартиране + 길이;
        int Позиция = Стартиране;
        while (Позиция + 1 < 끝) {
            합 += 큰순서짧은정수(данни, Позиция);
            Позиция += 2;
        }
        if (Позиция < 끝) {
            합 += (данни[Позиция] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] данни) {
        return данни != null && данни.length >= 14;
    }

    public static int 이더넷상위규약(byte[] данни) {
        if (!이더넷틀인가(данни)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(данни, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] данни, int Позиция) {
        if (данни == null || Позиция < 0 || данни.length - Позиция < 20) {
            return false;
        }
        int версия_стойност = (данни[Позиция] >>> 4) & 0xf;
        int 머리길이 = (данни[Позиция] & 0xf) * 4;
        return версия_стойност == 4 && 머리길이 >= 20 && данни.length - Позиция >= 머리길이;
    }

    private static void проверявам_обхват(byte[] данни, int Стартиране, int 길이) {
        if (данни == null || Стартиране < 0 || 길이 < 0 || Стартиране > данни.length - 길이) {
            throw new IllegalArgumentException("мрежа_стек данни 범위를 벗어났습니다.");
        }
    }
}

