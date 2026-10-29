// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 тегиздөө_маани энчилөө_сактагыч, чыгаруу_сактагыч, 병합을 담당한다. */
public final class эс_башкаруучу {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public эс_башкаруучу(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int энчилөө_сактагыч(int Өлчөмү) {
        return 정렬할당(Өлчөмү, 1);
    }

    public synchronized int 정렬할당(int Өлчөмү, int тегиздөө_маани) {
        if (Өлчөмү <= 0 || тегиздөө_маани <= 0 || (тегиздөө_маани & (тегиздөө_маани - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> киргизме_жазуу_маани : 빈영역.entrySet()) {
            int Жүргүзүү = киргизме_жазуу_маани.getKey().intValue();
            int 영역크기 = киргизме_жазуу_маани.getValue().intValue();
            int 정렬시작 = (Жүргүзүү + тегиздөө_маани - 1) & -тегиздөө_маани;
            int 앞크기 = 정렬시작 - Жүргүзүү;
            int 끝크기 = 영역크기 - 앞크기 - Өлчөмү;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Жүргүзүү));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Жүргүзүү), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Өлчөмү), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Өлчөмү));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Өлчөмү, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void чыгаруу_сактагыч(int дарек) {
        Integer көлөм_объект = 사용영역.remove(Integer.valueOf(дарек));
        if (көлөм_объект == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Жүргүзүү = дарек;
        int Өлчөмү = көлөм_объект.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Жүргүзүү));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Жүргүзүү) {
            Жүргүзүү = 앞.getKey().intValue();
            Өлчөмү += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Артка_маани = 빈영역.ceilingEntry(Integer.valueOf(Жүргүзүү));
        if (Артка_маани != null && Жүргүзүү + Өлчөмү == Артка_маани.getKey().intValue()) {
            Өлчөмү += Артка_маани.getValue().intValue();
            빈영역.remove(Артка_маани.getKey());
        }
        빈영역.put(Integer.valueOf(Жүргүзүү), Integer.valueOf(Өлчөмү));
    }

    public synchronized byte 바이트읽기(int дарек) {
        범위확인(дарек, 1);
        return 기억공간[дарек];
    }

    public synchronized void жазуу_байт_маани(int дарек, byte маани) {
        범위확인(дарек, 1);
        기억공간[дарек] = маани;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Өлчөмү : 사용영역.values()) {
            합계 += Өлчөмү.intValue();
        }
        return 합계;
    }

    private void 범위확인(int дарек, int Өлчөмү) {
        if (дарек < 0 || Өлчөмү < 0 || дарек > 기억공간.length - Өлчөмү) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

