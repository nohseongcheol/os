// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NOR.l_se;
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
    public static RandomAccessFile Raba(String path, String mode) throws IOException {
        return new RandomAccessFile(path, mode);
    }
    public static int Loga(RandomAccessFile Fiila, byte[] data) throws IOException {
        return Fiila.read(data);
    }
    public static void Čále(RandomAccessFile Fiila, byte[] data) throws IOException {
        Fiila.write(data);
    }
    public static void seek(RandomAccessFile Fiila, long position) throws IOException {
        Fiila.seek(position);
    }
    public static void sync(RandomAccessFile Fiila) throws IOException {
        Fiila.getFD().sync();
    }
    public static void Gidde(RandomAccessFile Fiila) throws IOException {
        Fiila.close();
    }
    public static void Váldde_eret(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long size(String path) throws IOException {
        return Files.size(Paths.get(path));
    }
    public static Socket connect(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Doaibma) {
        Thread thread = new Thread(Doaibma);
        thread.start();
        return thread;
    }
    public static Process Vuoje(List<String> Gohččun) throws IOException {
        return new ProcessBuilder(Gohččun).start();
    }
}
