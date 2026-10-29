// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.Mreža_snop;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Mreža_sloj {
    @FunctionalInterface
    public interface 자료처리기 {
        void proces_VALUE_unos(byte[] podaci, int Pokreni, int dužina_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void registrirati_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void registrirati_IP(int slučaj_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(slučaj_VALUE & 0xff), 처리기);
    }

    public void registrirati_korisnik_podaci_lekcija(int hardver_port, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(hardver_port & 0xffff), 처리기);
    }

    public void registrirati_prijenos_kontrola(int hardver_port, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(hardver_port & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] kadar_INDEX) {
        if (!Mreža_Alati.odjel_za_informacijske_tehnologije_Ethernet_kadar(kadar_INDEX)) {
            return false;
        }
        int 종류 = Mreža_Alati.Ethernet_UPPER_protokol(kadar_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.proces_VALUE_unos(kadar_INDEX, 14, kadar_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(kadar_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] podaci, int Pokreni) {
        if (!Mreža_Alati.상호통신망규약사판인가(podaci, Pokreni)) {
            return false;
        }
        int Zaglavlje_dužina = (podaci[Pokreni] & 0x0f) * 4;
        int 전체길이 = Mreža_Alati.큰순서짧은정수(podaci, Pokreni + 2);
        if (전체길이 < Zaglavlje_dužina || Pokreni + 전체길이 > podaci.length) {
            return false;
        }
        int slučaj_VALUE = podaci[Pokreni + 9] & 0xff;
        int Sadržaj_START = Pokreni + Zaglavlje_dužina;
        int Sadržaj_dužina = 전체길이 - Zaglavlje_dužina;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(slučaj_VALUE));
        if (직접처리기 != null) {
            직접처리기.proces_VALUE_unos(podaci, Sadržaj_START, Sadržaj_dužina);
            return true;
        }
        if (Sadržaj_dužina < 4) {
            return false;
        }
        int odredište_broj_priključka = Mreža_Alati.큰순서짧은정수(podaci, Sadržaj_START + 2);
        Map<Integer, 자료처리기> port_tabela = slučaj_VALUE == 17 ? 사용자자료단위처리기 : slučaj_VALUE == 6 ? 전송제어처리기 : null;
        if (port_tabela == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tabela.get(Integer.valueOf(odredište_broj_priključka));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.proces_VALUE_unos(podaci, Sadržaj_START, Sadržaj_dužina);
        return true;
    }
}

