// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 आंखचें_मोल नेमून_दिवचें_सांठवण, रिलीज_सांठवण, 병합을 담당한다. */
public final class मेमरी_वेवस्थापक {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public मेमरी_वेवस्थापक(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int नेमून_दिवचें_सांठवण(int आवाठ) {
        return 정렬할당(आवाठ, 1);
    }

    public synchronized int 정렬할당(int आवाठ, int आंखचें_मोल) {
        if (आवाठ <= 0 || आंखचें_मोल <= 0 || (आंखचें_मोल & (आंखचें_मोल - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> प्रवेश_मोल : 빈영역.entrySet()) {
            int चलोवप = प्रवेश_मोल.getKey().intValue();
            int 영역크기 = प्रवेश_मोल.getValue().intValue();
            int 정렬시작 = (चलोवप + आंखचें_मोल - 1) & -आंखचें_मोल;
            int 앞크기 = 정렬시작 - चलोवप;
            int 끝크기 = 영역크기 - 앞크기 - आवाठ;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(चलोवप));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(चलोवप), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + आवाठ), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(आवाठ));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + आवाठ, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void रिलीज_सांठवण(int नामो) {
        Integer आवाठ_ऑब्जॅक्ट = 사용영역.remove(Integer.valueOf(नामो));
        if (आवाठ_ऑब्जॅक्ट == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int चलोवप = नामो;
        int आवाठ = आवाठ_ऑब्जॅक्ट.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(चलोवप));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == चलोवप) {
            चलोवप = 앞.getKey().intValue();
            आवाठ += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> फाटीं_मोल = 빈영역.ceilingEntry(Integer.valueOf(चलोवप));
        if (फाटीं_मोल != null && चलोवप + आवाठ == फाटीं_मोल.getKey().intValue()) {
            आवाठ += फाटीं_मोल.getValue().intValue();
            빈영역.remove(फाटीं_मोल.getKey());
        }
        빈영역.put(Integer.valueOf(चलोवप), Integer.valueOf(आवाठ));
    }

    public synchronized byte 바이트읽기(int नामो) {
        범위확인(नामो, 1);
        return 기억공간[नामो];
    }

    public synchronized void बरोवचें_बायट_मोल(int नामो, byte मोल) {
        범위확인(नामो, 1);
        기억공간[नामो] = मोल;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer आवाठ : 사용영역.values()) {
            합계 += आवाठ.intValue();
        }
        return 합계;
    }

    private void 범위확인(int नामो, int आवाठ) {
        if (नामो < 0 || आवाठ < 0 || नामो > 기억공간.length - आवाठ) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

