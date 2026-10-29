// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 alignéieren_VALUE zouweisen_Späicher, Versioun_Späicher, 병합을 담당한다. */
public final class Späicher_Manager {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Späicher_Manager(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int zouweisen_Späicher(int d_Gréisst_veränneren) {
        return 정렬할당(d_Gréisst_veränneren, 1);
    }

    public synchronized int 정렬할당(int d_Gréisst_veränneren, int alignéieren_VALUE) {
        if (d_Gréisst_veränneren <= 0 || alignéieren_VALUE <= 0 || (alignéieren_VALUE & (alignéieren_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> Agab_VALUE : 빈영역.entrySet()) {
            int Laf = Agab_VALUE.getKey().intValue();
            int 영역크기 = Agab_VALUE.getValue().intValue();
            int 정렬시작 = (Laf + alignéieren_VALUE - 1) & -alignéieren_VALUE;
            int 앞크기 = 정렬시작 - Laf;
            int 끝크기 = 영역크기 - 앞크기 - d_Gréisst_veränneren;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Laf));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Laf), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + d_Gréisst_veränneren), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(d_Gréisst_veränneren));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + d_Gréisst_veränneren, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void Versioun_Späicher(int Adress) {
        Integer d_Gréisst_veränneren_Objet = 사용영역.remove(Integer.valueOf(Adress));
        if (d_Gréisst_veränneren_Objet == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Laf = Adress;
        int d_Gréisst_veränneren = d_Gréisst_veränneren_Objet.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Laf));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Laf) {
            Laf = 앞.getKey().intValue();
            d_Gréisst_veränneren += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Zeréck_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Laf));
        if (Zeréck_VALUE != null && Laf + d_Gréisst_veränneren == Zeréck_VALUE.getKey().intValue()) {
            d_Gréisst_veränneren += Zeréck_VALUE.getValue().intValue();
            빈영역.remove(Zeréck_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Laf), Integer.valueOf(d_Gréisst_veränneren));
    }

    public synchronized byte 바이트읽기(int Adress) {
        범위확인(Adress, 1);
        return 기억공간[Adress];
    }

    public synchronized void schreiwen_Byte_VALUE(int Adress, byte VALUE) {
        범위확인(Adress, 1);
        기억공간[Adress] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer d_Gréisst_veränneren : 사용영역.values()) {
            합계 += d_Gréisst_veränneren.intValue();
        }
        return 합계;
    }

    private void 범위확인(int Adress, int d_Gréisst_veränneren) {
        if (Adress < 0 || d_Gréisst_veränneren < 0 || Adress > 기억공간.length - d_Gréisst_veränneren) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

