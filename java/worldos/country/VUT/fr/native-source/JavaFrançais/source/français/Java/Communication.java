// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.Java;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class Communication {
    private Communication() {}
    /** Renvoie la réponse entière pour permettre aussi à l’appelant d’évaluer les états d’erreur HTTP. */
    public static HttpResponse<String> valeurPrendre(URI adresse, Duration limiteTemps)
            throws IOException, InterruptedException {
        HttpClient connecter = HttpClient.newBuilder().connectTimeout(limiteTemps).build();
        return connecter.send(HttpRequest.newBuilder(adresse).timeout(limiteTemps).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket connecterExtrémité(String adresse, int portMatériel, int millisecondesLimite) throws IOException {
        Socket connecter = new Socket();
        try {
            connecter.connect(new InetSocketAddress(adresse, portMatériel), millisecondesLimite);
            connecter.setSoTimeout(millisecondesLimite);
            return connecter;
        } catch (IOException erreur) { connecter.close(); throw erreur; }
    }
}
