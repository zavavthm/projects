
import requests
import time

# API endpoint for the rate-limited word service
API_ENDPOINT = "http://127.0.0.1:5000/word"

N_WORDS = 10
M_SECONDS = 0.01

def get_random_word():
    # Make GET request to the API endpoint
    try:
        response = requests.get(API_ENDPOINT).json()
    except Exception as e:
        print(f"Error making request: {e}")
        raise e
        
    # Extract the word from the response payload
    try:
        word = response["payload"]
    except Exception as e:
        print(f"Error extracting word from response: {e}")
        raise e
    return word

def get_n_words_every_m_secs(n, m):
    
    for i in range(n):
        try:
            word = get_random_word()
            print(f"Request {i+1}: {word}")
        except Exception as e:
            print(f"Request {i+1} failed: {e}")

        time.sleep(m)

def main():
    get_n_words_every_m_secs(N_WORDS, M_SECONDS)

if __name__ == "__main__":
    main()