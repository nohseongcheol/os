// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ruotsi.JSweOS.tiedostojärjestelmä;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Luku 계층과 같은 Luku 전용 tiedoston_nimi 저장소의 관리 모델이다. */
public final class tiedostojärjestelmä {
    static final class 열린파일 {
        final byte[] data;
        int paikka;
        int viite_LASKE = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void liitä_Tiedosto(String Nimi, byte[] data) {
        파일들.put(kanoninen_nimi(Nimi), Arrays.copyOf(data, data.length));
    }

    열린파일 Avaa(String Nimi) {
        byte[] data = 파일들.get(kanoninen_nimi(Nimi));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Nimi) {
        return 파일들.containsKey(kanoninen_nimi(Nimi));
    }

    public Tiedosto_info msinfo32_exe(String Nimi) {
        byte[] data = 파일들.get(kanoninen_nimi(Nimi));
        if (data == null) {
            return null;
        }
        return new Tiedosto_info(data.length, 0100444);
    }

    private String kanoninen_nimi(String Nimi) {
        if (Nimi == null) {
            throw new NullPointerException("tiedoston_nimi 이름이 없습니다.");
        }
        String TULOS = Nimi.startsWith("/") ? Nimi.substring(1) : Nimi;
        return TULOS.toUpperCase(Locale.ROOT);
    }
}
