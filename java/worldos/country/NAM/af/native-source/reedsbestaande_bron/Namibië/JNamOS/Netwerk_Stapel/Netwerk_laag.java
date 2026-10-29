// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Namibië.JNamOS.Netwerk_Stapel;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Netwerk_laag {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proses_VALUE_inskrywing(byte[] data, int Loop, int lengte_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void registreer_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void registreer_IP(int saak_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(saak_VALUE & 0xff), 처리기);
    }

    public void registreer_gebruiker_data_les(int hardeware_ombou, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(hardeware_ombou & 0xffff), 처리기);
    }

    public void registreer_oordrag_kontrole(int hardeware_ombou, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(hardeware_ombou & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] raam_INDEX) {
        if (!Netwerk_Nutsmiddels.이더넷틀인가(raam_INDEX)) {
            return false;
        }
        int 종류 = Netwerk_Nutsmiddels.Ethernet_UPPER_protokol(raam_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proses_VALUE_inskrywing(raam_INDEX, 14, raam_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(raam_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] data, int Loop) {
        if (!Netwerk_Nutsmiddels.상호통신망규약사판인가(data, Loop)) {
            return false;
        }
        int Loopkop_lengte = (data[Loop] & 0x0f) * 4;
        int 전체길이 = Netwerk_Nutsmiddels.큰순서짧은정수(data, Loop + 2);
        if (전체길이 < Loopkop_lengte || Loop + 전체길이 > data.length) {
            return false;
        }
        int saak_VALUE = data[Loop + 9] & 0xff;
        int Inhoud_BEGIN = Loop + Loopkop_lengte;
        int Inhoud_lengte = 전체길이 - Loopkop_lengte;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(saak_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proses_VALUE_inskrywing(data, Inhoud_BEGIN, Inhoud_lengte);
            return true;
        }
        if (Inhoud_lengte < 4) {
            return false;
        }
        int 목적포트 = Netwerk_Nutsmiddels.큰순서짧은정수(data, Inhoud_BEGIN + 2);
        Map<Integer, 자료처리기> ombou_tabel = saak_VALUE == 17 ? 사용자자료단위처리기 : saak_VALUE == 6 ? 전송제어처리기 : null;
        if (ombou_tabel == null) {
            return false;
        }
        자료처리기 포트처리기 = ombou_tabel.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proses_VALUE_inskrywing(data, Inhoud_BEGIN, Inhoud_lengte);
        return true;
    }
}

