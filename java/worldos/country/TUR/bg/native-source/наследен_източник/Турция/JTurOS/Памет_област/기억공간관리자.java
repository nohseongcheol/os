// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Турция.JTurOS.Памет_област;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 подравнявам_стойност заделям_Памет, издание_Памет, 병합을 담당한다. */
public final class 기억공간관리자 {
    private final byte[] Памет_област;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public 기억공간관리자(int общо_размер) {
        if (общо_размер < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Памет_област = new byte[общо_размер];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(общо_размер - 4096));
    }

    public synchronized int заделям_Памет(int Размер) {
        return 정렬할당(Размер, 1);
    }

    public synchronized int 정렬할당(int Размер, int подравнявам_стойност) {
        if (Размер <= 0 || подравнявам_стойност <= 0 || (подравнявам_стойност & (подравнявам_стойност - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> запис_стойност : 빈영역.entrySet()) {
            int Стартиране = запис_стойност.getKey().intValue();
            int област_размер = запис_стойност.getValue().intValue();
            int 정렬시작 = (Стартиране + подравнявам_стойност - 1) & -подравнявам_стойност;
            int предна_стойност_размер = 정렬시작 - Стартиране;
            int 끝크기 = област_размер - предна_стойност_размер - Размер;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Стартиране));
            if (предна_стойност_размер > 0) {
                빈영역.put(Integer.valueOf(Стартиране), Integer.valueOf(предна_стойност_размер));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Размер), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Размер));
            Arrays.fill(Памет_област, 정렬시작, 정렬시작 + Размер, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void издание_Памет(int адрес) {
        Integer размер_обект = 사용영역.remove(Integer.valueOf(адрес));
        if (размер_обект == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Стартиране = адрес;
        int Размер = размер_обект.intValue();
        Map.Entry<Integer, Integer> предна_стойност = 빈영역.lowerEntry(Integer.valueOf(Стартиране));
        if (предна_стойност != null && предна_стойност.getKey().intValue() + предна_стойност.getValue().intValue() == Стартиране) {
            Стартиране = предна_стойност.getKey().intValue();
            Размер += предна_стойност.getValue().intValue();
            빈영역.remove(предна_стойност.getKey());
        }
        Map.Entry<Integer, Integer> НАЗАД_стойност = 빈영역.ceilingEntry(Integer.valueOf(Стартиране));
        if (НАЗАД_стойност != null && Стартиране + Размер == НАЗАД_стойност.getKey().intValue()) {
            Размер += НАЗАД_стойност.getValue().intValue();
            빈영역.remove(НАЗАД_стойност.getKey());
        }
        빈영역.put(Integer.valueOf(Стартиране), Integer.valueOf(Размер));
    }

    public synchronized byte 바이트읽기(int адрес) {
        проверявам_обхват(адрес, 1);
        return Памет_област[адрес];
    }

    public synchronized void записване_байт_стойност(int адрес, byte стойност) {
        проверявам_обхват(адрес, 1);
        Памет_област[адрес] = стойност;
    }

    public synchronized int общо_размер() {
        return Памет_област.length;
    }

    public synchronized int 사용크기() {
        int общо_стойност = 0;
        for (Integer Размер : 사용영역.values()) {
            общо_стойност += Размер.intValue();
        }
        return общо_стойност;
    }

    private void проверявам_обхват(int адрес, int Размер) {
        if (адрес < 0 || Размер < 0 || адрес > Памет_област.length - Размер) {
            throw new IndexOutOfBoundsException("Памет_област 범위를 벗어났습니다.");
        }
    }
}

