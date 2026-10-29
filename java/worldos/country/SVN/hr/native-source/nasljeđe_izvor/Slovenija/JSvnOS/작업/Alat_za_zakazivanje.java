// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Slovenija.JSvnOS.Memorija_regije.dojaviti_Upravitelj;
import Slovenija.JSvnOS.datotečni_sustav.파일서술자표;

/** Proces_VALUE 식별자와 라운드로빈 Pripremi 대기열을 관리한다. */
public final class Alat_za_zakazivanje {
    private final dojaviti_Upravitelj 쪽관리;
    private final Map<Integer, Proces_VALUE> Popis_postupka = new HashMap<Integer, Proces_VALUE>();
    private final Queue<Proces_VALUE> 준비대기열 = new ArrayDeque<Proces_VALUE>();
    private int Dalje_identifikator = 1;

    public Alat_za_zakazivanje(dojaviti_Upravitelj 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proces_VALUE 첫과정(파일서술자표 파일서술자) {
        Proces_VALUE 새과정 = new Proces_VALUE(dodijeli_identifikator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Popis_postupka.put(Integer.valueOf(새과정.identifikator_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proces_VALUE klon_VALUE(Proces_VALUE roditeljski_VALUE) {
        Proces_VALUE dijete_VALUE = new Proces_VALUE(
                dodijeli_identifikator(),
                roditeljski_VALUE.identifikator_VALUE(),
                쪽관리.쓰기시복사복제(roditeljski_VALUE.adresa_Space()),
                roditeljski_VALUE.파일서술자().klon_VALUE());
        dijete_VALUE.skup_program_pauza(roditeljski_VALUE.program_pauza());
        Popis_postupka.put(Integer.valueOf(dijete_VALUE.identifikator_VALUE()), dijete_VALUE);
        준비대기열.offer(dijete_VALUE);
        return dijete_VALUE;
    }

    public Proces_VALUE Dalje_Proces() {
        int 검사수 = 준비대기열.size();
        for (int INDEX = 0; INDEX < 검사수; INDEX++) {
            Proces_VALUE Dalje_artikl = 준비대기열.poll();
            if (Dalje_artikl != null && (Dalje_artikl.Stanje_VALUE() == Proces_Stanje.Pripremi || Dalje_artikl.Stanje_VALUE() == Proces_Stanje.Izvrši_naredba)) {
                Dalje_artikl.skup_Stanje(Proces_Stanje.Izvrši_naredba);
                준비대기열.offer(Dalje_artikl);
                return Dalje_artikl;
            }
        }
        return null;
    }

    public int 자식기다리기(Proces_VALUE roditeljski_VALUE, int dijete_identifikator, boolean 기다리지않음) {
        for (Proces_VALUE 후보 : Popis_postupka.values()) {
            if (후보.roditeljski_identifikator() != roditeljski_VALUE.identifikator_VALUE()) {
                continue;
            }
            if (dijete_identifikator > 0 && 후보.identifikator_VALUE() != dijete_identifikator) {
                continue;
            }
            if (후보.Stanje_VALUE() == Proces_Stanje.Izlaz_program) {
                int REZULTAT = (후보.Izlaz_kod() & 0xff) << 8;
                Popis_postupka.remove(Integer.valueOf(후보.identifikator_VALUE()));
                return REZULTAT;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proces_VALUE FIND_Proces(int identifikator_VALUE) {
        return Popis_postupka.get(Integer.valueOf(identifikator_VALUE));
    }

    private int dodijeli_identifikator() {
        return Dalje_identifikator++;
    }
}
