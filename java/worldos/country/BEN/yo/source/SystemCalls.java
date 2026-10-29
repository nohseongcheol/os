// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BEN.l_yo;
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
    public static RandomAccessFile Ṣi(String path, String mode) throws IOException {
        return new RandomAccessFile(path, mode);
    }
    public static int Kàá(RandomAccessFile Fáìlì, byte[] data) throws IOException {
        return Fáìlì.read(data);
    }
    public static void Kọ(RandomAccessFile Fáìlì, byte[] data) throws IOException {
        Fáìlì.write(data);
    }
    public static void seek(RandomAccessFile Fáìlì, long position) throws IOException {
        Fáìlì.seek(position);
    }
    public static void sync(RandomAccessFile Fáìlì) throws IOException {
        Fáìlì.getFD().sync();
    }
    public static void Ti(RandomAccessFile Fáìlì) throws IOException {
        Fáìlì.close();
    }
    public static void Yọkúrò(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long Ìwọ̀n(String path) throws IOException {
        return Files.size(Paths.get(path));
    }
    public static Socket Darapọ̀(String address, int port) throws IOException {
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
    public static Process execute(List<String> Àṣẹ) throws IOException {
        return new ProcessBuilder(Àṣẹ).start();
    }
}
