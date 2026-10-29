// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Srbija.JSrbOS.sistem_datoteka;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 Datoteka 저장소의 관리 모델이다. */
public final class sistem_datoteka {
    static final class 열린파일 {
        final byte[] podaci;
        int pozicija;
        int referenca_COUNT = 1;

        열린파일(byte[] podaci) {
            this.podaci = podaci;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void dodati_Datoteka(String ime, byte[] podaci) {
        파일들.put(kanonsko_ime(ime), Arrays.copyOf(podaci, podaci.length));
    }

    열린파일 otvoren(String ime) {
        byte[] podaci = 파일들.get(kanonsko_ime(ime));
        if (podaci == null) {
            return null;
        }
        return new 열린파일(podaci);
    }

    public boolean 존재함(String ime) {
        return 파일들.containsKey(kanonsko_ime(ime));
    }

    public Datoteka_informacije msinfo32_exe(String ime) {
        byte[] podaci = 파일들.get(kanonsko_ime(ime));
        if (podaci == null) {
            return null;
        }
        return new Datoteka_informacije(podaci.length, 0100444);
    }

    private String kanonsko_ime(String ime) {
        if (ime == null) {
            throw new NullPointerException("Datoteka 이름이 없습니다.");
        }
        String KR = ime.startsWith("/") ? ime.substring(1) : ime;
        return KR.toUpperCase(Locale.ROOT);
    }
}
