// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.lìonra_stac;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 baidht_VALUE 순서와 검사합 도구다. */
public final class lìonra_innealan {
    private lìonra_innealan() {
    }

    public static int 큰순서짧은정수(byte[] dàta, int suidhich) {
        범위확인(dàta, suidhich, 2);
        return ((dàta[suidhich] & 0xff) << 8) | (dàta[suidhich + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] dàta, int suidhich) {
        범위확인(dàta, suidhich, 4);
        return ((long) (dàta[suidhich] & 0xff) << 24)
                | ((long) (dàta[suidhich + 1] & 0xff) << 16)
                | ((long) (dàta[suidhich + 2] & 0xff) << 8)
                | (dàta[suidhich + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] dàta, int ruith, int faid_VALUE) {
        범위확인(dàta, ruith, faid_VALUE);
        long SUM_VALUE = 0;
        int 끝 = ruith + faid_VALUE;
        int suidhich = ruith;
        while (suidhich + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(dàta, suidhich);
            suidhich += 2;
        }
        if (suidhich < 끝) {
            SUM_VALUE += (dàta[suidhich] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] dàta) {
        return dàta != null && dàta.length >= 14;
    }

    public static int Ethernet_UPPER_pròtacal(byte[] dàta) {
        if (!이더넷틀인가(dàta)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(dàta, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] dàta, int suidhich) {
        if (dàta == null || suidhich < 0 || dàta.length - suidhich < 20) {
            return false;
        }
        int tionndadh_VALUE = (dàta[suidhich] >>> 4) & 0xf;
        int bann_cinn_faid = (dàta[suidhich] & 0xf) * 4;
        return tionndadh_VALUE == 4 && bann_cinn_faid >= 20 && dàta.length - suidhich >= bann_cinn_faid;
    }

    private static void 범위확인(byte[] dàta, int ruith, int faid_VALUE) {
        if (dàta == null || ruith < 0 || faid_VALUE < 0 || ruith > dàta.length - faid_VALUE) {
            throw new IllegalArgumentException("lìonra_stac dàta 범위를 벗어났습니다.");
        }
    }
}

