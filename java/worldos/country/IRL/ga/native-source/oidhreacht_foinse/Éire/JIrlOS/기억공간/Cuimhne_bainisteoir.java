// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Éire.JIrlOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 ailínigh_VALUE leithdháil_Stóras, leagan_Stóras, 병합을 담당한다. */
public final class Cuimhne_bainisteoir {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Cuimhne_bainisteoir(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int leithdháil_Stóras(int Méid) {
        return 정렬할당(Méid, 1);
    }

    public synchronized int 정렬할당(int Méid, int ailínigh_VALUE) {
        if (Méid <= 0 || ailínigh_VALUE <= 0 || (ailínigh_VALUE & (ailínigh_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> iontráil_VALUE : 빈영역.entrySet()) {
            int Rith_2 = iontráil_VALUE.getKey().intValue();
            int 영역크기 = iontráil_VALUE.getValue().intValue();
            int 정렬시작 = (Rith_2 + ailínigh_VALUE - 1) & -ailínigh_VALUE;
            int 앞크기 = 정렬시작 - Rith_2;
            int 끝크기 = 영역크기 - 앞크기 - Méid;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Rith_2));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Rith_2), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Méid), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Méid));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Méid, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void leagan_Stóras(int ADDRESS) {
        Integer socraigh_méid_oibiacht = 사용영역.remove(Integer.valueOf(ADDRESS));
        if (socraigh_méid_oibiacht == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Rith_2 = ADDRESS;
        int Méid = socraigh_méid_oibiacht.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Rith_2));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Rith_2) {
            Rith_2 = 앞.getKey().intValue();
            Méid += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Siar_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Rith_2));
        if (Siar_VALUE != null && Rith_2 + Méid == Siar_VALUE.getKey().intValue()) {
            Méid += Siar_VALUE.getValue().intValue();
            빈영역.remove(Siar_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Rith_2), Integer.valueOf(Méid));
    }

    public synchronized byte 바이트읽기(int ADDRESS) {
        범위확인(ADDRESS, 1);
        return 기억공간[ADDRESS];
    }

    public synchronized void scríobh_beart_VALUE(int ADDRESS, byte VALUE) {
        범위확인(ADDRESS, 1);
        기억공간[ADDRESS] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Méid : 사용영역.values()) {
            합계 += Méid.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ADDRESS, int Méid) {
        if (ADDRESS < 0 || Méid < 0 || ADDRESS > 기억공간.length - Méid) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

