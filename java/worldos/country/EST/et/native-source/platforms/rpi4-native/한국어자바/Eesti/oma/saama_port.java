// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;

/** saama_VALUE(受信)·port_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class saama_port {
    private final java.net.ServerSocket 표준창구;
    private saama_port(int pordinumber) throws I_O_erand {
        try { 표준창구 = new java.net.ServerSocket(pordinumber);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static saama_port Ava(int pordinumber) throws I_O_erand {
        try { return new saama_port(pordinumber);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public ühendus saama() throws I_O_erand {
        try { return new ühendus(표준창구.accept());
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public int pordinumber() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_erand {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public boolean infotehnoloogia_suletud() { return 표준창구.isClosed(); }
    public void Suletud() throws I_O_erand {
        try { 표준창구.close();
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
}
