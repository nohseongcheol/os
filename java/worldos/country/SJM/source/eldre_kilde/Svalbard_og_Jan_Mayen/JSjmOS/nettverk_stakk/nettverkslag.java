// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.nettverk_stakk;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP motta_VERDI 분배를 한곳에서 관리한다. */
public final class nettverkslag {
    @FunctionalInterface
    public interface data_behandlingsprogram {
        void Prosess_VERDI_oppføring(byte[] data, int Kjør_2, int lengde_VERDI);
    }

    private final Map<Integer, data_behandlingsprogram> Ethernet_behandlingsprogram = new HashMap<Integer, data_behandlingsprogram>();
    private final Map<Integer, data_behandlingsprogram> IP_behandlingsprogram = new HashMap<Integer, data_behandlingsprogram>();
    private final Map<Integer, data_behandlingsprogram> bruker_data_enhet_behandlingsprogram = new HashMap<Integer, data_behandlingsprogram>();
    private final Map<Integer, data_behandlingsprogram> 전송제어처리기 = new HashMap<Integer, data_behandlingsprogram>();

    public void register_Ethernet(int 종류, data_behandlingsprogram behandlingsprogram) {
        Ethernet_behandlingsprogram.put(Integer.valueOf(종류 & 0xffff), behandlingsprogram);
    }

    public void register_IP(int kontraktverdi, data_behandlingsprogram behandlingsprogram) {
        IP_behandlingsprogram.put(Integer.valueOf(kontraktverdi & 0xff), behandlingsprogram);
    }

    public void register_bruker_data_enhet(int maskinvare_port, data_behandlingsprogram behandlingsprogram) {
        bruker_data_enhet_behandlingsprogram.put(Integer.valueOf(maskinvare_port & 0xffff), behandlingsprogram);
    }

    public void 전송제어등록(int maskinvare_port, data_behandlingsprogram behandlingsprogram) {
        전송제어처리기.put(Integer.valueOf(maskinvare_port & 0xffff), behandlingsprogram);
    }

    public boolean motta_Ethernet(byte[] bilde_INDEKS) {
        if (!nettverk_Verktøy.informasjonssystemer_Ethernet_bilde(bilde_INDEKS)) {
            return false;
        }
        int 종류 = nettverk_Verktøy.Ethernet_STORE_protokoll(bilde_INDEKS);
        data_behandlingsprogram 직접처리기 = Ethernet_behandlingsprogram.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Prosess_VERDI_oppføring(bilde_INDEKS, 14, bilde_INDEKS.length - 14);
            return true;
        }
        return 종류 == 0x0800 && motta_sky_pakke(bilde_INDEKS, 14);
    }

    private boolean motta_sky_pakke(byte[] data, int Kjør_2) {
        if (!nettverk_Verktøy.informasjonssystemer_FPA_4_protokoll(data, Kjør_2)) {
            return false;
        }
        int Topptekst_lengde = (data[Kjør_2] & 0x0f) * 4;
        int total_lengde = nettverk_Verktøy.큰순서짧은정수(data, Kjør_2 + 2);
        if (total_lengde < Topptekst_lengde || Kjør_2 + total_lengde > data.length) {
            return false;
        }
        int kontraktverdi = data[Kjør_2 + 9] & 0xff;
        int Innhold_START = Kjør_2 + Topptekst_lengde;
        int Innhold_lengde = total_lengde - Topptekst_lengde;
        data_behandlingsprogram 직접처리기 = IP_behandlingsprogram.get(Integer.valueOf(kontraktverdi));
        if (직접처리기 != null) {
            직접처리기.Prosess_VERDI_oppføring(data, Innhold_START, Innhold_lengde);
            return true;
        }
        if (Innhold_lengde < 4) {
            return false;
        }
        int mål_portnummer = nettverk_Verktøy.큰순서짧은정수(data, Innhold_START + 2);
        Map<Integer, data_behandlingsprogram> port_tabell = kontraktverdi == 17 ? bruker_data_enhet_behandlingsprogram : kontraktverdi == 6 ? 전송제어처리기 : null;
        if (port_tabell == null) {
            return false;
        }
        data_behandlingsprogram port_behandlingsprogram = port_tabell.get(Integer.valueOf(mål_portnummer));
        if (port_behandlingsprogram == null) {
            return false;
        }
        port_behandlingsprogram.Prosess_VERDI_oppføring(data, Innhold_START, Innhold_lengde);
        return true;
    }
}

