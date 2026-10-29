// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.Paměť_oblast;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 zarovnat_HODNOTA přidělit_Storage, verze_Storage, 병합을 담당한다. */
public final class Paměť_Správce {
    private final byte[] Paměť_oblast;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Paměť_Správce(int celkem_změnit_velikost) {
        if (celkem_změnit_velikost < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Paměť_oblast = new byte[celkem_změnit_velikost];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(celkem_změnit_velikost - 4096));
    }

    public synchronized int přidělit_Storage(int Velikost) {
        return 정렬할당(Velikost, 1);
    }

    public synchronized int 정렬할당(int Velikost, int zarovnat_HODNOTA) {
        if (Velikost <= 0 || zarovnat_HODNOTA <= 0 || (zarovnat_HODNOTA & (zarovnat_HODNOTA - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> položka_HODNOTA : 빈영역.entrySet()) {
            int Spustit_2 = položka_HODNOTA.getKey().intValue();
            int oblast_změnit_velikost = položka_HODNOTA.getValue().intValue();
            int 정렬시작 = (Spustit_2 + zarovnat_HODNOTA - 1) & -zarovnat_HODNOTA;
            int přední_fotoaparát_HODNOTA_změnit_velikost = 정렬시작 - Spustit_2;
            int 끝크기 = oblast_změnit_velikost - přední_fotoaparát_HODNOTA_změnit_velikost - Velikost;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Spustit_2));
            if (přední_fotoaparát_HODNOTA_změnit_velikost > 0) {
                빈영역.put(Integer.valueOf(Spustit_2), Integer.valueOf(přední_fotoaparát_HODNOTA_změnit_velikost));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Velikost), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Velikost));
            Arrays.fill(Paměť_oblast, 정렬시작, 정렬시작 + Velikost, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void verze_Storage(int Adresa) {
        Integer změnit_velikost_objekt = 사용영역.remove(Integer.valueOf(Adresa));
        if (změnit_velikost_objekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Spustit_2 = Adresa;
        int Velikost = změnit_velikost_objekt.intValue();
        Map.Entry<Integer, Integer> přední_fotoaparát_HODNOTA = 빈영역.lowerEntry(Integer.valueOf(Spustit_2));
        if (přední_fotoaparát_HODNOTA != null && přední_fotoaparát_HODNOTA.getKey().intValue() + přední_fotoaparát_HODNOTA.getValue().intValue() == Spustit_2) {
            Spustit_2 = přední_fotoaparát_HODNOTA.getKey().intValue();
            Velikost += přední_fotoaparát_HODNOTA.getValue().intValue();
            빈영역.remove(přední_fotoaparát_HODNOTA.getKey());
        }
        Map.Entry<Integer, Integer> BACK_HODNOTA = 빈영역.ceilingEntry(Integer.valueOf(Spustit_2));
        if (BACK_HODNOTA != null && Spustit_2 + Velikost == BACK_HODNOTA.getKey().intValue()) {
            Velikost += BACK_HODNOTA.getValue().intValue();
            빈영역.remove(BACK_HODNOTA.getKey());
        }
        빈영역.put(Integer.valueOf(Spustit_2), Integer.valueOf(Velikost));
    }

    public synchronized byte 바이트읽기(int Adresa) {
        šek_oblast(Adresa, 1);
        return Paměť_oblast[Adresa];
    }

    public synchronized void zápis_bajt_HODNOTA(int Adresa, byte HODNOTA) {
        šek_oblast(Adresa, 1);
        Paměť_oblast[Adresa] = HODNOTA;
    }

    public synchronized int celkem_změnit_velikost() {
        return Paměť_oblast.length;
    }

    public synchronized int 사용크기() {
        int celkem_HODNOTA = 0;
        for (Integer Velikost : 사용영역.values()) {
            celkem_HODNOTA += Velikost.intValue();
        }
        return celkem_HODNOTA;
    }

    private void šek_oblast(int Adresa, int Velikost) {
        if (Adresa < 0 || Velikost < 0 || Adresa > Paměť_oblast.length - Velikost) {
            throw new IndexOutOfBoundsException("Paměť_oblast 범위를 벗어났습니다.");
        }
    }
}

