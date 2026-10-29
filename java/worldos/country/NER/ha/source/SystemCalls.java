// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NER.l_ha;
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
    public static RandomAccessFile Buɗe(String path, String mode) throws IOException {
        return new RandomAccessFile(path, mode);
    }
    public static int Yi_Karatu(RandomAccessFile Fayil, byte[] data) throws IOException {
        return Fayil.read(data);
    }
    public static void Yi_Rubutu(RandomAccessFile Fayil, byte[] data) throws IOException {
        Fayil.write(data);
    }
    public static void seek(RandomAccessFile Fayil, long position) throws IOException {
        Fayil.seek(position);
    }
    public static void sync(RandomAccessFile Fayil) throws IOException {
        Fayil.getFD().sync();
    }
    public static void Rufe(RandomAccessFile Fayil) throws IOException {
        Fayil.close();
    }
    public static void Cire(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long Girma(String path) throws IOException {
        return Files.size(Paths.get(path));
    }
    public static Socket Haɗi(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Aiki) {
        Thread thread = new Thread(Aiki);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Umarni) throws IOException {
        return new ProcessBuilder(Umarni).start();
    }
}
