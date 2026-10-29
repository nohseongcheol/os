// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عێراق.JIrqOS.سیستمی_فایل;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 فایل 저장소의 관리 모델이다. */
public final class سیستمی_فایل {
    static final class 열린파일 {
        final byte[] دەیتا;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] دەیتا) {
            this.دەیتا = دەیتا;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ناو, byte[] دەیتا) {
        파일들.put(정규이름(ناو), Arrays.copyOf(دەیتا, دەیتا.length));
    }

    열린파일 کردنەوە(String ناو) {
        byte[] دەیتا = 파일들.get(정규이름(ناو));
        if (دەیتا == null) {
            return null;
        }
        return new 열린파일(دەیتا);
    }

    public boolean 존재함(String ناو) {
        return 파일들.containsKey(정규이름(ناو));
    }

    public فایل_زانیاری msinfo32_exe(String ناو) {
        byte[] دەیتا = 파일들.get(정규이름(ناو));
        if (دەیتا == null) {
            return null;
        }
        return new فایل_زانیاری(دەیتا.length, 0100444);
    }

    private String 정규이름(String ناو) {
        if (ناو == null) {
            throw new NullPointerException("فایل 이름이 없습니다.");
        }
        String 결과 = ناو.startsWith("/") ? ناو.substring(1) : ناو;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
