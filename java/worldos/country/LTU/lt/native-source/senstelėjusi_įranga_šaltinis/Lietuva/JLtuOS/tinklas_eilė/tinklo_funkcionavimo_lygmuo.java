// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuva.JLtuOS.tinklas_eilė;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP gauti_VALUE_cef4d8ab 분배를 한곳에서 관리한다. */
public final class tinklo_funkcionavimo_lygmuo {
    @FunctionalInterface
    public interface 자료처리기 {
        void Procesas_VALUE_įrašas(byte[] duomenys, int Paleisti, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void registras_eternetas(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void registras_IP(int sutarties_vertė, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(sutarties_vertė & 0xff), 처리기);
    }

    public void registras_naudotojas_duomenys_pamoka(int aparatūra_jungtis, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(aparatūra_jungtis & 0xffff), 처리기);
    }

    public void 전송제어등록(int aparatūra_jungtis, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(aparatūra_jungtis & 0xffff), 처리기);
    }

    public boolean gauti_eternetas(byte[] kadras_INDEX) {
        if (!tinklas_Įrankiai.informacinės_technologijos_eternetas_kadras(kadras_INDEX)) {
            return false;
        }
        int 종류 = tinklas_Įrankiai.eternetas_UPPER_protokolas(kadras_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Procesas_VALUE_įrašas(kadras_INDEX, 14, kadras_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && gauti_debesis_paketas(kadras_INDEX, 14);
    }

    private boolean gauti_debesis_paketas(byte[] duomenys, int Paleisti) {
        if (!tinklas_Įrankiai.informacinės_technologijos_SKN_4_protokolas(duomenys, Paleisti)) {
            return false;
        }
        int 머리길이 = (duomenys[Paleisti] & 0x0f) * 4;
        int 전체길이 = tinklas_Įrankiai.큰순서짧은정수(duomenys, Paleisti + 2);
        if (전체길이 < 머리길이 || Paleisti + 전체길이 > duomenys.length) {
            return false;
        }
        int sutarties_vertė = duomenys[Paleisti + 9] & 0xff;
        int Turinys_Start = Paleisti + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(sutarties_vertė));
        if (직접처리기 != null) {
            직접처리기.Procesas_VALUE_įrašas(duomenys, Turinys_Start, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int vieta_prievado_numeris = tinklas_Įrankiai.큰순서짧은정수(duomenys, Turinys_Start + 2);
        Map<Integer, 자료처리기> jungtis_lentelė = sutarties_vertė == 17 ? 사용자자료단위처리기 : sutarties_vertė == 6 ? 전송제어처리기 : null;
        if (jungtis_lentelė == null) {
            return false;
        }
        자료처리기 포트처리기 = jungtis_lentelė.get(Integer.valueOf(vieta_prievado_numeris));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Procesas_VALUE_įrašas(duomenys, Turinys_Start, 내용길이);
        return true;
    }
}

