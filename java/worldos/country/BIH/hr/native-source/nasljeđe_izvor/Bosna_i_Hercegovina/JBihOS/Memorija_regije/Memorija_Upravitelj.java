// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.Memorija_regije;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 poravnati_VALUE dodijeli_Pohrana, izdati_Pohrana, 병합을 담당한다. */
public final class Memorija_Upravitelj {
    private final byte[] Memorija_regije;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memorija_Upravitelj(int ukupni_zbroj_promijeniti_veličinu) {
        if (ukupni_zbroj_promijeniti_veličinu < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Memorija_regije = new byte[ukupni_zbroj_promijeniti_veličinu];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(ukupni_zbroj_promijeniti_veličinu - 4096));
    }

    public synchronized int dodijeli_Pohrana(int Veličina) {
        return 정렬할당(Veličina, 1);
    }

    public synchronized int 정렬할당(int Veličina, int poravnati_VALUE) {
        if (Veličina <= 0 || poravnati_VALUE <= 0 || (poravnati_VALUE & (poravnati_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> unos_VALUE : 빈영역.entrySet()) {
            int Pokreni = unos_VALUE.getKey().intValue();
            int regije_promijeniti_veličinu = unos_VALUE.getValue().intValue();
            int 정렬시작 = (Pokreni + poravnati_VALUE - 1) & -poravnati_VALUE;
            int prednja_VALUE_promijeniti_veličinu = 정렬시작 - Pokreni;
            int 끝크기 = regije_promijeniti_veličinu - prednja_VALUE_promijeniti_veličinu - Veličina;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Pokreni));
            if (prednja_VALUE_promijeniti_veličinu > 0) {
                빈영역.put(Integer.valueOf(Pokreni), Integer.valueOf(prednja_VALUE_promijeniti_veličinu));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Veličina), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Veličina));
            Arrays.fill(Memorija_regije, 정렬시작, 정렬시작 + Veličina, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void izdati_Pohrana(int adresa) {
        Integer promijeniti_veličinu_objekt = 사용영역.remove(Integer.valueOf(adresa));
        if (promijeniti_veličinu_objekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Pokreni = adresa;
        int Veličina = promijeniti_veličinu_objekt.intValue();
        Map.Entry<Integer, Integer> prednja_VALUE = 빈영역.lowerEntry(Integer.valueOf(Pokreni));
        if (prednja_VALUE != null && prednja_VALUE.getKey().intValue() + prednja_VALUE.getValue().intValue() == Pokreni) {
            Pokreni = prednja_VALUE.getKey().intValue();
            Veličina += prednja_VALUE.getValue().intValue();
            빈영역.remove(prednja_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> TRAG_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Pokreni));
        if (TRAG_VALUE != null && Pokreni + Veličina == TRAG_VALUE.getKey().intValue()) {
            Veličina += TRAG_VALUE.getValue().intValue();
            빈영역.remove(TRAG_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Pokreni), Integer.valueOf(Veličina));
    }

    public synchronized byte 바이트읽기(int adresa) {
        범위확인(adresa, 1);
        return Memorija_regije[adresa];
    }

    public synchronized void zapisivanje_bajt_VALUE(int adresa, byte VALUE) {
        범위확인(adresa, 1);
        Memorija_regije[adresa] = VALUE;
    }

    public synchronized int ukupni_zbroj_promijeniti_veličinu() {
        return Memorija_regije.length;
    }

    public synchronized int 사용크기() {
        int ukupni_zbroj_VALUE = 0;
        for (Integer Veličina : 사용영역.values()) {
            ukupni_zbroj_VALUE += Veličina.intValue();
        }
        return ukupni_zbroj_VALUE;
    }

    private void 범위확인(int adresa, int Veličina) {
        if (adresa < 0 || Veličina < 0 || adresa > Memorija_regije.length - Veličina) {
            throw new IndexOutOfBoundsException("Memorija_regije 범위를 벗어났습니다.");
        }
    }
}

