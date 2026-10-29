// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static Kgolagano bula(String aterese, int 접속번호) throws 입출력예외 {
        try { return Kgolagano.bula(aterese, 접속번호);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.bula(접속번호);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static Socket Golaganya(String aterese, int gorogisetsa_Boleng) throws 입출력예외 {
        try { return new Socket(aterese, gorogisetsa_Boleng);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static ServerSocket 듣기(int gorogisetsa_Boleng) throws 입출력예외 {
        try { return new ServerSocket(gorogisetsa_Boleng);
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
    public static Socket 받기(ServerSocket sefara_Boleng) throws 입출력예외 {
        try { return sefara_Boleng.accept();
        } catch (java.io.IOException phoso) { throw 예외변환.I_O(phoso); }
        catch (RuntimeException phoso) { throw 예외변환.diragatsa_Taelo(phoso); }
    }
}
