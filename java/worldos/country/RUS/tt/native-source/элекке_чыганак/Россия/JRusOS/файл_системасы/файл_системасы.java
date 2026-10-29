// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.файл_системасы;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 Birem 저장소의 관리 모델이다. */
public final class файл_системасы {
    static final class 열린파일 {
        final byte[] мәгълүмат;
        int урнаштыру;
        int Белешмәлекләр_COUNT = 1;

        열린파일(byte[] мәгълүмат) {
            this.мәгълүмат = мәгълүмат;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String исем, byte[] мәгълүмат) {
        파일들.put(정규이름(исем), Arrays.copyOf(мәгълүмат, мәгълүмат.length));
    }

    열린파일 ачу(String исем) {
        byte[] мәгълүмат = 파일들.get(정규이름(исем));
        if (мәгълүмат == null) {
            return null;
        }
        return new 열린파일(мәгълүмат);
    }

    public boolean 존재함(String исем) {
        return 파일들.containsKey(정규이름(исем));
    }

    public файл_мәгълүмат msinfo32_exe(String исем) {
        byte[] мәгълүмат = 파일들.get(정규이름(исем));
        if (мәгълүмат == null) {
            return null;
        }
        return new файл_мәгълүмат(мәгълүмат.length, 0100444);
    }

    private String 정규이름(String исем) {
        if (исем == null) {
            throw new NullPointerException("Birem 이름이 없습니다.");
        }
        String үлчәм = исем.startsWith("/") ? исем.substring(1) : исем;
        return үлчәм.toUpperCase(Locale.ROOT);
    }
}
