// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·port_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int portnummer) throws I_U_unntak {
        try { 표준창구 = new java.net.ServerSocket(portnummer);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static 수신창구 Opna(int portnummer) throws I_U_unntak {
        try { return new 수신창구(portnummer);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public kontakt 받기() throws I_U_unntak {
        try { return new kontakt(표준창구.accept());
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public int portnummer() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_U_unntak {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Lukk() throws I_U_unntak {
        try { 표준창구.close();
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
}
