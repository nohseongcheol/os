// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Shqipëri.JAlbOS.rrjet_Stivë;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class rrjet_Shtresë {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proces_VALUE_futje(byte[] të_dhëna, int Ekzekuto, int gjatësi_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void regjistroj_Eternet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void regjistroj_IP(int punë_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(punë_VALUE & 0xff), 처리기);
    }

    public void regjistroj_përdorues_të_dhëna_mësim(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void regjistroj_transmetim_kontroll(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] kuadër_INDEX) {
        if (!rrjet_Mjete.teknologjia_e_informacionit_Eternet_kuadër(kuadër_INDEX)) {
            return false;
        }
        int 종류 = rrjet_Mjete.Eternet_UPPER_protokoll(kuadër_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_futje(kuadër_INDEX, 14, kuadër_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(kuadër_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] të_dhëna, int Ekzekuto) {
        if (!rrjet_Mjete.상호통신망규약사판인가(të_dhëna, Ekzekuto)) {
            return false;
        }
        int Kreu_gjatësi = (të_dhëna[Ekzekuto] & 0x0f) * 4;
        int 전체길이 = rrjet_Mjete.큰순서짧은정수(të_dhëna, Ekzekuto + 2);
        if (전체길이 < Kreu_gjatësi || Ekzekuto + 전체길이 > të_dhëna.length) {
            return false;
        }
        int punë_VALUE = të_dhëna[Ekzekuto + 9] & 0xff;
        int Përmbajtje_nis = Ekzekuto + Kreu_gjatësi;
        int Përmbajtje_gjatësi = 전체길이 - Kreu_gjatësi;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(punë_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_futje(të_dhëna, Përmbajtje_nis, Përmbajtje_gjatësi);
            return true;
        }
        if (Përmbajtje_gjatësi < 4) {
            return false;
        }
        int vendmbërritje_numri_i_portës = rrjet_Mjete.큰순서짧은정수(të_dhëna, Përmbajtje_nis + 2);
        Map<Integer, 자료처리기> portë_tabelë = punë_VALUE == 17 ? 사용자자료단위처리기 : punë_VALUE == 6 ? 전송제어처리기 : null;
        if (portë_tabelë == null) {
            return false;
        }
        자료처리기 포트처리기 = portë_tabelë.get(Integer.valueOf(vendmbërritje_numri_i_portës));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proces_VALUE_futje(të_dhëna, Përmbajtje_nis, Përmbajtje_gjatësi);
        return true;
    }
}

