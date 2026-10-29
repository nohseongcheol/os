// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SUR.l_nl;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class systeemaanroep {
    private systeemaanroep() { }
    public static RandomAccessFile Openen(String pad, String Modus) throws IOException {
        return new RandomAccessFile(pad, Modus);
    }
    public static int Lezen(RandomAccessFile bestand, byte[] gegevens) throws IOException {
        return bestand.read(gegevens);
    }
    public static void Schrijven(RandomAccessFile bestand, byte[] gegevens) throws IOException {
        bestand.write(gegevens);
    }
    public static void seek(RandomAccessFile bestand, long positie) throws IOException {
        bestand.seek(positie);
    }
    public static void sync(RandomAccessFile bestand) throws IOException {
        bestand.getFD().sync();
    }
    public static void Sluiten(RandomAccessFile bestand) throws IOException {
        bestand.close();
    }
    public static void Verwijderen(String pad) throws IOException {
        Files.delete(Paths.get(pad));
    }
    public static long Grootte(String pad) throws IOException {
        return Files.size(Paths.get(pad));
    }
    public static Socket Verbinden(String address, int poortnummer) throws IOException {
        return new Socket(address, poortnummer);
    }
    public static DatagramSocket datagram(int poortnummer) throws SocketException {
        return new DatagramSocket(poortnummer);
    }
    public static Thread uitvoeringsdraad(Runnable Actie) {
        Thread uitvoeringsdraad = new Thread(Actie);
        uitvoeringsdraad.start();
        return uitvoeringsdraad;
    }
    public static Process Uitvoeren(List<String> opdracht) throws IOException {
        return new ProcessBuilder(opdracht).start();
    }
}
