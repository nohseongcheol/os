// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
import java.net.*;
public final class kontakt_přenos {
    private kontakt_přenos() {}
    public static kontakt Otevřít(String Adresa, int číslo_portu) throws vstup_a_výstup_výjimka {
        try { return kontakt.Otevřít(Adresa, číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static dostat_port 수신열기(int číslo_portu) throws vstup_a_výstup_výjimka {
        try { return dostat_port.Otevřít(číslo_portu);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static Socket Připojit(String Adresa, int port_HODNOTA) throws vstup_a_výstup_výjimka {
        try { return new Socket(Adresa, port_HODNOTA);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static ServerSocket naslouchat_účastník(int port_HODNOTA) throws vstup_a_výstup_výjimka {
        try { return new ServerSocket(port_HODNOTA);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static Socket dostat(ServerSocket server_HODNOTA) throws vstup_a_výstup_výjimka {
        try { return server_HODNOTA.accept();
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
}
