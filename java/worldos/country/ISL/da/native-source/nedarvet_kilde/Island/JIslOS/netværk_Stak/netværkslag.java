// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Island.JIslOS.netværk_Stak;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP modtage_VÆRDI 분배를 한곳에서 관리한다. */
public final class netværkslag {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proces_VÆRDI_post(byte[] data, int Kør_2, int varighed_VÆRDI);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void register_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void register_IP(int kontraktværdi, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(kontraktværdi & 0xff), 처리기);
    }

    public void register_bruger_data_enhed(int hardware_port, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(hardware_port & 0xffff), 처리기);
    }

    public void 전송제어등록(int hardware_port, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(hardware_port & 0xffff), 처리기);
    }

    public boolean modtage_Ethernet(byte[] ramme_INDEKS) {
        if (!netværk_Værktøjer.it_Ethernet_ramme(ramme_INDEKS)) {
            return false;
        }
        int 종류 = netværk_Værktøjer.Ethernet_STORE_BOGSTAVER_protokol(ramme_INDEKS);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proces_VÆRDI_post(ramme_INDEKS, 14, ramme_INDEKS.length - 14);
            return true;
        }
        return 종류 == 0x0800 && modtage_net_pakke(ramme_INDEKS, 14);
    }

    private boolean modtage_net_pakke(byte[] data, int Kør_2) {
        if (!netværk_Værktøjer.it_IPV_4_protokol(data, Kør_2)) {
            return false;
        }
        int Header_varighed = (data[Kør_2] & 0x0f) * 4;
        int i_alt_varighed = netværk_Værktøjer.큰순서짧은정수(data, Kør_2 + 2);
        if (i_alt_varighed < Header_varighed || Kør_2 + i_alt_varighed > data.length) {
            return false;
        }
        int kontraktværdi = data[Kør_2 + 9] & 0xff;
        int Indhold_START = Kør_2 + Header_varighed;
        int Indhold_varighed = i_alt_varighed - Header_varighed;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(kontraktværdi));
        if (직접처리기 != null) {
            직접처리기.Proces_VÆRDI_post(data, Indhold_START, Indhold_varighed);
            return true;
        }
        if (Indhold_varighed < 4) {
            return false;
        }
        int destination_portnummer = netværk_Værktøjer.큰순서짧은정수(data, Indhold_START + 2);
        Map<Integer, 자료처리기> port_tabel = kontraktværdi == 17 ? 사용자자료단위처리기 : kontraktværdi == 6 ? 전송제어처리기 : null;
        if (port_tabel == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tabel.get(Integer.valueOf(destination_portnummer));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proces_VÆRDI_post(data, Indhold_START, Indhold_varighed);
        return true;
    }
}

