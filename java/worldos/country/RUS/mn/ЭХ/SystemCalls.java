// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.RUS.l_mn;
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
    public static RandomAccessFile Нээх(String ЗАМ, String Горим) throws IOException {
        return new RandomAccessFile(ЗАМ, Горим);
    }
    public static int Унших(RandomAccessFile Файл, byte[] data) throws IOException {
        return Файл.read(data);
    }
    public static void Бичих(RandomAccessFile Файл, byte[] data) throws IOException {
        Файл.write(data);
    }
    public static void seek(RandomAccessFile Файл, long position) throws IOException {
        Файл.seek(position);
    }
    public static void sync(RandomAccessFile Файл) throws IOException {
        Файл.getFD().sync();
    }
    public static void Хаах(RandomAccessFile Файл) throws IOException {
        Файл.close();
    }
    public static void Устгах(String ЗАМ) throws IOException {
        Files.delete(Paths.get(ЗАМ));
    }
    public static long Хэмжээ(String ЗАМ) throws IOException {
        return Files.size(Paths.get(ЗАМ));
    }
    public static Socket Холбох(String address, int Порт) throws IOException {
        return new Socket(address, Порт);
    }
    public static DatagramSocket datagram(int Порт) throws SocketException {
        return new DatagramSocket(Порт);
    }
    public static Thread thread(Runnable Үйлдэл) {
        Thread thread = new Thread(Үйлдэл);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> Тушаал) throws IOException {
        return new ProcessBuilder(Тушаал).start();
    }
}
