// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package iLesotho.JLsoOS.isistimu_yefayela;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Funda 계층과 같은 Funda 전용 Ihele 저장소의 관리 모델이다. */
public final class isistimu_yefayela {
    static final class 열린파일 {
        final byte[] imininingwane;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] imininingwane) {
            this.imininingwane = imininingwane;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Igama, byte[] imininingwane) {
        파일들.put(정규이름(Igama), Arrays.copyOf(imininingwane, imininingwane.length));
    }

    열린파일 Vula(String Igama) {
        byte[] imininingwane = 파일들.get(정규이름(Igama));
        if (imininingwane == null) {
            return null;
        }
        return new 열린파일(imininingwane);
    }

    public boolean 존재함(String Igama) {
        return 파일들.containsKey(정규이름(Igama));
    }

    public ifayela_ulwazi I_msinfo32_exe(String Igama) {
        byte[] imininingwane = 파일들.get(정규이름(Igama));
        if (imininingwane == null) {
            return null;
        }
        return new ifayela_ulwazi(imininingwane.length, 0100444);
    }

    private String 정규이름(String Igama) {
        if (Igama == null) {
            throw new NullPointerException("Ihele 이름이 없습니다.");
        }
        String 결과 = Igama.startsWith("/") ? Igama.substring(1) : Igama;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
