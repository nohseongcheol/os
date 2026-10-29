// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Түркия.JTurOS.Жад_аумақ;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 туралау_мән бекіту_Жад, шығарылым_Жад, 병합을 담당한다. */
public final class Жад_менеджер {
    private final byte[] Жад_аумақ;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Жад_менеджер(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Жад_аумақ = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int бекіту_Жад(int Өлшемі) {
        return 정렬할당(Өлшемі, 1);
    }

    public synchronized int 정렬할당(int Өлшемі, int туралау_мән) {
        if (Өлшемі <= 0 || туралау_мән <= 0 || (туралау_мән & (туралау_мән - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> енгізу_мән : 빈영역.entrySet()) {
            int Орындау_2 = енгізу_мән.getKey().intValue();
            int аумақ_өлшемді_өзгерту = енгізу_мән.getValue().intValue();
            int 정렬시작 = (Орындау_2 + туралау_мән - 1) & -туралау_мән;
            int алдыңғы_камера_мән_өлшемді_өзгерту = 정렬시작 - Орындау_2;
            int 끝크기 = аумақ_өлшемді_өзгерту - алдыңғы_камера_мән_өлшемді_өзгерту - Өлшемі;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Орындау_2));
            if (алдыңғы_камера_мән_өлшемді_өзгерту > 0) {
                빈영역.put(Integer.valueOf(Орындау_2), Integer.valueOf(алдыңғы_камера_мән_өлшемді_өзгерту));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Өлшемі), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Өлшемі));
            Arrays.fill(Жад_аумақ, 정렬시작, 정렬시작 + Өлшемі, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void шығарылым_Жад(int мекенжай) {
        Integer өлшемді_өзгерту_нысан = 사용영역.remove(Integer.valueOf(мекенжай));
        if (өлшемді_өзгерту_нысан == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Орындау_2 = мекенжай;
        int Өлшемі = өлшемді_өзгерту_нысан.intValue();
        Map.Entry<Integer, Integer> алдыңғы_камера_мән = 빈영역.lowerEntry(Integer.valueOf(Орындау_2));
        if (алдыңғы_камера_мән != null && алдыңғы_камера_мән.getKey().intValue() + алдыңғы_камера_мән.getValue().intValue() == Орындау_2) {
            Орындау_2 = алдыңғы_камера_мән.getKey().intValue();
            Өлшемі += алдыңғы_камера_мән.getValue().intValue();
            빈영역.remove(алдыңғы_камера_мән.getKey());
        }
        Map.Entry<Integer, Integer> АРТҚА_мән = 빈영역.ceilingEntry(Integer.valueOf(Орындау_2));
        if (АРТҚА_мән != null && Орындау_2 + Өлшемі == АРТҚА_мән.getKey().intValue()) {
            Өлшемі += АРТҚА_мән.getValue().intValue();
            빈영역.remove(АРТҚА_мән.getKey());
        }
        빈영역.put(Integer.valueOf(Орындау_2), Integer.valueOf(Өлшемі));
    }

    public synchronized byte 바이트읽기(int мекенжай) {
        чек_ауқым(мекенжай, 1);
        return Жад_аумақ[мекенжай];
    }

    public synchronized void жазу_байт_мән(int мекенжай, byte мән) {
        чек_ауқым(мекенжай, 1);
        Жад_аумақ[мекенжай] = мән;
    }

    public synchronized int 전체크기() {
        return Жад_аумақ.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Өлшемі : 사용영역.values()) {
            합계 += Өлшемі.intValue();
        }
        return 합계;
    }

    private void чек_ауқым(int мекенжай, int Өлшемі) {
        if (мекенжай < 0 || Өлшемі < 0 || мекенжай > Жад_аумақ.length - Өлшемі) {
            throw new IndexOutOfBoundsException("Жад_аумақ 범위를 벗어났습니다.");
        }
    }
}

