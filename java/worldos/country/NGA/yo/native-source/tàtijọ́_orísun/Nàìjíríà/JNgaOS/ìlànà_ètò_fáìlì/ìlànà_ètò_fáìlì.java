// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nàìjíríà.JNgaOS.ìlànà_ètò_fáìlì;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Kàá 계층과 같은 Kàá 전용 Fáìlì 저장소의 관리 모델이다. */
public final class ìlànà_ètò_fáìlì {
    static final class 열린파일 {
        final byte[] détà;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] détà) {
            this.détà = détà;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Orúkọ, byte[] détà) {
        파일들.put(정규이름(Orúkọ), Arrays.copyOf(détà, détà.length));
    }

    열린파일 Ṣi(String Orúkọ) {
        byte[] détà = 파일들.get(정규이름(Orúkọ));
        if (détà == null) {
            return null;
        }
        return new 열린파일(détà);
    }

    public boolean 존재함(String Orúkọ) {
        return 파일들.containsKey(정규이름(Orúkọ));
    }

    public fáìlì_Ìwífún msinfo32_exe(String Orúkọ) {
        byte[] détà = 파일들.get(정규이름(Orúkọ));
        if (détà == null) {
            return null;
        }
        return new fáìlì_Ìwífún(détà.length, 0100444);
    }

    private String 정규이름(String Orúkọ) {
        if (Orúkọ == null) {
            throw new NullPointerException("Fáìlì 이름이 없습니다.");
        }
        String 결과 = Orúkọ.startsWith("/") ? Orúkọ.substring(1) : Orúkọ;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
