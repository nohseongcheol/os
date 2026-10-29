// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 അക്കം_മൂല്യം 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket തുറക്കുക(int പോര്_ട്ട്_മൂല്യം) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return new DatagramSocket(പോര്_ട്ട്_മൂല്യം);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public static void അയയ്ക്കുക(DatagramSocket അവസാനബിന്ദു, int പോര്_ട്ട്_മൂല്യം, String ഉള്ളടക്കം_മൂല്യം) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try {
        അയയ്ക്കുക(അവസാനബിന്ദു, "127.0.0.1", പോര്_ട്ട്_മൂല്യം, ഉള്ളടക്കം_മൂല്യം);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public static void അയയ്ക്കുക(DatagramSocket അവസാനബിന്ദു, String ഇമെയിൽ, int പോര്_ട്ട്_മൂല്യം, String ഉള്ളടക്കം_മൂല്യം) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try {
        byte[] బైట్_മൂല്യം = 문자.부호화(ഉള്ളടക്കം_മൂല്യം);
        അവസാനബിന്ദു.send(new DatagramPacket(బైట్_മൂല്യം, బైట్_മൂല്യം.length, InetAddress.getByName(ഇമെയിൽ), പോര്_ട്ട്_മൂല്യം));
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public static String 받기(DatagramSocket അവസാനബിന്ദു) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try {
        byte[] బైట్_മൂല്യം = new byte[512]; DatagramPacket 전문 = new DatagramPacket(బైట్_മൂല്യം, బైట్_മൂല്യം.length); അവസാനബിന്ദു.receive(전문);
        byte[] അളവ് = new byte[전문.getLength()]; System.arraycopy(బైట్_മൂല്യം, 0, അളവ്, 0, അളവ്.length); return 문자.ഗൂഢഭാഷമാറ്റുക_ഡാറ്റാ(അളവ്);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public static void ടൈംഔട്ട്(DatagramSocket അവസാനബിന്ദു, int 밀리초) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { അവസാനബിന്ദു.setSoTimeout(밀리초);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public static void അടയ്ക്കു(DatagramSocket അവസാനബിന്ദു) { അവസാനബിന്ദു.close(); }
}
