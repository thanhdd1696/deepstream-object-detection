# Object Detection Pipeline with NVIDIA DeepStream

## Project Overview

This project demonstrates the setup of an object detection pipeline leveraging NVIDIA's DeepStream technology. The pipeline is fully optimized for real-time object detection, and it's tested to handle RTSP streams efficiently. The core components of the pipeline include model deployment, data integration, and message forwarding, creating a robust system for various applications.

## Key Features

- **DeepStream Technology**: Utilizes NVIDIA DeepStream for accelerated video analytics, providing real-time object detection and classification capabilities.
- **RTSP Stream Handling**: The pipeline is fully tested with RTSP streams, ensuring smooth and reliable performance in real-world scenarios.
- **Model Deployment**: Supports easy deployment of different object detection models, allowing flexibility in application.
- **PostgreSQL Integration**: The pipeline is integrated with PostgreSQL for storing detection results and other relevant data, enabling efficient data management and retrieval.
- **RabbitMQ Messaging**: Outputs from DeepStream are forwarded to RabbitMQ, allowing seamless integration with other systems and real-time processing.

## Pipeline Architecture

The architecture of the pipeline consists of several key components:

1. **RTSP Stream Ingestion**: The pipeline ingests video streams from RTSP sources, preparing the data for processing.
2. **Object Detection using DeepStream**: Leveraging NVIDIA's DeepStream SDK, the video streams are processed to detect and classify objects in real-time.
3. **Data Storage in PostgreSQL**: Detected objects and metadata are stored in a PostgreSQL database for further analysis and reporting.
4. **Message Forwarding with RabbitMQ**: The detection results are sent to RabbitMQ, enabling asynchronous processing and integration with other systems or services.

## Technology Stack

- **NVIDIA DeepStream**: For real-time video analytics and object detection.
- **PostgreSQL**: For robust and scalable database management.
- **RabbitMQ**: For message brokering and forwarding.
- **RTSP**: For streaming video from various sources.

## Testing and Validation

The pipeline has been rigorously tested with multiple RTSP streams to ensure stability and performance. Various object detection models have been deployed and validated, ensuring the system's accuracy and efficiency.
