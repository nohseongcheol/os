// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NOR.l_nn;
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
    public static RandomAccessFile Opna(String STIGE, String Modus) throws IOException {
        return new RandomAccessFile(STIGE, Modus);
    }
    public static int Les(RandomAccessFile Fil, byte[] data) throws IOException {
        return Fil.read(data);
    }
    public static void Skriv(RandomAccessFile Fil, byte[] data) throws IOException {
        Fil.write(data);
    }
    public static void seek(RandomAccessFile Fil, long Posisjon) throws IOException {
        Fil.seek(Posisjon);
    }
    public static void sync(RandomAccessFile Fil) throws IOException {
        Fil.getFD().sync();
    }
    public static void Lukk(RandomAccessFile Fil) throws IOException {
        Fil.close();
    }
    public static void Fjern(String STIGE) throws IOException {
        Files.delete(Paths.get(STIGE));
    }
    public static long Storleik(String STIGE) throws IOException {
        return Files.size(Paths.get(STIGE));
    }
    public static Socket Kopla_til(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Handling) {
        Thread thread = new Thread(Handling);
        thread.start();
        return thread;
    }
    public static Process Køyr(List<String> Kommando) throws IOException {
        return new ProcessBuilder(Kommando).start();
    }
}
