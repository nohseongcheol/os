// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئێران.JIrnOS.تۆڕ_ستاك;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 بایت_نرخ 순서와 검사합 도구다. */
public final class تۆڕ_ئامرازەکان {
    private تۆڕ_ئامرازەکان() {
    }

    public static int 큰순서짧은정수(byte[] دەیتا, int 위치) {
        범위확인(دەیتا, 위치, 2);
        return ((دەیتا[위치] & 0xff) << 8) | (دەیتا[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] دەیتا, int 위치) {
        범위확인(دەیتا, 위치, 4);
        return ((long) (دەیتا[위치] & 0xff) << 24)
                | ((long) (دەیتا[위치 + 1] & 0xff) << 16)
                | ((long) (دەیتا[위치 + 2] & 0xff) << 8)
                | (دەیتا[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] دەیتا, int ڕادان, int درێژی_نرخ) {
        범위확인(دەیتا, ڕادان, درێژی_نرخ);
        long 합 = 0;
        int 끝 = ڕادان + درێژی_نرخ;
        int 위치 = ڕادان;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(دەیتا, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (دەیتا[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] دەیتا) {
        return دەیتا != null && دەیتا.length >= 14;
    }

    public static int 이더넷상위규약(byte[] دەیتا) {
        if (!이더넷틀인가(دەیتا)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(دەیتا, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] دەیتا, int 위치) {
        if (دەیتا == null || 위치 < 0 || دەیتا.length - 위치 < 20) {
            return false;
        }
        int وەشان_نرخ = (دەیتا[위치] >>> 4) & 0xf;
        int سەرپەڕ_درێژی = (دەیتا[위치] & 0xf) * 4;
        return وەشان_نرخ == 4 && سەرپەڕ_درێژی >= 20 && دەیتا.length - 위치 >= سەرپەڕ_درێژی;
    }

    private static void 범위확인(byte[] دەیتا, int ڕادان, int درێژی_نرخ) {
        if (دەیتا == null || ڕادان < 0 || درێژی_نرخ < 0 || ڕادان > دەیتا.length - درێژی_نرخ) {
            throw new IllegalArgumentException("تۆڕ_ستاك دەیتا 범위를 벗어났습니다.");
        }
    }
}

