// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.netwerk_Munzell;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class netwerk_saff {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proċess_VALUE_entrata(byte[] data, int serje, int tul_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void i_rreġistra_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void i_rreġistra_IP(int każ_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(każ_VALUE & 0xff), 처리기);
    }

    public void i_rreġistra_utent_data_lezzjoni(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void i_rreġistra_trażmissjoni_kontroll(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] frejm_INDEX) {
        if (!netwerk_Għodod.이더넷틀인가(frejm_INDEX)) {
            return false;
        }
        int 종류 = netwerk_Għodod.Ethernet_UPPER_protokoll(frejm_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proċess_VALUE_entrata(frejm_INDEX, 14, frejm_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(frejm_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] data, int serje) {
        if (!netwerk_Għodod.상호통신망규약사판인가(data, serje)) {
            return false;
        }
        int Intestazzjoni_tul = (data[serje] & 0x0f) * 4;
        int 전체길이 = netwerk_Għodod.큰순서짧은정수(data, serje + 2);
        if (전체길이 < Intestazzjoni_tul || serje + 전체길이 > data.length) {
            return false;
        }
        int każ_VALUE = data[serje + 9] & 0xff;
        int Kontenut_Bidu = serje + Intestazzjoni_tul;
        int Kontenut_tul = 전체길이 - Intestazzjoni_tul;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(każ_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proċess_VALUE_entrata(data, Kontenut_Bidu, Kontenut_tul);
            return true;
        }
        if (Kontenut_tul < 4) {
            return false;
        }
        int 목적포트 = netwerk_Għodod.큰순서짧은정수(data, Kontenut_Bidu + 2);
        Map<Integer, 자료처리기> port_tabella = każ_VALUE == 17 ? 사용자자료단위처리기 : każ_VALUE == 6 ? 전송제어처리기 : null;
        if (port_tabella == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tabella.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proċess_VALUE_entrata(data, Kontenut_Bidu, Kontenut_tul);
        return true;
    }
}

