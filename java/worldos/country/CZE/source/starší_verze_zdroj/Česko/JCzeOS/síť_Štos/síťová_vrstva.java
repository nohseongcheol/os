// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.síť_Štos;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP dostat_HODNOTA 분배를 한곳에서 관리한다. */
public final class síťová_vrstva {
    @FunctionalInterface
    public interface data_obslužná_rutina {
        void Proces_HODNOTA_položka(byte[] data, int Spustit_2, int délka_HODNOTA);
    }

    private final Map<Integer, data_obslužná_rutina> síť_Ethernet_obslužná_rutina = new HashMap<Integer, data_obslužná_rutina>();
    private final Map<Integer, data_obslužná_rutina> IP_obslužná_rutina = new HashMap<Integer, data_obslužná_rutina>();
    private final Map<Integer, data_obslužná_rutina> uživatel_data_lekce_obslužná_rutina = new HashMap<Integer, data_obslužná_rutina>();
    private final Map<Integer, data_obslužná_rutina> 전송제어처리기 = new HashMap<Integer, data_obslužná_rutina>();

    public void registr_síť_Ethernet(int Druh_HODNOTA, data_obslužná_rutina obslužná_rutina) {
        síť_Ethernet_obslužná_rutina.put(Integer.valueOf(Druh_HODNOTA & 0xffff), obslužná_rutina);
    }

    public void registr_IP(int hodnota_smlouvy, data_obslužná_rutina obslužná_rutina) {
        IP_obslužná_rutina.put(Integer.valueOf(hodnota_smlouvy & 0xff), obslužná_rutina);
    }

    public void registr_uživatel_data_lekce(int hardware_port, data_obslužná_rutina obslužná_rutina) {
        uživatel_data_lekce_obslužná_rutina.put(Integer.valueOf(hardware_port & 0xffff), obslužná_rutina);
    }

    public void 전송제어등록(int hardware_port, data_obslužná_rutina obslužná_rutina) {
        전송제어처리기.put(Integer.valueOf(hardware_port & 0xffff), obslužná_rutina);
    }

    public boolean dostat_síť_Ethernet(byte[] rámec_INDEX) {
        if (!síť_Nástroje.informační_systémy_síť_Ethernet_rámec(rámec_INDEX)) {
            return false;
        }
        int Druh_HODNOTA = síť_Nástroje.síť_Ethernet_VELKÁ_protokol(rámec_INDEX);
        data_obslužná_rutina 직접처리기 = síť_Ethernet_obslužná_rutina.get(Integer.valueOf(Druh_HODNOTA));
        if (직접처리기 != null) {
            직접처리기.Proces_HODNOTA_položka(rámec_INDEX, 14, rámec_INDEX.length - 14);
            return true;
        }
        return Druh_HODNOTA == 0x0800 && dostat_cloud_paket(rámec_INDEX, 14);
    }

    private boolean dostat_cloud_paket(byte[] data, int Spustit_2) {
        if (!síť_Nástroje.informační_systémy_OCF_4_protokol(data, Spustit_2)) {
            return false;
        }
        int Nadpis_délka = (data[Spustit_2] & 0x0f) * 4;
        int celkem_délka = síť_Nástroje.큰순서짧은정수(data, Spustit_2 + 2);
        if (celkem_délka < Nadpis_délka || Spustit_2 + celkem_délka > data.length) {
            return false;
        }
        int hodnota_smlouvy = data[Spustit_2 + 9] & 0xff;
        int Obsah_START = Spustit_2 + Nadpis_délka;
        int Obsah_délka = celkem_délka - Nadpis_délka;
        data_obslužná_rutina 직접처리기 = IP_obslužná_rutina.get(Integer.valueOf(hodnota_smlouvy));
        if (직접처리기 != null) {
            직접처리기.Proces_HODNOTA_položka(data, Obsah_START, Obsah_délka);
            return true;
        }
        if (Obsah_délka < 4) {
            return false;
        }
        int cíl_číslo_portu = síť_Nástroje.큰순서짧은정수(data, Obsah_START + 2);
        Map<Integer, data_obslužná_rutina> port_tabulka = hodnota_smlouvy == 17 ? uživatel_data_lekce_obslužná_rutina : hodnota_smlouvy == 6 ? 전송제어처리기 : null;
        if (port_tabulka == null) {
            return false;
        }
        data_obslužná_rutina port_obslužná_rutina = port_tabulka.get(Integer.valueOf(cíl_číslo_portu));
        if (port_obslužná_rutina == null) {
            return false;
        }
        port_obslužná_rutina.Proces_HODNOTA_položka(data, Obsah_START, Obsah_délka);
        return true;
    }
}

