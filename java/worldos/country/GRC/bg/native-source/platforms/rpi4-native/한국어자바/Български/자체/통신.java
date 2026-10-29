// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP дейтаграма. външен_стойност 주소는 цифра_стойност 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Отваряне(int порт_стойност) throws В_И_изключение {
        try { return new DatagramSocket(порт_стойност);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static void изпращам(DatagramSocket участник, int порт_стойност, String Съдържание_стойност) throws В_И_изключение {
        try {
        изпращам(участник, "127.0.0.1", порт_стойност, Съдържание_стойност);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static void изпращам(DatagramSocket участник, String адрес, int порт_стойност, String Съдържание_стойност) throws В_И_изключение {
        try {
        byte[] байт_стойност = 문자.кодирам(Съдържание_стойност);
        участник.send(new DatagramPacket(байт_стойност, байт_стойност.length, InetAddress.getByName(адрес), порт_стойност));
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static String получавам(DatagramSocket участник) throws В_И_изключение {
        try {
        byte[] байт_стойност = new byte[512]; DatagramPacket дейтаграма = new DatagramPacket(байт_стойност, байт_стойност.length); участник.receive(дейтаграма);
        byte[] РЕЗУЛТАТ = new byte[дейтаграма.getLength()]; System.arraycopy(байт_стойност, 0, РЕЗУЛТАТ, 0, РЕЗУЛТАТ.length); return 문자.дешифрирам_данни(РЕЗУЛТАТ);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static void време_на_изчакване(DatagramSocket участник, int 밀리초) throws В_И_изключение {
        try { участник.setSoTimeout(밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static void Затворен(DatagramSocket участник) { участник.close(); }
}
