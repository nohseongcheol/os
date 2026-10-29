// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Schweiz.JCheOS.Speicherraum;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** Verwaltet ausgerichtete Vergabe, Freigabe und Zusammenführung physischen Speichers. */
public final class SpeicherVerwalter {
    private final byte[] Speicherraum;
    private final TreeMap<Integer, Integer> leerwertGebiet = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> benutztGebiet = new TreeMap<Integer, Integer>();

    public SpeicherVerwalter(int gesamtwertGröße) {
        if (gesamtwertGröße < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Speicherraum = new byte[gesamtwertGröße];
        leerwertGebiet.put(Integer.valueOf(4096), Integer.valueOf(gesamtwertGröße - 4096));
    }

    public synchronized int speichergerätZuteilen(int größe) {
        return ausgerichtetZuteilen(größe, 1);
    }

    public synchronized int ausgerichtetZuteilen(int größe, int ausrichtenWert) {
        if (größe <= 0 || ausrichtenWert <= 0 || (ausrichtenWert & (ausrichtenWert - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> eintragWert : leerwertGebiet.entrySet()) {
            int ausführenVorgang = eintragWert.getKey().intValue();
            int gebietGröße = eintragWert.getValue().intValue();
            int ausgerichtetStarten = (ausführenVorgang + ausrichtenWert - 1) & -ausrichtenWert;
            int vorderseiteWertGröße = ausgerichtetStarten - ausführenVorgang;
            int abschließendGröße = gebietGröße - vorderseiteWertGröße - größe;
            if (abschließendGröße < 0) {
                continue;
            }
            leerwertGebiet.remove(Integer.valueOf(ausführenVorgang));
            if (vorderseiteWertGröße > 0) {
                leerwertGebiet.put(Integer.valueOf(ausführenVorgang), Integer.valueOf(vorderseiteWertGröße));
            }
            if (abschließendGröße > 0) {
                leerwertGebiet.put(Integer.valueOf(ausgerichtetStarten + größe), Integer.valueOf(abschließendGröße));
            }
            benutztGebiet.put(Integer.valueOf(ausgerichtetStarten), Integer.valueOf(größe));
            Arrays.fill(Speicherraum, ausgerichtetStarten, ausgerichtetStarten + größe, (byte) 0);
            return ausgerichtetStarten;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void speichergerätFreigeben(int adresse) {
        Integer größeObjekt = benutztGebiet.remove(Integer.valueOf(adresse));
        if (größeObjekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ausführenVorgang = adresse;
        int größe = größeObjekt.intValue();
        Map.Entry<Integer, Integer> vorderseiteWert = leerwertGebiet.lowerEntry(Integer.valueOf(ausführenVorgang));
        if (vorderseiteWert != null && vorderseiteWert.getKey().intValue() + vorderseiteWert.getValue().intValue() == ausführenVorgang) {
            ausführenVorgang = vorderseiteWert.getKey().intValue();
            größe += vorderseiteWert.getValue().intValue();
            leerwertGebiet.remove(vorderseiteWert.getKey());
        }
        Map.Entry<Integer, Integer> rückseiteWert = leerwertGebiet.ceilingEntry(Integer.valueOf(ausführenVorgang));
        if (rückseiteWert != null && ausführenVorgang + größe == rückseiteWert.getKey().intValue()) {
            größe += rückseiteWert.getValue().intValue();
            leerwertGebiet.remove(rückseiteWert.getKey());
        }
        leerwertGebiet.put(Integer.valueOf(ausführenVorgang), Integer.valueOf(größe));
    }

    public synchronized byte byteWertLesen(int adresse) {
        bereichPrüfen(adresse, 1);
        return Speicherraum[adresse];
    }

    public synchronized void byteWertSchreiben(int adresse, byte Wert) {
        bereichPrüfen(adresse, 1);
        Speicherraum[adresse] = Wert;
    }

    public synchronized int gesamtwertGröße() {
        return Speicherraum.length;
    }

    public synchronized int benutztGröße() {
        int gesamtwertWert = 0;
        for (Integer größe : benutztGebiet.values()) {
            gesamtwertWert += größe.intValue();
        }
        return gesamtwertWert;
    }

    private void bereichPrüfen(int adresse, int größe) {
        if (adresse < 0 || größe < 0 || adresse > Speicherraum.length - größe) {
            throw new IndexOutOfBoundsException("Speicherraum 범위를 벗어났습니다.");
        }
    }
}

