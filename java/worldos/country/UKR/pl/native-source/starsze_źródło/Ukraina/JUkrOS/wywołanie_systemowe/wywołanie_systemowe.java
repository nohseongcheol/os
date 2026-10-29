// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukraina.JUkrOS.wywołanie_systemowe;

import Ukraina.JUkrOS.Pamięć_region.strona_Menedżer;
import Ukraina.JUkrOS.작업.Proces_WARTOŚĆ;
import Ukraina.JUkrOS.작업.Scheduler;
import Ukraina.JUkrOS.system_plików.wykonywalny_moduł_ładujący;
import Ukraina.JUkrOS.system_plików.system_plików;
import Ukraina.JUkrOS.system_plików.Plik_informacje;
import Ukraina.JUkrOS.jądro.sprzęt_WARTOŚĆ;
import Ukraina.JUkrOS.wejście_WARTOŚĆ.wejście_Menedżer;
import Ukraina.JUkrOS.wejście_WARTOŚĆ.wejście_konkurs;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class wywołanie_systemowe {
    public static final int tylko_do_odczytu_flaga = 0;
    public static final int Search_START = 0;
    public static final int Search_bieżący = 1;
    public static final int ZNAJDŹ_wpis_Koniec = 2;

    private final system_plików system_plików;
    private final strona_Menedżer 쪽관리;
    private final Scheduler Scheduler;
    private final wykonywalny_moduł_ładujący moduł_ładujący = new wykonywalny_moduł_ładujący();
    private final sprzęt_WARTOŚĆ urządzenie_WARTOŚĆ;
    private final wejście_Menedżer 입력관리;

    public wywołanie_systemowe(system_plików system_plików, strona_Menedżer 쪽관리, Scheduler Scheduler, sprzęt_WARTOŚĆ urządzenie_WARTOŚĆ, wejście_Menedżer 입력관리) {
        this.system_plików = system_plików;
        this.쪽관리 = 쪽관리;
        this.Scheduler = Scheduler;
        this.urządzenie_WARTOŚĆ = urządzenie_WARTOŚĆ;
        this.입력관리 = 입력관리;
    }

    public int Proces_identyfikator(Proces_WARTOŚĆ bieżący_Proces) {
        return bieżący_Proces.identyfikator_WARTOŚĆ();
    }

    public int nadrzędny_Proces_identyfikator(Proces_WARTOŚĆ bieżący_Proces) {
        return bieżący_Proces.nadrzędny_identyfikator();
    }

    public int Otwórz(Proces_WARTOŚĆ bieżący_Proces, String Nazwa, int flaga_WARTOŚĆ) {
        if (flaga_WARTOŚĆ != tylko_do_odczytu_flaga) {
            return -30;
        }
        return bieżący_Proces.Plik_deskryptor().Otwórz(Nazwa);
    }

    public int Odczyt(Proces_WARTOŚĆ bieżący_Proces, int deskryptor_wpis, byte[] odbierać_cel, int Rozmiar) {
        if (deskryptor_wpis == 0) {
            if (Rozmiar <= 0 || odbierać_cel.length == 0) {
                return 0;
            }
            wejście_konkurs Wydarzenie = 입력관리.Dalej_konkurs();
            if (Wydarzenie == null || Wydarzenie.rodzaj_zdarzenia() != wejście_konkurs.Rodzaj_WARTOŚĆ.Klucz_niedziałający) {
                return -11;
            }
            odbierać_cel[0] = (byte) Wydarzenie.첫째값();
            return 1;
        }
        return bieżący_Proces.Plik_deskryptor().Odczyt(deskryptor_wpis, odbierać_cel, Rozmiar);
    }

    public int Zapis(Proces_WARTOŚĆ bieżący_Proces, int deskryptor_wpis, byte[] dane, int Rozmiar) {
        if (deskryptor_wpis != 1 && deskryptor_wpis != 2) {
            return bieżący_Proces.Plik_deskryptor().systemy_informacyjne_otwarty(deskryptor_wpis) ? -30 : -9;
        }
        if (Rozmiar < 0 || Rozmiar > dane.length) {
            return -22;
        }
        urządzenie_WARTOŚĆ.직렬출력(new String(dane, 0, Rozmiar, java.nio.charset.StandardCharsets.UTF_8));
        return Rozmiar;
    }

    public int Zamknięte(Proces_WARTOŚĆ bieżący_Proces, int deskryptor_wpis) {
        return bieżący_Proces.Plik_deskryptor().Zamknięte(deskryptor_wpis);
    }

    public int przenosić_stanowisko(Proces_WARTOŚĆ bieżący_Proces, int deskryptor_wpis, int 거리, int Project_korzeń) {
        return bieżący_Proces.Plik_deskryptor().przenosić_stanowisko(deskryptor_wpis, 거리, Project_korzeń);
    }

    public int Duplikuj_deskryptor(Proces_WARTOŚĆ bieżący_Proces, int deskryptor_wpis) {
        return bieżący_Proces.Plik_deskryptor().복제서술자(deskryptor_wpis, 0);
    }

    public int 지정서술자복제(Proces_WARTOŚĆ bieżący_Proces, int deskryptor_wpis, int 새서술자) {
        return bieżący_Proces.Plik_deskryptor().지정복제(deskryptor_wpis, 새서술자);
    }

    public int 접근가능(String Nazwa, int metoda_tryb) {
        Plik_informacje msinfo32_exe = system_plików.msinfo32_exe(Nazwa);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metoda_tryb & 1) != 0 && (msinfo32_exe.kształt_Rodzaj() & 0111) == 0) {
            return -13;
        }
        if ((metoda_tryb & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int zmiana_Lista_zadań(String Nazwa) {
        return "/".equals(Nazwa) ? 0 : -20;
    }

    public String bieżący_Lista_zadań(int odbierać_zmienić_rozmiar) {
        return odbierać_zmienić_rozmiar >= 2 ? "/" : null;
    }

    public int identyfikator_użytkownika() { return 0; }
    public int efektywny_identyfikator_użytkownika() { return 0; }
    public int grupa_identyfikator() { return 0; }
    public int efektywny_grupa_identyfikator() { return 0; }

    public int synchronizować_Plik(Proces_WARTOŚĆ bieżący_Proces, int deskryptor_wpis) {
        return bieżący_Proces.Plik_deskryptor().msinfo32_exe(deskryptor_wpis) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // bieżący_towar 파일체계는 Odczyt 전용이어서 밀어낼 자료가 없다.
    }

    public boolean systemy_informacyjne_Terminal(Proces_WARTOŚĆ bieżący_Proces, int deskryptor_wpis) {
        Plik_informacje msinfo32_exe = bieżący_Proces.Plik_deskryptor().msinfo32_exe(deskryptor_wpis);
        return msinfo32_exe != null && (msinfo32_exe.kształt_Rodzaj() & 0170000) == 0020000;
    }

    public int sterowanie_plikiem(Proces_WARTOŚĆ bieżący_Proces, int deskryptor_wpis, int polecenie, int parametr_argument) {
        if (polecenie == 0) {
            return bieżący_Proces.Plik_deskryptor().복제서술자(deskryptor_wpis, parametr_argument);
        }
        if (polecenie == 1) {
            return bieżący_Proces.Plik_deskryptor().실행시닫기값(deskryptor_wpis);
        }
        if (polecenie == 2) {
            return bieżący_Proces.Plik_deskryptor().실행시닫기설정(deskryptor_wpis, (parametr_argument & 1) != 0);
        }
        if (polecenie == 3) {
            return bieżący_Proces.Plik_deskryptor().msinfo32_exe(deskryptor_wpis) == null ? -9 : tylko_do_odczytu_flaga;
        }
        if (polecenie == 4) {
            return parametr_argument == tylko_do_odczytu_flaga ? 0 : -30;
        }
        return -22;
    }

    public int Twórca_wpis(String Nazwa, int pozwolenie_WARTOŚĆ) {
        return -30;
    }

    public Plik_informacje deskryptor_informacje(Proces_WARTOŚĆ bieżący_Proces, int deskryptor_wpis) {
        return bieżący_Proces.Plik_deskryptor().msinfo32_exe(deskryptor_wpis);
    }

    public System_Szczegóły System_Szczegóły() {
        return new System_Szczegóły("JUkrOS", "JUkrOS", "0.1", "Java managed kernel", "i386");
    }

    public Plik_informacje Plik_informacje(String Nazwa) {
        return system_plików.msinfo32_exe(Nazwa);
    }

    public Proces_WARTOŚĆ klon_Proces(Proces_WARTOŚĆ nadrzędny_WARTOŚĆ) {
        return Scheduler.klon_WARTOŚĆ(nadrzędny_WARTOŚĆ);
    }

    public int 자식기다리기(Proces_WARTOŚĆ nadrzędny_WARTOŚĆ, int dziecko_identyfikator, boolean 기다리지않음) {
        return Scheduler.자식기다리기(nadrzędny_WARTOŚĆ, dziecko_identyfikator, 기다리지않음);
    }

    public int program_przerwa(Proces_WARTOŚĆ bieżący_Proces, int 새끝) {
        int Wstecz_Koniec = bieżący_Proces.program_przerwa();
        if (새끝 == 0) {
            return Wstecz_Koniec;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Wstecz_Koniec / strona_Menedżer.rozmiar_strony;
        int 끝쪽 = (새끝 + strona_Menedżer.rozmiar_strony - 1) / strona_Menedżer.rozmiar_strony;
        if (새끝 > Wstecz_Koniec) {
            for (int INDEKS = 첫쪽; INDEKS < 끝쪽; INDEKS++) {
                int Adres = INDEKS * strona_Menedżer.rozmiar_strony;
                try {
                    쪽관리.바이트읽기(bieżący_Proces.przestrzeń_adresowa(), Adres);
                } catch (IllegalStateException błąd) {
                    쪽관리.MAP_strona(bieżący_Proces.przestrzeń_adresowa(), Adres, true);
                }
            }
        }
        bieżący_Proces.set_program_przerwa(새끝);
        return 새끝;
    }

    public int zwiększenie_stanu_program_przerwa(Proces_WARTOŚĆ bieżący_Proces, int przyrost_ilość) {
        int Wstecz_Koniec = bieżący_Proces.program_przerwa();
        int WYNIK = program_przerwa(bieżący_Proces, Wstecz_Koniec + przyrost_ilość);
        return WYNIK < 0 ? WYNIK : Wstecz_Koniec;
    }

    public int Wykonaj_polecenie(Proces_WARTOŚĆ bieżący_Proces, byte[] plik_wykonywalny) {
        return Wykonaj_polecenie(bieżący_Proces, plik_wykonywalny, new String[0], new String[0]);
    }

    public int Wykonaj_polecenie(Proces_WARTOŚĆ bieżący_Proces, byte[] plik_wykonywalny, String[] parametr_argument, String[] środowisko) {
        wykonywalny_moduł_ładujący.OBRAZ OBRAZ_WARTOŚĆ;
        try {
            OBRAZ_WARTOŚĆ = moduł_ładujący.검사(plik_wykonywalny);
        } catch (IllegalArgumentException błąd) {
            return -8;
        }
        if (parametr_argument == null || środowisko == null || parametr_argument.length > 16 || środowisko.length > 16) {
            return -7;
        }
        for (wykonywalny_moduł_ładujący.obszar_WARTOŚĆ_366e0bfa obszar_WARTOŚĆ_366e0bfa : OBRAZ_WARTOŚĆ.구역들()) {
            if ((obszar_WARTOŚĆ_366e0bfa.flaga_WARTOŚĆ() & 2) == 0 || obszar_WARTOŚĆ_366e0bfa.Rozmiar() == 0) {
                continue;
            }
            int 첫쪽 = obszar_WARTOŚĆ_366e0bfa.Adres() / strona_Menedżer.rozmiar_strony;
            int 끝쪽 = (obszar_WARTOŚĆ_366e0bfa.Adres() + obszar_WARTOŚĆ_366e0bfa.Rozmiar() + strona_Menedżer.rozmiar_strony - 1) / strona_Menedżer.rozmiar_strony;
            for (int INDEKS = 첫쪽; INDEKS < 끝쪽; INDEKS++) {
                int Adres = INDEKS * strona_Menedżer.rozmiar_strony;
                try {
                    쪽관리.바이트읽기(bieżący_Proces.przestrzeń_adresowa(), Adres);
                    쪽관리.Prywatne_zakres_zapis(bieżący_Proces.przestrzeń_adresowa(), Adres, strona_Menedżer.rozmiar_strony);
                } catch (IllegalStateException błąd) {
                    쪽관리.MAP_strona(bieżący_Proces.przestrzeń_adresowa(), Adres, true);
                }
            }
            for (int INDEKS = 0; INDEKS < obszar_WARTOŚĆ_366e0bfa.Rozmiar(); INDEKS++) {
                byte WARTOŚĆ = obszar_WARTOŚĆ_366e0bfa.Rodzaj_WARTOŚĆ() == 8 ? 0 : plik_wykonywalny[obszar_WARTOŚĆ_366e0bfa.Plik_stanowisko() + INDEKS];
                쪽관리.zapis_bajt_WARTOŚĆ(bieżący_Proces.przestrzeń_adresowa(), obszar_WARTOŚĆ_366e0bfa.Adres() + INDEKS, WARTOŚĆ);
            }
        }
        bieżący_Proces.set_kontekst(OBRAZ_WARTOŚĆ.START_ADRES(), parametr_argument, środowisko);
        bieżący_Proces.Plik_deskryptor().실행시닫기();
        return 0;
    }

    public void zakończ_program(Proces_WARTOŚĆ bieżący_Proces, int Stan_WARTOŚĆ) {
        bieżący_Proces.wyjść_program(Stan_WARTOŚĆ);
    }
}
