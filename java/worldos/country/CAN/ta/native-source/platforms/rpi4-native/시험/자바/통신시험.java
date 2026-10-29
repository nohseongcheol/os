// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import தமிழ்.자체.문자;
import தமிழ்.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket முன்_மதிப்பு = 통신.திற(9431), பின்_மதிப்பு = 통신.திற(9432);
        try {
            통신.அனுப்பு(முன்_மதிப்பு, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(பின்_மதிப்பு));
            byte[] மூலக்_கோப்பு = 문자.부호화("회신"); முன்_மதிப்பு.send(new DatagramPacket(மூலக்_கோப்பு, மூலக்_கோப்பு.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); பின்_மதிப்பு.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(பின்_மதிப்பு.getLocalPort());
            பின்_மதிப்பு.setSoTimeout(10);
            try { பின்_மதிப்பு.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 நேர_மதிப்பு 초과"); }
            பின்_மதிப்பு.close();
            try { பின்_மதிப்பு.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { முன்_மதிப்பு.close(); பின்_மதிப்பு.close(); }
    }
}
