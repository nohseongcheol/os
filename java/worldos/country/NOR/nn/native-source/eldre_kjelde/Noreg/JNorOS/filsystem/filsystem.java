// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.filsystem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Les 계층과 같은 Les 전용 Fil 저장소의 관리 모델이다. */
public final class filsystem {
    static final class 열린파일 {
        final byte[] data;
        int Posisjon;
        int Oppslagsverk_COUNT = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Namn, byte[] data) {
        파일들.put(정규이름(Namn), Arrays.copyOf(data, data.length));
    }

    열린파일 Opna(String Namn) {
        byte[] data = 파일들.get(정규이름(Namn));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Namn) {
        return 파일들.containsKey(정규이름(Namn));
    }

    public fil_informasjon msinfo32_exe(String Namn) {
        byte[] data = 파일들.get(정규이름(Namn));
        if (data == null) {
            return null;
        }
        return new fil_informasjon(data.length, 0100444);
    }

    private String 정규이름(String Namn) {
        if (Namn == null) {
            throw new NullPointerException("Fil 이름이 없습니다.");
        }
        String forretningsmål = Namn.startsWith("/") ? Namn.substring(1) : Namn;
        return forretningsmål.toUpperCase(Locale.ROOT);
    }
}
