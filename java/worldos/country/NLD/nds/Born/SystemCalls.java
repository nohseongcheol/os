// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NLD.l_nds;
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
    public static RandomAccessFile Opmaken(String PADD, String Modus) throws IOException {
        return new RandomAccessFile(PADD, Modus);
    }
    public static int Lesen(RandomAccessFile Datei, byte[] data) throws IOException {
        return Datei.read(data);
    }
    public static void Schrieven(RandomAccessFile Datei, byte[] data) throws IOException {
        Datei.write(data);
    }
    public static void seek(RandomAccessFile Datei, long Positschoon) throws IOException {
        Datei.seek(Positschoon);
    }
    public static void sync(RandomAccessFile Datei) throws IOException {
        Datei.getFD().sync();
    }
    public static void Sluten(RandomAccessFile Datei) throws IOException {
        Datei.close();
    }
    public static void Entfernen(String PADD) throws IOException {
        Files.delete(Paths.get(PADD));
    }
    public static long Gröte(String PADD) throws IOException {
        return Files.size(Paths.get(PADD));
    }
    public static Socket Verbinnen(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Akschoon) {
        Thread thread = new Thread(Akschoon);
        thread.start();
        return thread;
    }
    public static Process Utföhren(List<String> Order) throws IOException {
        return new ProcessBuilder(Order).start();
    }
}
