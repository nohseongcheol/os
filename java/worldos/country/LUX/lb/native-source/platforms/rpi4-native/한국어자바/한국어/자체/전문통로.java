// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·Kanal_Agab(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.ariichten(접속번호);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static 전문통로 ariichten(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public void mailen(String Adress, int 접속번호, String Daten) throws 입출력예외 {
        try { 통신.mailen(표준종단, Adress, 접속번호, Daten);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public void TIMEOUT(int 밀리초) throws 입출력예외 {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Clôture() { 통신.Clôture(표준종단); }
}
