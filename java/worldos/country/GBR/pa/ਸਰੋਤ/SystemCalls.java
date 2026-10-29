// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GBR.l_pa;
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
    public static RandomAccessFile ਖੋਲ੍ਹੋ(String ਮਾਰਗ, String ਮੋਡ) throws IOException {
        return new RandomAccessFile(ਮਾਰਗ, ਮੋਡ);
    }
    public static int ਪੜ੍ਹਨ(RandomAccessFile ਫਾਇਲ, byte[] data) throws IOException {
        return ਫਾਇਲ.read(data);
    }
    public static void ਲਿਖਣ(RandomAccessFile ਫਾਇਲ, byte[] data) throws IOException {
        ਫਾਇਲ.write(data);
    }
    public static void seek(RandomAccessFile ਫਾਇਲ, long ਸਥਿਤੀ) throws IOException {
        ਫਾਇਲ.seek(ਸਥਿਤੀ);
    }
    public static void sync(RandomAccessFile ਫਾਇਲ) throws IOException {
        ਫਾਇਲ.getFD().sync();
    }
    public static void ਬੰਦ_ਕਰੋ(RandomAccessFile ਫਾਇਲ) throws IOException {
        ਫਾਇਲ.close();
    }
    public static void ਹਟਾਓ(String ਮਾਰਗ) throws IOException {
        Files.delete(Paths.get(ਮਾਰਗ));
    }
    public static long ਆਕਾਰ(String ਮਾਰਗ) throws IOException {
        return Files.size(Paths.get(ਮਾਰਗ));
    }
    public static Socket ਕੁਨੈਕਸ਼ਨ_ਕਰੋ(String address, int ਪੋਰਟ) throws IOException {
        return new Socket(address, ਪੋਰਟ);
    }
    public static DatagramSocket datagram(int ਪੋਰਟ) throws SocketException {
        return new DatagramSocket(ਪੋਰਟ);
    }
    public static Thread thread(Runnable ਐਕਸ਼ਨ) {
        Thread thread = new Thread(ਐਕਸ਼ਨ);
        thread.start();
        return thread;
    }
    public static Process ਚਲਾਓ(List<String> ਕਮਾਂਡ) throws IOException {
        return new ProcessBuilder(ਕਮਾਂਡ).start();
    }
}
