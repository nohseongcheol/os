// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Íslenska.eigin.문자;
import Íslenska.eigin.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket myndavél_að_framan_VALUE = 통신.Opna(9431), TIL_BAKA_VALUE = 통신.Opna(9432);
        try {
            통신.senda(myndavél_að_framan_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(TIL_BAKA_VALUE));
            byte[] Uppruni = 문자.부호화("회신"); myndavél_að_framan_VALUE.send(new DatagramPacket(Uppruni, Uppruni.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); TIL_BAKA_VALUE.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(TIL_BAKA_VALUE.getLocalPort());
            TIL_BAKA_VALUE.setSoTimeout(10);
            try { TIL_BAKA_VALUE.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 TIME_VALUE 초과"); }
            TIL_BAKA_VALUE.close();
            try { TIL_BAKA_VALUE.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { myndavél_að_framan_VALUE.close(); TIL_BAKA_VALUE.close(); }
    }
}
