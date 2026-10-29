// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.datotečni_sistem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Branje 계층과 같은 Branje 전용 Datoteka 저장소의 관리 모델이다. */
public final class datotečni_sistem {
    static final class 열린파일 {
        final byte[] podatki;
        int Položaj;
        int Gradiva_COUNT = 1;

        열린파일(byte[] podatki) {
            this.podatki = podatki;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void dodati_Datoteka(String Ime, byte[] podatki) {
        파일들.put(kanonično_ime(Ime), Arrays.copyOf(podatki, podatki.length));
    }

    열린파일 Odpri(String Ime) {
        byte[] podatki = 파일들.get(kanonično_ime(Ime));
        if (podatki == null) {
            return null;
        }
        return new 열린파일(podatki);
    }

    public boolean 존재함(String Ime) {
        return 파일들.containsKey(kanonično_ime(Ime));
    }

    public Datoteka_informacije msinfo32_exe(String Ime) {
        byte[] podatki = 파일들.get(kanonično_ime(Ime));
        if (podatki == null) {
            return null;
        }
        return new Datoteka_informacije(podatki.length, 0100444);
    }

    private String kanonično_ime(String Ime) {
        if (Ime == null) {
            throw new NullPointerException("Datoteka 이름이 없습니다.");
        }
        String REZULTAT = Ime.startsWith("/") ? Ime.substring(1) : Ime;
        return REZULTAT.toUpperCase(Locale.ROOT);
    }
}
