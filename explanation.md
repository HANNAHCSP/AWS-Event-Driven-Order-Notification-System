# SQS Visibility Timeout and Dead Letter Queue (DLQ)

## Visibility Timeout

The **visibility timeout** is the period during which a message, once received by a Lambda function, becomes invisible to other consumers. In our system, it's set to **30 seconds**.

### Why It Matters

- **Prevents Duplicate Processing**  
  Ensures only one Lambda processes the message at a time.

- **Allows Processing Time**  
  Gives the function time to parse the message, update DynamoDB, and complete other tasks.

- **Supports Retry on Failure**  
  If the function fails or times out, the message becomes visible again for another attempt.

- **Conserves Resources**  
  Avoids multiple Lambdas working on the same message.

---

## Dead Letter Queue (DLQ)

A **Dead Letter Queue** captures messages that fail after multiple processing attempts. In our setup, messages are sent to the DLQ after **3 failed tries**.

### Why It Matters

- **Handles Bad Data Gracefully**  
  Keeps malformed or unprocessable messages from blocking the main queue.

- **Simplifies Debugging**  
  Problem messages can be examined and analyzed in the DLQ.

- **Enables Monitoring**  
  Alerts can be triggered when messages are sent to the DLQ (via CloudWatch).

- **Allows Message Recovery**  
  Messages can be reprocessed after the issue is fixed.

- **Improves System Stability**  
  Prevents endless retries and ensures smooth queue operation.

---

## Combined Benefits

Using **visibility timeout** with a **DLQ** creates a reliable and fault-tolerant system:

1. Messages get enough time to be processed.
2. Failures are retried up to 3 times.
3. Persistent issues are isolated in the DLQ.
4. The main queue stays clean and efficient.

This setup helps maintain **data integrity**, ensures **no lost orders**, and makes the system **easy to monitor and troubleshoot**.
