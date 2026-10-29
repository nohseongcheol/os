// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket сервер_қимат = new ServerSocket(9250);
        Socket меҳмон_қимат = new Socket("localhost", 9250);
        Socket ПАЙВАСТ = сервер_қимат.accept();
        if (ПАЙВАСТ.getPort() != меҳмон_қимат.getLocalPort() || меҳмон_қимат.getPort() != ПАЙВАСТ.getLocalPort()) throw new RuntimeException("порт_қимат 불일치");
        byte[] 전문 = "한글 ҷараён_қимат".getBytes("UTF-8");
        меҳмон_қимат.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int дарозӣ_қимат = ПАЙВАСТ.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(дарозӣ_қимат == 전문.length);
        for (int i = 0; i < дарозӣ_қимат; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Мӯҳтаво_қимат 불일치");
        ПАЙВАСТ.getOutputStream().write(42);
        System.out.println(меҳмон_қимат.getInputStream().read());
        меҳмон_қимат.close();
        System.out.println(ПАЙВАСТ.getInputStream().read());
        ПАЙВАСТ.close(); сервер_қимат.close();
        ServerSocket холӣ_сервер = new ServerSocket(9250);
        холӣ_сервер.setSoTimeout(10);
        try { холӣ_сервер.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        холӣ_сервер.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
