// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·mkondo_ingizo(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int namba_ya_kituo) throws I_T_vighairi {
        try { 표준종단 = 통신.unda(namba_ya_kituo);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static 전문통로 unda(int namba_ya_kituo) throws I_T_vighairi {
        try { return new 전문통로(namba_ya_kituo);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public void tuma(String anwani, int namba_ya_kituo, String data) throws I_T_vighairi {
        try { 통신.tuma(표준종단, anwani, namba_ya_kituo, data);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public String 받기() throws I_T_vighairi {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public void 대기시간(int 밀리초) throws I_T_vighairi {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public int namba_ya_kituo() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void funga() { 통신.funga(표준종단); }
}
