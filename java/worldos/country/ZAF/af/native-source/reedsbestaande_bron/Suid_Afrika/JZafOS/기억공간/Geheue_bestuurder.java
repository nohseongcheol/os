// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suid_Afrika.JZafOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 belyn_VALUE toewys_Berging, stel_vry_Berging, 병합을 담당한다. */
public final class Geheue_bestuurder {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Geheue_bestuurder(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int toewys_Berging(int Grootte) {
        return 정렬할당(Grootte, 1);
    }

    public synchronized int 정렬할당(int Grootte, int belyn_VALUE) {
        if (Grootte <= 0 || belyn_VALUE <= 0 || (belyn_VALUE & (belyn_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> inskrywing_VALUE : 빈영역.entrySet()) {
            int Loop = inskrywing_VALUE.getKey().intValue();
            int 영역크기 = inskrywing_VALUE.getValue().intValue();
            int 정렬시작 = (Loop + belyn_VALUE - 1) & -belyn_VALUE;
            int voor_VALUE_verstel = 정렬시작 - Loop;
            int 끝크기 = 영역크기 - voor_VALUE_verstel - Grootte;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Loop));
            if (voor_VALUE_verstel > 0) {
                빈영역.put(Integer.valueOf(Loop), Integer.valueOf(voor_VALUE_verstel));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Grootte), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Grootte));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Grootte, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void stel_vry_Berging(int adres) {
        Integer verstel_objek = 사용영역.remove(Integer.valueOf(adres));
        if (verstel_objek == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Loop = adres;
        int Grootte = verstel_objek.intValue();
        Map.Entry<Integer, Integer> voor_VALUE = 빈영역.lowerEntry(Integer.valueOf(Loop));
        if (voor_VALUE != null && voor_VALUE.getKey().intValue() + voor_VALUE.getValue().intValue() == Loop) {
            Loop = voor_VALUE.getKey().intValue();
            Grootte += voor_VALUE.getValue().intValue();
            빈영역.remove(voor_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> TERUG_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Loop));
        if (TERUG_VALUE != null && Loop + Grootte == TERUG_VALUE.getKey().intValue()) {
            Grootte += TERUG_VALUE.getValue().intValue();
            빈영역.remove(TERUG_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Loop), Integer.valueOf(Grootte));
    }

    public synchronized byte 바이트읽기(int adres) {
        범위확인(adres, 1);
        return 기억공간[adres];
    }

    public synchronized void skryf_greep_VALUE(int adres, byte VALUE) {
        범위확인(adres, 1);
        기억공간[adres] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Grootte : 사용영역.values()) {
            합계 += Grootte.intValue();
        }
        return 합계;
    }

    private void 범위확인(int adres, int Grootte) {
        if (adres < 0 || Grootte < 0 || adres > 기억공간.length - Grootte) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

