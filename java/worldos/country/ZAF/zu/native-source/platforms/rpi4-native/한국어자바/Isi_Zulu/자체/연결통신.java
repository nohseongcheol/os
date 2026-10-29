// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static uxhumano Vula(String ikheli, int 접속번호) throws 입출력예외 {
        try { return uxhumano.Vula(ikheli, 접속번호);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Vula(접속번호);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static Socket Xhumanisa(String ikheli, int intuba_inani) throws 입출력예외 {
        try { return new Socket(ikheli, intuba_inani);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static ServerSocket 듣기(int intuba_inani) throws 입출력예외 {
        try { return new ServerSocket(intuba_inani);
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
    public static Socket 받기(ServerSocket Iseva_inani) throws 입출력예외 {
        try { return Iseva_inani.accept();
        } catch (java.io.IOException Iphutha) { throw 예외변환.i_I_O(Iphutha); }
        catch (RuntimeException Iphutha) { throw 예외변환.yenza_umyalo(Iphutha); }
    }
}
