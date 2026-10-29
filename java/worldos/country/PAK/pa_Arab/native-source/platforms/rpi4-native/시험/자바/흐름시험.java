// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket سرور_قدر = new ServerSocket(9250);
        Socket مہمان_قدر = new Socket("localhost", 9250);
        Socket جڑو = سرور_قدر.accept();
        if (جڑو.getPort() != مہمان_قدر.getLocalPort() || مہمان_قدر.getPort() != جڑو.getLocalPort()) throw new RuntimeException("دہانہ_قدر 불일치");
        byte[] 전문 = "한글 سٹریم_قدر".getBytes("UTF-8");
        مہمان_قدر.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int لمبائی_قدر = جڑو.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(لمبائی_قدر == 전문.length);
        for (int i = 0; i < لمبائی_قدر; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("اجزاء_قدر 불일치");
        جڑو.getOutputStream().write(42);
        System.out.println(مہمان_قدر.getInputStream().read());
        مہمان_قدر.close();
        System.out.println(جڑو.getInputStream().read());
        جڑو.close(); سرور_قدر.close();
        ServerSocket خالی_سرور = new ServerSocket(9250);
        خالی_سرور.setSoTimeout(10);
        try { خالی_سرور.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        خالی_سرور.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
