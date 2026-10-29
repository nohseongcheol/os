// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eýran.JIrnOS.faýl_ulgamy;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Oka 계층과 같은 Oka 전용 Faýl 저장소의 관리 모델이다. */
public final class faýl_ulgamy {
    static final class 열린파일 {
        final byte[] maglumat;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] maglumat) {
            this.maglumat = maglumat;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Ad, byte[] maglumat) {
        파일들.put(정규이름(Ad), Arrays.copyOf(maglumat, maglumat.length));
    }

    열린파일 Aç(String Ad) {
        byte[] maglumat = 파일들.get(정규이름(Ad));
        if (maglumat == null) {
            return null;
        }
        return new 열린파일(maglumat);
    }

    public boolean 존재함(String Ad) {
        return 파일들.containsKey(정규이름(Ad));
    }

    public faýl_maglumat msinfo32_exe(String Ad) {
        byte[] maglumat = 파일들.get(정규이름(Ad));
        if (maglumat == null) {
            return null;
        }
        return new faýl_maglumat(maglumat.length, 0100444);
    }

    private String 정규이름(String Ad) {
        if (Ad == null) {
            throw new NullPointerException("Faýl 이름이 없습니다.");
        }
        String 결과 = Ad.startsWith("/") ? Ad.substring(1) : Ad;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
