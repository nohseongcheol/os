// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.mbaal_Tegalo;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class mbaal_déggoob_wet {
    @FunctionalInterface
    public interface 자료처리기 {
        void yokkute_xëyma_dugal_xabaar(byte[] mbir, int daw, int diir_xëyma);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void bindu_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void bindu_IP(int ay_xëyma, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ay_xëyma & 0xff), 처리기);
    }

    public void bindu_kiy_jariñoo_internet_mbir_sa(int jumtukaay_jël, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(jumtukaay_jël & 0xffff), 처리기);
    }

    public void bindu_jokalinu_xibaar_Saytu_doxinu_ordinateur(int jumtukaay_jël, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(jumtukaay_jël & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] kadar_àlluwa_tur) {
        if (!mbaal_Jumtukaay_yi.이더넷틀인가(kadar_àlluwa_tur)) {
            return false;
        }
        int 종류 = mbaal_Jumtukaay_yi.이더넷상위규약(kadar_àlluwa_tur);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.yokkute_xëyma_dugal_xabaar(kadar_àlluwa_tur, 14, kadar_àlluwa_tur.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(kadar_àlluwa_tur, 14);
    }

    private boolean 상호통신망받기(byte[] mbir, int daw) {
        if (!mbaal_Jumtukaay_yi.상호통신망규약사판인가(mbir, daw)) {
            return false;
        }
        int Tur_diir = (mbir[daw] & 0x0f) * 4;
        int 전체길이 = mbaal_Jumtukaay_yi.큰순서짧은정수(mbir, daw + 2);
        if (전체길이 < Tur_diir || daw + 전체길이 > mbir.length) {
            return false;
        }
        int ay_xëyma = mbir[daw + 9] & 0xff;
        int Këmb_Door = daw + Tur_diir;
        int Këmb_diir = 전체길이 - Tur_diir;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ay_xëyma));
        if (직접처리기 != null) {
            직접처리기.yokkute_xëyma_dugal_xabaar(mbir, Këmb_Door, Këmb_diir);
            return true;
        }
        if (Këmb_diir < 4) {
            return false;
        }
        int 목적포트 = mbaal_Jumtukaay_yi.큰순서짧은정수(mbir, Këmb_Door + 2);
        Map<Integer, 자료처리기> jël_àlluwa = ay_xëyma == 17 ? 사용자자료단위처리기 : ay_xëyma == 6 ? 전송제어처리기 : null;
        if (jël_àlluwa == null) {
            return false;
        }
        자료처리기 포트처리기 = jël_àlluwa.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.yokkute_xëyma_dugal_xabaar(mbir, Këmb_Door, Këmb_diir);
        return true;
    }
}

