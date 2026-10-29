// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static uqhagamshelo Vula(String idilesi, int 접속번호) throws 입출력예외 {
        try { return uqhagamshelo.Vula(idilesi, 접속번호);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Vula(접속번호);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static Socket Nxulumanisa(String idilesi, int iphothi_ixabiso) throws 입출력예외 {
        try { return new Socket(idilesi, iphothi_ixabiso);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static ServerSocket 듣기(int iphothi_ixabiso) throws 입출력예외 {
        try { return new ServerSocket(iphothi_ixabiso);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static Socket 받기(ServerSocket iseva_ixabiso) throws 입출력예외 {
        try { return iseva_ixabiso.accept();
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
}
