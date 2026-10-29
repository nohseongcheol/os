// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਯੂਨਾਈਟਡ_ਕਿੰਗਡਮ.JGbrOS.ਫਾਈਲ_ਸਿਸਟਮ;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT ਪੜ੍ਹਨ 계층과 같은 ਪੜ੍ਹਨ 전용 ਫਾਇਲ 저장소의 관리 모델이다. */
public final class ਫਾਈਲ_ਸਿਸਟਮ {
    static final class 열린파일 {
        final byte[] ਸਮੱਗਰੀ;
        int ਸਥਿਤੀ;
        int 참조수 = 1;

        열린파일(byte[] ਸਮੱਗਰੀ) {
            this.ਸਮੱਗਰੀ = ਸਮੱਗਰੀ;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ਨਾਂ, byte[] ਸਮੱਗਰੀ) {
        파일들.put(정규이름(ਨਾਂ), Arrays.copyOf(ਸਮੱਗਰੀ, ਸਮੱਗਰੀ.length));
    }

    열린파일 ਖੋਲ੍ਹੋ(String ਨਾਂ) {
        byte[] ਸਮੱਗਰੀ = 파일들.get(정규이름(ਨਾਂ));
        if (ਸਮੱਗਰੀ == null) {
            return null;
        }
        return new 열린파일(ਸਮੱਗਰੀ);
    }

    public boolean 존재함(String ਨਾਂ) {
        return 파일들.containsKey(정규이름(ਨਾਂ));
    }

    public ਲਿਖਤ_ਪੱਤਰ_ਜਾਣਕਾਰੀ ਸਿਸਟਮ_ਜਾਣਕਾਰੀ(String ਨਾਂ) {
        byte[] ਸਮੱਗਰੀ = 파일들.get(정규이름(ਨਾਂ));
        if (ਸਮੱਗਰੀ == null) {
            return null;
        }
        return new ਲਿਖਤ_ਪੱਤਰ_ਜਾਣਕਾਰੀ(ਸਮੱਗਰੀ.length, 0100444);
    }

    private String 정규이름(String ਨਾਂ) {
        if (ਨਾਂ == null) {
            throw new NullPointerException("ਫਾਇਲ 이름이 없습니다.");
        }
        String ਮਾਪ = ਨਾਂ.startsWith("/") ? ਨਾਂ.substring(1) : ਨਾਂ;
        return ਮਾਪ.toUpperCase(Locale.ROOT);
    }
}
