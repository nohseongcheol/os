// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** коммуникация(通信): IPv4 UDP датаграмма. внешний_ЗНАЧЕН 주소는 цифра_ЗНАЧЕН 주소를 사용한다. */
public final class коммуникация {
    private коммуникация() {}
    public static DatagramSocket Открыть(int порт_ЗНАЧЕН) throws входные_данные_выход_исключение {
        try { return new DatagramSocket(порт_ЗНАЧЕН);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static void написать(DatagramSocket участник, int порт_ЗНАЧЕН, String контент_ЗНАЧЕН) throws входные_данные_выход_исключение {
        try {
        написать(участник, "127.0.0.1", порт_ЗНАЧЕН, контент_ЗНАЧЕН);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static void написать(DatagramSocket участник, String АДРЕС, int порт_ЗНАЧЕН, String контент_ЗНАЧЕН) throws входные_данные_выход_исключение {
        try {
        byte[] байт_ЗНАЧЕН = 문자.кодировать(контент_ЗНАЧЕН);
        участник.send(new DatagramPacket(байт_ЗНАЧЕН, байт_ЗНАЧЕН.length, InetAddress.getByName(АДРЕС), порт_ЗНАЧЕН));
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static String получить(DatagramSocket участник) throws входные_данные_выход_исключение {
        try {
        byte[] байт_ЗНАЧЕН = new byte[512]; DatagramPacket датаграмма = new DatagramPacket(байт_ЗНАЧЕН, байт_ЗНАЧЕН.length); участник.receive(датаграмма);
        byte[] результат = new byte[датаграмма.getLength()]; System.arraycopy(байт_ЗНАЧЕН, 0, результат, 0, результат.length); return 문자.расшифровать_данные(результат);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static void ТАЙМАУТ(DatagramSocket участник, int 밀리초) throws входные_данные_выход_исключение {
        try { участник.setSoTimeout(밀리초);
        } catch (java.io.IOException ошибка) { throw ПРЕОБР_исключение.входные_данные_выход(ошибка); }
        catch (RuntimeException ошибка) { throw ПРЕОБР_исключение.실행(ошибка); }
    }
    public static void Закрыть(DatagramSocket участник) { участник.close(); }
}
