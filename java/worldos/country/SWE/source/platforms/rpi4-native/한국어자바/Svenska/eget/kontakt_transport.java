// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
import java.net.*;
public final class kontakt_transport {
    private kontakt_transport() {}
    public static kontakt Öppna(String Adress, int portnummer) throws indata_utleverans_fel {
        try { return kontakt.Öppna(Adress, portnummer);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static få_port 수신열기(int portnummer) throws indata_utleverans_fel {
        try { return få_port.Öppna(portnummer);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static Socket Anslut(String Adress, int port_värde) throws indata_utleverans_fel {
        try { return new Socket(Adress, port_värde);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static ServerSocket lyssna_deltagare(int port_värde) throws indata_utleverans_fel {
        try { return new ServerSocket(port_värde);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static Socket få(ServerSocket server_värde) throws indata_utleverans_fel {
        try { return server_värde.accept();
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
}
