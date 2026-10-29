// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Северна_Македонија.JMkdOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Северна_Македонија.JMkdOS.기억공간.страница_управник;
import Северна_Македонија.JMkdOS.систем_на_датотеки.파일서술자표;

/** Процес_VALUE 식별자와 라운드로빈 Подготви 대기열을 관리한다. */
public final class Распоредувач {
    private final страница_управник 쪽관리;
    private final Map<Integer, Процес_VALUE> Список_со_процеси = new HashMap<Integer, Процес_VALUE>();
    private final Queue<Процес_VALUE> 준비대기열 = new ArrayDeque<Процес_VALUE>();
    private int Следно_идентификатор = 1;

    public Распоредувач(страница_управник 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Процес_VALUE 첫과정(파일서술자표 파일서술자) {
        Процес_VALUE 새과정 = new Процес_VALUE(додели_идентификатор(), 0, 쪽관리.새주소공간(), 파일서술자);
        Список_со_процеси.put(Integer.valueOf(새과정.идентификатор_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Процес_VALUE 복제(Процес_VALUE 부모) {
        Процес_VALUE дете_VALUE = new Процес_VALUE(
                додели_идентификатор(),
                부모.идентификатор_VALUE(),
                쪽관리.쓰기시복사복제(부모.адреса_простор()),
                부모.파일서술자().복제());
        дете_VALUE.프로그램끝설정(부모.프로그램끝());
        Список_со_процеси.put(Integer.valueOf(дете_VALUE.идентификатор_VALUE()), дете_VALUE);
        준비대기열.offer(дете_VALUE);
        return дете_VALUE;
    }

    public Процес_VALUE Следно_Процес() {
        int провери_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < провери_COUNT; INDEX++) {
            Процес_VALUE Следно_ставка = 준비대기열.poll();
            if (Следно_ставка != null && (Следно_ставка.статус_VALUE() == Процес_статус.Подготви || Следно_ставка.статус_VALUE() == Процес_статус.Изврши_наредба)) {
                Следно_ставка.збир_статус(Процес_статус.Изврши_наредба);
                준비대기열.offer(Следно_ставка);
                return Следно_ставка;
            }
        }
        return null;
    }

    public int 자식기다리기(Процес_VALUE 부모, int дете_идентификатор, boolean 기다리지않음) {
        for (Процес_VALUE 후보 : Список_со_процеси.values()) {
            if (후보.부모식별자() != 부모.идентификатор_VALUE()) {
                continue;
            }
            if (дете_идентификатор > 0 && 후보.идентификатор_VALUE() != дете_идентификатор) {
                continue;
            }
            if (후보.статус_VALUE() == Процес_статус.Излез_програма) {
                int мерка = (후보.Излез_CODE() & 0xff) << 8;
                Список_со_процеси.remove(Integer.valueOf(후보.идентификатор_VALUE()));
                return мерка;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Процес_VALUE FIND_Процес(int идентификатор_VALUE) {
        return Список_со_процеси.get(Integer.valueOf(идентификатор_VALUE));
    }

    private int додели_идентификатор() {
        return Следно_идентификатор++;
    }
}
