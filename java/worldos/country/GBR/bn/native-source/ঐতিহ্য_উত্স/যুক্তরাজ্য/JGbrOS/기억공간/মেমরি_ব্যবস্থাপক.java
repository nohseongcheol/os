// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package যুক্তরাজ্য.JGbrOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 সারিকরণ_করা_মান বন্টন_করা_স্টোরেজ, রিলিজ_স্টোরেজ, 병합을 담당한다. */
public final class মেমরি_ব্যবস্থাপক {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public মেমরি_ব্যবস্থাপক(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int বন্টন_করা_স্টোরেজ(int আকার) {
        return 정렬할당(আকার, 1);
    }

    public synchronized int 정렬할당(int আকার, int সারিকরণ_করা_মান) {
        if (আকার <= 0 || সারিকরণ_করা_মান <= 0 || (সারিকরণ_করা_মান & (সারিকরণ_করা_মান - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ভুক্তি_মান : 빈영역.entrySet()) {
            int চালনা = ভুক্তি_মান.getKey().intValue();
            int 영역크기 = ভুক্তি_মান.getValue().intValue();
            int 정렬시작 = (চালনা + সারিকরণ_করা_মান - 1) & -সারিকরণ_করা_মান;
            int সম্মুখ_মান_আয়তন = 정렬시작 - চালনা;
            int 끝크기 = 영역크기 - সম্মুখ_মান_আয়তন - আকার;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(চালনা));
            if (সম্মুখ_মান_আয়তন > 0) {
                빈영역.put(Integer.valueOf(চালনা), Integer.valueOf(সম্মুখ_মান_আয়তন));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + আকার), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(আকার));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + আকার, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void রিলিজ_স্টোরেজ(int ইমেইল) {
        Integer আয়তন_বস্তু = 사용영역.remove(Integer.valueOf(ইমেইল));
        if (আয়তন_বস্তু == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int চালনা = ইমেইল;
        int আকার = আয়তন_বস্তু.intValue();
        Map.Entry<Integer, Integer> সম্মুখ_মান = 빈영역.lowerEntry(Integer.valueOf(চালনা));
        if (সম্মুখ_মান != null && সম্মুখ_মান.getKey().intValue() + সম্মুখ_মান.getValue().intValue() == চালনা) {
            চালনা = সম্মুখ_মান.getKey().intValue();
            আকার += সম্মুখ_মান.getValue().intValue();
            빈영역.remove(সম্মুখ_মান.getKey());
        }
        Map.Entry<Integer, Integer> ফিরে_যান_মান = 빈영역.ceilingEntry(Integer.valueOf(চালনা));
        if (ফিরে_যান_মান != null && চালনা + আকার == ফিরে_যান_মান.getKey().intValue()) {
            আকার += ফিরে_যান_মান.getValue().intValue();
            빈영역.remove(ফিরে_যান_মান.getKey());
        }
        빈영역.put(Integer.valueOf(চালনা), Integer.valueOf(আকার));
    }

    public synchronized byte 바이트읽기(int ইমেইল) {
        범위확인(ইমেইল, 1);
        return 기억공간[ইমেইল];
    }

    public synchronized void লেখা_বাইট_মান(int ইমেইল, byte মান) {
        범위확인(ইমেইল, 1);
        기억공간[ইমেইল] = মান;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer আকার : 사용영역.values()) {
            합계 += আকার.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ইমেইল, int আকার) {
        if (ইমেইল < 0 || আকার < 0 || ইমেইল > 기억공간.length - আকার) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

