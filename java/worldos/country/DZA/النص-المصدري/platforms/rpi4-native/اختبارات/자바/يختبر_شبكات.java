// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import العربية.ذاتي.문자;
import العربية.ذاتي.통신;
public class يختبر_شبكات {
    public static void main(String[] args) throws Exception {
        DatagramSocket الكاميرا_الأمامية_قيمة = 통신.فتح(9431), عودة_قيمة = 통신.فتح(9432);
        try {
            통신.يرسل(الكاميرا_الأمامية_قيمة, 9432, "자바 UDP 한글😀"); System.out.println(통신.يستلم(عودة_قيمة));
            byte[] مصدر = 문자.يرمّز("회신"); الكاميرا_الأمامية_قيمة.send(new DatagramPacket(مصدر, مصدر.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket رزمةمستقلة = new DatagramPacket(받은값, 받은값.length); عودة_قيمة.receive(رزمةمستقلة);
            System.out.println(رزمةمستقلة.getLength()); System.out.println(رزمةمستقلة.getPort()); System.out.println(رزمةمستقلة.getAddress().getHostAddress());
            System.out.println(عودة_قيمة.getLocalPort());
            عودة_قيمة.setSoTimeout(10);
            try { عودة_قيمة.receive(رزمةمستقلة); } catch (SocketTimeoutException e) { System.out.println("يستلم_قيمة قيمة_الوقت 초과"); }
            عودة_قيمة.close();
            try { عودة_قيمة.receive(رزمةمستقلة); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { الكاميرا_الأمامية_قيمة.close(); عودة_قيمة.close(); }
    }
}
