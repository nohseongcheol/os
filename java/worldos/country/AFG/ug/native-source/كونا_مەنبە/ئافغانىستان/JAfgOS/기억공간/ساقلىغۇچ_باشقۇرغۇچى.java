// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئافغانىستان.JAfgOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 توغرىلىماق_قىممىتى تەقسىملەش_بوشلۇق, تارقىتىش_بوشلۇق, 병합을 담당한다. */
public final class ساقلىغۇچ_باشقۇرغۇچى {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ساقلىغۇچ_باشقۇرغۇچى(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int تەقسىملەش_بوشلۇق(int چوڭلۇقى) {
        return 정렬할당(چوڭلۇقى, 1);
    }

    public synchronized int 정렬할당(int چوڭلۇقى, int توغرىلىماق_قىممىتى) {
        if (چوڭلۇقى <= 0 || توغرىلىماق_قىممىتى <= 0 || (توغرىلىماق_قىممىتى & (توغرىلىماق_قىممىتى - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> كىرگۈزۈش_قىممىتى : 빈영역.entrySet()) {
            int ئىجرا_قىل_2 = كىرگۈزۈش_قىممىتى.getKey().intValue();
            int 영역크기 = كىرگۈزۈش_قىممىتى.getValue().intValue();
            int 정렬시작 = (ئىجرا_قىل_2 + توغرىلىماق_قىممىتى - 1) & -توغرىلىماق_قىممىتى;
            int 앞크기 = 정렬시작 - ئىجرا_قىل_2;
            int 끝크기 = 영역크기 - 앞크기 - چوڭلۇقى;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ئىجرا_قىل_2));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ئىجرا_قىل_2), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + چوڭلۇقى), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(چوڭلۇقى));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + چوڭلۇقى, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void تارقىتىش_بوشلۇق(int ئادرېس) {
        Integer ئۆزگەرتمەك_ئوبيېكت = 사용영역.remove(Integer.valueOf(ئادرېس));
        if (ئۆزگەرتمەك_ئوبيېكت == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ئىجرا_قىل_2 = ئادرېس;
        int چوڭلۇقى = ئۆزگەرتمەك_ئوبيېكت.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ئىجرا_قىل_2));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ئىجرا_قىل_2) {
            ئىجرا_قىل_2 = 앞.getKey().intValue();
            چوڭلۇقى += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> ئارقىغا_قىممىتى = 빈영역.ceilingEntry(Integer.valueOf(ئىجرا_قىل_2));
        if (ئارقىغا_قىممىتى != null && ئىجرا_قىل_2 + چوڭلۇقى == ئارقىغا_قىممىتى.getKey().intValue()) {
            چوڭلۇقى += ئارقىغا_قىممىتى.getValue().intValue();
            빈영역.remove(ئارقىغا_قىممىتى.getKey());
        }
        빈영역.put(Integer.valueOf(ئىجرا_قىل_2), Integer.valueOf(چوڭلۇقى));
    }

    public synchronized byte 바이트읽기(int ئادرېس) {
        범위확인(ئادرېس, 1);
        return 기억공간[ئادرېس];
    }

    public synchronized void يازماق_بايت_قىممىتى(int ئادرېس, byte قىممىتى) {
        범위확인(ئادرېس, 1);
        기억공간[ئادرېس] = قىممىتى;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer چوڭلۇقى : 사용영역.values()) {
            합계 += چوڭلۇقى.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ئادرېس, int چوڭلۇقى) {
        if (ئادرېس < 0 || چوڭلۇقى < 0 || ئادرېس > 기억공간.length - چوڭلۇقى) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

