// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Rumunia.JRouOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Rumunia.JRouOS.Pamięć_region.strona_Menedżer;
import Rumunia.JRouOS.system_plików.Plik_deskryptor_tabela;

/** Proces_WARTOŚĆ 식별자와 라운드로빈 Przygotuj 대기열을 관리한다. */
public final class Scheduler {
    private final strona_Menedżer 쪽관리;
    private final Map<Integer, Proces_WARTOŚĆ> Lista_procesów = new HashMap<Integer, Proces_WARTOŚĆ>();
    private final Queue<Proces_WARTOŚĆ> 준비대기열 = new ArrayDeque<Proces_WARTOŚĆ>();
    private int Dalej_identyfikator = 1;

    public Scheduler(strona_Menedżer 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proces_WARTOŚĆ 첫과정(Plik_deskryptor_tabela Plik_deskryptor) {
        Proces_WARTOŚĆ 새과정 = new Proces_WARTOŚĆ(przydzielić_identyfikator(), 0, 쪽관리.새주소공간(), Plik_deskryptor);
        Lista_procesów.put(Integer.valueOf(새과정.identyfikator_WARTOŚĆ()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proces_WARTOŚĆ klon_WARTOŚĆ(Proces_WARTOŚĆ nadrzędny_WARTOŚĆ) {
        Proces_WARTOŚĆ dziecko_WARTOŚĆ = new Proces_WARTOŚĆ(
                przydzielić_identyfikator(),
                nadrzędny_WARTOŚĆ.identyfikator_WARTOŚĆ(),
                쪽관리.쓰기시복사복제(nadrzędny_WARTOŚĆ.przestrzeń_adresowa()),
                nadrzędny_WARTOŚĆ.Plik_deskryptor().klon_WARTOŚĆ());
        dziecko_WARTOŚĆ.set_program_przerwa(nadrzędny_WARTOŚĆ.program_przerwa());
        Lista_procesów.put(Integer.valueOf(dziecko_WARTOŚĆ.identyfikator_WARTOŚĆ()), dziecko_WARTOŚĆ);
        준비대기열.offer(dziecko_WARTOŚĆ);
        return dziecko_WARTOŚĆ;
    }

    public Proces_WARTOŚĆ Dalej_Proces() {
        int czek_ILE_LICZB = 준비대기열.size();
        for (int INDEKS = 0; INDEKS < czek_ILE_LICZB; INDEKS++) {
            Proces_WARTOŚĆ Dalej_towar = 준비대기열.poll();
            if (Dalej_towar != null && (Dalej_towar.Stan_WARTOŚĆ() == Proces_Stan.Przygotuj || Dalej_towar.Stan_WARTOŚĆ() == Proces_Stan.Wykonaj_polecenie)) {
                Dalej_towar.set_Stan(Proces_Stan.Wykonaj_polecenie);
                준비대기열.offer(Dalej_towar);
                return Dalej_towar;
            }
        }
        return null;
    }

    public int 자식기다리기(Proces_WARTOŚĆ nadrzędny_WARTOŚĆ, int dziecko_identyfikator, boolean 기다리지않음) {
        for (Proces_WARTOŚĆ kandydat : Lista_procesów.values()) {
            if (kandydat.nadrzędny_identyfikator() != nadrzędny_WARTOŚĆ.identyfikator_WARTOŚĆ()) {
                continue;
            }
            if (dziecko_identyfikator > 0 && kandydat.identyfikator_WARTOŚĆ() != dziecko_identyfikator) {
                continue;
            }
            if (kandydat.Stan_WARTOŚĆ() == Proces_Stan.wyjść_program) {
                int WYNIK = (kandydat.kod_zakończenia() & 0xff) << 8;
                Lista_procesów.remove(Integer.valueOf(kandydat.identyfikator_WARTOŚĆ()));
                return WYNIK;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proces_WARTOŚĆ ZNAJDŹ_Proces(int identyfikator_WARTOŚĆ) {
        return Lista_procesów.get(Integer.valueOf(identyfikator_WARTOŚĆ));
    }

    private int przydzielić_identyfikator() {
        return Dalej_identyfikator++;
    }
}
