// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;

/** 입력(入力)과 flux_VALUE: 순서대로 들어오는 바이트를 읽는 Canal_intrare. */
public final class flux_de_intrare {
    private final java.io.InputStream Standard_flux;
    flux_de_intrare(java.io.InputStream Standard_flux) { this.Standard_flux = Standard_flux; }
    public int Citire() throws I_O_excepție {
        try { return Standard_flux.read();
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public int Citire(byte[] date) throws I_O_excepție {
        try { return Standard_flux.read(date);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public int Citire(byte[] date, int Pornește, int lungime_VALUE) throws I_O_excepție {
        try { return Standard_flux.read(date, Pornește, lungime_VALUE);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public void Închide() throws I_O_excepție {
        try { Standard_flux.close();
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
}
