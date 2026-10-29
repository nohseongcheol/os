// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.Шабака_ҷамъ;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 байт_қимат 순서와 검사합 도구다. */
public final class Шабака_Абзорҳо {
    private Шабака_Абзорҳо() {
    }

    public static int 큰순서짧은정수(byte[] иттилоот, int 위치) {
        범위확인(иттилоот, 위치, 2);
        return ((иттилоот[위치] & 0xff) << 8) | (иттилоот[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] иттилоот, int 위치) {
        범위확인(иттилоот, 위치, 4);
        return ((long) (иттилоот[위치] & 0xff) << 24)
                | ((long) (иттилоот[위치 + 1] & 0xff) << 16)
                | ((long) (иттилоот[위치 + 2] & 0xff) << 8)
                | (иттилоот[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] иттилоот, int порча, int дарозӣ_қимат) {
        범위확인(иттилоот, порча, дарозӣ_қимат);
        long 합 = 0;
        int 끝 = порча + дарозӣ_қимат;
        int 위치 = порча;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(иттилоот, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (иттилоот[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] иттилоот) {
        return иттилоот != null && иттилоот.length >= 14;
    }

    public static int 이더넷상위규약(byte[] иттилоот) {
        if (!이더넷틀인가(иттилоот)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(иттилоот, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] иттилоот, int 위치) {
        if (иттилоот == null || 위치 < 0 || иттилоот.length - 위치 < 20) {
            return false;
        }
        int версия_қимат = (иттилоот[위치] >>> 4) & 0xf;
        int Сарнавор_дарозӣ = (иттилоот[위치] & 0xf) * 4;
        return версия_қимат == 4 && Сарнавор_дарозӣ >= 20 && иттилоот.length - 위치 >= Сарнавор_дарозӣ;
    }

    private static void 범위확인(byte[] иттилоот, int порча, int дарозӣ_қимат) {
        if (иттилоот == null || порча < 0 || дарозӣ_қимат < 0 || порча > иттилоот.length - дарозӣ_қимат) {
            throw new IllegalArgumentException("Шабака_ҷамъ иттилоот 범위를 벗어났습니다.");
        }
    }
}

