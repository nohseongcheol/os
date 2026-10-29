// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.KHM.l_km;
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
    public static RandomAccessFile បើក(String path, String របៀប) throws IOException {
        return new RandomAccessFile(path, របៀប);
    }
    public static int អាន(RandomAccessFile ឯកសារ, byte[] data) throws IOException {
        return ឯកសារ.read(data);
    }
    public static void សរសេរ(RandomAccessFile ឯកសារ, byte[] data) throws IOException {
        ឯកសារ.write(data);
    }
    public static void seek(RandomAccessFile ឯកសារ, long position) throws IOException {
        ឯកសារ.seek(position);
    }
    public static void sync(RandomAccessFile ឯកសារ) throws IOException {
        ឯកសារ.getFD().sync();
    }
    public static void close(RandomAccessFile ឯកសារ) throws IOException {
        ឯកសារ.close();
    }
    public static void យកចេញ(String path) throws IOException {
        Files.delete(Paths.get(path));
    }
    public static long size(String path) throws IOException {
        return Files.size(Paths.get(path));
    }
    public static Socket connect(String address, int ច្រក) throws IOException {
        return new Socket(address, ច្រក);
    }
    public static DatagramSocket datagram(int ច្រក) throws SocketException {
        return new DatagramSocket(ច្រក);
    }
    public static Thread thread(Runnable អំពើ) {
        Thread thread = new Thread(អំពើ);
        thread.start();
        return thread;
    }
    public static Process ប្រតិបត្តិ(List<String> ពាក្យ_បញ្ជា) throws IOException {
        return new ProcessBuilder(ពាក្យ_បញ្ជា).start();
    }
}
