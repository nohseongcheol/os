// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP дейтаграма. зовнішній_значення 주소는 цифра_значення 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Відкрити(int порт_значення) throws ввід_вивід_виняток {
        try { return new DatagramSocket(порт_значення);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static void надсилати(DatagramSocket учасник, int порт_значення, String Вміст_значення) throws ввід_вивід_виняток {
        try {
        надсилати(учасник, "127.0.0.1", порт_значення, Вміст_значення);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static void надсилати(DatagramSocket учасник, String Адреса, int порт_значення, String Вміст_значення) throws ввід_вивід_виняток {
        try {
        byte[] байт_значення = 문자.кодувати(Вміст_значення);
        учасник.send(new DatagramPacket(байт_значення, байт_значення.length, InetAddress.getByName(Адреса), порт_значення));
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static String отримувати(DatagramSocket учасник) throws ввід_вивід_виняток {
        try {
        byte[] байт_значення = new byte[512]; DatagramPacket дейтаграма = new DatagramPacket(байт_значення, байт_значення.length); учасник.receive(дейтаграма);
        byte[] результат = new byte[дейтаграма.getLength()]; System.arraycopy(байт_значення, 0, результат, 0, результат.length); return 문자.дешифрувати_дані(результат);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static void 대기시간(DatagramSocket учасник, int 밀리초) throws ввід_вивід_виняток {
        try { учасник.setSoTimeout(밀리초);
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static void Закрити(DatagramSocket учасник) { учасник.close(); }
}
