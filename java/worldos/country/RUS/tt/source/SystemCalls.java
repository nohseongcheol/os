// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.RUS.l_tt;
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
    public static RandomAccessFile open(String Yul, String Isul) throws IOException {
        return new RandomAccessFile(Yul, Isul);
    }
    public static int read(RandomAccessFile Birem, byte[] data) throws IOException {
        return Birem.read(data);
    }
    public static void write(RandomAccessFile Birem, byte[] data) throws IOException {
        Birem.write(data);
    }
    public static void seek(RandomAccessFile Birem, long position) throws IOException {
        Birem.seek(position);
    }
    public static void sync(RandomAccessFile Birem) throws IOException {
        Birem.getFD().sync();
    }
    public static void Yap(RandomAccessFile Birem) throws IOException {
        Birem.close();
    }
    public static void Бетерү(String Yul) throws IOException {
        Files.delete(Paths.get(Yul));
    }
    public static long size(String Yul) throws IOException {
        return Files.size(Paths.get(Yul));
    }
    public static Socket connect(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Гамәл) {
        Thread thread = new Thread(Гамәл);
        thread.start();
        return thread;
    }
    public static Process Башкару(List<String> command) throws IOException {
        return new ProcessBuilder(command).start();
    }
}
