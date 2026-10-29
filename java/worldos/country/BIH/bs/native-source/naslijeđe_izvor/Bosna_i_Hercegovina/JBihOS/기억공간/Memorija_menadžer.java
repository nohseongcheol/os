// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 poravnati_VALUE dodijeliti_Pohrana, izdanje_Pohrana, 병합을 담당한다. */
public final class Memorija_menadžer {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memorija_menadžer(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int dodijeliti_Pohrana(int Veličina) {
        return 정렬할당(Veličina, 1);
    }

    public synchronized int 정렬할당(int Veličina, int poravnati_VALUE) {
        if (Veličina <= 0 || poravnati_VALUE <= 0 || (poravnati_VALUE & (poravnati_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> unos_VALUE : 빈영역.entrySet()) {
            int Pokreni = unos_VALUE.getKey().intValue();
            int 영역크기 = unos_VALUE.getValue().intValue();
            int 정렬시작 = (Pokreni + poravnati_VALUE - 1) & -poravnati_VALUE;
            int 앞크기 = 정렬시작 - Pokreni;
            int 끝크기 = 영역크기 - 앞크기 - Veličina;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Pokreni));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Pokreni), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Veličina), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Veličina));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Veličina, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void izdanje_Pohrana(int adresa) {
        Integer podesiti_veličinu_objekt = 사용영역.remove(Integer.valueOf(adresa));
        if (podesiti_veličinu_objekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Pokreni = adresa;
        int Veličina = podesiti_veličinu_objekt.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Pokreni));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Pokreni) {
            Pokreni = 앞.getKey().intValue();
            Veličina += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> ZAD_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Pokreni));
        if (ZAD_VALUE != null && Pokreni + Veličina == ZAD_VALUE.getKey().intValue()) {
            Veličina += ZAD_VALUE.getValue().intValue();
            빈영역.remove(ZAD_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Pokreni), Integer.valueOf(Veličina));
    }

    public synchronized byte 바이트읽기(int adresa) {
        범위확인(adresa, 1);
        return 기억공간[adresa];
    }

    public synchronized void pisati_bajt_VALUE(int adresa, byte VALUE) {
        범위확인(adresa, 1);
        기억공간[adresa] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Veličina : 사용영역.values()) {
            합계 += Veličina.intValue();
        }
        return 합계;
    }

    private void 범위확인(int adresa, int Veličina) {
        if (adresa < 0 || Veličina < 0 || adresa > 기억공간.length - Veličina) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

