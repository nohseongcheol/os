// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sint_Maarten.JSxmOS.net_stack;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_WAARDE 순서와 controlesom 도구다. */
public final class net_Hulpprogramma_s {
    private net_Hulpprogramma_s() {
    }

    public static int 큰순서짧은정수(byte[] gegevens, int positie) {
        cheque_bereik(gegevens, positie, 2);
        return ((gegevens[positie] & 0xff) << 8) | (gegevens[positie + 1] & 0xff);
    }

    public static long big_endian_geheel_getal(byte[] gegevens, int positie) {
        cheque_bereik(gegevens, positie, 4);
        return ((long) (gegevens[positie] & 0xff) << 24)
                | ((long) (gegevens[positie + 1] & 0xff) << 16)
                | ((long) (gegevens[positie + 2] & 0xff) << 8)
                | (gegevens[positie + 3] & 0xffL);
    }

    public static int mesh_controlesom(byte[] gegevens, int starten, int tijdsduur_WAARDE) {
        cheque_bereik(gegevens, starten, tijdsduur_WAARDE);
        long SOM_WAARDE = 0;
        int 끝 = starten + tijdsduur_WAARDE;
        int positie = starten;
        while (positie + 1 < 끝) {
            SOM_WAARDE += 큰순서짧은정수(gegevens, positie);
            positie += 2;
        }
        if (positie < 끝) {
            SOM_WAARDE += (gegevens[positie] & 0xff) << 8;
        }
        while ((SOM_WAARDE >>> 16) != 0) {
            SOM_WAARDE = (SOM_WAARDE & 0xffff) + (SOM_WAARDE >>> 16);
        }
        return (int) (~SOM_WAARDE) & 0xffff;
    }

    public static boolean informatie_Ethernet_frame(byte[] gegevens) {
        return gegevens != null && gegevens.length >= 14;
    }

    public static int Ethernet_HOOFDLETTERS_protocol(byte[] gegevens) {
        if (!informatie_Ethernet_frame(gegevens)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(gegevens, 12);
    }

    public static boolean informatie_FPA_4_protocol(byte[] gegevens, int positie) {
        if (gegevens == null || positie < 0 || gegevens.length - positie < 20) {
            return false;
        }
        int versie_WAARDE = (gegevens[positie] >>> 4) & 0xf;
        int header_tijdsduur = (gegevens[positie] & 0xf) * 4;
        return versie_WAARDE == 4 && header_tijdsduur >= 20 && gegevens.length - positie >= header_tijdsduur;
    }

    private static void cheque_bereik(byte[] gegevens, int starten, int tijdsduur_WAARDE) {
        if (gegevens == null || starten < 0 || tijdsduur_WAARDE < 0 || starten > gegevens.length - tijdsduur_WAARDE) {
            throw new IllegalArgumentException("net_stack gegevens 범위를 벗어났습니다.");
        }
    }
}

