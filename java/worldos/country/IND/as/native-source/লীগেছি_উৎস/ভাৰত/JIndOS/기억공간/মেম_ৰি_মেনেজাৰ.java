// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 সংৰেখন_কৰক_মান আৱণ্টন_ষ্ট_ৰেজ, ৰিলিজ_ষ্ট_ৰেজ, 병합을 담당한다. */
public final class মেম_ৰি_মেনেজাৰ {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public মেম_ৰি_মেনেজাৰ(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int আৱণ্টন_ষ্ট_ৰেজ(int মাপ) {
        return 정렬할당(মাপ, 1);
    }

    public synchronized int 정렬할당(int মাপ, int সংৰেখন_কৰক_মান) {
        if (মাপ <= 0 || সংৰেখন_কৰক_মান <= 0 || (সংৰেখন_কৰক_মান & (সংৰেখন_কৰক_মান - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> প্রবিষ্ট_মান : 빈영역.entrySet()) {
            int সঞ্চালন = প্রবিষ্ট_মান.getKey().intValue();
            int 영역크기 = প্রবিষ্ট_মান.getValue().intValue();
            int 정렬시작 = (সঞ্চালন + সংৰেখন_কৰক_মান - 1) & -সংৰেখন_কৰক_মান;
            int 앞크기 = 정렬시작 - সঞ্চালন;
            int 끝크기 = 영역크기 - 앞크기 - মাপ;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(সঞ্চালন));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(সঞ্চালন), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + মাপ), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(মাপ));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + মাপ, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void ৰিলিজ_ষ্ট_ৰেজ(int ঠিকনা) {
        Integer আকাৰ_কৰক_অবজেক্ট = 사용영역.remove(Integer.valueOf(ঠিকনা));
        if (আকাৰ_কৰক_অবজেক্ট == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int সঞ্চালন = ঠিকনা;
        int মাপ = আকাৰ_কৰক_অবজেক্ট.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(সঞ্চালন));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == সঞ্চালন) {
            সঞ্চালন = 앞.getKey().intValue();
            মাপ += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> পাছলৈ_মান = 빈영역.ceilingEntry(Integer.valueOf(সঞ্চালন));
        if (পাছলৈ_মান != null && সঞ্চালন + মাপ == পাছলৈ_মান.getKey().intValue()) {
            মাপ += পাছলৈ_মান.getValue().intValue();
            빈영역.remove(পাছলৈ_মান.getKey());
        }
        빈영역.put(Integer.valueOf(সঞ্চালন), Integer.valueOf(মাপ));
    }

    public synchronized byte 바이트읽기(int ঠিকনা) {
        범위확인(ঠিকনা, 1);
        return 기억공간[ঠিকনা];
    }

    public synchronized void লিখক_বাইট_মান(int ঠিকনা, byte মান) {
        범위확인(ঠিকনা, 1);
        기억공간[ঠিকনা] = মান;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer মাপ : 사용영역.values()) {
            합계 += মাপ.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ঠিকনা, int মাপ) {
        if (ঠিকনা < 0 || মাপ < 0 || ঠিকনা > 기억공간.length - মাপ) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

