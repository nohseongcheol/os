// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 መስመር_ኣትሕዝ_ዋጋ ምምዳብ_መኽዘን, ፍታሕ_መኽዘን, 병합을 담당한다. */
public final class ማህደር_ዝኽረት_ኣካያዲ {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ማህደር_ዝኽረት_ኣካያዲ(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int ምምዳብ_መኽዘን(int መጠን) {
        return 정렬할당(መጠን, 1);
    }

    public synchronized int 정렬할당(int መጠን, int መስመር_ኣትሕዝ_ዋጋ) {
        if (መጠን <= 0 || መስመር_ኣትሕዝ_ዋጋ <= 0 || (መስመር_ኣትሕዝ_ዋጋ & (መስመር_ኣትሕዝ_ዋጋ - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ምእታው_ዋጋ : 빈영역.entrySet()) {
            int ኣኺድ = ምእታው_ዋጋ.getKey().intValue();
            int 영역크기 = ምእታው_ዋጋ.getValue().intValue();
            int 정렬시작 = (ኣኺድ + መስመር_ኣትሕዝ_ዋጋ - 1) & -መስመር_ኣትሕዝ_ዋጋ;
            int 앞크기 = 정렬시작 - ኣኺድ;
            int 끝크기 = 영역크기 - 앞크기 - መጠን;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ኣኺድ));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ኣኺድ), Integer.valueOf(앞크기));
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

    public synchronized void ፍታሕ_መኽዘን(int ኣድራሻ) {
        Integer መጠን_ነገር = 사용영역.remove(Integer.valueOf(ኣድራሻ));
        if (መጠን_ነገር == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ኣኺድ = ኣድራሻ;
        int መጠን = መጠን_ነገር.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ኣኺድ));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ኣኺድ) {
            ኣኺድ = 앞.getKey().intValue();
            መጠን += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> ድሕሪት_ዋጋ = 빈영역.ceilingEntry(Integer.valueOf(ኣኺድ));
        if (ድሕሪት_ዋጋ != null && ኣኺድ + መጠን == ድሕሪት_ዋጋ.getKey().intValue()) {
            መጠን += ድሕሪት_ዋጋ.getValue().intValue();
            빈영역.remove(ድሕሪት_ዋጋ.getKey());
        }
        빈영역.put(Integer.valueOf(ኣኺድ), Integer.valueOf(መጠን));
    }

    public synchronized byte 바이트읽기(int ኣድራሻ) {
        범위확인(ኣድራሻ, 1);
        return 기억공간[ኣድራሻ];
    }

    public synchronized void ጸሓፍ_ባይት_ዋጋ(int ኣድራሻ, byte ዋጋ) {
        범위확인(ኣድራሻ, 1);
        기억공간[ኣድራሻ] = ዋጋ;
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

    private void 범위확인(int ኣድራሻ, int መጠን) {
        if (ኣድራሻ < 0 || መጠን < 0 || ኣድራሻ > 기억공간.length - መጠን) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

