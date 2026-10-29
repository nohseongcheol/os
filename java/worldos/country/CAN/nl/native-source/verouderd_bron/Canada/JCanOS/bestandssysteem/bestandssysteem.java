// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.bestandssysteem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Lezen 계층과 같은 Lezen 전용 bestand 저장소의 관리 모델이다. */
public final class bestandssysteem {
    static final class 열린파일 {
        final byte[] gegevens;
        int positie;
        int verwijzen_AANTAL = 1;

        열린파일(byte[] gegevens) {
            this.gegevens = gegevens;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void toevoegen_Bestand(String Naam, byte[] gegevens) {
        파일들.put(canonieke_naam(Naam), Arrays.copyOf(gegevens, gegevens.length));
    }

    열린파일 Openen(String Naam) {
        byte[] gegevens = 파일들.get(canonieke_naam(Naam));
        if (gegevens == null) {
            return null;
        }
        return new 열린파일(gegevens);
    }

    public boolean 존재함(String Naam) {
        return 파일들.containsKey(canonieke_naam(Naam));
    }

    public Bestand_info msinfo32_exe(String Naam) {
        byte[] gegevens = 파일들.get(canonieke_naam(Naam));
        if (gegevens == null) {
            return null;
        }
        return new Bestand_info(gegevens.length, 0100444);
    }

    private String canonieke_naam(String Naam) {
        if (Naam == null) {
            throw new NullPointerException("bestand 이름이 없습니다.");
        }
        String resultaat = Naam.startsWith("/") ? Naam.substring(1) : Naam;
        return resultaat.toUpperCase(Locale.ROOT);
    }
}
