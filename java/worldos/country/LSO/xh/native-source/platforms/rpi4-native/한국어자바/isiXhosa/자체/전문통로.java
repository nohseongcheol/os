// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;

/** 전문(電文)·ijelo_ufako_nkcukacha(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.Vula(접속번호);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public static 전문통로 Vula(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public void thumela(String idilesi, int 접속번호, String iingcombolo) throws 입출력예외 {
        try { 통신.thumela(표준종단, idilesi, 접속번호, iingcombolo);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException Impazamo) { throw 예외변환.i_I_O(Impazamo); }
        catch (RuntimeException Impazamo) { throw 예외변환.ukwenza_umyalelo(Impazamo); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Vala() { 통신.Vala(표준종단); }
}
