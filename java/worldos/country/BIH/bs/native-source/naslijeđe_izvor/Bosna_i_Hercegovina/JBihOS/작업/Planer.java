// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Bosna_i_Hercegovina.JBihOS.기억공간.stranica_menadžer;
import Bosna_i_Hercegovina.JBihOS.fajl_sistem.파일서술자표;

/** proces_VALUE 식별자와 라운드로빈 Pripremiti 대기열을 관리한다. */
public final class Planer {
    private final stranica_menadžer 쪽관리;
    private final Map<Integer, proces_VALUE> Spisak_postupka = new HashMap<Integer, proces_VALUE>();
    private final Queue<proces_VALUE> 준비대기열 = new ArrayDeque<proces_VALUE>();
    private int Dalje_identifikator = 1;

    public Planer(stranica_menadžer 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public proces_VALUE 첫과정(파일서술자표 파일서술자) {
        proces_VALUE 새과정 = new proces_VALUE(dodijeliti_identifikator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Spisak_postupka.put(Integer.valueOf(새과정.identifikator_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public proces_VALUE 복제(proces_VALUE roditelj_VALUE) {
        proces_VALUE dijete_VALUE = new proces_VALUE(
                dodijeliti_identifikator(),
                roditelj_VALUE.identifikator_VALUE(),
                쪽관리.쓰기시복사복제(roditelj_VALUE.adresa_prostor()),
                roditelj_VALUE.파일서술자().복제());
        dijete_VALUE.프로그램끝설정(roditelj_VALUE.프로그램끝());
        Spisak_postupka.put(Integer.valueOf(dijete_VALUE.identifikator_VALUE()), dijete_VALUE);
        준비대기열.offer(dijete_VALUE);
        return dijete_VALUE;
    }

    public proces_VALUE Dalje_proces() {
        int ček_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < ček_COUNT; INDEX++) {
            proces_VALUE Dalje_stavka = 준비대기열.poll();
            if (Dalje_stavka != null && (Dalje_stavka.stanje_VALUE() == proces_stanje.Pripremiti || Dalje_stavka.stanje_VALUE() == proces_stanje.Izvrši_komanda)) {
                Dalje_stavka.skup_stanje(proces_stanje.Izvrši_komanda);
                준비대기열.offer(Dalje_stavka);
                return Dalje_stavka;
            }
        }
        return null;
    }

    public int 자식기다리기(proces_VALUE roditelj_VALUE, int dijete_identifikator, boolean 기다리지않음) {
        for (proces_VALUE 후보 : Spisak_postupka.values()) {
            if (후보.roditelj_identifikator() != roditelj_VALUE.identifikator_VALUE()) {
                continue;
            }
            if (dijete_identifikator > 0 && 후보.identifikator_VALUE() != dijete_identifikator) {
                continue;
            }
            if (후보.stanje_VALUE() == proces_stanje.izaći_program) {
                int mjera = (후보.izaći_kod() & 0xff) << 8;
                Spisak_postupka.remove(Integer.valueOf(후보.identifikator_VALUE()));
                return mjera;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public proces_VALUE FIND_proces(int identifikator_VALUE) {
        return Spisak_postupka.get(Integer.valueOf(identifikator_VALUE));
    }

    private int dodijeliti_identifikator() {
        return Dalje_identifikator++;
    }
}
