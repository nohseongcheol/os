// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.файлдық_жүйе;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Оқу 계층과 같은 Оқу 전용 Файл 저장소의 관리 모델이다. */
public final class файлдық_жүйе {
    static final class 열린파일 {
        final byte[] деректер;
        int Орны;
        int 참조수 = 1;

        열린파일(byte[] деректер) {
            this.деректер = деректер;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void қосу_файл(String Аты, byte[] деректер) {
        파일들.put(정규이름(Аты), Arrays.copyOf(деректер, деректер.length));
    }

    열린파일 Ашу(String Аты) {
        byte[] деректер = 파일들.get(정규이름(Аты));
        if (деректер == null) {
            return null;
        }
        return new 열린파일(деректер);
    }

    public boolean 존재함(String Аты) {
        return 파일들.containsKey(정규이름(Аты));
    }

    public файл_ақпарат Жүйелік_ақпарат(String Аты) {
        byte[] деректер = 파일들.get(정규이름(Аты));
        if (деректер == null) {
            return null;
        }
        return new файл_ақпарат(деректер.length, 0100444);
    }

    private String 정규이름(String Аты) {
        if (Аты == null) {
            throw new NullPointerException("Файл 이름이 없습니다.");
        }
        String НӘТИЖЕ = Аты.startsWith("/") ? Аты.substring(1) : Аты;
        return НӘТИЖЕ.toUpperCase(Locale.ROOT);
    }
}
