// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Грција.JGrcOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 порамни_VALUE додели_Склад, издание_Склад, 병합을 담당한다. */
public final class Меморија_управник {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Меморија_управник(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int додели_Склад(int Големина) {
        return 정렬할당(Големина, 1);
    }

    public synchronized int 정렬할당(int Големина, int порамни_VALUE) {
        if (Големина <= 0 || порамни_VALUE <= 0 || (порамни_VALUE & (порамни_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> внес_VALUE : 빈영역.entrySet()) {
            int Изврши_2 = внес_VALUE.getKey().intValue();
            int 영역크기 = внес_VALUE.getValue().intValue();
            int 정렬시작 = (Изврши_2 + порамни_VALUE - 1) & -порамни_VALUE;
            int предна_VALUE_големина = 정렬시작 - Изврши_2;
            int 끝크기 = 영역크기 - предна_VALUE_големина - Големина;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Изврши_2));
            if (предна_VALUE_големина > 0) {
                빈영역.put(Integer.valueOf(Изврши_2), Integer.valueOf(предна_VALUE_големина));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Големина), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Големина));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Големина, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void издание_Склад(int адреса) {
        Integer големина_објект = 사용영역.remove(Integer.valueOf(адреса));
        if (големина_објект == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Изврши_2 = адреса;
        int Големина = големина_објект.intValue();
        Map.Entry<Integer, Integer> предна_VALUE = 빈영역.lowerEntry(Integer.valueOf(Изврши_2));
        if (предна_VALUE != null && предна_VALUE.getKey().intValue() + предна_VALUE.getValue().intValue() == Изврши_2) {
            Изврши_2 = предна_VALUE.getKey().intValue();
            Големина += предна_VALUE.getValue().intValue();
            빈영역.remove(предна_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> Назад_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Изврши_2));
        if (Назад_VALUE != null && Изврши_2 + Големина == Назад_VALUE.getKey().intValue()) {
            Големина += Назад_VALUE.getValue().intValue();
            빈영역.remove(Назад_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Изврши_2), Integer.valueOf(Големина));
    }

    public synchronized byte 바이트읽기(int адреса) {
        범위확인(адреса, 1);
        return 기억공간[адреса];
    }

    public synchronized void запиши_бајт_VALUE(int адреса, byte VALUE) {
        범위확인(адреса, 1);
        기억공간[адреса] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Големина : 사용영역.values()) {
            합계 += Големина.intValue();
        }
        return 합계;
    }

    private void 범위확인(int адреса, int Големина) {
        if (адреса < 0 || Големина < 0 || адреса > 기억공간.length - Големина) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

