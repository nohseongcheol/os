// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.የፋይል_ስርዓት;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT ማንበቢያ 계층과 같은 ማንበቢያ 전용 ፋይል 저장소의 관리 모델이다. */
public final class የፋይል_ስርዓት {
    static final class 열린파일 {
        final byte[] ውሂብ;
        int አካባቢ;
        int 참조수 = 1;

        열린파일(byte[] ውሂብ) {
            this.ውሂብ = ውሂብ;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ስም, byte[] ውሂብ) {
        파일들.put(정규이름(ስም), Arrays.copyOf(ውሂብ, ውሂብ.length));
    }

    열린파일 መክፈቻ(String ስም) {
        byte[] ውሂብ = 파일들.get(정규이름(ስም));
        if (ውሂብ == null) {
            return null;
        }
        return new 열린파일(ውሂብ);
    }

    public boolean 존재함(String ስም) {
        return 파일들.containsKey(정규이름(ስም));
    }

    public ፋይል_መረጃ የስርዓት_መረጃ(String ስም) {
        byte[] ውሂብ = 파일들.get(정규이름(ስም));
        if (ውሂብ == null) {
            return null;
        }
        return new ፋይል_መረጃ(ውሂብ.length, 0100444);
    }

    private String 정규이름(String ስም) {
        if (ስም == null) {
            throw new NullPointerException("ፋይል 이름이 없습니다.");
        }
        String ልኬት = ስም.startsWith("/") ? ስም.substring(1) : ስም;
        return ልኬት.toUpperCase(Locale.ROOT);
    }
}
