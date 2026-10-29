// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Nederlands.Eigen.문자;
import Nederlands.Eigen.communicatie;
public class test_Netwerken {
    public static void main(String[] args) throws Exception {
        DatagramSocket voorkant_WAARDE = communicatie.Openen(9431), BACK_WAARDE = communicatie.Openen(9432);
        try {
            communicatie.e_mailen(voorkant_WAARDE, 9432, "자바 UDP 한글😀"); System.out.println(communicatie.ontvangen(BACK_WAARDE));
            byte[] broncode = 문자.coderen("회신"); voorkant_WAARDE.send(new DatagramPacket(broncode, broncode.length, InetAddress.getByName("localhost"), 9432));
            byte[] OPBRENGST_WAARDE = new byte[32]; DatagramPacket datagram = new DatagramPacket(OPBRENGST_WAARDE, OPBRENGST_WAARDE.length); BACK_WAARDE.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(BACK_WAARDE.getLocalPort());
            BACK_WAARDE.setSoTimeout(10);
            try { BACK_WAARDE.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("ontvangen_WAARDE TIJD_WAARDE 초과"); }
            BACK_WAARDE.close();
            try { BACK_WAARDE.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 communicatie"); }
        } finally { voorkant_WAARDE.close(); BACK_WAARDE.close(); }
    }
}
