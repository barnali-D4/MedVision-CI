
import time
import urllib.request
import urllib.error

url = "http://127.0.0.1:5001/health"

for attempt in range(12):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            body = response.read().decode()
            print(f"HTTP Status: {response.status}")
            print(f"Response: {body}")

            if response.status == 200:
                print("Container health check passed!")
                break

            raise SystemExit("Health check failed.")

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"Attempt {attempt + 1}/12: {error}")
        time.sleep(5)
else:
    raise SystemExit("Container health check failed after retries.")
