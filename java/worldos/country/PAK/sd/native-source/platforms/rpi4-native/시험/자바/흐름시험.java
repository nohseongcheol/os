// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket سرور_قدر = new ServerSocket(9250);
        Socket 손님 = new Socket("localhost", 9250);
        Socket ڪنيڪٽ = سرور_قدر.accept();
        if (ڪنيڪٽ.getPort() != 손님.getLocalPort() || 손님.getPort() != ڪنيڪٽ.getLocalPort()) throw new RuntimeException("پورٽ_قدر 불일치");
        byte[] 전문 = "한글 اسٽريم_قدر".getBytes("UTF-8");
        손님.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int لمبائي_قدر = ڪنيڪٽ.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(لمبائي_قدر == 전문.length);
        for (int i = 0; i < لمبائي_قدر; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("مواد_قدر 불일치");
        ڪنيڪٽ.getOutputStream().write(42);
        System.out.println(손님.getInputStream().read());
        손님.close();
        System.out.println(ڪنيڪٽ.getInputStream().read());
        ڪنيڪٽ.close(); سرور_قدر.close();
        ServerSocket خالي_سرور = new ServerSocket(9250);
        خالي_سرور.setSoTimeout(10);
        try { خالي_سرور.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        خالي_سرور.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
