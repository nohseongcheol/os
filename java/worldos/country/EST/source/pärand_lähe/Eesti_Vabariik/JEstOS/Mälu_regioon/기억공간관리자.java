// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.Mälu_regioon;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 joondama_VALUE lisama_salvesti, vabastama_salvesti, 병합을 담당한다. */
public final class 기억공간관리자 {
    private final byte[] Mälu_regioon;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public 기억공간관리자(int kokku_suurust_muutma) {
        if (kokku_suurust_muutma < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Mälu_regioon = new byte[kokku_suurust_muutma];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(kokku_suurust_muutma - 4096));
    }

    public synchronized int lisama_salvesti(int Suurus) {
        return 정렬할당(Suurus, 1);
    }

    public synchronized int 정렬할당(int Suurus, int joondama_VALUE) {
        if (Suurus <= 0 || joondama_VALUE <= 0 || (joondama_VALUE & (joondama_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> kirje_VALUE : 빈영역.entrySet()) {
            int Käivita_2 = kirje_VALUE.getKey().intValue();
            int regioon_suurust_muutma = kirje_VALUE.getValue().intValue();
            int 정렬시작 = (Käivita_2 + joondama_VALUE - 1) & -joondama_VALUE;
            int esikaamera_VALUE_suurust_muutma = 정렬시작 - Käivita_2;
            int 끝크기 = regioon_suurust_muutma - esikaamera_VALUE_suurust_muutma - Suurus;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Käivita_2));
            if (esikaamera_VALUE_suurust_muutma > 0) {
                빈영역.put(Integer.valueOf(Käivita_2), Integer.valueOf(esikaamera_VALUE_suurust_muutma));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Suurus), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Suurus));
            Arrays.fill(Mälu_regioon, 정렬시작, 정렬시작 + Suurus, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void vabastama_salvesti(int ADDRESS) {
        Integer suurust_muutma_objekt = 사용영역.remove(Integer.valueOf(ADDRESS));
        if (suurust_muutma_objekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Käivita_2 = ADDRESS;
        int Suurus = suurust_muutma_objekt.intValue();
        Map.Entry<Integer, Integer> esikaamera_VALUE = 빈영역.lowerEntry(Integer.valueOf(Käivita_2));
        if (esikaamera_VALUE != null && esikaamera_VALUE.getKey().intValue() + esikaamera_VALUE.getValue().intValue() == Käivita_2) {
            Käivita_2 = esikaamera_VALUE.getKey().intValue();
            Suurus += esikaamera_VALUE.getValue().intValue();
            빈영역.remove(esikaamera_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> Tagasi_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Käivita_2));
        if (Tagasi_VALUE != null && Käivita_2 + Suurus == Tagasi_VALUE.getKey().intValue()) {
            Suurus += Tagasi_VALUE.getValue().intValue();
            빈영역.remove(Tagasi_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Käivita_2), Integer.valueOf(Suurus));
    }

    public synchronized byte 바이트읽기(int ADDRESS) {
        tšekk_vahemik(ADDRESS, 1);
        return Mälu_regioon[ADDRESS];
    }

    public synchronized void kirjutamine_bait_VALUE(int ADDRESS, byte VALUE) {
        tšekk_vahemik(ADDRESS, 1);
        Mälu_regioon[ADDRESS] = VALUE;
    }

    public synchronized int kokku_suurust_muutma() {
        return Mälu_regioon.length;
    }

    public synchronized int 사용크기() {
        int kokku_VALUE = 0;
        for (Integer Suurus : 사용영역.values()) {
            kokku_VALUE += Suurus.intValue();
        }
        return kokku_VALUE;
    }

    private void tšekk_vahemik(int ADDRESS, int Suurus) {
        if (ADDRESS < 0 || Suurus < 0 || ADDRESS > Mälu_regioon.length - Suurus) {
            throw new IndexOutOfBoundsException("Mälu_regioon 범위를 벗어났습니다.");
        }
    }
}

