// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.системаи_файлӣ;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Хондан 계층과 같은 Хондан 전용 Файл 저장소의 관리 모델이다. */
public final class системаи_файлӣ {
    static final class 열린파일 {
        final byte[] иттилоот;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] иттилоот) {
            this.иттилоот = иттилоот;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Ном, byte[] иттилоот) {
        파일들.put(정규이름(Ном), Arrays.copyOf(иттилоот, иттилоот.length));
    }

    열린파일 кушодан(String Ном) {
        byte[] иттилоот = 파일들.get(정규이름(Ном));
        if (иттилоот == null) {
            return null;
        }
        return new 열린파일(иттилоот);
    }

    public boolean 존재함(String Ном) {
        return 파일들.containsKey(정규이름(Ном));
    }

    public файл_маълумот Маълумоти_система(String Ном) {
        byte[] иттилоот = 파일들.get(정규이름(Ном));
        if (иттилоот == null) {
            return null;
        }
        return new файл_маълумот(иттилоот.length, 0100444);
    }

    private String 정규이름(String Ном) {
        if (Ном == null) {
            throw new NullPointerException("Файл 이름이 없습니다.");
        }
        String 결과 = Ном.startsWith("/") ? Ном.substring(1) : Ном;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
