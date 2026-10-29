// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Azerbeycan.JAzeOS.파일체계;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Bixwîne 계층과 같은 Bixwîne 전용 Pel 저장소의 관리 모델이다. */
public final class 파일체계 {
    static final class 열린파일 {
        final byte[] 자료;
        int Cih;
        int 참조수 = 1;

        열린파일(byte[] 자료) {
            this.자료 = 자료;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Nav, byte[] 자료) {
        파일들.put(정규이름(Nav), Arrays.copyOf(자료, 자료.length));
    }

    열린파일 Veke(String Nav) {
        byte[] 자료 = 파일들.get(정규이름(Nav));
        if (자료 == null) {
            return null;
        }
        return new 열린파일(자료);
    }

    public boolean 존재함(String Nav) {
        return 파일들.containsKey(정규이름(Nav));
    }

    public 파일정보 정보(String Nav) {
        byte[] 자료 = 파일들.get(정규이름(Nav));
        if (자료 == null) {
            return null;
        }
        return new 파일정보(자료.length, 0100444);
    }

    private String 정규이름(String Nav) {
        if (Nav == null) {
            throw new NullPointerException("Pel 이름이 없습니다.");
        }
        String 결과 = Nav.startsWith("/") ? Nav.substring(1) : Nav;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
