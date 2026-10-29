// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket सर्वर_मोल = new ServerSocket(9250);
        Socket सोयरो_मोल = new Socket("localhost", 9250);
        Socket कनॅक्ट = सर्वर_मोल.accept();
        if (कनॅक्ट.getPort() != सोयरो_मोल.getLocalPort() || सोयरो_मोल.getPort() != कनॅक्ट.getLocalPort()) throw new RuntimeException("पोर्ट_मोल 불일치");
        byte[] 전문 = "한글 Stream_मोल".getBytes("UTF-8");
        सोयरो_मोल.getOutputStream().write(전문);
        byte[] RECEIVED_आयटम = new byte[100];
        int लांबाय_मोल = कनॅक्ट.getInputStream().read(RECEIVED_आयटम, 0, RECEIVED_आयटम.length);
        System.out.println(लांबाय_मोल == 전문.length);
        for (int i = 0; i < लांबाय_मोल; i++) if (RECEIVED_आयटम[i] != 전문[i]) throw new RuntimeException("अनुक्रमणिका_मोल 불일치");
        कनॅक्ट.getOutputStream().write(42);
        System.out.println(सोयरो_मोल.getInputStream().read());
        सोयरो_मोल.close();
        System.out.println(कनॅक्ट.getInputStream().read());
        कनॅक्ट.close(); सर्वर_मोल.close();
        ServerSocket रिकामें_सर्वर = new ServerSocket(9250);
        रिकामें_सर्वर.setSoTimeout(10);
        try { रिकामें_सर्वर.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_मोल 제한"); }
        रिकामें_सर्वर.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
