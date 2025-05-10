
# AWS Event-Driven Order Notification System

This project implements an event-driven architecture for an e-commerce platform's order processing system using AWS services:
- Amazon SNS for notifications
- Amazon SQS for queueing
- AWS Lambda for processing
- Amazon DynamoDB for data storage

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  SNS Topic  │────►│  SQS Queue  │────►│   Lambda    │────►│  DynamoDB   │
│ OrderTopic  │     │ OrderQueue  │     │ Function    │     │   Table     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │  Dead Letter│
                    │    Queue    │
                    └─────────────┘
```

## Setup Instructions

### 1. DynamoDB Table

Create a DynamoDB table with the following settings:
- Table Name: `Orders`
- Partition Key: `orderId` (String)
- Attributes: userId, itemName, quantity, status, timestamp

### 2. SNS Topic

Create an SNS Topic:
- Topic Name: `OrderTopic`
- Type: Standard

### 3. SQS Queues

Create two SQS queues:
- Main Queue: `OrderQueue`
- Dead Letter Queue: `OrderDLQ`

Configure the main queue:
- Type: Standard
- Dead-letter queue: Enabled, pointing to `OrderDLQ`
- Maximum receives: 3

### 4. SNS Subscription

Subscribe the SQS queue to the SNS topic:
- Select the SNS topic
- Create subscription
- Protocol: Amazon SQS
- Endpoint: ARN of the `OrderQueue`

### 5. Lambda Function

Create a Lambda function:
- Name: `OrderProcessor`
- Runtime: Python 3.11 or Node.js 18.x
- Trigger: SQS queue (`OrderQueue`)
- Permissions: Access to DynamoDB, SQS, and SNS

Deploy the Lambda function code provided in this repository.

## Testing

To test the system:

1. Publish a message to the SNS topic:
```json
{
  "orderId": "O1234",
  "userId": "U123",
  "itemName": "Laptop",
  "quantity": 1,
  "status": "new",
  "timestamp": "2025-05-03T12:00:00Z"
}
```

2. Check the Lambda CloudWatch logs to see if the message was processed
3. Verify in DynamoDB that the order was stored correctly

## Explanation of Visibility Timeout and DLQ

### Visibility Timeout

The visibility timeout in SQS defines how long a message remains invisible to other consumers after being retrieved. This is important for our order processing system because:

1. It prevents multiple Lambda instances from processing the same order
2. It gives our Lambda function enough time to process the message
3. If processing fails, the message becomes visible again after the timeout expires

For our system, a visibility timeout of 30 seconds provides sufficient time for the Lambda function to process the order and write it to DynamoDB.

### Dead Letter Queue (DLQ)

The Dead Letter Queue serves as a safety mechanism for handling problematic messages:

1. If our Lambda function fails to process a message after multiple attempts (maxReceiveCount=3), the message is moved to the DLQ
2. This prevents "poison messages" from blocking the main queue indefinitely
3. It allows us to investigate problematic messages without disrupting the main flow
4. We can set up separate monitoring on the DLQ to alert us about processing failures

The DLQ implementation in our system allows for:
- Identification of processing issues
- Manual intervention for problematic orders
- Analysis of failure patterns
- Potential reprocessing of fixed messages

By using both visibility timeout and DLQ properly, our system achieves better reliability and provides mechanisms for handling failures gracefully.

