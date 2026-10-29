// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Албанија.JAlbOS.систем_на_датотеки;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Читај 계층과 같은 Читај 전용 Датотека 저장소의 관리 모델이다. */
public final class систем_на_датотеки {
    static final class 열린파일 {
        final byte[] податоци;
        int Позиција;
        int Референци_COUNT = 1;

        열린파일(byte[] податоци) {
            this.податоци = податоци;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Име, byte[] податоци) {
        파일들.put(정규이름(Име), Arrays.copyOf(податоци, податоци.length));
    }

    열린파일 Отвори(String Име) {
        byte[] податоци = 파일들.get(정규이름(Име));
        if (податоци == null) {
            return null;
        }
        return new 열린파일(податоци);
    }

    public boolean 존재함(String Име) {
        return 파일들.containsKey(정규이름(Име));
    }

    public датотека_информации msinfo32_exe(String Име) {
        byte[] податоци = 파일들.get(정규이름(Име));
        if (податоци == null) {
            return null;
        }
        return new датотека_информации(податоци.length, 0100444);
    }

    private String 정규이름(String Име) {
        if (Име == null) {
            throw new NullPointerException("Датотека 이름이 없습니다.");
        }
        String мерка = Име.startsWith("/") ? Име.substring(1) : Име;
        return мерка.toUpperCase(Locale.ROOT);
    }
}
