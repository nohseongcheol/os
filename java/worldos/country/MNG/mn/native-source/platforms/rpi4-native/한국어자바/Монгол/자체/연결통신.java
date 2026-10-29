// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static холболт Нээх(String хаяг, int 접속번호) throws 입출력예외 {
        try { return холболт.Нээх(хаяг, 접속번호);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Нээх(접속번호);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static Socket Холбох(String хаяг, int порт_утга) throws 입출력예외 {
        try { return new Socket(хаяг, порт_утга);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static ServerSocket 듣기(int порт_утга) throws 입출력예외 {
        try { return new ServerSocket(порт_утга);
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static Socket 받기(ServerSocket сервер_утга) throws 입출력예외 {
        try { return сервер_утга.accept();
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
}
