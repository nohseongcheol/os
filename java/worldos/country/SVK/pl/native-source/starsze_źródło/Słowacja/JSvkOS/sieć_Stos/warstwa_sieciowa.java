// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Słowacja.JSvkOS.sieć_Stos;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP odbierać_WARTOŚĆ 분배를 한곳에서 관리한다. */
public final class warstwa_sieciowa {
    @FunctionalInterface
    public interface dane_procedura_obsługi {
        void Proces_WARTOŚĆ_wpis(byte[] dane, int Uruchom_2, int długość_WARTOŚĆ);
    }

    private final Map<Integer, dane_procedura_obsługi> Ethernet_procedura_obsługi = new HashMap<Integer, dane_procedura_obsługi>();
    private final Map<Integer, dane_procedura_obsługi> IP_procedura_obsługi = new HashMap<Integer, dane_procedura_obsługi>();
    private final Map<Integer, dane_procedura_obsługi> użytkownik_dane_lekcja_procedura_obsługi = new HashMap<Integer, dane_procedura_obsługi>();
    private final Map<Integer, dane_procedura_obsługi> 전송제어처리기 = new HashMap<Integer, dane_procedura_obsługi>();

    public void rejestr_Ethernet(int Rodzaj_WARTOŚĆ, dane_procedura_obsługi procedura_obsługi) {
        Ethernet_procedura_obsługi.put(Integer.valueOf(Rodzaj_WARTOŚĆ & 0xffff), procedura_obsługi);
    }

    public void rejestr_IP(int wartość_kontraktu, dane_procedura_obsługi procedura_obsługi) {
        IP_procedura_obsługi.put(Integer.valueOf(wartość_kontraktu & 0xff), procedura_obsługi);
    }

    public void rejestr_użytkownik_dane_lekcja(int sprzęt_port, dane_procedura_obsługi procedura_obsługi) {
        użytkownik_dane_lekcja_procedura_obsługi.put(Integer.valueOf(sprzęt_port & 0xffff), procedura_obsługi);
    }

    public void 전송제어등록(int sprzęt_port, dane_procedura_obsługi procedura_obsługi) {
        전송제어처리기.put(Integer.valueOf(sprzęt_port & 0xffff), procedura_obsługi);
    }

    public boolean odbierać_Ethernet(byte[] kadr_INDEKS) {
        if (!sieć_Narzędzia.systemy_informacyjne_Ethernet_kadr(kadr_INDEKS)) {
            return false;
        }
        int Rodzaj_WARTOŚĆ = sieć_Narzędzia.Ethernet_LITERY_WIELKIE_protokół(kadr_INDEKS);
        dane_procedura_obsługi 직접처리기 = Ethernet_procedura_obsługi.get(Integer.valueOf(Rodzaj_WARTOŚĆ));
        if (직접처리기 != null) {
            직접처리기.Proces_WARTOŚĆ_wpis(kadr_INDEKS, 14, kadr_INDEKS.length - 14);
            return true;
        }
        return Rodzaj_WARTOŚĆ == 0x0800 && odbierać_chmura_pakiet(kadr_INDEKS, 14);
    }

    private boolean odbierać_chmura_pakiet(byte[] dane, int Uruchom_2) {
        if (!sieć_Narzędzia.systemy_informacyjne_IPV_4_protokół(dane, Uruchom_2)) {
            return false;
        }
        int Nagłówek_długość = (dane[Uruchom_2] & 0x0f) * 4;
        int suma_długość = sieć_Narzędzia.큰순서짧은정수(dane, Uruchom_2 + 2);
        if (suma_długość < Nagłówek_długość || Uruchom_2 + suma_długość > dane.length) {
            return false;
        }
        int wartość_kontraktu = dane[Uruchom_2 + 9] & 0xff;
        int treść_START = Uruchom_2 + Nagłówek_długość;
        int treść_długość = suma_długość - Nagłówek_długość;
        dane_procedura_obsługi 직접처리기 = IP_procedura_obsługi.get(Integer.valueOf(wartość_kontraktu));
        if (직접처리기 != null) {
            직접처리기.Proces_WARTOŚĆ_wpis(dane, treść_START, treść_długość);
            return true;
        }
        if (treść_długość < 4) {
            return false;
        }
        int cel_numer_portu = sieć_Narzędzia.큰순서짧은정수(dane, treść_START + 2);
        Map<Integer, dane_procedura_obsługi> port_tabela = wartość_kontraktu == 17 ? użytkownik_dane_lekcja_procedura_obsługi : wartość_kontraktu == 6 ? 전송제어처리기 : null;
        if (port_tabela == null) {
            return false;
        }
        dane_procedura_obsługi port_procedura_obsługi = port_tabela.get(Integer.valueOf(cel_numer_portu));
        if (port_procedura_obsługi == null) {
            return false;
        }
        port_procedura_obsługi.Proces_WARTOŚĆ_wpis(dane, treść_START, treść_długość);
        return true;
    }
}

