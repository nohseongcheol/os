// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·seanail_cur_a_steach(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.fosgail(접속번호);
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public static 전문통로 fosgail(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public void cuir(String ADDRESS, int 접속번호, String dàta) throws 입출력예외 {
        try { 통신.cuir(표준종단, ADDRESS, 접속번호, dàta);
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public void TIMEOUT(int 밀리초) throws 입출력예외 {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void dùin() { 통신.dùin(표준종단); }
}
