// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frankrijk.JFraOS.net_stack;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP ontvangen_WAARDE 분배를 한곳에서 관리한다. */
public final class netwerklaag {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proces_WAARDE_invoer(byte[] gegevens, int starten, int tijdsduur_WAARDE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void register_Ethernet(int soort_WAARDE, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(soort_WAARDE & 0xffff), 처리기);
    }

    public void register_IP(int contractwaarde, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(contractwaarde & 0xff), 처리기);
    }

    public void register_gebruiker_gegevens_les(int hardware_poort, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(hardware_poort & 0xffff), 처리기);
    }

    public void 전송제어등록(int hardware_poort, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(hardware_poort & 0xffff), 처리기);
    }

    public boolean ontvangen_Ethernet(byte[] frame_INDEX) {
        if (!net_Hulpprogramma_s.informatie_Ethernet_frame(frame_INDEX)) {
            return false;
        }
        int soort_WAARDE = net_Hulpprogramma_s.Ethernet_HOOFDLETTERS_protocol(frame_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(soort_WAARDE));
        if (직접처리기 != null) {
            직접처리기.Proces_WAARDE_invoer(frame_INDEX, 14, frame_INDEX.length - 14);
            return true;
        }
        return soort_WAARDE == 0x0800 && ontvangen_mesh_pakket(frame_INDEX, 14);
    }

    private boolean ontvangen_mesh_pakket(byte[] gegevens, int starten) {
        if (!net_Hulpprogramma_s.informatie_FPA_4_protocol(gegevens, starten)) {
            return false;
        }
        int header_tijdsduur = (gegevens[starten] & 0x0f) * 4;
        int totaal_tijdsduur = net_Hulpprogramma_s.큰순서짧은정수(gegevens, starten + 2);
        if (totaal_tijdsduur < header_tijdsduur || starten + totaal_tijdsduur > gegevens.length) {
            return false;
        }
        int contractwaarde = gegevens[starten + 9] & 0xff;
        int Inhoud_START = starten + header_tijdsduur;
        int Inhoud_tijdsduur = totaal_tijdsduur - header_tijdsduur;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(contractwaarde));
        if (직접처리기 != null) {
            직접처리기.Proces_WAARDE_invoer(gegevens, Inhoud_START, Inhoud_tijdsduur);
            return true;
        }
        if (Inhoud_tijdsduur < 4) {
            return false;
        }
        int doel_poortnummer = net_Hulpprogramma_s.큰순서짧은정수(gegevens, Inhoud_START + 2);
        Map<Integer, 자료처리기> poort_tabel = contractwaarde == 17 ? 사용자자료단위처리기 : contractwaarde == 6 ? 전송제어처리기 : null;
        if (poort_tabel == null) {
            return false;
        }
        자료처리기 포트처리기 = poort_tabel.get(Integer.valueOf(doel_poortnummer));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proces_WAARDE_invoer(gegevens, Inhoud_START, Inhoud_tijdsduur);
        return true;
    }
}

