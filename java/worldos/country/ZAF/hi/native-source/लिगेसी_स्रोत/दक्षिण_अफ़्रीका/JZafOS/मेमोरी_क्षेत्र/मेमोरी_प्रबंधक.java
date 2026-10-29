// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package दक्षिण_अफ़्रीका.JZafOS.मेमोरी_क्षेत्र;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 संरेखित_करें_मान आवंटित_करें_संग्रहण, रिलीज़_संग्रहण, 병합을 담당한다. */
public final class मेमोरी_प्रबंधक {
    private final byte[] मेमोरी_क्षेत्र;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public मेमोरी_प्रबंधक(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        मेमोरी_क्षेत्र = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int आवंटित_करें_संग्रहण(int आकार) {
        return 정렬할당(आकार, 1);
    }

    public synchronized int 정렬할당(int आकार, int संरेखित_करें_मान) {
        if (आकार <= 0 || संरेखित_करें_मान <= 0 || (संरेखित_करें_मान & (संरेखित_करें_मान - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> एन्ट्री_मान : 빈영역.entrySet()) {
            int चलाएँ = एन्ट्री_मान.getKey().intValue();
            int क्षेत्र_आकार = एन्ट्री_मान.getValue().intValue();
            int 정렬시작 = (चलाएँ + संरेखित_करें_मान - 1) & -संरेखित_करें_मान;
            int सामने_मान_आकार = 정렬시작 - चलाएँ;
            int 끝크기 = क्षेत्र_आकार - सामने_मान_आकार - आकार;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(चलाएँ));
            if (सामने_मान_आकार > 0) {
                빈영역.put(Integer.valueOf(चलाएँ), Integer.valueOf(सामने_मान_आकार));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + आकार), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(आकार));
            Arrays.fill(मेमोरी_क्षेत्र, 정렬시작, 정렬시작 + आकार, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void रिलीज़_संग्रहण(int पता) {
        Integer आकार_ऑब्जेक्ट = 사용영역.remove(Integer.valueOf(पता));
        if (आकार_ऑब्जेक्ट == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int चलाएँ = पता;
        int आकार = आकार_ऑब्जेक्ट.intValue();
        Map.Entry<Integer, Integer> सामने_मान = 빈영역.lowerEntry(Integer.valueOf(चलाएँ));
        if (सामने_मान != null && सामने_मान.getKey().intValue() + सामने_मान.getValue().intValue() == चलाएँ) {
            चलाएँ = सामने_मान.getKey().intValue();
            आकार += सामने_मान.getValue().intValue();
            빈영역.remove(सामने_मान.getKey());
        }
        Map.Entry<Integer, Integer> वापस_मान = 빈영역.ceilingEntry(Integer.valueOf(चलाएँ));
        if (वापस_मान != null && चलाएँ + आकार == वापस_मान.getKey().intValue()) {
            आकार += वापस_मान.getValue().intValue();
            빈영역.remove(वापस_मान.getKey());
        }
        빈영역.put(Integer.valueOf(चलाएँ), Integer.valueOf(आकार));
    }

    public synchronized byte पढें_बाइट_मान(int पता) {
        जाँचें_श्रेणी(पता, 1);
        return मेमोरी_क्षेत्र[पता];
    }

    public synchronized void लिखना_बाइट_मान(int पता, byte मान) {
        जाँचें_श्रेणी(पता, 1);
        मेमोरी_क्षेत्र[पता] = मान;
    }

    public synchronized int 전체크기() {
        return मेमोरी_क्षेत्र.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer आकार : 사용영역.values()) {
            합계 += आकार.intValue();
        }
        return 합계;
    }

    private void जाँचें_श्रेणी(int पता, int आकार) {
        if (पता < 0 || आकार < 0 || पता > मेमोरी_क्षेत्र.length - आकार) {
            throw new IndexOutOfBoundsException("मेमोरी_क्षेत्र 범위를 벗어났습니다.");
        }
    }
}

