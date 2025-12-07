---
id: ros2-core-concepts
title: " ROS 2 Core Concepts (Nodes, Topics, Services, Actions)"
sidebar_label: "ROS 2 Core Concepts"
---

## Learning Objectives

- Understand the fundamental building blocks of ROS 2.
- Differentiate between ROS 2 nodes, topics, services, and actions.
- Learn how these concepts facilitate inter-process communication in robotics.

## Core Concepts

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It provides a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms. Its core concepts are essential for understanding how ROS 2 applications are structured and how different components communicate.

### Nodes

A **Node** is an executable process that performs computations. In ROS 2, each node is designed to do a single, well-defined task, such as controlling a motor, reading sensor data, or performing a path planning algorithm. This modularity allows for robust and maintainable robot software.

### Topics

**Topics** are the most common way for nodes to exchange data. A topic is a named bus over which nodes send (publish) and receive (subscribe) messages. This publish-subscribe communication pattern is asynchronous, meaning publishers send messages without knowing if any subscribers are listening, and subscribers receive messages without knowing who published them.

-   **Publishers**: Nodes that send messages to a topic.
-   **Subscribers**: Nodes that receive messages from a topic.
-   **Messages**: Data structures that contain information, defined by `.msg` files.

### Services

**Services** are a synchronous request/reply communication mechanism. Unlike topics, services involve a client node making a request to a server node, and the server node performing an operation and sending back a response. This is useful for operations that need a clear start and end, and where the client needs immediate feedback.

-   **Client**: A node that sends a request and waits for a response.
-   **Server**: A node that receives a request, performs a computation, and sends a response.
-   **Service Definitions**: Defined by `.srv` files, specifying the request and response message types.

### Actions

**Actions** are a high-level communication type designed for long-running, goal-oriented tasks. They extend the service concept by providing continuous feedback about the goal's progress and allowing preemption (canceling a goal before it's completed). Actions are particularly useful for tasks like navigating to a specific location or moving a robotic arm to a target pose.

-   **Action Client**: A node that sends a goal request, receives continuous feedback, and eventually a result.
-   **Action Server**: A node that accepts goal requests, provides feedback on progress, and sends a result upon completion.
-   **Action Definitions**: Defined by `.action` files, specifying the goal, feedback, and result message types.

## Step-by-Step Lab

This chapter will have an accompanying lab to demonstrate the concepts of Nodes, Topics, Services, and Actions. The lab will involve creating simple ROS 2 packages in Python for:
1.  **Publisher-Subscriber**: A node publishing a "hello world" message and another node subscribing to it.
2.  **Service Client-Server**: A client requesting a number addition from a server, and the server returning the sum.
3.  **Action Client-Server**: An action client requesting a countdown from an action server, with the server providing feedback on each count.

### Hardware/Cloud Alternative

All labs in this chapter will be runnable on a local Ubuntu 22.04 environment with ROS 2 Humble installed. No specific hardware or cloud resources are required.

## Code Examples

Examples will be provided in Python, demonstrating how to implement each core concept using `rclpy`.

## Summary

ROS 2 provides a robust and modular framework for robotics development through its core communication mechanisms: Nodes, Topics, Services, and Actions. Understanding these concepts is fundamental to building scalable and distributed robot applications. Nodes encapsulate specific functionalities, Topics enable asynchronous data streaming, Services facilitate synchronous request-response interactions, and Actions handle long-running, goal-oriented tasks with progress feedback.

## Assessment / Mini Project

1.  **Conceptual Question**: Explain a scenario where using a ROS 2 Action is more appropriate than using a ROS 2 Service.
2.  **Coding Challenge**: Modify the publisher-subscriber lab to publish custom messages containing a timestamp and a string, and have the subscriber log these messages.
3.  **Design Task**: Propose a ROS 2 architecture (nodes, topics, services, actions) for a robot tasked with picking up a specific object from a table.
