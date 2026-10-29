// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class kommunikation {
    private kommunikation() {}
    /** HTTP fel 상태도 호출자가 판단할 nummer 있도록 svara 전체를 반환한다. */
    public static HttpResponse<String> TA_värde(URI Adress, Duration tidsgräns)
            throws IOException, InterruptedException {
        HttpClient Anslut = HttpClient.newBuilder().connectTimeout(tidsgräns).build();
        return Anslut.send(HttpRequest.newBuilder(Adress).timeout(tidsgräns).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket Connect_Endpoint(String Adress, int maskinvara_port, int 제한밀리초) throws IOException {
        Socket Anslut = new Socket();
        try {
            Anslut.connect(new InetSocketAddress(Adress, maskinvara_port), 제한밀리초);
            Anslut.setSoTimeout(제한밀리초);
            return Anslut;
        } catch (IOException fel) { Anslut.close(); throw fel; }
    }
}
