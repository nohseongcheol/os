// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.फायल_प्रणाली;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 फायल 저장소의 관리 모델이다. */
public final class फायल_प्रणाली {
    static final class 열린파일 {
        final byte[] डेटा;
        int स्थिती;
        int संदर्भ_COUNT = 1;

        열린파일(byte[] डेटा) {
            this.डेटा = डेटा;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String नांव, byte[] डेटा) {
        파일들.put(정규이름(नांव), Arrays.copyOf(डेटा, डेटा.length));
    }

    열린파일 उगडचें(String नांव) {
        byte[] डेटा = 파일들.get(정규이름(नांव));
        if (डेटा == null) {
            return null;
        }
        return new 열린파일(डेटा);
    }

    public boolean 존재함(String नांव) {
        return 파일들.containsKey(정규이름(नांव));
    }

    public फायल_म्हायती msinfo32_exe(String नांव) {
        byte[] डेटा = 파일들.get(정규이름(नांव));
        if (डेटा == null) {
            return null;
        }
        return new फायल_म्हायती(डेटा.length, 0100444);
    }

    private String 정규이름(String नांव) {
        if (नांव == null) {
            throw new NullPointerException("फायल 이름이 없습니다.");
        }
        String मेजप = नांव.startsWith("/") ? नांव.substring(1) : नांव;
        return मेजप.toUpperCase(Locale.ROOT);
    }
}
