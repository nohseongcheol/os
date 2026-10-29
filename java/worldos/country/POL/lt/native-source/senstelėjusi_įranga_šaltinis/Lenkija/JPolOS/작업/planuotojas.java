// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lenkija.JPolOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Lenkija.JPolOS.atmintis_sritis.쪽관리자;
import Lenkija.JPolOS.failų_sistema.파일서술자표;

/** Procesas_VALUE 식별자와 라운드로빈 Parengti 대기열을 관리한다. */
public final class planuotojas {
    private final 쪽관리자 쪽관리;
    private final Map<Integer, Procesas_VALUE> Procesų_sąrašas = new HashMap<Integer, Procesas_VALUE>();
    private final Queue<Procesas_VALUE> 준비대기열 = new ArrayDeque<Procesas_VALUE>();
    private int toliau_identifikatorius = 1;

    public planuotojas(쪽관리자 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Procesas_VALUE 첫과정(파일서술자표 파일서술자) {
        Procesas_VALUE 새과정 = new Procesas_VALUE(priskirti_identifikatorius(), 0, 쪽관리.새주소공간(), 파일서술자);
        Procesų_sąrašas.put(Integer.valueOf(새과정.identifikatorius_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Procesas_VALUE klonas_VALUE(Procesas_VALUE pirminis_VALUE) {
        Procesas_VALUE vaikas_VALUE = new Procesas_VALUE(
                priskirti_identifikatorius(),
                pirminis_VALUE.identifikatorius_VALUE(),
                쪽관리.쓰기시복사복제(pirminis_VALUE.ADDRESS_erdvė()),
                pirminis_VALUE.파일서술자().klonas_VALUE());
        vaikas_VALUE.rinkinys_programa_nutraukti(pirminis_VALUE.programa_nutraukti());
        Procesų_sąrašas.put(Integer.valueOf(vaikas_VALUE.identifikatorius_VALUE()), vaikas_VALUE);
        준비대기열.offer(vaikas_VALUE);
        return vaikas_VALUE;
    }

    public Procesas_VALUE toliau_Procesas() {
        int čekis_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < čekis_COUNT; INDEX++) {
            Procesas_VALUE toliau_prekė = 준비대기열.poll();
            if (toliau_prekė != null && (toliau_prekė.Būsena_VALUE() == Procesas_Būsena.Parengti || toliau_prekė.Būsena_VALUE() == Procesas_Būsena.Vykdyti_komanda)) {
                toliau_prekė.rinkinys_Būsena(Procesas_Būsena.Vykdyti_komanda);
                준비대기열.offer(toliau_prekė);
                return toliau_prekė;
            }
        }
        return null;
    }

    public int 자식기다리기(Procesas_VALUE pirminis_VALUE, int vaikas_identifikatorius, boolean 기다리지않음) {
        for (Procesas_VALUE 후보 : Procesų_sąrašas.values()) {
            if (후보.pirminis_identifikatorius() != pirminis_VALUE.identifikatorius_VALUE()) {
                continue;
            }
            if (vaikas_identifikatorius > 0 && 후보.identifikatorius_VALUE() != vaikas_identifikatorius) {
                continue;
            }
            if (후보.Būsena_VALUE() == Procesas_Būsena.Baigti_programa_086bb533) {
                int REZULTATAS = (후보.Baigti_CODE() & 0xff) << 8;
                Procesų_sąrašas.remove(Integer.valueOf(후보.identifikatorius_VALUE()));
                return REZULTATAS;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Procesas_VALUE FIND_Procesas(int identifikatorius_VALUE) {
        return Procesų_sąrašas.get(Integer.valueOf(identifikatorius_VALUE));
    }

    private int priskirti_identifikatorius() {
        return toliau_identifikatorius++;
    }
}
