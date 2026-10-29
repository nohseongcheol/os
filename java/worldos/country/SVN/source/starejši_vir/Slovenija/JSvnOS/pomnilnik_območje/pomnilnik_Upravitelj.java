// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.pomnilnik_območje;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 poravnati_VALUE dodeliti_Senzor_prostora, izdaja_Senzor_prostora, 병합을 담당한다. */
public final class pomnilnik_Upravitelj {
    private final byte[] pomnilnik_območje;
    private final TreeMap<Integer, Integer> prazen_območje = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public pomnilnik_Upravitelj(int skupaj_spremeniti_velikost) {
        if (skupaj_spremeniti_velikost < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        pomnilnik_območje = new byte[skupaj_spremeniti_velikost];
        prazen_območje.put(Integer.valueOf(4096), Integer.valueOf(skupaj_spremeniti_velikost - 4096));
    }

    public synchronized int dodeliti_Senzor_prostora(int Velikost) {
        return 정렬할당(Velikost, 1);
    }

    public synchronized int 정렬할당(int Velikost, int poravnati_VALUE) {
        if (Velikost <= 0 || poravnati_VALUE <= 0 || (poravnati_VALUE & (poravnati_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> vnos_VALUE : prazen_območje.entrySet()) {
            int Zaženi = vnos_VALUE.getKey().intValue();
            int območje_spremeniti_velikost = vnos_VALUE.getValue().intValue();
            int 정렬시작 = (Zaženi + poravnati_VALUE - 1) & -poravnati_VALUE;
            int sprednja_VALUE_spremeniti_velikost = 정렬시작 - Zaženi;
            int 끝크기 = območje_spremeniti_velikost - sprednja_VALUE_spremeniti_velikost - Velikost;
            if (끝크기 < 0) {
                continue;
            }
            prazen_območje.remove(Integer.valueOf(Zaženi));
            if (sprednja_VALUE_spremeniti_velikost > 0) {
                prazen_območje.put(Integer.valueOf(Zaženi), Integer.valueOf(sprednja_VALUE_spremeniti_velikost));
            }
            if (끝크기 > 0) {
                prazen_območje.put(Integer.valueOf(정렬시작 + Velikost), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Velikost));
            Arrays.fill(pomnilnik_območje, 정렬시작, 정렬시작 + Velikost, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void izdaja_Senzor_prostora(int naslov) {
        Integer spremeniti_velikost_predmet = 사용영역.remove(Integer.valueOf(naslov));
        if (spremeniti_velikost_predmet == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Zaženi = naslov;
        int Velikost = spremeniti_velikost_predmet.intValue();
        Map.Entry<Integer, Integer> sprednja_VALUE = prazen_območje.lowerEntry(Integer.valueOf(Zaženi));
        if (sprednja_VALUE != null && sprednja_VALUE.getKey().intValue() + sprednja_VALUE.getValue().intValue() == Zaženi) {
            Zaženi = sprednja_VALUE.getKey().intValue();
            Velikost += sprednja_VALUE.getValue().intValue();
            prazen_območje.remove(sprednja_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> ZAJ_VALUE = prazen_območje.ceilingEntry(Integer.valueOf(Zaženi));
        if (ZAJ_VALUE != null && Zaženi + Velikost == ZAJ_VALUE.getKey().intValue()) {
            Velikost += ZAJ_VALUE.getValue().intValue();
            prazen_območje.remove(ZAJ_VALUE.getKey());
        }
        prazen_območje.put(Integer.valueOf(Zaženi), Integer.valueOf(Velikost));
    }

    public synchronized byte 바이트읽기(int naslov) {
        preveriti_obseg(naslov, 1);
        return pomnilnik_območje[naslov];
    }

    public synchronized void pisati_bajt_VALUE(int naslov, byte VALUE) {
        preveriti_obseg(naslov, 1);
        pomnilnik_območje[naslov] = VALUE;
    }

    public synchronized int skupaj_spremeniti_velikost() {
        return pomnilnik_območje.length;
    }

    public synchronized int 사용크기() {
        int skupaj_VALUE = 0;
        for (Integer Velikost : 사용영역.values()) {
            skupaj_VALUE += Velikost.intValue();
        }
        return skupaj_VALUE;
    }

    private void preveriti_obseg(int naslov, int Velikost) {
        if (naslov < 0 || Velikost < 0 || naslov > pomnilnik_območje.length - Velikost) {
            throw new IndexOutOfBoundsException("pomnilnik_območje 범위를 벗어났습니다.");
        }
    }
}

