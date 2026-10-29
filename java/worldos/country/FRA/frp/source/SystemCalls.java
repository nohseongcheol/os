// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.FRA.l_frp;
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
    public static int read(RandomAccessFile FICHIÉR, byte[] data) throws IOException {
        return FICHIÉR.read(data);
    }
    public static void write(RandomAccessFile FICHIÉR, byte[] data) throws IOException {
        FICHIÉR.write(data);
    }
    public static void seek(RandomAccessFile FICHIÉR, long position) throws IOException {
        FICHIÉR.seek(position);
    }
    public static void sync(RandomAccessFile FICHIÉR) throws IOException {
        FICHIÉR.getFD().sync();
    }
    public static void close(RandomAccessFile FICHIÉR) throws IOException {
        FICHIÉR.close();
    }
    public static void Revondre(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long Talyi(String path) throws IOException {
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
    public static Process execute(List<String> Comanda) throws IOException {
        return new ProcessBuilder(Comanda).start();
    }
}
