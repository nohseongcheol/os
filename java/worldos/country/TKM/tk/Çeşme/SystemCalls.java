// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.TKM.l_tk;
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
    public static RandomAccessFile Aç(String Ýol, String mode) throws IOException {
        return new RandomAccessFile(Ýol, mode);
    }
    public static int Oka(RandomAccessFile Faýl, byte[] data) throws IOException {
        return Faýl.read(data);
    }
    public static void Ýaz(RandomAccessFile Faýl, byte[] data) throws IOException {
        Faýl.write(data);
    }
    public static void seek(RandomAccessFile Faýl, long position) throws IOException {
        Faýl.seek(position);
    }
    public static void sync(RandomAccessFile Faýl) throws IOException {
        Faýl.getFD().sync();
    }
    public static void Ýap(RandomAccessFile Faýl) throws IOException {
        Faýl.close();
    }
    public static void Çykar(String Ýol) throws IOException {
        Files.delete(Paths.get(Ýol));
    }
    public static long Ululyk(String Ýol) throws IOException {
        return Files.size(Paths.get(Ýol));
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
