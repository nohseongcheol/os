// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Злучыцца(連結)·канал_увядзенне(通路): 상대와 이어진 TCP байт_значэнне 흐름의 종단. */
public final class кантакт {
    private final java.net.Socket 표준연결;
    кантакт(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static кантакт Адкрыць(String адрас, int нумар_порта) throws увод_вывад_выключэнне {
        try {
            return new кантакт(new java.net.Socket(адрас, нумар_порта));
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public 입력흐름 입력() throws увод_вывад_выключэнне {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public 출력흐름 Выхад() throws увод_вывад_выключэнне {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public void 대기시간(int 밀리초) throws увод_вывад_выключэнне {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public int нумар_порта() { return 표준연결.getPort(); }
    public int мясцовы_нумар_порта() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Закрыць() throws увод_вывад_выключэнне {
        try { 표준연결.close();
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
}
