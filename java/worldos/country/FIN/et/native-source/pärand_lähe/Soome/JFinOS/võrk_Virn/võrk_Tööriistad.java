// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.võrk_Virn;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bait_VALUE 순서와 kontrollsumma 도구다. */
public final class võrk_Tööriistad {
    private võrk_Tööriistad() {
    }

    public static int 큰순서짧은정수(byte[] andmed, int Asukoht) {
        tšekk_vahemik(andmed, Asukoht, 2);
        return ((andmed[Asukoht] & 0xff) << 8) | (andmed[Asukoht + 1] & 0xff);
    }

    public static long tavabaidijärjestusega_täisarv(byte[] andmed, int Asukoht) {
        tšekk_vahemik(andmed, Asukoht, 4);
        return ((long) (andmed[Asukoht] & 0xff) << 24)
                | ((long) (andmed[Asukoht + 1] & 0xff) << 16)
                | ((long) (andmed[Asukoht + 2] & 0xff) << 8)
                | (andmed[Asukoht + 3] & 0xffL);
    }

    public static int pilv_kontrollsumma(byte[] andmed, int Käivita_2, int 길이) {
        tšekk_vahemik(andmed, Käivita_2, 길이);
        long SUM_VALUE = 0;
        int 끝 = Käivita_2 + 길이;
        int Asukoht = Käivita_2;
        while (Asukoht + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(andmed, Asukoht);
            Asukoht += 2;
        }
        if (Asukoht < 끝) {
            SUM_VALUE += (andmed[Asukoht] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean infotehnoloogia_Ethernet_raam(byte[] andmed) {
        return andmed != null && andmed.length >= 14;
    }

    public static int Ethernet_UPPER_protokoll(byte[] andmed) {
        if (!infotehnoloogia_Ethernet_raam(andmed)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(andmed, 12);
    }

    public static boolean infotehnoloogia_AHH_4_protokoll(byte[] andmed, int Asukoht) {
        if (andmed == null || Asukoht < 0 || andmed.length - Asukoht < 20) {
            return false;
        }
        int versioon_VALUE = (andmed[Asukoht] >>> 4) & 0xf;
        int 머리길이 = (andmed[Asukoht] & 0xf) * 4;
        return versioon_VALUE == 4 && 머리길이 >= 20 && andmed.length - Asukoht >= 머리길이;
    }

    private static void tšekk_vahemik(byte[] andmed, int Käivita_2, int 길이) {
        if (andmed == null || Käivita_2 < 0 || 길이 < 0 || Käivita_2 > andmed.length - 길이) {
            throw new IllegalArgumentException("võrk_Virn andmed 범위를 벗어났습니다.");
        }
    }
}

