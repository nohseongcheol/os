// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class يختبر_بث {
    public static void main(String[] args) throws Exception {
        ServerSocket خادم_قيمة = new ServerSocket(9250);
        Socket ضيف_قيمة = new Socket("localhost", 9250);
        Socket اتصال = خادم_قيمة.accept();
        if (اتصال.getPort() != ضيف_قيمة.getLocalPort() || ضيف_قيمة.getPort() != اتصال.getLocalPort()) throw new RuntimeException("منفذ_قيمة 불일치");
        byte[] رزمةمستقلة = "한글 بث_قيمة".getBytes("UTF-8");
        ضيف_قيمة.getOutputStream().write(رزمةمستقلة);
        byte[] 받은것 = new byte[100];
        int 길이 = اتصال.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(길이 == رزمةمستقلة.length);
        for (int i = 0; i < 길이; i++) if (받은것[i] != رزمةمستقلة[i]) throw new RuntimeException("محتوى_قيمة 불일치");
        اتصال.getOutputStream().write(42);
        System.out.println(ضيف_قيمة.getInputStream().read());
        ضيف_قيمة.close();
        System.out.println(اتصال.getInputStream().read());
        اتصال.close(); خادم_قيمة.close();
        ServerSocket فارغ_خادم = new ServerSocket(9250);
        فارغ_خادم.setSoTimeout(10);
        try { فارغ_خادم.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("قيمة_الوقت 제한"); }
        فارغ_خادم.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
