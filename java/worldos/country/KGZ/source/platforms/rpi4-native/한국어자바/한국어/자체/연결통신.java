// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static туташуу Ачуу(String дарек, int 접속번호) throws 입출력예외 {
        try { return туташуу.Ачуу(дарек, 접속번호);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Ачуу(접속번호);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static Socket Туташуу(String дарек, int порт_маани) throws 입출력예외 {
        try { return new Socket(дарек, порт_маани);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static ServerSocket 듣기(int порт_маани) throws 입출력예외 {
        try { return new ServerSocket(порт_маани);
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static Socket 받기(ServerSocket сервер_маани) throws 입출력예외 {
        try { return сервер_маани.accept();
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
}
