// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static jokkalóo sos(String dëkkuwaay, int 접속번호) throws 입출력예외 {
        try { return jokkalóo.sos(dëkkuwaay, 접속번호);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.sos(접속번호);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static Socket JOKKOO(String dëkkuwaay, int jël_xëyma) throws 입출력예외 {
        try { return new Socket(dëkkuwaay, jël_xëyma);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static ServerSocket 듣기(int jël_xëyma) throws 입출력예외 {
        try { return new ServerSocket(jël_xëyma);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static Socket 받기(ServerSocket dëggu_xëyma) throws 입출력예외 {
        try { return dëggu_xëyma.accept();
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
}
