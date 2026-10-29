// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frantzia.JFraOS.fitxategi_sistema;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Irakurri 계층과 같은 Irakurri 전용 Fitxategia 저장소의 관리 모델이다. */
public final class fitxategi_sistema {
    static final class 열린파일 {
        final byte[] datuak;
        int Posizioa;
        int Erreferentzia_materiala_ZENBATU = 1;

        열린파일(byte[] datuak) {
            this.datuak = datuak;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Erantsi_fitxategi(String Izena, byte[] datuak) {
        파일들.put(정규이름(Izena), Arrays.copyOf(datuak, datuak.length));
    }

    열린파일 Ireki(String Izena) {
        byte[] datuak = 파일들.get(정규이름(Izena));
        if (datuak == null) {
            return null;
        }
        return new 열린파일(datuak);
    }

    public boolean 존재함(String Izena) {
        return 파일들.containsKey(정규이름(Izena));
    }

    public fitxategi_info msinfo32_exe(String Izena) {
        byte[] datuak = 파일들.get(정규이름(Izena));
        if (datuak == null) {
            return null;
        }
        return new fitxategi_info(datuak.length, 0100444);
    }

    private String 정규이름(String Izena) {
        if (Izena == null) {
            throw new NullPointerException("Fitxategia 이름이 없습니다.");
        }
        String EMAITZA = Izena.startsWith("/") ? Izena.substring(1) : Izena;
        return EMAITZA.toUpperCase(Locale.ROOT);
    }
}
