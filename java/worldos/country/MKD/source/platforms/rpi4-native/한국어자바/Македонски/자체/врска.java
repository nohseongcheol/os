// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;

/** Врзи_се(連結)·канал_внес(通路): 상대와 이어진 TCP бајт_VALUE 흐름의 종단. */
public final class врска {
    private final java.net.Socket 표준연결;
    врска(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static врска Отвори(String адреса, int број_на_порта) throws В_И_исклучок {
        try {
            return new врска(new java.net.Socket(адреса, број_на_порта));
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public 입력흐름 입력() throws В_И_исклучок {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public 출력흐름 출력() throws В_И_исклучок {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public void TIMEOUT(int 밀리초) throws В_И_исклучок {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public int број_на_порта() { return 표준연결.getPort(); }
    public int локален_број_на_порта() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Затвори() throws В_И_исклучок {
        try { 표준연결.close();
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
}
