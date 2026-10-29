// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.מערכת_קבצים;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT קרא 계층과 같은 קרא 전용 קובץ 저장소의 관리 모델이다. */
public final class מערכת_קבצים {
    static final class 열린파일 {
        final byte[] נתונים;
        int מיקום;
        int 참조수 = 1;

        열린파일(byte[] נתונים) {
            this.נתונים = נתונים;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void צירוף_קובץ(String שם, byte[] נתונים) {
        파일들.put(שם_קנוני(שם), Arrays.copyOf(נתונים, נתונים.length));
    }

    열린파일 פתח(String שם) {
        byte[] נתונים = 파일들.get(שם_קנוני(שם));
        if (נתונים == null) {
            return null;
        }
        return new 열린파일(נתונים);
    }

    public boolean 존재함(String שם) {
        return 파일들.containsKey(שם_קנוני(שם));
    }

    public קובץ_מידע מידע_מערכת(String שם) {
        byte[] נתונים = 파일들.get(שם_קנוני(שם));
        if (נתונים == null) {
            return null;
        }
        return new קובץ_מידע(נתונים.length, 0100444);
    }

    private String שם_קנוני(String שם) {
        if (שם == null) {
            throw new NullPointerException("קובץ 이름이 없습니다.");
        }
        String תוצאה = שם.startsWith("/") ? שם.substring(1) : שם;
        return תוצאה.toUpperCase(Locale.ROOT);
    }
}
