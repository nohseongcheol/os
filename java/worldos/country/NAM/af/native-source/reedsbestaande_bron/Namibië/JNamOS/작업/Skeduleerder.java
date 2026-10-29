// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Namibië.JNamOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Namibië.JNamOS.기억공간.bladsy_bestuurder;
import Namibië.JNamOS.lêerstelsel.파일서술자표;

/** Proses_VALUE 식별자와 라운드로빈 Maak_gereed 대기열을 관리한다. */
public final class Skeduleerder {
    private final bladsy_bestuurder 쪽관리;
    private final Map<Integer, Proses_VALUE> Proseslys = new HashMap<Integer, Proses_VALUE>();
    private final Queue<Proses_VALUE> 준비대기열 = new ArrayDeque<Proses_VALUE>();
    private int Volgende_waarde = 1;

    public Skeduleerder(bladsy_bestuurder 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proses_VALUE 첫과정(파일서술자표 파일서술자) {
        Proses_VALUE 새과정 = new Proses_VALUE(toewys_waarde(), 0, 쪽관리.새주소공간(), 파일서술자);
        Proseslys.put(Integer.valueOf(새과정.waarde_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proses_VALUE 복제(Proses_VALUE 부모) {
        Proses_VALUE kind_VALUE = new Proses_VALUE(
                toewys_waarde(),
                부모.waarde_VALUE(),
                쪽관리.쓰기시복사복제(부모.adres_ruimte()),
                부모.파일서술자().복제());
        kind_VALUE.프로그램끝설정(부모.프로그램끝());
        Proseslys.put(Integer.valueOf(kind_VALUE.waarde_VALUE()), kind_VALUE);
        준비대기열.offer(kind_VALUE);
        return kind_VALUE;
    }

    public Proses_VALUE Volgende_Proses() {
        int tjek_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < tjek_COUNT; INDEX++) {
            Proses_VALUE Volgende_item = 준비대기열.poll();
            if (Volgende_item != null && (Volgende_item.stand_VALUE() == Proses_stand.Maak_gereed || Volgende_item.stand_VALUE() == Proses_stand.uitvoer_bevel)) {
                Volgende_item.stel_stand(Proses_stand.uitvoer_bevel);
                준비대기열.offer(Volgende_item);
                return Volgende_item;
            }
        }
        return null;
    }

    public int 자식기다리기(Proses_VALUE 부모, int kind_waarde, boolean 기다리지않음) {
        for (Proses_VALUE 후보 : Proseslys.values()) {
            if (후보.부모식별자() != 부모.waarde_VALUE()) {
                continue;
            }
            if (kind_waarde > 0 && 후보.waarde_VALUE() != kind_waarde) {
                continue;
            }
            if (후보.stand_VALUE() == Proses_stand.Verlaat_program) {
                int maatreël = (후보.Verlaat_CODE() & 0xff) << 8;
                Proseslys.remove(Integer.valueOf(후보.waarde_VALUE()));
                return maatreël;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proses_VALUE FIND_Proses(int waarde_VALUE) {
        return Proseslys.get(Integer.valueOf(waarde_VALUE));
    }

    private int toewys_waarde() {
        return Volgende_waarde++;
    }
}
