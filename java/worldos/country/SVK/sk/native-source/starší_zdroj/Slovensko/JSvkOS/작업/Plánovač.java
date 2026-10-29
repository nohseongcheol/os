// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Slovensko.JSvkOS.Pamäť_oblasť.쪽관리자;
import Slovensko.JSvkOS.systém_súborov.파일서술자표;

/** Proces_VALUE 식별자와 라운드로빈 Pripraviť 대기열을 관리한다. */
public final class Plánovač {
    private final 쪽관리자 쪽관리;
    private final Map<Integer, Proces_VALUE> Zoznam_procesu = new HashMap<Integer, Proces_VALUE>();
    private final Queue<Proces_VALUE> 준비대기열 = new ArrayDeque<Proces_VALUE>();
    private int Ďalej_identifikátor = 1;

    public Plánovač(쪽관리자 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proces_VALUE 첫과정(파일서술자표 파일서술자) {
        Proces_VALUE 새과정 = new Proces_VALUE(vyhradiť_identifikátor(), 0, 쪽관리.새주소공간(), 파일서술자);
        Zoznam_procesu.put(Integer.valueOf(새과정.identifikátor_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proces_VALUE klon_VALUE(Proces_VALUE nadradený_VALUE) {
        Proces_VALUE dieťa_VALUE = new Proces_VALUE(
                vyhradiť_identifikátor(),
                nadradený_VALUE.identifikátor_VALUE(),
                쪽관리.쓰기시복사복제(nadradený_VALUE.adresa_priestor()),
                nadradený_VALUE.파일서술자().klon_VALUE());
        dieťa_VALUE.množina_program_prerušiť(nadradený_VALUE.program_prerušiť());
        Zoznam_procesu.put(Integer.valueOf(dieťa_VALUE.identifikátor_VALUE()), dieťa_VALUE);
        준비대기열.offer(dieťa_VALUE);
        return dieťa_VALUE;
    }

    public Proces_VALUE Ďalej_Proces() {
        int skontrolovať_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < skontrolovať_COUNT; INDEX++) {
            Proces_VALUE Ďalej_položka = 준비대기열.poll();
            if (Ďalej_položka != null && (Ďalej_položka.Stav_VALUE() == Proces_Stav.Pripraviť || Ďalej_položka.Stav_VALUE() == Proces_Stav.Vykonať_príkaz)) {
                Ďalej_položka.množina_Stav(Proces_Stav.Vykonať_príkaz);
                준비대기열.offer(Ďalej_položka);
                return Ďalej_položka;
            }
        }
        return null;
    }

    public int 자식기다리기(Proces_VALUE nadradený_VALUE, int dieťa_identifikátor, boolean 기다리지않음) {
        for (Proces_VALUE 후보 : Zoznam_procesu.values()) {
            if (후보.nadradený_identifikátor() != nadradený_VALUE.identifikátor_VALUE()) {
                continue;
            }
            if (dieťa_identifikátor > 0 && 후보.identifikátor_VALUE() != dieťa_identifikátor) {
                continue;
            }
            if (후보.Stav_VALUE() == Proces_Stav.Skončiť_program) {
                int KR = (후보.kód_ukončenia() & 0xff) << 8;
                Zoznam_procesu.remove(Integer.valueOf(후보.identifikátor_VALUE()));
                return KR;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proces_VALUE FIND_Proces(int identifikátor_VALUE) {
        return Zoznam_procesu.get(Integer.valueOf(identifikátor_VALUE));
    }

    private int vyhradiť_identifikátor() {
        return Ďalej_identifikátor++;
    }
}
