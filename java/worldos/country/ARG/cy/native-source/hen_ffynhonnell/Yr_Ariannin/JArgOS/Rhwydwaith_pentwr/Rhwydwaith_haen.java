// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yr_Ariannin.JArgOS.Rhwydwaith_pentwr;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Rhwydwaith_haen {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proses_VALUE_cofnod(byte[] data, int Gweithredu_2, int hyd_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void cofrestru_Ether_rwyd(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void cofrestru_IP(int tasg_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(tasg_VALUE & 0xff), 처리기);
    }

    public void cofrestru_defnyddiwr_data_gwers(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void cofrestru_trawsyriant_rheoli(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ffrâm_INDEX) {
        if (!Rhwydwaith_Offer.technoleg_gwybodaeth_Ether_rwyd_ffrâm(ffrâm_INDEX)) {
            return false;
        }
        int 종류 = Rhwydwaith_Offer.Ether_rwyd_UPPER_protocol(ffrâm_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proses_VALUE_cofnod(ffrâm_INDEX, 14, ffrâm_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ffrâm_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] data, int Gweithredu_2) {
        if (!Rhwydwaith_Offer.상호통신망규약사판인가(data, Gweithredu_2)) {
            return false;
        }
        int Pennyn_hyd = (data[Gweithredu_2] & 0x0f) * 4;
        int 전체길이 = Rhwydwaith_Offer.큰순서짧은정수(data, Gweithredu_2 + 2);
        if (전체길이 < Pennyn_hyd || Gweithredu_2 + 전체길이 > data.length) {
            return false;
        }
        int tasg_VALUE = data[Gweithredu_2 + 9] & 0xff;
        int Cynnwys_START = Gweithredu_2 + Pennyn_hyd;
        int Cynnwys_hyd = 전체길이 - Pennyn_hyd;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(tasg_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proses_VALUE_cofnod(data, Cynnwys_START, Cynnwys_hyd);
            return true;
        }
        if (Cynnwys_hyd < 4) {
            return false;
        }
        int cyrchfan_rhif_porth = Rhwydwaith_Offer.큰순서짧은정수(data, Cynnwys_START + 2);
        Map<Integer, 자료처리기> porth_tabl = tasg_VALUE == 17 ? 사용자자료단위처리기 : tasg_VALUE == 6 ? 전송제어처리기 : null;
        if (porth_tabl == null) {
            return false;
        }
        자료처리기 포트처리기 = porth_tabl.get(Integer.valueOf(cyrchfan_rhif_porth));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proses_VALUE_cofnod(data, Cynnwys_START, Cynnwys_hyd);
        return true;
    }
}

