// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Y_Deyrnas_Unedig.JGbrOS.system_ffeiliau;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Darllen 계층과 같은 Darllen 전용 Ffeil 저장소의 관리 모델이다. */
public final class system_ffeiliau {
    static final class 열린파일 {
        final byte[] data;
        int safle;
        int cyfeiriad_COUNT = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Enw, byte[] data) {
        파일들.put(정규이름(Enw), Arrays.copyOf(data, data.length));
    }

    열린파일 Agor(String Enw) {
        byte[] data = 파일들.get(정규이름(Enw));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Enw) {
        return 파일들.containsKey(정규이름(Enw));
    }

    public ffeil_gwybodaeth msinfo32_exe(String Enw) {
        byte[] data = 파일들.get(정규이름(Enw));
        if (data == null) {
            return null;
        }
        return new ffeil_gwybodaeth(data.length, 0100444);
    }

    private String 정규이름(String Enw) {
        if (Enw == null) {
            throw new NullPointerException("Ffeil 이름이 없습니다.");
        }
        String mesur = Enw.startsWith("/") ? Enw.substring(1) : Enw;
        return mesur.toUpperCase(Locale.ROOT);
    }
}
