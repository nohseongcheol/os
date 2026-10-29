// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkmaniston.JTkmOS.Tarmoq_Stack;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bayt_VALUE 순서와 검사합 도구다. */
public final class Tarmoq_Vositalar {
    private Tarmoq_Vositalar() {
    }

    public static int 큰순서짧은정수(byte[] ma_lumotlar, int Holati) {
        범위확인(ma_lumotlar, Holati, 2);
        return ((ma_lumotlar[Holati] & 0xff) << 8) | (ma_lumotlar[Holati + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ma_lumotlar, int Holati) {
        범위확인(ma_lumotlar, Holati, 4);
        return ((long) (ma_lumotlar[Holati] & 0xff) << 24)
                | ((long) (ma_lumotlar[Holati + 1] & 0xff) << 16)
                | ((long) (ma_lumotlar[Holati + 2] & 0xff) << 8)
                | (ma_lumotlar[Holati + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] ma_lumotlar, int Bajarish, int uzunlik_VALUE) {
        범위확인(ma_lumotlar, Bajarish, uzunlik_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Bajarish + uzunlik_VALUE;
        int Holati = Bajarish;
        while (Holati + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(ma_lumotlar, Holati);
            Holati += 2;
        }
        if (Holati < 끝) {
            SUM_VALUE += (ma_lumotlar[Holati] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] ma_lumotlar) {
        return ma_lumotlar != null && ma_lumotlar.length >= 14;
    }

    public static int Ethernet_UPPER_bayonnoma(byte[] ma_lumotlar) {
        if (!이더넷틀인가(ma_lumotlar)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ma_lumotlar, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ma_lumotlar, int Holati) {
        if (ma_lumotlar == null || Holati < 0 || ma_lumotlar.length - Holati < 20) {
            return false;
        }
        int versiya_VALUE = (ma_lumotlar[Holati] >>> 4) & 0xf;
        int Sarlavha_uzunlik = (ma_lumotlar[Holati] & 0xf) * 4;
        return versiya_VALUE == 4 && Sarlavha_uzunlik >= 20 && ma_lumotlar.length - Holati >= Sarlavha_uzunlik;
    }

    private static void 범위확인(byte[] ma_lumotlar, int Bajarish, int uzunlik_VALUE) {
        if (ma_lumotlar == null || Bajarish < 0 || uzunlik_VALUE < 0 || Bajarish > ma_lumotlar.length - uzunlik_VALUE) {
            throw new IllegalArgumentException("Tarmoq_Stack ma_lumotlar 범위를 벗어났습니다.");
        }
    }
}

