# API Integration Notes

## Client/Server Timeouts
- **Client Timeouts:** Clients should always specify connection and read timeouts (e.g., `requests.get(url, timeout=(3.05, 10))`). This prevents the client thread from hanging indefinitely if the server becomes unresponsive.
- **Server Timeouts:** The server should also implement timeouts (e.g., using a reverse proxy like Nginx or Gateway) to close stalled connections and free up resources.

## Retries
- Only idempotent requests (like `GET`, `PUT`, or properly implemented `POST` with an idempotency key) should be retried automatically.
- Retries should employ an **Exponential Backoff** strategy with **Jitter** to avoid the "thundering herd" problem when a service recovers.

## Idempotency
- In payment systems, an idempotency key (often passed as an HTTP header like `Idempotency-Key: UUID`) ensures that if a client retries a `POST /payments` request due to a network timeout, the server recognizes it has already processed the request and returns the cached response rather than charging the customer twice.

## HTTP 4xx vs 5xx Errors
- **4xx Errors (Client Error):** The client sent an invalid request (e.g., `400 Bad Request` for missing fields, `401 Unauthorized`, `404 Not Found`). **Do not retry** 4xx errors without modifying the request payload.
- **5xx Errors (Server Error):** The server failed to process a valid request (e.g., `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`). These are generally safe to **retry** using exponential backoff, assuming the operation is idempotent.
