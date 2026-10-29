// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.failu_sistēma;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Lasīt 계층과 같은 Lasīt 전용 Fails 저장소의 관리 모델이다. */
public final class failu_sistēma {
    static final class 열린파일 {
        final byte[] dati;
        int Novietojums;
        int Uzziņas_COUNT = 1;

        열린파일(byte[] dati) {
            this.dati = dati;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Pievienot_Fails(String Nosaukums, byte[] dati) {
        파일들.put(kanoniskais_nosaukums(Nosaukums), Arrays.copyOf(dati, dati.length));
    }

    열린파일 Atvērt(String Nosaukums) {
        byte[] dati = 파일들.get(kanoniskais_nosaukums(Nosaukums));
        if (dati == null) {
            return null;
        }
        return new 열린파일(dati);
    }

    public boolean 존재함(String Nosaukums) {
        return 파일들.containsKey(kanoniskais_nosaukums(Nosaukums));
    }

    public Fails_informācija msinfo32_exe(String Nosaukums) {
        byte[] dati = 파일들.get(kanoniskais_nosaukums(Nosaukums));
        if (dati == null) {
            return null;
        }
        return new Fails_informācija(dati.length, 0100444);
    }

    private String kanoniskais_nosaukums(String Nosaukums) {
        if (Nosaukums == null) {
            throw new NullPointerException("Fails 이름이 없습니다.");
        }
        String mērs = Nosaukums.startsWith("/") ? Nosaukums.substring(1) : Nosaukums;
        return mērs.toUpperCase(Locale.ROOT);
    }
}
