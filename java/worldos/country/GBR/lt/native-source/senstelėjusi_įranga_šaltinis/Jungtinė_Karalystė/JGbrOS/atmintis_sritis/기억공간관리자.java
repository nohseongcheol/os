// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.atmintis_sritis;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 lygiuoti_VALUE priskirti_Saugykla, išleisti_Saugykla, 병합을 담당한다. */
public final class 기억공간관리자 {
    private final byte[] atmintis_sritis;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public 기억공간관리자(int bendras_dydis) {
        if (bendras_dydis < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        atmintis_sritis = new byte[bendras_dydis];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(bendras_dydis - 4096));
    }

    public synchronized int priskirti_Saugykla(int Dydis) {
        return 정렬할당(Dydis, 1);
    }

    public synchronized int 정렬할당(int Dydis, int lygiuoti_VALUE) {
        if (Dydis <= 0 || lygiuoti_VALUE <= 0 || (lygiuoti_VALUE & (lygiuoti_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> įrašas_VALUE : 빈영역.entrySet()) {
            int Paleisti = įrašas_VALUE.getKey().intValue();
            int sritis_dydis = įrašas_VALUE.getValue().intValue();
            int 정렬시작 = (Paleisti + lygiuoti_VALUE - 1) & -lygiuoti_VALUE;
            int priekinis_VALUE_dydis = 정렬시작 - Paleisti;
            int 끝크기 = sritis_dydis - priekinis_VALUE_dydis - Dydis;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Paleisti));
            if (priekinis_VALUE_dydis > 0) {
                빈영역.put(Integer.valueOf(Paleisti), Integer.valueOf(priekinis_VALUE_dydis));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Dydis), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Dydis));
            Arrays.fill(atmintis_sritis, 정렬시작, 정렬시작 + Dydis, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void išleisti_Saugykla(int ADDRESS) {
        Integer dydis_objektas = 사용영역.remove(Integer.valueOf(ADDRESS));
        if (dydis_objektas == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Paleisti = ADDRESS;
        int Dydis = dydis_objektas.intValue();
        Map.Entry<Integer, Integer> priekinis_VALUE = 빈영역.lowerEntry(Integer.valueOf(Paleisti));
        if (priekinis_VALUE != null && priekinis_VALUE.getKey().intValue() + priekinis_VALUE.getValue().intValue() == Paleisti) {
            Paleisti = priekinis_VALUE.getKey().intValue();
            Dydis += priekinis_VALUE.getValue().intValue();
            빈영역.remove(priekinis_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> ATGAL_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Paleisti));
        if (ATGAL_VALUE != null && Paleisti + Dydis == ATGAL_VALUE.getKey().intValue()) {
            Dydis += ATGAL_VALUE.getValue().intValue();
            빈영역.remove(ATGAL_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Paleisti), Integer.valueOf(Dydis));
    }

    public synchronized byte 바이트읽기(int ADDRESS) {
        čekis_diapazonas(ADDRESS, 1);
        return atmintis_sritis[ADDRESS];
    }

    public synchronized void rašymas_baitas_VALUE(int ADDRESS, byte VALUE) {
        čekis_diapazonas(ADDRESS, 1);
        atmintis_sritis[ADDRESS] = VALUE;
    }

    public synchronized int bendras_dydis() {
        return atmintis_sritis.length;
    }

    public synchronized int 사용크기() {
        int bendras_VALUE = 0;
        for (Integer Dydis : 사용영역.values()) {
            bendras_VALUE += Dydis.intValue();
        }
        return bendras_VALUE;
    }

    private void čekis_diapazonas(int ADDRESS, int Dydis) {
        if (ADDRESS < 0 || Dydis < 0 || ADDRESS > atmintis_sritis.length - Dydis) {
            throw new IndexOutOfBoundsException("atmintis_sritis 범위를 벗어났습니다.");
        }
    }
}

