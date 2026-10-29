// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.Java;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class Kommunikation {
    private Kommunikation() {}
    /** Gibt die vollständige Antwort zurück, damit der Aufrufer auch HTTP-Fehlerstatus beurteilen kann. */
    public static HttpResponse<String> entnehmenWert(URI adresse, Duration zeitGrenzwert)
            throws IOException, InterruptedException {
        HttpClient verbinden = HttpClient.newBuilder().connectTimeout(zeitGrenzwert).build();
        return verbinden.send(HttpRequest.newBuilder(adresse).timeout(zeitGrenzwert).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket endpunktVerbinden(String adresse, int hardwarePort, int grenzwertMillisekunden) throws IOException {
        Socket verbinden = new Socket();
        try {
            verbinden.connect(new InetSocketAddress(adresse, hardwarePort), grenzwertMillisekunden);
            verbinden.setSoTimeout(grenzwertMillisekunden);
            return verbinden;
        } catch (IOException fehler) { verbinden.close(); throw fehler; }
    }
}
