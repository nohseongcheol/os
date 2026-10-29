// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turska.JTurOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Turska.JTurOS.Memorija_oblast.stranica_menadžer;
import Turska.JTurOS.sistem_datoteka.파일서술자표;

/** Proces_VALUE 식별자와 라운드로빈 Pripremi 대기열을 관리한다. */
public final class Planer {
    private final stranica_menadžer 쪽관리;
    private final Map<Integer, Proces_VALUE> Lista_procesa = new HashMap<Integer, Proces_VALUE>();
    private final Queue<Proces_VALUE> 준비대기열 = new ArrayDeque<Proces_VALUE>();
    private int Dalje_identifikator = 1;

    public Planer(stranica_menadžer 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proces_VALUE 첫과정(파일서술자표 파일서술자) {
        Proces_VALUE 새과정 = new Proces_VALUE(dodeliti_identifikator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Lista_procesa.put(Integer.valueOf(새과정.identifikator_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proces_VALUE klon_VALUE(Proces_VALUE nadređen_VALUE) {
        Proces_VALUE dete_VALUE = new Proces_VALUE(
                dodeliti_identifikator(),
                nadređen_VALUE.identifikator_VALUE(),
                쪽관리.쓰기시복사복제(nadređen_VALUE.adresa_prostor()),
                nadređen_VALUE.파일서술자().klon_VALUE());
        dete_VALUE.skup_program_pauza(nadređen_VALUE.program_pauza());
        Lista_procesa.put(Integer.valueOf(dete_VALUE.identifikator_VALUE()), dete_VALUE);
        준비대기열.offer(dete_VALUE);
        return dete_VALUE;
    }

    public Proces_VALUE Dalje_Proces() {
        int proveriti_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < proveriti_COUNT; INDEX++) {
            Proces_VALUE Dalje_stavka = 준비대기열.poll();
            if (Dalje_stavka != null && (Dalje_stavka.Status_VALUE() == Proces_Status.Pripremi || Dalje_stavka.Status_VALUE() == Proces_Status.Izvrši_komanda)) {
                Dalje_stavka.skup_Status(Proces_Status.Izvrši_komanda);
                준비대기열.offer(Dalje_stavka);
                return Dalje_stavka;
            }
        }
        return null;
    }

    public int 자식기다리기(Proces_VALUE nadređen_VALUE, int dete_identifikator, boolean 기다리지않음) {
        for (Proces_VALUE 후보 : Lista_procesa.values()) {
            if (후보.nadređen_identifikator() != nadređen_VALUE.identifikator_VALUE()) {
                continue;
            }
            if (dete_identifikator > 0 && 후보.identifikator_VALUE() != dete_identifikator) {
                continue;
            }
            if (후보.Status_VALUE() == Proces_Status.Izađi_program) {
                int KR = (후보.Izađi_kôd() & 0xff) << 8;
                Lista_procesa.remove(Integer.valueOf(후보.identifikator_VALUE()));
                return KR;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proces_VALUE FIND_Proces(int identifikator_VALUE) {
        return Lista_procesa.get(Integer.valueOf(identifikator_VALUE));
    }

    private int dodeliti_identifikator() {
        return Dalje_identifikator++;
    }
}
