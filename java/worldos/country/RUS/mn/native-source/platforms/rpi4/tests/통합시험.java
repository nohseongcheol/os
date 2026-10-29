// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Монгол.자바.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import javax.swing.*;
import java.net.*;
import java.io.*;
import java.nio.file.*;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class 통합시험 {
    interface утга { long Унших(); }
    static class 부모 { protected long утга = 42; }
    static class хүүхэд_утга extends 부모 implements утга { public long Унших() { return утга; } }
    private static void шалгах(boolean нөхцөл, String Нэр) {
        if (!нөхцөл) throw new AssertionError(Нэр);
        System.out.println("PASS " + Нэр);
    }
    public static void main(String[] 인수) throws Exception {
        String Бичвэр = "한글 日本語 العربية हिन्दी 😀";
        Path хадгалах_утга = Path.of(System.getProperty("user.home"), "баталгаажуулалт_өгөгдөл.txt");
        Файл.Бичих(хадгалах_утга, Бичвэр);
        шалгах(Файл.Унших(хадгалах_утга).equals(Бичвэр), "UTF8_FILE");
        шалгах(문자.코드포인트수("한😀") == 2, "UNICODE");
        шалгах(문자.нормчлох_утга("\u1100\u1161").equals("가"), "NORMALIZATION");
        утга объект_утга = new хүүхэд_утга();
        шалгах(объект_утга.Унших() == 42 && (long)хүүхэд_утга.class.getMethod("Унших").invoke(объект_утга) == 42, "OBJECT_INHERITANCE_REFLECTION");
        шалгах(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("баталгаажуулах"); }
        catch (IOException 예외) { шалгах(예외.getMessage().equals("баталгаажуулах"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread яриа_утга = 작업.Ажиллуулах("한글 яриа_утга", () -> 합.set(123));
        작업.기다리기(яриа_утга);
        шалгах(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket сервер_утга = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> хариулах = 일꾼.submit(() -> {
                try (Socket 소켓 = сервер_утга.accept()) {
                    BufferedReader Унших = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Шугам;
                    while ((Шугам = Унших.readLine()) != null && !Шугам.isEmpty()) {}
                    byte[] үндсэн_бичвэр = 문자.부호화(Бичвэр);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + үндсэн_бичвэр.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(үндсэн_бичвэр);
                } catch (IOException Алдаа) { throw new UncheckedIOException(Алдаа); }
            });
            шалгах(통신.가져오기(URI.create("http://127.0.0.1:" + сервер_утга.getLocalPort()), Duration.ofSeconds(30)).body().equals(Бичвэр), "HTTP_TCP");
            хариулах.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        шалгах(new ProcessBuilder("/bin/echo", "үйл_явц_утга").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font үсгийн_хэв_утга = new Font("Dialog", Font.PLAIN, 18);
                шалгах(үсгийн_хэв_утга.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                шалгах(үсгийн_хэв_утга.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea Бичвэрийн_муж = new JTextArea(Бичвэр);
                Бичвэрийн_муж.setFont(үсгийн_хэв_утга);
                JFrame цонх = 화면.цонх("그래픽 баталгаажуулах", Бичвэрийн_муж, 800, 240);
                BufferedImage зураг_утга_c143fe9e = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = зураг_утга_c143fe9e.createGraphics();
                цонх.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(зураг_утга_c143fe9e, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Алдаа) { throw new UncheckedIOException(Алдаа); }
                цонх.dispose();
                шалгах(Бичвэрийн_муж.getText().equals(Бичвэр), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
