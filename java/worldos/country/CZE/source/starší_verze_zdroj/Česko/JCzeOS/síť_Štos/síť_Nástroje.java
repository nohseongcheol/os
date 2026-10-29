// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.síť_Štos;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bajt_HODNOTA 순서와 kontrolní_součet 도구다. */
public final class síť_Nástroje {
    private síť_Nástroje() {
    }

    public static int 큰순서짧은정수(byte[] data, int pozice) {
        šek_oblast(data, pozice, 2);
        return ((data[pozice] & 0xff) << 8) | (data[pozice + 1] & 0xff);
    }

    public static long ve_formátu_Big_Endian_integer(byte[] data, int pozice) {
        šek_oblast(data, pozice, 4);
        return ((long) (data[pozice] & 0xff) << 24)
                | ((long) (data[pozice + 1] & 0xff) << 16)
                | ((long) (data[pozice + 2] & 0xff) << 8)
                | (data[pozice + 3] & 0xffL);
    }

    public static int cloud_kontrolní_součet(byte[] data, int Spustit_2, int délka_HODNOTA) {
        šek_oblast(data, Spustit_2, délka_HODNOTA);
        long SUMA_HODNOTA = 0;
        int 끝 = Spustit_2 + délka_HODNOTA;
        int pozice = Spustit_2;
        while (pozice + 1 < 끝) {
            SUMA_HODNOTA += 큰순서짧은정수(data, pozice);
            pozice += 2;
        }
        if (pozice < 끝) {
            SUMA_HODNOTA += (data[pozice] & 0xff) << 8;
        }
        while ((SUMA_HODNOTA >>> 16) != 0) {
            SUMA_HODNOTA = (SUMA_HODNOTA & 0xffff) + (SUMA_HODNOTA >>> 16);
        }
        return (int) (~SUMA_HODNOTA) & 0xffff;
    }

    public static boolean informační_systémy_síť_Ethernet_rámec(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int síť_Ethernet_VELKÁ_protokol(byte[] data) {
        if (!informační_systémy_síť_Ethernet_rámec(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean informační_systémy_OCF_4_protokol(byte[] data, int pozice) {
        if (data == null || pozice < 0 || data.length - pozice < 20) {
            return false;
        }
        int verze_HODNOTA = (data[pozice] >>> 4) & 0xf;
        int Nadpis_délka = (data[pozice] & 0xf) * 4;
        return verze_HODNOTA == 4 && Nadpis_délka >= 20 && data.length - pozice >= Nadpis_délka;
    }

    private static void šek_oblast(byte[] data, int Spustit_2, int délka_HODNOTA) {
        if (data == null || Spustit_2 < 0 || délka_HODNOTA < 0 || Spustit_2 > data.length - délka_HODNOTA) {
            throw new IllegalArgumentException("síť_Štos data 범위를 벗어났습니다.");
        }
    }
}

