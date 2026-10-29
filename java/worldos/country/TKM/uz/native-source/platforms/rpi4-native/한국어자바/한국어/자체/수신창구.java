// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·port_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int 접속번호) throws I_O_istisno {
        try { 표준창구 = new java.net.ServerSocket(접속번호);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static 수신창구 Ochish(int 접속번호) throws I_O_istisno {
        try { return new 수신창구(접속번호);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public aloqa 받기() throws I_O_istisno {
        try { return new aloqa(표준창구.accept());
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public int 접속번호() { return 표준창구.getLocalPort(); }
    public void TANAFFUS(int 밀리초) throws I_O_istisno {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Yopish() throws I_O_istisno {
        try { 표준창구.close();
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
}
