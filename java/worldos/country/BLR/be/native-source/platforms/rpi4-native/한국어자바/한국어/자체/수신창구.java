// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·порт_значэнне(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int нумар_порта) throws увод_вывад_выключэнне {
        try { 표준창구 = new java.net.ServerSocket(нумар_порта);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static 수신창구 Адкрыць(int нумар_порта) throws увод_вывад_выключэнне {
        try { return new 수신창구(нумар_порта);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public кантакт 받기() throws увод_вывад_выключэнне {
        try { return new кантакт(표준창구.accept());
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public int нумар_порта() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws увод_вывад_выключэнне {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Закрыць() throws увод_вывад_выключэнне {
        try { 표준창구.close();
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
}
