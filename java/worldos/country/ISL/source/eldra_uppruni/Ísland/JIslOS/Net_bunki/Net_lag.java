// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.Net_bunki;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Net_lag {
    @FunctionalInterface
    public interface 자료처리기 {
        void Ferli_VALUE_færsla(byte[] gögn, int Keyra_2, int lengd_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void skrá_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void skrá_IP(int samningsvirði, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(samningsvirði & 0xff), 처리기);
    }

    public void skrá_notandi_gögn_eining(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void skrá_sending_stýring(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ramma_INDEX) {
        if (!Net_Verkfæri.upplýsingatækni_Ethernet_ramma(ramma_INDEX)) {
            return false;
        }
        int 종류 = Net_Verkfæri.Ethernet_UPPER_samskiptaregla(ramma_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Ferli_VALUE_færsla(ramma_INDEX, 14, ramma_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ramma_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] gögn, int Keyra_2) {
        if (!Net_Verkfæri.upplýsingatækni_verðfrávik_reiknings_4_samskiptaregla(gögn, Keyra_2)) {
            return false;
        }
        int Haus_lengd = (gögn[Keyra_2] & 0x0f) * 4;
        int samtala_lengd = Net_Verkfæri.큰순서짧은정수(gögn, Keyra_2 + 2);
        if (samtala_lengd < Haus_lengd || Keyra_2 + samtala_lengd > gögn.length) {
            return false;
        }
        int samningsvirði = gögn[Keyra_2 + 9] & 0xff;
        int Efni_Opna = Keyra_2 + Haus_lengd;
        int Efni_lengd = samtala_lengd - Haus_lengd;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(samningsvirði));
        if (직접처리기 != null) {
            직접처리기.Ferli_VALUE_færsla(gögn, Efni_Opna, Efni_lengd);
            return true;
        }
        if (Efni_lengd < 4) {
            return false;
        }
        int endastaður_tengisnúmer = Net_Verkfæri.큰순서짧은정수(gögn, Efni_Opna + 2);
        Map<Integer, 자료처리기> gátt_tafla = samningsvirði == 17 ? 사용자자료단위처리기 : samningsvirði == 6 ? 전송제어처리기 : null;
        if (gátt_tafla == null) {
            return false;
        }
        자료처리기 포트처리기 = gátt_tafla.get(Integer.valueOf(endastaður_tengisnúmer));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Ferli_VALUE_færsla(gögn, Efni_Opna, Efni_lengd);
        return true;
    }
}

