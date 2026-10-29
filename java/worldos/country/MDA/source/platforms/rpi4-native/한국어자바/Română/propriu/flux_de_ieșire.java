// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;

/** Rezultat(出力)과 flux_VALUE: 순서를 보존해 내보내는 바이트의 Canal_intrare. */
public final class flux_de_ieșire {
    private final java.io.OutputStream Standard_flux;
    flux_de_ieșire(java.io.OutputStream Standard_flux) { this.Standard_flux = Standard_flux; }
    public void Scriere(int VALUE) throws I_O_excepție {
        try { Standard_flux.write(VALUE);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public void Scriere(byte[] date) throws I_O_excepție {
        try { Standard_flux.write(date);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public void Scriere(byte[] date, int Pornește, int lungime_VALUE) throws I_O_excepție {
        try { Standard_flux.write(date, Pornește, lungime_VALUE);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public void 내보내기() throws I_O_excepție {
        try { Standard_flux.flush();
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public void Închide() throws I_O_excepție {
        try { Standard_flux.close();
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
}
