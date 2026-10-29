// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SWE.l_yi;
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
    public static RandomAccessFile עפֿן(String path, String מאָדע) throws IOException {
        return new RandomAccessFile(path, מאָדע);
    }
    public static int read(RandomAccessFile טעקע, byte[] data) throws IOException {
        return טעקע.read(data);
    }
    public static void write(RandomAccessFile טעקע, byte[] data) throws IOException {
        טעקע.write(data);
    }
    public static void seek(RandomAccessFile טעקע, long position) throws IOException {
        טעקע.seek(position);
    }
    public static void sync(RandomAccessFile טעקע) throws IOException {
        טעקע.getFD().sync();
    }
    public static void פֿאַרמאַך(RandomAccessFile טעקע) throws IOException {
        טעקע.close();
    }
    public static void remove(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long גרײס(String path) throws IOException {
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
