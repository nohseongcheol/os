// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_dz;
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
    public static RandomAccessFile ཁ_ཕྱེ(String འགྲུལ_ལམ, String ཐབས_ལམ) throws IOException {
        return new RandomAccessFile(འགྲུལ_ལམ, ཐབས_ལམ);
    }
    public static int ལྷག(RandomAccessFile ཡིག_སྣོད, byte[] data) throws IOException {
        return ཡིག_སྣོད.read(data);
    }
    public static void བྲིས(RandomAccessFile ཡིག_སྣོད, byte[] data) throws IOException {
        ཡིག_སྣོད.write(data);
    }
    public static void seek(RandomAccessFile ཡིག_སྣོད, long གནས_ས) throws IOException {
        ཡིག_སྣོད.seek(གནས_ས);
    }
    public static void sync(RandomAccessFile ཡིག_སྣོད) throws IOException {
        ཡིག_སྣོད.getFD().sync();
    }
    public static void ཁ_བསྡམས(RandomAccessFile ཡིག_སྣོད) throws IOException {
        ཡིག_སྣོད.close();
    }
    public static void རྩ_བསྐྲད_གཏང(String འགྲུལ_ལམ) throws IOException {
        Files.delete(Paths.get(འགྲུལ_ལམ));
    }
    public static long ཚད(String འགྲུལ_ལམ) throws IOException {
        return Files.size(Paths.get(འགྲུལ_ལམ));
    }
    public static Socket མཐུད(String address, int འདྲེན_ལམ) throws IOException {
        return new Socket(address, འདྲེན_ལམ);
    }
    public static DatagramSocket datagram(int འདྲེན_ལམ) throws SocketException {
        return new DatagramSocket(འདྲེན_ལམ);
    }
    public static Thread thread(Runnable བྱ_བ) {
        Thread thread = new Thread(བྱ_བ);
        thread.start();
        return thread;
    }
    public static Process execute(List<String> བརྡ_བཀོད) throws IOException {
        return new ProcessBuilder(བརྡ_བཀོད).start();
    }
}
