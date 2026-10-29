// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static врска Отвори(String адреса, int број_на_порта) throws В_И_исклучок {
        try { return врска.Отвори(адреса, број_на_порта);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static 수신창구 수신열기(int број_на_порта) throws В_И_исклучок {
        try { return 수신창구.Отвори(број_на_порта);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static Socket Врзи_се(String адреса, int порта_VALUE) throws В_И_исклучок {
        try { return new Socket(адреса, порта_VALUE);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static ServerSocket 듣기(int порта_VALUE) throws В_И_исклучок {
        try { return new ServerSocket(порта_VALUE);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static Socket 받기(ServerSocket сервер_VALUE) throws В_И_исклучок {
        try { return сервер_VALUE.accept();
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
}
