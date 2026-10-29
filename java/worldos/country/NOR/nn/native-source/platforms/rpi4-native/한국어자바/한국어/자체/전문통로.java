// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·kanal_oppføring(通路): 경계를 가진 UDP 자료를 주고받는 endepunkt. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int portnummer) throws I_U_unntak {
        try { 표준종단 = 통신.Opna(portnummer);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static 전문통로 Opna(int portnummer) throws I_U_unntak {
        try { return new 전문통로(portnummer);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public void sende(String ADDRESS, int portnummer, String data) throws I_U_unntak {
        try { 통신.sende(표준종단, ADDRESS, portnummer, data);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public String 받기() throws I_U_unntak {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public void TIMEOUT(int 밀리초) throws I_U_unntak {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public int portnummer() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Lukk() { 통신.Lukk(표준종단); }
}
