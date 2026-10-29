// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Crna_Gora.JMneOS.Mreža_stek;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP primiti_VALUE 분배를 한곳에서 관리한다. */
public final class sloj_mreže {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proces_VALUE_stavka(byte[] podaci, int koristiti, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void registar_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void registar_IP(int ugovor_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ugovor_VALUE & 0xff), 처리기);
    }

    public void registar_korisnik_podaci_lekcija(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean primiti_Ethernet(byte[] kadar_INDEX) {
        if (!Mreža_Alatke.informatičko_odeljenje_Ethernet_kadar(kadar_INDEX)) {
            return false;
        }
        int 종류 = Mreža_Alatke.Ethernet_UPPER_protokol(kadar_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_stavka(kadar_INDEX, 14, kadar_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && primiti_oblak_paket(kadar_INDEX, 14);
    }

    private boolean primiti_oblak_paket(byte[] podaci, int koristiti) {
        if (!Mreža_Alatke.상호통신망규약사판인가(podaci, koristiti)) {
            return false;
        }
        int 머리길이 = (podaci[koristiti] & 0x0f) * 4;
        int 전체길이 = Mreža_Alatke.큰순서짧은정수(podaci, koristiti + 2);
        if (전체길이 < 머리길이 || koristiti + 전체길이 > podaci.length) {
            return false;
        }
        int ugovor_VALUE = podaci[koristiti + 9] & 0xff;
        int Sadržaj_START = koristiti + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ugovor_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proces_VALUE_stavka(podaci, Sadržaj_START, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int odredište_broj_porta = Mreža_Alatke.큰순서짧은정수(podaci, Sadržaj_START + 2);
        Map<Integer, 자료처리기> port_tabela = ugovor_VALUE == 17 ? 사용자자료단위처리기 : ugovor_VALUE == 6 ? 전송제어처리기 : null;
        if (port_tabela == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tabela.get(Integer.valueOf(odredište_broj_porta));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proces_VALUE_stavka(podaci, Sadržaj_START, 내용길이);
        return true;
    }
}

