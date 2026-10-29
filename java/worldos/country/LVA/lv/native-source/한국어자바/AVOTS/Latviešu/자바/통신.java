// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Kļūda 상태도 호출자가 판단할 numurs 있도록 atbilde 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI adrese, Duration laika_ierobežojums)
            throws IOException, InterruptedException {
        HttpClient Savienoties = HttpClient.newBuilder().connectTimeout(laika_ierobežojums).build();
        return Savienoties.send(HttpRequest.newBuilder(adrese).timeout(laika_ierobežojums).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket saziņa_dalībnieks(String adrese, int 포트, int 제한밀리초) throws IOException {
        Socket Savienoties = new Socket();
        try {
            Savienoties.connect(new InetSocketAddress(adrese, 포트), 제한밀리초);
            Savienoties.setSoTimeout(제한밀리초);
            return Savienoties;
        } catch (IOException Kļūda) { Savienoties.close(); throw Kļūda; }
    }
}
