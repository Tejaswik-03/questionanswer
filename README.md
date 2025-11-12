A lightweight natural-language question-answering service that extracts answers from member-related messages.
Given a user’s question (e.g., “When is Layla planning her trip to London?”), the API searches all available public messages, identifies relevant context, and returns the best possible answer.

**Features**

Extracts member names from natural-language questions

Searches public messages for relevant information

Uses a real public API as the data source

Returns clear, human-readable answers

Provides fallback responses when no match is found

**Public API used:**

GET https://november7-730026606190.europe-west1.run.app/messages


**How It Works**

Parse question → detect member names, keywords, and context

Fetch messages → retrieve all data from the provided public API

Match content → find entries related to the question

Extract details → dates, places, counts, or descriptive info

Return answer → best match or fallback

**Built With**

Python

FastAPI – web framework

Uvicorn – ASGI server

Requests – external API client

python-dotenv – environment variable management
**
install everything:**

pip install -r requirements.txt
Installation
# Clone the repository
git clone <your-repository-url>
cd questionanswer

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Mac/Linux
# or
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

3. Run the Server
uvicorn app:app --reload


**The API will run at:**

Swagger UI: http://127.0.0.1:8000/docs

Root endpoint: http://127.0.0.1:8000

Usage

**Main endpoint:**

GET /ask?question=YOUR_QUESTION

**Alternative Approaches Considered**

Several options were explored before choosing the final design:

1.** Embedding-Based Semantic Search**

Use vector embeddings and cosine similarity to match questions with messages.
More accurate but requires ML models and more complex deployment.

2**. Custom NLP Models**

Train classifiers or entity extractors to understand intents (travel, bookings, preferences).
Too heavy for the small dataset provided.

**3. Rule-Based Parsing**

Manually define rules for keywords, dates, names, and actions.
Reliable but time-consuming to maintain.

4. LLM-Based Retrieval

Send question + messages to an LLM for inference.
Extremely accurate but not allowed because the service must run standalone.

**Final choice:**
A lightweight keyword-based matching system — simple, fast, and deployable.


**Data Insights**

A few observations from analyzing the dataset:

Contact information is updated frequently, sometimes multiple times by the same user.

Some example questions cannot be answered because the dataset lacks that information (e.g., car ownership).

Many messages are preferences, not concrete facts (e.g., “I prefer aisle seats”).

Time references can be vague, such as “this Friday” without a clear date.

Users often have long message histories, allowing preference inference but requiring careful matching.
