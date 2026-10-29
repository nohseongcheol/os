// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijeriya.JNgaOS.tsarin_fayil_a_kwamfuta;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Yi_Karatu 계층과 같은 Yi_Karatu 전용 Fayil 저장소의 관리 모델이다. */
public final class tsarin_fayil_a_kwamfuta {
    static final class 열린파일 {
        final byte[] Tarin_bayani;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] Tarin_bayani) {
            this.Tarin_bayani = Tarin_bayani;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Suna, byte[] Tarin_bayani) {
        파일들.put(정규이름(Suna), Arrays.copyOf(Tarin_bayani, Tarin_bayani.length));
    }

    열린파일 Buɗe(String Suna) {
        byte[] Tarin_bayani = 파일들.get(정규이름(Suna));
        if (Tarin_bayani == null) {
            return null;
        }
        return new 열린파일(Tarin_bayani);
    }

    public boolean 존재함(String Suna) {
        return 파일들.containsKey(정규이름(Suna));
    }

    public Fayil_bayani msinfo32_exe(String Suna) {
        byte[] Tarin_bayani = 파일들.get(정규이름(Suna));
        if (Tarin_bayani == null) {
            return null;
        }
        return new Fayil_bayani(Tarin_bayani.length, 0100444);
    }

    private String 정규이름(String Suna) {
        if (Suna == null) {
            throw new NullPointerException("Fayil 이름이 없습니다.");
        }
        String 결과 = Suna.startsWith("/") ? Suna.substring(1) : Suna;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
