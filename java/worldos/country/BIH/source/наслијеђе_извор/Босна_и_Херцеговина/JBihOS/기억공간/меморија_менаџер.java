// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 поравнати_вриједност 할당, 해제, 병합을 담당한다. */
public final class меморија_менаџер {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public меморија_менаџер(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int 할당(int подесити_величину) {
        return 정렬할당(подесити_величину, 1);
    }

    public synchronized int 정렬할당(int подесити_величину, int поравнати_вриједност) {
        if (подесити_величину <= 0 || поравнати_вриједност <= 0 || (поравнати_вриједност & (поравнати_вриједност - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> унос_вриједност : 빈영역.entrySet()) {
            int 시작 = унос_вриједност.getKey().intValue();
            int 영역크기 = унос_вриједност.getValue().intValue();
            int 정렬시작 = (시작 + поравнати_вриједност - 1) & -поравнати_вриједност;
            int 앞크기 = 정렬시작 - 시작;
            int 끝크기 = 영역크기 - 앞크기 - подесити_величину;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(시작));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(시작), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + подесити_величину), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(подесити_величину));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + подесити_величину, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void 해제(int адреса) {
        Integer подесити_величину_објект = 사용영역.remove(Integer.valueOf(адреса));
        if (подесити_величину_објект == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int 시작 = адреса;
        int подесити_величину = подесити_величину_објект.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(시작));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == 시작) {
            시작 = 앞.getKey().intValue();
            подесити_величину += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Назад_вриједност = 빈영역.ceilingEntry(Integer.valueOf(시작));
        if (Назад_вриједност != null && 시작 + подесити_величину == Назад_вриједност.getKey().intValue()) {
            подесити_величину += Назад_вриједност.getValue().intValue();
            빈영역.remove(Назад_вриједност.getKey());
        }
        빈영역.put(Integer.valueOf(시작), Integer.valueOf(подесити_величину));
    }

    public synchronized byte 바이트읽기(int адреса) {
        범위확인(адреса, 1);
        return 기억공간[адреса];
    }

    public synchronized void писати_бајт_вриједност(int адреса, byte вриједност) {
        범위확인(адреса, 1);
        기억공간[адреса] = вриједност;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer подесити_величину : 사용영역.values()) {
            합계 += подесити_величину.intValue();
        }
        return 합계;
    }

    private void 범위확인(int адреса, int подесити_величину) {
        if (адреса < 0 || подесити_величину < 0 || адреса > 기억공간.length - подесити_величину) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

