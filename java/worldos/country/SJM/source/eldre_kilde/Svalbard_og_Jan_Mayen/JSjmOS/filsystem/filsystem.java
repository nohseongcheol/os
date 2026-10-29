// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.filsystem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Les 계층과 같은 Les 전용 Fil 저장소의 관리 모델이다. */
public final class filsystem {
    static final class 열린파일 {
        final byte[] data;
        int Posisjon;
        int referere_ANTALL = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Tilføye_Fil(String Navn, byte[] data) {
        파일들.put(kanonisk_navn(Navn), Arrays.copyOf(data, data.length));
    }

    열린파일 Åpne(String Navn) {
        byte[] data = 파일들.get(kanonisk_navn(Navn));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Navn) {
        return 파일들.containsKey(kanonisk_navn(Navn));
    }

    public Fil_info msinfo32_exe(String Navn) {
        byte[] data = 파일들.get(kanonisk_navn(Navn));
        if (data == null) {
            return null;
        }
        return new Fil_info(data.length, 0100444);
    }

    private String kanonisk_navn(String Navn) {
        if (Navn == null) {
            throw new NullPointerException("Fil 이름이 없습니다.");
        }
        String KR = Navn.startsWith("/") ? Navn.substring(1) : Navn;
        return KR.toUpperCase(Locale.ROOT);
    }
}
