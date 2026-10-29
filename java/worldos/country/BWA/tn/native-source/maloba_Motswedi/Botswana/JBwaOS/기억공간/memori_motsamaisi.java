// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 tlhamalatsa_Boleng abela_Polokelo, ntsha_Polokelo, 병합을 담당한다. */
public final class memori_motsamaisi {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public memori_motsamaisi(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int abela_Polokelo(int lekanya) {
        return 정렬할당(lekanya, 1);
    }

    public synchronized int 정렬할당(int lekanya, int tlhamalatsa_Boleng) {
        if (lekanya <= 0 || tlhamalatsa_Boleng <= 0 || (tlhamalatsa_Boleng & (tlhamalatsa_Boleng - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> tsenyo_Boleng : 빈영역.entrySet()) {
            int dirisa = tsenyo_Boleng.getKey().intValue();
            int 영역크기 = tsenyo_Boleng.getValue().intValue();
            int 정렬시작 = (dirisa + tlhamalatsa_Boleng - 1) & -tlhamalatsa_Boleng;
            int 앞크기 = 정렬시작 - dirisa;
            int 끝크기 = 영역크기 - 앞크기 - lekanya;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(dirisa));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(dirisa), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + lekanya), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(lekanya));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + lekanya, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void ntsha_Polokelo(int aterese) {
        Integer lekanya_selwana = 사용영역.remove(Integer.valueOf(aterese));
        if (lekanya_selwana == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int dirisa = aterese;
        int lekanya = lekanya_selwana.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(dirisa));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == dirisa) {
            dirisa = 앞.getKey().intValue();
            lekanya += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Morago_Boleng = 빈영역.ceilingEntry(Integer.valueOf(dirisa));
        if (Morago_Boleng != null && dirisa + lekanya == Morago_Boleng.getKey().intValue()) {
            lekanya += Morago_Boleng.getValue().intValue();
            빈영역.remove(Morago_Boleng.getKey());
        }
        빈영역.put(Integer.valueOf(dirisa), Integer.valueOf(lekanya));
    }

    public synchronized byte 바이트읽기(int aterese) {
        범위확인(aterese, 1);
        return 기억공간[aterese];
    }

    public synchronized void kwala_baete_Boleng(int aterese, byte Boleng) {
        범위확인(aterese, 1);
        기억공간[aterese] = Boleng;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer lekanya : 사용영역.values()) {
            합계 += lekanya.intValue();
        }
        return 합계;
    }

    private void 범위확인(int aterese, int lekanya) {
        if (aterese < 0 || lekanya < 0 || aterese > 기억공간.length - lekanya) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

