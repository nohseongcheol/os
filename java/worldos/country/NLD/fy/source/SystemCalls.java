// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NLD.l_fy;
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
    public static RandomAccessFile Iepenje(String path, String mode) throws IOException {
        return new RandomAccessFile(path, mode);
    }
    public static int Lêze(RandomAccessFile Bestân, byte[] data) throws IOException {
        return Bestân.read(data);
    }
    public static void Skriuwe(RandomAccessFile Bestân, byte[] data) throws IOException {
        Bestân.write(data);
    }
    public static void seek(RandomAccessFile Bestân, long position) throws IOException {
        Bestân.seek(position);
    }
    public static void sync(RandomAccessFile Bestân) throws IOException {
        Bestân.getFD().sync();
    }
    public static void Slute(RandomAccessFile Bestân) throws IOException {
        Bestân.close();
    }
    public static void Fuortsmite(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long Grutte(String path) throws IOException {
        return Files.size(Paths.get(path));
    }
    public static Socket connect(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Aksje) {
        Thread thread = new Thread(Aksje);
        thread.start();
        return thread;
    }
    public static Process Utfiere(List<String> Kommando) throws IOException {
        return new ProcessBuilder(Kommando).start();
    }
}
