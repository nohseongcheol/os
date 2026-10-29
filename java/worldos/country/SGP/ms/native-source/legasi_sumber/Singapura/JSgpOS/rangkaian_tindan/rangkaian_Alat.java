// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Singapura.JSgpOS.rangkaian_tindan;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bait_VALUE 순서와 hasil_tambah_semak 도구다. */
public final class rangkaian_Alat {
    private rangkaian_Alat() {
    }

    public static int 큰순서짧은정수(byte[] data, int Kedudukan) {
        cek_julat(data, Kedudukan, 2);
        return ((data[Kedudukan] & 0xff) << 8) | (data[Kedudukan + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] data, int Kedudukan) {
        cek_julat(data, Kedudukan, 4);
        return ((long) (data[Kedudukan] & 0xff) << 24)
                | ((long) (data[Kedudukan + 1] & 0xff) << 16)
                | ((long) (data[Kedudukan + 2] & 0xff) << 8)
                | (data[Kedudukan + 3] & 0xffL);
    }

    public static int awan_hasil_tambah_semak(byte[] data, int Jalan, int kepanjangan_VALUE) {
        cek_julat(data, Jalan, kepanjangan_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Jalan + kepanjangan_VALUE;
        int Kedudukan = Jalan;
        while (Kedudukan + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(data, Kedudukan);
            Kedudukan += 2;
        }
        if (Kedudukan < 끝) {
            SUM_VALUE += (data[Kedudukan] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean teknologi_maklumat_Ethernet_bingkai(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ethernet_UPPER_protokol(byte[] data) {
        if (!teknologi_maklumat_Ethernet_bingkai(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] data, int Kedudukan) {
        if (data == null || Kedudukan < 0 || data.length - Kedudukan < 20) {
            return false;
        }
        int versi_VALUE = (data[Kedudukan] >>> 4) & 0xf;
        int Pengepala_kepanjangan = (data[Kedudukan] & 0xf) * 4;
        return versi_VALUE == 4 && Pengepala_kepanjangan >= 20 && data.length - Kedudukan >= Pengepala_kepanjangan;
    }

    private static void cek_julat(byte[] data, int Jalan, int kepanjangan_VALUE) {
        if (data == null || Jalan < 0 || kepanjangan_VALUE < 0 || Jalan > data.length - kepanjangan_VALUE) {
            throw new IllegalArgumentException("rangkaian_tindan data 범위를 벗어났습니다.");
        }
    }
}

