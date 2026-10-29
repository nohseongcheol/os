// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.Netwọọkụ_ikpo;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 baịtị_valuu 순서와 검사합 도구다. */
public final class Netwọọkụ_Ngwaọrụ {
    private Netwọọkụ_Ngwaọrụ() {
    }

    public static int 큰순서짧은정수(byte[] datà, int 위치) {
        범위확인(datà, 위치, 2);
        return ((datà[위치] & 0xff) << 8) | (datà[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] datà, int 위치) {
        범위확인(datà, 위치, 4);
        return ((long) (datà[위치] & 0xff) << 24)
                | ((long) (datà[위치 + 1] & 0xff) << 16)
                | ((long) (datà[위치 + 2] & 0xff) << 8)
                | (datà[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] datà, int Bido, int ogologo_valuu) {
        범위확인(datà, Bido, ogologo_valuu);
        long 합 = 0;
        int 끝 = Bido + ogologo_valuu;
        int 위치 = Bido;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(datà, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (datà[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] datà) {
        return datà != null && datà.length >= 14;
    }

    public static int 이더넷상위규약(byte[] datà) {
        if (!이더넷틀인가(datà)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(datà, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] datà, int 위치) {
        if (datà == null || 위치 < 0 || datà.length - 위치 < 20) {
            return false;
        }
        int ụdị_valuu = (datà[위치] >>> 4) & 0xf;
        int isi_ogologo = (datà[위치] & 0xf) * 4;
        return ụdị_valuu == 4 && isi_ogologo >= 20 && datà.length - 위치 >= isi_ogologo;
    }

    private static void 범위확인(byte[] datà, int Bido, int ogologo_valuu) {
        if (datà == null || Bido < 0 || ogologo_valuu < 0 || Bido > datà.length - ogologo_valuu) {
            throw new IllegalArgumentException("Netwọọkụ_ikpo datà 범위를 벗어났습니다.");
        }
    }
}

