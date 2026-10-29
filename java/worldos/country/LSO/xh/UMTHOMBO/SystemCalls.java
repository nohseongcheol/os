// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.LSO.l_xh;
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
    public static RandomAccessFile Vula(String INDLELA, String Imowudi) throws IOException {
        return new RandomAccessFile(INDLELA, Imowudi);
    }
    public static int Funda(RandomAccessFile iFayili, byte[] data) throws IOException {
        return iFayili.read(data);
    }
    public static void Bhala(RandomAccessFile iFayili, byte[] data) throws IOException {
        iFayili.write(data);
    }
    public static void seek(RandomAccessFile iFayili, long position) throws IOException {
        iFayili.seek(position);
    }
    public static void sync(RandomAccessFile iFayili) throws IOException {
        iFayili.getFD().sync();
    }
    public static void Vala(RandomAccessFile iFayili) throws IOException {
        iFayili.close();
    }
    public static void Susa(String INDLELA) throws IOException {
        Files.delete(Paths.get(INDLELA));
    }
    public static long Ubukhulu(String INDLELA) throws IOException {
        return Files.size(Paths.get(INDLELA));
    }
    public static Socket Nxulumanisa(String address, int Isiqhagamsheli) throws IOException {
        return new Socket(address, Isiqhagamsheli);
    }
    public static DatagramSocket datagram(int Isiqhagamsheli) throws SocketException {
        return new DatagramSocket(Isiqhagamsheli);
    }
    public static Thread thread(Runnable Intshukumo) {
        Thread thread = new Thread(Intshukumo);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Umyalelo) throws IOException {
        return new ProcessBuilder(Umyalelo).start();
    }
}
