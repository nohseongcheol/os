// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
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
    interface 값 { long Llectura(); }
    static class 부모 { protected long 값 = 42; }
    static class 자식 extends 부모 implements 값 { public long Llectura() { return 값; } }
    private static void 확인(boolean 조건, String Nome) {
        if (!조건) throw new AssertionError(Nome);
        System.out.println("PASS " + Nome);
    }
    public static void main(String[] Argumentu) throws Exception {
        String Testu = "한글 日本語 العربية हिन्दी 😀";
        Path 저장 = Path.of(System.getProperty("user.home"), "검증자료.txt");
        Ficheru.Escritura(저장, Testu);
        확인(Ficheru.Llectura(저장).equals(Testu), "UTF8_FILE");
        확인(문자.코드포인트수("한😀") == 2, "UNICODE");
        확인(문자.정규화("\u1100\u1161").equals("가"), "NORMALIZATION");
        값 객체 = new 자식();
        확인(객체.Llectura() == 42 && (long)자식.class.getMethod("Llectura").invoke(객체) == 42, "OBJECT_INHERITANCE_REFLECTION");
        확인(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("검증"); }
        catch (IOException 예외) { 확인(예외.getMessage().equals("검증"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread 가닥 = 작업.Executar_2("한글 가닥", () -> 합.set(123));
        작업.기다리기(가닥);
        확인(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket 서버 = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> 응답 = 일꾼.submit(() -> {
                try (Socket 소켓 = 서버.accept()) {
                    BufferedReader Llectura = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String Llinia;
                    while ((Llinia = Llectura.readLine()) != null && !Llinia.isEmpty()) {}
                    byte[] 본문 = 문자.부호화(Testu);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + 본문.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(본문);
                } catch (IOException Fallu) { throw new UncheckedIOException(Fallu); }
            });
            확인(통신.가져오기(URI.create("http://127.0.0.1:" + 서버.getLocalPort()), Duration.ofSeconds(30)).body().equals(Testu), "HTTP_TCP");
            응답.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        확인(new ProcessBuilder("/bin/echo", "과정").start().waitFor() == 0, "PROCESS");
        if (Argumentu.length > 0 && Argumentu[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font 글꼴 = new Font("Dialog", Font.PLAIN, 18);
                확인(글꼴.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                확인(글꼴.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea 글상자 = new JTextArea(Testu);
                글상자.setFont(글꼴);
                JFrame Ventana = 화면.Ventana("그래픽 검증", 글상자, 800, 240);
                BufferedImage 그림 = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = 그림.createGraphics();
                Ventana.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(그림, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException Fallu) { throw new UncheckedIOException(Fallu); }
                Ventana.dispose();
                확인(글상자.getText().equals(Testu), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
