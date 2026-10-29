// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aforika_Borwa.JZafOS.Neteweke_kokoanyodinepe;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 baete_Boleng 순서와 검사합 도구다. */
public final class Neteweke_Thuluse {
    private Neteweke_Thuluse() {
    }

    public static int 큰순서짧은정수(byte[] tshedimosetso, int 위치) {
        범위확인(tshedimosetso, 위치, 2);
        return ((tshedimosetso[위치] & 0xff) << 8) | (tshedimosetso[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] tshedimosetso, int 위치) {
        범위확인(tshedimosetso, 위치, 4);
        return ((long) (tshedimosetso[위치] & 0xff) << 24)
                | ((long) (tshedimosetso[위치 + 1] & 0xff) << 16)
                | ((long) (tshedimosetso[위치 + 2] & 0xff) << 8)
                | (tshedimosetso[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] tshedimosetso, int dirisa, int boleele_Boleng) {
        범위확인(tshedimosetso, dirisa, boleele_Boleng);
        long 합 = 0;
        int 끝 = dirisa + boleele_Boleng;
        int 위치 = dirisa;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(tshedimosetso, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (tshedimosetso[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] tshedimosetso) {
        return tshedimosetso != null && tshedimosetso.length >= 14;
    }

    public static int 이더넷상위규약(byte[] tshedimosetso) {
        if (!이더넷틀인가(tshedimosetso)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(tshedimosetso, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] tshedimosetso, int 위치) {
        if (tshedimosetso == null || 위치 < 0 || tshedimosetso.length - 위치 < 20) {
            return false;
        }
        int kgaolo_Boleng = (tshedimosetso[위치] >>> 4) & 0xf;
        int setlhogo_boleele = (tshedimosetso[위치] & 0xf) * 4;
        return kgaolo_Boleng == 4 && setlhogo_boleele >= 20 && tshedimosetso.length - 위치 >= setlhogo_boleele;
    }

    private static void 범위확인(byte[] tshedimosetso, int dirisa, int boleele_Boleng) {
        if (tshedimosetso == null || dirisa < 0 || boleele_Boleng < 0 || dirisa > tshedimosetso.length - boleele_Boleng) {
            throw new IllegalArgumentException("Neteweke_kokoanyodinepe tshedimosetso 범위를 벗어났습니다.");
        }
    }
}

