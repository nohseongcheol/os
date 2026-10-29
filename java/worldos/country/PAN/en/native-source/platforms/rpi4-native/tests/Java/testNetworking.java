// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import English.Native.Characters;
import English.Native.communication;
public class testNetworking {
    public static void main(String[] args) throws Exception {
        DatagramSocket frontValue = communication.open(9431), backValue = communication.open(9432);
        try {
            communication.send(frontValue, 9432, "Java UDP 한글😀"); System.out.println(communication.receive(backValue));
            byte[] source = Characters.encode("회신"); frontValue.send(new DatagramPacket(source, source.length, InetAddress.getByName("localhost"), 9432));
            byte[] receivedValue = new byte[32]; DatagramPacket datagram = new DatagramPacket(receivedValue, receivedValue.length); backValue.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(backValue.getLocalPort());
            backValue.setSoTimeout(10);
            try { backValue.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("receiveValue timeValue 초과"); }
            backValue.close();
            try { backValue.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 communication"); }
        } finally { frontValue.close(); backValue.close(); }
    }
}
