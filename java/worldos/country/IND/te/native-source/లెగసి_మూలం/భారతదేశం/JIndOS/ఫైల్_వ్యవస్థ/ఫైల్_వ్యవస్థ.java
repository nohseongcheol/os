// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.ఫైల్_వ్యవస్థ;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT చదువు 계층과 같은 చదువు 전용 దస్త్రం 저장소의 관리 모델이다. */
public final class ఫైల్_వ్యవస్థ {
    static final class 열린파일 {
        final byte[] డేటా;
        int స్థానము;
        int 참조수 = 1;

        열린파일(byte[] డేటా) {
            this.డేటా = డేటా;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String పేరు, byte[] డేటా) {
        파일들.put(정규이름(పేరు), Arrays.copyOf(డేటా, డేటా.length));
    }

    열린파일 తెరువు(String పేరు) {
        byte[] డేటా = 파일들.get(정규이름(పేరు));
        if (డేటా == null) {
            return null;
        }
        return new 열린파일(డేటా);
    }

    public boolean 존재함(String పేరు) {
        return 파일들.containsKey(정규이름(పేరు));
    }

    public ఫైలు_సమాచారం సిస్టమ్_సమాచారం(String పేరు) {
        byte[] డేటా = 파일들.get(정규이름(పేరు));
        if (డేటా == null) {
            return null;
        }
        return new ఫైలు_సమాచారం(డేటా.length, 0100444);
    }

    private String 정규이름(String పేరు) {
        if (పేరు == null) {
            throw new NullPointerException("దస్త్రం 이름이 없습니다.");
        }
        String ప్రమాణం = పేరు.startsWith("/") ? పేరు.substring(1) : పేరు;
        return ప్రమాణం.toUpperCase(Locale.ROOT);
    }
}
