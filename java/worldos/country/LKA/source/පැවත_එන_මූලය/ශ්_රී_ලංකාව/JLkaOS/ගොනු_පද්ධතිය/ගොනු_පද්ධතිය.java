// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.ගොනු_පද්ධතිය;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT කියවීම 계층과 같은 කියවීම 전용 ගොනු 저장소의 관리 모델이다. */
public final class ගොනු_පද්ධතිය {
    static final class 열린파일 {
        final byte[] දත්ත;
        int පිහිටීම;
        int 참조수 = 1;

        열린파일(byte[] දත්ත) {
            this.දත්ත = දත්ත;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String නම, byte[] දත්ත) {
        파일들.put(정규이름(නම), Arrays.copyOf(දත්ත, දත්ත.length));
    }

    열린파일 විවෘත_කරන්න(String නම) {
        byte[] දත්ත = 파일들.get(정규이름(නම));
        if (දත්ත == null) {
            return null;
        }
        return new 열린파일(දත්ත);
    }

    public boolean 존재함(String නම) {
        return 파일들.containsKey(정규이름(නම));
    }

    public ගොනුව_තතු පද්ධති_තොරතුරු(String නම) {
        byte[] දත්ත = 파일들.get(정규이름(නම));
        if (දත්ත == null) {
            return null;
        }
        return new ගොනුව_තතු(දත්ත.length, 0100444);
    }

    private String 정규이름(String නම) {
        if (නම == null) {
            throw new NullPointerException("ගොනු 이름이 없습니다.");
        }
        String 결과 = නම.startsWith("/") ? නම.substring(1) : නම;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
