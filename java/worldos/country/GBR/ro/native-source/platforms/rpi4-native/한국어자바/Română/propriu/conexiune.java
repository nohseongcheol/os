// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;

/** Conectează(連結)·Canal_intrare(通路): 상대와 이어진 TCP byte_VALUE 흐름의 participant. */
public final class conexiune {
    private final java.net.Socket Standard_bibliotecă_punte;
    conexiune(java.net.Socket Standard_bibliotecă_punte) { this.Standard_bibliotecă_punte = Standard_bibliotecă_punte; }
    public static conexiune Deschide(String adresa, int număr_port) throws I_O_excepție {
        try {
            return new conexiune(new java.net.Socket(adresa, număr_port));
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public flux_de_intrare 입력() throws I_O_excepție {
        try { return new flux_de_intrare(Standard_bibliotecă_punte.getInputStream());
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public flux_de_ieșire Rezultat() throws I_O_excepție {
        try { return new flux_de_ieșire(Standard_bibliotecă_punte.getOutputStream());
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_excepție {
        try { Standard_bibliotecă_punte.setSoTimeout(밀리초);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public int număr_port() { return Standard_bibliotecă_punte.getPort(); }
    public int local_număr_port() { return Standard_bibliotecă_punte.getLocalPort(); }
    public boolean 닫힘() { return Standard_bibliotecă_punte.isClosed(); }
    public boolean 연결됨() { return Standard_bibliotecă_punte.isConnected(); }
    public void Închide() throws I_O_excepție {
        try { Standard_bibliotecă_punte.close();
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
}
