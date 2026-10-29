// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ڀارت.JIndOS.فائل_سسٽم;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 فائل 저장소의 관리 모델이다. */
public final class فائل_سسٽم {
    static final class 열린파일 {
        final byte[] ڪوائف;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] ڪوائف) {
            this.ڪوائف = ڪوائف;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String نالو, byte[] ڪوائف) {
        파일들.put(정규이름(نالو), Arrays.copyOf(ڪوائف, ڪوائف.length));
    }

    열린파일 ٺاھيو(String نالو) {
        byte[] ڪوائف = 파일들.get(정규이름(نالو));
        if (ڪوائف == null) {
            return null;
        }
        return new 열린파일(ڪوائف);
    }

    public boolean 존재함(String نالو) {
        return 파일들.containsKey(정규이름(نالو));
    }

    public فائل_معلومات سسٽم_معلومات(String نالو) {
        byte[] ڪوائف = 파일들.get(정규이름(نالو));
        if (ڪوائف == null) {
            return null;
        }
        return new فائل_معلومات(ڪوائف.length, 0100444);
    }

    private String 정규이름(String نالو) {
        if (نالو == null) {
            throw new NullPointerException("فائل 이름이 없습니다.");
        }
        String 결과 = نالو.startsWith("/") ? نالو.substring(1) : نالو;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
