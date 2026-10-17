import json
import os
import sys
from decimal import Decimal
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import lambda_function  # noqa: E402


def make_fake_table(count):
    table = MagicMock()
    table.update_item.return_value = {"Attributes": {"count": Decimal(count)}}
    return table


def test_returns_200_and_new_count():
    fake = make_fake_table(5)
    with patch.object(lambda_function, "get_table", return_value=fake):
        result = lambda_function.lambda_handler({}, None)

    assert result["statusCode"] == 200
    assert json.loads(result["body"]) == {"count": 5}


def test_increments_the_visits_item():
    fake = make_fake_table(1)
    with patch.object(lambda_function, "get_table", return_value=fake):
        lambda_function.lambda_handler({}, None)

    kwargs = fake.update_item.call_args.kwargs
    assert kwargs["Key"] == {"id": "visits"}
    assert kwargs["ExpressionAttributeValues"] == {":inc": 1}