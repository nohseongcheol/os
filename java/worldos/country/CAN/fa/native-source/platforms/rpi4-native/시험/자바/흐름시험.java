// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket سرور_مقدار = new ServerSocket(9250);
        Socket مهمان_مقدار = new Socket("localhost", 9250);
        Socket اتصال = سرور_مقدار.accept();
        if (اتصال.getPort() != مهمان_مقدار.getLocalPort() || مهمان_مقدار.getPort() != اتصال.getLocalPort()) throw new RuntimeException("تبدیل_مقدار 불일치");
        byte[] 전문 = "한글 جریان_مقدار".getBytes("UTF-8");
        مهمان_مقدار.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int طول_مقدار = اتصال.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(طول_مقدار == 전문.length);
        for (int i = 0; i < طول_مقدار; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("محتوا_مقدار 불일치");
        اتصال.getOutputStream().write(42);
        System.out.println(مهمان_مقدار.getInputStream().read());
        مهمان_مقدار.close();
        System.out.println(اتصال.getInputStream().read());
        اتصال.close(); سرور_مقدار.close();
        ServerSocket خالی_سرور = new ServerSocket(9250);
        خالی_سرور.setSoTimeout(10);
        try { خالی_سرور.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("زمان_مقدار 제한"); }
        خالی_سرور.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
