// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package iNingizimu_Afrika.JZafOS.iNethiwekhi_Isitaki;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 ibhayithi_inani 순서와 검사합 도구다. */
public final class iNethiwekhi_Amathuluzi {
    private iNethiwekhi_Amathuluzi() {
    }

    public static int 큰순서짧은정수(byte[] imininingwane, int 위치) {
        범위확인(imininingwane, 위치, 2);
        return ((imininingwane[위치] & 0xff) << 8) | (imininingwane[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] imininingwane, int 위치) {
        범위확인(imininingwane, 위치, 4);
        return ((long) (imininingwane[위치] & 0xff) << 24)
                | ((long) (imininingwane[위치 + 1] & 0xff) << 16)
                | ((long) (imininingwane[위치 + 2] & 0xff) << 8)
                | (imininingwane[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] imininingwane, int Sebenzisa, int ubude_inani) {
        범위확인(imininingwane, Sebenzisa, ubude_inani);
        long 합 = 0;
        int 끝 = Sebenzisa + ubude_inani;
        int 위치 = Sebenzisa;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(imininingwane, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (imininingwane[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] imininingwane) {
        return imininingwane != null && imininingwane.length >= 14;
    }

    public static int 이더넷상위규약(byte[] imininingwane) {
        if (!이더넷틀인가(imininingwane)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(imininingwane, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] imininingwane, int 위치) {
        if (imininingwane == null || 위치 < 0 || imininingwane.length - 위치 < 20) {
            return false;
        }
        int isibuyekezo_inani = (imininingwane[위치] >>> 4) & 0xf;
        int Unhlokweni_ubude = (imininingwane[위치] & 0xf) * 4;
        return isibuyekezo_inani == 4 && Unhlokweni_ubude >= 20 && imininingwane.length - 위치 >= Unhlokweni_ubude;
    }

    private static void 범위확인(byte[] imininingwane, int Sebenzisa, int ubude_inani) {
        if (imininingwane == null || Sebenzisa < 0 || ubude_inani < 0 || Sebenzisa > imininingwane.length - ubude_inani) {
            throw new IllegalArgumentException("iNethiwekhi_Isitaki imininingwane 범위를 벗어났습니다.");
        }
    }
}

