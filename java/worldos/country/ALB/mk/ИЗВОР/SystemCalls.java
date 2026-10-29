// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ALB.l_mk;
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
    public static RandomAccessFile Отвори(String ПАТЕКА, String Режим) throws IOException {
        return new RandomAccessFile(ПАТЕКА, Режим);
    }
    public static int Читај(RandomAccessFile Датотека, byte[] data) throws IOException {
        return Датотека.read(data);
    }
    public static void Запиши(RandomAccessFile Датотека, byte[] data) throws IOException {
        Датотека.write(data);
    }
    public static void seek(RandomAccessFile Датотека, long Позиција) throws IOException {
        Датотека.seek(Позиција);
    }
    public static void sync(RandomAccessFile Датотека) throws IOException {
        Датотека.getFD().sync();
    }
    public static void Затвори(RandomAccessFile Датотека) throws IOException {
        Датотека.close();
    }
    public static void Отстрани(String ПАТЕКА) throws IOException {
        Files.delete(Paths.get(ПАТЕКА));
    }
    public static long Големина(String ПАТЕКА) throws IOException {
        return Files.size(Paths.get(ПАТЕКА));
    }
    public static Socket Врзи_се(String address, int Порта) throws IOException {
        return new Socket(address, Порта);
    }
    public static DatagramSocket datagram(int Порта) throws SocketException {
        return new DatagramSocket(Порта);
    }
    public static Thread thread(Runnable Дејство) {
        Thread thread = new Thread(Дејство);
        thread.start();
        return thread;
    }
    public static Process Изврши(List<String> Команда) throws IOException {
        return new ProcessBuilder(Команда).start();
    }
}
