// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package இந்தியா.JIndOS.கோப்பு_முறைமை;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT படி 계층과 같은 படி 전용 கோப்பின்_பெயர் 저장소의 관리 모델이다. */
public final class கோப்பு_முறைமை {
    static final class 열린파일 {
        final byte[] தரவு;
        int இடம்;
        int 참조수 = 1;

        열린파일(byte[] தரவு) {
            this.தரவு = தரவு;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String பெயர், byte[] தரவு) {
        파일들.put(정규이름(பெயர்), Arrays.copyOf(தரவு, தரவு.length));
    }

    열린파일 திற(String பெயர்) {
        byte[] தரவு = 파일들.get(정규이름(பெயர்));
        if (தரவு == null) {
            return null;
        }
        return new 열린파일(தரவு);
    }

    public boolean 존재함(String பெயர்) {
        return 파일들.containsKey(정규이름(பெயர்));
    }

    public கோப்பு_தகவல் கணினித்_தகவல்(String பெயர்) {
        byte[] தரவு = 파일들.get(정규이름(பெயர்));
        if (தரவு == null) {
            return null;
        }
        return new கோப்பு_தகவல்(தரவு.length, 0100444);
    }

    private String 정규이름(String பெயர்) {
        if (பெயர் == null) {
            throw new NullPointerException("கோப்பின்_பெயர் 이름이 없습니다.");
        }
        String அளவிடக்கூடியது = பெயர்.startsWith("/") ? பெயர்.substring(1) : பெயர்;
        return அளவிடக்கூடியது.toUpperCase(Locale.ROOT);
    }
}
