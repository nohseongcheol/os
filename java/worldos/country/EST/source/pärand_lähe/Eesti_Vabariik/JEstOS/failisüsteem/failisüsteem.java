// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.failisüsteem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Lugemine 계층과 같은 Lugemine 전용 Fail 저장소의 관리 모델이다. */
public final class failisüsteem {
    static final class 열린파일 {
        final byte[] andmed;
        int Asukoht;
        int viide_COUNT = 1;

        열린파일(byte[] andmed) {
            this.andmed = andmed;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Lisa_Fail(String Nimi_2, byte[] andmed) {
        파일들.put(kanooniline_nimi(Nimi_2), Arrays.copyOf(andmed, andmed.length));
    }

    열린파일 Ava(String Nimi_2) {
        byte[] andmed = 파일들.get(kanooniline_nimi(Nimi_2));
        if (andmed == null) {
            return null;
        }
        return new 열린파일(andmed);
    }

    public boolean 존재함(String Nimi_2) {
        return 파일들.containsKey(kanooniline_nimi(Nimi_2));
    }

    public Fail_teave msinfo32_exe(String Nimi_2) {
        byte[] andmed = 파일들.get(kanooniline_nimi(Nimi_2));
        if (andmed == null) {
            return null;
        }
        return new Fail_teave(andmed.length, 0100444);
    }

    private String kanooniline_nimi(String Nimi_2) {
        if (Nimi_2 == null) {
            throw new NullPointerException("Fail 이름이 없습니다.");
        }
        String TULEMUS = Nimi_2.startsWith("/") ? Nimi_2.substring(1) : Nimi_2;
        return TULEMUS.toUpperCase(Locale.ROOT);
    }
}
