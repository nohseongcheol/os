// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Թուրքիա.JTurOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 հավասարեցնել_արժեք հատկացնել_Պահեստ, արձակել_Պահեստ, 병합을 담당한다. */
public final class Հիշողություն_կառավարիչ {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Հիշողություն_կառավարիչ(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int հատկացնել_Պահեստ(int Չափս) {
        return 정렬할당(Չափս, 1);
    }

    public synchronized int 정렬할당(int Չափս, int հավասարեցնել_արժեք) {
        if (Չափս <= 0 || հավասարեցնել_արժեք <= 0 || (հավասարեցնել_արժեք & (հավասարեցնել_արժեք - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> մուտքագրում_արժեք : 빈영역.entrySet()) {
            int Գործարկել = մուտքագրում_արժեք.getKey().intValue();
            int 영역크기 = մուտքագրում_արժեք.getValue().intValue();
            int 정렬시작 = (Գործարկել + հավասարեցնել_արժեք - 1) & -հավասարեցնել_արժեք;
            int 앞크기 = 정렬시작 - Գործարկել;
            int 끝크기 = 영역크기 - 앞크기 - Չափս;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Գործարկել));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Գործարկել), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Չափս), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Չափս));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Չափս, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void արձակել_Պահեստ(int հասցե) {
        Integer չափափոխել_առարկա = 사용영역.remove(Integer.valueOf(հասցե));
        if (չափափոխել_առարկա == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Գործարկել = հասցե;
        int Չափս = չափափոխել_առարկա.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Գործարկել));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Գործարկել) {
            Գործարկել = 앞.getKey().intValue();
            Չափս += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Հետ_արժեք = 빈영역.ceilingEntry(Integer.valueOf(Գործարկել));
        if (Հետ_արժեք != null && Գործարկել + Չափս == Հետ_արժեք.getKey().intValue()) {
            Չափս += Հետ_արժեք.getValue().intValue();
            빈영역.remove(Հետ_արժեք.getKey());
        }
        빈영역.put(Integer.valueOf(Գործարկել), Integer.valueOf(Չափս));
    }

    public synchronized byte 바이트읽기(int հասցե) {
        범위확인(հասցե, 1);
        return 기억공간[հասցե];
    }

    public synchronized void գրել_բայթ_արժեք(int հասցե, byte արժեք) {
        범위확인(հասցե, 1);
        기억공간[հասցե] = արժեք;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Չափս : 사용영역.values()) {
            합계 += Չափս.intValue();
        }
        return 합계;
    }

    private void 범위확인(int հասցե, int Չափս) {
        if (հասցե < 0 || Չափս < 0 || հասցե > 기억공간.length - Չափս) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

