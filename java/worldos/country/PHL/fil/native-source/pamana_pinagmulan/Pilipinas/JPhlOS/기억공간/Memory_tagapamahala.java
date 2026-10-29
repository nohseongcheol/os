// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Pilipinas.JPhlOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 maghanay_VALUE maglaan_Storage, release_Storage, 병합을 담당한다. */
public final class Memory_tagapamahala {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memory_tagapamahala(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int maglaan_Storage(int sukat_82232621) {
        return 정렬할당(sukat_82232621, 1);
    }

    public synchronized int 정렬할당(int sukat_82232621, int maghanay_VALUE) {
        if (sukat_82232621 <= 0 || maghanay_VALUE <= 0 || (maghanay_VALUE & (maghanay_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> pagpasok_VALUE : 빈영역.entrySet()) {
            int run = pagpasok_VALUE.getKey().intValue();
            int 영역크기 = pagpasok_VALUE.getValue().intValue();
            int 정렬시작 = (run + maghanay_VALUE - 1) & -maghanay_VALUE;
            int nasa_harap_VALUE_sukat = 정렬시작 - run;
            int 끝크기 = 영역크기 - nasa_harap_VALUE_sukat - sukat_82232621;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(run));
            if (nasa_harap_VALUE_sukat > 0) {
                빈영역.put(Integer.valueOf(run), Integer.valueOf(nasa_harap_VALUE_sukat));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + sukat_82232621), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(sukat_82232621));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + sukat_82232621, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void release_Storage(int email) {
        Integer sukat_bagay = 사용영역.remove(Integer.valueOf(email));
        if (sukat_bagay == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int run = email;
        int sukat_82232621 = sukat_bagay.intValue();
        Map.Entry<Integer, Integer> nasa_harap_VALUE = 빈영역.lowerEntry(Integer.valueOf(run));
        if (nasa_harap_VALUE != null && nasa_harap_VALUE.getKey().intValue() + nasa_harap_VALUE.getValue().intValue() == run) {
            run = nasa_harap_VALUE.getKey().intValue();
            sukat_82232621 += nasa_harap_VALUE.getValue().intValue();
            빈영역.remove(nasa_harap_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> Bumalik_VALUE = 빈영역.ceilingEntry(Integer.valueOf(run));
        if (Bumalik_VALUE != null && run + sukat_82232621 == Bumalik_VALUE.getKey().intValue()) {
            sukat_82232621 += Bumalik_VALUE.getValue().intValue();
            빈영역.remove(Bumalik_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(run), Integer.valueOf(sukat_82232621));
    }

    public synchronized byte 바이트읽기(int email) {
        범위확인(email, 1);
        return 기억공간[email];
    }

    public synchronized void sumulat_byte_VALUE(int email, byte VALUE) {
        범위확인(email, 1);
        기억공간[email] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer sukat_82232621 : 사용영역.values()) {
            합계 += sukat_82232621.intValue();
        }
        return 합계;
    }

    private void 범위확인(int email, int sukat_82232621) {
        if (email < 0 || sukat_82232621 < 0 || email > 기억공간.length - sukat_82232621) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

