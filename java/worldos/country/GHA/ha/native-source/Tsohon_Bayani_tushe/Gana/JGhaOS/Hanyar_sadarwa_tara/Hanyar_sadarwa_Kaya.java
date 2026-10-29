// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gana.JGhaOS.Hanyar_sadarwa_tara;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bayit_Daraja 순서와 checksum 도구다. */
public final class Hanyar_sadarwa_Kaya {
    private Hanyar_sadarwa_Kaya() {
    }

    public static int 큰순서짧은정수(byte[] Tarin_bayani, int 위치) {
        범위확인(Tarin_bayani, 위치, 2);
        return ((Tarin_bayani[위치] & 0xff) << 8) | (Tarin_bayani[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] Tarin_bayani, int 위치) {
        범위확인(Tarin_bayani, 위치, 4);
        return ((long) (Tarin_bayani[위치] & 0xff) << 24)
                | ((long) (Tarin_bayani[위치 + 1] & 0xff) << 16)
                | ((long) (Tarin_bayani[위치 + 2] & 0xff) << 8)
                | (Tarin_bayani[위치 + 3] & 0xffL);
    }

    public static int Intanet_checksum(byte[] Tarin_bayani, int Tafiyar_da, int Tsawo_Daraja) {
        범위확인(Tarin_bayani, Tafiyar_da, Tsawo_Daraja);
        long 합 = 0;
        int 끝 = Tafiyar_da + Tsawo_Daraja;
        int 위치 = Tafiyar_da;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(Tarin_bayani, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (Tarin_bayani[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean kimiyar_bayanai_Wayar_kwamfuta_ta_yanar_gizo_allo(byte[] Tarin_bayani) {
        return Tarin_bayani != null && Tarin_bayani.length >= 14;
    }

    public static int 이더넷상위규약(byte[] Tarin_bayani) {
        if (!kimiyar_bayanai_Wayar_kwamfuta_ta_yanar_gizo_allo(Tarin_bayani)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(Tarin_bayani, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] Tarin_bayani, int 위치) {
        if (Tarin_bayani == null || 위치 < 0 || Tarin_bayani.length - 위치 < 20) {
            return false;
        }
        int siga_Daraja = (Tarin_bayani[위치] >>> 4) & 0xf;
        int Kai_Tsawo = (Tarin_bayani[위치] & 0xf) * 4;
        return siga_Daraja == 4 && Kai_Tsawo >= 20 && Tarin_bayani.length - 위치 >= Kai_Tsawo;
    }

    private static void 범위확인(byte[] Tarin_bayani, int Tafiyar_da, int Tsawo_Daraja) {
        if (Tarin_bayani == null || Tafiyar_da < 0 || Tsawo_Daraja < 0 || Tafiyar_da > Tarin_bayani.length - Tsawo_Daraja) {
            throw new IllegalArgumentException("Hanyar_sadarwa_tara Tarin_bayani 범위를 벗어났습니다.");
        }
    }
}

