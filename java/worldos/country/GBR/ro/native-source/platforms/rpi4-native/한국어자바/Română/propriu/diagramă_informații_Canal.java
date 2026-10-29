// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;

/** diagramă_informații(電文)·Canal_intrare(通路): 경계를 가진 UDP 자료를 주고받는 participant. */
public final class diagramă_informații_Canal {
    private final java.net.DatagramSocket Standard_participant;
    private diagramă_informații_Canal(int număr_port) throws I_O_excepție {
        try { Standard_participant = 통신.Deschide(număr_port);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static diagramă_informații_Canal Deschide(int număr_port) throws I_O_excepție {
        try { return new diagramă_informații_Canal(număr_port);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public void trimite(String adresa, int număr_port, String date) throws I_O_excepție {
        try { 통신.trimite(Standard_participant, adresa, număr_port, date);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public String primi() throws I_O_excepție {
        try { return 통신.primi(Standard_participant);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_excepție {
        try { 통신.TIMEOUT(Standard_participant, 밀리초);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public int număr_port() { return Standard_participant.getLocalPort(); }
    public boolean 닫힘() { return Standard_participant.isClosed(); }
    public void Închide() { 통신.Închide(Standard_participant); }
}
