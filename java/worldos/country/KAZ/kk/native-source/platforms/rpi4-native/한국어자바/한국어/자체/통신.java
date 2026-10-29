// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. сыртқы_мән 주소는 сан_мән 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Ашу(int порт_мән) throws енгізу_шығару_ерекшелік {
        try { return new DatagramSocket(порт_мән);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static void жіберу(DatagramSocket қатысушы, int порт_мән, String мазмұн_мән) throws енгізу_шығару_ерекшелік {
        try {
        жіберу(қатысушы, "127.0.0.1", порт_мән, мазмұн_мән);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static void жіберу(DatagramSocket қатысушы, String мекенжай, int порт_мән, String мазмұн_мән) throws енгізу_шығару_ерекшелік {
        try {
        byte[] байт_мән = 문자.부호화(мазмұн_мән);
        қатысушы.send(new DatagramPacket(байт_мән, байт_мән.length, InetAddress.getByName(мекенжай), порт_мән));
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static String 받기(DatagramSocket қатысушы) throws енгізу_шығару_ерекшелік {
        try {
        byte[] байт_мән = new byte[512]; DatagramPacket 전문 = new DatagramPacket(байт_мән, байт_мән.length); қатысушы.receive(전문);
        byte[] НӘТИЖЕ = new byte[전문.getLength()]; System.arraycopy(байт_мән, 0, НӘТИЖЕ, 0, НӘТИЖЕ.length); return 문자.шифрді_шешу_деректер(НӘТИЖЕ);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static void ТАЙМ_АУТ(DatagramSocket қатысушы, int 밀리초) throws енгізу_шығару_ерекшелік {
        try { қатысушы.setSoTimeout(밀리초);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static void Жабу(DatagramSocket қатысушы) { қатысушы.close(); }
}
