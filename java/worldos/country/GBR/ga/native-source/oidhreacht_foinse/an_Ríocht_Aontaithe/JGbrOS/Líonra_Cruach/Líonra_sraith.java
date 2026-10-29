// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.Líonra_Cruach;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Líonra_sraith {
    @FunctionalInterface
    public interface 자료처리기 {
        void Próiseas_VALUE_iontráil(byte[] sonraí, int Rith_2, int fad_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void cláraigh_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void cláraigh_IP(int cás_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(cás_VALUE & 0xff), 처리기);
    }

    public void cláraigh_úsáideoir_sonraí_aonaid(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void cláraigh_tarchur_rialú(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] fráma_INDEX) {
        if (!Líonra_Uirlisí.teicneolaíocht_faisnéise_Ethernet_fráma(fráma_INDEX)) {
            return false;
        }
        int 종류 = Líonra_Uirlisí.Ethernet_UPPER_prótacal(fráma_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Próiseas_VALUE_iontráil(fráma_INDEX, 14, fráma_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(fráma_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] sonraí, int Rith_2) {
        if (!Líonra_Uirlisí.상호통신망규약사판인가(sonraí, Rith_2)) {
            return false;
        }
        int Ceanntásc_fad = (sonraí[Rith_2] & 0x0f) * 4;
        int 전체길이 = Líonra_Uirlisí.큰순서짧은정수(sonraí, Rith_2 + 2);
        if (전체길이 < Ceanntásc_fad || Rith_2 + 전체길이 > sonraí.length) {
            return false;
        }
        int cás_VALUE = sonraí[Rith_2 + 9] & 0xff;
        int Inneachar_Start = Rith_2 + Ceanntásc_fad;
        int Inneachar_fad = 전체길이 - Ceanntásc_fad;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(cás_VALUE));
        if (직접처리기 != null) {
            직접처리기.Próiseas_VALUE_iontráil(sonraí, Inneachar_Start, Inneachar_fad);
            return true;
        }
        if (Inneachar_fad < 4) {
            return false;
        }
        int sprioc_uimhir_phoirt = Líonra_Uirlisí.큰순서짧은정수(sonraí, Inneachar_Start + 2);
        Map<Integer, 자료처리기> port_tábla = cás_VALUE == 17 ? 사용자자료단위처리기 : cás_VALUE == 6 ? 전송제어처리기 : null;
        if (port_tábla == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tábla.get(Integer.valueOf(sprioc_uimhir_phoirt));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Próiseas_VALUE_iontráil(sonraí, Inneachar_Start, Inneachar_fad);
        return true;
    }
}

