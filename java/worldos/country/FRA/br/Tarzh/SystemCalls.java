// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.FRA.l_br;
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
    public static RandomAccessFile Digeriñ(String TREUG, String Mod) throws IOException {
        return new RandomAccessFile(TREUG, Mod);
    }
    public static int Lenn(RandomAccessFile Restr, byte[] data) throws IOException {
        return Restr.read(data);
    }
    public static void Skrivañ(RandomAccessFile Restr, byte[] data) throws IOException {
        Restr.write(data);
    }
    public static void seek(RandomAccessFile Restr, long Lec_hiadur) throws IOException {
        Restr.seek(Lec_hiadur);
    }
    public static void sync(RandomAccessFile Restr) throws IOException {
        Restr.getFD().sync();
    }
    public static void Serriñ(RandomAccessFile Restr) throws IOException {
        Restr.close();
    }
    public static void Dilemel(String TREUG) throws IOException {
        Files.delete(Paths.get(TREUG));
    }
    public static long Ment(String TREUG) throws IOException {
        return Files.size(Paths.get(TREUG));
    }
    public static Socket Kennaskañ(String address, int Porzh) throws IOException {
        return new Socket(address, Porzh);
    }
    public static DatagramSocket datagram(int Porzh) throws SocketException {
        return new DatagramSocket(Porzh);
    }
    public static Thread thread(Runnable Gwezhiad) {
        Thread thread = new Thread(Gwezhiad);
        thread.start();
        return thread;
    }
    public static Process Seveniñ(List<String> Arc_had) throws IOException {
        return new ProcessBuilder(Arc_had).start();
    }
}
