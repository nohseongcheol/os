// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.atmiņa_reģions;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 līdzināt_VALUE piešķirt_Krātuve, izlaist_Krātuve, 병합을 담당한다. */
public final class 기억공간관리자 {
    private final byte[] atmiņa_reģions;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public 기억공간관리자(int kopsumma_mainīt_izmērus) {
        if (kopsumma_mainīt_izmērus < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        atmiņa_reģions = new byte[kopsumma_mainīt_izmērus];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(kopsumma_mainīt_izmērus - 4096));
    }

    public synchronized int piešķirt_Krātuve(int Izmērs) {
        return 정렬할당(Izmērs, 1);
    }

    public synchronized int 정렬할당(int Izmērs, int līdzināt_VALUE) {
        if (Izmērs <= 0 || līdzināt_VALUE <= 0 || (līdzināt_VALUE & (līdzināt_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ievade_VALUE : 빈영역.entrySet()) {
            int Palaist = ievade_VALUE.getKey().intValue();
            int reģions_mainīt_izmērus = ievade_VALUE.getValue().intValue();
            int 정렬시작 = (Palaist + līdzināt_VALUE - 1) & -līdzināt_VALUE;
            int priekšējā_VALUE_mainīt_izmērus = 정렬시작 - Palaist;
            int 끝크기 = reģions_mainīt_izmērus - priekšējā_VALUE_mainīt_izmērus - Izmērs;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Palaist));
            if (priekšējā_VALUE_mainīt_izmērus > 0) {
                빈영역.put(Integer.valueOf(Palaist), Integer.valueOf(priekšējā_VALUE_mainīt_izmērus));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Izmērs), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Izmērs));
            Arrays.fill(atmiņa_reģions, 정렬시작, 정렬시작 + Izmērs, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void izlaist_Krātuve(int adrese) {
        Integer mainīt_izmērus_objekts = 사용영역.remove(Integer.valueOf(adrese));
        if (mainīt_izmērus_objekts == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Palaist = adrese;
        int Izmērs = mainīt_izmērus_objekts.intValue();
        Map.Entry<Integer, Integer> priekšējā_VALUE = 빈영역.lowerEntry(Integer.valueOf(Palaist));
        if (priekšējā_VALUE != null && priekšējā_VALUE.getKey().intValue() + priekšējā_VALUE.getValue().intValue() == Palaist) {
            Palaist = priekšējā_VALUE.getKey().intValue();
            Izmērs += priekšējā_VALUE.getValue().intValue();
            빈영역.remove(priekšējā_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> ATPAKAĻ_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Palaist));
        if (ATPAKAĻ_VALUE != null && Palaist + Izmērs == ATPAKAĻ_VALUE.getKey().intValue()) {
            Izmērs += ATPAKAĻ_VALUE.getValue().intValue();
            빈영역.remove(ATPAKAĻ_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Palaist), Integer.valueOf(Izmērs));
    }

    public synchronized byte 바이트읽기(int adrese) {
        čeks_diapazons(adrese, 1);
        return atmiņa_reģions[adrese];
    }

    public synchronized void rakstīšana_byte_VALUE(int adrese, byte VALUE) {
        čeks_diapazons(adrese, 1);
        atmiņa_reģions[adrese] = VALUE;
    }

    public synchronized int kopsumma_mainīt_izmērus() {
        return atmiņa_reģions.length;
    }

    public synchronized int 사용크기() {
        int kopsumma_VALUE = 0;
        for (Integer Izmērs : 사용영역.values()) {
            kopsumma_VALUE += Izmērs.intValue();
        }
        return kopsumma_VALUE;
    }

    private void čeks_diapazons(int adrese, int Izmērs) {
        if (adrese < 0 || Izmērs < 0 || adrese > atmiņa_reģions.length - Izmērs) {
            throw new IndexOutOfBoundsException("atmiņa_reģions 범위를 벗어났습니다.");
        }
    }
}

