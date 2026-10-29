// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.Pamäť_oblasť;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 zarovnať_VALUE vyhradiť_Úložisko, vydať_Úložisko, 병합을 담당한다. */
public final class 기억공간관리자 {
    private final byte[] Pamäť_oblasť;
    private final TreeMap<Integer, Integer> prázdny_oblasť = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public 기억공간관리자(int celkovo_zmeniť_veľkosť) {
        if (celkovo_zmeniť_veľkosť < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Pamäť_oblasť = new byte[celkovo_zmeniť_veľkosť];
        prázdny_oblasť.put(Integer.valueOf(4096), Integer.valueOf(celkovo_zmeniť_veľkosť - 4096));
    }

    public synchronized int vyhradiť_Úložisko(int Veľkosť) {
        return 정렬할당(Veľkosť, 1);
    }

    public synchronized int 정렬할당(int Veľkosť, int zarovnať_VALUE) {
        if (Veľkosť <= 0 || zarovnať_VALUE <= 0 || (zarovnať_VALUE & (zarovnať_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> položka_VALUE : prázdny_oblasť.entrySet()) {
            int Spustiť_2 = položka_VALUE.getKey().intValue();
            int oblasť_zmeniť_veľkosť = položka_VALUE.getValue().intValue();
            int 정렬시작 = (Spustiť_2 + zarovnať_VALUE - 1) & -zarovnať_VALUE;
            int predný_VALUE_zmeniť_veľkosť = 정렬시작 - Spustiť_2;
            int 끝크기 = oblasť_zmeniť_veľkosť - predný_VALUE_zmeniť_veľkosť - Veľkosť;
            if (끝크기 < 0) {
                continue;
            }
            prázdny_oblasť.remove(Integer.valueOf(Spustiť_2));
            if (predný_VALUE_zmeniť_veľkosť > 0) {
                prázdny_oblasť.put(Integer.valueOf(Spustiť_2), Integer.valueOf(predný_VALUE_zmeniť_veľkosť));
            }
            if (끝크기 > 0) {
                prázdny_oblasť.put(Integer.valueOf(정렬시작 + Veľkosť), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Veľkosť));
            Arrays.fill(Pamäť_oblasť, 정렬시작, 정렬시작 + Veľkosť, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void vydať_Úložisko(int adresa) {
        Integer zmeniť_veľkosť_objekt = 사용영역.remove(Integer.valueOf(adresa));
        if (zmeniť_veľkosť_objekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Spustiť_2 = adresa;
        int Veľkosť = zmeniť_veľkosť_objekt.intValue();
        Map.Entry<Integer, Integer> predný_VALUE = prázdny_oblasť.lowerEntry(Integer.valueOf(Spustiť_2));
        if (predný_VALUE != null && predný_VALUE.getKey().intValue() + predný_VALUE.getValue().intValue() == Spustiť_2) {
            Spustiť_2 = predný_VALUE.getKey().intValue();
            Veľkosť += predný_VALUE.getValue().intValue();
            prázdny_oblasť.remove(predný_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> BACK_VALUE = prázdny_oblasť.ceilingEntry(Integer.valueOf(Spustiť_2));
        if (BACK_VALUE != null && Spustiť_2 + Veľkosť == BACK_VALUE.getKey().intValue()) {
            Veľkosť += BACK_VALUE.getValue().intValue();
            prázdny_oblasť.remove(BACK_VALUE.getKey());
        }
        prázdny_oblasť.put(Integer.valueOf(Spustiť_2), Integer.valueOf(Veľkosť));
    }

    public synchronized byte 바이트읽기(int adresa) {
        skontrolovať_rozsah(adresa, 1);
        return Pamäť_oblasť[adresa];
    }

    public synchronized void zapísať_Byte_VALUE(int adresa, byte VALUE) {
        skontrolovať_rozsah(adresa, 1);
        Pamäť_oblasť[adresa] = VALUE;
    }

    public synchronized int celkovo_zmeniť_veľkosť() {
        return Pamäť_oblasť.length;
    }

    public synchronized int 사용크기() {
        int celkovo_VALUE = 0;
        for (Integer Veľkosť : 사용영역.values()) {
            celkovo_VALUE += Veľkosť.intValue();
        }
        return celkovo_VALUE;
    }

    private void skontrolovať_rozsah(int adresa, int Veľkosť) {
        if (adresa < 0 || Veľkosť < 0 || adresa > Pamäť_oblasť.length - Veľkosť) {
            throw new IndexOutOfBoundsException("Pamäť_oblasť 범위를 벗어났습니다.");
        }
    }
}

