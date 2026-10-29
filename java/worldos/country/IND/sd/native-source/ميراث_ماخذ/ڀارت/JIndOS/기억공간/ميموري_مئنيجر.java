// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ڀارت.JIndOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 سڌو_قدر مختص_ڪريو_ذخيرو, جاري_ڪريو_ذخيرو, 병합을 담당한다. */
public final class ميموري_مئنيجر {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ميموري_مئنيجر(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int مختص_ڪريو_ذخيرو(int سائيز) {
        return 정렬할당(سائيز, 1);
    }

    public synchronized int 정렬할당(int سائيز, int سڌو_قدر) {
        if (سائيز <= 0 || سڌو_قدر <= 0 || (سڌو_قدر & (سڌو_قدر - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> داخلا_قدر : 빈영역.entrySet()) {
            int هلائڻ = داخلا_قدر.getKey().intValue();
            int 영역크기 = داخلا_قدر.getValue().intValue();
            int 정렬시작 = (هلائڻ + سڌو_قدر - 1) & -سڌو_قدر;
            int 앞크기 = 정렬시작 - هلائڻ;
            int 끝크기 = 영역크기 - 앞크기 - سائيز;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(هلائڻ));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(هلائڻ), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + سائيز), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(سائيز));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + سائيز, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void جاري_ڪريو_ذخيرو(int پتو) {
        Integer سائيز_عنصر = 사용영역.remove(Integer.valueOf(پتو));
        if (سائيز_عنصر == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int هلائڻ = پتو;
        int سائيز = سائيز_عنصر.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(هلائڻ));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == هلائڻ) {
            هلائڻ = 앞.getKey().intValue();
            سائيز += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> واپس_قدر = 빈영역.ceilingEntry(Integer.valueOf(هلائڻ));
        if (واپس_قدر != null && هلائڻ + سائيز == واپس_قدر.getKey().intValue()) {
            سائيز += واپس_قدر.getValue().intValue();
            빈영역.remove(واپس_قدر.getKey());
        }
        빈영역.put(Integer.valueOf(هلائڻ), Integer.valueOf(سائيز));
    }

    public synchronized byte 바이트읽기(int پتو) {
        범위확인(پتو, 1);
        return 기억공간[پتو];
    }

    public synchronized void لکو_بائٽ_قدر(int پتو, byte قدر) {
        범위확인(پتو, 1);
        기억공간[پتو] = قدر;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer سائيز : 사용영역.values()) {
            합계 += سائيز.intValue();
        }
        return 합계;
    }

    private void 범위확인(int پتو, int سائيز) {
        if (پتو < 0 || سائيز < 0 || پتو > 기억공간.length - سائيز) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

