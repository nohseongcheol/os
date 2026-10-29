// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.RUS.l_sr;
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
    public static RandomAccessFile Отвори(String ПУТАЊА, String Начин_рада) throws IOException {
        return new RandomAccessFile(ПУТАЊА, Начин_рада);
    }
    public static int Чита(RandomAccessFile Датотека, byte[] data) throws IOException {
        return Датотека.read(data);
    }
    public static void Пише(RandomAccessFile Датотека, byte[] data) throws IOException {
        Датотека.write(data);
    }
    public static void seek(RandomAccessFile Датотека, long Положај) throws IOException {
        Датотека.seek(Положај);
    }
    public static void sync(RandomAccessFile Датотека) throws IOException {
        Датотека.getFD().sync();
    }
    public static void Затворен(RandomAccessFile Датотека) throws IOException {
        Датотека.close();
    }
    public static void Уклони(String ПУТАЊА) throws IOException {
        Files.delete(Paths.get(ПУТАЊА));
    }
    public static long Величина(String ПУТАЊА) throws IOException {
        return Files.size(Paths.get(ПУТАЊА));
    }
    public static Socket Повежи_се(String address, int Порт) throws IOException {
        return new Socket(address, Порт);
    }
    public static DatagramSocket datagram(int Порт) throws SocketException {
        return new DatagramSocket(Порт);
    }
    public static Thread thread(Runnable радња) {
        Thread thread = new Thread(радња);
        thread.start();
        return thread;
    }
    public static Process Изврши(List<String> Наредба) throws IOException {
        return new ProcessBuilder(Наредба).start();
    }
}
