// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class grenzstellenPrüfung {
    static int fehlschlagWert() { throw new IllegalStateException("Aufgabe 중 ausnahme"); }
    public static void main(String[] a) throws Exception {
        Object klartextDatenfeld = new Object[2]; System.out.println(klartextDatenfeld instanceof String[]);
        try { String[] ungültigErgebnis = (String[])klartextDatenfeld; } catch (ClassCastException e) { System.out.println("datenfeldWert wertUmwandeln Prüfpunkte"); }
        Object[] textListe = new String[2];
        try { textListe[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("datenfeldWert typWert Prüfpunkte"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, textListe, 0, 2); } catch (ArrayStoreException e) { System.out.println("wertKopieren typWert Prüfpunkte"); }
        System.out.println((String)textListe[0]);
        try { "Text".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("Zeichen beschneiden"); }
        Integer einsWert = Integer.valueOf(127), zweiWert = Integer.valueOf(127); System.out.println(einsWert == zweiWert);
        Object sperreWert = new Object(); try { synchronized (sperreWert) { fehlschlagWert(); } } catch (IllegalStateException e) { System.out.println("sperreWert ausnahme"); }
        synchronized (sperreWert) { System.out.println("sperreWert 회수"); }
        byte[] Daten = {0, (byte)128, (byte)255, 10};
        FileOutputStream Ausgabe = new FileOutputStream("byteWert.bin"); Ausgabe.write(Daten); Ausgabe.flush(); Ausgabe.close();
        FileInputStream Eingabewert = new FileInputStream("byteWert.bin"); byte[] ergebnisLesen = new byte[8];
        System.out.println(Eingabewert.read(ergebnisLesen, 2, 4)); System.out.println(ergebnisLesen[3] + ":" + ergebnisLesen[4]);
        System.out.println(Eingabewert.read(ergebnisLesen)); System.out.println(Eingabewert.read(ergebnisLesen, 0, 0)); Eingabewert.close();
        try { Eingabewert.read(); } catch (IOException e) { System.out.println("닫힌 Datei"); }
    }
}
