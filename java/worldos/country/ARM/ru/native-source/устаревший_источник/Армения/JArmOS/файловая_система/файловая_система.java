// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Армения.JArmOS.файловая_система;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Чтение 계층과 같은 Чтение 전용 файл 저장소의 관리 모델이다. */
public final class файловая_система {
    static final class 열린파일 {
        final byte[] данные;
        int позиция;
        int ссылка_СЧЁТ = 1;

        열린파일(byte[] данные) {
            this.данные = данные;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void добавить_файл(String Название, byte[] данные) {
        파일들.put(каноническое_имя(Название), Arrays.copyOf(данные, данные.length));
    }

    열린파일 Открыть(String Название) {
        byte[] данные = 파일들.get(каноническое_имя(Название));
        if (данные == null) {
            return null;
        }
        return new 열린파일(данные);
    }

    public boolean 존재함(String Название) {
        return 파일들.containsKey(каноническое_имя(Название));
    }

    public файл_сведения msinfo32_exe(String Название) {
        byte[] данные = 파일들.get(каноническое_имя(Название));
        if (данные == null) {
            return null;
        }
        return new файл_сведения(данные.length, 0100444);
    }

    private String каноническое_имя(String Название) {
        if (Название == null) {
            throw new NullPointerException("файл 이름이 없습니다.");
        }
        String результат = Название.startsWith("/") ? Название.substring(1) : Название;
        return результат.toUpperCase(Locale.ROOT);
    }
}
