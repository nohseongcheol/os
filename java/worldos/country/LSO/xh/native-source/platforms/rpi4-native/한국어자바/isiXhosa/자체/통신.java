// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 inani_ixabiso 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Vula(int iphothi_ixabiso) throws 입출력예외 {
        try { return new DatagramSocket(iphothi_ixabiso);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static void thumela(DatagramSocket 종단, int iphothi_ixabiso, String Isiqulatho_ixabiso) throws 입출력예외 {
        try {
        thumela(종단, "127.0.0.1", iphothi_ixabiso, Isiqulatho_ixabiso);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static void thumela(DatagramSocket 종단, String idilesi, int iphothi_ixabiso, String Isiqulatho_ixabiso) throws 입출력예외 {
        try {
        byte[] ibhayithi_ixabiso = 문자.부호화(Isiqulatho_ixabiso);
        종단.send(new DatagramPacket(ibhayithi_ixabiso, ibhayithi_ixabiso.length, InetAddress.getByName(idilesi), iphothi_ixabiso));
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] ibhayithi_ixabiso = new byte[512]; DatagramPacket 전문 = new DatagramPacket(ibhayithi_ixabiso, ibhayithi_ixabiso.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(ibhayithi_ixabiso, 0, 결과, 0, 결과.length); return 문자.buyisela_ubhalo_oluqhelekileyo_iingcombolo(결과);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static void Vala(DatagramSocket 종단) { 종단.close(); }
}
