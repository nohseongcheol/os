// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import فارسی.بومی.문자;
import فارسی.بومی.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket جلو_مقدار = 통신.باز_کردن(9431), برگشت_مقدار = 통신.باز_کردن(9432);
        try {
            통신.ارسال(جلو_مقدار, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(برگشت_مقدار));
            byte[] مبداء = 문자.부호화("회신"); جلو_مقدار.send(new DatagramPacket(مبداء, مبداء.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); برگشت_مقدار.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(برگشت_مقدار.getLocalPort());
            برگشت_مقدار.setSoTimeout(10);
            try { برگشت_مقدار.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 زمان_مقدار 초과"); }
            برگشت_مقدار.close();
            try { برگشت_مقدار.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { جلو_مقدار.close(); برگشت_مقدار.close(); }
    }
}
