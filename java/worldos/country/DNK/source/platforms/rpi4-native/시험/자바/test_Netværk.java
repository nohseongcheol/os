// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Dansk.eget.문자;
import Dansk.eget.통신;
public class test_Netværk {
    public static void main(String[] args) throws Exception {
        DatagramSocket frontvendt_VÆRDI = 통신.Åbn(9431), BACK_VÆRDI = 통신.Åbn(9432);
        try {
            통신.maile(frontvendt_VÆRDI, 9432, "자바 UDP 한글😀"); System.out.println(통신.modtage(BACK_VÆRDI));
            byte[] KILDE = 문자.kode("회신"); frontvendt_VÆRDI.send(new DatagramPacket(KILDE, KILDE.length, InetAddress.getByName("localhost"), 9432));
            byte[] MODTAGET_VED_UDLØB_VÆRDI = new byte[32]; DatagramPacket datagram = new DatagramPacket(MODTAGET_VED_UDLØB_VÆRDI, MODTAGET_VED_UDLØB_VÆRDI.length); BACK_VÆRDI.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(BACK_VÆRDI.getLocalPort());
            BACK_VÆRDI.setSoTimeout(10);
            try { BACK_VÆRDI.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("modtage_VÆRDI TID_VÆRDI 초과"); }
            BACK_VÆRDI.close();
            try { BACK_VÆRDI.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { frontvendt_VÆRDI.close(); BACK_VÆRDI.close(); }
    }
}
