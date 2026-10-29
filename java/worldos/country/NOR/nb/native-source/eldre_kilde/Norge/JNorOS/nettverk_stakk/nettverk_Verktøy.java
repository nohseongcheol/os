// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.nettverk_stakk;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VERDI 순서와 kontrollsum 도구다. */
public final class nettverk_Verktøy {
    private nettverk_Verktøy() {
    }

    public static int 큰순서짧은정수(byte[] data, int Posisjon) {
        sjekk_område(data, Posisjon, 2);
        return ((data[Posisjon] & 0xff) << 8) | (data[Posisjon + 1] & 0xff);
    }

    public static long big_endian_heltall(byte[] data, int Posisjon) {
        sjekk_område(data, Posisjon, 4);
        return ((long) (data[Posisjon] & 0xff) << 24)
                | ((long) (data[Posisjon + 1] & 0xff) << 16)
                | ((long) (data[Posisjon + 2] & 0xff) << 8)
                | (data[Posisjon + 3] & 0xffL);
    }

    public static int sky_kontrollsum(byte[] data, int Kjør_2, int lengde_VERDI) {
        sjekk_område(data, Kjør_2, lengde_VERDI);
        long SUMMER_VERDI = 0;
        int 끝 = Kjør_2 + lengde_VERDI;
        int Posisjon = Kjør_2;
        while (Posisjon + 1 < 끝) {
            SUMMER_VERDI += 큰순서짧은정수(data, Posisjon);
            Posisjon += 2;
        }
        if (Posisjon < 끝) {
            SUMMER_VERDI += (data[Posisjon] & 0xff) << 8;
        }
        while ((SUMMER_VERDI >>> 16) != 0) {
            SUMMER_VERDI = (SUMMER_VERDI & 0xffff) + (SUMMER_VERDI >>> 16);
        }
        return (int) (~SUMMER_VERDI) & 0xffff;
    }

    public static boolean informasjonssystemer_Ethernet_bilde(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ethernet_STORE_protokoll(byte[] data) {
        if (!informasjonssystemer_Ethernet_bilde(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean informasjonssystemer_FPA_4_protokoll(byte[] data, int Posisjon) {
        if (data == null || Posisjon < 0 || data.length - Posisjon < 20) {
            return false;
        }
        int versjon_VERDI = (data[Posisjon] >>> 4) & 0xf;
        int Topptekst_lengde = (data[Posisjon] & 0xf) * 4;
        return versjon_VERDI == 4 && Topptekst_lengde >= 20 && data.length - Posisjon >= Topptekst_lengde;
    }

    private static void sjekk_område(byte[] data, int Kjør_2, int lengde_VERDI) {
        if (data == null || Kjør_2 < 0 || lengde_VERDI < 0 || Kjør_2 > data.length - lengde_VERDI) {
            throw new IllegalArgumentException("nettverk_stakk data 범위를 벗어났습니다.");
        }
    }
}

