// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئافغانىستان.JAfgOS.ھۆججەت_سىستېمىسى;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT ئوقۇ 계층과 같은 ئوقۇ 전용 ھۆججەت 저장소의 관리 모델이다. */
public final class ھۆججەت_سىستېمىسى {
    static final class 열린파일 {
        final byte[] مەلۇمات;
        int ئورۇن;
        int 참조수 = 1;

        열린파일(byte[] مەلۇمات) {
            this.مەلۇمات = مەلۇمات;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ئاتى, byte[] مەلۇمات) {
        파일들.put(정규이름(ئاتى), Arrays.copyOf(مەلۇمات, مەلۇمات.length));
    }

    열린파일 ئاچ(String ئاتى) {
        byte[] مەلۇمات = 파일들.get(정규이름(ئاتى));
        if (مەلۇمات == null) {
            return null;
        }
        return new 열린파일(مەلۇمات);
    }

    public boolean 존재함(String ئاتى) {
        return 파일들.containsKey(정규이름(ئاتى));
    }

    public ھۆججەت_ئۇچۇر سىستېما_ئۇچۇرى(String ئاتى) {
        byte[] مەلۇمات = 파일들.get(정규이름(ئاتى));
        if (مەلۇمات == null) {
            return null;
        }
        return new ھۆججەت_ئۇچۇر(مەلۇمات.length, 0100444);
    }

    private String 정규이름(String ئاتى) {
        if (ئاتى == null) {
            throw new NullPointerException("ھۆججەت 이름이 없습니다.");
        }
        String ئۆلچەم = ئاتى.startsWith("/") ? ئاتى.substring(1) : ئاتى;
        return ئۆلچەم.toUpperCase(Locale.ROOT);
    }
}
