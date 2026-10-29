// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Java;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class communication {
    private communication() {}
    /** Returns the full response so the caller can also inspect HTTP error status codes. */
    public static HttpResponse<String> takeValue(URI address, Duration timeLimit)
            throws IOException, InterruptedException {
        HttpClient connect = HttpClient.newBuilder().connectTimeout(timeLimit).build();
        return connect.send(HttpRequest.newBuilder(address).timeout(timeLimit).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket connectEndpoint(String address, int hardwarePort, int limitMilliseconds) throws IOException {
        Socket connect = new Socket();
        try {
            connect.connect(new InetSocketAddress(address, hardwarePort), limitMilliseconds);
            connect.setSoTimeout(limitMilliseconds);
            return connect;
        } catch (IOException error) { connect.close(); throw error; }
    }
}
