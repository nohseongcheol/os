// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.DEU.l_hsb;
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
    public static RandomAccessFile Wočinić(String path, String mode) throws IOException {
        return new RandomAccessFile(path, mode);
    }
    public static int Čitać(RandomAccessFile Dataja, byte[] data) throws IOException {
        return Dataja.read(data);
    }
    public static void Pisać(RandomAccessFile Dataja, byte[] data) throws IOException {
        Dataja.write(data);
    }
    public static void seek(RandomAccessFile Dataja, long position) throws IOException {
        Dataja.seek(position);
    }
    public static void sync(RandomAccessFile Dataja) throws IOException {
        Dataja.getFD().sync();
    }
    public static void close(RandomAccessFile Dataja) throws IOException {
        Dataja.close();
    }
    public static void Zničić(String path) throws IOException {
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
    public static Thread thread(Runnable Akcija) {
        Thread thread = new Thread(Akcija);
        thread.start();
        return thread;
    }
    public static Process Wuwjesć(List<String> command) throws IOException {
        return new ProcessBuilder(command).start();
    }
}
