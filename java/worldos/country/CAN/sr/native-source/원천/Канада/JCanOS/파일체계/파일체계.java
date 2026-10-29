// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Канада.JCanOS.파일체계;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Чита 계층과 같은 Чита 전용 Датотека 저장소의 관리 모델이다. */
public final class 파일체계 {
    static final class 열린파일 {
        final byte[] 자료;
        int Положај;
        int 참조수 = 1;

        열린파일(byte[] 자료) {
            this.자료 = 자료;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Назив, byte[] 자료) {
        파일들.put(정규이름(Назив), Arrays.copyOf(자료, 자료.length));
    }

    열린파일 Отвори(String Назив) {
        byte[] 자료 = 파일들.get(정규이름(Назив));
        if (자료 == null) {
            return null;
        }
        return new 열린파일(자료);
    }

    public boolean 존재함(String Назив) {
        return 파일들.containsKey(정규이름(Назив));
    }

    public 파일정보 정보(String Назив) {
        byte[] 자료 = 파일들.get(정규이름(Назив));
        if (자료 == null) {
            return null;
        }
        return new 파일정보(자료.length, 0100444);
    }

    private String 정규이름(String Назив) {
        if (Назив == null) {
            throw new NullPointerException("Датотека 이름이 없습니다.");
        }
        String ИСХОД = Назив.startsWith("/") ? Назив.substring(1) : Назив;
        return ИСХОД.toUpperCase(Locale.ROOT);
    }
}
