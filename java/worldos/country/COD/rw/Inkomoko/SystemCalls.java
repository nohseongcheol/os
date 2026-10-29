// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.COD.l_rw;
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
    public static RandomAccessFile Gufungura(String Inzira, String Ubwoko) throws IOException {
        return new RandomAccessFile(Inzira, Ubwoko);
    }
    public static int read(RandomAccessFile Idosiye, byte[] data) throws IOException {
        return Idosiye.read(data);
    }
    public static void write(RandomAccessFile Idosiye, byte[] data) throws IOException {
        Idosiye.write(data);
    }
    public static void seek(RandomAccessFile Idosiye, long position) throws IOException {
        Idosiye.seek(position);
    }
    public static void sync(RandomAccessFile Idosiye) throws IOException {
        Idosiye.getFD().sync();
    }
    public static void Gufunga(RandomAccessFile Idosiye) throws IOException {
        Idosiye.close();
    }
    public static void Gukuraho(String Inzira) throws IOException {
        Files.delete(Paths.get(Inzira));
    }
    public static long Ingano(String Inzira) throws IOException {
        return Files.size(Paths.get(Inzira));
    }
    public static Socket connect(String address, int Umuyoboro) throws IOException {
        return new Socket(address, Umuyoboro);
    }
    public static DatagramSocket datagram(int Umuyoboro) throws SocketException {
        return new DatagramSocket(Umuyoboro);
    }
    public static Thread thread(Runnable Igikorwa) {
        Thread thread = new Thread(Igikorwa);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Icyo_wifuza) throws IOException {
        return new ProcessBuilder(Icyo_wifuza).start();
    }
}
