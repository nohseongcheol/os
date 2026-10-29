// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ભારત.JIndOS.ફાઇલ_સિસ્ટમ;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT વાંચો 계층과 같은 વાંચો 전용 ફાઈલ 저장소의 관리 모델이다. */
public final class ફાઇલ_સિસ્ટમ {
    static final class 열린파일 {
        final byte[] ડેટા;
        int સ્થાન;
        int 참조수 = 1;

        열린파일(byte[] ડેટા) {
            this.ડેટા = ડેટા;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String નામ, byte[] ડેટા) {
        파일들.put(정규이름(નામ), Arrays.copyOf(ડેટા, ડેટા.length));
    }

    열린파일 ખોલો(String નામ) {
        byte[] ડેટા = 파일들.get(정규이름(નામ));
        if (ડેટા == null) {
            return null;
        }
        return new 열린파일(ડેટા);
    }

    public boolean 존재함(String નામ) {
        return 파일들.containsKey(정규이름(નામ));
    }

    public ફાઇલ_માહિતી સિસ્ટમ_માહિતી(String નામ) {
        byte[] ડેટા = 파일들.get(정규이름(નામ));
        if (ડેટા == null) {
            return null;
        }
        return new ફાઇલ_માહિતી(ડેટા.length, 0100444);
    }

    private String 정규이름(String નામ) {
        if (નામ == null) {
            throw new NullPointerException("ફાઈલ 이름이 없습니다.");
        }
        String પરિમાણ = નામ.startsWith("/") ? નામ.substring(1) : નામ;
        return પરિમાણ.toUpperCase(Locale.ROOT);
    }
}
