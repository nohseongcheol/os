// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Australia.JAusOS.rete_Pila;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP ricevere_VALORE 분배를 한곳에서 관리한다. */
public final class livello_rete {
    @FunctionalInterface
    public interface dati_gestore {
        void Processi_VALORE_voce(byte[] dati, int avvia, int durata_VALORE);
    }

    private final Map<Integer, dati_gestore> Ethernet_gestore = new HashMap<Integer, dati_gestore>();
    private final Map<Integer, dati_gestore> IP_gestore = new HashMap<Integer, dati_gestore>();
    private final Map<Integer, dati_gestore> USER_dati_unità_gestore = new HashMap<Integer, dati_gestore>();
    private final Map<Integer, dati_gestore> trasmissione_controllo_gestore = new HashMap<Integer, dati_gestore>();

    public void registro_Ethernet(int Kind_VALORE, dati_gestore gestore) {
        Ethernet_gestore.put(Integer.valueOf(Kind_VALORE & 0xffff), gestore);
    }

    public void registro_IP(int valore_di_contratto, dati_gestore gestore) {
        IP_gestore.put(Integer.valueOf(valore_di_contratto & 0xff), gestore);
    }

    public void registro_USER_dati_unità(int hardware_porta, dati_gestore gestore) {
        USER_dati_unità_gestore.put(Integer.valueOf(hardware_porta & 0xffff), gestore);
    }

    public void registro_trasmissione_controllo(int hardware_porta, dati_gestore gestore) {
        trasmissione_controllo_gestore.put(Integer.valueOf(hardware_porta & 0xffff), gestore);
    }

    public boolean ricevere_Ethernet(byte[] frame_INDICE) {
        if (!rete_Strumenti.reparto_IT_Ethernet_frame(frame_INDICE)) {
            return false;
        }
        int Kind_VALORE = rete_Strumenti.Ethernet_MAIUSC_protocollo(frame_INDICE);
        dati_gestore 직접처리기 = Ethernet_gestore.get(Integer.valueOf(Kind_VALORE));
        if (직접처리기 != null) {
            직접처리기.Processi_VALORE_voce(frame_INDICE, 14, frame_INDICE.length - 14);
            return true;
        }
        return Kind_VALORE == 0x0800 && ricevere_cloud_pacchetto(frame_INDICE, 14);
    }

    private boolean ricevere_cloud_pacchetto(byte[] dati, int avvia) {
        if (!rete_Strumenti.reparto_IT_IPV_4_protocollo(dati, avvia)) {
            return false;
        }
        int Intestazione_durata = (dati[avvia] & 0x0f) * 4;
        int totale_durata = rete_Strumenti.큰순서짧은정수(dati, avvia + 2);
        if (totale_durata < Intestazione_durata || avvia + totale_durata > dati.length) {
            return false;
        }
        int valore_di_contratto = dati[avvia + 9] & 0xff;
        int Contenuto_START = avvia + Intestazione_durata;
        int Contenuto_durata = totale_durata - Intestazione_durata;
        dati_gestore 직접처리기 = IP_gestore.get(Integer.valueOf(valore_di_contratto));
        if (직접처리기 != null) {
            직접처리기.Processi_VALORE_voce(dati, Contenuto_START, Contenuto_durata);
            return true;
        }
        if (Contenuto_durata < 4) {
            return false;
        }
        int meta_numero_di_porta = rete_Strumenti.큰순서짧은정수(dati, Contenuto_START + 2);
        Map<Integer, dati_gestore> porta_tabella = valore_di_contratto == 17 ? USER_dati_unità_gestore : valore_di_contratto == 6 ? trasmissione_controllo_gestore : null;
        if (porta_tabella == null) {
            return false;
        }
        dati_gestore porta_gestore = porta_tabella.get(Integer.valueOf(meta_numero_di_porta));
        if (porta_gestore == null) {
            return false;
        }
        porta_gestore.Processi_VALORE_voce(dati, Contenuto_START, Contenuto_durata);
        return true;
    }
}

