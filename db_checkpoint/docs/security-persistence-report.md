# Security and Persistence Report

## Database schema

The application uses SQLite through SQLAlchemy. `database.py` configures the database at `sqlite:///./app.db`, creates a session per request with `get_db()`, and closes that session in a `finally` block. `Base.metadata.create_all(bind=engine)` is called when `main.py` is imported.

The persistence model has three tables:

- **`users`**: `id` primary key, unique non-null `email`, non-null `password_hash`, and `created_at`.
- **`conversations`**: `id` primary key, non-null `user_id` foreign key to `users.id`, non-null `title`, `created_at`, and `tokens_used`. A user has many conversations.
- **`messages`**: `id` primary key, non-null `conversation_id` foreign key to `conversations.id`, non-null `role`, non-null text `content`, and `created_at`. A conversation has many messages.

The foreign keys establish the relationship chain `User -> Conversation -> Message`. The model relationships are configured with `back_populates`; the application does not currently configure cascade deletion or database-level foreign-key enforcement.

## Authentication flow

1. `POST /signup` validates the email and password shape with `UserCreate`.
2. `create_user` hashes the password with bcrypt, rejects a duplicate email, stores the user, and returns a JWT.
3. `POST /login` finds the user by email and verifies the bcrypt hash. On success, it creates a JWT with the user ID in the `sub` claim.
4. `get_current_user` obtains a bearer token through `OAuth2PasswordBearer`, decodes it with the configured HS256 secret, checks the expiration, converts `sub` to an integer, and loads that `User` from the database.
5. The `/chat` route depends on `get_current_user`, so requests without a valid, non-expired token are rejected before chat persistence occurs.

Tokens expire after 30 minutes. The signing secret is loaded from `.env` and the application refuses to start when it is absent.

## Ownership rule

The security invariant is:

> A user may create, read, update, or append messages only for a conversation whose `conversations.user_id` equals the authenticated user's `users.id`.

Ownership must be checked in the database query that selects the conversation, not inferred from a client-provided conversation ID. For example, a protected lookup must include both predicates:

```python
conversation = db.scalar(
    select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id,
    )
)
```

The current write path does not fully enforce this rule. `/chat` accepts `session_id` from the request, and `create_conversation` selects a conversation by ID alone. Therefore, a user who learns another user's conversation ID could append messages to that conversation. There is no conversation-read endpoint in the current router, but the same ownership predicate is required for any future read endpoint.

## Private-data protection test

This regression test expresses the required persistence boundary: a conversation owned by one user must not be returned when queried in the context of another user. It should be placed in a pytest test module after adding the ownership-filtered repository/service query.

```python
from sqlalchemy import select

from models import Conversation, User


def test_user_cannot_access_another_users_conversation(db):
    owner = User(email="owner@example.com", password_hash="hash")
    other_user = User(email="other@example.com", password_hash="hash")
    db.add_all([owner, other_user])
    db.commit()
    db.refresh(owner)
    db.refresh(other_user)

    conversation = Conversation(user_id=owner.id, title="Private")
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    result = db.scalar(
        select(Conversation).where(
            Conversation.id == conversation.id,
            Conversation.user_id == other_user.id,
        )
    )

    assert result is None
```

This test proves the ownership predicate used by protected persistence operations. In the current codebase, the equivalent unfiltered lookup in `create_conversation` would not satisfy the invariant; that function and any future conversation reads should apply the same `user_id` condition and return an authorization error when the filtered lookup finds nothing.
