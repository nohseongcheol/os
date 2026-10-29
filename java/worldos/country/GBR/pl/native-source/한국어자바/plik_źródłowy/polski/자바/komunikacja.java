// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class komunikacja {
    private komunikacja() {}
    /** HTTP błąd 상태도 호출자가 판단할 identyfikator 있도록 odpowiedź 전체를 반환한다. */
    public static HttpResponse<String> WYCINEK_WARTOŚĆ(URI Adres, Duration limit_czasu)
            throws IOException, InterruptedException {
        HttpClient Połącz = HttpClient.newBuilder().connectTimeout(limit_czasu).build();
        return Połącz.send(HttpRequest.newBuilder(Adres).timeout(limit_czasu).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket punkt_końcowy_połączenia(String Adres, int sprzęt_port, int 제한밀리초) throws IOException {
        Socket Połącz = new Socket();
        try {
            Połącz.connect(new InetSocketAddress(Adres, sprzęt_port), 제한밀리초);
            Połącz.setSoTimeout(제한밀리초);
            return Połącz;
        } catch (IOException błąd) { Połącz.close(); throw błąd; }
    }
}
