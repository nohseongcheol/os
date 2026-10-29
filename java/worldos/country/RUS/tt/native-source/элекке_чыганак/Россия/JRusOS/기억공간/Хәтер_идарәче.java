// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 тигезләү_VALUE атап_бирү_Саклагыч, Чыгарылыш_Саклагыч, 병합을 담당한다. */
public final class Хәтер_идарәче {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Хәтер_идарәче(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int атап_бирү_Саклагыч(int үлчәмен_үзгәртү) {
        return 정렬할당(үлчәмен_үзгәртү, 1);
    }

    public synchronized int 정렬할당(int үлчәмен_үзгәртү, int тигезләү_VALUE) {
        if (үлчәмен_үзгәртү <= 0 || тигезләү_VALUE <= 0 || (тигезләү_VALUE & (тигезләү_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> кертү_VALUE : 빈영역.entrySet()) {
            int эшләтү = кертү_VALUE.getKey().intValue();
            int 영역크기 = кертү_VALUE.getValue().intValue();
            int 정렬시작 = (эшләтү + тигезләү_VALUE - 1) & -тигезләү_VALUE;
            int 앞크기 = 정렬시작 - эшләтү;
            int 끝크기 = 영역크기 - 앞크기 - үлчәмен_үзгәртү;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(эшләтү));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(эшләтү), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + үлчәмен_үзгәртү), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(үлчәмен_үзгәртү));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + үлчәмен_үзгәртү, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void Чыгарылыш_Саклагыч(int адрес) {
        Integer үлчәмен_үзгәртү_объект = 사용영역.remove(Integer.valueOf(адрес));
        if (үлчәмен_үзгәртү_объект == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int эшләтү = адрес;
        int үлчәмен_үзгәртү = үлчәмен_үзгәртү_объект.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(эшләтү));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == эшләтү) {
            эшләтү = 앞.getKey().intValue();
            үлчәмен_үзгәртү += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Артка_VALUE = 빈영역.ceilingEntry(Integer.valueOf(эшләтү));
        if (Артка_VALUE != null && эшләтү + үлчәмен_үзгәртү == Артка_VALUE.getKey().intValue()) {
            үлчәмен_үзгәртү += Артка_VALUE.getValue().intValue();
            빈영역.remove(Артка_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(эшләтү), Integer.valueOf(үлчәмен_үзгәртү));
    }

    public synchronized byte 바이트읽기(int адрес) {
        범위확인(адрес, 1);
        return 기억공간[адрес];
    }

    public synchronized void язу_байт_VALUE(int адрес, byte VALUE) {
        범위확인(адрес, 1);
        기억공간[адрес] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer үлчәмен_үзгәртү : 사용영역.values()) {
            합계 += үлчәмен_үзгәртү.intValue();
        }
        return 합계;
    }

    private void 범위확인(int адрес, int үлчәмен_үзгәртү) {
        if (адрес < 0 || үлчәмен_үзгәртү < 0 || адрес > 기억공간.length - үлчәмен_үзгәртү) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

