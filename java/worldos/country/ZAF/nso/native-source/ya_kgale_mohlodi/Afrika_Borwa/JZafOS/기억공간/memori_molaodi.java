// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 tsepanya_boleng aba_Bobolokelo, lokolla_Bobolokelo, 병합을 담당한다. */
public final class memori_molaodi {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public memori_molaodi(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int aba_Bobolokelo(int Bogolo) {
        return 정렬할당(Bogolo, 1);
    }

    public synchronized int 정렬할당(int Bogolo, int tsepanya_boleng) {
        if (Bogolo <= 0 || tsepanya_boleng <= 0 || (tsepanya_boleng & (tsepanya_boleng - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> go_tsenya_tshedimošo_boleng : 빈영역.entrySet()) {
            int Diriša = go_tsenya_tshedimošo_boleng.getKey().intValue();
            int 영역크기 = go_tsenya_tshedimošo_boleng.getValue().intValue();
            int 정렬시작 = (Diriša + tsepanya_boleng - 1) & -tsepanya_boleng;
            int 앞크기 = 정렬시작 - Diriša;
            int 끝크기 = 영역크기 - 앞크기 - Bogolo;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Diriša));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Diriša), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Bogolo), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Bogolo));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Bogolo, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void lokolla_Bobolokelo(int atrese) {
        Integer bogolo_selo = 사용영역.remove(Integer.valueOf(atrese));
        if (bogolo_selo == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Diriša = atrese;
        int Bogolo = bogolo_selo.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Diriša));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Diriša) {
            Diriša = 앞.getKey().intValue();
            Bogolo += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Morago_boleng = 빈영역.ceilingEntry(Integer.valueOf(Diriša));
        if (Morago_boleng != null && Diriša + Bogolo == Morago_boleng.getKey().intValue()) {
            Bogolo += Morago_boleng.getValue().intValue();
            빈영역.remove(Morago_boleng.getKey());
        }
        빈영역.put(Integer.valueOf(Diriša), Integer.valueOf(Bogolo));
    }

    public synchronized byte 바이트읽기(int atrese) {
        범위확인(atrese, 1);
        return 기억공간[atrese];
    }

    public synchronized void ngwala_paete_boleng(int atrese, byte boleng) {
        범위확인(atrese, 1);
        기억공간[atrese] = boleng;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Bogolo : 사용영역.values()) {
            합계 += Bogolo.intValue();
        }
        return 합계;
    }

    private void 범위확인(int atrese, int Bogolo) {
        if (atrese < 0 || Bogolo < 0 || atrese > 기억공간.length - Bogolo) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

