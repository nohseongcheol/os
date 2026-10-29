// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.lêerstelsel;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Lees 계층과 같은 Lees 전용 Lêer 저장소의 관리 모델이다. */
public final class lêerstelsel {
    static final class 열린파일 {
        final byte[] data;
        int Posisie;
        int Naslaan_COUNT = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Naam, byte[] data) {
        파일들.put(정규이름(Naam), Arrays.copyOf(data, data.length));
    }

    열린파일 skep(String Naam) {
        byte[] data = 파일들.get(정규이름(Naam));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Naam) {
        return 파일들.containsKey(정규이름(Naam));
    }

    public lêer_inligting Stelselinfo(String Naam) {
        byte[] data = 파일들.get(정규이름(Naam));
        if (data == null) {
            return null;
        }
        return new lêer_inligting(data.length, 0100444);
    }

    private String 정규이름(String Naam) {
        if (Naam == null) {
            throw new NullPointerException("Lêer 이름이 없습니다.");
        }
        String maatreël = Naam.startsWith("/") ? Naam.substring(1) : Naam;
        return maatreël.toUpperCase(Locale.ROOT);
    }
}
