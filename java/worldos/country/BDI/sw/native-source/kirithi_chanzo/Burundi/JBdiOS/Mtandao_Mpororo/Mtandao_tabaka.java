// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Burundi.JBdiOS.Mtandao_Mpororo;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Mtandao_tabaka {
    @FunctionalInterface
    public interface 자료처리기 {
        void Mchakato_thamani_ingizo(byte[] data, int endesha, int urefu_thamani);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void sajili_Ethaneti(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void sajili_IP(int Kazi_thamani, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(Kazi_thamani & 0xff), 처리기);
    }

    public void sajili_mtumiaji_data_funzo(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void sajili_urushaji_udhibiti(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] fremu_kielezo) {
        if (!Mtandao_Zana.teknolojia_ya_maelezo_Ethaneti_fremu(fremu_kielezo)) {
            return false;
        }
        int 종류 = Mtandao_Zana.이더넷상위규약(fremu_kielezo);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Mchakato_thamani_ingizo(fremu_kielezo, 14, fremu_kielezo.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(fremu_kielezo, 14);
    }

    private boolean 상호통신망받기(byte[] data, int endesha) {
        if (!Mtandao_Zana.상호통신망규약사판인가(data, endesha)) {
            return false;
        }
        int kichwa_urefu = (data[endesha] & 0x0f) * 4;
        int 전체길이 = Mtandao_Zana.큰순서짧은정수(data, endesha + 2);
        if (전체길이 < kichwa_urefu || endesha + 전체길이 > data.length) {
            return false;
        }
        int Kazi_thamani = data[endesha + 9] & 0xff;
        int maudhui_Anza = endesha + kichwa_urefu;
        int maudhui_urefu = 전체길이 - kichwa_urefu;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(Kazi_thamani));
        if (직접처리기 != null) {
            직접처리기.Mchakato_thamani_ingizo(data, maudhui_Anza, maudhui_urefu);
            return true;
        }
        if (maudhui_urefu < 4) {
            return false;
        }
        int fikio_namba_ya_kituo = Mtandao_Zana.큰순서짧은정수(data, maudhui_Anza + 2);
        Map<Integer, 자료처리기> kituo_jedwali = Kazi_thamani == 17 ? 사용자자료단위처리기 : Kazi_thamani == 6 ? 전송제어처리기 : null;
        if (kituo_jedwali == null) {
            return false;
        }
        자료처리기 포트처리기 = kituo_jedwali.get(Integer.valueOf(fikio_namba_ya_kituo));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Mchakato_thamani_ingizo(data, maudhui_Anza, maudhui_urefu);
        return true;
    }
}

