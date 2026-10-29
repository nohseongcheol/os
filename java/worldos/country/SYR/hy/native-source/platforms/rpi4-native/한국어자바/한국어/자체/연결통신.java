// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static կապ_d584d28a Բաց(String հասցե, int 접속번호) throws 입출력예외 {
        try { return կապ_d584d28a.Բաց(հասցե, 접속번호);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Բաց(접속번호);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static Socket Միացնել(String հասցե, int միացք_արժեք) throws 입출력예외 {
        try { return new Socket(հասցե, միացք_արժեք);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static ServerSocket 듣기(int միացք_արժեք) throws 입출력예외 {
        try { return new ServerSocket(միացք_արժեք);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static Socket 받기(ServerSocket սպասարկիչ_արժեք) throws 입출력예외 {
        try { return սպասարկիչ_արժեք.accept();
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
}
