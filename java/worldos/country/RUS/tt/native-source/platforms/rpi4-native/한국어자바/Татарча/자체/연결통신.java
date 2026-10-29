// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static тоташу ачу(String адрес, int 접속번호) throws 입출력예외 {
        try { return тоташу.ачу(адрес, 접속번호);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.ачу(접속번호);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static Socket ялгау(String адрес, int порт_VALUE) throws 입출력예외 {
        try { return new Socket(адрес, порт_VALUE);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static ServerSocket 듣기(int порт_VALUE) throws 입출력예외 {
        try { return new ServerSocket(порт_VALUE);
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static Socket 받기(ServerSocket сервер_VALUE) throws 입출력예외 {
        try { return сервер_VALUE.accept();
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
}
