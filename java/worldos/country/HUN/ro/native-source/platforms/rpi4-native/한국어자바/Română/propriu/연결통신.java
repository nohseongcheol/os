// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static conexiune Deschide(String adresa, int număr_port) throws I_O_excepție {
        try { return conexiune.Deschide(adresa, număr_port);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static primi_muta 수신열기(int număr_port) throws I_O_excepție {
        try { return primi_muta.Deschide(număr_port);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static Socket Conectează(String adresa, int muta_VALUE) throws I_O_excepție {
        try { return new Socket(adresa, muta_VALUE);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static ServerSocket asculta_participant(int muta_VALUE) throws I_O_excepție {
        try { return new ServerSocket(muta_VALUE);
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static Socket primi(ServerSocket server_VALUE) throws I_O_excepție {
        try { return server_VALUE.accept();
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
}
