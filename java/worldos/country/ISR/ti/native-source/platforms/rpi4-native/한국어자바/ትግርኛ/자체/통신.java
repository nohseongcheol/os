// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 ኣሃዝ_ዋጋ 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket ክፈት(int ወደብ_ዋጋ) throws 입출력예외 {
        try { return new DatagramSocket(ወደብ_ዋጋ);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static void ለኣኽ(DatagramSocket 종단, int ወደብ_ዋጋ, String ትሕዝቶ_ዋጋ) throws 입출력예외 {
        try {
        ለኣኽ(종단, "127.0.0.1", ወደብ_ዋጋ, ትሕዝቶ_ዋጋ);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static void ለኣኽ(DatagramSocket 종단, String ኣድራሻ, int ወደብ_ዋጋ, String ትሕዝቶ_ዋጋ) throws 입출력예외 {
        try {
        byte[] ባይት_ዋጋ = 문자.부호화(ትሕዝቶ_ዋጋ);
        종단.send(new DatagramPacket(ባይት_ዋጋ, ባይት_ዋጋ.length, InetAddress.getByName(ኣድራሻ), ወደብ_ዋጋ));
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] ባይት_ዋጋ = new byte[512]; DatagramPacket 전문 = new DatagramPacket(ባይት_ዋጋ, ባይት_ዋጋ.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(ባይት_ዋጋ, 0, 결과, 0, 결과.length); return 문자.ምስጢር_ፍታሕ_ሓበሬታ(결과);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static void ዕጸው(DatagramSocket 종단) { 종단.close(); }
}
