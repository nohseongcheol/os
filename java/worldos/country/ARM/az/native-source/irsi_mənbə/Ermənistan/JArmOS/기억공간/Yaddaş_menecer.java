// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ermənistan.JArmOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 düzləndirmək_VALUE ayırmaq_Yaddaş, burax_Yaddaş, 병합을 담당한다. */
public final class Yaddaş_menecer {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Yaddaş_menecer(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int ayırmaq_Yaddaş(int Böyüklük) {
        return 정렬할당(Böyüklük, 1);
    }

    public synchronized int 정렬할당(int Böyüklük, int düzləndirmək_VALUE) {
        if (Böyüklük <= 0 || düzləndirmək_VALUE <= 0 || (düzləndirmək_VALUE & (düzləndirmək_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> daxiletmə_VALUE : 빈영역.entrySet()) {
            int İcra_Et = daxiletmə_VALUE.getKey().intValue();
            int 영역크기 = daxiletmə_VALUE.getValue().intValue();
            int 정렬시작 = (İcra_Et + düzləndirmək_VALUE - 1) & -düzləndirmək_VALUE;
            int ön_VALUE_ölçünü_dəyişmək = 정렬시작 - İcra_Et;
            int 끝크기 = 영역크기 - ön_VALUE_ölçünü_dəyişmək - Böyüklük;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(İcra_Et));
            if (ön_VALUE_ölçünü_dəyişmək > 0) {
                빈영역.put(Integer.valueOf(İcra_Et), Integer.valueOf(ön_VALUE_ölçünü_dəyişmək));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Böyüklük), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Böyüklük));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Böyüklük, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void burax_Yaddaş(int ünvan) {
        Integer ölçünü_dəyişmək_obyekt = 사용영역.remove(Integer.valueOf(ünvan));
        if (ölçünü_dəyişmək_obyekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int İcra_Et = ünvan;
        int Böyüklük = ölçünü_dəyişmək_obyekt.intValue();
        Map.Entry<Integer, Integer> ön_VALUE = 빈영역.lowerEntry(Integer.valueOf(İcra_Et));
        if (ön_VALUE != null && ön_VALUE.getKey().intValue() + ön_VALUE.getValue().intValue() == İcra_Et) {
            İcra_Et = ön_VALUE.getKey().intValue();
            Böyüklük += ön_VALUE.getValue().intValue();
            빈영역.remove(ön_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> GERİ_VALUE = 빈영역.ceilingEntry(Integer.valueOf(İcra_Et));
        if (GERİ_VALUE != null && İcra_Et + Böyüklük == GERİ_VALUE.getKey().intValue()) {
            Böyüklük += GERİ_VALUE.getValue().intValue();
            빈영역.remove(GERİ_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(İcra_Et), Integer.valueOf(Böyüklük));
    }

    public synchronized byte 바이트읽기(int ünvan) {
        범위확인(ünvan, 1);
        return 기억공간[ünvan];
    }

    public synchronized void yazmaq_bayt_VALUE(int ünvan, byte VALUE) {
        범위확인(ünvan, 1);
        기억공간[ünvan] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Böyüklük : 사용영역.values()) {
            합계 += Böyüklük.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ünvan, int Böyüklük) {
        if (ünvan < 0 || Böyüklük < 0 || ünvan > 기억공간.length - Böyüklük) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

