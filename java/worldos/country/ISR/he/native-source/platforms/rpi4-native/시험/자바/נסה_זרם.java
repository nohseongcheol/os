// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class נסה_זרם {
    public static void main(String[] args) throws Exception {
        ServerSocket שרת_ערך = new ServerSocket(9250);
        Socket אורח_ערך = new Socket("localhost", 9250);
        Socket חיבור = שרת_ערך.accept();
        if (חיבור.getPort() != אורח_ערך.getLocalPort() || אורח_ערך.getPort() != חיבור.getLocalPort()) throw new RuntimeException("הסב_ערך 불일치");
        byte[] יחידת_נתונים = "한글 זרם_ערך".getBytes("UTF-8");
        אורח_ערך.getOutputStream().write(יחידת_נתונים);
        byte[] 받은것 = new byte[100];
        int 길이 = חיבור.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(길이 == יחידת_נתונים.length);
        for (int i = 0; i < 길이; i++) if (받은것[i] != יחידת_נתונים[i]) throw new RuntimeException("תוכן_ערך 불일치");
        חיבור.getOutputStream().write(42);
        System.out.println(אורח_ערך.getInputStream().read());
        אורח_ערך.close();
        System.out.println(חיבור.getInputStream().read());
        חיבור.close(); שרת_ערך.close();
        ServerSocket ריק_שרת = new ServerSocket(9250);
        ריק_שרת.setSoTimeout(10);
        try { ריק_שרת.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("ערך_זמן 제한"); }
        ריק_שרת.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
