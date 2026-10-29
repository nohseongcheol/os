// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukraina.JUkrOS.system_plików;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Odczyt 계층과 같은 Odczyt 전용 nazwa_pliku 저장소의 관리 모델이다. */
public final class system_plików {
    static final class 열린파일 {
        final byte[] dane;
        int pozycja;
        int odwołanie_ILE_LICZB = 1;

        열린파일(byte[] dane) {
            this.dane = dane;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void dołączać_Plik(String Nazwa, byte[] dane) {
        파일들.put(nazwa_kanoniczna(Nazwa), Arrays.copyOf(dane, dane.length));
    }

    열린파일 Otwórz(String Nazwa) {
        byte[] dane = 파일들.get(nazwa_kanoniczna(Nazwa));
        if (dane == null) {
            return null;
        }
        return new 열린파일(dane);
    }

    public boolean 존재함(String Nazwa) {
        return 파일들.containsKey(nazwa_kanoniczna(Nazwa));
    }

    public Plik_informacje msinfo32_exe(String Nazwa) {
        byte[] dane = 파일들.get(nazwa_kanoniczna(Nazwa));
        if (dane == null) {
            return null;
        }
        return new Plik_informacje(dane.length, 0100444);
    }

    private String nazwa_kanoniczna(String Nazwa) {
        if (Nazwa == null) {
            throw new NullPointerException("nazwa_pliku 이름이 없습니다.");
        }
        String WYNIK = Nazwa.startsWith("/") ? Nazwa.substring(1) : Nazwa;
        return WYNIK.toUpperCase(Locale.ROOT);
    }
}
