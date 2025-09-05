from flask import Flask
from multithreading import thread

app = Flask(__name__)

class RateLimiter:
    # First need to implement rate limiter to limit the requests coming to the server
    def __init__(self, window_size, max_limit, algo):
        self.window_size = window_size
        self.max_limit = max_limit
        self.algo = algo

    def process_request(self, request_ts, window_start, window_end):
        # based on window size and the max limit, check if limit is breached or not.
        # if breached, return False, else return True
        pass
    
    def get_window(self):
        # if seconds == 0,10,20,30,40,50 , return window_start = ts, window_end = ts+10 seconds
        pass

@app.route("/request/")
def process_request(request):
    payload = request['data']
    window_start, window_end = fw_rl.get_window()
    if fw_rl.process_request(payload['ts'], window_start, window_end):
        return backend_service(request)
    

if __name__ == "__main__":
    app.run(debug=True)
    fw_rl = RateLimiter(10, 100, 'fw')