// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Románia.JRouOS.hálózat_Sor;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bájt_ÉRTÉK 순서와 ellenőrzőösszeg 도구다. */
public final class hálózat_Eszközök {
    private hálózat_Eszközök() {
    }

    public static int 큰순서짧은정수(byte[] adat, int Pozíció) {
        csekk_tartomány(adat, Pozíció, 2);
        return ((adat[Pozíció] & 0xff) << 8) | (adat[Pozíció + 1] & 0xff);
    }

    public static long csökkenő_helyiértékű_egész_szám(byte[] adat, int Pozíció) {
        csekk_tartomány(adat, Pozíció, 4);
        return ((long) (adat[Pozíció] & 0xff) << 24)
                | ((long) (adat[Pozíció + 1] & 0xff) << 16)
                | ((long) (adat[Pozíció + 2] & 0xff) << 8)
                | (adat[Pozíció + 3] & 0xffL);
    }

    public static int háló_ellenőrzőösszeg(byte[] adat, int Futtatás, int hossz_ÉRTÉK) {
        csekk_tartomány(adat, Futtatás, hossz_ÉRTÉK);
        long SUM_ÉRTÉK = 0;
        int 끝 = Futtatás + hossz_ÉRTÉK;
        int Pozíció = Futtatás;
        while (Pozíció + 1 < 끝) {
            SUM_ÉRTÉK += 큰순서짧은정수(adat, Pozíció);
            Pozíció += 2;
        }
        if (Pozíció < 끝) {
            SUM_ÉRTÉK += (adat[Pozíció] & 0xff) << 8;
        }
        while ((SUM_ÉRTÉK >>> 16) != 0) {
            SUM_ÉRTÉK = (SUM_ÉRTÉK & 0xffff) + (SUM_ÉRTÉK >>> 16);
        }
        return (int) (~SUM_ÉRTÉK) & 0xffff;
    }

    public static boolean informatikai_részleg_Ethernet_doboz(byte[] adat) {
        return adat != null && adat.length >= 14;
    }

    public static int Ethernet_NAGYBETŰS_protokoll(byte[] adat) {
        if (!informatikai_részleg_Ethernet_doboz(adat)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(adat, 12);
    }

    public static boolean informatikai_részleg_számlázási_árkülönbözet_4_protokoll(byte[] adat, int Pozíció) {
        if (adat == null || Pozíció < 0 || adat.length - Pozíció < 20) {
            return false;
        }
        int verzió_ÉRTÉK = (adat[Pozíció] >>> 4) & 0xf;
        int fejléc_hossz = (adat[Pozíció] & 0xf) * 4;
        return verzió_ÉRTÉK == 4 && fejléc_hossz >= 20 && adat.length - Pozíció >= fejléc_hossz;
    }

    private static void csekk_tartomány(byte[] adat, int Futtatás, int hossz_ÉRTÉK) {
        if (adat == null || Futtatás < 0 || hossz_ÉRTÉK < 0 || Futtatás > adat.length - hossz_ÉRTÉK) {
            throw new IllegalArgumentException("hálózat_Sor adat 범위를 벗어났습니다.");
        }
    }
}

