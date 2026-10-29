// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ITA.l_fur;
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
    public static RandomAccessFile Vierç(String Percors, String Mût) throws IOException {
        return new RandomAccessFile(Percors, Mût);
    }
    public static int Lei(RandomAccessFile file, byte[] data) throws IOException {
        return file.read(data);
    }
    public static void Scrivi(RandomAccessFile file, byte[] data) throws IOException {
        file.write(data);
    }
    public static void seek(RandomAccessFile file, long Posizion) throws IOException {
        file.seek(Posizion);
    }
    public static void sync(RandomAccessFile file) throws IOException {
        file.getFD().sync();
    }
    public static void Siere(RandomAccessFile file) throws IOException {
        file.close();
    }
    public static void Gjave(String Percors) throws IOException {
        Files.delete(Paths.get(Percors));
    }
    public static long Dimension(String Percors) throws IOException {
        return Files.size(Paths.get(Percors));
    }
    public static Socket Conetiti(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Azion) {
        Thread thread = new Thread(Azion);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Comant) throws IOException {
        return new ProcessBuilder(Comant).start();
    }
}
