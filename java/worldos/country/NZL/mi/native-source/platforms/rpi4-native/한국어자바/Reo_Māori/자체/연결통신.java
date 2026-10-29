// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static hononga_d584d28a Huaki(String ADDRESS, int 접속번호) throws 입출력예외 {
        try { return hononga_d584d28a.Huaki(ADDRESS, 접속번호);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.Huaki(접속번호);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static Socket TŪHONO(String ADDRESS, int kawe_uara) throws 입출력예외 {
        try { return new Socket(ADDRESS, kawe_uara);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static ServerSocket 듣기(int kawe_uara) throws 입출력예외 {
        try { return new ServerSocket(kawe_uara);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static Socket 받기(ServerSocket tūmau_uara) throws 입출력예외 {
        try { return tūmau_uara.accept();
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
}
