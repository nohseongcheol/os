// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Россия.JRusOS.기억공간.бит_идарәче;
import Россия.JRusOS.файл_системасы.파일서술자표;

/** Процесс_VALUE 식별자와 라운드로빈 Әзерләү 대기열을 관리한다. */
public final class Планлаштыручы {
    private final бит_идарәче 쪽관리;
    private final Map<Integer, Процесс_VALUE> Процесс_исемлеге = new HashMap<Integer, Процесс_VALUE>();
    private final Queue<Процесс_VALUE> 준비대기열 = new ArrayDeque<Процесс_VALUE>();
    private int Киләсе_күрсәткеч = 1;

    public Планлаштыручы(бит_идарәче 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Процесс_VALUE 첫과정(파일서술자표 파일서술자) {
        Процесс_VALUE 새과정 = new Процесс_VALUE(атап_бирү_күрсәткеч(), 0, 쪽관리.새주소공간(), 파일서술자);
        Процесс_исемлеге.put(Integer.valueOf(새과정.күрсәткеч_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Процесс_VALUE 복제(Процесс_VALUE 부모) {
        Процесс_VALUE бала_VALUE = new Процесс_VALUE(
                атап_бирү_күрсәткеч(),
                부모.күрсәткеч_VALUE(),
                쪽관리.쓰기시복사복제(부모.адрес_өлкә()),
                부모.파일서술자().복제());
        бала_VALUE.프로그램끝설정(부모.프로그램끝());
        Процесс_исемлеге.put(Integer.valueOf(бала_VALUE.күрсәткеч_VALUE()), бала_VALUE);
        준비대기열.offer(бала_VALUE);
        return бала_VALUE;
    }

    public Процесс_VALUE Киләсе_Процесс() {
        int чек_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < чек_COUNT; INDEX++) {
            Процесс_VALUE Киләсе_элемент = 준비대기열.poll();
            if (Киләсе_элемент != null && (Киләсе_элемент.халәт_VALUE() == Процесс_халәт.Әзерләү || Киләсе_элемент.халәт_VALUE() == Процесс_халәт.үтәргә_команда)) {
                Киләсе_элемент.җыелма_халәт(Процесс_халәт.үтәргә_команда);
                준비대기열.offer(Киләсе_элемент);
                return Киләсе_элемент;
            }
        }
        return null;
    }

    public int 자식기다리기(Процесс_VALUE 부모, int бала_күрсәткеч, boolean 기다리지않음) {
        for (Процесс_VALUE 후보 : Процесс_исемлеге.values()) {
            if (후보.부모식별자() != 부모.күрсәткеч_VALUE()) {
                continue;
            }
            if (бала_күрсәткеч > 0 && 후보.күрсәткеч_VALUE() != бала_күрсәткеч) {
                continue;
            }
            if (후보.халәт_VALUE() == Процесс_халәт.Чыгу_кушымта) {
                int үлчәм = (후보.Чыгу_CODE() & 0xff) << 8;
                Процесс_исемлеге.remove(Integer.valueOf(후보.күрсәткеч_VALUE()));
                return үлчәм;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Процесс_VALUE FIND_Процесс(int күрсәткеч_VALUE) {
        return Процесс_исемлеге.get(Integer.valueOf(күрсәткеч_VALUE));
    }

    private int атап_бирү_күрсәткеч() {
        return Киләсе_күрсәткеч++;
    }
}
