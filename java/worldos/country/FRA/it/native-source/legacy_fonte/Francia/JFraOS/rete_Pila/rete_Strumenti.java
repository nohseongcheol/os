// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Francia.JFraOS.rete_Pila;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VALORE 순서와 checksum 도구다. */
public final class rete_Strumenti {
    private rete_Strumenti() {
    }

    public static int 큰순서짧은정수(byte[] dati, int posizione) {
        assegno_intervallo(dati, posizione, 2);
        return ((dati[posizione] & 0xff) << 8) | (dati[posizione + 1] & 0xff);
    }

    public static long big_endian_intero(byte[] dati, int posizione) {
        assegno_intervallo(dati, posizione, 4);
        return ((long) (dati[posizione] & 0xff) << 24)
                | ((long) (dati[posizione + 1] & 0xff) << 16)
                | ((long) (dati[posizione + 2] & 0xff) << 8)
                | (dati[posizione + 3] & 0xffL);
    }

    public static int cloud_checksum(byte[] dati, int avvia, int durata_VALORE) {
        assegno_intervallo(dati, avvia, durata_VALORE);
        long SUM_VALORE = 0;
        int 끝 = avvia + durata_VALORE;
        int posizione = avvia;
        while (posizione + 1 < 끝) {
            SUM_VALORE += 큰순서짧은정수(dati, posizione);
            posizione += 2;
        }
        if (posizione < 끝) {
            SUM_VALORE += (dati[posizione] & 0xff) << 8;
        }
        while ((SUM_VALORE >>> 16) != 0) {
            SUM_VALORE = (SUM_VALORE & 0xffff) + (SUM_VALORE >>> 16);
        }
        return (int) (~SUM_VALORE) & 0xffff;
    }

    public static boolean reparto_IT_Ethernet_frame(byte[] dati) {
        return dati != null && dati.length >= 14;
    }

    public static int Ethernet_MAIUSC_protocollo(byte[] dati) {
        if (!reparto_IT_Ethernet_frame(dati)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(dati, 12);
    }

    public static boolean reparto_IT_IPV_4_protocollo(byte[] dati, int posizione) {
        if (dati == null || posizione < 0 || dati.length - posizione < 20) {
            return false;
        }
        int versione_VALORE = (dati[posizione] >>> 4) & 0xf;
        int Intestazione_durata = (dati[posizione] & 0xf) * 4;
        return versione_VALORE == 4 && Intestazione_durata >= 20 && dati.length - posizione >= Intestazione_durata;
    }

    private static void assegno_intervallo(byte[] dati, int avvia, int durata_VALORE) {
        if (dati == null || avvia < 0 || durata_VALORE < 0 || avvia > dati.length - durata_VALORE) {
            throw new IllegalArgumentException("rete_Pila dati 범위를 벗어났습니다.");
        }
    }
}

