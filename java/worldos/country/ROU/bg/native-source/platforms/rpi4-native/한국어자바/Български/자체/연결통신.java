// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static връзка Отваряне(String адрес, int номер_на_порт) throws В_И_изключение {
        try { return връзка.Отваряне(адрес, номер_на_порт);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static получавам_порт 수신열기(int номер_на_порт) throws В_И_изключение {
        try { return получавам_порт.Отваряне(номер_на_порт);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static Socket Свързване(String адрес, int порт_стойност) throws В_И_изключение {
        try { return new Socket(адрес, порт_стойност);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static ServerSocket чакам_участник(int порт_стойност) throws В_И_изключение {
        try { return new ServerSocket(порт_стойност);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static Socket получавам(ServerSocket сървър_стойност) throws В_И_изключение {
        try { return сървър_стойност.accept();
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
}
