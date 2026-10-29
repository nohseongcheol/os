// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 co_thaobhaich_VALUE sònraich_stòras, sgaoileadh_stòras, 병합을 담당한다. */
public final class cuimhne_manaidsear {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public cuimhne_manaidsear(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int sònraich_stòras(int atharraich_am_meud) {
        return 정렬할당(atharraich_am_meud, 1);
    }

    public synchronized int 정렬할당(int atharraich_am_meud, int co_thaobhaich_VALUE) {
        if (atharraich_am_meud <= 0 || co_thaobhaich_VALUE <= 0 || (co_thaobhaich_VALUE & (co_thaobhaich_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> cur_a_steach_VALUE : 빈영역.entrySet()) {
            int ruith = cur_a_steach_VALUE.getKey().intValue();
            int 영역크기 = cur_a_steach_VALUE.getValue().intValue();
            int 정렬시작 = (ruith + co_thaobhaich_VALUE - 1) & -co_thaobhaich_VALUE;
            int 앞크기 = 정렬시작 - ruith;
            int 끝크기 = 영역크기 - 앞크기 - atharraich_am_meud;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ruith));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ruith), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + atharraich_am_meud), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(atharraich_am_meud));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + atharraich_am_meud, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void sgaoileadh_stòras(int ADDRESS) {
        Integer atharraich_am_meud_nì = 사용영역.remove(Integer.valueOf(ADDRESS));
        if (atharraich_am_meud_nì == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ruith = ADDRESS;
        int atharraich_am_meud = atharraich_am_meud_nì.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ruith));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ruith) {
            ruith = 앞.getKey().intValue();
            atharraich_am_meud += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Air_ais_VALUE = 빈영역.ceilingEntry(Integer.valueOf(ruith));
        if (Air_ais_VALUE != null && ruith + atharraich_am_meud == Air_ais_VALUE.getKey().intValue()) {
            atharraich_am_meud += Air_ais_VALUE.getValue().intValue();
            빈영역.remove(Air_ais_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(ruith), Integer.valueOf(atharraich_am_meud));
    }

    public synchronized byte 바이트읽기(int ADDRESS) {
        범위확인(ADDRESS, 1);
        return 기억공간[ADDRESS];
    }

    public synchronized void sgrìobh_baidht_VALUE(int ADDRESS, byte VALUE) {
        범위확인(ADDRESS, 1);
        기억공간[ADDRESS] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer atharraich_am_meud : 사용영역.values()) {
            합계 += atharraich_am_meud.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ADDRESS, int atharraich_am_meud) {
        if (ADDRESS < 0 || atharraich_am_meud < 0 || ADDRESS > 기억공간.length - atharraich_am_meud) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

