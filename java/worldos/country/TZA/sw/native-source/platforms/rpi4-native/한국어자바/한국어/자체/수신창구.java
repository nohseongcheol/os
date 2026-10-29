// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·kituo_thamani(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int namba_ya_kituo) throws I_T_vighairi {
        try { 표준창구 = new java.net.ServerSocket(namba_ya_kituo);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static 수신창구 unda(int namba_ya_kituo) throws I_T_vighairi {
        try { return new 수신창구(namba_ya_kituo);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public muunganisho 받기() throws I_T_vighairi {
        try { return new muunganisho(표준창구.accept());
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public int namba_ya_kituo() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws I_T_vighairi {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void funga() throws I_T_vighairi {
        try { 표준창구.close();
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
}
