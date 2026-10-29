// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ermənistan.JArmOS.Şəbəkə_Yığın;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bayt_VALUE 순서와 검사합 도구다. */
public final class Şəbəkə_Alətlər {
    private Şəbəkə_Alətlər() {
    }

    public static int 큰순서짧은정수(byte[] verilənlər, int yerinə_qoymaq) {
        범위확인(verilənlər, yerinə_qoymaq, 2);
        return ((verilənlər[yerinə_qoymaq] & 0xff) << 8) | (verilənlər[yerinə_qoymaq + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] verilənlər, int yerinə_qoymaq) {
        범위확인(verilənlər, yerinə_qoymaq, 4);
        return ((long) (verilənlər[yerinə_qoymaq] & 0xff) << 24)
                | ((long) (verilənlər[yerinə_qoymaq + 1] & 0xff) << 16)
                | ((long) (verilənlər[yerinə_qoymaq + 2] & 0xff) << 8)
                | (verilənlər[yerinə_qoymaq + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] verilənlər, int İcra_Et, int uzunluq_VALUE) {
        범위확인(verilənlər, İcra_Et, uzunluq_VALUE);
        long SUM_VALUE = 0;
        int 끝 = İcra_Et + uzunluq_VALUE;
        int yerinə_qoymaq = İcra_Et;
        while (yerinə_qoymaq + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(verilənlər, yerinə_qoymaq);
            yerinə_qoymaq += 2;
        }
        if (yerinə_qoymaq < 끝) {
            SUM_VALUE += (verilənlər[yerinə_qoymaq] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] verilənlər) {
        return verilənlər != null && verilənlər.length >= 14;
    }

    public static int Ethernet_UPPER_protokol(byte[] verilənlər) {
        if (!이더넷틀인가(verilənlər)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(verilənlər, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] verilənlər, int yerinə_qoymaq) {
        if (verilənlər == null || yerinə_qoymaq < 0 || verilənlər.length - yerinə_qoymaq < 20) {
            return false;
        }
        int versiya_VALUE = (verilənlər[yerinə_qoymaq] >>> 4) & 0xf;
        int Başlıq_uzunluq = (verilənlər[yerinə_qoymaq] & 0xf) * 4;
        return versiya_VALUE == 4 && Başlıq_uzunluq >= 20 && verilənlər.length - yerinə_qoymaq >= Başlıq_uzunluq;
    }

    private static void 범위확인(byte[] verilənlər, int İcra_Et, int uzunluq_VALUE) {
        if (verilənlər == null || İcra_Et < 0 || uzunluq_VALUE < 0 || İcra_Et > verilənlər.length - uzunluq_VALUE) {
            throw new IllegalArgumentException("Şəbəkə_Yığın verilənlər 범위를 벗어났습니다.");
        }
    }
}

