// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.a_yatawaajiraaya_anaajaalaairua;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 anaajaalaa 저장소의 관리 모델이다. */
public final class a_yatawaajiraaya_anaajaalaairua {
    static final class 열린파일 {
        final byte[] atijaaya;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] atijaaya) {
            this.atijaaya = atijaaya;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String 이름, byte[] atijaaya) {
        파일들.put(정규이름(이름), Arrays.copyOf(atijaaya, atijaaya.length));
    }

    열린파일 열기(String 이름) {
        byte[] atijaaya = 파일들.get(정규이름(이름));
        if (atijaaya == null) {
            return null;
        }
        return new 열린파일(atijaaya);
    }

    public boolean 존재함(String 이름) {
        return 파일들.containsKey(정규이름(이름));
    }

    public 파일정보 정보(String 이름) {
        byte[] atijaaya = 파일들.get(정규이름(이름));
        if (atijaaya == null) {
            return null;
        }
        return new 파일정보(atijaaya.length, 0100444);
    }

    private String 정규이름(String 이름) {
        if (이름 == null) {
            throw new NullPointerException("anaajaalaa 이름이 없습니다.");
        }
        String 결과 = 이름.startsWith("/") ? 이름.substring(1) : 이름;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
