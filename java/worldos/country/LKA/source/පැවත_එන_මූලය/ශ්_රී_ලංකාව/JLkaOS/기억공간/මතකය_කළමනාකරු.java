// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 පෙළ_ගස්වන්න_අගය විබෙදන්න_ගබඩාව, මුදාහැරීම_ගබඩාව, 병합을 담당한다. */
public final class මතකය_කළමනාකරු {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public මතකය_කළමනාකරු(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int විබෙදන්න_ගබඩාව(int ප්_රමාණය) {
        return 정렬할당(ප්_රමාණය, 1);
    }

    public synchronized int 정렬할당(int ප්_රමාණය, int පෙළ_ගස්වන්න_අගය) {
        if (ප්_රමාණය <= 0 || පෙළ_ගස්වන්න_අගය <= 0 || (පෙළ_ගස්වන්න_අගය & (පෙළ_ගස්වන්න_අගය - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> පිවිසුම_අගය : 빈영역.entrySet()) {
            int ක්_රියාත්මක_කරන්න_2 = පිවිසුම_අගය.getKey().intValue();
            int 영역크기 = පිවිසුම_අගය.getValue().intValue();
            int 정렬시작 = (ක්_රියාත්මක_කරන්න_2 + පෙළ_ගස්වන්න_අගය - 1) & -පෙළ_ගස්වන්න_අගය;
            int 앞크기 = 정렬시작 - ක්_රියාත්මක_කරන්න_2;
            int 끝크기 = 영역크기 - 앞크기 - ප්_රමාණය;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ක්_රියාත්මක_කරන්න_2));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ක්_රියාත්මක_කරන්න_2), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + ප්_රමාණය), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(ප්_රමාණය));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + ප්_රමාණය, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void මුදාහැරීම_ගබඩාව(int යොමුව) {
        Integer ප්_රමාණනය_වස්තුව = 사용영역.remove(Integer.valueOf(යොමුව));
        if (ප්_රමාණනය_වස්තුව == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ක්_රියාත්මක_කරන්න_2 = යොමුව;
        int ප්_රමාණය = ප්_රමාණනය_වස්තුව.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ක්_රියාත්මක_කරන්න_2));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ක්_රියාත්මක_කරන්න_2) {
            ක්_රියාත්මක_කරන්න_2 = 앞.getKey().intValue();
            ප්_රමාණය += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> ආපසු_අගය = 빈영역.ceilingEntry(Integer.valueOf(ක්_රියාත්මක_කරන්න_2));
        if (ආපසු_අගය != null && ක්_රියාත්මක_කරන්න_2 + ප්_රමාණය == ආපසු_අගය.getKey().intValue()) {
            ප්_රමාණය += ආපසු_අගය.getValue().intValue();
            빈영역.remove(ආපසු_අගය.getKey());
        }
        빈영역.put(Integer.valueOf(ක්_රියාත්මක_කරන්න_2), Integer.valueOf(ප්_රමාණය));
    }

    public synchronized byte 바이트읽기(int යොමුව) {
        범위확인(යොමුව, 1);
        return 기억공간[යොමුව];
    }

    public synchronized void ලියන්න_බයිටය_අගය(int යොමුව, byte අගය) {
        범위확인(යොමුව, 1);
        기억공간[යොමුව] = අගය;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer ප්_රමාණය : 사용영역.values()) {
            합계 += ප්_රමාණය.intValue();
        }
        return 합계;
    }

    private void 범위확인(int යොමුව, int ප්_රමාණය) {
        if (යොමුව < 0 || ප්_රමාණය < 0 || යොමුව > 기억공간.length - ප්_රමාණය) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

