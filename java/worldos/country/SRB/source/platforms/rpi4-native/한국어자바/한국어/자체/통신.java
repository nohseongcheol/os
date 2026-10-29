// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. екстерни_вриједност 주소는 цифра_вриједност 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Отвори(int порт_вриједност) throws У_И_изузетак {
        try { return new DatagramSocket(порт_вриједност);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static void послати(DatagramSocket крајња_тачка, int порт_вриједност, String Садржај_вриједност) throws У_И_изузетак {
        try {
        послати(крајња_тачка, "127.0.0.1", порт_вриједност, Садржај_вриједност);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static void послати(DatagramSocket крајња_тачка, String адреса, int порт_вриједност, String Садржај_вриједност) throws У_И_изузетак {
        try {
        byte[] бајт_вриједност = 문자.부호화(Садржај_вриједност);
        крајња_тачка.send(new DatagramPacket(бајт_вриједност, бајт_вриједност.length, InetAddress.getByName(адреса), порт_вриједност));
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static String 받기(DatagramSocket крајња_тачка) throws У_И_изузетак {
        try {
        byte[] бајт_вриједност = new byte[512]; DatagramPacket 전문 = new DatagramPacket(бајт_вриједност, бајт_вриједност.length); крајња_тачка.receive(전문);
        byte[] ИСХОД = new byte[전문.getLength()]; System.arraycopy(бајт_вриједност, 0, ИСХОД, 0, ИСХОД.length); return 문자.дешифровати_подаци(ИСХОД);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static void 대기시간(DatagramSocket крајња_тачка, int 밀리초) throws У_И_изузетак {
        try { крајња_тачка.setSoTimeout(밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw конвертовати_изузетак.У_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw конвертовати_изузетак.Изврши_команда(ГРЕШКА); }
    }
    public static void Затворен(DatagramSocket крајња_тачка) { крајња_тачка.close(); }
}
