// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import slovenščina.lastno.문자;
import slovenščina.lastno.통신;
public class preskusiti_Uporaba_omrežij {
    public static void main(String[] args) throws Exception {
        DatagramSocket sprednja_VALUE = 통신.Odpri(9431), ZAJ_VALUE = 통신.Odpri(9432);
        try {
            통신.poslati(sprednja_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.sprejeti_sprejemati_prejeti_prejemati(ZAJ_VALUE));
            byte[] VIR = 문자.kodirati("회신"); sprednja_VALUE.send(new DatagramPacket(VIR, VIR.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket datagram = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); ZAJ_VALUE.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(ZAJ_VALUE.getLocalPort());
            ZAJ_VALUE.setSoTimeout(10);
            try { ZAJ_VALUE.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("sprejeti_sprejemati_prejeti_prejemati_VALUE čas_VALUE 초과"); }
            ZAJ_VALUE.close();
            try { ZAJ_VALUE.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { sprednja_VALUE.close(); ZAJ_VALUE.close(); }
    }
}
