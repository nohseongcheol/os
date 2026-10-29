// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP αυτοδύναμο_πακέτο. εξωτερικός_τιμή 주소는 ψηφίο_τιμή 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Άνοιγμα(int θύρα_τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try { return new DatagramSocket(θύρα_τιμή);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static void στέλνω(DatagramSocket τελικό_σημείο, int θύρα_τιμή, String Περιεχόμενο_τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try {
        στέλνω(τελικό_σημείο, "127.0.0.1", θύρα_τιμή, Περιεχόμενο_τιμή);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static void στέλνω(DatagramSocket τελικό_σημείο, String διεύθυνση, int θύρα_τιμή, String Περιεχόμενο_τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try {
        byte[] 바이트 = 문자.κωδικοποιώ(Περιεχόμενο_τιμή);
        τελικό_σημείο.send(new DatagramPacket(바이트, 바이트.length, InetAddress.getByName(διεύθυνση), θύρα_τιμή));
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static String λαμβάνω(DatagramSocket τελικό_σημείο) throws είσοδος_έξοδος_εξαίρεση {
        try {
        byte[] 바이트 = new byte[512]; DatagramPacket αυτοδύναμο_πακέτο = new DatagramPacket(바이트, 바이트.length); τελικό_σημείο.receive(αυτοδύναμο_πακέτο);
        byte[] μέτρηση = new byte[αυτοδύναμο_πακέτο.getLength()]; System.arraycopy(바이트, 0, μέτρηση, 0, μέτρηση.length); return 문자.αποκρυπτογραφώ_δεδομένα(μέτρηση);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static void ΤΕΛΟΣ_ΧΡΟΝΟΥ(DatagramSocket τελικό_σημείο, int 밀리초) throws είσοδος_έξοδος_εξαίρεση {
        try { τελικό_σημείο.setSoTimeout(밀리초);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static void Κλείσιμο(DatagramSocket τελικό_σημείο) { τελικό_σημείο.close(); }
}
