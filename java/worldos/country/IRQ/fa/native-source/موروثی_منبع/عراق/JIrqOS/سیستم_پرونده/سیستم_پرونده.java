// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عراق.JIrqOS.سیستم_پرونده;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT خواندن 계층과 같은 خواندن 전용 پرونده 저장소의 관리 모델이다. */
public final class سیستم_پرونده {
    static final class 열린파일 {
        final byte[] داده_ها;
        int مرتب_کردن;
        int 참조수 = 1;

        열린파일(byte[] داده_ها) {
            this.داده_ها = داده_ها;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String نام, byte[] داده_ها) {
        파일들.put(정규이름(نام), Arrays.copyOf(داده_ها, داده_ها.length));
    }

    열린파일 باز_کردن(String نام) {
        byte[] داده_ها = 파일들.get(정규이름(نام));
        if (داده_ها == null) {
            return null;
        }
        return new 열린파일(داده_ها);
    }

    public boolean 존재함(String نام) {
        return 파일들.containsKey(정규이름(نام));
    }

    public فایل_اطلاعات اطلاعات_سیستم(String نام) {
        byte[] داده_ها = 파일들.get(정규이름(نام));
        if (داده_ها == null) {
            return null;
        }
        return new فایل_اطلاعات(داده_ها.length, 0100444);
    }

    private String 정규이름(String نام) {
        if (نام == null) {
            throw new NullPointerException("پرونده 이름이 없습니다.");
        }
        String سنجش = نام.startsWith("/") ? نام.substring(1) : نام;
        return سنجش.toUpperCase(Locale.ROOT);
    }
}
