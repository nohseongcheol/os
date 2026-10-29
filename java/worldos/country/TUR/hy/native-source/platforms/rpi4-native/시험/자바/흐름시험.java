// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket սպասարկիչ_արժեք = new ServerSocket(9250);
        Socket հյուր_արժեք = new Socket("localhost", 9250);
        Socket Միացնել = սպասարկիչ_արժեք.accept();
        if (Միացնել.getPort() != հյուր_արժեք.getLocalPort() || հյուր_արժեք.getPort() != Միացնել.getLocalPort()) throw new RuntimeException("միացք_արժեք 불일치");
        byte[] 전문 = "한글 հոսք_արժեք".getBytes("UTF-8");
        հյուր_արժեք.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int տեւողություն_արժեք = Միացնել.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(տեւողություն_արժեք == 전문.length);
        for (int i = 0; i < տեւողություն_արժեք; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Բովանդակություն_արժեք 불일치");
        Միացնել.getOutputStream().write(42);
        System.out.println(հյուր_արժեք.getInputStream().read());
        հյուր_արժեք.close();
        System.out.println(Միացնել.getInputStream().read());
        Միացնել.close(); սպասարկիչ_արժեք.close();
        ServerSocket դատարկ_սպասարկիչ = new ServerSocket(9250);
        դատարկ_սպասարկիչ.setSoTimeout(10);
        try { դատարկ_սպասարկիչ.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        դատարկ_սպասարկիչ.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
