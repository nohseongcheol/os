// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.mreža_Sklad;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP sprejeti_sprejemati_prejeti_prejemati_VALUE 분배를 한곳에서 관리한다. */
public final class omrežna_plast {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proces_VALUE_vnos(byte[] podatki, int Zaženi, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void register_ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void register_IP(int primer_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(primer_VALUE & 0xff), 처리기);
    }

    public void register_uporabnik_podatki_enota(int strojna_oprema_vrata, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(strojna_oprema_vrata & 0xffff), 처리기);
    }

    public void 전송제어등록(int strojna_oprema_vrata, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(strojna_oprema_vrata & 0xffff), 처리기);
    }

    public boolean sprejeti_sprejemati_prejeti_prejemati_ethernet(byte[] okvir_INDEX) {
        if (!mreža_Orodja.informacijska_tehnologija_ethernet_okvir(okvir_INDEX)) {
            return false;
        }
        int 종류 = mreža_Orodja.ethernet_UPPER_protokol(okvir_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_vnos(okvir_INDEX, 14, okvir_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && sprejeti_sprejemati_prejeti_prejemati_oblak_paket(okvir_INDEX, 14);
    }

    private boolean sprejeti_sprejemati_prejeti_prejemati_oblak_paket(byte[] podatki, int Zaženi) {
        if (!mreža_Orodja.상호통신망규약사판인가(podatki, Zaženi)) {
            return false;
        }
        int 머리길이 = (podatki[Zaženi] & 0x0f) * 4;
        int 전체길이 = mreža_Orodja.큰순서짧은정수(podatki, Zaženi + 2);
        if (전체길이 < 머리길이 || Zaženi + 전체길이 > podatki.length) {
            return false;
        }
        int primer_VALUE = podatki[Zaženi + 9] & 0xff;
        int vsebina_Start = Zaženi + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(primer_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_vnos(podatki, vsebina_Start, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int cilj_številka_vrat = mreža_Orodja.큰순서짧은정수(podatki, vsebina_Start + 2);
        Map<Integer, 자료처리기> vrata_tabela = primer_VALUE == 17 ? 사용자자료단위처리기 : primer_VALUE == 6 ? 전송제어처리기 : null;
        if (vrata_tabela == null) {
            return false;
        }
        자료처리기 포트처리기 = vrata_tabela.get(Integer.valueOf(cilj_številka_vrat));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proces_VALUE_vnos(podatki, vsebina_Start, 내용길이);
        return true;
    }
}

