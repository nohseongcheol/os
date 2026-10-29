// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import বাংলা.নিজ.문자;
import বাংলা.নিজ.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket সম্মুখ_মান = 통신.খুলুন(9431), ফিরে_যান_মান = 통신.খুলুন(9432);
        try {
            통신.পাঠান(সম্মুখ_মান, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(ফিরে_যান_মান));
            byte[] উৎস_নথি = 문자.부호화("회신"); সম্মুখ_মান.send(new DatagramPacket(উৎস_নথি, উৎস_নথি.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); ফিরে_যান_মান.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(ফিরে_যান_মান.getLocalPort());
            ফিরে_যান_মান.setSoTimeout(10);
            try { ফিরে_যান_মান.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 সময়_মান 초과"); }
            ফিরে_যান_মান.close();
            try { ফিরে_যান_মান.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { সম্মুখ_মান.close(); ফিরে_যান_মান.close(); }
    }
}
