// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.jaringan_tumpuk;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VALUE 순서와 checksum 도구다. */
public final class jaringan_Alat {
    private jaringan_Alat() {
    }

    public static int 큰순서짧은정수(byte[] data, int posisi) {
        cek_rentang(data, posisi, 2);
        return ((data[posisi] & 0xff) << 8) | (data[posisi + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] data, int posisi) {
        cek_rentang(data, posisi, 4);
        return ((long) (data[posisi] & 0xff) << 24)
                | ((long) (data[posisi + 1] & 0xff) << 16)
                | ((long) (data[posisi + 2] & 0xff) << 8)
                | (data[posisi + 3] & 0xffL);
    }

    public static int cloud_checksum(byte[] data, int jalankan, int panjang_VALUE) {
        cek_rentang(data, jalankan, panjang_VALUE);
        long SUM_VALUE = 0;
        int 끝 = jalankan + panjang_VALUE;
        int posisi = jalankan;
        while (posisi + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(data, posisi);
            posisi += 2;
        }
        if (posisi < 끝) {
            SUM_VALUE += (data[posisi] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean teknologi_informasi_Ethernet_bingkai(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ethernet_UPPER_protokol(byte[] data) {
        if (!teknologi_informasi_Ethernet_bingkai(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean teknologi_informasi_IPV_4_protokol(byte[] data, int posisi) {
        if (data == null || posisi < 0 || data.length - posisi < 20) {
            return false;
        }
        int versi_VALUE = (data[posisi] >>> 4) & 0xf;
        int judul_panjang = (data[posisi] & 0xf) * 4;
        return versi_VALUE == 4 && judul_panjang >= 20 && data.length - posisi >= judul_panjang;
    }

    private static void cek_rentang(byte[] data, int jalankan, int panjang_VALUE) {
        if (data == null || jalankan < 0 || panjang_VALUE < 0 || jalankan > data.length - panjang_VALUE) {
            throw new IllegalArgumentException("jaringan_tumpuk data 범위를 벗어났습니다.");
        }
    }
}

