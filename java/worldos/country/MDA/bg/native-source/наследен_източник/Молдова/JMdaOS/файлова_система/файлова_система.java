// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Молдова.JMdaOS.файлова_система;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Четене 계층과 같은 Четене 전용 Файл 저장소의 관리 모델이다. */
public final class файлова_система {
    static final class 열린파일 {
        final byte[] данни;
        int Позиция;
        int 참조수 = 1;

        열린파일(byte[] данни) {
            this.данни = данни;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void добавям_Файл(String Име, byte[] данни) {
        파일들.put(канонично_име(Име), Arrays.copyOf(данни, данни.length));
    }

    열린파일 Отваряне(String Име) {
        byte[] данни = 파일들.get(канонично_име(Име));
        if (данни == null) {
            return null;
        }
        return new 열린파일(данни);
    }

    public boolean 존재함(String Име) {
        return 파일들.containsKey(канонично_име(Име));
    }

    public Файл_инфо Системна_информация(String Име) {
        byte[] данни = 파일들.get(канонично_име(Име));
        if (данни == null) {
            return null;
        }
        return new Файл_инфо(данни.length, 0100444);
    }

    private String канонично_име(String Име) {
        if (Име == null) {
            throw new NullPointerException("Файл 이름이 없습니다.");
        }
        String РЕЗУЛТАТ = Име.startsWith("/") ? Име.substring(1) : Име;
        return РЕЗУЛТАТ.toUpperCase(Locale.ROOT);
    }
}
