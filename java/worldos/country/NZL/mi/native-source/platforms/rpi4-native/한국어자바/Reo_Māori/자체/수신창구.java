// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;

/** 수신(受信)·kawe_uara(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int 접속번호) throws 입출력예외 {
        try { 표준창구 = new java.net.ServerSocket(접속번호);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public static 수신창구 Huaki(int 접속번호) throws 입출력예외 {
        try { return new 수신창구(접속번호);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public hononga_d584d28a 받기() throws 입출력예외 {
        try { return new hononga_d584d28a(표준창구.accept());
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public int 접속번호() { return 표준창구.getLocalPort(); }
    public void KUA_PAU_TE_WĀ(int 밀리초) throws 입출력예외 {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Kati() throws 입출력예외 {
        try { 표준창구.close();
        } catch (java.io.IOException Pōhēhē) { throw 예외변환.I_O(Pōhēhē); }
        catch (RuntimeException Pōhēhē) { throw 예외변환.kawe_tono(Pōhēhē); }
    }
}
