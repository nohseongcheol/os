// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Island.JIslOS.filsystem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Læse 계층과 같은 Læse 전용 Fil 저장소의 관리 모델이다. */
public final class filsystem {
    static final class 열린파일 {
        final byte[] data;
        int Placering;
        int referere_TÆL = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void tilføj_fil(String Navn, byte[] data) {
        파일들.put(vedtaget_navn(Navn), Arrays.copyOf(data, data.length));
    }

    열린파일 Åbn(String Navn) {
        byte[] data = 파일들.get(vedtaget_navn(Navn));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Navn) {
        return 파일들.containsKey(vedtaget_navn(Navn));
    }

    public fil_info msinfo32_exe(String Navn) {
        byte[] data = 파일들.get(vedtaget_navn(Navn));
        if (data == null) {
            return null;
        }
        return new fil_info(data.length, 0100444);
    }

    private String vedtaget_navn(String Navn) {
        if (Navn == null) {
            throw new NullPointerException("Fil 이름이 없습니다.");
        }
        String KR = Navn.startsWith("/") ? Navn.substring(1) : Navn;
        return KR.toUpperCase(Locale.ROOT);
    }
}
