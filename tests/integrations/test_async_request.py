"""
Test the RequestConfiguration plumbing, which underpins the integrations'
handling of request-specific data in async contexts
"""
import asyncio
import pytest

import bugsnag
from bugsnag.configuration import RequestConfiguration


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_async_task_metadata():
    bugsnag.configure_request(wins={'total': 3, 'last': 2})

    async def coro():
        bugsnag.configure_request(wins={'total': 1, 'last': 1})

    asyncio.ensure_future(coro())
    data = RequestConfiguration.get_instance().wins

    assert data['total'] == 3
    assert data['last'] == 2


async def test_async_context_storage():
    async def slow_crash():
        bugsnag.configure_request(local_data={'apples': 1})
        await asyncio.sleep(1)
        data = RequestConfiguration.get_instance().local_data
        assert data['apples'] == 1

    async def other_func():
        bugsnag.configure_request(local_data={'apples': 4})

    await asyncio.gather(slow_crash(), other_func())
