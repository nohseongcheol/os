// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польшча.JPolOS.файлавая_сістэма;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Чытанне 계층과 같은 Чытанне 전용 Файл 저장소의 관리 모델이다. */
public final class файлавая_сістэма {
    static final class 열린파일 {
        final byte[] дадзеныя;
        int Пазіцыя;
        int 참조수 = 1;

        열린파일(byte[] дадзеныя) {
            this.дадзеныя = дадзеныя;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Назва, byte[] дадзеныя) {
        파일들.put(정규이름(Назва), Arrays.copyOf(дадзеныя, дадзеныя.length));
    }

    열린파일 Адкрыць(String Назва) {
        byte[] дадзеныя = 파일들.get(정규이름(Назва));
        if (дадзеныя == null) {
            return null;
        }
        return new 열린파일(дадзеныя);
    }

    public boolean 존재함(String Назва) {
        return 파일들.containsKey(정규이름(Назва));
    }

    public файл_звесткі Сістэмная_інфармацыя(String Назва) {
        byte[] дадзеныя = 파일들.get(정규이름(Назва));
        if (дадзеныя == null) {
            return null;
        }
        return new файл_звесткі(дадзеныя.length, 0100444);
    }

    private String 정규이름(String Назва) {
        if (Назва == null) {
            throw new NullPointerException("Файл 이름이 없습니다.");
        }
        String 결과 = Назва.startsWith("/") ? Назва.substring(1) : Назва;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
