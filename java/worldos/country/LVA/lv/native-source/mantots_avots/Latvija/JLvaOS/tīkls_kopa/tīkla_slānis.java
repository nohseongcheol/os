// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.tīkls_kopa;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP saņemt_VALUE 분배를 한곳에서 관리한다. */
public final class tīkla_slānis {
    @FunctionalInterface
    public interface 자료처리기 {
        void Process_VALUE_ievade(byte[] dati, int Palaist, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void reģistrs_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void reģistrs_IP(int līguma_vērtība, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(līguma_vērtība & 0xff), 처리기);
    }

    public void reģistrs_lietotājs_dati_vienība(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean saņemt_Ethernet(byte[] kadrs_INDEX) {
        if (!tīkls_Rīki.informācijas_tehnoloģija_Ethernet_kadrs(kadrs_INDEX)) {
            return false;
        }
        int 종류 = tīkls_Rīki.Ethernet_UPPER_protokols(kadrs_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Process_VALUE_ievade(kadrs_INDEX, 14, kadrs_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && saņemt_mākonis_pakete(kadrs_INDEX, 14);
    }

    private boolean saņemt_mākonis_pakete(byte[] dati, int Palaist) {
        if (!tīkls_Rīki.informācijas_tehnoloģija_RCN_4_protokols(dati, Palaist)) {
            return false;
        }
        int 머리길이 = (dati[Palaist] & 0x0f) * 4;
        int 전체길이 = tīkls_Rīki.큰순서짧은정수(dati, Palaist + 2);
        if (전체길이 < 머리길이 || Palaist + 전체길이 > dati.length) {
            return false;
        }
        int līguma_vērtība = dati[Palaist + 9] & 0xff;
        int Saturs_Sākt = Palaist + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(līguma_vērtība));
        if (직접처리기 != null) {
            직접처리기.Process_VALUE_ievade(dati, Saturs_Sākt, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int mērķis_porta_numurs = tīkls_Rīki.큰순서짧은정수(dati, Saturs_Sākt + 2);
        Map<Integer, 자료처리기> ports_tabula = līguma_vērtība == 17 ? 사용자자료단위처리기 : līguma_vērtība == 6 ? 전송제어처리기 : null;
        if (ports_tabula == null) {
            return false;
        }
        자료처리기 포트처리기 = ports_tabula.get(Integer.valueOf(mērķis_porta_numurs));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Process_VALUE_ievade(dati, Saturs_Sākt, 내용길이);
        return true;
    }
}

