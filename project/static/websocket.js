// Title: Websocket Connection to Message Broker Implementation.
// Brief: This file defines how users connect to the message broker.
// Author: Joseph.
// ----------------------------------------------------------------------------
/* The Message Broker Connection implementation. MessageBrokerConnection 
   extends the built-in JavaScript Websocket class.
 */
class MessageBrokerConnection extends WebSocket {
    constructor(url, protocols) {
        super(url, protocols);
        super.onmessage = this.notify.bind(this);
    }
  
    // Override the send method with the publish method to enhance the
    // system-wide naming convention.
    publish(event) {
        super.send(event);
    }

    // The notify method is called when the websocket receives a message.
    notify(event) {
        //
        // Handle incomming messages here.
        //

        // For now, just output the message to the console.
        console.log(event);
    }
}


// ----------------------------------------------------------------------------
/* Where the Message Broker's route is defined. For more info, see:
   project/modules/UserMessageBroker/routing.py
 */
const MESSAGE_BROKER_URL = 'ws://localhost:8000/ws/messagebroker/';

/* This is an asynchronous way of connecting to the Message Broker through use
   of promises.
 */
function connectToMessageBroker() {
    const promise = new Promise((resolve, reject) => {
        const connection = new MessageBrokerConnection(MESSAGE_BROKER_URL);
        connection.onopen = () => {
            resolve(connection);
        }
        connection.onerror = (error) => {
            console.error("Could not open web socket: ", error);
            reject(error);
        }
    }); 
    return promise;
}
// ----------------------------------------------------------------------------
