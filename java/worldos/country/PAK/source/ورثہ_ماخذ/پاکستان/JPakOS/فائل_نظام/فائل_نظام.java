// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.فائل_نظام;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT پڑھیں 계층과 같은 پڑھیں 전용 فائل_کا_نام 저장소의 관리 모델이다. */
public final class فائل_نظام {
    static final class 열린파일 {
        final byte[] کوائف;
        int مقام;
        int 참조수 = 1;

        열린파일(byte[] کوائف) {
            this.کوائف = کوائف;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String نام, byte[] کوائف) {
        파일들.put(정규이름(نام), Arrays.copyOf(کوائف, کوائف.length));
    }

    열린파일 کھولیں(String نام) {
        byte[] کوائف = 파일들.get(정규이름(نام));
        if (کوائف == null) {
            return null;
        }
        return new 열린파일(کوائف);
    }

    public boolean 존재함(String نام) {
        return 파일들.containsKey(정규이름(نام));
    }

    public فائل_معلومات نظام_کی_معلومات(String نام) {
        byte[] کوائف = 파일들.get(정규이름(نام));
        if (کوائف == null) {
            return null;
        }
        return new فائل_معلومات(کوائف.length, 0100444);
    }

    private String 정규이름(String نام) {
        if (نام == null) {
            throw new NullPointerException("فائل_کا_نام 이름이 없습니다.");
        }
        String پیمائش = نام.startsWith("/") ? نام.substring(1) : نام;
        return پیمائش.toUpperCase(Locale.ROOT);
    }
}
