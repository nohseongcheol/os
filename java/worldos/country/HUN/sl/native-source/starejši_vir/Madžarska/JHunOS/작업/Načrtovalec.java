// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Madžarska.JHunOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Madžarska.JHunOS.pomnilnik_območje.stran_Upravitelj;
import Madžarska.JHunOS.datotečni_sistem.파일서술자표;

/** Proces_VALUE 식별자와 라운드로빈 Pripravi 대기열을 관리한다. */
public final class Načrtovalec {
    private final stran_Upravitelj 쪽관리;
    private final Map<Integer, Proces_VALUE> Seznam_procesov = new HashMap<Integer, Proces_VALUE>();
    private final Queue<Proces_VALUE> 준비대기열 = new ArrayDeque<Proces_VALUE>();
    private int Naprej_identifikator = 1;

    public Načrtovalec(stran_Upravitelj 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proces_VALUE 첫과정(파일서술자표 파일서술자) {
        Proces_VALUE 새과정 = new Proces_VALUE(dodeliti_identifikator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Seznam_procesov.put(Integer.valueOf(새과정.identifikator_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proces_VALUE klon_VALUE(Proces_VALUE nadrejen_VALUE) {
        Proces_VALUE otrok_VALUE = new Proces_VALUE(
                dodeliti_identifikator(),
                nadrejen_VALUE.identifikator_VALUE(),
                쪽관리.쓰기시복사복제(nadrejen_VALUE.naslov_Space()),
                nadrejen_VALUE.파일서술자().klon_VALUE());
        otrok_VALUE.nabor_aplikacija_odmor(nadrejen_VALUE.aplikacija_odmor());
        Seznam_procesov.put(Integer.valueOf(otrok_VALUE.identifikator_VALUE()), otrok_VALUE);
        준비대기열.offer(otrok_VALUE);
        return otrok_VALUE;
    }

    public Proces_VALUE Naprej_Proces() {
        int preveriti_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < preveriti_COUNT; INDEX++) {
            Proces_VALUE Naprej_element = 준비대기열.poll();
            if (Naprej_element != null && (Naprej_element.stanje_VALUE() == Proces_stanje.Pripravi || Naprej_element.stanje_VALUE() == Proces_stanje.Izvedi_ukaz)) {
                Naprej_element.nabor_stanje(Proces_stanje.Izvedi_ukaz);
                준비대기열.offer(Naprej_element);
                return Naprej_element;
            }
        }
        return null;
    }

    public int 자식기다리기(Proces_VALUE nadrejen_VALUE, int otrok_identifikator, boolean 기다리지않음) {
        for (Proces_VALUE 후보 : Seznam_procesov.values()) {
            if (후보.nadrejen_identifikator() != nadrejen_VALUE.identifikator_VALUE()) {
                continue;
            }
            if (otrok_identifikator > 0 && 후보.identifikator_VALUE() != otrok_identifikator) {
                continue;
            }
            if (후보.stanje_VALUE() == Proces_stanje.Izhod_aplikacija) {
                int REZULTAT = (후보.izhodna_koda() & 0xff) << 8;
                Seznam_procesov.remove(Integer.valueOf(후보.identifikator_VALUE()));
                return REZULTAT;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proces_VALUE FIND_Proces(int identifikator_VALUE) {
        return Seznam_procesov.get(Integer.valueOf(identifikator_VALUE));
    }

    private int dodeliti_identifikator() {
        return Naprej_identifikator++;
    }
}
