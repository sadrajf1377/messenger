

📨 Messenger - A Real-Time Group Chat System with Django Channels
Messenger is a scalable, real-time group chat application built with Django, Django Channels, and WebSockets, providing instant communication capabilities between users. It supports dynamic group management, real-time messaging, file attachments, message history pagination, and live event broadcasting — all integrated seamlessly with a persistent backend.

Designed for modern web applications that demand fast, real-time interactions and clean architecture.

🚀 Key Features
🔗 Real-Time Messaging: Bi-directional communication using Django Channels & WebSockets.

👥 Dynamic Group Creation: Users can create chat groups, add members, and see updates in real-time.

🧠 Smart WebSocket Management: Each group maintains its own WebSocket channel to ensure message isolation.

📦 Message History Pagination: Chat messages are lazily loaded in batches (e.g., 20 at a time), improving performance and UX.

📁 File Attachments: Supports file uploads directly within messages.

🔔 Instant Notifications: Events such as joining, leaving, or creating groups are broadcast live to all affected users.

⚙️ Persistent Storage: All messages, groups, and notifications are stored in a relational database.

📱 Clean UI/UX: A responsive frontend with real-time DOM updates, ensuring a smooth user experience.

🧩 Architecture Overview
The system is built on the Django ecosystem with the addition of asynchronous capabilities provided by Django Channels. Each user’s active group subscriptions are mapped to separate WebSocket connections. Key architectural components include:

Channel Layers: Used for inter-process communication (With Django's In Memory Caching).

Consumers: synchronous WebSocket consumers manage individual group logic.

Frontend Layer: JS-based WebSocket clients handle dynamic DOM updates and group-specific message flows.

Database Models: Track users, groups, messages, file attachments, and system notifications,sqlite3 is used for data storage.

you can pull it's image from here -> sadrajaf77/chat_platform:latest
