// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.TJK.l_tg;
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
    public static RandomAccessFile open(String path, String mode) throws IOException {
        return new RandomAccessFile(path, mode);
    }
    public static int Хондан(RandomAccessFile Файл, byte[] data) throws IOException {
        return Файл.read(data);
    }
    public static void Навиштан(RandomAccessFile Файл, byte[] data) throws IOException {
        Файл.write(data);
    }
    public static void seek(RandomAccessFile Файл, long position) throws IOException {
        Файл.seek(position);
    }
    public static void sync(RandomAccessFile Файл) throws IOException {
        Файл.getFD().sync();
    }
    public static void Пӯшидан(RandomAccessFile Файл) throws IOException {
        Файл.close();
    }
    public static void Нобуд_кардан(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long size(String path) throws IOException {
        return Files.size(Paths.get(path));
    }
    public static Socket connect(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Амал) {
        Thread thread = new Thread(Амал);
        thread.start();
        return thread;
    }
    public static Process Иҷро_кардан(List<String> command) throws IOException {
        return new ProcessBuilder(command).start();
    }
}
