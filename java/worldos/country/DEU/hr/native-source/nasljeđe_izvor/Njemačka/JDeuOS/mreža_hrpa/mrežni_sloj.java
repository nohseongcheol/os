// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Njemačka.JDeuOS.mreža_hrpa;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP primiti_VALUE 분배를 한곳에서 관리한다. */
public final class mrežni_sloj {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proces_VALUE_unos(byte[] podaci, int Pokreni, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void registar_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void registar_IP(int slučaj_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(slučaj_VALUE & 0xff), 처리기);
    }

    public void registar_korisnik_podaci_lekcija(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean primiti_Ethernet(byte[] kadar_INDEX) {
        if (!mreža_Alati.odjel_informacijske_tehnologije_Ethernet_kadar(kadar_INDEX)) {
            return false;
        }
        int 종류 = mreža_Alati.Ethernet_UPPER_protokol(kadar_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_unos(kadar_INDEX, 14, kadar_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && primiti_oblak_paket(kadar_INDEX, 14);
    }

    private boolean primiti_oblak_paket(byte[] podaci, int Pokreni) {
        if (!mreža_Alati.상호통신망규약사판인가(podaci, Pokreni)) {
            return false;
        }
        int 머리길이 = (podaci[Pokreni] & 0x0f) * 4;
        int 전체길이 = mreža_Alati.큰순서짧은정수(podaci, Pokreni + 2);
        if (전체길이 < 머리길이 || Pokreni + 전체길이 > podaci.length) {
            return false;
        }
        int slučaj_VALUE = podaci[Pokreni + 9] & 0xff;
        int Sadržaj_START = Pokreni + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(slučaj_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_unos(podaci, Sadržaj_START, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int odredište_broj_priključka = mreža_Alati.큰순서짧은정수(podaci, Sadržaj_START + 2);
        Map<Integer, 자료처리기> prebaciti_tablica = slučaj_VALUE == 17 ? 사용자자료단위처리기 : slučaj_VALUE == 6 ? 전송제어처리기 : null;
        if (prebaciti_tablica == null) {
            return false;
        }
        자료처리기 포트처리기 = prebaciti_tablica.get(Integer.valueOf(odredište_broj_priključka));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proces_VALUE_unos(podaci, Sadržaj_START, 내용길이);
        return true;
    }
}

