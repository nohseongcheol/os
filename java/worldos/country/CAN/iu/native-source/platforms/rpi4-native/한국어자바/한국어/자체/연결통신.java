// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static kasuqsimaniq matuirli(String turaarut, int 접속번호) throws 입출력예외 {
        try { return kasuqsimaniq.matuirli(turaarut, 접속번호);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.matuirli(접속번호);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static Socket kasurli(String turaarut, int kapputigaq_atuutilik) throws 입출력예외 {
        try { return new Socket(turaarut, kapputigaq_atuutilik);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static ServerSocket 듣기(int kapputigaq_atuutilik) throws 입출력예외 {
        try { return new ServerSocket(kapputigaq_atuutilik);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static Socket 받기(ServerSocket ikiaqqitittivik_atuutilik) throws 입출력예외 {
        try { return ikiaqqitittivik_atuutilik.accept();
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
}
