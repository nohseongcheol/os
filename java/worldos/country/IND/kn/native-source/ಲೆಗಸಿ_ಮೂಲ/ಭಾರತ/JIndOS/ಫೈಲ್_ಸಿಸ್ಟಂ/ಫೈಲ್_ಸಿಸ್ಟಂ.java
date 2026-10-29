// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ಫೈಲ್_ಸಿಸ್ಟಂ;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT ಓದು 계층과 같은 ಓದು 전용 ಕಡತ 저장소의 관리 모델이다. */
public final class ಫೈಲ್_ಸಿಸ್ಟಂ {
    static final class 열린파일 {
        final byte[] ಡೇಟಾ;
        int ಸ್ಥಾನ;
        int 참조수 = 1;

        열린파일(byte[] ಡೇಟಾ) {
            this.ಡೇಟಾ = ಡೇಟಾ;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ಹೆಸರು, byte[] ಡೇಟಾ) {
        파일들.put(정규이름(ಹೆಸರು), Arrays.copyOf(ಡೇಟಾ, ಡೇಟಾ.length));
    }

    열린파일 ತೆರೆ(String ಹೆಸರು) {
        byte[] ಡೇಟಾ = 파일들.get(정규이름(ಹೆಸರು));
        if (ಡೇಟಾ == null) {
            return null;
        }
        return new 열린파일(ಡೇಟಾ);
    }

    public boolean 존재함(String ಹೆಸರು) {
        return 파일들.containsKey(정규이름(ಹೆಸರು));
    }

    public ಫೈಲ್_ಮಾಹಿತಿ ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ(String ಹೆಸರು) {
        byte[] ಡೇಟಾ = 파일들.get(정규이름(ಹೆಸರು));
        if (ಡೇಟಾ == null) {
            return null;
        }
        return new ಫೈಲ್_ಮಾಹಿತಿ(ಡೇಟಾ.length, 0100444);
    }

    private String 정규이름(String ಹೆಸರು) {
        if (ಹೆಸರು == null) {
            throw new NullPointerException("ಕಡತ 이름이 없습니다.");
        }
        String ಮಾಪನ = ಹೆಸರು.startsWith("/") ? ಹೆಸರು.substring(1) : ಹೆಸರು;
        return ಮಾಪನ.toUpperCase(Locale.ROOT);
    }
}
