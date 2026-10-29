// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
import java.net.*;
public final class ühendus_transport {
    private ühendus_transport() {}
    public static ühendus Ava(String ADDRESS, int pordinumber) throws I_O_erand {
        try { return ühendus.Ava(ADDRESS, pordinumber);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static saama_port 수신열기(int pordinumber) throws I_O_erand {
        try { return saama_port.Ava(pordinumber);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static Socket Ühendu(String ADDRESS, int port_VALUE) throws I_O_erand {
        try { return new Socket(ADDRESS, port_VALUE);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static ServerSocket jälgima_osaleja(int port_VALUE) throws I_O_erand {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static Socket saama(ServerSocket server_VALUE) throws I_O_erand {
        try { return server_VALUE.accept();
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
}
