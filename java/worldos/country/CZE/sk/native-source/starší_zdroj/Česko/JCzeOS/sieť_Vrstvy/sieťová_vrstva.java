// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.sieť_Vrstvy;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP dostať_VALUE 분배를 한곳에서 관리한다. */
public final class sieťová_vrstva {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proces_VALUE_položka(byte[] údaje, int Spustiť_2, int dĺžka_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void register_sieť_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void register_IP(int prípad_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(prípad_VALUE & 0xff), 처리기);
    }

    public void register_používateľ_údaje_lekcia(int hardvér_port, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(hardvér_port & 0xffff), 처리기);
    }

    public void 전송제어등록(int hardvér_port, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(hardvér_port & 0xffff), 처리기);
    }

    public boolean dostať_sieť_Ethernet(byte[] rám_INDEX) {
        if (!sieť_Nástroje.Informačné_systémy_sieť_Ethernet_rám(rám_INDEX)) {
            return false;
        }
        int 종류 = sieť_Nástroje.sieť_Ethernet_UPPER_protokol(rám_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_položka(rám_INDEX, 14, rám_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && dostať_cloud_paket(rám_INDEX, 14);
    }

    private boolean dostať_cloud_paket(byte[] údaje, int Spustiť_2) {
        if (!sieť_Nástroje.상호통신망규약사판인가(údaje, Spustiť_2)) {
            return false;
        }
        int Nadpis_dĺžka = (údaje[Spustiť_2] & 0x0f) * 4;
        int celkovo_dĺžka = sieť_Nástroje.큰순서짧은정수(údaje, Spustiť_2 + 2);
        if (celkovo_dĺžka < Nadpis_dĺžka || Spustiť_2 + celkovo_dĺžka > údaje.length) {
            return false;
        }
        int prípad_VALUE = údaje[Spustiť_2 + 9] & 0xff;
        int obsah_START = Spustiť_2 + Nadpis_dĺžka;
        int obsah_dĺžka = celkovo_dĺžka - Nadpis_dĺžka;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(prípad_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_položka(údaje, obsah_START, obsah_dĺžka);
            return true;
        }
        if (obsah_dĺžka < 4) {
            return false;
        }
        int cieľ_číslo_portu = sieť_Nástroje.큰순서짧은정수(údaje, obsah_START + 2);
        Map<Integer, 자료처리기> port_tabuľka = prípad_VALUE == 17 ? 사용자자료단위처리기 : prípad_VALUE == 6 ? 전송제어처리기 : null;
        if (port_tabuľka == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tabuľka.get(Integer.valueOf(cieľ_číslo_portu));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proces_VALUE_položka(údaje, obsah_START, obsah_dĺžka);
        return true;
    }
}

