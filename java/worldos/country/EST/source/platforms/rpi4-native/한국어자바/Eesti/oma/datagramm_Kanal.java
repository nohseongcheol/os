// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;

/** datagramm(電文)·Kanal_kirje(通路): 경계를 가진 UDP 자료를 주고받는 osaleja. */
public final class datagramm_Kanal {
    private final java.net.DatagramSocket 표준종단;
    private datagramm_Kanal(int pordinumber) throws I_O_erand {
        try { 표준종단 = 통신.Ava(pordinumber);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static datagramm_Kanal Ava(int pordinumber) throws I_O_erand {
        try { return new datagramm_Kanal(pordinumber);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public void saatma(String ADDRESS, int pordinumber, String andmed) throws I_O_erand {
        try { 통신.saatma(표준종단, ADDRESS, pordinumber, andmed);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public String saama() throws I_O_erand {
        try { return 통신.saama(표준종단);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_erand {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public int pordinumber() { return 표준종단.getLocalPort(); }
    public boolean infotehnoloogia_suletud() { return 표준종단.isClosed(); }
    public void Suletud() { 통신.Suletud(표준종단); }
}
