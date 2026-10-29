// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.Netweke_kgoboko;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Netweke_llaga {
    @FunctionalInterface
    public interface 자료처리기 {
        void tiragalo_boleng_go_tsenya_tshedimošo(byte[] data, int Diriša, int botelele_boleng);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void ngwadiša_Ethenete(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void ngwadiša_IP(int taba_boleng, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(taba_boleng & 0xff), 처리기);
    }

    public void ngwadiša_mošomiši_data_thutišo(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void ngwadiša_phetišetšo_taolo(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] freime_lokela) {
        if (!Netweke_Ditholosi.이더넷틀인가(freime_lokela)) {
            return false;
        }
        int 종류 = Netweke_Ditholosi.이더넷상위규약(freime_lokela);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.tiragalo_boleng_go_tsenya_tshedimošo(freime_lokela, 14, freime_lokela.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(freime_lokela, 14);
    }

    private boolean 상호통신망받기(byte[] data, int Diriša) {
        if (!Netweke_Ditholosi.상호통신망규약사판인가(data, Diriša)) {
            return false;
        }
        int Hlogo_botelele = (data[Diriša] & 0x0f) * 4;
        int 전체길이 = Netweke_Ditholosi.큰순서짧은정수(data, Diriša + 2);
        if (전체길이 < Hlogo_botelele || Diriša + 전체길이 > data.length) {
            return false;
        }
        int taba_boleng = data[Diriša + 9] & 0xff;
        int Diteng_Thomišo = Diriša + Hlogo_botelele;
        int Diteng_botelele = 전체길이 - Hlogo_botelele;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(taba_boleng));
        if (직접처리기 != null) {
            직접처리기.tiragalo_boleng_go_tsenya_tshedimošo(data, Diteng_Thomišo, Diteng_botelele);
            return true;
        }
        if (Diteng_botelele < 4) {
            return false;
        }
        int 목적포트 = Netweke_Ditholosi.큰순서짧은정수(data, Diteng_Thomišo + 2);
        Map<Integer, 자료처리기> phote_tafola = taba_boleng == 17 ? 사용자자료단위처리기 : taba_boleng == 6 ? 전송제어처리기 : null;
        if (phote_tafola == null) {
            return false;
        }
        자료처리기 포트처리기 = phote_tafola.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.tiragalo_boleng_go_tsenya_tshedimošo(data, Diteng_Thomišo, Diteng_botelele);
        return true;
    }
}

