// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ESP.l_eu;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class SystemCalls {
    private SystemCalls() { }
    public static RandomAccessFile Ireki(String Bide_izena, String Modua) throws IOException {
        return new RandomAccessFile(Bide_izena, Modua);
    }
    public static int Irakurri(RandomAccessFile Fitxategia, byte[] data) throws IOException {
        return Fitxategia.read(data);
    }
    public static void Idatzi(RandomAccessFile Fitxategia, byte[] data) throws IOException {
        Fitxategia.write(data);
    }
    public static void seek(RandomAccessFile Fitxategia, long Posizioa) throws IOException {
        Fitxategia.seek(Posizioa);
    }
    public static void sync(RandomAccessFile Fitxategia) throws IOException {
        Fitxategia.getFD().sync();
    }
    public static void Itxi(RandomAccessFile Fitxategia) throws IOException {
        Fitxategia.close();
    }
    public static void Kendu(String Bide_izena) throws IOException {
        Files.delete(Paths.get(Bide_izena));
    }
    public static long Tamaina(String Bide_izena) throws IOException {
        return Files.size(Paths.get(Bide_izena));
    }
    public static Socket Konektatu(String address, int Ataka) throws IOException {
        return new Socket(address, Ataka);
    }
    public static DatagramSocket datagram(int Ataka) throws SocketException {
        return new DatagramSocket(Ataka);
    }
    public static Thread thread(Runnable Ekintza) {
        Thread thread = new Thread(Ekintza);
        thread.start();
        return thread;
    }
    public static Process Exekutatu(List<String> Komandoa) throws IOException {
        return new ProcessBuilder(Komandoa).start();
    }
}
