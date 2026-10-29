// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.datotečni_sustav;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Čitaj 계층과 같은 Čitaj 전용 Datoteka 저장소의 관리 모델이다. */
public final class datotečni_sustav {
    static final class 열린파일 {
        final byte[] podaci;
        int Položaj;
        int Reference_COUNT = 1;

        열린파일(byte[] podaci) {
            this.podaci = podaci;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void dodati_Datoteka(String Ime, byte[] podaci) {
        파일들.put(kanonski_naziv(Ime), Arrays.copyOf(podaci, podaci.length));
    }

    열린파일 Otvori(String Ime) {
        byte[] podaci = 파일들.get(kanonski_naziv(Ime));
        if (podaci == null) {
            return null;
        }
        return new 열린파일(podaci);
    }

    public boolean 존재함(String Ime) {
        return 파일들.containsKey(kanonski_naziv(Ime));
    }

    public Datoteka_informacija Podaci_o_sustavu(String Ime) {
        byte[] podaci = 파일들.get(kanonski_naziv(Ime));
        if (podaci == null) {
            return null;
        }
        return new Datoteka_informacija(podaci.length, 0100444);
    }

    private String kanonski_naziv(String Ime) {
        if (Ime == null) {
            throw new NullPointerException("Datoteka 이름이 없습니다.");
        }
        String REZULTAT = Ime.startsWith("/") ? Ime.substring(1) : Ime;
        return REZULTAT.toUpperCase(Locale.ROOT);
    }
}
