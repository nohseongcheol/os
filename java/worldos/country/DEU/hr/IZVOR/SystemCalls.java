// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.DEU.l_hr;
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
    public static RandomAccessFile Otvori(String PUTANJA, String Način_rada) throws IOException {
        return new RandomAccessFile(PUTANJA, Način_rada);
    }
    public static int Čitaj(RandomAccessFile Datoteka, byte[] data) throws IOException {
        return Datoteka.read(data);
    }
    public static void Zapisuj(RandomAccessFile Datoteka, byte[] data) throws IOException {
        Datoteka.write(data);
    }
    public static void seek(RandomAccessFile Datoteka, long Položaj) throws IOException {
        Datoteka.seek(Položaj);
    }
    public static void sync(RandomAccessFile Datoteka) throws IOException {
        Datoteka.getFD().sync();
    }
    public static void Zatvori(RandomAccessFile Datoteka) throws IOException {
        Datoteka.close();
    }
    public static void Ukloni(String PUTANJA) throws IOException {
        Files.delete(Paths.get(PUTANJA));
    }
    public static long Veličina(String PUTANJA) throws IOException {
        return Files.size(Paths.get(PUTANJA));
    }
    public static Socket Spoji_se(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Aktivnost) {
        Thread thread = new Thread(Aktivnost);
        thread.start();
        return thread;
    }
    public static Process Izvrši(List<String> Naredba) throws IOException {
        return new ProcessBuilder(Naredba).start();
    }
}
