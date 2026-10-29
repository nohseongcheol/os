// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frantzia.JFraOS.sare_pila;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class sare_maila {
    @FunctionalInterface
    public interface 자료처리기 {
        void prozesu_balio_sarrera(byte[] datuak, int Exekutatu_2, int luzera_balio);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void izena_eman_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void izena_eman_IP(int kasu_balio, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(kasu_balio & 0xff), 처리기);
    }

    public void izena_eman_erabiltzaile_datuak_unitate(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void izena_eman_transmisio_kontrol(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] marko_INDIZE) {
        if (!sare_Tresnak.informatika_Ethernet_marko(marko_INDIZE)) {
            return false;
        }
        int 종류 = sare_Tresnak.Ethernet_MAIUSKULA_protokolo(marko_INDIZE);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.prozesu_balio_sarrera(marko_INDIZE, 14, marko_INDIZE.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(marko_INDIZE, 14);
    }

    private boolean 상호통신망받기(byte[] datuak, int Exekutatu_2) {
        if (!sare_Tresnak.상호통신망규약사판인가(datuak, Exekutatu_2)) {
            return false;
        }
        int goiburu_luzera = (datuak[Exekutatu_2] & 0x0f) * 4;
        int 전체길이 = sare_Tresnak.큰순서짧은정수(datuak, Exekutatu_2 + 2);
        if (전체길이 < goiburu_luzera || Exekutatu_2 + 전체길이 > datuak.length) {
            return false;
        }
        int kasu_balio = datuak[Exekutatu_2 + 9] & 0xff;
        int eduki_HASI = Exekutatu_2 + goiburu_luzera;
        int eduki_luzera = 전체길이 - goiburu_luzera;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(kasu_balio));
        if (직접처리기 != null) {
            직접처리기.prozesu_balio_sarrera(datuak, eduki_HASI, eduki_luzera);
            return true;
        }
        if (eduki_luzera < 4) {
            return false;
        }
        int helburu_ataka_zenbaki = sare_Tresnak.큰순서짧은정수(datuak, eduki_HASI + 2);
        Map<Integer, 자료처리기> ataka_taula = kasu_balio == 17 ? 사용자자료단위처리기 : kasu_balio == 6 ? 전송제어처리기 : null;
        if (ataka_taula == null) {
            return false;
        }
        자료처리기 포트처리기 = ataka_taula.get(Integer.valueOf(helburu_ataka_zenbaki));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.prozesu_balio_sarrera(datuak, eduki_HASI, eduki_luzera);
        return true;
    }
}

