// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GRC.l_sq;
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
    public static RandomAccessFile Hap(String POZICIONI, String Modaliteti) throws IOException {
        return new RandomAccessFile(POZICIONI, Modaliteti);
    }
    public static int Leximi(RandomAccessFile Kartelë, byte[] data) throws IOException {
        return Kartelë.read(data);
    }
    public static void Shkrimi(RandomAccessFile Kartelë, byte[] data) throws IOException {
        Kartelë.write(data);
    }
    public static void seek(RandomAccessFile Kartelë, long Pozicioni) throws IOException {
        Kartelë.seek(Pozicioni);
    }
    public static void sync(RandomAccessFile Kartelë) throws IOException {
        Kartelë.getFD().sync();
    }
    public static void Mbyll(RandomAccessFile Kartelë) throws IOException {
        Kartelë.close();
    }
    public static void Hiq(String POZICIONI) throws IOException {
        Files.delete(Paths.get(POZICIONI));
    }
    public static long Madhësi(String POZICIONI) throws IOException {
        return Files.size(Paths.get(POZICIONI));
    }
    public static Socket Lidhu(String address, int Porta) throws IOException {
        return new Socket(address, Porta);
    }
    public static DatagramSocket datagram(int Porta) throws SocketException {
        return new DatagramSocket(Porta);
    }
    public static Thread thread(Runnable Veprim) {
        Thread thread = new Thread(Veprim);
        thread.start();
        return thread;
    }
    public static Process Kryej(List<String> Komanda) throws IOException {
        return new ProcessBuilder(Komanda).start();
    }
}
