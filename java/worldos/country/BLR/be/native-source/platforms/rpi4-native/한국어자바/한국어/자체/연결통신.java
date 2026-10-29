// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static кантакт Адкрыць(String адрас, int нумар_порта) throws увод_вывад_выключэнне {
        try { return кантакт.Адкрыць(адрас, нумар_порта);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static 수신창구 수신열기(int нумар_порта) throws увод_вывад_выключэнне {
        try { return 수신창구.Адкрыць(нумар_порта);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static Socket Злучыцца(String адрас, int порт_значэнне) throws увод_вывад_выключэнне {
        try { return new Socket(адрас, порт_значэнне);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static ServerSocket 듣기(int порт_значэнне) throws увод_вывад_выключэнне {
        try { return new ServerSocket(порт_значэнне);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static Socket 받기(ServerSocket сервер_значэнне) throws увод_вывад_выключэнне {
        try { return сервер_значэнне.accept();
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
}
