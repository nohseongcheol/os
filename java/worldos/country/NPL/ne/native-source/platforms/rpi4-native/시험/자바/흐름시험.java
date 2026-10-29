// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket सर्भर_मान = new ServerSocket(9250);
        Socket अतिथि_मान = new Socket("localhost", 9250);
        Socket जडान = सर्भर_मान.accept();
        if (जडान.getPort() != अतिथि_मान.getLocalPort() || अतिथि_मान.getPort() != जडान.getLocalPort()) throw new RuntimeException("पोर्ट_मान 불일치");
        byte[] 전문 = "한글 प्रवाह_मान".getBytes("UTF-8");
        अतिथि_मान.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int लम्बाइ_मान = जडान.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(लम्बाइ_मान == 전문.length);
        for (int i = 0; i < लम्बाइ_मान; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("सामग्री_मान 불일치");
        जडान.getOutputStream().write(42);
        System.out.println(अतिथि_मान.getInputStream().read());
        अतिथि_मान.close();
        System.out.println(जडान.getInputStream().read());
        जडान.close(); सर्भर_मान.close();
        ServerSocket रिक्त_सर्भर = new ServerSocket(9250);
        रिक्त_सर्भर.setSoTimeout(10);
        try { रिक्त_सर्भर.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        रिक्त_सर्भर.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
