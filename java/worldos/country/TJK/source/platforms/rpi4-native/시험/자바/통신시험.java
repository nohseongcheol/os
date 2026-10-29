// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 앞 = 통신.кушодан(9431), Бозгашт_қимат = 통신.кушодан(9432);
        try {
            통신.фиристодан(앞, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(Бозгашт_қимат));
            byte[] манбаъ = 문자.부호화("회신"); 앞.send(new DatagramPacket(манбаъ, манбаъ.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); Бозгашт_қимат.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(Бозгашт_қимат.getLocalPort());
            Бозгашт_қимат.setSoTimeout(10);
            try { Бозгашт_қимат.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 시간 초과"); }
            Бозгашт_қимат.close();
            try { Бозгашт_қимат.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { 앞.close(); Бозгашт_қимат.close(); }
    }
}
