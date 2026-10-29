// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static σύνδεση Άνοιγμα(String διεύθυνση, int αριθμός_θύρας) throws είσοδος_έξοδος_εξαίρεση {
        try { return σύνδεση.Άνοιγμα(διεύθυνση, αριθμός_θύρας);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static λαμβάνω_θύρα 수신열기(int αριθμός_θύρας) throws είσοδος_έξοδος_εξαίρεση {
        try { return λαμβάνω_θύρα.Άνοιγμα(αριθμός_θύρας);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static Socket Σύνδεση(String διεύθυνση, int θύρα_τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try { return new Socket(διεύθυνση, θύρα_τιμή);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static ServerSocket ακρόαση_τελικό_σημείο(int θύρα_τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try { return new ServerSocket(θύρα_τιμή);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static Socket λαμβάνω(ServerSocket διακομιστής_τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try { return διακομιστής_τιμή.accept();
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
}
