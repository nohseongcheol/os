// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 поравнати_вриједност доделити_похрана, издање_похрана, 병합을 담당한다. */
public final class Меморија_менаџер {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Меморија_менаџер(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int доделити_похрана(int Величина) {
        return 정렬할당(Величина, 1);
    }

    public synchronized int 정렬할당(int Величина, int поравнати_вриједност) {
        if (Величина <= 0 || поравнати_вриједност <= 0 || (поравнати_вриједност & (поравнати_вриједност - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> унос_вриједност : 빈영역.entrySet()) {
            int Покрени = унос_вриједност.getKey().intValue();
            int 영역크기 = унос_вриједност.getValue().intValue();
            int 정렬시작 = (Покрени + поравнати_вриједност - 1) & -поравнати_вриједност;
            int 앞크기 = 정렬시작 - Покрени;
            int 끝크기 = 영역크기 - 앞크기 - Величина;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Покрени));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Покрени), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Величина), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Величина));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Величина, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void издање_похрана(int адреса) {
        Integer подесити_величину_објекат = 사용영역.remove(Integer.valueOf(адреса));
        if (подесити_величину_објекат == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Покрени = адреса;
        int Величина = подесити_величину_објекат.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Покрени));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Покрени) {
            Покрени = 앞.getKey().intValue();
            Величина += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> НАЗАД_вриједност = 빈영역.ceilingEntry(Integer.valueOf(Покрени));
        if (НАЗАД_вриједност != null && Покрени + Величина == НАЗАД_вриједност.getKey().intValue()) {
            Величина += НАЗАД_вриједност.getValue().intValue();
            빈영역.remove(НАЗАД_вриједност.getKey());
        }
        빈영역.put(Integer.valueOf(Покрени), Integer.valueOf(Величина));
    }

    public synchronized byte 바이트읽기(int адреса) {
        чек_опсег(адреса, 1);
        return 기억공간[адреса];
    }

    public synchronized void писати_бајт_вриједност(int адреса, byte вриједност) {
        чек_опсег(адреса, 1);
        기억공간[адреса] = вриједност;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Величина : 사용영역.values()) {
            합계 += Величина.intValue();
        }
        return 합계;
    }

    private void чек_опсег(int адреса, int Величина) {
        if (адреса < 0 || Величина < 0 || адреса > 기억공간.length - Величина) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

