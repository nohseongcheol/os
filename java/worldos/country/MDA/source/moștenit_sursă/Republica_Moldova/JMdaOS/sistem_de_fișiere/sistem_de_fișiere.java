// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republica_Moldova.JMdaOS.sistem_de_fișiere;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Citire 계층과 같은 Citire 전용 Fișier 저장소의 관리 모델이다. */
public final class sistem_de_fișiere {
    static final class 열린파일 {
        final byte[] date;
        int Poziție;
        int referință_COUNT = 1;

        열린파일(byte[] date) {
            this.date = date;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void adăuga_Fișier(String Nume, byte[] date) {
        파일들.put(nume_canonic(Nume), Arrays.copyOf(date, date.length));
    }

    열린파일 Deschide(String Nume) {
        byte[] date = 파일들.get(nume_canonic(Nume));
        if (date == null) {
            return null;
        }
        return new 열린파일(date);
    }

    public boolean 존재함(String Nume) {
        return 파일들.containsKey(nume_canonic(Nume));
    }

    public Fișier_info msinfo32_exe(String Nume) {
        byte[] date = 파일들.get(nume_canonic(Nume));
        if (date == null) {
            return null;
        }
        return new Fișier_info(date.length, 0100444);
    }

    private String nume_canonic(String Nume) {
        if (Nume == null) {
            throw new NullPointerException("Fișier 이름이 없습니다.");
        }
        String KR = Nume.startsWith("/") ? Nume.substring(1) : Nume;
        return KR.toUpperCase(Locale.ROOT);
    }
}
