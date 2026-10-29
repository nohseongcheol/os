// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GEO.l_ka;
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
    public static RandomAccessFile გახსნა(String გეზი, String რეჟიმი) throws IOException {
        return new RandomAccessFile(გეზი, რეჟიმი);
    }
    public static int კითხვა(RandomAccessFile ფაილი, byte[] data) throws IOException {
        return ფაილი.read(data);
    }
    public static void ჩაწერა(RandomAccessFile ფაილი, byte[] data) throws IOException {
        ფაილი.write(data);
    }
    public static void seek(RandomAccessFile ფაილი, long position) throws IOException {
        ფაილი.seek(position);
    }
    public static void sync(RandomAccessFile ფაილი) throws IOException {
        ფაილი.getFD().sync();
    }
    public static void დახურვა(RandomAccessFile ფაილი) throws IOException {
        ფაილი.close();
    }
    public static void წაშლა(String გეზი) throws IOException {
        Files.delete(Paths.get(გეზი));
    }
    public static long ზომა(String გეზი) throws IOException {
        return Files.size(Paths.get(გეზი));
    }
    public static Socket დაკავშირება(String address, int პორტი) throws IOException {
        return new Socket(address, პორტი);
    }
    public static DatagramSocket datagram(int პორტი) throws SocketException {
        return new DatagramSocket(პორტი);
    }
    public static Thread thread(Runnable ქმედება) {
        Thread thread = new Thread(ქმედება);
        thread.start();
        return thread;
    }
    public static Process შესრულება(List<String> ბრძანება) throws IOException {
        return new ProcessBuilder(ბრძანება).start();
    }
}
