// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SWE.l_ia;
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
    public static RandomAccessFile Aperir(String Percurso, String mode) throws IOException {
        return new RandomAccessFile(Percurso, mode);
    }
    public static int Lege(RandomAccessFile file, byte[] data) throws IOException {
        return file.read(data);
    }
    public static void Scribe(RandomAccessFile file, byte[] data) throws IOException {
        file.write(data);
    }
    public static void seek(RandomAccessFile file, long position) throws IOException {
        file.seek(position);
    }
    public static void sync(RandomAccessFile file) throws IOException {
        file.getFD().sync();
    }
    public static void Clauder(RandomAccessFile file) throws IOException {
        file.close();
    }
    public static void Remover(String Percurso) throws IOException {
        Files.delete(Paths.get(Percurso));
    }
    public static long Grandor(String Percurso) throws IOException {
        return Files.size(Paths.get(Percurso));
    }
    public static Socket connect(String address, int Porto) throws IOException {
        return new Socket(address, Porto);
    }
    public static DatagramSocket datagram(int Porto) throws SocketException {
        return new DatagramSocket(Porto);
    }
    public static Thread thread(Runnable action) {
        Thread thread = new Thread(action);
        thread.start();
        return thread;
    }
    public static Process Executa(List<String> Commando) throws IOException {
        return new ProcessBuilder(Commando).start();
    }
}
