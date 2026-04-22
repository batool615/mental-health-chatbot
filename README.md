# Wanees Mental Health Chatbot

## Project Description
Wanees is an AI-powered mental health chatbot application designed to support users by listening to their thoughts, providing empathetic responses, and monitoring their emotional states. The application supports natural language interaction, mood tracking via image selections, and persists all data safely using a robust, SQLAlchemy-managed MySQL database.

## Database Schema

The database relies on **MySQL** (Database: `mental_chatbot`). Below is the structured schema for the tables used by the application:

### 1. `conversations`
Stores the chat history between the user and the Wanees chatbot.
| Column         | Type       | Description                                  |
| -------------- | ---------- | -------------------------------------------- |
| `id`           | Integer    | Primary Key, Auto-incremented                |
| `user_message` | Text       | The user's text input to the chatbot         |
| `bot_response` | Text       | The AI-generated response from Wanees        |
| `timestamp`    | DateTime   | Time the message was recorded (default: now) |

### 2. `image_selections`
Logs the visual choices made by users to determine and track their mood state.
| Column         | Type         | Description                                    |
| -------------- | ------------ | ---------------------------------------------- |
| `id`           | Integer      | Primary Key, Auto-incremented                  |
| `choice_index` | Integer      | The specific index of the chosen image         |
| `mood_type`    | String(50)   | Assessed mood (e.g., calm, stressed, neutral)  |
| `emoji`        | String(10)   | Emoji associated with the tracked mood         |
| `image_url`    | String(500)  | URL or relative path to the image              |
| `user_message` | Text         | Additional message/context provided by user    |
| `timestamp`    | DateTime     | Time of the selection (default: now)           |

## Quick Setup & Initialization

1. Update your MySQL credentials located inside `backend/init_db.py` and `backend/database.py`.
2. Execute `python backend/init_db.py` to seamlessly initialize all tables.
3. *Note:* If you have legacy `.json` files in the `data/` directory, the script will transparently migrate those over to your newly generated SQL tables!
