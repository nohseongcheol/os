// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CAN.l_hu;
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
    public static RandomAccessFile Megnyitás(String ÚTVONAL, String Mód) throws IOException {
        return new RandomAccessFile(ÚTVONAL, Mód);
    }
    public static int Olvasás(RandomAccessFile Fájl, byte[] data) throws IOException {
        return Fájl.read(data);
    }
    public static void Írás(RandomAccessFile Fájl, byte[] data) throws IOException {
        Fájl.write(data);
    }
    public static void seek(RandomAccessFile Fájl, long Pozíció) throws IOException {
        Fájl.seek(Pozíció);
    }
    public static void sync(RandomAccessFile Fájl) throws IOException {
        Fájl.getFD().sync();
    }
    public static void Bezárás(RandomAccessFile Fájl) throws IOException {
        Fájl.close();
    }
    public static void Eltávolítás(String ÚTVONAL) throws IOException {
        Files.delete(Paths.get(ÚTVONAL));
    }
    public static long Méret(String ÚTVONAL) throws IOException {
        return Files.size(Paths.get(ÚTVONAL));
    }
    public static Socket Kapcsolódás(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Művelet) {
        Thread thread = new Thread(Művelet);
        thread.start();
        return thread;
    }
    public static Process Végrehajtás(List<String> Parancs) throws IOException {
        return new ProcessBuilder(Parancs).start();
    }
}
