// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gana.JGhaOS.Hanyar_sadarwa_tara;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Hanyar_sadarwa_Tsarkiya {
    @FunctionalInterface
    public interface 자료처리기 {
        void haryar_aikin_na_ura_Daraja_Mashigar_bayanai(byte[] Tarin_bayani, int Tafiyar_da, int Tsawo_Daraja);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int Kes_Daraja, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(Kes_Daraja & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int kayan_haɗi_na_kwamfuta_fot, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(kayan_haɗi_na_kwamfuta_fot & 0xffff), 처리기);
    }

    public void 전송제어등록(int kayan_haɗi_na_kwamfuta_fot, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(kayan_haɗi_na_kwamfuta_fot & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] allo_Indes) {
        if (!Hanyar_sadarwa_Kaya.kimiyar_bayanai_Wayar_kwamfuta_ta_yanar_gizo_allo(allo_Indes)) {
            return false;
        }
        int 종류 = Hanyar_sadarwa_Kaya.이더넷상위규약(allo_Indes);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.haryar_aikin_na_ura_Daraja_Mashigar_bayanai(allo_Indes, 14, allo_Indes.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(allo_Indes, 14);
    }

    private boolean 상호통신망받기(byte[] Tarin_bayani, int Tafiyar_da) {
        if (!Hanyar_sadarwa_Kaya.상호통신망규약사판인가(Tarin_bayani, Tafiyar_da)) {
            return false;
        }
        int Kai_Tsawo = (Tarin_bayani[Tafiyar_da] & 0x0f) * 4;
        int 전체길이 = Hanyar_sadarwa_Kaya.큰순서짧은정수(Tarin_bayani, Tafiyar_da + 2);
        if (전체길이 < Kai_Tsawo || Tafiyar_da + 전체길이 > Tarin_bayani.length) {
            return false;
        }
        int Kes_Daraja = Tarin_bayani[Tafiyar_da + 9] & 0xff;
        int kunshiya_Fara = Tafiyar_da + Kai_Tsawo;
        int kunshiya_Tsawo = 전체길이 - Kai_Tsawo;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(Kes_Daraja));
        if (직접처리기 != null) {
            직접처리기.haryar_aikin_na_ura_Daraja_Mashigar_bayanai(Tarin_bayani, kunshiya_Fara, kunshiya_Tsawo);
            return true;
        }
        if (kunshiya_Tsawo < 4) {
            return false;
        }
        int Zangon_ƙarshe_lambar_kafa = Hanyar_sadarwa_Kaya.큰순서짧은정수(Tarin_bayani, kunshiya_Fara + 2);
        Map<Integer, 자료처리기> fot_tebur = Kes_Daraja == 17 ? 사용자자료단위처리기 : Kes_Daraja == 6 ? 전송제어처리기 : null;
        if (fot_tebur == null) {
            return false;
        }
        자료처리기 포트처리기 = fot_tebur.get(Integer.valueOf(Zangon_ƙarshe_lambar_kafa));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.haryar_aikin_na_ura_Daraja_Mashigar_bayanai(Tarin_bayani, kunshiya_Fara, kunshiya_Tsawo);
        return true;
    }
}

