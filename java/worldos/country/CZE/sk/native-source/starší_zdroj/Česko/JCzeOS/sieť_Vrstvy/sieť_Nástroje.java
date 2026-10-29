// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.sieť_Vrstvy;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 Byte_VALUE 순서와 kontrolný_súčet 도구다. */
public final class sieť_Nástroje {
    private sieť_Nástroje() {
    }

    public static int 큰순서짧은정수(byte[] údaje, int Pozícia) {
        skontrolovať_rozsah(údaje, Pozícia, 2);
        return ((údaje[Pozícia] & 0xff) << 8) | (údaje[Pozícia + 1] & 0xff);
    }

    public static long vo_formáte_Big_Endian_celé_číslo(byte[] údaje, int Pozícia) {
        skontrolovať_rozsah(údaje, Pozícia, 4);
        return ((long) (údaje[Pozícia] & 0xff) << 24)
                | ((long) (údaje[Pozícia + 1] & 0xff) << 16)
                | ((long) (údaje[Pozícia + 2] & 0xff) << 8)
                | (údaje[Pozícia + 3] & 0xffL);
    }

    public static int cloud_kontrolný_súčet(byte[] údaje, int Spustiť_2, int dĺžka_VALUE) {
        skontrolovať_rozsah(údaje, Spustiť_2, dĺžka_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Spustiť_2 + dĺžka_VALUE;
        int Pozícia = Spustiť_2;
        while (Pozícia + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(údaje, Pozícia);
            Pozícia += 2;
        }
        if (Pozícia < 끝) {
            SUM_VALUE += (údaje[Pozícia] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean Informačné_systémy_sieť_Ethernet_rám(byte[] údaje) {
        return údaje != null && údaje.length >= 14;
    }

    public static int sieť_Ethernet_UPPER_protokol(byte[] údaje) {
        if (!Informačné_systémy_sieť_Ethernet_rám(údaje)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(údaje, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] údaje, int Pozícia) {
        if (údaje == null || Pozícia < 0 || údaje.length - Pozícia < 20) {
            return false;
        }
        int verzia_VALUE = (údaje[Pozícia] >>> 4) & 0xf;
        int Nadpis_dĺžka = (údaje[Pozícia] & 0xf) * 4;
        return verzia_VALUE == 4 && Nadpis_dĺžka >= 20 && údaje.length - Pozícia >= Nadpis_dĺžka;
    }

    private static void skontrolovať_rozsah(byte[] údaje, int Spustiť_2, int dĺžka_VALUE) {
        if (údaje == null || Spustiť_2 < 0 || dĺžka_VALUE < 0 || Spustiť_2 > údaje.length - dĺžka_VALUE) {
            throw new IllegalArgumentException("sieť_Vrstvy údaje 범위를 벗어났습니다.");
        }
    }
}

