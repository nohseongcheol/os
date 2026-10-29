// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GBR.l_cy;
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
    public static RandomAccessFile Agor(String LLWYBR, String Modd) throws IOException {
        return new RandomAccessFile(LLWYBR, Modd);
    }
    public static int Darllen(RandomAccessFile Ffeil, byte[] data) throws IOException {
        return Ffeil.read(data);
    }
    public static void Ysgrifennu(RandomAccessFile Ffeil, byte[] data) throws IOException {
        Ffeil.write(data);
    }
    public static void seek(RandomAccessFile Ffeil, long position) throws IOException {
        Ffeil.seek(position);
    }
    public static void sync(RandomAccessFile Ffeil) throws IOException {
        Ffeil.getFD().sync();
    }
    public static void Cau(RandomAccessFile Ffeil) throws IOException {
        Ffeil.close();
    }
    public static void Tynnu(String LLWYBR) throws IOException {
        Files.delete(Paths.get(LLWYBR));
    }
    public static long Maint(String LLWYBR) throws IOException {
        return Files.size(Paths.get(LLWYBR));
    }
    public static Socket connect(String address, int Porth) throws IOException {
        return new Socket(address, Porth);
    }
    public static DatagramSocket datagram(int Porth) throws SocketException {
        return new DatagramSocket(Porth);
    }
    public static Thread thread(Runnable Gweithrediad) {
        Thread thread = new Thread(Gweithrediad);
        thread.start();
        return thread;
    }
    public static Process Gweithredu(List<String> Gorchymyn) throws IOException {
        return new ProcessBuilder(Gorchymyn).start();
    }
}
