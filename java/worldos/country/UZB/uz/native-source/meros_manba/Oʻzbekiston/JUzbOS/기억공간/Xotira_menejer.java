// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Oʻzbekiston.JUzbOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 tenglashtirmoq_VALUE joylashtirmoq_Xotira, nashr_Xotira, 병합을 담당한다. */
public final class Xotira_menejer {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Xotira_menejer(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int joylashtirmoq_Xotira(int Hajmi) {
        return 정렬할당(Hajmi, 1);
    }

    public synchronized int 정렬할당(int Hajmi, int tenglashtirmoq_VALUE) {
        if (Hajmi <= 0 || tenglashtirmoq_VALUE <= 0 || (tenglashtirmoq_VALUE & (tenglashtirmoq_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> kiritish_VALUE : 빈영역.entrySet()) {
            int Bajarish = kiritish_VALUE.getKey().intValue();
            int 영역크기 = kiritish_VALUE.getValue().intValue();
            int 정렬시작 = (Bajarish + tenglashtirmoq_VALUE - 1) & -tenglashtirmoq_VALUE;
            int old_kamera_VALUE_o_lcham = 정렬시작 - Bajarish;
            int 끝크기 = 영역크기 - old_kamera_VALUE_o_lcham - Hajmi;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Bajarish));
            if (old_kamera_VALUE_o_lcham > 0) {
                빈영역.put(Integer.valueOf(Bajarish), Integer.valueOf(old_kamera_VALUE_o_lcham));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Hajmi), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Hajmi));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Hajmi, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void nashr_Xotira(int manzil) {
        Integer o_lcham_obyekt = 사용영역.remove(Integer.valueOf(manzil));
        if (o_lcham_obyekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Bajarish = manzil;
        int Hajmi = o_lcham_obyekt.intValue();
        Map.Entry<Integer, Integer> old_kamera_VALUE = 빈영역.lowerEntry(Integer.valueOf(Bajarish));
        if (old_kamera_VALUE != null && old_kamera_VALUE.getKey().intValue() + old_kamera_VALUE.getValue().intValue() == Bajarish) {
            Bajarish = old_kamera_VALUE.getKey().intValue();
            Hajmi += old_kamera_VALUE.getValue().intValue();
            빈영역.remove(old_kamera_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> Orqaga_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Bajarish));
        if (Orqaga_VALUE != null && Bajarish + Hajmi == Orqaga_VALUE.getKey().intValue()) {
            Hajmi += Orqaga_VALUE.getValue().intValue();
            빈영역.remove(Orqaga_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Bajarish), Integer.valueOf(Hajmi));
    }

    public synchronized byte 바이트읽기(int manzil) {
        범위확인(manzil, 1);
        return 기억공간[manzil];
    }

    public synchronized void yozmoq_bayt_VALUE(int manzil, byte VALUE) {
        범위확인(manzil, 1);
        기억공간[manzil] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Hajmi : 사용영역.values()) {
            합계 += Hajmi.intValue();
        }
        return 합계;
    }

    private void 범위확인(int manzil, int Hajmi) {
        if (manzil < 0 || Hajmi < 0 || manzil > 기억공간.length - Hajmi) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

