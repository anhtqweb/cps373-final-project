#include <asio.hpp>

using asio::ip::tcp;

void handle_request(tcp::acceptor& acceptor) {
    acceptor.async_accept([&](std::error_code ec, tcp::socket&& socket) {
        while (true) {
            
        }
    });
}

int main() {
    asio::io_context io_context;
    tcp::acceptor acceptor(io_context, tcp::endpoint(tcp::v4(), 3000));

    io_context.run();
    return 0;
}