// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket сервер_значэнне = new ServerSocket(9250);
        Socket госць_значэнне = new Socket("localhost", 9250);
        Socket Злучыцца = сервер_значэнне.accept();
        if (Злучыцца.getPort() != госць_значэнне.getLocalPort() || госць_значэнне.getPort() != Злучыцца.getLocalPort()) throw new RuntimeException("порт_значэнне 불일치");
        byte[] 전문 = "한글 паток_значэнне".getBytes("UTF-8");
        госць_значэнне.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int даўжыня_значэнне = Злучыцца.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(даўжыня_значэнне == 전문.length);
        for (int i = 0; i < даўжыня_значэнне; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("кантэнт_значэнне 불일치");
        Злучыцца.getOutputStream().write(42);
        System.out.println(госць_значэнне.getInputStream().read());
        госць_значэнне.close();
        System.out.println(Злучыцца.getInputStream().read());
        Злучыцца.close(); сервер_значэнне.close();
        ServerSocket нулявая_сервер = new ServerSocket(9250);
        нулявая_сервер.setSoTimeout(10);
        try { нулявая_сервер.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("час_значэнне 제한"); }
        нулявая_сервер.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
