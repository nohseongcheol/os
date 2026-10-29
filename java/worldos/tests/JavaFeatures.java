// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import java.lang.management.ManagementFactory;
import java.awt.event.*;
import java.io.*;
import java.net.*;
import java.net.http.*;
import java.nio.*;
import java.nio.channels.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.*;
import java.security.cert.CertificateFactory;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.jar.*;
import javax.net.ssl.*;
import javax.swing.*;
import javax.tools.ToolProvider;

public final class JavaFeatures {
    static void check(boolean value, String feature) {
        if (!value) throw new AssertionError(feature);
        System.out.println("PASS " + feature);
    }
    static String command(String... command) throws Exception {
        Process process = new ProcessBuilder(command).redirectErrorStream(true).start();
        String result = new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        if (process.waitFor() != 0) throw new AssertionError(Arrays.toString(command)+"\n"+result);
        return result;
    }
    public static void main(String[] args) {
        try { verify(args); } catch (Throwable error) { error.printStackTrace(); System.exit(1); }
    }
    static void verify(String[] args) throws Exception {
        Path workspace=Paths.get("/home/user/workspace");
        Path file=workspace.resolve("저장_日本語_العربية_हिन्दी.txt");
        String message="WorldOS persistent UTF-8 한글 日本語 العربية हिन्दी";
        boolean reboot=Files.exists(file);
        if (reboot) check(Files.readString(file).equals(message),"persistence-after-reboot");
        Files.writeString(file,message);
        try(FileChannel channel=FileChannel.open(file,StandardOpenOption.WRITE)){channel.force(true);}
        check(Files.readString(file).equals(message),"file-io-unicode");
        Path moved=workspace.resolve("atomic.txt");
        Files.writeString(moved,message);Files.move(moved,workspace.resolve("atomic-result.txt"),StandardCopyOption.REPLACE_EXISTING,StandardCopyOption.ATOMIC_MOVE);
        check(Files.exists(workspace.resolve("atomic-result.txt")),"atomic-move");
        Path link=workspace.resolve("symbolic");Files.deleteIfExists(link);Files.createSymbolicLink(link,file);
        check(Files.isSymbolicLink(link)&&Files.readString(link).equals(message),"symbolic-links");
        Path mapped=workspace.resolve("mapped.bin");
        try(FileChannel channel=FileChannel.open(mapped,StandardOpenOption.READ,StandardOpenOption.WRITE,StandardOpenOption.CREATE)){
            MappedByteBuffer buffer=channel.map(FileChannel.MapMode.READ_WRITE,0,4096);buffer.putInt(0,2026);buffer.force();check(buffer.getInt(0)==2026,"memory-map");
        }
        String source="public class 사용자 { public static void main(String[] 인수) { System.out.println(\"UNICODE_COMPILED\"); } }";
        Path javaFile=workspace.resolve("사용자.java");Files.writeString(javaFile,source);
        check(ToolProvider.getSystemJavaCompiler()!=null,"jdk-compiler-module");
        check(command("javac","-encoding","UTF-8",javaFile.toString()).isEmpty(),"guest-javac");
        check(command("java","-cp",workspace.toString(),"사용자").contains("UNICODE_COMPILED"),"guest-java-unicode-class");
        check(command("jar","--create","--file",workspace.resolve("sample.jar").toString(),"--main-class","사용자","-C",workspace.toString(),"사용자.class").isEmpty(),"guest-jar");
        check(command("java","-jar",workspace.resolve("sample.jar").toString()).contains("UNICODE_COMPILED"),"executable-jar");
        AtomicInteger count=new AtomicInteger();Thread[] threads=new Thread[8];
        for(int i=0;i<threads.length;i++){threads[i]=new Thread(()->{for(int j=0;j<10000;j++)count.incrementAndGet();});threads[i].start();}
        for(Thread thread:threads)thread.join();check(count.get()==80000,"threads-atomics");
        ExecutorService executor=Executors.newCachedThreadPool();
        try(ServerSocket server=new ServerSocket(0)){
            Future<?> reply=executor.submit(()->{try(Socket socket=server.accept()){socket.getOutputStream().write(socket.getInputStream().readNBytes(4));}catch(IOException e){throw new UncheckedIOException(e);}});
            try(Socket client=new Socket("127.0.0.1",server.getLocalPort())){client.setSoTimeout(5000);client.getOutputStream().write(new byte[]{1,2,3,4});check(Arrays.equals(client.getInputStream().readNBytes(4),new byte[]{1,2,3,4}),"tcp-loopback");}reply.get(10,TimeUnit.SECONDS);
        }
        try(DatagramSocket receiver=new DatagramSocket(0);DatagramSocket sender=new DatagramSocket()){
            receiver.setSoTimeout(5000);byte[] data=message.getBytes(StandardCharsets.UTF_8);
            sender.send(new DatagramPacket(data,data.length,InetAddress.getLoopbackAddress(),receiver.getLocalPort()));
            DatagramPacket packet=new DatagramPacket(new byte[256],256);receiver.receive(packet);check(packet.getLength()==data.length,"udp-loopback");
        }
        Properties network=new Properties();try(Reader reader=Files.newBufferedReader(Paths.get("/opt/worldos/network.properties"))){network.load(reader);}
        HttpClient client=HttpClient.newBuilder().connectTimeout(java.time.Duration.ofSeconds(60)).build();
        String http=client.send(HttpRequest.newBuilder(URI.create(network.getProperty("http"))).build(),HttpResponse.BodyHandlers.ofString()).body();
        check(http.equals(network.getProperty("token")),"http-external-to-guest");
        KeyStore store=KeyStore.getInstance(KeyStore.getDefaultType());store.load(null,null);
        try(InputStream input=Files.newInputStream(Paths.get("/opt/worldos/server.crt"))){store.setCertificateEntry("test",CertificateFactory.getInstance("X.509").generateCertificate(input));}
        TrustManagerFactory trust=TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());trust.init(store);
        SSLContext tls=SSLContext.getInstance("TLS");tls.init(null,trust.getTrustManagers(),null);
        HttpClient secure=HttpClient.newBuilder().sslContext(tls).connectTimeout(java.time.Duration.ofSeconds(60)).build();
        check(secure.send(HttpRequest.newBuilder(URI.create(network.getProperty("https"))).build(),HttpResponse.BodyHandlers.ofString()).body().equals(network.getProperty("token")),"https-verified-certificate");
        check(InetAddress.getAllByName("example.com").length>0,"dns-resolution");
        check(Class.forName("javax.swing.JFrame").getMethod("setVisible",boolean.class)!=null,"reflection");
        check(ManagementFactory.getCompilationMXBean()!=null,"jit-compiler");
        check(!GraphicsEnvironment.isHeadless(),"headful-awt");
        CountDownLatch clicked=new CountDownLatch(1);AtomicReference<JButton> button=new AtomicReference<>();AtomicReference<JFrame> frame=new AtomicReference<>();
        SwingUtilities.invokeAndWait(()->{JFrame window=new JFrame("WorldOS · 한글 · 日本語 · العربية · हिन्दी");JButton control=new JButton("OpenJDK Swing — click test");control.addActionListener(event->clicked.countDown());window.add(control);window.setSize(640,300);window.setLocation(100,100);window.setVisible(true);button.set(control);frame.set(window);});
        Robot robot=new Robot();robot.waitForIdle();Thread.sleep(500);
        AtomicReference<Point> location=new AtomicReference<>();SwingUtilities.invokeAndWait(()->location.set(button.get().getLocationOnScreen()));
        robot.mouseMove(location.get().x+100,location.get().y+80);robot.mousePress(InputEvent.BUTTON1_DOWN_MASK);robot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
        check(clicked.await(5,TimeUnit.SECONDS),"swing-robot-input");
        javax.imageio.ImageIO.write(robot.createScreenCapture(new Rectangle(Toolkit.getDefaultToolkit().getScreenSize())),"png",workspace.resolve("swing.png").toFile());
        SwingUtilities.invokeAndWait(()->frame.get().dispose());executor.shutdownNow();
        System.out.println("WORLDOS_JAVA_FEATURES_OK reboot="+reboot);
    }
}
