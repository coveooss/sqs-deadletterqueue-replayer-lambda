# sqs-deadletterqueue-replayer-lambda
Simple lambda to replay a sqs dead letter queue's messages into its original queue.

## Usage
Create a new lambda with sqs-deadletterqueue-replayer-lambda.py.

Your lambda's timeout must be at least 30 seconds to work properly.

The lambda must be called with an event like this one :
```json
{
  "target_queue_name": "test-queue",
  "source_queue_name": "test-queue-deadletter"
}
```
The lambda will attempt to send as many documents as possible from test-queue-deadletter to test-queue. Succesfully sent messages will be deleted from the source queue. 
