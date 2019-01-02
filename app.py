from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, disconnect
import eventlet

eventlet.monkey_patch()
app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app, async_mode='eventlet'))

class CountdownTask(object):

    _running = False

    def __init__(self, socketio):
        """
        assign socketio object to emit
        """
        self.socketio = socketio
        self._running = True

    def run(self, n):
        """
        emit message
        """
        while self._running and n > 0:
            n -= 1
            self.socketio.emit("update", {"msg": str(n)}, namespace="/socket")
            eventlet.sleep(1)
        self.stop()

    def stop(self):
        """
        stop the loop
        """
        self._running = False


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/sockettest')
def connect()socket
    """
    connect
    """
    global worker
    worker = CountdownTask(socketio)

@socketio.on('start', namespace='/socket')
def start_work():
    """
    trigger background thread
    """
    emit("update", {"msg": "starting timer"})
    # notice that the method is not called - don't put braces after method name
    socketio.start_background_task(target=worker.run, n=10)
    #worker.run(10)
    #worker.stop()
    #disconnect()

@socketio.on('stop', namespace='/socket')
def stop_work():
    """
    trigger background thread
    """
    worker.stop()
    print('Timer has been stoppped')
    emit("update", {"msg": "Timer has been stoppped"})
    disconnect()

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    socketio.run(app, debug=True, host='localhost')