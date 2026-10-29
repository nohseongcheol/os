// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frantzia.JFraOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 lerrokatu_balio esleitu_biltegi, askatu_biltegi, 병합을 담당한다. */
public final class Memoria_kudeatzaile {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memoria_kudeatzaile(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int esleitu_biltegi(int Tamaina) {
        return 정렬할당(Tamaina, 1);
    }

    public synchronized int 정렬할당(int Tamaina, int lerrokatu_balio) {
        if (Tamaina <= 0 || lerrokatu_balio <= 0 || (lerrokatu_balio & (lerrokatu_balio - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> sarrera_balio : 빈영역.entrySet()) {
            int Exekutatu_2 = sarrera_balio.getKey().intValue();
            int 영역크기 = sarrera_balio.getValue().intValue();
            int 정렬시작 = (Exekutatu_2 + lerrokatu_balio - 1) & -lerrokatu_balio;
            int 앞크기 = 정렬시작 - Exekutatu_2;
            int 끝크기 = 영역크기 - 앞크기 - Tamaina;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Exekutatu_2));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Exekutatu_2), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Tamaina), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Tamaina));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Tamaina, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void askatu_biltegi(int helbide) {
        Integer 크기객체 = 사용영역.remove(Integer.valueOf(helbide));
        if (크기객체 == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Exekutatu_2 = helbide;
        int Tamaina = 크기객체.intValue();
        Map.Entry<Integer, Integer> aurrekoa_balio = 빈영역.lowerEntry(Integer.valueOf(Exekutatu_2));
        if (aurrekoa_balio != null && aurrekoa_balio.getKey().intValue() + aurrekoa_balio.getValue().intValue() == Exekutatu_2) {
            Exekutatu_2 = aurrekoa_balio.getKey().intValue();
            Tamaina += aurrekoa_balio.getValue().intValue();
            빈영역.remove(aurrekoa_balio.getKey());
        }
        Map.Entry<Integer, Integer> ATZERA_balio = 빈영역.ceilingEntry(Integer.valueOf(Exekutatu_2));
        if (ATZERA_balio != null && Exekutatu_2 + Tamaina == ATZERA_balio.getKey().intValue()) {
            Tamaina += ATZERA_balio.getValue().intValue();
            빈영역.remove(ATZERA_balio.getKey());
        }
        빈영역.put(Integer.valueOf(Exekutatu_2), Integer.valueOf(Tamaina));
    }

    public synchronized byte 바이트읽기(int helbide) {
        txeke_barruti(helbide, 1);
        return 기억공간[helbide];
    }

    public synchronized void idatzi_byte_balio(int helbide, byte balio) {
        txeke_barruti(helbide, 1);
        기억공간[helbide] = balio;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Tamaina : 사용영역.values()) {
            합계 += Tamaina.intValue();
        }
        return 합계;
    }

    private void txeke_barruti(int helbide, int Tamaina) {
        if (helbide < 0 || Tamaina < 0 || helbide > 기억공간.length - Tamaina) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

