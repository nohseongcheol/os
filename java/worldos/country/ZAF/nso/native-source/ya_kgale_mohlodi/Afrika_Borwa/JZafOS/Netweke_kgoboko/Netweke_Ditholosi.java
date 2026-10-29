// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.Netweke_kgoboko;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 paete_boleng 순서와 검사합 도구다. */
public final class Netweke_Ditholosi {
    private Netweke_Ditholosi() {
    }

    public static int 큰순서짧은정수(byte[] data, int 위치) {
        범위확인(data, 위치, 2);
        return ((data[위치] & 0xff) << 8) | (data[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] data, int 위치) {
        범위확인(data, 위치, 4);
        return ((long) (data[위치] & 0xff) << 24)
                | ((long) (data[위치 + 1] & 0xff) << 16)
                | ((long) (data[위치 + 2] & 0xff) << 8)
                | (data[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] data, int Diriša, int botelele_boleng) {
        범위확인(data, Diriša, botelele_boleng);
        long 합 = 0;
        int 끝 = Diriša + botelele_boleng;
        int 위치 = Diriša;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(data, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (data[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int 이더넷상위규약(byte[] data) {
        if (!이더넷틀인가(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] data, int 위치) {
        if (data == null || 위치 < 0 || data.length - 위치 < 20) {
            return false;
        }
        int bešene_boleng = (data[위치] >>> 4) & 0xf;
        int Hlogo_botelele = (data[위치] & 0xf) * 4;
        return bešene_boleng == 4 && Hlogo_botelele >= 20 && data.length - 위치 >= Hlogo_botelele;
    }

    private static void 범위확인(byte[] data, int Diriša, int botelele_boleng) {
        if (data == null || Diriša < 0 || botelele_boleng < 0 || Diriša > data.length - botelele_boleng) {
            throw new IllegalArgumentException("Netweke_kgoboko data 범위를 벗어났습니다.");
        }
    }
}

