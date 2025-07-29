import io from "socket.io-client";

export class SioService {
    private readonly socket: SocketIOClient.Socket;
    // private readonly listeners: { [key: string]: ((string) => void)[] };

    constructor() {
        const socket = io(
            "http://localhost:8112", // Server URL
            {
                autoConnect: false, // Don't connect automatically
                reconnectionAttempts: 5, // Try to reconnect 5 times
                reconnectionDelay: 1000, // Start with 1s delay between reconnections
                timeout: 10000, // Connection timeout (10s)
            }
        );
        this.socket = socket;
        socket.connect();
    }

    public Send(channel: string, data: any) {
        this.socket.emit(channel, data)
    }

    public RegisterCallback(channel: string, handler: (data: string) => void) {
        this.socket.on(channel, handler);
    }

    public RemoveCallback(channel: string, handler: (data: string) => void) {
        this.socket.off(channel, handler);
    }
}
