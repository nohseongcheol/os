// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package نيجيريا.JNgaOS.نظام_الملفات;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT قراءة 계층과 같은 قراءة 전용 ملف 저장소의 관리 모델이다. */
public final class نظام_الملفات {
    static final class 열린파일 {
        final byte[] بيانات;
        int موضع;
        int 참조수 = 1;

        열린파일(byte[] بيانات) {
            this.بيانات = بيانات;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void إلحاق_ملف(String اسم, byte[] بيانات) {
        파일들.put(اسم_متعارف_عليه(اسم), Arrays.copyOf(بيانات, بيانات.length));
    }

    열린파일 فتح(String اسم) {
        byte[] بيانات = 파일들.get(اسم_متعارف_عليه(اسم));
        if (بيانات == null) {
            return null;
        }
        return new 열린파일(بيانات);
    }

    public boolean 존재함(String اسم) {
        return 파일들.containsKey(اسم_متعارف_عليه(اسم));
    }

    public ملف_معلومات معلومات_النظام(String اسم) {
        byte[] بيانات = 파일들.get(اسم_متعارف_عليه(اسم));
        if (بيانات == null) {
            return null;
        }
        return new ملف_معلومات(بيانات.length, 0100444);
    }

    private String اسم_متعارف_عليه(String اسم) {
        if (اسم == null) {
            throw new NullPointerException("ملف 이름이 없습니다.");
        }
        String نتيجة = اسم.startsWith("/") ? اسم.substring(1) : اسم;
        return نتيجة.toUpperCase(Locale.ROOT);
    }
}
