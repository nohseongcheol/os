// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 justere_VALUE tildele_Lagring, frigi_Lagring, 병합을 담당한다. */
public final class Minne_leiar {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Minne_leiar(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int tildele_Lagring(int Storleik) {
        return 정렬할당(Storleik, 1);
    }

    public synchronized int 정렬할당(int Storleik, int justere_VALUE) {
        if (Storleik <= 0 || justere_VALUE <= 0 || (justere_VALUE & (justere_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> oppføring_VALUE : 빈영역.entrySet()) {
            int Køyr_2 = oppføring_VALUE.getKey().intValue();
            int 영역크기 = oppføring_VALUE.getValue().intValue();
            int 정렬시작 = (Køyr_2 + justere_VALUE - 1) & -justere_VALUE;
            int 앞크기 = 정렬시작 - Køyr_2;
            int 끝크기 = 영역크기 - 앞크기 - Storleik;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Køyr_2));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Køyr_2), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Storleik), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Storleik));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Storleik, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void frigi_Lagring(int ADDRESS) {
        Integer endre_storleik_objekt = 사용영역.remove(Integer.valueOf(ADDRESS));
        if (endre_storleik_objekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Køyr_2 = ADDRESS;
        int Storleik = endre_storleik_objekt.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Køyr_2));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Køyr_2) {
            Køyr_2 = 앞.getKey().intValue();
            Storleik += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> TILBAKE_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Køyr_2));
        if (TILBAKE_VALUE != null && Køyr_2 + Storleik == TILBAKE_VALUE.getKey().intValue()) {
            Storleik += TILBAKE_VALUE.getValue().intValue();
            빈영역.remove(TILBAKE_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Køyr_2), Integer.valueOf(Storleik));
    }

    public synchronized byte 바이트읽기(int ADDRESS) {
        범위확인(ADDRESS, 1);
        return 기억공간[ADDRESS];
    }

    public synchronized void skrive_byte_VALUE(int ADDRESS, byte VALUE) {
        범위확인(ADDRESS, 1);
        기억공간[ADDRESS] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Storleik : 사용영역.values()) {
            합계 += Storleik.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ADDRESS, int Storleik) {
        if (ADDRESS < 0 || Storleik < 0 || ADDRESS > 기억공간.length - Storleik) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

