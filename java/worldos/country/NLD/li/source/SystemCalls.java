// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NLD.l_li;
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
    public static RandomAccessFile Äöpene(String Paad, String Modus) throws IOException {
        return new RandomAccessFile(Paad, Modus);
    }
    public static int Laeze(RandomAccessFile Besjtandj, byte[] data) throws IOException {
        return Besjtandj.read(data);
    }
    public static void Sjrieve(RandomAccessFile Besjtandj, byte[] data) throws IOException {
        Besjtandj.write(data);
    }
    public static void seek(RandomAccessFile Besjtandj, long position) throws IOException {
        Besjtandj.seek(position);
    }
    public static void sync(RandomAccessFile Besjtandj) throws IOException {
        Besjtandj.getFD().sync();
    }
    public static void Sjloete(RandomAccessFile Besjtandj) throws IOException {
        Besjtandj.close();
    }
    public static void Ewegdoon(String Paad) throws IOException {
        Files.delete(Paths.get(Paad));
    }
    public static long Gruutde(String Paad) throws IOException {
        return Files.size(Paths.get(Paad));
    }
    public static Socket Verbènje(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable action) {
        Thread thread = new Thread(action);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> command) throws IOException {
        return new ProcessBuilder(command).start();
    }
}
