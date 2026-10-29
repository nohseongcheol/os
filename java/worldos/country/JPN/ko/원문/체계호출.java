// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.JPN.l_ko;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class 체계호출 {
    private 체계호출() { }
    public static RandomAccessFile 열기(String 경로, String 방식) throws IOException {
        return new RandomAccessFile(경로, 방식);
    }
    public static int 읽기(RandomAccessFile 자료파일, byte[] 자료) throws IOException {
        return 자료파일.read(자료);
    }
    public static void 쓰기(RandomAccessFile 자료파일, byte[] 자료) throws IOException {
        자료파일.write(자료);
    }
    public static void 위치옮기기(RandomAccessFile 자료파일, long 위치) throws IOException {
        자료파일.seek(위치);
    }
    public static void 기록맞추기(RandomAccessFile 자료파일) throws IOException {
        자료파일.getFD().sync();
    }
    public static void 닫기(RandomAccessFile 자료파일) throws IOException {
        자료파일.close();
    }
    public static void 지우기(String 경로) throws IOException {
        Files.delete(Paths.get(경로));
    }
    public static long 크기(String 경로) throws IOException {
        return Files.size(Paths.get(경로));
    }
    public static Socket 연결하기(String 주소, int 통신문번호) throws IOException {
        return new Socket(주소, 통신문번호);
    }
    public static DatagramSocket 독립전문(int 통신문번호) throws SocketException {
        return new DatagramSocket(통신문번호);
    }
    public static Thread 실행가닥(Runnable 동작) {
        Thread 실행가닥 = new Thread(동작);
        실행가닥.start();
        return 실행가닥;
    }
    public static Process 실행하기(List<String> 명령) throws IOException {
        return new ProcessBuilder(명령).start();
    }
}
