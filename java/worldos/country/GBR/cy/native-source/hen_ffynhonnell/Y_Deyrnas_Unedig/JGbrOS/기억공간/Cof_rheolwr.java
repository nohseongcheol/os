// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Y_Deyrnas_Unedig.JGbrOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 alinio_VALUE dyrannu_Storio, rhyddhau_Storio, 병합을 담당한다. */
public final class Cof_rheolwr {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Cof_rheolwr(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int dyrannu_Storio(int Maint) {
        return 정렬할당(Maint, 1);
    }

    public synchronized int 정렬할당(int Maint, int alinio_VALUE) {
        if (Maint <= 0 || alinio_VALUE <= 0 || (alinio_VALUE & (alinio_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> cofnod_VALUE : 빈영역.entrySet()) {
            int Gweithredu_2 = cofnod_VALUE.getKey().intValue();
            int 영역크기 = cofnod_VALUE.getValue().intValue();
            int 정렬시작 = (Gweithredu_2 + alinio_VALUE - 1) & -alinio_VALUE;
            int 앞크기 = 정렬시작 - Gweithredu_2;
            int 끝크기 = 영역크기 - 앞크기 - Maint;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Gweithredu_2));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Gweithredu_2), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Maint), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Maint));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Maint, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void rhyddhau_Storio(int ADDRESS) {
        Integer newid_maint_gwrthrych = 사용영역.remove(Integer.valueOf(ADDRESS));
        if (newid_maint_gwrthrych == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Gweithredu_2 = ADDRESS;
        int Maint = newid_maint_gwrthrych.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Gweithredu_2));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Gweithredu_2) {
            Gweithredu_2 = 앞.getKey().intValue();
            Maint += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> BACK_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Gweithredu_2));
        if (BACK_VALUE != null && Gweithredu_2 + Maint == BACK_VALUE.getKey().intValue()) {
            Maint += BACK_VALUE.getValue().intValue();
            빈영역.remove(BACK_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Gweithredu_2), Integer.valueOf(Maint));
    }

    public synchronized byte 바이트읽기(int ADDRESS) {
        범위확인(ADDRESS, 1);
        return 기억공간[ADDRESS];
    }

    public synchronized void ysgrifennu_beit_VALUE(int ADDRESS, byte VALUE) {
        범위확인(ADDRESS, 1);
        기억공간[ADDRESS] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Maint : 사용영역.values()) {
            합계 += Maint.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ADDRESS, int Maint) {
        if (ADDRESS < 0 || Maint < 0 || ADDRESS > 기억공간.length - Maint) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

