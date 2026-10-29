// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_ks;
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
    public static RandomAccessFile open(String path, String mode) throws IOException {
        return new RandomAccessFile(path, mode);
    }
    public static int read(RandomAccessFile फ़ाइल, byte[] data) throws IOException {
        return फ़ाइल.read(data);
    }
    public static void write(RandomAccessFile फ़ाइल, byte[] data) throws IOException {
        फ़ाइल.write(data);
    }
    public static void seek(RandomAccessFile फ़ाइल, long जाय_प्य्यटठ) throws IOException {
        फ़ाइल.seek(जाय_प्य्यटठ);
    }
    public static void sync(RandomAccessFile फ़ाइल) throws IOException {
        फ़ाइल.getFD().sync();
    }
    public static void बंद_करिव(RandomAccessFile फ़ाइल) throws IOException {
        फ़ाइल.close();
    }
    public static void remove(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long नाप(String path) throws IOException {
        return Files.size(Paths.get(path));
    }
    public static Socket connect(String address, int port) throws IOException {
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
