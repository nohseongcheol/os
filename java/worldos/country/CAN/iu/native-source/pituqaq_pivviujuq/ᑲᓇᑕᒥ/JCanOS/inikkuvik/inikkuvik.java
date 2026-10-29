// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.inikkuvik;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 ini 저장소의 관리 모델이다. */
public final class inikkuvik {
    static final class 열린파일 {
        final byte[] titiqqat;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] titiqqat) {
            this.titiqqat = titiqqat;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String atiq, byte[] titiqqat) {
        파일들.put(정규이름(atiq), Arrays.copyOf(titiqqat, titiqqat.length));
    }

    열린파일 matuirli(String atiq) {
        byte[] titiqqat = 파일들.get(정규이름(atiq));
        if (titiqqat == null) {
            return null;
        }
        return new 열린파일(titiqqat);
    }

    public boolean 존재함(String atiq) {
        return 파일들.containsKey(정규이름(atiq));
    }

    public ini_tukisigiarut msinfo32_exe(String atiq) {
        byte[] titiqqat = 파일들.get(정규이름(atiq));
        if (titiqqat == null) {
            return null;
        }
        return new ini_tukisigiarut(titiqqat.length, 0100444);
    }

    private String 정규이름(String atiq) {
        if (atiq == null) {
            throw new NullPointerException("ini 이름이 없습니다.");
        }
        String 결과 = atiq.startsWith("/") ? atiq.substring(1) : atiq;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
