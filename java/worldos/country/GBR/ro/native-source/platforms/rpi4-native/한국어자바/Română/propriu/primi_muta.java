// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;

/** primi_VALUE(受信)·muta_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class primi_muta {
    private final java.net.ServerSocket Standard_muta;
    private primi_muta(int număr_port) throws I_O_excepție {
        try { Standard_muta = new java.net.ServerSocket(număr_port);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static primi_muta Deschide(int număr_port) throws I_O_excepție {
        try { return new primi_muta(număr_port);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public conexiune primi() throws I_O_excepție {
        try { return new conexiune(Standard_muta.accept());
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public int număr_port() { return Standard_muta.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_excepție {
        try { Standard_muta.setSoTimeout(밀리초);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public boolean 닫힘() { return Standard_muta.isClosed(); }
    public void Închide() throws I_O_excepție {
        try { Standard_muta.close();
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
}
