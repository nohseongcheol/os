// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.Neteweke_kokoanyodinepe;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Neteweke_boalo {
    @FunctionalInterface
    public interface 자료처리기 {
        void Thulaganyo_Boleng_tsenyo(byte[] tshedimosetso, int dirisa, int boleele_Boleng);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void kwadisa_Ithanete(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void kwadisa_IP(int konteraka_Boleng, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(konteraka_Boleng & 0xff), 처리기);
    }

    public void kwadisa_modirisi_tshedimosetso_thuto(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void kwadisa_phetiso_taolo(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] Foreimi_tshupane) {
        if (!Neteweke_Thuluse.이더넷틀인가(Foreimi_tshupane)) {
            return false;
        }
        int 종류 = Neteweke_Thuluse.이더넷상위규약(Foreimi_tshupane);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Thulaganyo_Boleng_tsenyo(Foreimi_tshupane, 14, Foreimi_tshupane.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(Foreimi_tshupane, 14);
    }

    private boolean 상호통신망받기(byte[] tshedimosetso, int dirisa) {
        if (!Neteweke_Thuluse.상호통신망규약사판인가(tshedimosetso, dirisa)) {
            return false;
        }
        int setlhogo_boleele = (tshedimosetso[dirisa] & 0x0f) * 4;
        int 전체길이 = Neteweke_Thuluse.큰순서짧은정수(tshedimosetso, dirisa + 2);
        if (전체길이 < setlhogo_boleele || dirisa + 전체길이 > tshedimosetso.length) {
            return false;
        }
        int konteraka_Boleng = tshedimosetso[dirisa + 9] & 0xff;
        int Diteng_simolola = dirisa + setlhogo_boleele;
        int Diteng_boleele = 전체길이 - setlhogo_boleele;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(konteraka_Boleng));
        if (직접처리기 != null) {
            직접처리기.Thulaganyo_Boleng_tsenyo(tshedimosetso, Diteng_simolola, Diteng_boleele);
            return true;
        }
        if (Diteng_boleele < 4) {
            return false;
        }
        int 목적포트 = Neteweke_Thuluse.큰순서짧은정수(tshedimosetso, Diteng_simolola + 2);
        Map<Integer, 자료처리기> gorogisetsa_lenaneothalo = konteraka_Boleng == 17 ? 사용자자료단위처리기 : konteraka_Boleng == 6 ? 전송제어처리기 : null;
        if (gorogisetsa_lenaneothalo == null) {
            return false;
        }
        자료처리기 포트처리기 = gorogisetsa_lenaneothalo.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Thulaganyo_Boleng_tsenyo(tshedimosetso, Diteng_simolola, Diteng_boleele);
        return true;
    }
}

