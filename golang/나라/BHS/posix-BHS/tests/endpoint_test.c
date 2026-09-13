#include <network_conversion/byte_order.h>
#include <errno.h>
#include <system/socket.h>
#include <unistd.h>

static unsigned int length_of_text(const char *examined_data)
{
    unsigned int n = 0;
    while (examined_data[n] != 0) n++;
    return n;
}

static void write_message(const char *examined_data) { (void)write(standard_output_descriptor, examined_data, length_of_text(examined_data)); }

static void report_result(const char *system_identity, int test_pass)
{
    write_message(test_pass ? "NTEST:PASS:" : "NTEST:FAIL:");
    write_message(system_identity);
    write_message("\n");
}

int main(void)
{
    struct internetwork_endpoint_address server_endpoint_address = {0};
    struct internetwork_endpoint_address source = {0};
    address_length_type source_address_size = sizeof(source);
    char transfer_buffer_2[8] = {0};
    int server_endpoint = socket(internetwork_address_family_code, datagram_endpoint, user_datagram_protocol);
    int client_endpoint = socket(internetwork_address_family_code, datagram_endpoint, 0);

    report_result("socket-server", server_endpoint >= 3);
    report_result("socket-client", client_endpoint >= 3 && client_endpoint != server_endpoint);
    server_endpoint_address.internetwork_address_family = internetwork_address_family_code;
    server_endpoint_address.transport_port_number = htons(32345);
    server_endpoint_address.internetwork_address_field.address_value = htonl(loopback_address);
    report_result("bind", bind(server_endpoint, (const struct endpoint_address *)&server_endpoint_address,
                        sizeof(server_endpoint_address)) == 0);
    report_result("connect", connect(client_endpoint, (const struct endpoint_address *)&server_endpoint_address,
                              sizeof(server_endpoint_address)) == 0);
    report_result("send", send(client_endpoint, "ping", 4, 0) == 4);
    report_result("recvfrom", recvfrom(server_endpoint, transfer_buffer_2, sizeof(transfer_buffer_2), 0,
                                (struct endpoint_address *)&source, &source_address_size) == 4 &&
                       transfer_buffer_2[0] == 'p' && transfer_buffer_2[3] == 'g' && source_address_size == 16);
    errno = 0;
    report_result("empty-eagain", recv(server_endpoint, transfer_buffer_2, sizeof(transfer_buffer_2), 0) == -1 && errno == temporarily_unavailable);
    report_result("getsockname", getsockname(server_endpoint, (struct endpoint_address *)&source,
                                      &source_address_size) == 0 && source.transport_port_number == htons(32345));
    errno = 0;
    report_result("udp-listen-not-supported", listen(server_endpoint, 1) == -1 && errno == operation_not_supported);
    report_result("close-client", close(client_endpoint) == 0);
    report_result("close-server", close(server_endpoint) == 0);
    write_message("NTEST:DONE\n");
    return 0;
}
