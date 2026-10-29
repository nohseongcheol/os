// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 አሰልፍ_እሴት መደብ_ማከማቻ, ልቀቅ_ማከማቻ, 병합을 담당한다. */
public final class ማስቀመጫ_አስተዳዳሪ {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ማስቀመጫ_አስተዳዳሪ(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int መደብ_ማከማቻ(int መጠን) {
        return 정렬할당(መጠን, 1);
    }

    public synchronized int 정렬할당(int መጠን, int አሰልፍ_እሴት) {
        if (መጠን <= 0 || አሰልፍ_እሴት <= 0 || (አሰልፍ_እሴት & (አሰልፍ_እሴት - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ምዝግብ_እሴት : 빈영역.entrySet()) {
            int ማስኬጃ = ምዝግብ_እሴት.getKey().intValue();
            int 영역크기 = ምዝግብ_እሴት.getValue().intValue();
            int 정렬시작 = (ማስኬጃ + አሰልፍ_እሴት - 1) & -አሰልፍ_እሴት;
            int ፊት_እሴት_መጠን_ቀይር = 정렬시작 - ማስኬጃ;
            int 끝크기 = 영역크기 - ፊት_እሴት_መጠን_ቀይር - መጠን;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ማስኬጃ));
            if (ፊት_እሴት_መጠን_ቀይር > 0) {
                빈영역.put(Integer.valueOf(ማስኬጃ), Integer.valueOf(ፊት_እሴት_መጠን_ቀይር));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + መጠን), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(መጠን));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + መጠን, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void ልቀቅ_ማከማቻ(int አድራሻ) {
        Integer መጠን_ቀይር_ነገር = 사용영역.remove(Integer.valueOf(አድራሻ));
        if (መጠን_ቀይር_ነገር == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ማስኬጃ = አድራሻ;
        int መጠን = መጠን_ቀይር_ነገር.intValue();
        Map.Entry<Integer, Integer> ፊት_እሴት = 빈영역.lowerEntry(Integer.valueOf(ማስኬጃ));
        if (ፊት_እሴት != null && ፊት_እሴት.getKey().intValue() + ፊት_እሴት.getValue().intValue() == ማስኬጃ) {
            ማስኬጃ = ፊት_እሴት.getKey().intValue();
            መጠን += ፊት_እሴት.getValue().intValue();
            빈영역.remove(ፊት_እሴት.getKey());
        }
        Map.Entry<Integer, Integer> ተመለስ_እሴት = 빈영역.ceilingEntry(Integer.valueOf(ማስኬጃ));
        if (ተመለስ_እሴት != null && ማስኬጃ + መጠን == ተመለስ_እሴት.getKey().intValue()) {
            መጠን += ተመለስ_እሴት.getValue().intValue();
            빈영역.remove(ተመለስ_እሴት.getKey());
        }
        빈영역.put(Integer.valueOf(ማስኬጃ), Integer.valueOf(መጠን));
    }

    public synchronized byte 바이트읽기(int አድራሻ) {
        범위확인(አድራሻ, 1);
        return 기억공간[አድራሻ];
    }

    public synchronized void ጻፍ_ባይት_እሴት(int አድራሻ, byte እሴት) {
        범위확인(አድራሻ, 1);
        기억공간[አድራሻ] = እሴት;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer መጠን : 사용영역.values()) {
            합계 += መጠን.intValue();
        }
        return 합계;
    }

    private void 범위확인(int አድራሻ, int መጠን) {
        if (አድራሻ < 0 || መጠን < 0 || አድራሻ > 기억공간.length - መጠን) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

