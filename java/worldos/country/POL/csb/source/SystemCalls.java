// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.POL.l_csb;
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
    public static int Przeczëtóné(RandomAccessFile Lopk, byte[] data) throws IOException {
        return Lopk.read(data);
    }
    public static void Zapiszë(RandomAccessFile Lopk, byte[] data) throws IOException {
        Lopk.write(data);
    }
    public static void seek(RandomAccessFile Lopk, long position) throws IOException {
        Lopk.seek(position);
    }
    public static void sync(RandomAccessFile Lopk) throws IOException {
        Lopk.getFD().sync();
    }
    public static void close(RandomAccessFile Lopk) throws IOException {
        Lopk.close();
    }
    public static void Rëmôj(String path) throws IOException {
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
    public static Thread thread(Runnable Dzejanié) {
        Thread thread = new Thread(Dzejanié);
        thread.start();
        return thread;
    }
    public static Process Zrëszë(List<String> Pòlét) throws IOException {
        return new ProcessBuilder(Pòlét).start();
    }
}
