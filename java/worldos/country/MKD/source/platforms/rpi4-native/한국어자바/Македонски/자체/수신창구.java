// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;

/** 수신(受信)·порта_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int број_на_порта) throws В_И_исклучок {
        try { 표준창구 = new java.net.ServerSocket(број_на_порта);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static 수신창구 Отвори(int број_на_порта) throws В_И_исклучок {
        try { return new 수신창구(број_на_порта);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public врска 받기() throws В_И_исклучок {
        try { return new врска(표준창구.accept());
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public int број_на_порта() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws В_И_исклучок {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Затвори() throws В_И_исклучок {
        try { 표준창구.close();
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
}
