// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
import java.net.*;
public final class verbinding_transport {
    private verbinding_transport() {}
    public static verbinding Openen(String ADRES, int poortnummer) throws I_O_uitzondering {
        try { return verbinding.Openen(ADRES, poortnummer);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static ontvangen_poort 수신열기(int poortnummer) throws I_O_uitzondering {
        try { return ontvangen_poort.Openen(poortnummer);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static Socket Verbinden(String ADRES, int poort_WAARDE) throws I_O_uitzondering {
        try { return new Socket(ADRES, poort_WAARDE);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static ServerSocket 듣기(int poort_WAARDE) throws I_O_uitzondering {
        try { return new ServerSocket(poort_WAARDE);
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static Socket ontvangen(ServerSocket server_WAARDE) throws I_O_uitzondering {
        try { return server_WAARDE.accept();
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
}
