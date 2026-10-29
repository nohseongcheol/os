// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 숫자 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket ᎯᏍᏚᎢ(int ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try { return new DatagramSocket(ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static void ᏫᎦᏅᏗ(DatagramSocket 종단, int ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ, String ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try {
        ᏫᎦᏅᏗ(종단, "127.0.0.1", ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static void ᏫᎦᏅᏗ(DatagramSocket 종단, String ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ, String ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try {
        byte[] byte_ᏧᎬᏩᎶᏗᏯ = 문자.부호화(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ);
        종단.send(new DatagramPacket(byte_ᏧᎬᏩᎶᏗᏯ, byte_ᏧᎬᏩᎶᏗᏯ.length, InetAddress.getByName(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ), ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ));
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] byte_ᏧᎬᏩᎶᏗᏯ = new byte[512]; DatagramPacket 전문 = new DatagramPacket(byte_ᏧᎬᏩᎶᏗᏯ, byte_ᏧᎬᏩᎶᏗᏯ.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(byte_ᏧᎬᏩᎶᏗᏯ, 0, 결과, 0, 결과.length); return 문자.ᎠᎭᏓᏗᎭ_ᎦᏟᏌᏅᎯ(결과);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static void ᎯᏍᏚᎲᎦ(DatagramSocket 종단) { 종단.close(); }
}
