// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.файл_тутуму;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Окуу 계층과 같은 Окуу 전용 Файл 저장소의 관리 모델이다. */
public final class файл_тутуму {
    static final class 열린파일 {
        final byte[] берилмелер;
        int Турган_жери;
        int 참조수 = 1;

        열린파일(byte[] берилмелер) {
            this.берилмелер = берилмелер;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Аты, byte[] берилмелер) {
        파일들.put(정규이름(Аты), Arrays.copyOf(берилмелер, берилмелер.length));
    }

    열린파일 Ачуу(String Аты) {
        byte[] берилмелер = 파일들.get(정규이름(Аты));
        if (берилмелер == null) {
            return null;
        }
        return new 열린파일(берилмелер);
    }

    public boolean 존재함(String Аты) {
        return 파일들.containsKey(정규이름(Аты));
    }

    public файл_маалымат Система_маалыматы(String Аты) {
        byte[] берилмелер = 파일들.get(정규이름(Аты));
        if (берилмелер == null) {
            return null;
        }
        return new файл_маалымат(берилмелер.length, 0100444);
    }

    private String 정규이름(String Аты) {
        if (Аты == null) {
            throw new NullPointerException("Файл 이름이 없습니다.");
        }
        String 결과 = Аты.startsWith("/") ? Аты.substring(1) : Аты;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
