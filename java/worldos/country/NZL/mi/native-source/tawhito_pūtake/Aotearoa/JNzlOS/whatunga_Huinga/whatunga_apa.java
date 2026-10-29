// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.whatunga_Huinga;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class whatunga_apa {
    @FunctionalInterface
    public interface 자료처리기 {
        void Hātepe_uara_tāurunga(byte[] raraunga, int whakahaere, int roa_uara);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void rēhita_Itarangi(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void rēhita_IP(int kēhi_uara, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(kēhi_uara & 0xff), 처리기);
    }

    public void rēhita_kaiwhakamahi_raraunga_ngā_wae(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void rēhita_tarenga_mana(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] tāpare_INDEX) {
        if (!whatunga_Ngā_Utauta.이더넷틀인가(tāpare_INDEX)) {
            return false;
        }
        int 종류 = whatunga_Ngā_Utauta.Itarangi_UPPER_kawa(tāpare_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Hātepe_uara_tāurunga(tāpare_INDEX, 14, tāpare_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(tāpare_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] raraunga, int whakahaere) {
        if (!whatunga_Ngā_Utauta.상호통신망규약사판인가(raraunga, whakahaere)) {
            return false;
        }
        int Pane_roa = (raraunga[whakahaere] & 0x0f) * 4;
        int 전체길이 = whatunga_Ngā_Utauta.큰순서짧은정수(raraunga, whakahaere + 2);
        if (전체길이 < Pane_roa || whakahaere + 전체길이 > raraunga.length) {
            return false;
        }
        int kēhi_uara = raraunga[whakahaere + 9] & 0xff;
        int Ihirangi_Start = whakahaere + Pane_roa;
        int Ihirangi_roa = 전체길이 - Pane_roa;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(kēhi_uara));
        if (직접처리기 != null) {
            직접처리기.Hātepe_uara_tāurunga(raraunga, Ihirangi_Start, Ihirangi_roa);
            return true;
        }
        if (Ihirangi_roa < 4) {
            return false;
        }
        int 목적포트 = whatunga_Ngā_Utauta.큰순서짧은정수(raraunga, Ihirangi_Start + 2);
        Map<Integer, 자료처리기> kawe_ripanga = kēhi_uara == 17 ? 사용자자료단위처리기 : kēhi_uara == 6 ? 전송제어처리기 : null;
        if (kawe_ripanga == null) {
            return false;
        }
        자료처리기 포트처리기 = kawe_ripanga.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Hātepe_uara_tāurunga(raraunga, Ihirangi_Start, Ihirangi_roa);
        return true;
    }
}

