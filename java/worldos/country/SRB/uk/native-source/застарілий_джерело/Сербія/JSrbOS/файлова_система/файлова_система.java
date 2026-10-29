// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Сербія.JSrbOS.файлова_система;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Читання 계층과 같은 Читання 전용 файл 저장소의 관리 모델이다. */
public final class файлова_система {
    static final class 열린파일 {
        final byte[] дані;
        int позиція;
        int 참조수 = 1;

        열린파일(byte[] дані) {
            this.дані = дані;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void додавати_Файл(String Назва, byte[] дані) {
        파일들.put(канонічне_ім_я(Назва), Arrays.copyOf(дані, дані.length));
    }

    열린파일 Відкрити(String Назва) {
        byte[] дані = 파일들.get(канонічне_ім_я(Назва));
        if (дані == null) {
            return null;
        }
        return new 열린파일(дані);
    }

    public boolean 존재함(String Назва) {
        return 파일들.containsKey(канонічне_ім_я(Назва));
    }

    public Файл_відомості Відомості_про_систему(String Назва) {
        byte[] дані = 파일들.get(канонічне_ім_я(Назва));
        if (дані == null) {
            return null;
        }
        return new Файл_відомості(дані.length, 0100444);
    }

    private String канонічне_ім_я(String Назва) {
        if (Назва == null) {
            throw new NullPointerException("файл 이름이 없습니다.");
        }
        String результат = Назва.startsWith("/") ? Назва.substring(1) : Назва;
        return результат.toUpperCase(Locale.ROOT);
    }
}
