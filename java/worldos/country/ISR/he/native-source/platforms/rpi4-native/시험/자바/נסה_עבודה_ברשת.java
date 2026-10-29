// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import עברית.עצמי.문자;
import עברית.עצמי.통신;
public class נסה_עבודה_ברשת {
    public static void main(String[] args) throws Exception {
        DatagramSocket מצלמה_קדמית_ערך_ec1a6b96 = 통신.פתח(9431), הקודם_ערך = 통신.פתח(9432);
        try {
            통신.שלח(מצלמה_קדמית_ערך_ec1a6b96, 9432, "자바 UDP 한글😀"); System.out.println(통신.לקבל(הקודם_ערך));
            byte[] קודמקור = 문자.לקדד("회신"); מצלמה_קדמית_ערך_ec1a6b96.send(new DatagramPacket(קודמקור, קודמקור.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket יחידת_נתונים = new DatagramPacket(받은값, 받은값.length); הקודם_ערך.receive(יחידת_נתונים);
            System.out.println(יחידת_נתונים.getLength()); System.out.println(יחידת_נתונים.getPort()); System.out.println(יחידת_נתונים.getAddress().getHostAddress());
            System.out.println(הקודם_ערך.getLocalPort());
            הקודם_ערך.setSoTimeout(10);
            try { הקודם_ערך.receive(יחידת_נתונים); } catch (SocketTimeoutException e) { System.out.println("לקבל_ערך_cef4d8ab ערך_זמן 초과"); }
            הקודם_ערך.close();
            try { הקודם_ערך.receive(יחידת_נתונים); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { מצלמה_קדמית_ערך_ec1a6b96.close(); הקודם_ערך.close(); }
    }
}
