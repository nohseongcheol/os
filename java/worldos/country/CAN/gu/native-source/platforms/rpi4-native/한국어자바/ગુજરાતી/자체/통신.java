// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 અંક_મૂલ્ય 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket ખોલો(int પૉર્ટ_મૂલ્ય) throws 입출력예외 {
        try { return new DatagramSocket(પૉર્ટ_મૂલ્ય);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static void મોકલો(DatagramSocket 종단, int પૉર્ટ_મૂલ્ય, String સામગ્રી_મૂલ્ય) throws 입출력예외 {
        try {
        મોકલો(종단, "127.0.0.1", પૉર્ટ_મૂલ્ય, સામગ્રી_મૂલ્ય);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static void મોકલો(DatagramSocket 종단, String સરનામું, int પૉર્ટ_મૂલ્ય, String સામગ્રી_મૂલ્ય) throws 입출력예외 {
        try {
        byte[] બાઇટ_મૂલ્ય = 문자.부호화(સામગ્રી_મૂલ્ય);
        종단.send(new DatagramPacket(બાઇટ_મૂલ્ય, બાઇટ_મૂલ્ય.length, InetAddress.getByName(સરનામું), પૉર્ટ_મૂલ્ય));
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] બાઇટ_મૂલ્ય = new byte[512]; DatagramPacket 전문 = new DatagramPacket(બાઇટ_મૂલ્ય, બાઇટ_મૂલ્ય.length); 종단.receive(전문);
        byte[] પરિમાણ = new byte[전문.getLength()]; System.arraycopy(બાઇટ_મૂલ્ય, 0, પરિમાણ, 0, પરિમાણ.length); return 문자.ડિક્રિપ્ટ_કરો_ડેટા(પરિમાણ);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static void બંધ_કરો(DatagramSocket 종단) { 종단.close(); }
}
