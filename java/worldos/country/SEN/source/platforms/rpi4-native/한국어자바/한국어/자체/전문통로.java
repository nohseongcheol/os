// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·Yoon_dugal_xabaar(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.sos(접속번호);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public static 전문통로 sos(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public void Yónnee(String dëkkuwaay, int 접속번호, String mbir) throws 입출력예외 {
        try { 통신.Yónnee(표준종단, dëkkuwaay, 접속번호, mbir);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException njumte) { throw 예외변환.D_G(njumte); }
        catch (RuntimeException njumte) { throw 예외변환.def_ndigel(njumte); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Tej() { 통신.Tej(표준종단); }
}
