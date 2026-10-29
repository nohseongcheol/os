// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republica_Moldova.JMdaOS.rețea_Teanc;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VALUE 순서와 sumă_de_verificare 도구다. */
public final class rețea_Instrumente {
    private rețea_Instrumente() {
    }

    public static int 큰순서짧은정수(byte[] date, int Poziție) {
        verifica_zonă(date, Poziție, 2);
        return ((date[Poziție] & 0xff) << 8) | (date[Poziție + 1] & 0xff);
    }

    public static long big_endian_întreg(byte[] date, int Poziție) {
        verifica_zonă(date, Poziție, 4);
        return ((long) (date[Poziție] & 0xff) << 24)
                | ((long) (date[Poziție + 1] & 0xff) << 16)
                | ((long) (date[Poziție + 2] & 0xff) << 8)
                | (date[Poziție + 3] & 0xffL);
    }

    public static int cloud_sumă_de_verificare(byte[] date, int Pornește, int lungime_VALUE) {
        verifica_zonă(date, Pornește, lungime_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Pornește + lungime_VALUE;
        int Poziție = Pornește;
        while (Poziție + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(date, Poziție);
            Poziție += 2;
        }
        if (Poziție < 끝) {
            SUM_VALUE += (date[Poziție] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean sisteme_de_informații_Ethernet_cadru(byte[] date) {
        return date != null && date.length >= 14;
    }

    public static int Ethernet_UPPER_protocol(byte[] date) {
        if (!sisteme_de_informații_Ethernet_cadru(date)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(date, 12);
    }

    public static boolean sisteme_de_informații_IPV_4_protocol(byte[] date, int Poziție) {
        if (date == null || Poziție < 0 || date.length - Poziție < 20) {
            return false;
        }
        int versiune_VALUE = (date[Poziție] >>> 4) & 0xf;
        int Antet_lungime = (date[Poziție] & 0xf) * 4;
        return versiune_VALUE == 4 && Antet_lungime >= 20 && date.length - Poziție >= Antet_lungime;
    }

    private static void verifica_zonă(byte[] date, int Pornește, int lungime_VALUE) {
        if (date == null || Pornește < 0 || lungime_VALUE < 0 || Pornește > date.length - lungime_VALUE) {
            throw new IllegalArgumentException("rețea_Teanc date 범위를 벗어났습니다.");
        }
    }
}

