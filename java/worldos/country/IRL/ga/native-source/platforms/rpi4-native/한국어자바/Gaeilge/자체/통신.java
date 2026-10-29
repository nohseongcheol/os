// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 digit_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Oscail(int port_VALUE) throws I_O_eisceacht {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static void seol(DatagramSocket 종단, int port_VALUE, String Inneachar_VALUE) throws I_O_eisceacht {
        try {
        seol(종단, "127.0.0.1", port_VALUE, Inneachar_VALUE);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static void seol(DatagramSocket 종단, String ADDRESS, int port_VALUE, String Inneachar_VALUE) throws I_O_eisceacht {
        try {
        byte[] beart_VALUE = 문자.부호화(Inneachar_VALUE);
        종단.send(new DatagramPacket(beart_VALUE, beart_VALUE.length, InetAddress.getByName(ADDRESS), port_VALUE));
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static String 받기(DatagramSocket 종단) throws I_O_eisceacht {
        try {
        byte[] beart_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(beart_VALUE, beart_VALUE.length); 종단.receive(전문);
        byte[] tomhas = new byte[전문.getLength()]; System.arraycopy(beart_VALUE, 0, tomhas, 0, tomhas.length); return 문자.díchriptigh_sonraí(tomhas);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static void TIMEOUT(DatagramSocket 종단, int 밀리초) throws I_O_eisceacht {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static void Dún(DatagramSocket 종단) { 종단.close(); }
}
