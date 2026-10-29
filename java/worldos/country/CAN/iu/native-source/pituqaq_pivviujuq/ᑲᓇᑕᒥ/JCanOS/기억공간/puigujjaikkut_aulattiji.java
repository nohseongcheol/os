// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 nalimutirli_atuutilik 할당, 해제, 병합을 담당한다. */
public final class puigujjaikkut_aulattiji {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public puigujjaikkut_aulattiji(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int 할당(int anininga) {
        return 정렬할당(anininga, 1);
    }

    public synchronized int 정렬할당(int anininga, int nalimutirli_atuutilik) {
        if (anininga <= 0 || nalimutirli_atuutilik <= 0 || (nalimutirli_atuutilik & (nalimutirli_atuutilik - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> Iliniku_atuutilik : 빈영역.entrySet()) {
            int 시작 = Iliniku_atuutilik.getKey().intValue();
            int 영역크기 = Iliniku_atuutilik.getValue().intValue();
            int 정렬시작 = (시작 + nalimutirli_atuutilik - 1) & -nalimutirli_atuutilik;
            int 앞크기 = 정렬시작 - 시작;
            int 끝크기 = 영역크기 - 앞크기 - anininga;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(시작));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(시작), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + anininga), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(anininga));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + anininga, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void 해제(int turaarut) {
        Integer anininga_kisu = 사용영역.remove(Integer.valueOf(turaarut));
        if (anininga_kisu == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int 시작 = turaarut;
        int anininga = anininga_kisu.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(시작));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == 시작) {
            시작 = 앞.getKey().intValue();
            anininga += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Utimut_atuutilik = 빈영역.ceilingEntry(Integer.valueOf(시작));
        if (Utimut_atuutilik != null && 시작 + anininga == Utimut_atuutilik.getKey().intValue()) {
            anininga += Utimut_atuutilik.getValue().intValue();
            빈영역.remove(Utimut_atuutilik.getKey());
        }
        빈영역.put(Integer.valueOf(시작), Integer.valueOf(anininga));
    }

    public synchronized byte 바이트읽기(int turaarut) {
        범위확인(turaarut, 1);
        return 기억공간[turaarut];
    }

    public synchronized void titiraq_byte_atuutilik(int turaarut, byte atuutilik) {
        범위확인(turaarut, 1);
        기억공간[turaarut] = atuutilik;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer anininga : 사용영역.values()) {
            합계 += anininga.intValue();
        }
        return 합계;
    }

    private void 범위확인(int turaarut, int anininga) {
        if (turaarut < 0 || anininga < 0 || turaarut > 기억공간.length - anininga) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

