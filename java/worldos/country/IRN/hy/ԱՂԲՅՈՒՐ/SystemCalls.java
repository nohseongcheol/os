// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IRN.l_hy;
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
    public static RandomAccessFile Բաց(String Ճանապարհ, String Ռեժիմ) throws IOException {
        return new RandomAccessFile(Ճանապարհ, Ռեժիմ);
    }
    public static int Ընթերցում(RandomAccessFile Ֆայլ, byte[] data) throws IOException {
        return Ֆայլ.read(data);
    }
    public static void Գրել(RandomAccessFile Ֆայլ, byte[] data) throws IOException {
        Ֆայլ.write(data);
    }
    public static void seek(RandomAccessFile Ֆայլ, long Դիրք) throws IOException {
        Ֆայլ.seek(Դիրք);
    }
    public static void sync(RandomAccessFile Ֆայլ) throws IOException {
        Ֆայլ.getFD().sync();
    }
    public static void Փակ(RandomAccessFile Ֆայլ) throws IOException {
        Ֆայլ.close();
    }
    public static void Հեռացնել(String Ճանապարհ) throws IOException {
        Files.delete(Paths.get(Ճանապարհ));
    }
    public static long Չափս(String Ճանապարհ) throws IOException {
        return Files.size(Paths.get(Ճանապարհ));
    }
    public static Socket Միացնել(String address, int Պորտ) throws IOException {
        return new Socket(address, Պորտ);
    }
    public static DatagramSocket datagram(int Պորտ) throws SocketException {
        return new DatagramSocket(Պորտ);
    }
    public static Thread thread(Runnable Գործողություն) {
        Thread thread = new Thread(Գործողություն);
        thread.start();
        return thread;
    }
    public static Process Կատարել(List<String> Հրահանգ) throws IOException {
        return new ProcessBuilder(Հրահանգ).start();
    }
}
