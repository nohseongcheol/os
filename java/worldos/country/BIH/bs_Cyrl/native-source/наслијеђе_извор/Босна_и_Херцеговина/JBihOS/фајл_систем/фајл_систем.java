// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.фајл_систем;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 фајл 저장소의 관리 모델이다. */
public final class фајл_систем {
    static final class 열린파일 {
        final byte[] подаци;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] подаци) {
            this.подаци = подаци;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String назив, byte[] подаци) {
        파일들.put(정규이름(назив), Arrays.copyOf(подаци, подаци.length));
    }

    열린파일 отворити(String назив) {
        byte[] подаци = 파일들.get(정규이름(назив));
        if (подаци == null) {
            return null;
        }
        return new 열린파일(подаци);
    }

    public boolean 존재함(String назив) {
        return 파일들.containsKey(정규이름(назив));
    }

    public фајл_информација систем_информација(String назив) {
        byte[] подаци = 파일들.get(정규이름(назив));
        if (подаци == null) {
            return null;
        }
        return new фајл_информација(подаци.length, 0100444);
    }

    private String 정규이름(String назив) {
        if (назив == null) {
            throw new NullPointerException("фајл 이름이 없습니다.");
        }
        String 결과 = назив.startsWith("/") ? назив.substring(1) : назив;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
