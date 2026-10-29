// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sverige.JSweOS.nätverk_Stack;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP få_värde 분배를 한곳에서 관리한다. */
public final class nätverksnivå {
    @FunctionalInterface
    public interface 자료처리기 {
        void Process_värde_post(byte[] data, int Kör, int längd_värde);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void register_Ethernet(int variant_värde, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(variant_värde & 0xffff), 처리기);
    }

    public void register_IP(int kontraktsvärde, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(kontraktsvärde & 0xff), 처리기);
    }

    public void register_användare_data_enhet(int maskinvara_port, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(maskinvara_port & 0xffff), 처리기);
    }

    public void 전송제어등록(int maskinvara_port, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(maskinvara_port & 0xffff), 처리기);
    }

    public boolean få_Ethernet(byte[] ram_INDEX) {
        if (!nätverk_Verktyg.informationsteknik_Ethernet_ram(ram_INDEX)) {
            return false;
        }
        int variant_värde = nätverk_Verktyg.Ethernet_VERSALER_protokoll(ram_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(variant_värde));
        if (직접처리기 != null) {
            직접처리기.Process_värde_post(ram_INDEX, 14, ram_INDEX.length - 14);
            return true;
        }
        return variant_värde == 0x0800 && få_nät_paket(ram_INDEX, 14);
    }

    private boolean få_nät_paket(byte[] data, int Kör) {
        if (!nätverk_Verktyg.informationsteknik_FPV_4_protokoll(data, Kör)) {
            return false;
        }
        int huvud_längd = (data[Kör] & 0x0f) * 4;
        int summa_längd = nätverk_Verktyg.큰순서짧은정수(data, Kör + 2);
        if (summa_längd < huvud_längd || Kör + summa_längd > data.length) {
            return false;
        }
        int kontraktsvärde = data[Kör + 9] & 0xff;
        int Innehåll_START = Kör + huvud_längd;
        int Innehåll_längd = summa_längd - huvud_längd;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(kontraktsvärde));
        if (직접처리기 != null) {
            직접처리기.Process_värde_post(data, Innehåll_START, Innehåll_längd);
            return true;
        }
        if (Innehåll_längd < 4) {
            return false;
        }
        int mål_portnummer = nätverk_Verktyg.큰순서짧은정수(data, Innehåll_START + 2);
        Map<Integer, 자료처리기> port_tabell = kontraktsvärde == 17 ? 사용자자료단위처리기 : kontraktsvärde == 6 ? 전송제어처리기 : null;
        if (port_tabell == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tabell.get(Integer.valueOf(mål_portnummer));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Process_värde_post(data, Innehåll_START, Innehåll_längd);
        return true;
    }
}

