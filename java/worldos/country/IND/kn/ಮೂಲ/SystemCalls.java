// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_kn;
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
    public static RandomAccessFile ತೆರೆ(String ಮಾರ್ಗ, String ಸ್ಥಿತಿ) throws IOException {
        return new RandomAccessFile(ಮಾರ್ಗ, ಸ್ಥಿತಿ);
    }
    public static int ಓದು(RandomAccessFile ಕಡತ, byte[] data) throws IOException {
        return ಕಡತ.read(data);
    }
    public static void ಬರೆ(RandomAccessFile ಕಡತ, byte[] data) throws IOException {
        ಕಡತ.write(data);
    }
    public static void seek(RandomAccessFile ಕಡತ, long ಸ್ಥಾನ) throws IOException {
        ಕಡತ.seek(ಸ್ಥಾನ);
    }
    public static void sync(RandomAccessFile ಕಡತ) throws IOException {
        ಕಡತ.getFD().sync();
    }
    public static void ಮುಚ್ಚು(RandomAccessFile ಕಡತ) throws IOException {
        ಕಡತ.close();
    }
    public static void ತೆಗೆದು_ಹಾಕು(String ಮಾರ್ಗ) throws IOException {
        Files.delete(Paths.get(ಮಾರ್ಗ));
    }
    public static long ಗಾತ್ರ(String ಮಾರ್ಗ) throws IOException {
        return Files.size(Paths.get(ಮಾರ್ಗ));
    }
    public static Socket ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು(String address, int ಸಂಪರ್ಕಸ್ಥಾನ) throws IOException {
        return new Socket(address, ಸಂಪರ್ಕಸ್ಥಾನ);
    }
    public static DatagramSocket datagram(int ಸಂಪರ್ಕಸ್ಥಾನ) throws SocketException {
        return new DatagramSocket(ಸಂಪರ್ಕಸ್ಥಾನ);
    }
    public static Thread thread(Runnable ಹಕ್ರಿಯೆ) {
        Thread thread = new Thread(ಹಕ್ರಿಯೆ);
        thread.start();
        return thread;
    }
    public static Process ಚಲಾಯಿಸು(List<String> ಆಜ್ಞೆ) throws IOException {
        return new ProcessBuilder(ಆಜ್ಞೆ).start();
    }
}
