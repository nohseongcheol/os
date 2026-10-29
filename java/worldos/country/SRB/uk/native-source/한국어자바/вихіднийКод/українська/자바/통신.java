// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ПОМИЛКА 상태도 호출자가 판단할 수 있도록 відповідь 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI Адреса, Duration обмеження_часу)
            throws IOException, InterruptedException {
        HttpClient З_єднання = HttpClient.newBuilder().connectTimeout(обмеження_часу).build();
        return З_єднання.send(HttpRequest.newBuilder(Адреса).timeout(обмеження_часу).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket зв_язок_учасник(String Адреса, int обладнання_порт, int 제한밀리초) throws IOException {
        Socket З_єднання = new Socket();
        try {
            З_єднання.connect(new InetSocketAddress(Адреса, обладнання_порт), 제한밀리초);
            З_єднання.setSoTimeout(제한밀리초);
            return З_єднання;
        } catch (IOException ПОМИЛКА) { З_єднання.close(); throw ПОМИЛКА; }
    }
}
