// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Luxemburg.JLuxOS.DateiSystem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** Verwaltetes Modell eines schreibgeschützten Dateispeichers entsprechend der engos-FAT-Leseschicht. */
public final class DateiSystem {
    static final class geöffnetDatei {
        final byte[] Daten;
        int position;
        int verweisAnzahl = 1;

        geöffnetDatei(byte[] Daten) {
            this.Daten = Daten;
        }
    }

    private final Map<String, byte[]> dateiEinträge = new LinkedHashMap<String, byte[]>();

    public void dateiAnhängen(String Name, byte[] Daten) {
        dateiEinträge.put(kanonischName(Name), Arrays.copyOf(Daten, Daten.length));
    }

    geöffnetDatei öffnen(String Name) {
        byte[] Daten = dateiEinträge.get(kanonischName(Name));
        if (Daten == null) {
            return null;
        }
        return new geöffnetDatei(Daten);
    }

    public boolean existiertWert(String Name) {
        return dateiEinträge.containsKey(kanonischName(Name));
    }

    public dateiInformation systemInformation(String Name) {
        byte[] Daten = dateiEinträge.get(kanonischName(Name));
        if (Daten == null) {
            return null;
        }
        return new dateiInformation(Daten.length, 0100444);
    }

    private String kanonischName(String Name) {
        if (Name == null) {
            throw new NullPointerException("Datei 이름이 없습니다.");
        }
        String ergebnis = Name.startsWith("/") ? Name.substring(1) : Name;
        return ergebnis.toUpperCase(Locale.ROOT);
    }
}
