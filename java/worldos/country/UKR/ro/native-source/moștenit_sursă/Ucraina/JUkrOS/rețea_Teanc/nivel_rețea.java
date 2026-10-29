// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ucraina.JUkrOS.rețea_Teanc;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP primi_VALUE 분배를 한곳에서 관리한다. */
public final class nivel_rețea {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proces_VALUE_intrare(byte[] date, int Pornește, int lungime_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void registru_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void registru_IP(int caz_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(caz_VALUE & 0xff), 처리기);
    }

    public void registru_utilizator_date_lecție(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean primi_Ethernet(byte[] cadru_INDEX) {
        if (!rețea_Instrumente.sisteme_de_informații_Ethernet_cadru(cadru_INDEX)) {
            return false;
        }
        int 종류 = rețea_Instrumente.Ethernet_UPPER_protocol(cadru_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_intrare(cadru_INDEX, 14, cadru_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && primi_cloud_pachet(cadru_INDEX, 14);
    }

    private boolean primi_cloud_pachet(byte[] date, int Pornește) {
        if (!rețea_Instrumente.sisteme_de_informații_IPV_4_protocol(date, Pornește)) {
            return false;
        }
        int Antet_lungime = (date[Pornește] & 0x0f) * 4;
        int total_lungime = rețea_Instrumente.큰순서짧은정수(date, Pornește + 2);
        if (total_lungime < Antet_lungime || Pornește + total_lungime > date.length) {
            return false;
        }
        int caz_VALUE = date[Pornește + 9] & 0xff;
        int Conținut_buta = Pornește + Antet_lungime;
        int Conținut_lungime = total_lungime - Antet_lungime;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(caz_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_intrare(date, Conținut_buta, Conținut_lungime);
            return true;
        }
        if (Conținut_lungime < 4) {
            return false;
        }
        int destinație_număr_port = rețea_Instrumente.큰순서짧은정수(date, Conținut_buta + 2);
        Map<Integer, 자료처리기> muta_tabel = caz_VALUE == 17 ? 사용자자료단위처리기 : caz_VALUE == 6 ? 전송제어처리기 : null;
        if (muta_tabel == null) {
            return false;
        }
        자료처리기 포트처리기 = muta_tabel.get(Integer.valueOf(destinație_număr_port));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proces_VALUE_intrare(date, Conținut_buta, Conținut_lungime);
        return true;
    }
}

