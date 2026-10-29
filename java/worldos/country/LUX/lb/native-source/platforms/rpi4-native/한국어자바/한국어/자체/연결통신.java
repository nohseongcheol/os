// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static Verbindung ariichten(String Adress, int 접속번호) throws 입출력예외 {
        try { return Verbindung.ariichten(Adress, 접속번호);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.ariichten(접속번호);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static Socket Verbannen(String Adress, int Port_VALUE) throws 입출력예외 {
        try { return new Socket(Adress, Port_VALUE);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static ServerSocket 듣기(int Port_VALUE) throws 입출력예외 {
        try { return new ServerSocket(Port_VALUE);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static Socket 받기(ServerSocket Server_VALUE) throws 입출력예외 {
        try { return Server_VALUE.accept();
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
}
