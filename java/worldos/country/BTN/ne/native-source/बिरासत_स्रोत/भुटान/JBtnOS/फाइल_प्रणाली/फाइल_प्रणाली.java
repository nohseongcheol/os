// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भुटान.JBtnOS.फाइल_प्रणाली;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT पढनुहोस् 계층과 같은 पढनुहोस् 전용 फाइल 저장소의 관리 모델이다. */
public final class फाइल_प्रणाली {
    static final class 열린파일 {
        final byte[] लगत;
        int स्थिति;
        int 참조수 = 1;

        열린파일(byte[] लगत) {
            this.लगत = लगत;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String नाम, byte[] लगत) {
        파일들.put(정규이름(नाम), Arrays.copyOf(लगत, लगत.length));
    }

    열린파일 खोल्नुहोस्(String नाम) {
        byte[] लगत = 파일들.get(정규이름(नाम));
        if (लगत == null) {
            return null;
        }
        return new 열린파일(लगत);
    }

    public boolean 존재함(String नाम) {
        return 파일들.containsKey(정규이름(नाम));
    }

    public फाइल_जानकारी प्रणाली_जानकारी(String नाम) {
        byte[] लगत = 파일들.get(정규이름(नाम));
        if (लगत == null) {
            return null;
        }
        return new फाइल_जानकारी(लगत.length, 0100444);
    }

    private String 정규이름(String नाम) {
        if (नाम == null) {
            throw new NullPointerException("फाइल 이름이 없습니다.");
        }
        String मापन = नाम.startsWith("/") ? नाम.substring(1) : नाम;
        return मापन.toUpperCase(Locale.ROOT);
    }
}
