// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import नेपाली.निज.문자;
import नेपाली.निज.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 앞 = 통신.खोल्नुहोस्(9431), पछाडि_मान = 통신.खोल्नुहोस्(9432);
        try {
            통신.पठाउनुहोस्(앞, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(पछाडि_मान));
            byte[] स्रोत = 문자.부호화("회신"); 앞.send(new DatagramPacket(स्रोत, स्रोत.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); पछाडि_मान.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(पछाडि_मान.getLocalPort());
            पछाडि_मान.setSoTimeout(10);
            try { पछाडि_मान.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 시간 초과"); }
            पछाडि_मान.close();
            try { पछाडि_मान.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { 앞.close(); पछाडि_मान.close(); }
    }
}
