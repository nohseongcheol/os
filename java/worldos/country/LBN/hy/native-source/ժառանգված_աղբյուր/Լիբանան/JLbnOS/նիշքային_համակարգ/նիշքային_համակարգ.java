// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Լիբանան.JLbnOS.նիշքային_համակարգ;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Ընթերցում 계층과 같은 Ընթերցում 전용 Ֆայլ 저장소의 관리 모델이다. */
public final class նիշքային_համակարգ {
    static final class 열린파일 {
        final byte[] տվյալ;
        int Դիրք;
        int 참조수 = 1;

        열린파일(byte[] տվյալ) {
            this.տվյալ = տվյալ;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Անուն, byte[] տվյալ) {
        파일들.put(정규이름(Անուն), Arrays.copyOf(տվյալ, տվյալ.length));
    }

    열린파일 Բաց(String Անուն) {
        byte[] տվյալ = 파일들.get(정규이름(Անուն));
        if (տվյալ == null) {
            return null;
        }
        return new 열린파일(տվյալ);
    }

    public boolean 존재함(String Անուն) {
        return 파일들.containsKey(정규이름(Անուն));
    }

    public նիշք_տեղեկություն Համակարգի_տեղեկություն(String Անուն) {
        byte[] տվյալ = 파일들.get(정규이름(Անուն));
        if (տվյալ == null) {
            return null;
        }
        return new նիշք_տեղեկություն(տվյալ.length, 0100444);
    }

    private String 정규이름(String Անուն) {
        if (Անուն == null) {
            throw new NullPointerException("Ֆայլ 이름이 없습니다.");
        }
        String չափ = Անուն.startsWith("/") ? Անուն.substring(1) : Անուն;
        return չափ.toUpperCase(Locale.ROOT);
    }
}
