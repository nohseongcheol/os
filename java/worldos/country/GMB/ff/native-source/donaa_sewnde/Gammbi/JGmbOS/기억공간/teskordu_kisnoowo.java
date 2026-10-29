// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gammbi.JGmbOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 fonndude_njaru 할당, 해제, 병합을 담당한다. */
public final class teskordu_kisnoowo {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public teskordu_kisnoowo(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int 할당(int waylude_etannde) {
        return 정렬할당(waylude_etannde, 1);
    }

    public synchronized int 정렬할당(int waylude_etannde, int fonndude_njaru) {
        if (waylude_etannde <= 0 || fonndude_njaru <= 0 || (fonndude_njaru & (fonndude_njaru - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> naatnugol_njaru : 빈영역.entrySet()) {
            int huutoraade = naatnugol_njaru.getKey().intValue();
            int 영역크기 = naatnugol_njaru.getValue().intValue();
            int 정렬시작 = (huutoraade + fonndude_njaru - 1) & -fonndude_njaru;
            int 앞크기 = 정렬시작 - huutoraade;
            int 끝크기 = 영역크기 - 앞크기 - waylude_etannde;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(huutoraade));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(huutoraade), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + waylude_etannde), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(waylude_etannde));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + waylude_etannde, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void 해제(int ñiiɓirde) {
        Integer waylude_etannde_huunde = 사용영역.remove(Integer.valueOf(ñiiɓirde));
        if (waylude_etannde_huunde == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int huutoraade = ñiiɓirde;
        int waylude_etannde = waylude_etannde_huunde.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(huutoraade));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == huutoraade) {
            huutoraade = 앞.getKey().intValue();
            waylude_etannde += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Caggal_njaru = 빈영역.ceilingEntry(Integer.valueOf(huutoraade));
        if (Caggal_njaru != null && huutoraade + waylude_etannde == Caggal_njaru.getKey().intValue()) {
            waylude_etannde += Caggal_njaru.getValue().intValue();
            빈영역.remove(Caggal_njaru.getKey());
        }
        빈영역.put(Integer.valueOf(huutoraade), Integer.valueOf(waylude_etannde));
    }

    public synchronized byte 바이트읽기(int ñiiɓirde) {
        범위확인(ñiiɓirde, 1);
        return 기억공간[ñiiɓirde];
    }

    public synchronized void winndude_oktee_njaru(int ñiiɓirde, byte njaru) {
        범위확인(ñiiɓirde, 1);
        기억공간[ñiiɓirde] = njaru;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer waylude_etannde : 사용영역.values()) {
            합계 += waylude_etannde.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ñiiɓirde, int waylude_etannde) {
        if (ñiiɓirde < 0 || waylude_etannde < 0 || ñiiɓirde > 기억공간.length - waylude_etannde) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

