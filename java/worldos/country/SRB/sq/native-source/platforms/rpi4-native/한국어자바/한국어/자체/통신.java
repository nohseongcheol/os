// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 shifër_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Hap(int portë_VALUE) throws I_O_përjashtim {
        try { return new DatagramSocket(portë_VALUE);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static void dërgoj(DatagramSocket 종단, int portë_VALUE, String Përmbajtje_VALUE) throws I_O_përjashtim {
        try {
        dërgoj(종단, "127.0.0.1", portë_VALUE, Përmbajtje_VALUE);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static void dërgoj(DatagramSocket 종단, String email, int portë_VALUE, String Përmbajtje_VALUE) throws I_O_përjashtim {
        try {
        byte[] bajt_VALUE = 문자.부호화(Përmbajtje_VALUE);
        종단.send(new DatagramPacket(bajt_VALUE, bajt_VALUE.length, InetAddress.getByName(email), portë_VALUE));
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static String 받기(DatagramSocket 종단) throws I_O_përjashtim {
        try {
        byte[] bajt_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(bajt_VALUE, bajt_VALUE.length); 종단.receive(전문);
        byte[] llogaritje = new byte[전문.getLength()]; System.arraycopy(bajt_VALUE, 0, llogaritje, 0, llogaritje.length); return 문자.dekriptoj_të_dhëna(llogaritje);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static void TIMEOUT(DatagramSocket 종단, int 밀리초) throws I_O_përjashtim {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static void Mbyll(DatagramSocket 종단) { 종단.close(); }
}
