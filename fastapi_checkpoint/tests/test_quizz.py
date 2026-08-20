import pytest

from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio

async def test_quiz_missing_topic_returns_422():

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.post("/quizz",json={"number" : 5})
        assert response.status_code == 422
@pytest.mark.asyncio

async def test_quizz_too_many_question():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url="http://test"
        ) as client:
            response = await client.post("/quizz",json={"subject":"API","number" : 50})
            assert response.status_code == 422
