// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भुटान.JBtnOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 पङ्_क्तिबद्ध_गर्नुहोस्_मान निर्धारण_गर्नुहोस्_भण्डारण, जारी_भण्डारण, 병합을 담당한다. */
public final class मेमोरी_प्रबन्धक {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public मेमोरी_प्रबन्धक(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int निर्धारण_गर्नुहोस्_भण्डारण(int आकार) {
        return 정렬할당(आकार, 1);
    }

    public synchronized int 정렬할당(int आकार, int पङ्_क्तिबद्ध_गर्नुहोस्_मान) {
        if (आकार <= 0 || पङ्_क्तिबद्ध_गर्नुहोस्_मान <= 0 || (पङ्_क्तिबद्ध_गर्नुहोस्_मान & (पङ्_क्तिबद्ध_गर्नुहोस्_मान - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> प्रविष्टि_मान : 빈영역.entrySet()) {
            int चलाउनुहोस् = प्रविष्टि_मान.getKey().intValue();
            int 영역크기 = प्रविष्टि_मान.getValue().intValue();
            int 정렬시작 = (चलाउनुहोस् + पङ्_क्तिबद्ध_गर्नुहोस्_मान - 1) & -पङ्_क्तिबद्ध_गर्नुहोस्_मान;
            int 앞크기 = 정렬시작 - चलाउनुहोस्;
            int 끝크기 = 영역크기 - 앞크기 - आकार;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(चलाउनुहोस्));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(चलाउनुहोस्), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + आकार), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(आकार));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + आकार, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void जारी_भण्डारण(int ठेगाना) {
        Integer साइज_वस्तु = 사용영역.remove(Integer.valueOf(ठेगाना));
        if (साइज_वस्तु == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int चलाउनुहोस् = ठेगाना;
        int आकार = साइज_वस्तु.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(चलाउनुहोस्));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == चलाउनुहोस्) {
            चलाउनुहोस् = 앞.getKey().intValue();
            आकार += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> पछाडि_मान = 빈영역.ceilingEntry(Integer.valueOf(चलाउनुहोस्));
        if (पछाडि_मान != null && चलाउनुहोस् + आकार == पछाडि_मान.getKey().intValue()) {
            आकार += पछाडि_मान.getValue().intValue();
            빈영역.remove(पछाडि_मान.getKey());
        }
        빈영역.put(Integer.valueOf(चलाउनुहोस्), Integer.valueOf(आकार));
    }

    public synchronized byte 바이트읽기(int ठेगाना) {
        범위확인(ठेगाना, 1);
        return 기억공간[ठेगाना];
    }

    public synchronized void लेख्नुहोस्_बाइट_मान(int ठेगाना, byte मान) {
        범위확인(ठेगाना, 1);
        기억공간[ठेगाना] = मान;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer आकार : 사용영역.values()) {
            합계 += आकार.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ठेगाना, int आकार) {
        if (ठेगाना < 0 || आकार < 0 || ठेगाना > 기억공간.length - आकार) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

