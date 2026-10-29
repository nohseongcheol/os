// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.MOZ.l_ndc;
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
    public static int read(RandomAccessFile file, byte[] data) throws IOException {
        return file.read(data);
    }
    public static void write(RandomAccessFile file, byte[] data) throws IOException {
        file.write(data);
    }
    public static void seek(RandomAccessFile file, long position) throws IOException {
        file.seek(position);
    }
    public static void sync(RandomAccessFile file) throws IOException {
        file.getFD().sync();
    }
    public static void close(RandomAccessFile file) throws IOException {
        file.close();
    }
    public static void remove(String path) throws IOException {
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
    public static Thread thread(Runnable action) {
        Thread thread = new Thread(action);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> command) throws IOException {
        return new ProcessBuilder(command).start();
    }
}
