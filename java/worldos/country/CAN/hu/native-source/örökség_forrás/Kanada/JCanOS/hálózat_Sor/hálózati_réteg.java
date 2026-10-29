// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.hálózat_Sor;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP fogad_ÉRTÉK 분배를 한곳에서 관리한다. */
public final class hálózati_réteg {
    @FunctionalInterface
    public interface 자료처리기 {
        void folyamat_ÉRTÉK_bejegyzés(byte[] adat, int Futtatás, int hossz_ÉRTÉK);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void jegyzék_Ethernet(int Altípus_ÉRTÉK, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(Altípus_ÉRTÉK & 0xffff), 처리기);
    }

    public void jegyzék_IP(int szerződés_értéke, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(szerződés_értéke & 0xff), 처리기);
    }

    public void jegyzék_felhasználó_adat_lecke(int hardver_port, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(hardver_port & 0xffff), 처리기);
    }

    public void 전송제어등록(int hardver_port, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(hardver_port & 0xffff), 처리기);
    }

    public boolean fogad_Ethernet(byte[] doboz_INDEX) {
        if (!hálózat_Eszközök.informatikai_részleg_Ethernet_doboz(doboz_INDEX)) {
            return false;
        }
        int Altípus_ÉRTÉK = hálózat_Eszközök.Ethernet_NAGYBETŰS_protokoll(doboz_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(Altípus_ÉRTÉK));
        if (직접처리기 != null) {
            직접처리기.folyamat_ÉRTÉK_bejegyzés(doboz_INDEX, 14, doboz_INDEX.length - 14);
            return true;
        }
        return Altípus_ÉRTÉK == 0x0800 && fogad_háló_csomag(doboz_INDEX, 14);
    }

    private boolean fogad_háló_csomag(byte[] adat, int Futtatás) {
        if (!hálózat_Eszközök.informatikai_részleg_számlázási_árkülönbözet_4_protokoll(adat, Futtatás)) {
            return false;
        }
        int fejléc_hossz = (adat[Futtatás] & 0x0f) * 4;
        int összesen_hossz = hálózat_Eszközök.큰순서짧은정수(adat, Futtatás + 2);
        if (összesen_hossz < fejléc_hossz || Futtatás + összesen_hossz > adat.length) {
            return false;
        }
        int szerződés_értéke = adat[Futtatás + 9] & 0xff;
        int Tartalom_START = Futtatás + fejléc_hossz;
        int Tartalom_hossz = összesen_hossz - fejléc_hossz;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(szerződés_értéke));
        if (직접처리기 != null) {
            직접처리기.folyamat_ÉRTÉK_bejegyzés(adat, Tartalom_START, Tartalom_hossz);
            return true;
        }
        if (Tartalom_hossz < 4) {
            return false;
        }
        int cél_portszám = hálózat_Eszközök.큰순서짧은정수(adat, Tartalom_START + 2);
        Map<Integer, 자료처리기> port_tábla = szerződés_értéke == 17 ? 사용자자료단위처리기 : szerződés_értéke == 6 ? 전송제어처리기 : null;
        if (port_tábla == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tábla.get(Integer.valueOf(cél_portszám));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.folyamat_ÉRTÉK_bejegyzés(adat, Tartalom_START, Tartalom_hossz);
        return true;
    }
}

