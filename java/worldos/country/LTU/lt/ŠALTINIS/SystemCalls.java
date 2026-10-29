// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.LTU.l_lt;
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
    public static RandomAccessFile Atverti(String KELIAS, String Veiksena) throws IOException {
        return new RandomAccessFile(KELIAS, Veiksena);
    }
    public static int Skaitymas(RandomAccessFile Failas, byte[] data) throws IOException {
        return Failas.read(data);
    }
    public static void Rašymas(RandomAccessFile Failas, byte[] data) throws IOException {
        Failas.write(data);
    }
    public static void seek(RandomAccessFile Failas, long Pozicija) throws IOException {
        Failas.seek(Pozicija);
    }
    public static void sync(RandomAccessFile Failas) throws IOException {
        Failas.getFD().sync();
    }
    public static void Užverti(RandomAccessFile Failas) throws IOException {
        Failas.close();
    }
    public static void Šalinti(String KELIAS) throws IOException {
        Files.delete(Paths.get(KELIAS));
    }
    public static long Dydis(String KELIAS) throws IOException {
        return Files.size(Paths.get(KELIAS));
    }
    public static Socket Prisijungti(String address, int Prievadas) throws IOException {
        return new Socket(address, Prievadas);
    }
    public static DatagramSocket datagram(int Prievadas) throws SocketException {
        return new DatagramSocket(Prievadas);
    }
    public static Thread thread(Runnable Veiksmas) {
        Thread thread = new Thread(Veiksmas);
        thread.start();
        return thread;
    }
    public static Process Vykdyti(List<String> Komanda) throws IOException {
        return new ProcessBuilder(Komanda).start();
    }
}
