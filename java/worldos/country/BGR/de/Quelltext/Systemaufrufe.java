// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BGR.l_de;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class Systemaufrufe {
    private Systemaufrufe() { }
    public static RandomAccessFile öffnen(String Pfad, String Modus) throws IOException {
        return new RandomAccessFile(Pfad, Modus);
    }
    public static int lesen(RandomAccessFile Datei, byte[] Daten) throws IOException {
        return Datei.read(Daten);
    }
    public static void schreiben(RandomAccessFile Datei, byte[] Daten) throws IOException {
        Datei.write(Daten);
    }
    public static void positionieren(RandomAccessFile Datei, long Position) throws IOException {
        Datei.seek(Position);
    }
    public static void abgleichen(RandomAccessFile Datei) throws IOException {
        Datei.getFD().sync();
    }
    public static void schließen(RandomAccessFile Datei) throws IOException {
        Datei.close();
    }
    public static void entfernen(String Pfad) throws IOException {
        Files.delete(Paths.get(Pfad));
    }
    public static long Größe(String Pfad) throws IOException {
        return Files.size(Paths.get(Pfad));
    }
    public static Socket verbinden(String Adresse, int Anschlussnummer) throws IOException {
        return new Socket(Adresse, Anschlussnummer);
    }
    public static DatagramSocket Datagramm(int Anschlussnummer) throws SocketException {
        return new DatagramSocket(Anschlussnummer);
    }
    public static Thread Ausführungsfaden(Runnable Aktion) {
        Thread Ausführungsfaden = new Thread(Aktion);
        Ausführungsfaden.start();
        return Ausführungsfaden;
    }
    public static Process ausführen(List<String> Befehl) throws IOException {
        return new ProcessBuilder(Befehl).start();
    }
}
