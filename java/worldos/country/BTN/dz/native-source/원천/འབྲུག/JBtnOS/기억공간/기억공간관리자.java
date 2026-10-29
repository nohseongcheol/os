// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package འབྲུག.JBtnOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 정렬 할당, 해제, 병합을 담당한다. */
public final class 기억공간관리자 {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public 기억공간관리자(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int 할당(int ཚད) {
        return 정렬할당(ཚད, 1);
    }

    public synchronized int 정렬할당(int ཚད, int 정렬) {
        if (ཚད <= 0 || 정렬 <= 0 || (정렬 & (정렬 - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> 항목 : 빈영역.entrySet()) {
            int གཡོག_བཀོལ = 항목.getKey().intValue();
            int 영역크기 = 항목.getValue().intValue();
            int 정렬시작 = (གཡོག_བཀོལ + 정렬 - 1) & -정렬;
            int 앞크기 = 정렬시작 - གཡོག_བཀོལ;
            int 끝크기 = 영역크기 - 앞크기 - ཚད;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(གཡོག_བཀོལ));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(གཡོག_བཀོལ), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + ཚད), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(ཚད));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + ཚད, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void 해제(int 주소) {
        Integer 크기객체 = 사용영역.remove(Integer.valueOf(주소));
        if (크기객체 == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int གཡོག_བཀོལ = 주소;
        int ཚད = 크기객체.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(གཡོག_བཀོལ));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == གཡོག_བཀོལ) {
            གཡོག_བཀོལ = 앞.getKey().intValue();
            ཚད += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> 뒤 = 빈영역.ceilingEntry(Integer.valueOf(གཡོག_བཀོལ));
        if (뒤 != null && གཡོག_བཀོལ + ཚད == 뒤.getKey().intValue()) {
            ཚད += 뒤.getValue().intValue();
            빈영역.remove(뒤.getKey());
        }
        빈영역.put(Integer.valueOf(གཡོག_བཀོལ), Integer.valueOf(ཚད));
    }

    public synchronized byte 바이트읽기(int 주소) {
        범위확인(주소, 1);
        return 기억공간[주소];
    }

    public synchronized void 바이트쓰기(int 주소, byte 값) {
        범위확인(주소, 1);
        기억공간[주소] = 값;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer ཚད : 사용영역.values()) {
            합계 += ཚད.intValue();
        }
        return 합계;
    }

    private void 범위확인(int 주소, int ཚད) {
        if (주소 < 0 || ཚད < 0 || 주소 > 기억공간.length - ཚད) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

