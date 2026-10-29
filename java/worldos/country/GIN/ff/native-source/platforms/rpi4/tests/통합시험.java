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
    interface njaru { long 읽기(); }
    static class 부모 { protected long njaru = 42; }
    static class 자식 extends 부모 implements njaru { public long 읽기() { return njaru; } }
    private static void ƴeewtaade(boolean ngonka, String innde) {
        if (!ngonka) throw new AssertionError(innde);
        System.out.println("PASS " + innde);
    }
    public static void main(String[] 인수) throws Exception {
        String binndi = "한글 日本語 العربية हिन्दी 😀";
        Path resde_njaru = Path.of(System.getProperty("user.home"), "teeŋtingol_keɓe.txt");
        fiilde.winndude(resde_njaru, binndi);
        ƴeewtaade(fiilde.읽기(resde_njaru).equals(binndi), "UTF8_FILE");
        ƴeewtaade(문자.코드포인트수("한😀") == 2, "UNICODE");
        ƴeewtaade(문자.정규화("\u1100\u1161").equals("가"), "NORMALIZATION");
        njaru huunde_njaru = new 자식();
        ƴeewtaade(huunde_njaru.읽기() == 42 && (long)자식.class.getMethod("읽기").invoke(huunde_njaru) == 42, "OBJECT_INHERITANCE_REFLECTION");
        ƴeewtaade(Arrays.asList(1, 2, 3).stream().mapToInt(x -> x * x).sum() == 14, "LAMBDA_STREAM");
        try { throw new IOException("검증"); }
        catch (IOException 예외) { ƴeewtaade(예외.getMessage().equals("검증"), "EXCEPTION"); }
        AtomicInteger 합 = new AtomicInteger();
        Thread piilol_njaru = 작업.huutoraade("한글 piilol_njaru", () -> 합.set(123));
        작업.기다리기(piilol_njaru);
        ƴeewtaade(합.get() == 123, "THREAD");
        ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
        try (ServerSocket sarworde_njaru = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Future<?> 응답 = 일꾼.submit(() -> {
                try (Socket 소켓 = sarworde_njaru.accept()) {
                    BufferedReader 읽기 = new BufferedReader(new InputStreamReader(소켓.getInputStream()));
                    String diidol;
                    while ((diidol = 읽기.readLine()) != null && !diidol.isEmpty()) {}
                    byte[] 본문 = 문자.부호화(binndi);
                    소켓.getOutputStream().write(("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + 본문.length + "\r\nConnection: close\r\n\r\n").getBytes("US-ASCII"));
                    소켓.getOutputStream().write(본문);
                } catch (IOException juumre) { throw new UncheckedIOException(juumre); }
            });
            ƴeewtaade(통신.가져오기(URI.create("http://127.0.0.1:" + sarworde_njaru.getLocalPort()), Duration.ofSeconds(30)).body().equals(binndi), "HTTP_TCP");
            응답.get(30, TimeUnit.SECONDS);
        } finally { 일꾼.shutdownNow(); }
        ƴeewtaade(new ProcessBuilder("/bin/echo", "Yuɓɓo_golle_njaru").start().waitFor() == 0, "PROCESS");
        if (인수.length > 0 && 인수[0].equals("gui")) {
            SwingUtilities.invokeAndWait(() -> {
                Font fontere_njaru = new Font("Dialog", Font.PLAIN, 18);
                ƴeewtaade(fontere_njaru.canDisplayUpTo("한글日本語") == -1, "CJK_FONT");
                ƴeewtaade(fontere_njaru.canDisplayUpTo("العربيةहिन्दी") == -1, "ARABIC_DEVANAGARI_FONT");
                JTextArea 글상자 = new JTextArea(binndi);
                글상자.setFont(fontere_njaru);
                JFrame falanteere = 화면.falanteere("그래픽 검증", 글상자, 800, 240);
                BufferedImage natal_njaru_c143fe9e = new BufferedImage(800, 240, BufferedImage.TYPE_INT_RGB);
                Graphics2D 붓 = natal_njaru_c143fe9e.createGraphics();
                falanteere.paint(붓); 붓.dispose();
                try { javax.imageio.ImageIO.write(natal_njaru_c143fe9e, "png", Path.of(System.getProperty("user.home"), "그래픽시험.png").toFile()); }
                catch (IOException juumre) { throw new UncheckedIOException(juumre); }
                falanteere.dispose();
                ƴeewtaade(글상자.getText().equals(binndi), "SWING");
            });
        }
        System.out.println("JKOROS_JAVA_TEST_PASS");
    }
}
