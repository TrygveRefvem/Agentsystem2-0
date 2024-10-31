export class WebSocketClient {
    constructor(url, handlers = {}) {
        this.url = url;
        this.handlers = handlers;
        this.connect();
    }

    connect() {
        console.log('Connecting to WebSocket...');
        this.ws = new WebSocket(this.url);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Received message:', data.type);
            if (this.handlers[data.type]) {
                this.handlers[data.type](data);
            }
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket closed, reconnecting...');
            setTimeout(() => this.connect(), 1000);
        };
    }

    send(data) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.error('WebSocket is not open');
        }
    }
}
