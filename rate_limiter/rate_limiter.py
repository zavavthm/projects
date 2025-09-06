
import time
from flask import Flask
from abc import ABC, abstractmethod

# Initialize Flask application
app = Flask(__name__)

class RateLimiter(ABC):
    """
    Abstract base class for rate limiting implementations.
    
    This class defines the common interface that all rate limiting strategies
    must implement. It provides the basic structure for tracking request limits
    within a specified time window.
    
    Attributes:
        max_requests (int): Maximum number of requests allowed in the time window
        window_size (int): Size of the time window in seconds
    """
    
    def __init__(self, max_requests, window_size):
        """
        Initialize the rate limiter with request limits and time window.
        
        Args:
            max_requests (int): Maximum number of requests allowed in the window
            window_size (int): Time window size in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size
    
    @abstractmethod
    def allow_request(self):
        """
        Check if a new request should be allowed based on current rate limiting rules.
        
        This method must be implemented by all concrete rate limiting classes.
        It should return True if the request is allowed, False otherwise.
        
        Returns:
            bool: True if request is allowed, False if rate limit is exceeded
        """
        pass

class FixedWindowRateLimiter(RateLimiter):
    """
    Fixed Window Rate Limiter Implementation
    
    This rate limiter uses a fixed time window approach where requests are counted
    within non-overlapping time windows. Once the maximum number of requests is
    reached within a window, all subsequent requests are rejected until the next
    window begins.
    
    Key Characteristics:
    - Fixed time windows (e.g., every 60 seconds)
    - Request counter resets at the start of each new window
    - Simple and predictable behavior
    - May allow bursts of requests at window boundaries
    
    Approach:
    Creates fixed time windows aligned to the window_size boundary.
    For example, if window_size is 60 seconds, windows start at:
    00:00, 01:00, 02:00, etc.
    
    Attributes:
        window_start_time (int): Unix timestamp of current window start
        window_end_time (int): Unix timestamp of current window end
        requests_count (int): Number of requests made in current window
    """
    
    def __init__(self, max_requests, window_size):
        """
        Initialize the fixed window rate limiter.
        
        Args:
            max_requests (int): Maximum requests allowed per window
            window_size (int): Window duration in seconds
        """
        super().__init__(max_requests, window_size)
        
        # Initialize window boundaries aligned to window_size
        current_time = int(time.time())
        self.window_start_time = current_time - (current_time % self.window_size)
        self.window_end_time = self.window_start_time + self.window_size
        
        # Initialize request counter for current window
        self.requests_count = 0
    
    def allow_request(self):
        """
        Check if a new request should be allowed based on the fixed window rate limiting.
        
        This method implements the core logic of the fixed window rate limiter:
        1. Check if current time has exceeded the current window
        2. If yes, create a new window and reset the counter
        3. If no, check if we're within the request limit for current window
        
        Returns:
            bool: True if request is allowed, False if rate limit exceeded
        """
        curr_time = int(time.time())
        
        # Check if we need to start a new window
        if curr_time > self.window_start_time + self.window_size:
            # Current time has exceeded the window boundary
            # Create a new window aligned to the window_size boundary
            self.window_start_time = curr_time - (curr_time % self.window_size)
            self.window_end_time = self.window_start_time + self.window_size
            
            # Reset counter to 1 (not 0) because we're processing this request
            # as the first request in the new window
            self.requests_count = 1
            
            # Debug output for window transitions
            print("****** new window set ******")
            print(f"Window start: {self.window_start_time}")
            print(f"Window end: {self.window_end_time}")
            print(f"Request count: {self.requests_count}")
            
            return True
        else:
            # Current time is within the existing window
            # Check if we've reached the maximum request limit
            if self.requests_count >= self.max_requests:
                print(f"Rate limit exceeded: {self.requests_count}/{self.max_requests} requests used")
                return False
            else:
                # Increment request counter and allow the request
                self.requests_count += 1
                return True

